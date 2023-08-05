# -*- coding: utf-8 -*-

from turbogears.toolbox.admi18n import pygettext

def test_support_explicit_lang():
    """Test that i18n msg extraction handles arguments in gettext calls correctly."""
    assert _('Something', 'en') == u'Something'
    assert _('New', 'en') == u'New'
