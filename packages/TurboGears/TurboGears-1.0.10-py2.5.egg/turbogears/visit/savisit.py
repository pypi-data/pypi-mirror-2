from datetime import datetime

from sqlalchemy import Table, Column, String, DateTime
from sqlalchemy.orm import class_mapper

from turbogears import config
from turbogears.database import get_engine, metadata, session, mapper
from turbogears.util import load_class
from turbogears.visit.api import BaseVisitManager, Visit

import logging
log = logging.getLogger("turbogears.identity.savisit")

visit_class = None


class SqlAlchemyVisitManager(BaseVisitManager):

    def __init__(self, timeout):
        global visit_class
        visit_class_path = config.get("visit.saprovider.model",
            "turbogears.visit.savisit.TG_Visit")
        visit_class = load_class(visit_class_path)
        if visit_class is None:
            msg = 'No visit class found for %s' % visit_class_path
            msg += ', did you run setup.py develop?'
            log.error(msg)

        get_engine()
        if visit_class is TG_Visit:
            mapper(visit_class, visits_table)
        # base-class' __init__ triggers self.create_model, so mappers need to
        # be initialized before.
        super(SqlAlchemyVisitManager, self).__init__(timeout)

    def create_model(self):
        """Create the Visit table if it doesn't already exist."""
        get_engine()
        class_mapper(visit_class).local_table.create(checkfirst=True)

    def new_visit_with_key(self, visit_key):
        created = datetime.now()
        visit = visit_class()
        visit.visit_key = visit_key
        visit.created = created
        visit.expiry = created + self.timeout
        session.flush()
        return Visit(visit_key, True)

    def visit_for_key(self, visit_key):
        """Return the visit for this key.

        Returns None if the visit doesn't exist or has expired.

        """
        try:
            expiry = self.queue[visit_key]
        except KeyError:
            visit = visit_class.lookup_visit(visit_key)
            if not visit:
                return None
            expiry = visit.expiry
        now = datetime.now(expiry.tzinfo)
        if expiry < now:
            return None
        # Visit hasn't expired, extend it
        self.update_visit(visit_key, now + self.timeout)
        return Visit(visit_key, False)

    def update_queued_visits(self, queue):
        # TODO this should be made transactional
        table = class_mapper(visit_class).mapped_table
        # Now update each of the visits with the most recent expiry
        for visit_key, expiry in queue.items():
            log.info("updating visit (%s) to expire at %s", visit_key,
                      expiry)
            get_engine().execute(table.update(table.c.visit_key == visit_key,
                values=dict(expiry=expiry)))


# The Visit table

visits_table = Table('tg_visit', metadata,
    Column('visit_key', String(40), primary_key=True),
    Column('created', DateTime, nullable=False, default=datetime.now),
    Column('expiry', DateTime)
)


class TG_Visit(object):

    def lookup_visit(cls, visit_key):
        return Visit.get(visit_key)
    lookup_visit = classmethod(lookup_visit)
