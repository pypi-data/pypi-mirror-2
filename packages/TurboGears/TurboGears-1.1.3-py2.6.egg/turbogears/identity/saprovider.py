import logging

from turbogears import config, identity
from turbogears.database import bind_metadata, session
from turbogears.util import load_class

from sqlalchemy.orm import class_mapper
try:
    from sqlalchemy.exc import IntegrityError
except ImportError: # SQLAlchemy < 0.5
    from sqlalchemy.exceptions import IntegrityError


log = logging.getLogger("turbogears.identity.saprovider")


# Global class references --
# these will be set when the provider is initialized.
user_class = None
group_class = None
permission_class = None
visit_class = None


class SqlAlchemyIdentity(object):
    """Identity that uses a model from a database (via SQLAlchemy)."""

    def __init__(self, visit_key=None, user=None):
        self.visit_key = visit_key
        if user:
            self._user = user
            if visit_key is not None:
                self.login()

    @property
    def user(self):
        """Get user instance for this identity."""
        try:
            return self._user
        except AttributeError:
            # User hasn't already been set
            pass
        # Attempt to load the user. After this code executes, there *will* be
        # a _user attribute, even if the value is None.
        visit = self.visit_link
        self._user = visit and session.query(user_class).get(visit.user_id)
        return self._user

    @property
    def user_name(self):
        """Get user name of this identity."""
        if not self.user:
            return None
        return self.user.user_name

    @property
    def user_id(self):
        """Get user id of this identity."""
        if not self.user:
            return None
        return self.user.user_id

    @property
    def anonymous(self):
        """Return true if not logged in."""
        return not self.user

    @property
    def permissions(self):
        """Get set of permission names of this identity."""
        try:
            return self._permissions
        except AttributeError:
            # Permissions haven't been computed yet
            pass
        if not self.user:
            self._permissions = frozenset()
        else:
            self._permissions = frozenset(
                p.permission_name for p in self.user.permissions)
        return self._permissions

    @property
    def groups(self):
        """Get set of group names of this identity."""
        try:
            return self._groups
        except AttributeError:
            # Groups haven't been computed yet
            pass
        if not self.user:
            self._groups = frozenset()
        else:
            self._groups = frozenset(g.group_name for g in self.user.groups)
        return self._groups

    @property
    def group_ids(self):
        """Get set of group IDs of this identity."""
        try:
            return self._group_ids
        except AttributeError:
            # Groups haven't been computed yet
            pass
        if not self.user:
            self._group_ids = frozenset()
        else:
            self._group_ids = frozenset(g.group_id for g in self.user.groups)
        return self._group_ids

    @property
    def visit_link(self):
        """Get the visit link to this identity."""
        if self.visit_key is None:
            return None
        return session.query(visit_class).filter_by(
            visit_key=self.visit_key).first()

    @property
    def login_url(self):
        """Get the URL for the login page."""
        return identity.get_failure_url()

    def login(self):
        """Set the link between this identity and the visit."""
        visit = self.visit_link
        if not visit:
            visit = visit_class()
            visit.visit_key = self.visit_key
            session.add(visit)
        visit.user_id = self._user.user_id
        try:
            session.flush()
        except IntegrityError:
            visit = self.visit_link
            if not visit:
                raise
            visit.user_id = self._user.user_id
            session.flush()

    def logout(self):
        """Remove the link between this identity and the visit."""
        visit = self.visit_link
        if visit:
            session.delete(visit)
            session.flush()
        # Clear the current identity
        identity.set_current_identity(SqlAlchemyIdentity())


class SqlAlchemyIdentityProvider(object):
    """IdentityProvider that uses a model from a database (via SQLAlchemy)."""

    def __init__(self):
        super(SqlAlchemyIdentityProvider, self).__init__()
        glob_ns = globals()

        for classname in ('user', 'group', 'permission', 'visit'):
            default_classname = '.TG_' + (classname == 'visit'
                and 'VisitIdentity' or classname.capitalize())
            class_path = config.get("identity.saprovider.model.%s" % classname,
                __name__ + default_classname)
            class_ = load_class(class_path)
            if class_:
                log.info('Successfully loaded "%s".', class_path)
                glob_ns['%s_class' % classname] = class_
            else:
                log.error('Could not load class "%s". Check '
                    'identity.saprovider.model.%s setting', class_path, classname)

    def encrypt_password(self, password):
        # Default encryption algorithm is to use plain text passwords
        algorithm = config.get("identity.saprovider.encryption_algorithm", None)
        return identity.encrypt_pw_with_algorithm(algorithm, password)

    def create_provider_model(self):
        """Create the database tables if they don't already exist."""
        bind_metadata()
        class_mapper(user_class).local_table.create(checkfirst=True)
        class_mapper(group_class).local_table.create(checkfirst=True)
        class_mapper(permission_class).local_table.create(checkfirst=True)
        class_mapper(visit_class).local_table.create(checkfirst=True)

    def validate_identity(self, user_name, password, visit_key):
        """Validate the identity represented by user_name using the password.

        Must return either None if the credentials weren't valid or an object
        with the following properties:
            user_name: original user name
            user: a provider dependent object (TG_User or similar)
            groups: a set of group names
            permissions: a set of permission names

        """
        user = session.query(user_class).filter_by(
                user_name=user_name).first()

        if not user:
            log.warning("No such user: %s", user_name)
            return None

        if not self.validate_password(user, user_name, password):
            log.info("Passwords don't match for user: %s", user_name)
            return None

        log.info("Associating user (%s) with visit (%s)",
                user_name, visit_key)
        return SqlAlchemyIdentity(visit_key, user)

    def validate_password(self, user, user_name, password):
        """Check the user_name and password against existing credentials.

        Note: user_name is not used here, but is required by external
        password validation schemes that might override this method.
        If you use SqlAlchemyIdentityProvider, but want to check the passwords
        against an external source (i.e. PAM, LDAP, Windows domain, etc),
        subclass SqlAlchemyIdentityProvider, and override this method.

        """
        return user.password == self.encrypt_password(password)

    def load_identity(self, visit_key):
        """Lookup the principal represented by user_name.

        Return None if there is no principal for the given user ID.

        Must return an object with the following properties:
            user_name: original user name
            user: a provider dependent object (TG_User or similar)
            groups: a set of group names
            permissions: a set of permission names

        """
        return SqlAlchemyIdentity(visit_key)

    def anonymous_identity(self):
        """Return anonymous identity.

        Must return an object with the following properties:
            user_name: original user name
            user: a provider dependent object (TG_User or similar)
            groups: a set of group names
            permissions: a set of permission names

        """
        return SqlAlchemyIdentity()

    def authenticated_identity(self, user):
        """Construct Identity object for users with no visit_key."""
        return SqlAlchemyIdentity(user=user)
