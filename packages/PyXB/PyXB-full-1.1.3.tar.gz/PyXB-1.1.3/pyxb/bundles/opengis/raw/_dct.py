# ./pyxb/bundles/opengis/raw/_dct.py
# PyXB bindings for NM:62e52a6e1b0d23522982e9c2905e5cb67ad01951
# Generated 2011-09-09 14:19:15.800919 by PyXB version 1.1.3
# Namespace http://purl.org/dc/terms/ [xmlns:dct]

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9b8fedac-db18-11e0-abb2-001fbc013adc')

# Import bindings for namespaces imported into schema
import pyxb.bundles.opengis.raw._nsgroup_2

Namespace = pyxb.namespace.NamespaceForURI(u'http://purl.org/dc/terms/', create_if_missing=True)
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

from pyxb.bundles.opengis.raw._nsgroup_2 import conformsTo # {http://purl.org/dc/terms/}conformsTo
from pyxb.bundles.opengis.raw._nsgroup_2 import mediator # {http://purl.org/dc/terms/}mediator
from pyxb.bundles.opengis.raw._nsgroup_2 import modified # {http://purl.org/dc/terms/}modified
from pyxb.bundles.opengis.raw._nsgroup_2 import accessRights # {http://purl.org/dc/terms/}accessRights
from pyxb.bundles.opengis.raw._nsgroup_2 import provenance # {http://purl.org/dc/terms/}provenance
from pyxb.bundles.opengis.raw._nsgroup_2 import references # {http://purl.org/dc/terms/}references
from pyxb.bundles.opengis.raw._nsgroup_2 import isVersionOf # {http://purl.org/dc/terms/}isVersionOf
from pyxb.bundles.opengis.raw._nsgroup_2 import requires # {http://purl.org/dc/terms/}requires
from pyxb.bundles.opengis.raw._nsgroup_2 import rightsHolder # {http://purl.org/dc/terms/}rightsHolder
from pyxb.bundles.opengis.raw._nsgroup_2 import spatial # {http://purl.org/dc/terms/}spatial
from pyxb.bundles.opengis.raw._nsgroup_2 import tableOfContents # {http://purl.org/dc/terms/}tableOfContents
from pyxb.bundles.opengis.raw._nsgroup_2 import license # {http://purl.org/dc/terms/}license
from pyxb.bundles.opengis.raw._nsgroup_2 import temporal # {http://purl.org/dc/terms/}temporal
from pyxb.bundles.opengis.raw._nsgroup_2 import valid # {http://purl.org/dc/terms/}valid
from pyxb.bundles.opengis.raw._nsgroup_2 import isPartOf # {http://purl.org/dc/terms/}isPartOf
from pyxb.bundles.opengis.raw._nsgroup_2 import bibliographicCitation # {http://purl.org/dc/terms/}bibliographicCitation
from pyxb.bundles.opengis.raw._nsgroup_2 import audience # {http://purl.org/dc/terms/}audience
from pyxb.bundles.opengis.raw._nsgroup_2 import available # {http://purl.org/dc/terms/}available
from pyxb.bundles.opengis.raw._nsgroup_2 import created # {http://purl.org/dc/terms/}created
from pyxb.bundles.opengis.raw._nsgroup_2 import replaces # {http://purl.org/dc/terms/}replaces
from pyxb.bundles.opengis.raw._nsgroup_2 import dateAccepted # {http://purl.org/dc/terms/}dateAccepted
from pyxb.bundles.opengis.raw._nsgroup_2 import dateCopyrighted # {http://purl.org/dc/terms/}dateCopyrighted
from pyxb.bundles.opengis.raw._nsgroup_2 import alternative # {http://purl.org/dc/terms/}alternative
from pyxb.bundles.opengis.raw._nsgroup_2 import hasPart # {http://purl.org/dc/terms/}hasPart
from pyxb.bundles.opengis.raw._nsgroup_2 import dateSubmitted # {http://purl.org/dc/terms/}dateSubmitted
from pyxb.bundles.opengis.raw._nsgroup_2 import hasFormat # {http://purl.org/dc/terms/}hasFormat
from pyxb.bundles.opengis.raw._nsgroup_2 import abstract # {http://purl.org/dc/terms/}abstract
from pyxb.bundles.opengis.raw._nsgroup_2 import extent # {http://purl.org/dc/terms/}extent
from pyxb.bundles.opengis.raw._nsgroup_2 import hasVersion # {http://purl.org/dc/terms/}hasVersion
from pyxb.bundles.opengis.raw._nsgroup_2 import medium # {http://purl.org/dc/terms/}medium
from pyxb.bundles.opengis.raw._nsgroup_2 import isFormatOf # {http://purl.org/dc/terms/}isFormatOf
from pyxb.bundles.opengis.raw._nsgroup_2 import isReferencedBy # {http://purl.org/dc/terms/}isReferencedBy
from pyxb.bundles.opengis.raw._nsgroup_2 import isRequiredBy # {http://purl.org/dc/terms/}isRequiredBy
from pyxb.bundles.opengis.raw._nsgroup_2 import isReplacedBy # {http://purl.org/dc/terms/}isReplacedBy
from pyxb.bundles.opengis.raw._nsgroup_2 import issued # {http://purl.org/dc/terms/}issued
from pyxb.bundles.opengis.raw._nsgroup_2 import educationLevel # {http://purl.org/dc/terms/}educationLevel
