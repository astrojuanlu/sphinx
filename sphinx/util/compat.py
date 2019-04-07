"""
    sphinx.util.compat
    ~~~~~~~~~~~~~~~~~~

    modules for backward compatibility

    :copyright: Copyright 2007-2019 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import sys
import warnings

from docutils.utils import get_source_line

from sphinx import addnodes
from sphinx.deprecation import RemovedInSphinx40Warning
from sphinx.transforms import SphinxTransform

if False:
    # For type annotation
    from typing import Any, Dict  # NOQA
    from sphinx.application import Sphinx  # NOQA
    from sphinx.config import Config  # NOQA


def register_application_for_autosummary(app):
    # type: (Sphinx) -> None
    """Register application object to autosummary module.

    Since Sphinx-1.7, documenters and attrgetters are registered into
    applicaiton object.  As a result, the arguments of
    ``get_documenter()`` has been changed.  To keep compatibility,
    this handler registers application object to the module.
    """
    if 'sphinx.ext.autosummary' in sys.modules:
        from sphinx.ext import autosummary
        autosummary._app = app


class IndexEntriesMigrator(SphinxTransform):
    """Migrating indexentries from old style (4columns) to new style (5columns)."""
    default_priority = 700

    def apply(self, **kwargs):
        # type: (Any) -> None
        for node in self.document.traverse(addnodes.index):
            for i, entries in enumerate(node['entries']):
                if len(entries) == 4:
                    source, line = get_source_line(node)
                    warnings.warn('An old styled index node found: %r at (%s:%s)' %
                                  (node, source, line), RemovedInSphinx40Warning)
                    node['entries'][i] = entries + (None,)


def setup(app):
    # type: (Sphinx) -> Dict[str, Any]
    app.add_transform(IndexEntriesMigrator)
    app.connect('builder-inited', register_application_for_autosummary)

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
