
import types
from math import ceil
import logging
import warnings

try:
    set
except NameError: # Python 2.3
    from sets import Set as set

import cherrypy
try:
    import sqlobject
except ImportError:
    sqlobject = None

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

import turbogears
from turbogears.controllers import redirect
from turbogears.decorator import weak_signature_decorator
from turbogears.view import variable_providers
from formencode.variabledecode import variable_encode
from turbogears.widgets import PaginateDataGrid
from turbogears.util import add_tg_args

log = logging.getLogger("turbogears.paginate")


# lists of databases that lack support for OFFSET
# this will need to be updated periodically as modules change
_so_no_offset = 'mssql maxdb sybase'.split()
_sa_no_offset = 'mssql maxdb access'.split()

# this is a global that is set the first time paginate() is called
_simulate_offset = None

# these are helper classes for getting data that has no table column
class attrwrapper:
    """Helper class for accessing objec attributes."""
    def __init__(self, name):
        self.name = name
    def __call__(self, obj):
        for name in self.name.split('.'):
            obj = getattr(obj, name)
        return obj

class itemwrapper:
    """Helper class for dicitionary access."""
    def __init__(self, name):
        self.name = name
    def __call__(self, obj):
        return obj[self.name]


def paginate(var_name, default_order='', default_reversed=None, limit=10,
            max_limit=0, allow_limit_override=None, max_pages=5,
            max_sort=1000, dynamic_limit=None):
    """The famous TurboGears paginate decorator.

    @param var_name: The variable name that the paginate decorator will try
    to control. This key must be present in the dictionnary returned from your
    controller in order for the paginate decorator to be able to handle it.
    @type var_name: string

    @param default_order: The column name(s) that will be used to orde
    pagination results. Due to the way pagination is implemented specifying a
    default_order will override any result ordering performed in the controller.
    @type default_order: string or a list of strings. Any string starting with
    "-" (minus sign) indicates a reverse order for that field/column.

    @param default_reversed: Deprecated, use default_order with minus sign.
    @type default_reversed: Boolean

    @param limit: The hard-coded limit that the paginate decorator will impose
    on the number of "var_name" to display at the same time. This value can be
    overridden by the use of the dynamic_limit keyword argument.
    @type limit: integer

    @param max_limit: The maximum number to which the imposed limit can be
    increased using the "var_name"_tgp_limit keyword argument in the URL.
    If this is set to 0, no dynamic change at all will be allowed;
    if it is set to None, any change will be allowed.
    @type max_limit: int

    @param allow_limit_override: Deprecated, use max_limit.
    @type allow_limit_override: Boolean

    @param max_pages: Used to generate the tg.paginate.pages variable. If the
    page count is larger than max_pages, tg.paginate.pages will only contain
    the page numbers surrounding the current page at a distance of max_pages/2.
    A zero value means that all pages will be shown, no matter how much.
    @type max_pages: integer

    @param max_sort: The maximum number of records that will be sorted in
    memory if the data cannot be sorted using SQL. If set to 0, sorting in
    memory will never be performed; if set to None, no limit will be imposed.
    @type max_sort: integer

    @param dynamic_limit: If specified, this parameter must be the name
    of a key present in the dictionary returned by your decorated
    controller. The value found for this key will be used as the limit
    for our pagination and will override the other settings, the hard-coded
    one declared in the decorator itself AND the URL parameter one.
    This enables the programmer to store a limit settings inside the
    application preferences and then let the user manage it.
    @type dynamic_limit: string

    """

    if default_reversed is not None:
        warnings.warn("default_reversed is deprecated."
            " Use default_order='-field' to indicate"
            " default reversed order, or"
            " default_order=['field1', '-field2, 'field3']"
            " for multiple fields.", DeprecationWarning, 2)
    if allow_limit_override is not None:
        warnings.warn("allow_limit_override is deprecated."
            " Use max_limit to specify an upper bound for limit.",
            DeprecationWarning, 2)

    def entangle(func):

        get = turbogears.config.get

        def decorated(func, *args, **kw):

            def kwpop(name, default=None):
                return kw.pop(var_name + '_tgp_' + name,
                    kw.pop('tg_paginate_' + name, default))

            page = kwpop('no')
            if page is None:
                page = 1
            elif page == 'last':
                page = None
            else:
                try:
                    page = int(page)
                    if page < 1:
                        raise ValueError
                except (TypeError, ValueError):
                    page = 1
                    if get('paginate.redirect_on_out_of_range'):
                        cherrypy.request.params[var_name + '_tgp_no'] = page
                        redirect(cherrypy.request.path_info, cherrypy.request.params)

            try:
                limit_ = int(kwpop('limit'))
                if max_limit is not None and not (
                        allow_limit_override and max_limit == 0):
                    if max_limit <= 0:
                        raise ValueError
                    limit_ = min(limit_, max_limit)
            except (TypeError, ValueError):
                limit_ = limit
            order = kwpop('order')
            ordering = kwpop('ordering')

            log.debug("paginate params: page=%s, limit=%s, order=%s",
                page, limit_, order)

            # get the output from the decorated function
            output = func(*args, **kw)
            if not isinstance(output, dict):
                return output

            try:
                var_data = output[var_name]
            except KeyError:
                raise KeyError("paginate: var_name"
                    " (%s) not found in output dict" % var_name)
            if not hasattr(var_data, '__getitem__') and callable(var_data):
                # e.g. SQLAlchemy query class
                var_data = var_data()
                if not hasattr(var_data, '__getitem__'):
                    raise TypeError('Paginate variable is not a sequence')

            if dynamic_limit:
                try:
                    dyn_limit = output[dynamic_limit]
                except KeyError:
                    raise KeyError("paginate: dynamic_limit"
                        " (%s) not found in output dict" % dynamic_limit)
                limit_ = dyn_limit

            if ordering:
                ordering = str(ordering).split(',')
            else:
                ordering = default_order or []
                if isinstance(ordering, basestring):
                    # adapt old style default_order to new style
                    if default_reversed:
                        ordering = "-" + ordering
                    ordering = [ordering]
                elif default_reversed:
                    raise ValueError("paginate: default_reversed (deprecated)"
                        " only allowed when default_order is a basestring")

            if order:
                order = str(order)
                log.debug('paginate: ordering was %s, sort is %s',
                    ordering, order)
                sort_ordering(ordering, order)
            log.debug('paginate: ordering is %s', ordering)

            try:
                row_count = len(var_data)
            except TypeError:
                try: # SQL query
                    row_count = var_data.count() or 0
                except AttributeError: # other iterator
                    var_data = list(var_data)
                    row_count = len(var_data)

            if ordering:
                var_data = sort_data(var_data, ordering,
                    max_sort is None or 0 < row_count <= max_sort)

            # If limit is zero then return all our rows
            if not limit_:
                limit_ = row_count or 1

            page_count = int(ceil(float(row_count)/limit_))

            if page is None:
                page = max(page_count, 1)
                if get('paginate.redirect_on_last_page'):
                    cherrypy.request.params[var_name + '_tgp_no'] = page
                    redirect(cherrypy.request.path_info, cherrypy.request.params)
            elif page > page_count:
                page = max(page_count, 1)
                if get('paginate.redirect_on_out_of_range'):
                    cherrypy.request.params[var_name + '_tgp_no'] = page
                    redirect(cherrypy.request.path_info, cherrypy.request.params)

            offset = (page-1) * limit_

            pages_to_show = _select_pages_to_show(page, page_count, max_pages)

            # remove pagination parameters from request
            input_values =  variable_encode(cherrypy.request.params.copy())
            input_values.pop('self', None)
            for input_key in input_values.keys():
                if (input_key.startswith(var_name + '_tgp_') or
                        input_key.startswith('tg_paginate_')):
                    del input_values[input_key]

            paginate_instance = Paginate(
                current_page=page,
                limit=limit_,
                pages=pages_to_show,
                page_count=page_count,
                input_values=input_values,
                order=order,
                ordering=ordering,
                row_count=row_count,
                var_name=var_name)

            cherrypy.request.paginate = paginate_instance
            if not hasattr(cherrypy.request, 'paginates'):
                cherrypy.request.paginates = dict()
            cherrypy.request.paginates[var_name] = paginate_instance

            # we replace the var with the sliced one
            endpoint = offset + limit_
            log.debug("paginate: slicing data between %d and %d",
                offset, endpoint)

            global _simulate_offset
            if _simulate_offset is None:
                _simulate_offset = get('paginate.simulate_offset', None)
                if _simulate_offset is None:
                    _simulate_offset = False
                    so_db = get('sqlobject.dburi', 'NOMATCH:').split(':', 1)[0]
                    sa_db = get('sqlalchemy.dburi', 'NOMATCH:').split(':', 1)[0]
                    if so_db in _so_no_offset or sa_db in _sa_no_offset:
                        _simulate_offset = True
                        log.warning("paginate: simulating OFFSET,"
                            " paginate may be slow"
                            " (disable with paginate.simulate_offset=False)")

            if _simulate_offset:
                var_data = iter(var_data[:endpoint])
                # skip over the number of records specified by offset
                for i in xrange(offset):
                    var_data.next()
                # return the records that remain
                output[var_name] = list(var_data)
            else:
                try:
                    output[var_name] = var_data[offset:endpoint]
                except TypeError:
                    for i in xrange(offset):
                        var_data.next()
                    output[var_name] = [var_data.next()
                        for i in xrange(offset, endpoint)]

            return output

        if not get('tg.strict_parameters', False):
            # add hint that paginate parameters shall be left intact
            args = set()
            for arg in 'no', 'limit', 'order', 'ordering':
                args.add(var_name + '_tgp_' + arg)
                args.add('tg_paginate_' + arg)
            add_tg_args(func, args)
        return decorated

    return weak_signature_decorator(entangle)


def _paginate_var_provider(d):
    """Auxiliary function for providing the paginate variable."""
    paginate = getattr(cherrypy.request, 'paginate', None)
    if paginate:
        d.update(dict(paginate=paginate))
    paginates = getattr(cherrypy.request, 'paginates', None)
    if paginates:
        d.update(dict(paginates=paginates))
variable_providers.append(_paginate_var_provider)


class Paginate:
    """Class for paginate variable provider."""

    def __init__(self, current_page, pages, page_count, input_values,
                 limit, order, ordering, row_count, var_name):

        self.var_name = var_name
        self.pages = pages
        self.limit = limit
        self.page_count = page_count
        self.current_page = current_page
        self.input_values = input_values
        self.order = order
        self.ordering = ordering
        self.row_count = row_count
        self.first_item = page_count and ((current_page - 1) * limit + 1) or 0
        self.last_item = min(current_page * limit, row_count)

        self.reversed = ordering and ordering[0][0] == '-'

        # If ordering is empty, don't add it.
        input_values = {var_name + '_tgp_limit': limit}
        if ordering:
            input_values[var_name + '_tgp_ordering'] = ','.join(ordering)
        self.input_values.update(input_values)

        if current_page < page_count:
            self.input_values.update({
                var_name + '_tgp_no': current_page + 1,
                var_name + '_tgp_limit': limit
            })
            self.href_next = turbogears.url(
                cherrypy.request.path_info, self.input_values)
            self.input_values.update({
                var_name + '_tgp_no': 'last',
                var_name + '_tgp_limit': limit
            })
            self.href_last = turbogears.url(
                cherrypy.request.path_info, self.input_values)
        else:
            self.href_next = None
            self.href_last = None

        if current_page > 1:
            self.input_values.update({
                var_name + '_tgp_no': current_page - 1,
                var_name + '_tgp_limit': limit
            })
            self.href_prev = turbogears.url(
                cherrypy.request.path_info, self.input_values)
            self.input_values.update({
                var_name + '_tgp_no': 1,
                var_name + '_tgp_limit': limit
            })
            self.href_first = turbogears.url(
                cherrypy.request.path_info, self.input_values)
        else:
            self.href_prev = None
            self.href_first = None

    def get_href(self, page, order=None, reverse_order=None):
        # Note that reverse_order is not used.  It should be cleaned up here
        # and in the template.  I'm not removing it now because I don't want
        # to break the API.
        order = order or None
        input_values = self.input_values.copy()
        input_values[self.var_name + '_tgp_no'] = page
        if order:
            input_values[ self.var_name + '_tgp_order'] = order
        return turbogears.url('', input_values)


def _select_pages_to_show(current_page, page_count, max_pages=None):
    """Auxiliary function for getting the range of pages to show."""
    if max_pages is not None and max_pages > 0:
        start = current_page - (max_pages // 2) - (max_pages % 2) + 1
        end = start + max_pages - 1
        if start < 1:
            start, end = 1, min(page_count, max_pages)
        elif end > page_count:
            start, end = max(1, page_count - max_pages + 1), page_count
    else:
        start, end = 1, page_count
    return xrange(start, end + 1)


# Auxiliary functions for dealing with columns and SQL

def sort_ordering(ordering, sort_name):
    """Rearrange ordering based on sort_name."""
    try:
        index = ordering.index(sort_name)
    except ValueError:
        try:
            index = ordering.index('-' + sort_name)
        except ValueError:
            ordering.insert(0, sort_name)
        else:
            del ordering[index]
            ordering.insert(0, (index and '-' or '') + sort_name)
    else:
        del ordering[index]
        ordering.insert(0, (not index and '-' or '') + sort_name)

def sqlalchemy_get_column(colname, var_data):
    """Return a column from sqlalchemy var_data based on colname."""
    try:
        mapper = var_data.mapper
    except AttributeError: # SQLAlchemy >= 0.5
        try:
            mapper = var_data._mapper_zero()
        except AttributeError: # SQLAlchemy <= 0.4 and SelectResullts
            mapper = var_data._query.mapper
    propnames = colname.split('.')
    colname = propnames.pop()
    for propname in propnames:
        prop = mapper.get_property(
            propname, resolve_synonyms=True, raiseerr=False)
        if not prop:
            break
        mapper = prop.mapper
    if mapper.column_prefix:
        # for SQLAlchemy <= 0.4.0 we may need to remove the column_prefix
        return getattr(mapper.c, colname,
            getattr(mapper.c, colname[len(mapper.column_prefix):], None))
    else:
        return getattr(mapper.c, colname, None)

def sqlobject_get_column(colname, var_data):
    """Return a column from sqlobject var_data based on colname."""
    return getattr(var_data.sourceClass.q, colname, None)

def sql_get_column(colname, var_data):
    """Return a column from var_data based on colname."""
    if sqlalchemy:
        try:
            return sqlalchemy_get_column(colname, var_data)
        except AttributeError:
            pass
    if sqlobject:
        try:
            return sqlobject_get_column(colname, var_data)
        except AttributeError:
            pass
    raise TypeError('Cannot find columns of paginate variable')

def sqlalchemy_order_col(col, descending=False):
    """Return an sqlalchemy ordered column for col."""
    if descending:
        return sqlalchemy.sql.desc(col)
    else:
        return sqlalchemy.sql.asc(col)

def sqlobject_order_col(col, descending=False):
    """Return an sqlobject ordered column for col."""
    if descending:
        return sqlobject.DESC(col)
    else:
        return col

def sql_order_col(col, ascending=True):
    """Return an ordered column for col."""
    if sqlalchemy and isinstance(col, sqlalchemy.sql.ColumnElement):
        return sqlalchemy_order_col(col, ascending)
    elif sqlobject and isinstance(col, types.InstanceType):
        # Sadly, there is no better way to check for sqlobject col type
        return sqlobject_order_col(col, ascending)
    raise TypeError("Expected Column, but got %s" % type(col))

def sort_data(data, ordering, in_memory=True):
    """Sort data based on ordering.

    Tries to sort the data using SQL whenever possible,
    otherwise sorts the data as list in memory unless in_memory is false.

    """
    try:
        order_by = data.order_by # SQLAlchemy
        get_column, order_col = sqlalchemy_get_column, sqlalchemy_order_col
    except AttributeError:
        try:
            order_by = data.orderBy # SQLObject
            get_column, order_col = sqlobject_get_column, sqlobject_order_col
        except AttributeError:
            order_by = None
    order_cols = []
    key_cols = []
    num_ascending = num_descending = 0
    for order in ordering:
        if order[0] == '-':
            order = order[1:]
            descending = True
        else:
            descending = False
        if order_by:
            col = get_column(order, data)
            if col is not None:
                order_cols.append(order_col(col, descending))
                continue
        if not order_cols:
            key_cols.append((order, descending))
            if descending:
                num_descending += 1
            else:
                num_ascending += 1
    if order_by and order_cols:
        data = order_by(order_cols)
    if key_cols:
        if in_memory:
            data = list(data)
            if not data:
                return data
            wrapper = isinstance(data[0], dict) and itemwrapper or attrwrapper
            keys = [(wrapper(col[0]), col[1]) for col in key_cols]
            if num_ascending == 0 or num_descending == 0:
                reverse = num_ascending == 0
                keys = [key[0] for key in keys]
                if len(key_cols) == 1:
                    key = keys[0]
                else:
                    key = lambda row: [key(row) for key in keys]
            else:
                reverse = num_descending > num_ascending
                def reverse_key(key, descending):
                    if reverse == descending:
                        return key
                    else:
                        keys = map(key, data)
                        try:
                            keys = list(set(keys))
                        except TypeError: # unhashable
                            keys.sort()
                            return lambda row: -keys.index(key(row))
                        else:
                            keys.sort()
                            keys = dict([(k, -n) for n, k in enumerate(keys)])
                            return lambda row: keys[key(row)]
                keys = [reverse_key(*key) for key in keys]
                key = lambda row: [key(row) for key in keys]
            try:
                data.sort(key=key, reverse=reverse)
            except TypeError: # Python 2.3
                if reverse:
                    cmpkey = lambda row1, row2: cmp(key(row2), key(row1))
                else:
                    cmpkey = lambda row1, row2: cmp(key(row1), key(row2))
                data.sort(cmpkey)
        else:
            log.debug("paginate: sorting in memory not allowed")
    return data
