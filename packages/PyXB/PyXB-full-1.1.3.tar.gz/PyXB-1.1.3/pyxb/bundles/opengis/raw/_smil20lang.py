# ./pyxb/bundles/opengis/raw/_smil20lang.py
# PyXB bindings for NM:d0802cbbff8747c6667e7e00aecfa8342125f24f
# Generated 2011-09-09 14:18:49.475525 by PyXB version 1.1.3
# Namespace http://www.w3.org/2001/SMIL20/Language [xmlns:smil20lang]

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:8ad340a4-db18-11e0-8861-001fbc013adc')

# Import bindings for namespaces imported into schema
import pyxb.bundles.opengis.raw._nsgroup_

Namespace = pyxb.namespace.NamespaceForURI(u'http://www.w3.org/2001/SMIL20/Language', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
ModuleRecord = Namespace.lookupModuleRecordByUID(_GenerationUID, create_if_missing=True)
ModuleRecord._setModule(sys.modules[__name__])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a Python instance."""
    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=Namespace.fallbackNamespace(), location_base=location_base)
    handler = saxer.getContentHandler()
    saxer.parse(StringIO.StringIO(xml_text))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, _fallback_namespace=default_namespace)

from pyxb.bundles.opengis.raw._nsgroup_ import set # {http://www.w3.org/2001/SMIL20/Language}set
from pyxb.bundles.opengis.raw._nsgroup_ import animateMotion_ as animateMotion # {http://www.w3.org/2001/SMIL20/Language}animateMotion
from pyxb.bundles.opengis.raw._nsgroup_ import animate_ as animate # {http://www.w3.org/2001/SMIL20/Language}animate
from pyxb.bundles.opengis.raw._nsgroup_ import animateColor_ as animateColor # {http://www.w3.org/2001/SMIL20/Language}animateColor
from pyxb.bundles.opengis.raw._nsgroup_ import setType # {http://www.w3.org/2001/SMIL20/Language}setType
from pyxb.bundles.opengis.raw._nsgroup_ import animateMotionType # {http://www.w3.org/2001/SMIL20/Language}animateMotionType
from pyxb.bundles.opengis.raw._nsgroup_ import animateType # {http://www.w3.org/2001/SMIL20/Language}animateType
from pyxb.bundles.opengis.raw._nsgroup_ import animateColorType # {http://www.w3.org/2001/SMIL20/Language}animateColorType
