# ./pyxb/bundles/opengis/raw/ic_ism_2_1.py
# PyXB bindings for NM:6a2dbc65b53dd34df1735f2f95a5cdb99288cc6f
# Generated 2011-09-09 14:19:01.183166 by PyXB version 1.1.3
# Namespace urn:us:gov:ic:ism:v2

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:92e442de-db18-11e0-b5fe-001fbc013adc')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2', create_if_missing=True)
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


# Atomic SimpleTypeDefinition
class STD_ANON (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON._InitializeFacetMap()

# Atomic SimpleTypeDefinition
class ClassificationType (pyxb.binding.datatypes.NMTOKEN, pyxb.binding.basis.enumeration_mixin):

    """
        This simple type is used by the classification attribute to identify the highest level of classification of the information being encoded. It is manifested in portion marks and security banners.

        PERMISSIBLE VALUES

        The permissible values for this simple type are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:

         US Classification Markings - Authorized Portion Markings
         NATO Classification Markings - Authorized Portion Markings

      """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ClassificationType')
    _Documentation = u'\n        This simple type is used by the classification attribute to identify the highest level of classification of the information being encoded. It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this simple type are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n         US Classification Markings - Authorized Portion Markings\n         NATO Classification Markings - Authorized Portion Markings\n\n      '
ClassificationType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ClassificationType, enum_prefix=None)
ClassificationType.U = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'U', tag=u'U')
ClassificationType.C = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'C', tag=u'C')
ClassificationType.S = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'S', tag=u'S')
ClassificationType.TS = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'TS', tag=u'TS')
ClassificationType.R = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'R', tag=u'R')
ClassificationType.CTS = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'CTS', tag=u'CTS')
ClassificationType.CTS_B = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'CTS-B', tag=u'CTS_B')
ClassificationType.CTS_BALK = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'CTS-BALK', tag=u'CTS_BALK')
ClassificationType.NU = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'NU', tag=u'NU')
ClassificationType.NR = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'NR', tag=u'NR')
ClassificationType.NC = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'NC', tag=u'NC')
ClassificationType.NS = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'NS', tag=u'NS')
ClassificationType.NS_S = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'NS-S', tag=u'NS_S')
ClassificationType.NS_A = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'NS-A', tag=u'NS_A')
ClassificationType.CTSA = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'CTSA', tag=u'CTSA')
ClassificationType.NSAT = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'NSAT', tag=u'NSAT')
ClassificationType.NCA = ClassificationType._CF_enumeration.addEnumeration(unicode_value=u'NCA', tag=u'NCA')
ClassificationType._InitializeFacetMap(ClassificationType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ClassificationType', ClassificationType)

# Atomic SimpleTypeDefinition
class STD_ANON_ (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_._InitializeFacetMap()

# Atomic SimpleTypeDefinition
class STD_ANON_2 (pyxb.binding.datatypes.boolean):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_2._InitializeFacetMap()

# Atomic SimpleTypeDefinition
class STD_ANON_3 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_3._InitializeFacetMap()

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.NMTOKENS
class STD_ANON_4 (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.NMTOKEN."""

    _ExpandedName = None
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.NMTOKEN
STD_ANON_4._InitializeFacetMap()

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.NMTOKENS
class STD_ANON_5 (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.NMTOKEN."""

    _ExpandedName = None
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.NMTOKEN
STD_ANON_5._InitializeFacetMap()

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.NMTOKENS
class STD_ANON_6 (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.NMTOKEN."""

    _ExpandedName = None
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.NMTOKEN
STD_ANON_6._InitializeFacetMap()

# Atomic SimpleTypeDefinition
class STD_ANON_7 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_7._InitializeFacetMap()

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.NMTOKENS
class STD_ANON_8 (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.NMTOKEN."""

    _ExpandedName = None
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.NMTOKEN
STD_ANON_8._InitializeFacetMap()

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.NMTOKENS
class STD_ANON_9 (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.NMTOKEN."""

    _ExpandedName = None
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.NMTOKEN
STD_ANON_9._InitializeFacetMap()

# Atomic SimpleTypeDefinition
class STD_ANON_10 (pyxb.binding.datatypes.date):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_10._InitializeFacetMap()

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.NMTOKENS
class STD_ANON_11 (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.NMTOKEN."""

    _ExpandedName = None
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.NMTOKEN
STD_ANON_11._InitializeFacetMap()

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.NMTOKENS
class STD_ANON_12 (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.NMTOKEN."""

    _ExpandedName = None
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.NMTOKEN
STD_ANON_12._InitializeFacetMap()

# Atomic SimpleTypeDefinition
class STD_ANON_13 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_13._InitializeFacetMap()

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.NMTOKENS
class STD_ANON_14 (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.NMTOKEN."""

    _ExpandedName = None
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.NMTOKEN
STD_ANON_14._InitializeFacetMap()

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.NMTOKENS
class STD_ANON_15 (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.NMTOKEN."""

    _ExpandedName = None
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.NMTOKEN
STD_ANON_15._InitializeFacetMap()

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.NMTOKENS
class STD_ANON_16 (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.NMTOKEN."""

    _ExpandedName = None
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.NMTOKEN
STD_ANON_16._InitializeFacetMap()

# Atomic SimpleTypeDefinition
class STD_ANON_17 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_17._InitializeFacetMap()
