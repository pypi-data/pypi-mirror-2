import dispatch
from turbogears import config
from turbogears.util import get_model
try:
    from sqlalchemy import MetaData, exceptions, Table, String, Unicode
    from turbogears.database import metadata, get_engine
except ImportError: # if not available, complain only at run-time
    get_engine = None
else:
    try:
        from sqlalchemy import Text, UnicodeText
    except ImportError: # SQLAlchemy < 0.4.3
        Text, UnicodeText = String, Unicode

[dispatch.generic()]
def sacommand(command, args):
    pass

[sacommand.around("command and command != 'help' and not get_engine")]
def no_engine(command, args):
    print "Error: SQLAlchemy not installed."

[sacommand.when("command == 'help'")]
def help(command, args):
    print """TurboGears SQLAlchemy Helper

tg-admin sql command [options]

Available commands:
    create  Create tables
    execute Execute SQL statements
    help    Show help
    list    List tables that appear in the model
    status  Show differences between model and database
"""

[sacommand.when("command == 'create'")]
def create(command, args):
    print "Creating tables at %s" % (config.get("sqlalchemy.dburi"))
    get_engine()
    get_model()
    metadata.create_all()

[sacommand.when("command == 'list'")]
def list_(command, args):
    get_model()
    for tbl in metadata.tables.values():
        print tbl.fullname

[sacommand.when("command == 'execute'")]
def execute(command, args):
    eng = get_engine()
    for cmd in args[2:]:
        ret = eng.execute(cmd)
        try:
            print list(ret)
        except:
            # Proceed silently if the command produced no results
            pass

[sacommand.when("command == 'status'")]
def status(command, args):
    get_engine()
    get_model()
    ret = compare_metadata(metadata, MetaData(metadata.bind))
    for l in ret:
        print l
    if not ret:
        print "Database matches model"

def indent(ls):
    return ['    ' + l for l in ls]

def compare_metadata(pym, dbm):
    rc = []
    for pyt in pym.tables.values():
        try:
            dbt = Table(pyt.name, dbm, autoload=True, schema=pyt.schema)
        except exceptions.NoSuchTableError:
            rc.extend(("Create table " + pyt.fullname, ''))
        else:
            ret = compare_table(pyt, dbt)
            if ret:
                rc.append("Change table " + pyt.fullname)
                rc.extend(indent(ret) + [''])
    return rc

def compare_table(pyt, dbt):
    rc = []
    dbcols = dict([(s.lower(), s) for s in dbt.columns.keys()])
    any_pkey = bool([1 for c in dbt.columns if c.primary_key])
    for pyc in pyt.columns:
        name = pyc.name.lower()
        if dbcols.has_key(name):
            ret = compare_column(pyc, dbt.columns[dbcols[name]], any_pkey)
            if ret:
                rc.append("Change column " + pyc.name)
                rc.extend(indent(ret))
            dbcols.pop(name)
        else:
            rc.append("Add column " + pyc.name)
    for dbcol in dbcols:
        rc.append("Remove column " + dbcol)
    return rc

def compare_column(pyc, dbc, any_pkey):
    rc = []
    pyt, dbt = pyc.type, dbc.type

    # Table reflection cannot recognize Unicode, so check only for String
    if isinstance(pyt, Unicode):
        pyt = String(pyt.length)
    elif isinstance(pyt, UnicodeText):
        pyt = Text(pyt.length)

    # Check type
    if not isinstance(dbt, pyt.__class__):
        rc.append('Change type to ' + pyt.__class__.__name__)

    # Check length (for strings)
    else:
        if isinstance(pyt, String):
            if pyt.length != dbt.length:
                rc.append('Change length to ' + str(pyt.length))

    # Check primary key
    if any_pkey and dbc.primary_key != pyc.primary_key:
        rc.append(pyc.primary_key and 'Make primary key' or 'Remove primary key')

    # TODO: Check foreign keys

    # Check default
    if (dbc.default is not None and pyc.default is not None
            and dbc.default != pyc.default):
        rc.append('Change default to ' + str(pyc.default.arg))

    # Check index
    if dbc.index is not None and dbc.index != pyc.index:
        rc.append(pyc.index and 'Add index' or 'Remove index')

    return rc
