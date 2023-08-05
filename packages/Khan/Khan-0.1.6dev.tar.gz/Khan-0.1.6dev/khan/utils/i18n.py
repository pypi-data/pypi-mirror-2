# -*- coding: utf-8 -*-

"""
Khan 内部的国际化支持
=================================

索引
=================================

* :func:`_`

=================================

.. autofunction:: _
"""

import os, gettext

__all__ = ["_"]

DOMAIN = "khan"

gettext.bindtextdomain(DOMAIN, os.path.join(os.path.dirname(os.path.dirname(__file__)), "locales"))
gettext.textdomain(DOMAIN)

_ = gettext.gettext
