# -*- coding: UTF-8 -*-

import os
import sys

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

if sys.version_info < (2, 4):
    raise SystemExit("Python 2.4 or later is required")

# import meta data (version, author etc.)
execfile(os.path.join("turbogears", "release.py"))

# setup params
install_requires = [
    "CherryPy >= 2.3.0, < 3.0dev",
    "ConfigObj >= 4.3.2",
    "FormEncode >= 1.2.1",
    "Genshi >= 0.4.4",
    "PasteScript[Cheetah] >= 1.7",
    "PEAK-Rules >= 0.5a1.dev-r2555",
    "setuptools >= 0.6c11",
    "simplejson >= 1.9.1",
    # TurboJson < 1.2 uses RuleDispatch
    "TurboJson >= 1.2.1",
    "tgMochiKit >= 1.4.2",
]

# for when we get rid of Kid & SQLObject dependency
compat = [
    "TurboCheetah >= 1.0",
    "TurboKid >= 1.0.5",
]

sqlobject = [
    "SQLObject >= 0.10.1",
]

future = []

sqlalchemy = [
    "Elixir >= 0.6.1",
    "SQLAlchemy >= 0.4.3",
] + compat

toscawidgets = [
    "ToscaWidgets >= 0.9.6",
    "tw.forms >= 0.9.6"
]

testtools = [
    "nose >= 0.9.3",
    "WebTest"
]

tgtesttools = testtools

if sys.version_info < (2, 5):
    tgtesttools.extend([
            # Python < 2.5 does not include SQLite
            "pysqlite",
            # WebTest needs a current wsgiref version
            "wsgiref >= 0.1.2",
        ])

develop_requires = (install_requires
    + future + tgtesttools + sqlalchemy + sqlobject)

setup(
    name="TurboGears",
    description=description,
    long_description=long_description,
    version=version,
    author=author,
    author_email=email,
    maintainer=maintainer,
    maintainer_email=maintainer_email,
    url=url,
    download_url=download_url,
    dependency_links=dependency_links,
    license=license,
    zip_safe=False,
    install_requires = install_requires,
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={"thirdparty": ["*"]},
    entry_points = """
    [console_scripts]
    tg-admin = turbogears.command:main

    [distutils.commands]
    docs = turbogears.docgen:GenSite

    [paste.paster_create_template]
    tgbase = turbogears.command.quickstart:BaseTemplate
    turbogears = turbogears.command.quickstart:TurbogearsTemplate
    tgbig = turbogears.command.quickstart:TGBig
    tgwidget = turbogears.command.quickstart:TGWidgetTemplate

    [turbogears.command]
    quickstart = turbogears.command.quickstart:quickstart
    sql = turbogears.command.base:SQL
    shell = turbogears.command.base:Shell
    toolbox = turbogears.command.base:ToolboxCommand
    update = turbogears.command.quickstart:update
    i18n = turbogears.command.i18n:InternationalizationTool
    info = turbogears.command.info:InfoCommand
    kid2genshi = turbogears.command.kid2genshi:Kid2Genshi

    [turbogears.identity.provider]
    sqlobject = turbogears.identity.soprovider:SqlObjectIdentityProvider
    sqlalchemy= turbogears.identity.saprovider:SqlAlchemyIdentityProvider

    [turbogears.extensions]
    identity = turbogears.identity.visitor
    visit = turbogears.visit

    [turbogears.visit.manager]
    sqlobject = turbogears.visit.sovisit:SqlObjectVisitManager
    sqlalchemy = turbogears.visit.savisit:SqlAlchemyVisitManager

    [turbogears.toolboxcommand]
    widgets = turbogears.toolbox.base:WidgetBrowser
    shell = turbogears.toolbox.shell:WebConsole
    admi18n = turbogears.toolbox.admi18n:Internationalization
    designer = turbogears.toolbox.designer:Designer
    info = turbogears.toolbox.base:Info
    catwalk = turbogears.toolbox.catwalk:CatWalk

    """,
    extras_require = {
        'compat': compat,
        'sqlobject': sqlobject,
        'sqlalchemy': sqlalchemy,
        'toscawidgets': toscawidgets,
        'future': future,
        'testtools': testtools,
        'tgtesttools': tgtesttools,
        'develop': develop_requires,
    },
    tests_require = develop_requires,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: TurboGears',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    test_suite = 'nose.collector',
)
