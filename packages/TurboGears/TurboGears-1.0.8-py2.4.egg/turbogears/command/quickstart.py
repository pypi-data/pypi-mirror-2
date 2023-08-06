"""Quickstart command to generate a new project.

Quickstart takes the files from turbogears.quickstart and processes them to produce
a new, ready-to-run project.

"""

import pkg_resources
import re
import os
import os.path
import shutil
import stat
import optparse
import sys
import turbogears
from paste.script import templates, create_distro

try:
    set
except NameError: # Python 2.3
    from sets import Set as set

beginning_letter = re.compile(r"^[^a-z]*")
valid_only = re.compile(r"[^a-z0-9_]")


class TGTemplate(templates.Template):
    def run(self, command, output_dirs, vars):
        vars.setdefault('einame', vars['project'].replace('-', '_'))
        vars.setdefault('turbogearsversion',
                pkg_resources.get_distribution('turbogears').version)
        vars.setdefault('sys_executable', os.path.normpath(sys.executable))
        # define version-compatible decorator syntax
        if sys.version_info >= (2, 4):
            vars['b'] = '@'
            vars['e'] = ''
        else:
            vars['b'] = '['
            vars['e'] = ']'
        super(TGTemplate, self).run(command, output_dirs, vars)


class BaseTemplate(TGTemplate):
    egg_plugins = ["TurboGears"]
    _template_dir = pkg_resources.resource_filename(
                        "turbogears.qstemplates",
                        "qsbase"
                    )
    summary = "tg base template"
    use_cheetah = True


class TurbogearsTemplate(TGTemplate):
    required_templates = ["tgbase"]
    _template_dir = pkg_resources.resource_filename(
                            "turbogears.qstemplates",
                            "quickstart")
    summary = "web framework"
    use_cheetah = True


class TGBig(TGTemplate):
    required_templates = ["turbogears"]
    _template_dir = pkg_resources.resource_filename(
                            "turbogears.qstemplates",
                            "quickstartbig")
    summary = "For more complex projects"
    use_cheetah = True

    def post(self, command, output_dir, vars):
        packagedir = os.path.join(output_dir, vars["package"])
        controllersdir = os.path.join(packagedir, "controllers")
        controllersfile = os.path.join(packagedir, "controllers.py")
        rootfile = os.path.join(controllersdir, "root.py")
        if os.path.exists(controllersdir) and \
            os.path.exists(controllersfile):
            controllerstext = open(controllersfile).read()
            roottext = open(rootfile).read()
            from paste.script.copydir import query_interactive
            thesame = controllerstext == roottext
            if not thesame:
                print "\nYou seem to be upgrading from a smaller quickstart."
                print "There is currently a controllers package and a"
                print "controllers module, which would get confusing."
            if not command.simulate and (controllerstext == roottext
                    or query_interactive(controllersfile, rootfile,
                        controllerstext, roottext, False)):
                shutil.copyfile(controllersfile, rootfile)
                try:
                    if not os.path.exists(os.path.join(os.path.dirname(
                            os.path.abspath(controllersfile)), '.svn')):
                        raise OSError
                    command.run_command('svn', 'revert', controllersfile)
                    command.run_command('svn', 'delete', controllersfile)
                except OSError:
                    os.unlink(controllersfile)
                controllerspyc = controllersfile + "c"
                if os.path.exists(controllerspyc):
                    os.unlink(controllerspyc)


class TGWidgetTemplate(TGTemplate):
    required_templates = ["tgbase"]
    _template_dir = pkg_resources.resource_filename(
                            "turbogears.qstemplates",
                            "widget")
    summary = "TurboGears widget projects"


def get_requirement(name, pkg=None):
    dist = pkg_resources.get_distribution("TurboGears")
    for r in set(dist.requires((name,))) - set(dist.requires()):
        if r.project_name.lower() == (pkg or name):
            return r
    raise ValueError("Did not find matching %s requirement"
        " in the TurboGears setup.py:extras_require." % name)


class quickstart:
    "Implementation of quickstart."

    desc = "Create a new TurboGears project"

    name = None
    package = None
    templates = "turbogears"
    svn_repository = None
    sqlalchemy = False
    sqlobject = False
    elixir = False
    identity = False

    def __init__(self, version):
        parser = optparse.OptionParser(
                    usage="%prog quickstart [options] [project name]",
                    version="%prog " + version)
        parser.add_option("-s", "--sqlalchemy",
            help="use SQLAlchemy instead of SQLObject",
            action="store_true", dest="sqlalchemy", default = False)
        parser.add_option("-e", "--elixir",
            help="use SQLAlchemy Elixir instead of SQLObject",
            action="store_true", dest="elixir", default = False)
        parser.add_option("-o", "--sqlobject",
            help="use SQLObject instead of SQLAlchemy",
            action="store_true", dest="sqlobject", default = False)
        parser.add_option("-i", "--identity",
            help="provide Identity support",
            action="store_true", dest="identity", default = False)
        parser.add_option("-p", "--package",
            help="package name for the code",
            dest="package")
        parser.add_option("-t", "--templates",
            help="user specific templates",
            dest="templates", default = self.templates)
        parser.add_option("-r", "--svn-repository", metavar="REPOS",
            help="create project in given SVN repository",
            dest="svn_repository", default = self.svn_repository)
        parser.add_option("--dry-run",
            help="dry run (don't actually do anything)",
            action="store_true", dest="dry_run")

        options, args = parser.parse_args()
        self.__dict__.update(options.__dict__)
        if not True in [self.elixir, self.sqlalchemy, self.sqlobject]:
            self.sqlobject = True
        if self.elixir:
            self.sqlalchemy = True

        if args:
            self.name = args[0]
        self.turbogearsversion = version

    def run(self):
        "Quickstarts the new project."

        while not self.name:
            self.name = raw_input("Enter project name: ")

        while not self.package:
            package = self.name.lower()
            package = beginning_letter.sub("", package)
            package = valid_only.sub("", package)
            self.package = raw_input("Enter package name [%s]: " % package)
            if not self.package:
                self.package = package

        doidentity = self.identity
        while not doidentity:
            doidentity = raw_input("Do you need Identity "
                        "(usernames/passwords) in this project? [no] ")
            doidentity = doidentity.lower()
            if not doidentity or doidentity.startswith('n'):
                self.identity="none"
                break
            if doidentity.startswith("y"):
                doidentity = True
                break
            print "Please enter y(es) or n(o)."
            doidentity = None

        if doidentity is True:
            if self.sqlalchemy or self.elixir:
                self.identity = "sqlalchemy"
            else:
                self.identity = "sqlobject"
        self.name = pkg_resources.safe_name(self.name)

        env = pkg_resources.Environment()
        if self.name.lower() in env:
            print 'The name "%s" is already in use by' % self.name,
            for dist in env[self.name]:
                print dist
                return

        import imp
        try:
            if imp.find_module(self.package):
                print 'The package name "%s" is already in use' % self.package
                return
        except ImportError:
            pass

        if os.path.exists(self.name):
            print 'A directory called "%s" already exists. Exiting.' % self.name
            return

        command = create_distro.CreateDistroCommand("quickstart")
        cmd_args = []
        for template in self.templates.split(" "):
            cmd_args.append("--template=%s" % template)
        if self.svn_repository:
            cmd_args.append("--svn-repository=%s" % self.svn_repository)
        if self.dry_run:
            cmd_args.append("--simulate")
            cmd_args.append("-q")
        cmd_args.append(self.name)
        cmd_args.append("sqlalchemy=%s" % self.sqlalchemy)
        cmd_args.append("elixir=%s" % self.elixir)
        cmd_args.append("sqlobject=%s" % self.sqlobject)
        cmd_args.append("identity=%s" % self.identity)
        cmd_args.append("package=%s" % self.package)
        # set the exact ORM-version for the proper requirements
        # it's extracted from our own requirements, so looking
        # them up must be in sync (there must be the extras_require named sqlobject/sqlalchemy)
        if self.sqlobject:
            sqlobjectversion = str(get_requirement('sqlobject'))
            cmd_args.append("sqlobjectversion=%s" % sqlobjectversion)
        if self.sqlalchemy:
            sqlalchemyversion = str(get_requirement('sqlalchemy'))
            cmd_args.append("sqlalchemyversion=%s" % sqlalchemyversion)
        if self.elixir:
            elixirversion = str(get_requirement('future', 'elixir'))
            cmd_args.append("elixirversion=%s" % elixirversion)

        command.run(cmd_args)

        if not self.dry_run:
            os.chdir(self.name)
            if self.sqlobject:
                # Create the SQLObject history directory only when needed.
                # With paste.script it's only possible to skip files, but
                # not directories. So we are handling this manually.
                sodir = '%s/sqlobject-history' % self.package
                if not os.path.exists(sodir):
                    os.mkdir(sodir)
                try:
                    if not os.path.exists(os.path.join(os.path.dirname(
                            os.path.abspath(sodir)), '.svn')):
                        raise OSError
                    command.run_command('svn', 'add', sodir)
                except OSError:
                    pass

            startscript = "start-%s.py" % self.package
            if os.path.exists(startscript):
                oldmode = os.stat(startscript).st_mode
                os.chmod(startscript,
                        oldmode | stat.S_IXUSR)
            sys.argv = ["setup.py", "egg_info"]
            import imp
            imp.load_module("setup", *imp.find_module("setup", ["."]))

        # dirty hack to allow "empty" dirs
        for base, path, files in os.walk("./"):
            for file in files:
                if file == "empty":
                    os.remove(os.path.join(base, file))


class update:
    "Implementation of update"

    desc = "Update an existing turbogears project"
    need_project = True

    name = None
    templates = "turbogears"
    identity = False
    sqlalchemy = False
    sqlobject = True
    elixir = False

    def __init__(self, version):
        parser = optparse.OptionParser(usage="%prog update [options]",
                                       version="%prog " + version)
        parser.add_option("-s", "--sqlalchemy",
            help="use SQLAlchemy instead of SQLObject",
            action="store_true", dest="sqlalchemy", default = False)
        parser.add_option("-e", "--elixir",
            help="use SQLAlchemy Elixir instead of SQLObject",
            action="store_true", dest="elixir", default = False)
        parser.add_option("-o", "--sqlobject",
            help="use SQLObject instead of SQLAlchemy",
            action="store_true", dest="sqlobject", default = True)
        parser.add_option("-i", "--identity",
            help="provide Identity support",
            action="store_true", dest="identity", default = False)
        parser.add_option("-t", "--templates", help="user specific templates",
            dest="templates", default=self.templates)
        options, args = parser.parse_args()
        self.__dict__.update(options.__dict__)

    def run(self):
        "Updates an existing project"
        self.name = turbogears.util.get_project_name()
        self.package = turbogears.util.get_package_name()
        turbogears.command.base.load_project_config()

        if not self.sqlalchemy:
            if turbogears.config.get('sqlalchemy.dburi'):
                self.sqlalchemy = True

        if self.elixir:
            self.sqlalchemy = True
            self.sqlobject = False
        elif self.sqlalchemy:
            self.sqlobject = False
        else:
            self.sqlobject = True

        if not self.identity:
            if turbogears.config.get('identity.on'):
                self.identity = True

        if self.identity:
            if self.sqlalchemy:
                self.identity = 'sqlalchemy'
            else:
                self.identity =  'sqlobject'
        else:
            self.identity = 'none'
        currentdir = os.path.basename(os.getcwd())
        if not currentdir == self.name:
            print 'It looks like your project dir "%s" is named wrongly.' % currentdir
            print 'Please rename it to "%s".' % self.name
            return

        command = create_distro.CreateDistroCommand("update")
        cmd_args = []
        cmd_args.append("-o../")
        for template in self.templates.split(" "):
            cmd_args.append("--template=%s" % template)
        cmd_args.append(self.name)
        cmd_args.append("sqlalchemy=%s" % self.sqlalchemy)
        cmd_args.append("elixir=%s" % self.elixir)
        cmd_args.append("sqlobject=%s" % self.sqlobject)
        cmd_args.append("identity=%s" % self.identity)
        cmd_args.append("package=%s" % self.package)
        # set the exact ORM-version for the proper requirements
        # it's extracted from our own requirements, so looking
        # them up must be in sync (there must be the extras_require named sqlobject/sqlalchemy)
        if self.sqlobject:
            sqlobjectversion = str(get_requirement('sqlobject'))
            cmd_args.append("sqlobjectversion=%s" % sqlobjectversion)

        if self.sqlalchemy:
            sqlalchemyversion = str(get_requirement('sqlalchemy'))
            cmd_args.append("sqlalchemyversion=%s" % sqlalchemyversion)

        command.run(cmd_args)

        startscript = "start-%s.py" % self.package
        if os.path.exists(startscript):
            oldmode = os.stat(startscript).st_mode
            os.chmod(startscript,
                    oldmode | stat.S_IXUSR)
        sys.argv = ["setup.py", "egg_info"]
        import imp
        imp.load_module("setup", *imp.find_module("setup", ["."]))

        # dirty hack to allow "empty" dirs
        for base, path, files in os.walk("./"):
            for file in files:
                if file == "empty":
                    os.remove(os.path.join(base, file))
