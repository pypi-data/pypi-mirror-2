# ./pyxb/bundles/opengis/raw/swe_1_0_0.py
# PyXB bindings for NM:f1da75586f8f2412f0605d01316001be0779ca84
# Generated 2011-09-09 14:18:54.694995 by PyXB version 1.1.3
# Namespace http://www.opengis.net/swe/1.0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:8e6b4aa4-db18-11e0-8c56-001fbc013adc')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.opengis.gml
import pyxb.bundles.opengis.misc.xlinks

Namespace = pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/swe/1.0', create_if_missing=True)
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


# Union SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class timePositionType (pyxb.binding.basis.STD_union):

    """Choice of time position encodings, including numeric representation but no frame. 
	A minor variation on gml:TimePositionUnion - carrying "indeterminate value" as content instead of an attribute. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'timePositionType')
    _Documentation = u'Choice of time position encodings, including numeric representation but no frame. \n\tA minor variation on gml:TimePositionUnion - carrying "indeterminate value" as content instead of an attribute. '

    _MemberTypes = ( pyxb.binding.datatypes.date, pyxb.binding.datatypes.time, pyxb.binding.datatypes.dateTime, pyxb.bundles.opengis.gml.TimeIndeterminateValueType, pyxb.binding.datatypes.double, )
timePositionType._CF_pattern = pyxb.binding.facets.CF_pattern()
timePositionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=timePositionType)
timePositionType.after = u'after'                 # originally pyxb.bundles.opengis.gml.TimeIndeterminateValueType.after
timePositionType.before = u'before'               # originally pyxb.bundles.opengis.gml.TimeIndeterminateValueType.before
timePositionType.now = u'now'                     # originally pyxb.bundles.opengis.gml.TimeIndeterminateValueType.now
timePositionType.unknown = u'unknown'             # originally pyxb.bundles.opengis.gml.TimeIndeterminateValueType.unknown
timePositionType._InitializeFacetMap(timePositionType._CF_pattern,
   timePositionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'timePositionType', timePositionType)

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class timeList (pyxb.binding.basis.STD_list):

    """Simple list of time positions. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'timeList')
    _Documentation = u'Simple list of time positions. '

    _ItemType = timePositionType
timeList._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'timeList', timeList)

# List SimpleTypeDefinition
# superclasses timeList
class timePair (pyxb.binding.basis.STD_list):

    """Pair of time positions. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'timePair')
    _Documentation = u'Pair of time positions. '

    _ItemType = timePositionType
timePair._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(2L))
timePair._InitializeFacetMap(timePair._CF_length)
Namespace.addCategoryObject('typeBinding', u'timePair', timePair)

# Atomic SimpleTypeDefinition
class UomURI (pyxb.binding.datatypes.anyURI):

    """Local copy of GML 3.2 uom URI definition"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'UomURI')
    _Documentation = u'Local copy of GML 3.2 uom URI definition'
UomURI._CF_pattern = pyxb.binding.facets.CF_pattern()
UomURI._CF_pattern.addPattern(pattern=u'([a-zA-Z][a-zA-Z0-9\\-\\+\\.]*:|\\.\\./|\\./|#).*')
UomURI._InitializeFacetMap(UomURI._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'UomURI', UomURI)

# Atomic SimpleTypeDefinition
class UomSymbol (pyxb.binding.datatypes.string):

    """Local copy of GML 3.2 uom symbol definition
			Included for forward compatibility. 
			Note: in future of this specification based on GML 3.2, these will be removed in favour of the GML 3.2 implementation"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'UomSymbol')
    _Documentation = u'Local copy of GML 3.2 uom symbol definition\n\t\t\tIncluded for forward compatibility. \n\t\t\tNote: in future of this specification based on GML 3.2, these will be removed in favour of the GML 3.2 implementation'
UomSymbol._CF_pattern = pyxb.binding.facets.CF_pattern()
UomSymbol._CF_pattern.addPattern(pattern=u'[^: \\n\\r\\t]+')
UomSymbol._InitializeFacetMap(UomSymbol._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'UomSymbol', UomSymbol)

# Union SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class UomIdentifier (pyxb.binding.basis.STD_union):

    """Local copy of GML 3.2 uom identifier definition"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'UomIdentifier')
    _Documentation = u'Local copy of GML 3.2 uom identifier definition'

    _MemberTypes = ( UomSymbol, UomURI, )
UomIdentifier._CF_pattern = pyxb.binding.facets.CF_pattern()
UomIdentifier._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=UomIdentifier)
UomIdentifier._InitializeFacetMap(UomIdentifier._CF_pattern,
   UomIdentifier._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'UomIdentifier', UomIdentifier)

# Union SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class timeIso8601 (pyxb.binding.basis.STD_union):

    """Choice of time position encodings, not including numeric representation. 
	      A minor variation on gml:TimePositionUnion - carrying "indeterminate value" as content instead of an attribute."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'timeIso8601')
    _Documentation = u'Choice of time position encodings, not including numeric representation. \n\t      A minor variation on gml:TimePositionUnion - carrying "indeterminate value" as content instead of an attribute.'

    _MemberTypes = ( pyxb.binding.datatypes.date, pyxb.binding.datatypes.time, pyxb.binding.datatypes.dateTime, pyxb.bundles.opengis.gml.TimeIndeterminateValueType, )
timeIso8601._CF_pattern = pyxb.binding.facets.CF_pattern()
timeIso8601._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=timeIso8601)
timeIso8601.after = u'after'                      # originally pyxb.bundles.opengis.gml.TimeIndeterminateValueType.after
timeIso8601.before = u'before'                    # originally pyxb.bundles.opengis.gml.TimeIndeterminateValueType.before
timeIso8601.now = u'now'                          # originally pyxb.bundles.opengis.gml.TimeIndeterminateValueType.now
timeIso8601.unknown = u'unknown'                  # originally pyxb.bundles.opengis.gml.TimeIndeterminateValueType.unknown
timeIso8601._InitializeFacetMap(timeIso8601._CF_pattern,
   timeIso8601._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'timeIso8601', timeIso8601)

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class tokenList (pyxb.binding.basis.STD_list):

    """Simple list of tokens. 
			Note: xs:token is a string with no embedded white-space allowed"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'tokenList')
    _Documentation = u'Simple list of tokens. \n\t\t\tNote: xs:token is a string with no embedded white-space allowed'

    _ItemType = pyxb.binding.datatypes.token
tokenList._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'tokenList', tokenList)

# Atomic SimpleTypeDefinition
class byteOrder (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'byteOrder')
    _Documentation = None
byteOrder._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=byteOrder, enum_prefix=None)
byteOrder.bigEndian = byteOrder._CF_enumeration.addEnumeration(unicode_value=u'bigEndian', tag=u'bigEndian')
byteOrder.littleEndian = byteOrder._CF_enumeration.addEnumeration(unicode_value=u'littleEndian', tag=u'littleEndian')
byteOrder._InitializeFacetMap(byteOrder._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'byteOrder', byteOrder)

# Atomic SimpleTypeDefinition
class byteEncoding (pyxb.binding.datatypes.token, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'byteEncoding')
    _Documentation = None
byteEncoding._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=byteEncoding, enum_prefix=None)
byteEncoding.base64 = byteEncoding._CF_enumeration.addEnumeration(unicode_value=u'base64', tag=u'base64')
byteEncoding.raw = byteEncoding._CF_enumeration.addEnumeration(unicode_value=u'raw', tag=u'raw')
byteEncoding.hex = byteEncoding._CF_enumeration.addEnumeration(unicode_value=u'hex', tag=u'hex')
byteEncoding._InitializeFacetMap(byteEncoding._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'byteEncoding', byteEncoding)

# Atomic SimpleTypeDefinition
class textSeparator (pyxb.binding.datatypes.string):

    """Max three characters to use as token or block separator"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'textSeparator')
    _Documentation = u'Max three characters to use as token or block separator'
textSeparator._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(3L))
textSeparator._InitializeFacetMap(textSeparator._CF_maxLength)
Namespace.addCategoryObject('typeBinding', u'textSeparator', textSeparator)

# Atomic SimpleTypeDefinition
class decimalSeparator (pyxb.binding.datatypes.token):

    """One character to use as a decimal separator"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'decimalSeparator')
    _Documentation = u'One character to use as a decimal separator'
decimalSeparator._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(1L))
decimalSeparator._InitializeFacetMap(decimalSeparator._CF_length)
Namespace.addCategoryObject('typeBinding', u'decimalSeparator', decimalSeparator)

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class decimalList (pyxb.binding.basis.STD_list):

    """Simple list of double-precision numbers. 
	Note: xs:double supports either decimal or scientific notation"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'decimalList')
    _Documentation = u'Simple list of double-precision numbers. \n\tNote: xs:double supports either decimal or scientific notation'

    _ItemType = pyxb.binding.datatypes.double
decimalList._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'decimalList', decimalList)

# List SimpleTypeDefinition
# superclasses decimalList
class decimalPair (pyxb.binding.basis.STD_list):

    """Pair of double-precision numbers. 
	Note: xs:double supports either decimal or scientific notation"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'decimalPair')
    _Documentation = u'Pair of double-precision numbers. \n\tNote: xs:double supports either decimal or scientific notation'

    _ItemType = pyxb.binding.datatypes.double
decimalPair._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(2L))
decimalPair._InitializeFacetMap(decimalPair._CF_length)
Namespace.addCategoryObject('typeBinding', u'decimalPair', decimalPair)

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class TimeValueList (pyxb.binding.basis.STD_list):

    """Compact list of time instants, following gml:posList pattern. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeValueList')
    _Documentation = u'Compact list of time instants, following gml:posList pattern. '

    _ItemType = pyxb.bundles.opengis.gml.TimePositionUnion
TimeValueList._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'TimeValueList', TimeValueList)

# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class countList (pyxb.binding.basis.STD_list):

    """Simple list of integers. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'countList')
    _Documentation = u'Simple list of integers. '

    _ItemType = pyxb.binding.datatypes.integer
countList._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'countList', countList)

# List SimpleTypeDefinition
# superclasses countList
class countPair (pyxb.binding.basis.STD_list):

    """Pair of integers. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'countPair')
    _Documentation = u'Pair of integers. '

    _ItemType = pyxb.binding.datatypes.integer
countPair._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(2L))
countPair._InitializeFacetMap(countPair._CF_length)
Namespace.addCategoryObject('typeBinding', u'countPair', countPair)

# Complex type AbstractDataComponentType with content type ELEMENT_ONLY
class AbstractDataComponentType (pyxb.bundles.opengis.gml.AbstractGMLType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AbstractDataComponentType')
    # Base type is pyxb.bundles.opengis.gml.AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed uses Python identifier fixed
    __fixed = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'fixed'), 'fixed', '__httpwww_opengis_netswe1_0_AbstractDataComponentType_fixed', pyxb.binding.datatypes.boolean, unicode_default=u'false')
    
    fixed = property(__fixed.value, __fixed.set, None, u'Specifies if the value of a component stays fixed in time or is variable. Default is variable')

    
    # Attribute definition uses Python identifier definition
    __definition = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'definition'), 'definition', '__httpwww_opengis_netswe1_0_AbstractDataComponentType_definition', pyxb.binding.datatypes.anyURI)
    
    definition = property(__definition.value, __definition.set, None, u'Points to semantics information defining the precise nature of the component')

    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = pyxb.bundles.opengis.gml.AbstractGMLType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = pyxb.bundles.opengis.gml.AbstractGMLType._AttributeMap.copy()
    _AttributeMap.update({
        __fixed.name() : __fixed,
        __definition.name() : __definition
    })
Namespace.addCategoryObject('typeBinding', u'AbstractDataComponentType', AbstractDataComponentType)


# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractDataComponentType
    
    # Element {http://www.opengis.net/swe/1.0}quality uses Python identifier quality
    __quality = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'quality'), 'quality', '__httpwww_opengis_netswe1_0_CTD_ANON_httpwww_opengis_netswe1_0quality', False)

    
    quality = property(__quality.value, __quality.set, None, u'The quality property provides an indication of the reliability of estimates of the asociated value')

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netswe1_0_CTD_ANON_httpwww_opengis_netswe1_0value', False)

    
    value_ = property(__value.value, __value.set, None, u'Value is optional, to enable structure to act in a schema for values provided using other encodings')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute axisID uses Python identifier axisID
    __axisID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'axisID'), 'axisID', '__httpwww_opengis_netswe1_0_CTD_ANON_axisID', pyxb.binding.datatypes.token)
    
    axisID = property(__axisID.value, __axisID.set, None, u'Specifies the reference axis using the gml:axisID. The reference frame URI is inherited from parent Vector')

    
    # Attribute referenceFrame uses Python identifier referenceFrame
    __referenceFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceFrame'), 'referenceFrame', '__httpwww_opengis_netswe1_0_CTD_ANON_referenceFrame', pyxb.binding.datatypes.anyURI)
    
    referenceFrame = property(__referenceFrame.value, __referenceFrame.set, None, u'A reference frame anchors a value to a datum or interval scale')

    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType

    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        __quality.name() : __quality,
        __value.name() : __value
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        __axisID.name() : __axisID,
        __referenceFrame.name() : __referenceFrame
    })



# Complex type CTD_ANON_ with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}CountRange uses Python identifier CountRange
    __CountRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'CountRange'), 'CountRange', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netswe1_0CountRange', False)

    
    CountRange = property(__CountRange.value, __CountRange.set, None, u'Integer pair used for specifying a count range')

    
    # Element {http://www.opengis.net/swe/1.0}Boolean uses Python identifier Boolean
    __Boolean = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), 'Boolean', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netswe1_0Boolean', False)

    
    Boolean = property(__Boolean.value, __Boolean.set, None, u'Scalar component used to express truth: True or False, 0 or 1')

    
    # Element {http://www.opengis.net/swe/1.0}Category uses Python identifier Category
    __Category = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Category'), 'Category', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netswe1_0Category', False)

    
    Category = property(__Category.value, __Category.set, None, u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value')

    
    # Element {http://www.opengis.net/swe/1.0}QuantityRange uses Python identifier QuantityRange
    __QuantityRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), 'QuantityRange', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netswe1_0QuantityRange', False)

    
    QuantityRange = property(__QuantityRange.value, __QuantityRange.set, None, u'Decimal pair for specifying a quantity range with constraints')

    
    # Element {http://www.opengis.net/swe/1.0}AbstractDataRecord uses Python identifier AbstractDataRecord
    __AbstractDataRecord = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord'), 'AbstractDataRecord', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netswe1_0AbstractDataRecord', False)

    
    AbstractDataRecord = property(__AbstractDataRecord.value, __AbstractDataRecord.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}Time uses Python identifier Time
    __Time = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Time'), 'Time', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netswe1_0Time', False)

    
    Time = property(__Time.value, __Time.set, None, u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin')

    
    # Element {http://www.opengis.net/swe/1.0}Quantity uses Python identifier Quantity
    __Quantity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), 'Quantity', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netswe1_0Quantity', False)

    
    Quantity = property(__Quantity.value, __Quantity.set, None, u'Decimal number with optional unit and constraints')

    
    # Element {http://www.opengis.net/swe/1.0}AbstractDataArray uses Python identifier AbstractDataArray
    __AbstractDataArray = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray'), 'AbstractDataArray', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netswe1_0AbstractDataArray', False)

    
    AbstractDataArray = property(__AbstractDataArray.value, __AbstractDataArray.set, None, u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways')

    
    # Element {http://www.opengis.net/swe/1.0}TimeRange uses Python identifier TimeRange
    __TimeRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeRange'), 'TimeRange', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netswe1_0TimeRange', False)

    
    TimeRange = property(__TimeRange.value, __TimeRange.set, None, u'Time value pair for specifying a time range (can be a decimal or ISO 8601)')

    
    # Element {http://www.opengis.net/swe/1.0}Text uses Python identifier Text
    __Text = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Text'), 'Text', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netswe1_0Text', False)

    
    Text = property(__Text.value, __Text.set, None, u'Free textual component')

    
    # Element {http://www.opengis.net/swe/1.0}Count uses Python identifier Count
    __Count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Count'), 'Count', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netswe1_0Count', False)

    
    Count = property(__Count.value, __Count.set, None, u'Integer number used for a counting value')

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_CTD_ANON__httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)


    _ElementMap = {
        __CountRange.name() : __CountRange,
        __Boolean.name() : __Boolean,
        __Category.name() : __Category,
        __QuantityRange.name() : __QuantityRange,
        __AbstractDataRecord.name() : __AbstractDataRecord,
        __Time.name() : __Time,
        __Quantity.name() : __Quantity,
        __AbstractDataArray.name() : __AbstractDataArray,
        __TimeRange.name() : __TimeRange,
        __Text.name() : __Text,
        __Count.name() : __Count
    }
    _AttributeMap = {
        __type.name() : __type,
        __title.name() : __title,
        __role.name() : __role,
        __actuate.name() : __actuate,
        __remoteSchema.name() : __remoteSchema,
        __arcrole.name() : __arcrole,
        __show.name() : __show,
        __href.name() : __href
    }



# Complex type PhenomenonPropertyType with content type ELEMENT_ONLY
class PhenomenonPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PhenomenonPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Phenomenon uses Python identifier Phenomenon
    __Phenomenon = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Phenomenon'), 'Phenomenon', '__httpwww_opengis_netswe1_0_PhenomenonPropertyType_httpwww_opengis_netswe1_0Phenomenon', False)

    
    Phenomenon = property(__Phenomenon.value, __Phenomenon.set, None, u'Basic Phenomenon definition, and head of substitution group of specialized phenomenon defs. ')

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_PhenomenonPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_PhenomenonPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_PhenomenonPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_PhenomenonPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_PhenomenonPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_PhenomenonPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_PhenomenonPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_PhenomenonPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")


    _ElementMap = {
        __Phenomenon.name() : __Phenomenon
    }
    _AttributeMap = {
        __show.name() : __show,
        __href.name() : __href,
        __role.name() : __role,
        __remoteSchema.name() : __remoteSchema,
        __type.name() : __type,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __actuate.name() : __actuate
    }
Namespace.addCategoryObject('typeBinding', u'PhenomenonPropertyType', PhenomenonPropertyType)


# Complex type CTD_ANON_2 with content type ELEMENT_ONLY
class CTD_ANON_2 (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractDataComponentType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netswe1_0_CTD_ANON_2_httpwww_opengis_netswe1_0value', False)

    
    value_ = property(__value.value, __value.set, None, u'Value is optional, to enable structure to act in a schema for values provided using other encodings')

    
    # Element {http://www.opengis.net/swe/1.0}quality uses Python identifier quality
    __quality = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'quality'), 'quality', '__httpwww_opengis_netswe1_0_CTD_ANON_2_httpwww_opengis_netswe1_0quality', True)

    
    quality = property(__quality.value, __quality.set, None, u'The quality property provides an indication of the reliability of estimates of the asociated value')

    
    # Element {http://www.opengis.net/swe/1.0}constraint uses Python identifier constraint
    __constraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'constraint'), 'constraint', '__httpwww_opengis_netswe1_0_CTD_ANON_2_httpwww_opengis_netswe1_0constraint', False)

    
    constraint = property(__constraint.value, __constraint.set, None, u'The constraint property defines the permitted values, as a range or enumerated list')

    
    # Attribute referenceFrame uses Python identifier referenceFrame
    __referenceFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceFrame'), 'referenceFrame', '__httpwww_opengis_netswe1_0_CTD_ANON_2_referenceFrame', pyxb.binding.datatypes.anyURI)
    
    referenceFrame = property(__referenceFrame.value, __referenceFrame.set, None, u'A reference frame anchors a value to a datum or interval scale')

    
    # Attribute axisID uses Python identifier axisID
    __axisID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'axisID'), 'axisID', '__httpwww_opengis_netswe1_0_CTD_ANON_2_axisID', pyxb.binding.datatypes.token)
    
    axisID = property(__axisID.value, __axisID.set, None, u'Specifies the reference axis using the gml:axisID. The reference frame URI is inherited from parent Vector')

    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType

    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        __value.name() : __value,
        __quality.name() : __quality,
        __constraint.name() : __constraint
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        __referenceFrame.name() : __referenceFrame,
        __axisID.name() : __axisID
    })



# Complex type AbstractDataRecordType with content type ELEMENT_ONLY
class AbstractDataRecordType (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecordType')
    # Base type is AbstractDataComponentType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AbstractDataRecordType', AbstractDataRecordType)


# Complex type AbstractVectorType with content type ELEMENT_ONLY
class AbstractVectorType (AbstractDataRecordType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AbstractVectorType')
    # Base type is AbstractDataRecordType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute referenceFrame uses Python identifier referenceFrame
    __referenceFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceFrame'), 'referenceFrame', '__httpwww_opengis_netswe1_0_AbstractVectorType_referenceFrame', pyxb.binding.datatypes.anyURI)
    
    referenceFrame = property(__referenceFrame.value, __referenceFrame.set, None, u'Points to a spatial reference frame definition. Coordinates of the vector will be expressed in this reference frame')

    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute localFrame uses Python identifier localFrame
    __localFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'localFrame'), 'localFrame', '__httpwww_opengis_netswe1_0_AbstractVectorType_localFrame', pyxb.binding.datatypes.anyURI)
    
    localFrame = property(__localFrame.value, __localFrame.set, None, u'Specifies the spatial frame which location and/or orientation is given by the enclosing vector')


    _ElementMap = AbstractDataRecordType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = AbstractDataRecordType._AttributeMap.copy()
    _AttributeMap.update({
        __referenceFrame.name() : __referenceFrame,
        __localFrame.name() : __localFrame
    })
Namespace.addCategoryObject('typeBinding', u'AbstractVectorType', AbstractVectorType)


# Complex type VectorType with content type ELEMENT_ONLY
class VectorType (AbstractVectorType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'VectorType')
    # Base type is AbstractVectorType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}coordinate uses Python identifier coordinate
    __coordinate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'coordinate'), 'coordinate', '__httpwww_opengis_netswe1_0_VectorType_httpwww_opengis_netswe1_0coordinate', True)

    
    coordinate = property(__coordinate.value, __coordinate.set, None, None)

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute referenceFrame inherited from {http://www.opengis.net/swe/1.0}AbstractVectorType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute localFrame inherited from {http://www.opengis.net/swe/1.0}AbstractVectorType

    _ElementMap = AbstractVectorType._ElementMap.copy()
    _ElementMap.update({
        __coordinate.name() : __coordinate
    })
    _AttributeMap = AbstractVectorType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'VectorType', VectorType)


# Complex type CTD_ANON_3 with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}ConditionalValue uses Python identifier ConditionalValue
    __ConditionalValue = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ConditionalValue'), 'ConditionalValue', '__httpwww_opengis_netswe1_0_CTD_ANON_3_httpwww_opengis_netswe1_0ConditionalValue', False)

    
    ConditionalValue = property(__ConditionalValue.value, __ConditionalValue.set, None, u'Qualifies data (scalar or not) with one or more conditions')

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_CTD_ANON_3_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_CTD_ANON_3_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_CTD_ANON_3_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_CTD_ANON_3_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_CTD_ANON_3_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_CTD_ANON_3_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_netswe1_0_CTD_ANON_3_name', pyxb.binding.datatypes.token, required=True)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_CTD_ANON_3_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_CTD_ANON_3_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)


    _ElementMap = {
        __ConditionalValue.name() : __ConditionalValue
    }
    _AttributeMap = {
        __show.name() : __show,
        __role.name() : __role,
        __type.name() : __type,
        __href.name() : __href,
        __actuate.name() : __actuate,
        __remoteSchema.name() : __remoteSchema,
        __name.name() : __name,
        __title.name() : __title,
        __arcrole.name() : __arcrole
    }



# Complex type SimpleDataRecordType with content type ELEMENT_ONLY
class SimpleDataRecordType (AbstractDataRecordType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SimpleDataRecordType')
    # Base type is AbstractDataRecordType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}field uses Python identifier field
    __field = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'field'), 'field', '__httpwww_opengis_netswe1_0_SimpleDataRecordType_httpwww_opengis_netswe1_0field', True)

    
    field = property(__field.value, __field.set, None, None)

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractDataRecordType._ElementMap.copy()
    _ElementMap.update({
        __field.name() : __field
    })
    _AttributeMap = AbstractDataRecordType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'SimpleDataRecordType', SimpleDataRecordType)


# Complex type CTD_ANON_4 with content type ELEMENT_ONLY
class CTD_ANON_4 (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractDataComponentType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}constraint uses Python identifier constraint
    __constraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'constraint'), 'constraint', '__httpwww_opengis_netswe1_0_CTD_ANON_4_httpwww_opengis_netswe1_0constraint', False)

    
    constraint = property(__constraint.value, __constraint.set, None, u'The constraint property defines the permitted values, as an enumerated list')

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}quality uses Python identifier quality
    __quality = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'quality'), 'quality', '__httpwww_opengis_netswe1_0_CTD_ANON_4_httpwww_opengis_netswe1_0quality', False)

    
    quality = property(__quality.value, __quality.set, None, u'The quality property provides an indication of the reliability of estimates of the asociated value')

    
    # Element {http://www.opengis.net/swe/1.0}codeSpace uses Python identifier codeSpace
    __codeSpace = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'codeSpace'), 'codeSpace', '__httpwww_opengis_netswe1_0_CTD_ANON_4_httpwww_opengis_netswe1_0codeSpace', False)

    
    codeSpace = property(__codeSpace.value, __codeSpace.set, None, u'Provides link to dictionary or rule set to which the value belongs')

    
    # Element {http://www.opengis.net/swe/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netswe1_0_CTD_ANON_4_httpwww_opengis_netswe1_0value', False)

    
    value_ = property(__value.value, __value.set, None, u'Value is optional, to enable structure to act in a schema for values provided using other encodings')

    
    # Attribute referenceFrame uses Python identifier referenceFrame
    __referenceFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceFrame'), 'referenceFrame', '__httpwww_opengis_netswe1_0_CTD_ANON_4_referenceFrame', pyxb.binding.datatypes.anyURI)
    
    referenceFrame = property(__referenceFrame.value, __referenceFrame.set, None, u'A reference frame anchors a value to a datum or interval scale')

    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute axisID uses Python identifier axisID
    __axisID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'axisID'), 'axisID', '__httpwww_opengis_netswe1_0_CTD_ANON_4_axisID', pyxb.binding.datatypes.token)
    
    axisID = property(__axisID.value, __axisID.set, None, u'Specifies the reference axis using the gml:axisID. The reference frame URI is inherited from parent Vector')


    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        __constraint.name() : __constraint,
        __quality.name() : __quality,
        __codeSpace.name() : __codeSpace,
        __value.name() : __value
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        __referenceFrame.name() : __referenceFrame,
        __axisID.name() : __axisID
    })



# Complex type CTD_ANON_5 with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}valueList uses Python identifier valueList
    __valueList = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'valueList'), 'valueList', '__httpwww_opengis_netswe1_0_CTD_ANON_5_httpwww_opengis_netswe1_0valueList', True)

    
    valueList = property(__valueList.value, __valueList.set, None, u'List of allowed token values for this component')

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'id'), 'id', '__httpwww_opengis_netswe1_0_CTD_ANON_5_id', pyxb.binding.datatypes.ID)
    
    id = property(__id.value, __id.set, None, None)


    _ElementMap = {
        __valueList.name() : __valueList
    }
    _AttributeMap = {
        __id.name() : __id
    }



# Complex type TimeGeometricComplexPropertyType with content type ELEMENT_ONLY
class TimeGeometricComplexPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeGeometricComplexPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}TimeGeometricComplex uses Python identifier TimeGeometricComplex
    __TimeGeometricComplex = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeGeometricComplex'), 'TimeGeometricComplex', '__httpwww_opengis_netswe1_0_TimeGeometricComplexPropertyType_httpwww_opengis_netswe1_0TimeGeometricComplex', False)

    
    TimeGeometricComplex = property(__TimeGeometricComplex.value, __TimeGeometricComplex.set, None, u'Explicit implementation of ISO 19108 TM_GeometricComplex - a self-consistent set of TimeInstants and TimePeriods')

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_TimeGeometricComplexPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_TimeGeometricComplexPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_TimeGeometricComplexPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_TimeGeometricComplexPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_TimeGeometricComplexPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_TimeGeometricComplexPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_TimeGeometricComplexPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_TimeGeometricComplexPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)


    _ElementMap = {
        __TimeGeometricComplex.name() : __TimeGeometricComplex
    }
    _AttributeMap = {
        __role.name() : __role,
        __remoteSchema.name() : __remoteSchema,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __actuate.name() : __actuate,
        __type.name() : __type,
        __show.name() : __show,
        __href.name() : __href
    }
Namespace.addCategoryObject('typeBinding', u'TimeGeometricComplexPropertyType', TimeGeometricComplexPropertyType)


# Complex type NormalizedCurveType with content type ELEMENT_ONLY
class NormalizedCurveType (AbstractDataRecordType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NormalizedCurveType')
    # Base type is AbstractDataRecordType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}outputBias uses Python identifier outputBias
    __outputBias = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'outputBias'), 'outputBias', '__httpwww_opengis_netswe1_0_NormalizedCurveType_httpwww_opengis_netswe1_0outputBias', False)

    
    outputBias = property(__outputBias.value, __outputBias.set, None, None)

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}function uses Python identifier function
    __function = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'function'), 'function', '__httpwww_opengis_netswe1_0_NormalizedCurveType_httpwww_opengis_netswe1_0function', False)

    
    function = property(__function.value, __function.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}interpolationMethod uses Python identifier interpolationMethod
    __interpolationMethod = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'interpolationMethod'), 'interpolationMethod', '__httpwww_opengis_netswe1_0_NormalizedCurveType_httpwww_opengis_netswe1_0interpolationMethod', False)

    
    interpolationMethod = property(__interpolationMethod.value, __interpolationMethod.set, None, None)

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}inputBias uses Python identifier inputBias
    __inputBias = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'inputBias'), 'inputBias', '__httpwww_opengis_netswe1_0_NormalizedCurveType_httpwww_opengis_netswe1_0inputBias', False)

    
    inputBias = property(__inputBias.value, __inputBias.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}inputGain uses Python identifier inputGain
    __inputGain = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'inputGain'), 'inputGain', '__httpwww_opengis_netswe1_0_NormalizedCurveType_httpwww_opengis_netswe1_0inputGain', False)

    
    inputGain = property(__inputGain.value, __inputGain.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}outputGain uses Python identifier outputGain
    __outputGain = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'outputGain'), 'outputGain', '__httpwww_opengis_netswe1_0_NormalizedCurveType_httpwww_opengis_netswe1_0outputGain', False)

    
    outputGain = property(__outputGain.value, __outputGain.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}extrapolationMethod uses Python identifier extrapolationMethod
    __extrapolationMethod = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'extrapolationMethod'), 'extrapolationMethod', '__httpwww_opengis_netswe1_0_NormalizedCurveType_httpwww_opengis_netswe1_0extrapolationMethod', False)

    
    extrapolationMethod = property(__extrapolationMethod.value, __extrapolationMethod.set, None, None)

    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractDataRecordType._ElementMap.copy()
    _ElementMap.update({
        __outputBias.name() : __outputBias,
        __function.name() : __function,
        __interpolationMethod.name() : __interpolationMethod,
        __inputBias.name() : __inputBias,
        __inputGain.name() : __inputGain,
        __outputGain.name() : __outputGain,
        __extrapolationMethod.name() : __extrapolationMethod
    })
    _AttributeMap = AbstractDataRecordType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'NormalizedCurveType', NormalizedCurveType)


# Complex type QuantityPropertyType with content type ELEMENT_ONLY
class QuantityPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'QuantityPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Quantity uses Python identifier Quantity
    __Quantity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), 'Quantity', '__httpwww_opengis_netswe1_0_QuantityPropertyType_httpwww_opengis_netswe1_0Quantity', False)

    
    Quantity = property(__Quantity.value, __Quantity.set, None, u'Decimal number with optional unit and constraints')


    _ElementMap = {
        __Quantity.name() : __Quantity
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'QuantityPropertyType', QuantityPropertyType)


# Complex type VectorOrSquareMatrixPropertyType with content type ELEMENT_ONLY
class VectorOrSquareMatrixPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'VectorOrSquareMatrixPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Vector uses Python identifier Vector
    __Vector = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Vector'), 'Vector', '__httpwww_opengis_netswe1_0_VectorOrSquareMatrixPropertyType_httpwww_opengis_netswe1_0Vector', False)

    
    Vector = property(__Vector.value, __Vector.set, None, u'A Vector is a special type of DataRecord that takes a list of numerical scalars called coordinates. The Vector has a referenceFrame in which the coordinates are expressed')

    
    # Element {http://www.opengis.net/swe/1.0}SquareMatrix uses Python identifier SquareMatrix
    __SquareMatrix = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'SquareMatrix'), 'SquareMatrix', '__httpwww_opengis_netswe1_0_VectorOrSquareMatrixPropertyType_httpwww_opengis_netswe1_0SquareMatrix', False)

    
    SquareMatrix = property(__SquareMatrix.value, __SquareMatrix.set, None, u'This is a square matrix (so the size is the square of one dimension) which is a DataArray of Quantities. \t\tIt has a referenceFrame in which the matrix components are described')


    _ElementMap = {
        __Vector.name() : __Vector,
        __SquareMatrix.name() : __SquareMatrix
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'VectorOrSquareMatrixPropertyType', VectorOrSquareMatrixPropertyType)


# Complex type TypedValuePropertyType with content type ELEMENT_ONLY
class TypedValuePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TypedValuePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}TypedValue uses Python identifier TypedValue
    __TypedValue = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TypedValue'), 'TypedValue', '__httpwww_opengis_netswe1_0_TypedValuePropertyType_httpwww_opengis_netswe1_0TypedValue', False)

    
    TypedValue = property(__TypedValue.value, __TypedValue.set, None, u'A generic soft-typed value')


    _ElementMap = {
        __TypedValue.name() : __TypedValue
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TypedValuePropertyType', TypedValuePropertyType)


# Complex type CurvePropertyType with content type ELEMENT_ONLY
class CurvePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CurvePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Curve uses Python identifier Curve
    __Curve = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Curve'), 'Curve', '__httpwww_opengis_netswe1_0_CurvePropertyType_httpwww_opengis_netswe1_0Curve', False)

    
    Curve = property(__Curve.value, __Curve.set, None, u'Curve describing variations of a parameter vs. another quantity')


    _ElementMap = {
        __Curve.name() : __Curve
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'CurvePropertyType', CurvePropertyType)


# Complex type TypedValueListType with content type ELEMENT_ONLY
class TypedValueListType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TypedValueListType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}property uses Python identifier property_
    __property = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'property'), 'property_', '__httpwww_opengis_netswe1_0_TypedValueListType_httpwww_opengis_netswe1_0property', False)

    
    property_ = property(__property.value, __property.set, None, u'This element attribute indicates the semantics of the typed value. \n\t\t\t\t\tUsually identifies a property or phenomenon definition. ')

    
    # Element {http://www.opengis.net/swe/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netswe1_0_TypedValueListType_httpwww_opengis_netswe1_0value', True)

    
    value_ = property(__value.value, __value.set, None, u'Implicit xs:anyType')


    _ElementMap = {
        __property.name() : __property,
        __value.name() : __value
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TypedValueListType', TypedValueListType)


# Complex type AbstractEncodingType with content type EMPTY
class AbstractEncodingType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AbstractEncodingType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'id'), 'id', '__httpwww_opengis_netswe1_0_AbstractEncodingType_id', pyxb.binding.datatypes.ID)
    
    id = property(__id.value, __id.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __id.name() : __id
    }
Namespace.addCategoryObject('typeBinding', u'AbstractEncodingType', AbstractEncodingType)


# Complex type CTD_ANON_6 with content type EMPTY
class CTD_ANON_6 (AbstractEncodingType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractEncodingType
    
    # Attribute mimeType uses Python identifier mimeType
    __mimeType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'mimeType'), 'mimeType', '__httpwww_opengis_netswe1_0_CTD_ANON_6_mimeType', pyxb.binding.datatypes.token, required=True)
    
    mimeType = property(__mimeType.value, __mimeType.set, None, None)

    
    # Attribute id inherited from {http://www.opengis.net/swe/1.0}AbstractEncodingType

    _ElementMap = AbstractEncodingType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = AbstractEncodingType._AttributeMap.copy()
    _AttributeMap.update({
        __mimeType.name() : __mimeType
    })



# Complex type TimeAggregateType with content type ELEMENT_ONLY
class TimeAggregateType (pyxb.bundles.opengis.gml.AbstractTimeObjectType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeAggregateType')
    # Base type is pyxb.bundles.opengis.gml.AbstractTimeObjectType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}member uses Python identifier member
    __member = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'member'), 'member', '__httpwww_opengis_netswe1_0_TimeAggregateType_httpwww_opengis_netswe1_0member', True)

    
    member = property(__member.value, __member.set, None, None)

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = pyxb.bundles.opengis.gml.AbstractTimeObjectType._ElementMap.copy()
    _ElementMap.update({
        __member.name() : __member
    })
    _AttributeMap = pyxb.bundles.opengis.gml.AbstractTimeObjectType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'TimeAggregateType', TimeAggregateType)


# Complex type CTD_ANON_7 with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Component uses Python identifier Component
    __Component = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Component'), 'Component', '__httpwww_opengis_netswe1_0_CTD_ANON_7_httpwww_opengis_netswe1_0Component', False)

    
    Component = property(__Component.value, __Component.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}Block uses Python identifier Block
    __Block = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Block'), 'Block', '__httpwww_opengis_netswe1_0_CTD_ANON_7_httpwww_opengis_netswe1_0Block', False)

    
    Block = property(__Block.value, __Block.set, None, None)


    _ElementMap = {
        __Component.name() : __Component,
        __Block.name() : __Block
    }
    _AttributeMap = {
        
    }



# Complex type TimeGeometricComplexType with content type ELEMENT_ONLY
class TimeGeometricComplexType (pyxb.bundles.opengis.gml.AbstractTimeComplexType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeGeometricComplexType')
    # Base type is pyxb.bundles.opengis.gml.AbstractTimeComplexType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}primitive uses Python identifier primitive
    __primitive = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'primitive'), 'primitive', '__httpwww_opengis_netswe1_0_TimeGeometricComplexType_httpwww_opengis_netswe1_0primitive', True)

    
    primitive = property(__primitive.value, __primitive.set, None, u'Reference to an identified time primitive')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = pyxb.bundles.opengis.gml.AbstractTimeComplexType._ElementMap.copy()
    _ElementMap.update({
        __primitive.name() : __primitive
    })
    _AttributeMap = pyxb.bundles.opengis.gml.AbstractTimeComplexType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'TimeGeometricComplexType', TimeGeometricComplexType)


# Complex type CTD_ANON_8 with content type ELEMENT_ONLY
class CTD_ANON_8 (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractDataComponentType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netswe1_0_CTD_ANON_8_httpwww_opengis_netswe1_0value', False)

    
    value_ = property(__value.value, __value.set, None, u'Value is optional, to enable structure to act in a schema for values provided using other encodings')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        __value.name() : __value
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_9 with content type ELEMENT_ONLY
class CTD_ANON_9 (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractDataComponentType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}constraint uses Python identifier constraint
    __constraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'constraint'), 'constraint', '__httpwww_opengis_netswe1_0_CTD_ANON_9_httpwww_opengis_netswe1_0constraint', False)

    
    constraint = property(__constraint.value, __constraint.set, None, u'The constraint property defines the permitted values, as a range or enumerated list')

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}quality uses Python identifier quality
    __quality = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'quality'), 'quality', '__httpwww_opengis_netswe1_0_CTD_ANON_9_httpwww_opengis_netswe1_0quality', False)

    
    quality = property(__quality.value, __quality.set, None, u'The quality property provides an indication of the reliability of estimates of the asociated value')

    
    # Element {http://www.opengis.net/swe/1.0}uom uses Python identifier uom
    __uom = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uom'), 'uom', '__httpwww_opengis_netswe1_0_CTD_ANON_9_httpwww_opengis_netswe1_0uom', False)

    
    uom = property(__uom.value, __uom.set, None, u'Unit of measure')

    
    # Element {http://www.opengis.net/swe/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netswe1_0_CTD_ANON_9_httpwww_opengis_netswe1_0value', False)

    
    value_ = property(__value.value, __value.set, None, u'Value is optional, to enable structure to act in a schema for values provided using other encodings')

    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute referenceTime uses Python identifier referenceTime
    __referenceTime = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceTime'), 'referenceTime', '__httpwww_opengis_netswe1_0_CTD_ANON_9_referenceTime', timeIso8601)
    
    referenceTime = property(__referenceTime.value, __referenceTime.set, None, u'Specifies the origin of the temporal reference frame as an ISO8601 date (used to specify time after an epoch)')

    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute referenceFrame uses Python identifier referenceFrame
    __referenceFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceFrame'), 'referenceFrame', '__httpwww_opengis_netswe1_0_CTD_ANON_9_referenceFrame', pyxb.binding.datatypes.anyURI)
    
    referenceFrame = property(__referenceFrame.value, __referenceFrame.set, None, u'Points to a temporal reference frame definition. Time value will be expressed relative to this frame')

    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute localFrame uses Python identifier localFrame
    __localFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'localFrame'), 'localFrame', '__httpwww_opengis_netswe1_0_CTD_ANON_9_localFrame', pyxb.binding.datatypes.anyURI)
    
    localFrame = property(__localFrame.value, __localFrame.set, None, u'Specifies the temporal frame which origin is given by this time component')


    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        __constraint.name() : __constraint,
        __quality.name() : __quality,
        __uom.name() : __uom,
        __value.name() : __value
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        __referenceTime.name() : __referenceTime,
        __referenceFrame.name() : __referenceFrame,
        __localFrame.name() : __localFrame
    })



# Complex type DataRecordType with content type ELEMENT_ONLY
class DataRecordType (AbstractDataRecordType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataRecordType')
    # Base type is AbstractDataRecordType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}field uses Python identifier field
    __field = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'field'), 'field', '__httpwww_opengis_netswe1_0_DataRecordType_httpwww_opengis_netswe1_0field', True)

    
    field = property(__field.value, __field.set, None, None)

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractDataRecordType._ElementMap.copy()
    _ElementMap.update({
        __field.name() : __field
    })
    _AttributeMap = AbstractDataRecordType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'DataRecordType', DataRecordType)


# Complex type XMLDataPropertyType with content type ELEMENT_ONLY
class XMLDataPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'XMLDataPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Item uses Python identifier Item
    __Item = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Item'), 'Item', '__httpwww_opengis_netswe1_0_XMLDataPropertyType_httpwww_opengis_netswe1_0Item', False)

    
    Item = property(__Item.value, __Item.set, None, u'An Item is an item of data of any type')

    
    # Element {http://www.opengis.net/swe/1.0}Record uses Python identifier Record
    __Record = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Record'), 'Record', '__httpwww_opengis_netswe1_0_XMLDataPropertyType_httpwww_opengis_netswe1_0Record', False)

    
    Record = property(__Record.value, __Record.set, None, u'A record is a list of fields')

    
    # Element {http://www.opengis.net/swe/1.0}Array uses Python identifier Array
    __Array = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Array'), 'Array', '__httpwww_opengis_netswe1_0_XMLDataPropertyType_httpwww_opengis_netswe1_0Array', False)

    
    Array = property(__Array.value, __Array.set, None, u'An array is an indexed set of records of homogeneous type')


    _ElementMap = {
        __Item.name() : __Item,
        __Record.name() : __Record,
        __Array.name() : __Array
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'XMLDataPropertyType', XMLDataPropertyType)


# Complex type CTD_ANON_10 with content type EMPTY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute bitLength uses Python identifier bitLength
    __bitLength = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'bitLength'), 'bitLength', '__httpwww_opengis_netswe1_0_CTD_ANON_10_bitLength', pyxb.binding.datatypes.positiveInteger)
    
    bitLength = property(__bitLength.value, __bitLength.set, None, None)

    
    # Attribute paddingBits-before uses Python identifier paddingBits_before
    __paddingBits_before = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'paddingBits-before'), 'paddingBits_before', '__httpwww_opengis_netswe1_0_CTD_ANON_10_paddingBits_before', pyxb.binding.datatypes.nonNegativeInteger, unicode_default=u'0')
    
    paddingBits_before = property(__paddingBits_before.value, __paddingBits_before.set, None, None)

    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ref'), 'ref', '__httpwww_opengis_netswe1_0_CTD_ANON_10_ref', pyxb.binding.datatypes.token, required=True)
    
    ref = property(__ref.value, __ref.set, None, None)

    
    # Attribute paddingBits-after uses Python identifier paddingBits_after
    __paddingBits_after = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'paddingBits-after'), 'paddingBits_after', '__httpwww_opengis_netswe1_0_CTD_ANON_10_paddingBits_after', pyxb.binding.datatypes.nonNegativeInteger, unicode_default=u'0')
    
    paddingBits_after = property(__paddingBits_after.value, __paddingBits_after.set, None, None)

    
    # Attribute encryption uses Python identifier encryption
    __encryption = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'encryption'), 'encryption', '__httpwww_opengis_netswe1_0_CTD_ANON_10_encryption', pyxb.binding.datatypes.anyURI)
    
    encryption = property(__encryption.value, __encryption.set, None, None)

    
    # Attribute significantBits uses Python identifier significantBits
    __significantBits = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'significantBits'), 'significantBits', '__httpwww_opengis_netswe1_0_CTD_ANON_10_significantBits', pyxb.binding.datatypes.positiveInteger)
    
    significantBits = property(__significantBits.value, __significantBits.set, None, None)

    
    # Attribute dataType uses Python identifier dataType
    __dataType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dataType'), 'dataType', '__httpwww_opengis_netswe1_0_CTD_ANON_10_dataType', pyxb.binding.datatypes.anyURI)
    
    dataType = property(__dataType.value, __dataType.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __bitLength.name() : __bitLength,
        __paddingBits_before.name() : __paddingBits_before,
        __ref.name() : __ref,
        __paddingBits_after.name() : __paddingBits_after,
        __encryption.name() : __encryption,
        __significantBits.name() : __significantBits,
        __dataType.name() : __dataType
    }



# Complex type DataArrayPropertyType with content type ELEMENT_ONLY
class DataArrayPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataArrayPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}DataArray uses Python identifier DataArray
    __DataArray = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'DataArray'), 'DataArray', '__httpwww_opengis_netswe1_0_DataArrayPropertyType_httpwww_opengis_netswe1_0DataArray', False)

    
    DataArray = property(__DataArray.value, __DataArray.set, None, u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways')


    _ElementMap = {
        __DataArray.name() : __DataArray
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'DataArrayPropertyType', DataArrayPropertyType)


# Complex type ArrayType with content type ELEMENT_ONLY
class ArrayType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ArrayType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}element uses Python identifier element
    __element = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'element'), 'element', '__httpwww_opengis_netswe1_0_ArrayType_httpwww_opengis_netswe1_0element', True)

    
    element = property(__element.value, __element.set, None, u'An Array/element contains an Item or a Record or an Array')

    
    # Attribute RS uses Python identifier RS
    __RS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'RS'), 'RS', '__httpwww_opengis_netswe1_0_ArrayType_RS', pyxb.binding.datatypes.anyURI)
    
    RS = property(__RS.value, __RS.set, None, u'Optional pointer to the record-type schema. This should be used when the elements of the array are Records')

    
    # Attribute elementCount uses Python identifier elementCount
    __elementCount = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'elementCount'), 'elementCount', '__httpwww_opengis_netswe1_0_ArrayType_elementCount', pyxb.binding.datatypes.positiveInteger)
    
    elementCount = property(__elementCount.value, __elementCount.set, None, u'Optional count of the number of elements in the array. ')


    _ElementMap = {
        __element.name() : __element
    }
    _AttributeMap = {
        __RS.name() : __RS,
        __elementCount.name() : __elementCount
    }
Namespace.addCategoryObject('typeBinding', u'ArrayType', ArrayType)


# Complex type CTD_ANON_11 with content type ELEMENT_ONLY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Count uses Python identifier Count
    __Count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Count'), 'Count', '__httpwww_opengis_netswe1_0_CTD_ANON_11_httpwww_opengis_netswe1_0Count', False)

    
    Count = property(__Count.value, __Count.set, None, u'Integer number used for a counting value')

    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ref'), 'ref', '__httpwww_opengis_netswe1_0_CTD_ANON_11_ref', pyxb.binding.datatypes.IDREF)
    
    ref = property(__ref.value, __ref.set, None, u'If present, the array size is variable and should be obtained from the referenced component.\n\t\t\t                    The referenced component must occur before the array values in a data stream to allow parsing.')


    _ElementMap = {
        __Count.name() : __Count
    }
    _AttributeMap = {
        __ref.name() : __ref
    }



# Complex type TimeGridType with content type ELEMENT_ONLY
class TimeGridType (pyxb.bundles.opengis.gml.AbstractTimeComplexType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeGridType')
    # Base type is pyxb.bundles.opengis.gml.AbstractTimeComplexType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}origin uses Python identifier origin
    __origin = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'origin'), 'origin', '__httpwww_opengis_netswe1_0_TimeGridType_httpwww_opengis_netswe1_0origin', False)

    
    origin = property(__origin.value, __origin.set, None, u'Reference to an identified time instant')

    
    # Element {http://www.opengis.net/swe/1.0}duration uses Python identifier duration
    __duration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'duration'), 'duration', '__httpwww_opengis_netswe1_0_TimeGridType_httpwww_opengis_netswe1_0duration', False)

    
    duration = property(__duration.value, __duration.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}offsetDuration uses Python identifier offsetDuration
    __offsetDuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'offsetDuration'), 'offsetDuration', '__httpwww_opengis_netswe1_0_TimeGridType_httpwww_opengis_netswe1_0offsetDuration', False)

    
    offsetDuration = property(__offsetDuration.value, __offsetDuration.set, None, u'XML Schema built-in simple type for duration: e.g. \n                P1Y (1 year) \n                P1M (1 month) \n                P1DT12H (1 day 12 hours) \n                PT5M (5 minutes) \n                PT0.007S (7 milliseconds)')

    
    # Element {http://www.opengis.net/swe/1.0}originPos uses Python identifier originPos
    __originPos = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'originPos'), 'originPos', '__httpwww_opengis_netswe1_0_TimeGridType_httpwww_opengis_netswe1_0originPos', False)

    
    originPos = property(__originPos.value, __originPos.set, None, u'Simple-content time position')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}offsetInterval uses Python identifier offsetInterval
    __offsetInterval = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'offsetInterval'), 'offsetInterval', '__httpwww_opengis_netswe1_0_TimeGridType_httpwww_opengis_netswe1_0offsetInterval', False)

    
    offsetInterval = property(__offsetInterval.value, __offsetInterval.set, None, u'representation of the ISO 11404 model of a time interval length: e.g. \n                value=1, unit="year"  \n                value=1, unit="other:month" (or see next)\n                value=1, unit="year" radix="12" factor="1" (1/12 year)\n                value=1.5, unit="day"  \n                value=36, unit="hour" \n                value=5, unit="minute"  \n                value=7, unit="second" radix="10" factor="3" (7 milliseconds)')

    
    # Element {http://www.opengis.net/swe/1.0}extent uses Python identifier extent
    __extent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'extent'), 'extent', '__httpwww_opengis_netswe1_0_TimeGridType_httpwww_opengis_netswe1_0extent', False)

    
    extent = property(__extent.value, __extent.set, None, None)

    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = pyxb.bundles.opengis.gml.AbstractTimeComplexType._ElementMap.copy()
    _ElementMap.update({
        __origin.name() : __origin,
        __duration.name() : __duration,
        __offsetDuration.name() : __offsetDuration,
        __originPos.name() : __originPos,
        __offsetInterval.name() : __offsetInterval,
        __extent.name() : __extent
    })
    _AttributeMap = pyxb.bundles.opengis.gml.AbstractTimeComplexType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'TimeGridType', TimeGridType)


# Complex type TimeInstantGridType with content type ELEMENT_ONLY
class TimeInstantGridType (TimeGridType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeInstantGridType')
    # Base type is TimeGridType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element origin ({http://www.opengis.net/swe/1.0}origin) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Element duration ({http://www.opengis.net/swe/1.0}duration) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Element offsetDuration ({http://www.opengis.net/swe/1.0}offsetDuration) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Element originPos ({http://www.opengis.net/swe/1.0}originPos) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element offsetInterval ({http://www.opengis.net/swe/1.0}offsetInterval) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Element extent ({http://www.opengis.net/swe/1.0}extent) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = TimeGridType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = TimeGridType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'TimeInstantGridType', TimeInstantGridType)


# Complex type CodeSpacePropertyType with content type EMPTY
class CodeSpacePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CodeSpacePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_CodeSpacePropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_CodeSpacePropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_CodeSpacePropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_CodeSpacePropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_CodeSpacePropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_CodeSpacePropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_CodeSpacePropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_CodeSpacePropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")


    _ElementMap = {
        
    }
    _AttributeMap = {
        __remoteSchema.name() : __remoteSchema,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __role.name() : __role,
        __show.name() : __show,
        __href.name() : __href,
        __type.name() : __type,
        __actuate.name() : __actuate
    }
Namespace.addCategoryObject('typeBinding', u'CodeSpacePropertyType', CodeSpacePropertyType)


# Complex type ArrayPropertyType with content type ELEMENT_ONLY
class ArrayPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ArrayPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Array uses Python identifier Array
    __Array = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Array'), 'Array', '__httpwww_opengis_netswe1_0_ArrayPropertyType_httpwww_opengis_netswe1_0Array', False)

    
    Array = property(__Array.value, __Array.set, None, u'An array is an indexed set of records of homogeneous type')


    _ElementMap = {
        __Array.name() : __Array
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ArrayPropertyType', ArrayPropertyType)


# Complex type DataComponentPropertyType with content type ELEMENT_ONLY
class DataComponentPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataComponentPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Quantity uses Python identifier Quantity
    __Quantity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), 'Quantity', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netswe1_0Quantity', False)

    
    Quantity = property(__Quantity.value, __Quantity.set, None, u'Decimal number with optional unit and constraints')

    
    # Element {http://www.opengis.net/swe/1.0}Time uses Python identifier Time
    __Time = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Time'), 'Time', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netswe1_0Time', False)

    
    Time = property(__Time.value, __Time.set, None, u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin')

    
    # Element {http://www.opengis.net/swe/1.0}QuantityRange uses Python identifier QuantityRange
    __QuantityRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), 'QuantityRange', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netswe1_0QuantityRange', False)

    
    QuantityRange = property(__QuantityRange.value, __QuantityRange.set, None, u'Decimal pair for specifying a quantity range with constraints')

    
    # Element {http://www.opengis.net/swe/1.0}AbstractDataRecord uses Python identifier AbstractDataRecord
    __AbstractDataRecord = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord'), 'AbstractDataRecord', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netswe1_0AbstractDataRecord', False)

    
    AbstractDataRecord = property(__AbstractDataRecord.value, __AbstractDataRecord.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}Text uses Python identifier Text
    __Text = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Text'), 'Text', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netswe1_0Text', False)

    
    Text = property(__Text.value, __Text.set, None, u'Free textual component')

    
    # Element {http://www.opengis.net/swe/1.0}CountRange uses Python identifier CountRange
    __CountRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'CountRange'), 'CountRange', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netswe1_0CountRange', False)

    
    CountRange = property(__CountRange.value, __CountRange.set, None, u'Integer pair used for specifying a count range')

    
    # Element {http://www.opengis.net/swe/1.0}Boolean uses Python identifier Boolean
    __Boolean = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), 'Boolean', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netswe1_0Boolean', False)

    
    Boolean = property(__Boolean.value, __Boolean.set, None, u'Scalar component used to express truth: True or False, 0 or 1')

    
    # Element {http://www.opengis.net/swe/1.0}AbstractDataArray uses Python identifier AbstractDataArray
    __AbstractDataArray = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray'), 'AbstractDataArray', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netswe1_0AbstractDataArray', False)

    
    AbstractDataArray = property(__AbstractDataArray.value, __AbstractDataArray.set, None, u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways')

    
    # Element {http://www.opengis.net/swe/1.0}Count uses Python identifier Count
    __Count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Count'), 'Count', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netswe1_0Count', False)

    
    Count = property(__Count.value, __Count.set, None, u'Integer number used for a counting value')

    
    # Element {http://www.opengis.net/swe/1.0}TimeRange uses Python identifier TimeRange
    __TimeRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeRange'), 'TimeRange', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netswe1_0TimeRange', False)

    
    TimeRange = property(__TimeRange.value, __TimeRange.set, None, u'Time value pair for specifying a time range (can be a decimal or ISO 8601)')

    
    # Element {http://www.opengis.net/swe/1.0}Category uses Python identifier Category
    __Category = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Category'), 'Category', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netswe1_0Category', False)

    
    Category = property(__Category.value, __Category.set, None, u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value')

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_name', pyxb.binding.datatypes.token, required=True)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_DataComponentPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)


    _ElementMap = {
        __Quantity.name() : __Quantity,
        __Time.name() : __Time,
        __QuantityRange.name() : __QuantityRange,
        __AbstractDataRecord.name() : __AbstractDataRecord,
        __Text.name() : __Text,
        __CountRange.name() : __CountRange,
        __Boolean.name() : __Boolean,
        __AbstractDataArray.name() : __AbstractDataArray,
        __Count.name() : __Count,
        __TimeRange.name() : __TimeRange,
        __Category.name() : __Category
    }
    _AttributeMap = {
        __remoteSchema.name() : __remoteSchema,
        __actuate.name() : __actuate,
        __name.name() : __name,
        __arcrole.name() : __arcrole,
        __role.name() : __role,
        __show.name() : __show,
        __type.name() : __type,
        __href.name() : __href,
        __title.name() : __title
    }
Namespace.addCategoryObject('typeBinding', u'DataComponentPropertyType', DataComponentPropertyType)


# Complex type QualityPropertyType with content type ELEMENT_ONLY
class QualityPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'QualityPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Quantity uses Python identifier Quantity
    __Quantity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), 'Quantity', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_opengis_netswe1_0Quantity', False)

    
    Quantity = property(__Quantity.value, __Quantity.set, None, u'Decimal number with optional unit and constraints')

    
    # Element {http://www.opengis.net/swe/1.0}QuantityRange uses Python identifier QuantityRange
    __QuantityRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), 'QuantityRange', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_opengis_netswe1_0QuantityRange', False)

    
    QuantityRange = property(__QuantityRange.value, __QuantityRange.set, None, u'Decimal pair for specifying a quantity range with constraints')

    
    # Element {http://www.opengis.net/swe/1.0}Text uses Python identifier Text
    __Text = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Text'), 'Text', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_opengis_netswe1_0Text', False)

    
    Text = property(__Text.value, __Text.set, None, u'Free textual component')

    
    # Element {http://www.opengis.net/swe/1.0}Category uses Python identifier Category
    __Category = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Category'), 'Category', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_opengis_netswe1_0Category', False)

    
    Category = property(__Category.value, __Category.set, None, u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value')

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_QualityPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")


    _ElementMap = {
        __Quantity.name() : __Quantity,
        __QuantityRange.name() : __QuantityRange,
        __Text.name() : __Text,
        __Category.name() : __Category
    }
    _AttributeMap = {
        __actuate.name() : __actuate,
        __href.name() : __href,
        __remoteSchema.name() : __remoteSchema,
        __role.name() : __role,
        __type.name() : __type,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __show.name() : __show
    }
Namespace.addCategoryObject('typeBinding', u'QualityPropertyType', QualityPropertyType)


# Complex type IntervalType with content type ELEMENT_ONLY
class IntervalType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IntervalType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}upperBound uses Python identifier upperBound
    __upperBound = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'upperBound'), 'upperBound', '__httpwww_opengis_netswe1_0_IntervalType_httpwww_opengis_netswe1_0upperBound', False)

    
    upperBound = property(__upperBound.value, __upperBound.set, None, u'Implicit xs:anyType')

    
    # Element {http://www.opengis.net/swe/1.0}lowerBound uses Python identifier lowerBound
    __lowerBound = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lowerBound'), 'lowerBound', '__httpwww_opengis_netswe1_0_IntervalType_httpwww_opengis_netswe1_0lowerBound', False)

    
    lowerBound = property(__lowerBound.value, __lowerBound.set, None, u'Implicit xs:anyType')


    _ElementMap = {
        __upperBound.name() : __upperBound,
        __lowerBound.name() : __lowerBound
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'IntervalType', IntervalType)


# Complex type DataValuePropertyType with content type MIXED
class DataValuePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataValuePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_DataValuePropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_DataValuePropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_DataValuePropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_DataValuePropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_DataValuePropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_DataValuePropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_DataValuePropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_DataValuePropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _HasWildcardElement = True

    _ElementMap = {
        
    }
    _AttributeMap = {
        __role.name() : __role,
        __type.name() : __type,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __actuate.name() : __actuate,
        __show.name() : __show,
        __remoteSchema.name() : __remoteSchema,
        __href.name() : __href
    }
Namespace.addCategoryObject('typeBinding', u'DataValuePropertyType', DataValuePropertyType)


# Complex type TextPropertyType with content type ELEMENT_ONLY
class TextPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TextPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Text uses Python identifier Text
    __Text = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Text'), 'Text', '__httpwww_opengis_netswe1_0_TextPropertyType_httpwww_opengis_netswe1_0Text', False)

    
    Text = property(__Text.value, __Text.set, None, u'Free textual component')


    _ElementMap = {
        __Text.name() : __Text
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TextPropertyType', TextPropertyType)


# Complex type BlockEncodingPropertyType with content type ELEMENT_ONLY
class BlockEncodingPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BlockEncodingPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}TextBlock uses Python identifier TextBlock
    __TextBlock = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TextBlock'), 'TextBlock', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_opengis_netswe1_0TextBlock', False)

    
    TextBlock = property(__TextBlock.value, __TextBlock.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}XMLBlock uses Python identifier XMLBlock
    __XMLBlock = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'XMLBlock'), 'XMLBlock', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_opengis_netswe1_0XMLBlock', False)

    
    XMLBlock = property(__XMLBlock.value, __XMLBlock.set, None, u'Carries the designator for an element implementing an XML-encoded data-type')

    
    # Element {http://www.opengis.net/swe/1.0}StandardFormat uses Python identifier StandardFormat
    __StandardFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'StandardFormat'), 'StandardFormat', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_opengis_netswe1_0StandardFormat', False)

    
    StandardFormat = property(__StandardFormat.value, __StandardFormat.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}BinaryBlock uses Python identifier BinaryBlock
    __BinaryBlock = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'BinaryBlock'), 'BinaryBlock', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_opengis_netswe1_0BinaryBlock', False)

    
    BinaryBlock = property(__BinaryBlock.value, __BinaryBlock.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_BlockEncodingPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")


    _ElementMap = {
        __TextBlock.name() : __TextBlock,
        __XMLBlock.name() : __XMLBlock,
        __StandardFormat.name() : __StandardFormat,
        __BinaryBlock.name() : __BinaryBlock
    }
    _AttributeMap = {
        __remoteSchema.name() : __remoteSchema,
        __role.name() : __role,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __show.name() : __show,
        __type.name() : __type,
        __href.name() : __href,
        __actuate.name() : __actuate
    }
Namespace.addCategoryObject('typeBinding', u'BlockEncodingPropertyType', BlockEncodingPropertyType)


# Complex type SimpleDataPropertyType with content type ELEMENT_ONLY
class SimpleDataPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SimpleDataPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}AbstractDataRecord uses Python identifier AbstractDataRecord
    __AbstractDataRecord = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord'), 'AbstractDataRecord', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netswe1_0AbstractDataRecord', False)

    
    AbstractDataRecord = property(__AbstractDataRecord.value, __AbstractDataRecord.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}CountRange uses Python identifier CountRange
    __CountRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'CountRange'), 'CountRange', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netswe1_0CountRange', False)

    
    CountRange = property(__CountRange.value, __CountRange.set, None, u'Integer pair used for specifying a count range')

    
    # Element {http://www.opengis.net/swe/1.0}Count uses Python identifier Count
    __Count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Count'), 'Count', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netswe1_0Count', False)

    
    Count = property(__Count.value, __Count.set, None, u'Integer number used for a counting value')

    
    # Element {http://www.opengis.net/swe/1.0}Category uses Python identifier Category
    __Category = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Category'), 'Category', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netswe1_0Category', False)

    
    Category = property(__Category.value, __Category.set, None, u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value')

    
    # Element {http://www.opengis.net/swe/1.0}AbstractDataArray uses Python identifier AbstractDataArray
    __AbstractDataArray = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray'), 'AbstractDataArray', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netswe1_0AbstractDataArray', False)

    
    AbstractDataArray = property(__AbstractDataArray.value, __AbstractDataArray.set, None, u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways')

    
    # Element {http://www.opengis.net/swe/1.0}TimeRange uses Python identifier TimeRange
    __TimeRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeRange'), 'TimeRange', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netswe1_0TimeRange', False)

    
    TimeRange = property(__TimeRange.value, __TimeRange.set, None, u'Time value pair for specifying a time range (can be a decimal or ISO 8601)')

    
    # Element {http://www.opengis.net/swe/1.0}Time uses Python identifier Time
    __Time = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Time'), 'Time', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netswe1_0Time', False)

    
    Time = property(__Time.value, __Time.set, None, u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin')

    
    # Element {http://www.opengis.net/swe/1.0}Quantity uses Python identifier Quantity
    __Quantity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), 'Quantity', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netswe1_0Quantity', False)

    
    Quantity = property(__Quantity.value, __Quantity.set, None, u'Decimal number with optional unit and constraints')

    
    # Element {http://www.opengis.net/swe/1.0}QuantityRange uses Python identifier QuantityRange
    __QuantityRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), 'QuantityRange', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netswe1_0QuantityRange', False)

    
    QuantityRange = property(__QuantityRange.value, __QuantityRange.set, None, u'Decimal pair for specifying a quantity range with constraints')

    
    # Element {http://www.opengis.net/swe/1.0}Text uses Python identifier Text
    __Text = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Text'), 'Text', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netswe1_0Text', False)

    
    Text = property(__Text.value, __Text.set, None, u'Free textual component')

    
    # Element {http://www.opengis.net/swe/1.0}Boolean uses Python identifier Boolean
    __Boolean = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), 'Boolean', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netswe1_0Boolean', False)

    
    Boolean = property(__Boolean.value, __Boolean.set, None, u'Scalar component used to express truth: True or False, 0 or 1')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_SimpleDataPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')


    _ElementMap = {
        __AbstractDataRecord.name() : __AbstractDataRecord,
        __CountRange.name() : __CountRange,
        __Count.name() : __Count,
        __Category.name() : __Category,
        __AbstractDataArray.name() : __AbstractDataArray,
        __TimeRange.name() : __TimeRange,
        __Time.name() : __Time,
        __Quantity.name() : __Quantity,
        __QuantityRange.name() : __QuantityRange,
        __Text.name() : __Text,
        __Boolean.name() : __Boolean
    }
    _AttributeMap = {
        __href.name() : __href,
        __role.name() : __role,
        __type.name() : __type,
        __show.name() : __show,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __actuate.name() : __actuate,
        __remoteSchema.name() : __remoteSchema
    }
Namespace.addCategoryObject('typeBinding', u'SimpleDataPropertyType', SimpleDataPropertyType)


# Complex type UomPropertyType with content type ELEMENT_ONLY
class UomPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'UomPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/gml}UnitDefinition uses Python identifier UnitDefinition
    __UnitDefinition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'UnitDefinition'), 'UnitDefinition', '__httpwww_opengis_netswe1_0_UomPropertyType_httpwww_opengis_netgmlUnitDefinition', False)

    
    UnitDefinition = property(__UnitDefinition.value, __UnitDefinition.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_UomPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_UomPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute code uses Python identifier code
    __code = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'code'), 'code', '__httpwww_opengis_netswe1_0_UomPropertyType_code', UomSymbol)
    
    code = property(__code.value, __code.set, None, u'Specifies a unit by using a UCUM expression (prefered)')

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_UomPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_UomPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_UomPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_UomPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_UomPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_UomPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)


    _ElementMap = {
        __UnitDefinition.name() : __UnitDefinition
    }
    _AttributeMap = {
        __show.name() : __show,
        __href.name() : __href,
        __code.name() : __code,
        __remoteSchema.name() : __remoteSchema,
        __arcrole.name() : __arcrole,
        __role.name() : __role,
        __title.name() : __title,
        __actuate.name() : __actuate,
        __type.name() : __type
    }
Namespace.addCategoryObject('typeBinding', u'UomPropertyType', UomPropertyType)


# Complex type CTD_ANON_12 with content type ELEMENT_ONLY
class CTD_ANON_12 (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractDataComponentType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}quality uses Python identifier quality
    __quality = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'quality'), 'quality', '__httpwww_opengis_netswe1_0_CTD_ANON_12_httpwww_opengis_netswe1_0quality', True)

    
    quality = property(__quality.value, __quality.set, None, u'The quality property provides an indication of the reliability of estimates of the asociated value')

    
    # Element {http://www.opengis.net/swe/1.0}uom uses Python identifier uom
    __uom = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uom'), 'uom', '__httpwww_opengis_netswe1_0_CTD_ANON_12_httpwww_opengis_netswe1_0uom', False)

    
    uom = property(__uom.value, __uom.set, None, u'Unit of measure')

    
    # Element {http://www.opengis.net/swe/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netswe1_0_CTD_ANON_12_httpwww_opengis_netswe1_0value', False)

    
    value_ = property(__value.value, __value.set, None, u'Value is optional, to enable structure to act in a schema for values provided using other encodings')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}constraint uses Python identifier constraint
    __constraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'constraint'), 'constraint', '__httpwww_opengis_netswe1_0_CTD_ANON_12_httpwww_opengis_netswe1_0constraint', False)

    
    constraint = property(__constraint.value, __constraint.set, None, u'The constraint property defines the permitted values, as a range or enumerated list')

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute referenceFrame uses Python identifier referenceFrame
    __referenceFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceFrame'), 'referenceFrame', '__httpwww_opengis_netswe1_0_CTD_ANON_12_referenceFrame', pyxb.binding.datatypes.anyURI)
    
    referenceFrame = property(__referenceFrame.value, __referenceFrame.set, None, u'A reference frame anchors a value to a datum or interval scale')

    
    # Attribute axisID uses Python identifier axisID
    __axisID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'axisID'), 'axisID', '__httpwww_opengis_netswe1_0_CTD_ANON_12_axisID', pyxb.binding.datatypes.token)
    
    axisID = property(__axisID.value, __axisID.set, None, u'Specifies the reference axis using the gml:axisID. The reference frame URI is inherited from parent Vector')


    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        __quality.name() : __quality,
        __uom.name() : __uom,
        __value.name() : __value,
        __constraint.name() : __constraint
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        __referenceFrame.name() : __referenceFrame,
        __axisID.name() : __axisID
    })



# Complex type CTD_ANON_13 with content type ELEMENT_ONLY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}max uses Python identifier max
    __max = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'max'), 'max', '__httpwww_opengis_netswe1_0_CTD_ANON_13_httpwww_opengis_netswe1_0max', False)

    
    max = property(__max.value, __max.set, None, u'Specifies maximum allowed value for an open interval (no min)')

    
    # Element {http://www.opengis.net/swe/1.0}interval uses Python identifier interval
    __interval = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'interval'), 'interval', '__httpwww_opengis_netswe1_0_CTD_ANON_13_httpwww_opengis_netswe1_0interval', True)

    
    interval = property(__interval.value, __interval.set, None, u'Range of allowed values (closed interval) for this component')

    
    # Element {http://www.opengis.net/swe/1.0}min uses Python identifier min
    __min = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'min'), 'min', '__httpwww_opengis_netswe1_0_CTD_ANON_13_httpwww_opengis_netswe1_0min', False)

    
    min = property(__min.value, __min.set, None, u'Specifies minimum allowed value for an open interval (no max)')

    
    # Element {http://www.opengis.net/swe/1.0}valueList uses Python identifier valueList
    __valueList = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'valueList'), 'valueList', '__httpwww_opengis_netswe1_0_CTD_ANON_13_httpwww_opengis_netswe1_0valueList', True)

    
    valueList = property(__valueList.value, __valueList.set, None, u'List of allowed values for this component')

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'id'), 'id', '__httpwww_opengis_netswe1_0_CTD_ANON_13_id', pyxb.binding.datatypes.ID)
    
    id = property(__id.value, __id.set, None, None)


    _ElementMap = {
        __max.name() : __max,
        __interval.name() : __interval,
        __min.name() : __min,
        __valueList.name() : __valueList
    }
    _AttributeMap = {
        __id.name() : __id
    }



# Complex type AbstractDataArrayType with content type ELEMENT_ONLY
class AbstractDataArrayType (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArrayType')
    # Base type is AbstractDataComponentType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}elementCount uses Python identifier elementCount
    __elementCount = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'elementCount'), 'elementCount', '__httpwww_opengis_netswe1_0_AbstractDataArrayType_httpwww_opengis_netswe1_0elementCount', False)

    
    elementCount = property(__elementCount.value, __elementCount.set, None, u'Specifies the size of the array (i.e. the number of elements of the defined type it contains)')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        __elementCount.name() : __elementCount
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AbstractDataArrayType', AbstractDataArrayType)


# Complex type DataArrayType with content type ELEMENT_ONLY
class DataArrayType (AbstractDataArrayType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataArrayType')
    # Base type is AbstractDataArrayType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element elementCount ({http://www.opengis.net/swe/1.0}elementCount) inherited from {http://www.opengis.net/swe/1.0}AbstractDataArrayType
    
    # Element {http://www.opengis.net/swe/1.0}encoding uses Python identifier encoding
    __encoding = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'encoding'), 'encoding', '__httpwww_opengis_netswe1_0_DataArrayType_httpwww_opengis_netswe1_0encoding', False)

    
    encoding = property(__encoding.value, __encoding.set, None, u'Specifies an encoding for the data structure defined by the enclosing element')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}elementType uses Python identifier elementType
    __elementType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'elementType'), 'elementType', '__httpwww_opengis_netswe1_0_DataArrayType_httpwww_opengis_netswe1_0elementType', False)

    
    elementType = property(__elementType.value, __elementType.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}values uses Python identifier values
    __values = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'values'), 'values', '__httpwww_opengis_netswe1_0_DataArrayType_httpwww_opengis_netswe1_0values', False)

    
    values = property(__values.value, __values.set, None, u'Carries the block of values encoded as specified by the encoding element')

    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractDataArrayType._ElementMap.copy()
    _ElementMap.update({
        __encoding.name() : __encoding,
        __elementType.name() : __elementType,
        __values.name() : __values
    })
    _AttributeMap = AbstractDataArrayType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'DataArrayType', DataArrayType)


# Complex type TimeIntervalGridType with content type ELEMENT_ONLY
class TimeIntervalGridType (TimeGridType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeIntervalGridType')
    # Base type is TimeGridType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element origin ({http://www.opengis.net/swe/1.0}origin) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Element {http://www.opengis.net/swe/1.0}windowInterval uses Python identifier windowInterval
    __windowInterval = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'windowInterval'), 'windowInterval', '__httpwww_opengis_netswe1_0_TimeIntervalGridType_httpwww_opengis_netswe1_0windowInterval', False)

    
    windowInterval = property(__windowInterval.value, __windowInterval.set, None, u'representation of the ISO 11404 model of a time interval length')

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element originPos ({http://www.opengis.net/swe/1.0}originPos) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Element offsetDuration ({http://www.opengis.net/swe/1.0}offsetDuration) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Element {http://www.opengis.net/swe/1.0}windowDuration uses Python identifier windowDuration
    __windowDuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'windowDuration'), 'windowDuration', '__httpwww_opengis_netswe1_0_TimeIntervalGridType_httpwww_opengis_netswe1_0windowDuration', False)

    
    windowDuration = property(__windowDuration.value, __windowDuration.set, None, u'XML Schema built-in simple type for duration')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element duration ({http://www.opengis.net/swe/1.0}duration) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Element offsetInterval ({http://www.opengis.net/swe/1.0}offsetInterval) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Element extent ({http://www.opengis.net/swe/1.0}extent) inherited from {http://www.opengis.net/swe/1.0}TimeGridType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = TimeGridType._ElementMap.copy()
    _ElementMap.update({
        __windowInterval.name() : __windowInterval,
        __windowDuration.name() : __windowDuration
    })
    _AttributeMap = TimeGridType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'TimeIntervalGridType', TimeIntervalGridType)


# Complex type PhenomenonType with content type ELEMENT_ONLY
class PhenomenonType (pyxb.bundles.opengis.gml.DefinitionType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PhenomenonType')
    # Base type is pyxb.bundles.opengis.gml.DefinitionType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute id_ inherited from {http://www.opengis.net/gml}DefinitionType

    _ElementMap = pyxb.bundles.opengis.gml.DefinitionType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = pyxb.bundles.opengis.gml.DefinitionType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'PhenomenonType', PhenomenonType)


# Complex type CompoundPhenomenonType with content type ELEMENT_ONLY
class CompoundPhenomenonType (PhenomenonType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CompoundPhenomenonType')
    # Base type is PhenomenonType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute dimension uses Python identifier dimension
    __dimension = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dimension'), 'dimension', '__httpwww_opengis_netswe1_0_CompoundPhenomenonType_dimension', pyxb.binding.datatypes.positiveInteger, required=True)
    
    dimension = property(__dimension.value, __dimension.set, None, u'The number of components in the tuple')

    
    # Attribute id_ inherited from {http://www.opengis.net/gml}DefinitionType

    _ElementMap = PhenomenonType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = PhenomenonType._AttributeMap.copy()
    _AttributeMap.update({
        __dimension.name() : __dimension
    })
Namespace.addCategoryObject('typeBinding', u'CompoundPhenomenonType', CompoundPhenomenonType)


# Complex type CompositePhenomenonType with content type ELEMENT_ONLY
class CompositePhenomenonType (CompoundPhenomenonType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CompositePhenomenonType')
    # Base type is CompoundPhenomenonType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}component uses Python identifier component
    __component = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'component'), 'component', '__httpwww_opengis_netswe1_0_CompositePhenomenonType_httpwww_opengis_netswe1_0component', True)

    
    component = property(__component.value, __component.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}base uses Python identifier base
    __base = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'base'), 'base', '__httpwww_opengis_netswe1_0_CompositePhenomenonType_httpwww_opengis_netswe1_0base', False)

    
    base = property(__base.value, __base.set, None, u'Optional phenomenon that forms the basis for generating more specialized composite Phenomenon by adding more components')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute dimension inherited from {http://www.opengis.net/swe/1.0}CompoundPhenomenonType
    
    # Attribute id_ inherited from {http://www.opengis.net/gml}DefinitionType

    _ElementMap = CompoundPhenomenonType._ElementMap.copy()
    _ElementMap.update({
        __component.name() : __component,
        __base.name() : __base
    })
    _AttributeMap = CompoundPhenomenonType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'CompositePhenomenonType', CompositePhenomenonType)


# Complex type CTD_ANON_14 with content type ELEMENT_ONLY
class CTD_ANON_14 (AbstractEncodingType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractEncodingType
    
    # Element {http://www.opengis.net/swe/1.0}member uses Python identifier member
    __member = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'member'), 'member', '__httpwww_opengis_netswe1_0_CTD_ANON_14_httpwww_opengis_netswe1_0member', True)

    
    member = property(__member.value, __member.set, None, None)

    
    # Attribute byteLength uses Python identifier byteLength
    __byteLength = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'byteLength'), 'byteLength', '__httpwww_opengis_netswe1_0_CTD_ANON_14_byteLength', pyxb.binding.datatypes.positiveInteger)
    
    byteLength = property(__byteLength.value, __byteLength.set, None, None)

    
    # Attribute byteEncoding uses Python identifier byteEncoding
    __byteEncoding = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'byteEncoding'), 'byteEncoding', '__httpwww_opengis_netswe1_0_CTD_ANON_14_byteEncoding', byteEncoding, required=True)
    
    byteEncoding = property(__byteEncoding.value, __byteEncoding.set, None, None)

    
    # Attribute id inherited from {http://www.opengis.net/swe/1.0}AbstractEncodingType
    
    # Attribute byteOrder uses Python identifier byteOrder
    __byteOrder = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'byteOrder'), 'byteOrder', '__httpwww_opengis_netswe1_0_CTD_ANON_14_byteOrder', byteOrder, required=True)
    
    byteOrder = property(__byteOrder.value, __byteOrder.set, None, None)


    _ElementMap = AbstractEncodingType._ElementMap.copy()
    _ElementMap.update({
        __member.name() : __member
    })
    _AttributeMap = AbstractEncodingType._AttributeMap.copy()
    _AttributeMap.update({
        __byteLength.name() : __byteLength,
        __byteEncoding.name() : __byteEncoding,
        __byteOrder.name() : __byteOrder
    })



# Complex type CTD_ANON_15 with content type ELEMENT_ONLY
class CTD_ANON_15 (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractDataComponentType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}uom uses Python identifier uom
    __uom = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uom'), 'uom', '__httpwww_opengis_netswe1_0_CTD_ANON_15_httpwww_opengis_netswe1_0uom', False)

    
    uom = property(__uom.value, __uom.set, None, u'Unit of measure')

    
    # Element {http://www.opengis.net/swe/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netswe1_0_CTD_ANON_15_httpwww_opengis_netswe1_0value', False)

    
    value_ = property(__value.value, __value.set, None, u'Value is optional, to enable structure to act in a schema for values provided using other encodings')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}constraint uses Python identifier constraint
    __constraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'constraint'), 'constraint', '__httpwww_opengis_netswe1_0_CTD_ANON_15_httpwww_opengis_netswe1_0constraint', False)

    
    constraint = property(__constraint.value, __constraint.set, None, u'The constraint property defines the permitted values, as a range or enumerated list')

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}quality uses Python identifier quality
    __quality = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'quality'), 'quality', '__httpwww_opengis_netswe1_0_CTD_ANON_15_httpwww_opengis_netswe1_0quality', True)

    
    quality = property(__quality.value, __quality.set, None, u'The quality property provides an indication of the reliability of estimates of the asociated value')

    
    # Attribute axisID uses Python identifier axisID
    __axisID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'axisID'), 'axisID', '__httpwww_opengis_netswe1_0_CTD_ANON_15_axisID', pyxb.binding.datatypes.token)
    
    axisID = property(__axisID.value, __axisID.set, None, u'Specifies the reference axis using the gml:axisID. The reference frame URI is inherited from parent Vector')

    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute referenceFrame uses Python identifier referenceFrame
    __referenceFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceFrame'), 'referenceFrame', '__httpwww_opengis_netswe1_0_CTD_ANON_15_referenceFrame', pyxb.binding.datatypes.anyURI)
    
    referenceFrame = property(__referenceFrame.value, __referenceFrame.set, None, u'A reference frame anchors a value to a datum or interval scale')

    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType

    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        __uom.name() : __uom,
        __value.name() : __value,
        __constraint.name() : __constraint,
        __quality.name() : __quality
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        __axisID.name() : __axisID,
        __referenceFrame.name() : __referenceFrame
    })



# Complex type VectorPropertyType with content type ELEMENT_ONLY
class VectorPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'VectorPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Vector uses Python identifier Vector
    __Vector = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Vector'), 'Vector', '__httpwww_opengis_netswe1_0_VectorPropertyType_httpwww_opengis_netswe1_0Vector', False)

    
    Vector = property(__Vector.value, __Vector.set, None, u'A Vector is a special type of DataRecord that takes a list of numerical scalars called coordinates. The Vector has a referenceFrame in which the coordinates are expressed')

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_VectorPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_VectorPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_VectorPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_VectorPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_VectorPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_VectorPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_VectorPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_VectorPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")


    _ElementMap = {
        __Vector.name() : __Vector
    }
    _AttributeMap = {
        __show.name() : __show,
        __href.name() : __href,
        __role.name() : __role,
        __type.name() : __type,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __remoteSchema.name() : __remoteSchema,
        __actuate.name() : __actuate
    }
Namespace.addCategoryObject('typeBinding', u'VectorPropertyType', VectorPropertyType)


# Complex type DataRecordPropertyType with content type ELEMENT_ONLY
class DataRecordPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataRecordPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}DataRecord uses Python identifier DataRecord
    __DataRecord = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'DataRecord'), 'DataRecord', '__httpwww_opengis_netswe1_0_DataRecordPropertyType_httpwww_opengis_netswe1_0DataRecord', False)

    
    DataRecord = property(__DataRecord.value, __DataRecord.set, None, u'Implementation of ISO-11404 Record datatype. This allows grouping of data components which can themselves be Records, Arrays or Simple Types')


    _ElementMap = {
        __DataRecord.name() : __DataRecord
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'DataRecordPropertyType', DataRecordPropertyType)


# Complex type RecordPropertyType with content type ELEMENT_ONLY
class RecordPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RecordPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Record uses Python identifier Record
    __Record = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Record'), 'Record', '__httpwww_opengis_netswe1_0_RecordPropertyType_httpwww_opengis_netswe1_0Record', False)

    
    Record = property(__Record.value, __Record.set, None, u'A record is a list of fields')


    _ElementMap = {
        __Record.name() : __Record
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'RecordPropertyType', RecordPropertyType)


# Complex type TypedValueListPropertyType with content type ELEMENT_ONLY
class TypedValueListPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TypedValueListPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}TypedValueList uses Python identifier TypedValueList
    __TypedValueList = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TypedValueList'), 'TypedValueList', '__httpwww_opengis_netswe1_0_TypedValueListPropertyType_httpwww_opengis_netswe1_0TypedValueList', False)

    
    TypedValueList = property(__TypedValueList.value, __TypedValueList.set, None, u'A generic soft-typed list of values')


    _ElementMap = {
        __TypedValueList.name() : __TypedValueList
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TypedValueListPropertyType', TypedValueListPropertyType)


# Complex type PhenomenonSeriesType with content type ELEMENT_ONLY
class PhenomenonSeriesType (CompoundPhenomenonType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PhenomenonSeriesType')
    # Base type is CompoundPhenomenonType
    
    # Element {http://www.opengis.net/swe/1.0}otherConstraint uses Python identifier otherConstraint
    __otherConstraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'otherConstraint'), 'otherConstraint', '__httpwww_opengis_netswe1_0_PhenomenonSeriesType_httpwww_opengis_netswe1_0otherConstraint', True)

    
    otherConstraint = property(__otherConstraint.value, __otherConstraint.set, None, u'Other constraints are described in text')

    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}base uses Python identifier base
    __base = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'base'), 'base', '__httpwww_opengis_netswe1_0_PhenomenonSeriesType_httpwww_opengis_netswe1_0base', False)

    
    base = property(__base.value, __base.set, None, u'Phenomenon that forms the basis for generating a set of more refined Phenomena; e.g. Chemical Composition, Radiance')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}constraintList uses Python identifier constraintList
    __constraintList = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'constraintList'), 'constraintList', '__httpwww_opengis_netswe1_0_PhenomenonSeriesType_httpwww_opengis_netswe1_0constraintList', True)

    
    constraintList = property(__constraintList.value, __constraintList.set, None, u'A set of values of some secondary property that constraints the basePhenomenon to generate a Phenomenon set.  \n\t\t\t\t\t\t\tIf more than one set of constraints are possible, then these are applied simultaneously to generate')

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute dimension inherited from {http://www.opengis.net/swe/1.0}CompoundPhenomenonType
    
    # Attribute id_ inherited from {http://www.opengis.net/gml}DefinitionType

    _ElementMap = CompoundPhenomenonType._ElementMap.copy()
    _ElementMap.update({
        __otherConstraint.name() : __otherConstraint,
        __base.name() : __base,
        __constraintList.name() : __constraintList
    })
    _AttributeMap = CompoundPhenomenonType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'PhenomenonSeriesType', PhenomenonSeriesType)


# Complex type CategoryPropertyType with content type ELEMENT_ONLY
class CategoryPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CategoryPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Category uses Python identifier Category
    __Category = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Category'), 'Category', '__httpwww_opengis_netswe1_0_CategoryPropertyType_httpwww_opengis_netswe1_0Category', False)

    
    Category = property(__Category.value, __Category.set, None, u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value')


    _ElementMap = {
        __Category.name() : __Category
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'CategoryPropertyType', CategoryPropertyType)


# Complex type CTD_ANON_16 with content type ELEMENT_ONLY
class CTD_ANON_16 (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractDataComponentType
    
    # Element {http://www.opengis.net/swe/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netswe1_0_CTD_ANON_16_httpwww_opengis_netswe1_0value', False)

    
    value_ = property(__value.value, __value.set, None, u'Value is optional, to enable structure to act in a schema for values provided using other encodings')

    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}quality uses Python identifier quality
    __quality = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'quality'), 'quality', '__httpwww_opengis_netswe1_0_CTD_ANON_16_httpwww_opengis_netswe1_0quality', True)

    
    quality = property(__quality.value, __quality.set, None, u'The quality property provides an indication of the reliability of estimates of the asociated value')

    
    # Element {http://www.opengis.net/swe/1.0}constraint uses Python identifier constraint
    __constraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'constraint'), 'constraint', '__httpwww_opengis_netswe1_0_CTD_ANON_16_httpwww_opengis_netswe1_0constraint', False)

    
    constraint = property(__constraint.value, __constraint.set, None, u'The constraint property defines the permitted values, as a range or enumerated list')

    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute referenceFrame uses Python identifier referenceFrame
    __referenceFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceFrame'), 'referenceFrame', '__httpwww_opengis_netswe1_0_CTD_ANON_16_referenceFrame', pyxb.binding.datatypes.anyURI)
    
    referenceFrame = property(__referenceFrame.value, __referenceFrame.set, None, u'A reference frame anchors a value to a datum or interval scale')

    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute axisID uses Python identifier axisID
    __axisID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'axisID'), 'axisID', '__httpwww_opengis_netswe1_0_CTD_ANON_16_axisID', pyxb.binding.datatypes.token)
    
    axisID = property(__axisID.value, __axisID.set, None, u'Specifies the reference axis using the gml:axisID. The reference frame URI is inherited from parent Vector')


    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        __value.name() : __value,
        __quality.name() : __quality,
        __constraint.name() : __constraint
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        __referenceFrame.name() : __referenceFrame,
        __axisID.name() : __axisID
    })



# Complex type QuantityRangePropertyType with content type ELEMENT_ONLY
class QuantityRangePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'QuantityRangePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}QuantityRange uses Python identifier QuantityRange
    __QuantityRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), 'QuantityRange', '__httpwww_opengis_netswe1_0_QuantityRangePropertyType_httpwww_opengis_netswe1_0QuantityRange', False)

    
    QuantityRange = property(__QuantityRange.value, __QuantityRange.set, None, u'Decimal pair for specifying a quantity range with constraints')


    _ElementMap = {
        __QuantityRange.name() : __QuantityRange
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'QuantityRangePropertyType', QuantityRangePropertyType)


# Complex type CTD_ANON_17 with content type ELEMENT_ONLY
class CTD_ANON_17 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}interval uses Python identifier interval
    __interval = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'interval'), 'interval', '__httpwww_opengis_netswe1_0_CTD_ANON_17_httpwww_opengis_netswe1_0interval', True)

    
    interval = property(__interval.value, __interval.set, None, u'Range of allowed time values (closed interval) for this component')

    
    # Element {http://www.opengis.net/swe/1.0}max uses Python identifier max
    __max = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'max'), 'max', '__httpwww_opengis_netswe1_0_CTD_ANON_17_httpwww_opengis_netswe1_0max', False)

    
    max = property(__max.value, __max.set, None, u'Specifies maximum allowed time value for an open interval (no min)')

    
    # Element {http://www.opengis.net/swe/1.0}min uses Python identifier min
    __min = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'min'), 'min', '__httpwww_opengis_netswe1_0_CTD_ANON_17_httpwww_opengis_netswe1_0min', False)

    
    min = property(__min.value, __min.set, None, u'Specifies minimum allowed time value for an open interval (no max)')

    
    # Element {http://www.opengis.net/swe/1.0}valueList uses Python identifier valueList
    __valueList = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'valueList'), 'valueList', '__httpwww_opengis_netswe1_0_CTD_ANON_17_httpwww_opengis_netswe1_0valueList', True)

    
    valueList = property(__valueList.value, __valueList.set, None, u'List of allowed time values for this component')

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'id'), 'id', '__httpwww_opengis_netswe1_0_CTD_ANON_17_id', pyxb.binding.datatypes.ID)
    
    id = property(__id.value, __id.set, None, None)


    _ElementMap = {
        __interval.name() : __interval,
        __max.name() : __max,
        __min.name() : __min,
        __valueList.name() : __valueList
    }
    _AttributeMap = {
        __id.name() : __id
    }



# Complex type CTD_ANON_18 with content type EMPTY
class CTD_ANON_18 (AbstractEncodingType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractEncodingType
    
    # Attribute id inherited from {http://www.opengis.net/swe/1.0}AbstractEncodingType
    
    # Attribute decimalSeparator uses Python identifier decimalSeparator
    __decimalSeparator = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'decimalSeparator'), 'decimalSeparator', '__httpwww_opengis_netswe1_0_CTD_ANON_18_decimalSeparator', decimalSeparator, required=True)
    
    decimalSeparator = property(__decimalSeparator.value, __decimalSeparator.set, None, None)

    
    # Attribute tokenSeparator uses Python identifier tokenSeparator
    __tokenSeparator = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'tokenSeparator'), 'tokenSeparator', '__httpwww_opengis_netswe1_0_CTD_ANON_18_tokenSeparator', textSeparator, required=True)
    
    tokenSeparator = property(__tokenSeparator.value, __tokenSeparator.set, None, None)

    
    # Attribute blockSeparator uses Python identifier blockSeparator
    __blockSeparator = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'blockSeparator'), 'blockSeparator', '__httpwww_opengis_netswe1_0_CTD_ANON_18_blockSeparator', textSeparator, required=True)
    
    blockSeparator = property(__blockSeparator.value, __blockSeparator.set, None, None)


    _ElementMap = AbstractEncodingType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = AbstractEncodingType._AttributeMap.copy()
    _AttributeMap.update({
        __decimalSeparator.name() : __decimalSeparator,
        __tokenSeparator.name() : __tokenSeparator,
        __blockSeparator.name() : __blockSeparator
    })



# Complex type AllowedValuesPropertyType with content type ELEMENT_ONLY
class AllowedValuesPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AllowedValuesPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}AllowedValues uses Python identifier AllowedValues
    __AllowedValues = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AllowedValues'), 'AllowedValues', '__httpwww_opengis_netswe1_0_AllowedValuesPropertyType_httpwww_opengis_netswe1_0AllowedValues', False)

    
    AllowedValues = property(__AllowedValues.value, __AllowedValues.set, None, u'List of allowed values (There is an implicit AND between all members)')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_AllowedValuesPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_AllowedValuesPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_AllowedValuesPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_AllowedValuesPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_AllowedValuesPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_AllowedValuesPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_AllowedValuesPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_AllowedValuesPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)


    _ElementMap = {
        __AllowedValues.name() : __AllowedValues
    }
    _AttributeMap = {
        __href.name() : __href,
        __role.name() : __role,
        __type.name() : __type,
        __title.name() : __title,
        __remoteSchema.name() : __remoteSchema,
        __actuate.name() : __actuate,
        __show.name() : __show,
        __arcrole.name() : __arcrole
    }
Namespace.addCategoryObject('typeBinding', u'AllowedValuesPropertyType', AllowedValuesPropertyType)


# Complex type MultiplexedStreamFormatType with content type EMPTY
class MultiplexedStreamFormatType (AbstractEncodingType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MultiplexedStreamFormatType')
    # Base type is AbstractEncodingType
    
    # Attribute id inherited from {http://www.opengis.net/swe/1.0}AbstractEncodingType
    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpwww_opengis_netswe1_0_MultiplexedStreamFormatType_version', pyxb.binding.datatypes.string, required=True)
    
    version = property(__version.value, __version.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'type'), 'type', '__httpwww_opengis_netswe1_0_MultiplexedStreamFormatType_type', pyxb.binding.datatypes.anyURI, required=True)
    
    type = property(__type.value, __type.set, None, None)


    _ElementMap = AbstractEncodingType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = AbstractEncodingType._AttributeMap.copy()
    _AttributeMap.update({
        __version.name() : __version,
        __type.name() : __type
    })
Namespace.addCategoryObject('typeBinding', u'MultiplexedStreamFormatType', MultiplexedStreamFormatType)


# Complex type TimeGeometricPrimitivePropertyType with content type ELEMENT_ONLY
class TimeGeometricPrimitivePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeGeometricPrimitivePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/gml}_TimeGeometricPrimitive uses Python identifier TimeGeometricPrimitive
    __TimeGeometricPrimitive = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_TimeGeometricPrimitive'), 'TimeGeometricPrimitive', '__httpwww_opengis_netswe1_0_TimeGeometricPrimitivePropertyType_httpwww_opengis_netgml_TimeGeometricPrimitive', False)

    
    TimeGeometricPrimitive = property(__TimeGeometricPrimitive.value, __TimeGeometricPrimitive.set, None, u'This abstract element acts as the head of the substitution group for temporal geometric primitives.')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_TimeGeometricPrimitivePropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_TimeGeometricPrimitivePropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_TimeGeometricPrimitivePropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_TimeGeometricPrimitivePropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_TimeGeometricPrimitivePropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_TimeGeometricPrimitivePropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_TimeGeometricPrimitivePropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_TimeGeometricPrimitivePropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')


    _ElementMap = {
        __TimeGeometricPrimitive.name() : __TimeGeometricPrimitive
    }
    _AttributeMap = {
        __href.name() : __href,
        __role.name() : __role,
        __title.name() : __title,
        __type.name() : __type,
        __arcrole.name() : __arcrole,
        __show.name() : __show,
        __actuate.name() : __actuate,
        __remoteSchema.name() : __remoteSchema
    }
Namespace.addCategoryObject('typeBinding', u'TimeGeometricPrimitivePropertyType', TimeGeometricPrimitivePropertyType)


# Complex type AbstractMatrixType with content type ELEMENT_ONLY
class AbstractMatrixType (AbstractDataArrayType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AbstractMatrixType')
    # Base type is AbstractDataArrayType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element elementCount ({http://www.opengis.net/swe/1.0}elementCount) inherited from {http://www.opengis.net/swe/1.0}AbstractDataArrayType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute localFrame uses Python identifier localFrame
    __localFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'localFrame'), 'localFrame', '__httpwww_opengis_netswe1_0_AbstractMatrixType_localFrame', pyxb.binding.datatypes.anyURI)
    
    localFrame = property(__localFrame.value, __localFrame.set, None, u'Specifies the spatial frame which location and/or orientation is given by the enclosing vector')

    
    # Attribute referenceFrame uses Python identifier referenceFrame
    __referenceFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceFrame'), 'referenceFrame', '__httpwww_opengis_netswe1_0_AbstractMatrixType_referenceFrame', pyxb.binding.datatypes.anyURI)
    
    referenceFrame = property(__referenceFrame.value, __referenceFrame.set, None, u'Points to a spatial reference frame definition. Coordinates of the vector will be expressed in this reference frame')

    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType

    _ElementMap = AbstractDataArrayType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = AbstractDataArrayType._AttributeMap.copy()
    _AttributeMap.update({
        __localFrame.name() : __localFrame,
        __referenceFrame.name() : __referenceFrame
    })
Namespace.addCategoryObject('typeBinding', u'AbstractMatrixType', AbstractMatrixType)


# Complex type SquareMatrixType with content type ELEMENT_ONLY
class SquareMatrixType (AbstractMatrixType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SquareMatrixType')
    # Base type is AbstractMatrixType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element elementCount ({http://www.opengis.net/swe/1.0}elementCount) inherited from {http://www.opengis.net/swe/1.0}AbstractDataArrayType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}elementType uses Python identifier elementType
    __elementType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'elementType'), 'elementType', '__httpwww_opengis_netswe1_0_SquareMatrixType_httpwww_opengis_netswe1_0elementType', False)

    
    elementType = property(__elementType.value, __elementType.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}values uses Python identifier values
    __values = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'values'), 'values', '__httpwww_opengis_netswe1_0_SquareMatrixType_httpwww_opengis_netswe1_0values', False)

    
    values = property(__values.value, __values.set, None, u'Carries the block of values encoded as specified by the encoding element')

    
    # Element {http://www.opengis.net/swe/1.0}encoding uses Python identifier encoding
    __encoding = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'encoding'), 'encoding', '__httpwww_opengis_netswe1_0_SquareMatrixType_httpwww_opengis_netswe1_0encoding', False)

    
    encoding = property(__encoding.value, __encoding.set, None, u'Specifies an encoding for the data structure defined by the enclosing element')

    
    # Attribute localFrame inherited from {http://www.opengis.net/swe/1.0}AbstractMatrixType
    
    # Attribute referenceFrame inherited from {http://www.opengis.net/swe/1.0}AbstractMatrixType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType

    _ElementMap = AbstractMatrixType._ElementMap.copy()
    _ElementMap.update({
        __elementType.name() : __elementType,
        __values.name() : __values,
        __encoding.name() : __encoding
    })
    _AttributeMap = AbstractMatrixType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'SquareMatrixType', SquareMatrixType)


# Complex type CTD_ANON_19 with content type ELEMENT_ONLY
class CTD_ANON_19 (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractDataComponentType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}quality uses Python identifier quality
    __quality = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'quality'), 'quality', '__httpwww_opengis_netswe1_0_CTD_ANON_19_httpwww_opengis_netswe1_0quality', False)

    
    quality = property(__quality.value, __quality.set, None, u'The quality property provides an indication of the reliability of estimates of the asociated value')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}uom uses Python identifier uom
    __uom = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uom'), 'uom', '__httpwww_opengis_netswe1_0_CTD_ANON_19_httpwww_opengis_netswe1_0uom', False)

    
    uom = property(__uom.value, __uom.set, None, u'Unit of measure')

    
    # Element {http://www.opengis.net/swe/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netswe1_0_CTD_ANON_19_httpwww_opengis_netswe1_0value', False)

    
    value_ = property(__value.value, __value.set, None, u'Value is optional, to enable structure to act in a schema for values provided using other encodings')

    
    # Element {http://www.opengis.net/swe/1.0}constraint uses Python identifier constraint
    __constraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'constraint'), 'constraint', '__httpwww_opengis_netswe1_0_CTD_ANON_19_httpwww_opengis_netswe1_0constraint', False)

    
    constraint = property(__constraint.value, __constraint.set, None, u'The constraint property defines the permitted values, as a range or enumerated list')

    
    # Attribute referenceTime uses Python identifier referenceTime
    __referenceTime = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceTime'), 'referenceTime', '__httpwww_opengis_netswe1_0_CTD_ANON_19_referenceTime', timeIso8601)
    
    referenceTime = property(__referenceTime.value, __referenceTime.set, None, u'Specifies the origin of the temporal reference frame as an ISO8601 date (used to specify time after an epoch)')

    
    # Attribute referenceFrame uses Python identifier referenceFrame
    __referenceFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'referenceFrame'), 'referenceFrame', '__httpwww_opengis_netswe1_0_CTD_ANON_19_referenceFrame', pyxb.binding.datatypes.anyURI)
    
    referenceFrame = property(__referenceFrame.value, __referenceFrame.set, None, u'Points to a temporal reference frame definition. Time value will be expressed relative to this frame')

    
    # Attribute localFrame uses Python identifier localFrame
    __localFrame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'localFrame'), 'localFrame', '__httpwww_opengis_netswe1_0_CTD_ANON_19_localFrame', pyxb.binding.datatypes.anyURI)
    
    localFrame = property(__localFrame.value, __localFrame.set, None, u'Specifies the temporal frame which origin is given by this time component')

    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType

    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        __quality.name() : __quality,
        __uom.name() : __uom,
        __value.name() : __value,
        __constraint.name() : __constraint
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        __referenceTime.name() : __referenceTime,
        __referenceFrame.name() : __referenceFrame,
        __localFrame.name() : __localFrame
    })



# Complex type XMLBlockType with content type EMPTY
class XMLBlockType (AbstractEncodingType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'XMLBlockType')
    # Base type is AbstractEncodingType
    
    # Attribute xmlElement uses Python identifier xmlElement
    __xmlElement = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'xmlElement'), 'xmlElement', '__httpwww_opengis_netswe1_0_XMLBlockType_xmlElement', pyxb.binding.datatypes.QName)
    
    xmlElement = property(__xmlElement.value, __xmlElement.set, None, u'May be any XML Schema defined global element. \n\t\ttypically this will be swe:Array, swe:Record, cv:CV_DiscreteCoverage, etc')

    
    # Attribute id inherited from {http://www.opengis.net/swe/1.0}AbstractEncodingType

    _ElementMap = AbstractEncodingType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = AbstractEncodingType._AttributeMap.copy()
    _AttributeMap.update({
        __xmlElement.name() : __xmlElement
    })
Namespace.addCategoryObject('typeBinding', u'XMLBlockType', XMLBlockType)


# Complex type DataStreamDefinitionType with content type ELEMENT_ONLY
class DataStreamDefinitionType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataStreamDefinitionType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}streamEncoding uses Python identifier streamEncoding
    __streamEncoding = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'streamEncoding'), 'streamEncoding', '__httpwww_opengis_netswe1_0_DataStreamDefinitionType_httpwww_opengis_netswe1_0streamEncoding', False)

    
    streamEncoding = property(__streamEncoding.value, __streamEncoding.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}streamComponent uses Python identifier streamComponent
    __streamComponent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'streamComponent'), 'streamComponent', '__httpwww_opengis_netswe1_0_DataStreamDefinitionType_httpwww_opengis_netswe1_0streamComponent', True)

    
    streamComponent = property(__streamComponent.value, __streamComponent.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'id'), 'id', '__httpwww_opengis_netswe1_0_DataStreamDefinitionType_id', pyxb.binding.datatypes.ID)
    
    id = property(__id.value, __id.set, None, None)


    _ElementMap = {
        __streamEncoding.name() : __streamEncoding,
        __streamComponent.name() : __streamComponent
    }
    _AttributeMap = {
        __id.name() : __id
    }
Namespace.addCategoryObject('typeBinding', u'DataStreamDefinitionType', DataStreamDefinitionType)


# Complex type DataBlockDefinitionPropertyType with content type ELEMENT_ONLY
class DataBlockDefinitionPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataBlockDefinitionPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}DataBlockDefinition uses Python identifier DataBlockDefinition
    __DataBlockDefinition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'DataBlockDefinition'), 'DataBlockDefinition', '__httpwww_opengis_netswe1_0_DataBlockDefinitionPropertyType_httpwww_opengis_netswe1_0DataBlockDefinition', False)

    
    DataBlockDefinition = property(__DataBlockDefinition.value, __DataBlockDefinition.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_DataBlockDefinitionPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_DataBlockDefinitionPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_DataBlockDefinitionPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_DataBlockDefinitionPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_DataBlockDefinitionPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_DataBlockDefinitionPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_DataBlockDefinitionPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_DataBlockDefinitionPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")


    _ElementMap = {
        __DataBlockDefinition.name() : __DataBlockDefinition
    }
    _AttributeMap = {
        __show.name() : __show,
        __href.name() : __href,
        __role.name() : __role,
        __type.name() : __type,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __remoteSchema.name() : __remoteSchema,
        __actuate.name() : __actuate
    }
Namespace.addCategoryObject('typeBinding', u'DataBlockDefinitionPropertyType', DataBlockDefinitionPropertyType)


# Complex type ItemPropertyType with content type ELEMENT_ONLY
class ItemPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ItemPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Item uses Python identifier Item
    __Item = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Item'), 'Item', '__httpwww_opengis_netswe1_0_ItemPropertyType_httpwww_opengis_netswe1_0Item', False)

    
    Item = property(__Item.value, __Item.set, None, u'An Item is an item of data of any type')


    _ElementMap = {
        __Item.name() : __Item
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ItemPropertyType', ItemPropertyType)


# Complex type TimePositionListType with content type SIMPLE
class TimePositionListType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = TimeValueList
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimePositionListType')
    # Base type is TimeValueList
    
    # Attribute frame uses Python identifier frame
    __frame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'frame'), 'frame', '__httpwww_opengis_netswe1_0_TimePositionListType_frame', pyxb.binding.datatypes.anyURI, unicode_default=u'#ISO-8601')
    
    frame = property(__frame.value, __frame.set, None, None)

    
    # Attribute calendarEraName uses Python identifier calendarEraName
    __calendarEraName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'calendarEraName'), 'calendarEraName', '__httpwww_opengis_netswe1_0_TimePositionListType_calendarEraName', pyxb.binding.datatypes.string)
    
    calendarEraName = property(__calendarEraName.value, __calendarEraName.set, None, None)

    
    # Attribute count uses Python identifier count
    __count = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'count'), 'count', '__httpwww_opengis_netswe1_0_TimePositionListType_count', pyxb.binding.datatypes.positiveInteger)
    
    count = property(__count.value, __count.set, None, u'"count" allows to specify the number of direct positions in the list. ')

    
    # Attribute indeterminatePosition uses Python identifier indeterminatePosition
    __indeterminatePosition = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'indeterminatePosition'), 'indeterminatePosition', '__httpwww_opengis_netswe1_0_TimePositionListType_indeterminatePosition', pyxb.bundles.opengis.gml.TimeIndeterminateValueType)
    
    indeterminatePosition = property(__indeterminatePosition.value, __indeterminatePosition.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __frame.name() : __frame,
        __calendarEraName.name() : __calendarEraName,
        __count.name() : __count,
        __indeterminatePosition.name() : __indeterminatePosition
    }
Namespace.addCategoryObject('typeBinding', u'TimePositionListType', TimePositionListType)


# Complex type PositionType with content type ELEMENT_ONLY
class PositionType (AbstractVectorType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PositionType')
    # Base type is AbstractVectorType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}location uses Python identifier location
    __location = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'location'), 'location', '__httpwww_opengis_netswe1_0_PositionType_httpwww_opengis_netswe1_0location', False)

    
    location = property(__location.value, __location.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}acceleration uses Python identifier acceleration
    __acceleration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'acceleration'), 'acceleration', '__httpwww_opengis_netswe1_0_PositionType_httpwww_opengis_netswe1_0acceleration', False)

    
    acceleration = property(__acceleration.value, __acceleration.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}orientation uses Python identifier orientation
    __orientation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'orientation'), 'orientation', '__httpwww_opengis_netswe1_0_PositionType_httpwww_opengis_netswe1_0orientation', False)

    
    orientation = property(__orientation.value, __orientation.set, None, None)

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}angularAcceleration uses Python identifier angularAcceleration
    __angularAcceleration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'angularAcceleration'), 'angularAcceleration', '__httpwww_opengis_netswe1_0_PositionType_httpwww_opengis_netswe1_0angularAcceleration', False)

    
    angularAcceleration = property(__angularAcceleration.value, __angularAcceleration.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}velocity uses Python identifier velocity
    __velocity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'velocity'), 'velocity', '__httpwww_opengis_netswe1_0_PositionType_httpwww_opengis_netswe1_0velocity', False)

    
    velocity = property(__velocity.value, __velocity.set, None, None)

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}state uses Python identifier state
    __state = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'state'), 'state', '__httpwww_opengis_netswe1_0_PositionType_httpwww_opengis_netswe1_0state', False)

    
    state = property(__state.value, __state.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}time uses Python identifier time
    __time = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'time'), 'time', '__httpwww_opengis_netswe1_0_PositionType_httpwww_opengis_netswe1_0time', False)

    
    time = property(__time.value, __time.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}angularVelocity uses Python identifier angularVelocity
    __angularVelocity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'angularVelocity'), 'angularVelocity', '__httpwww_opengis_netswe1_0_PositionType_httpwww_opengis_netswe1_0angularVelocity', False)

    
    angularVelocity = property(__angularVelocity.value, __angularVelocity.set, None, None)

    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute referenceFrame inherited from {http://www.opengis.net/swe/1.0}AbstractVectorType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute localFrame inherited from {http://www.opengis.net/swe/1.0}AbstractVectorType

    _ElementMap = AbstractVectorType._ElementMap.copy()
    _ElementMap.update({
        __location.name() : __location,
        __acceleration.name() : __acceleration,
        __orientation.name() : __orientation,
        __angularAcceleration.name() : __angularAcceleration,
        __velocity.name() : __velocity,
        __state.name() : __state,
        __time.name() : __time,
        __angularVelocity.name() : __angularVelocity
    })
    _AttributeMap = AbstractVectorType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'PositionType', PositionType)


# Complex type ConstrainedPhenomenonType with content type ELEMENT_ONLY
class ConstrainedPhenomenonType (PhenomenonType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ConstrainedPhenomenonType')
    # Base type is PhenomenonType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}base uses Python identifier base
    __base = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'base'), 'base', '__httpwww_opengis_netswe1_0_ConstrainedPhenomenonType_httpwww_opengis_netswe1_0base', False)

    
    base = property(__base.value, __base.set, None, u'Property that forms the basis for generating a set of more refined Phenomena; e.g. Chemical Composition, Radiance')

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}otherConstraint uses Python identifier otherConstraint
    __otherConstraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'otherConstraint'), 'otherConstraint', '__httpwww_opengis_netswe1_0_ConstrainedPhenomenonType_httpwww_opengis_netswe1_0otherConstraint', True)

    
    otherConstraint = property(__otherConstraint.value, __otherConstraint.set, None, u'Constraints that cannot be expressed as values of an orthogonal/helper phenomenon')

    
    # Element {http://www.opengis.net/swe/1.0}singleConstraint uses Python identifier singleConstraint
    __singleConstraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'singleConstraint'), 'singleConstraint', '__httpwww_opengis_netswe1_0_ConstrainedPhenomenonType_httpwww_opengis_netswe1_0singleConstraint', True)

    
    singleConstraint = property(__singleConstraint.value, __singleConstraint.set, None, u'Constraint expressed as a value or range of an orthogonal/helper phenomenon')

    
    # Attribute id_ inherited from {http://www.opengis.net/gml}DefinitionType

    _ElementMap = PhenomenonType._ElementMap.copy()
    _ElementMap.update({
        __base.name() : __base,
        __otherConstraint.name() : __otherConstraint,
        __singleConstraint.name() : __singleConstraint
    })
    _AttributeMap = PhenomenonType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ConstrainedPhenomenonType', ConstrainedPhenomenonType)


# Complex type CTD_ANON_20 with content type ELEMENT_ONLY
class CTD_ANON_20 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Count uses Python identifier Count
    __Count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Count'), 'Count', '__httpwww_opengis_netswe1_0_CTD_ANON_20_httpwww_opengis_netswe1_0Count', False)

    
    Count = property(__Count.value, __Count.set, None, u'Integer number used for a counting value')

    
    # Element {http://www.opengis.net/swe/1.0}Time uses Python identifier Time
    __Time = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Time'), 'Time', '__httpwww_opengis_netswe1_0_CTD_ANON_20_httpwww_opengis_netswe1_0Time', False)

    
    Time = property(__Time.value, __Time.set, None, u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin')

    
    # Element {http://www.opengis.net/swe/1.0}Quantity uses Python identifier Quantity
    __Quantity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), 'Quantity', '__httpwww_opengis_netswe1_0_CTD_ANON_20_httpwww_opengis_netswe1_0Quantity', False)

    
    Quantity = property(__Quantity.value, __Quantity.set, None, u'Decimal number with optional unit and constraints')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_netswe1_0_CTD_ANON_20_name', pyxb.binding.datatypes.token, required=True)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __Count.name() : __Count,
        __Time.name() : __Time,
        __Quantity.name() : __Quantity
    }
    _AttributeMap = {
        __name.name() : __name
    }



# Complex type RecordType with content type ELEMENT_ONLY
class RecordType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RecordType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}field uses Python identifier field
    __field = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'field'), 'field', '__httpwww_opengis_netswe1_0_RecordType_httpwww_opengis_netswe1_0field', True)

    
    field = property(__field.value, __field.set, None, u'A Record/field contains an item of data')

    
    # Attribute RS uses Python identifier RS
    __RS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'RS'), 'RS', '__httpwww_opengis_netswe1_0_RecordType_RS', pyxb.binding.datatypes.anyURI)
    
    RS = property(__RS.value, __RS.set, None, u'Optional pointer to record-type schema')

    
    # Attribute fieldCount uses Python identifier fieldCount
    __fieldCount = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'fieldCount'), 'fieldCount', '__httpwww_opengis_netswe1_0_RecordType_fieldCount', pyxb.binding.datatypes.positiveInteger)
    
    fieldCount = property(__fieldCount.value, __fieldCount.set, None, u'Optional count of the number of fields in the record. ')


    _ElementMap = {
        __field.name() : __field
    }
    _AttributeMap = {
        __RS.name() : __RS,
        __fieldCount.name() : __fieldCount
    }
Namespace.addCategoryObject('typeBinding', u'RecordType', RecordType)


# Complex type CTD_ANON_21 with content type EMPTY
class CTD_ANON_21 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute paddingBytes-before uses Python identifier paddingBytes_before
    __paddingBytes_before = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'paddingBytes-before'), 'paddingBytes_before', '__httpwww_opengis_netswe1_0_CTD_ANON_21_paddingBytes_before', pyxb.binding.datatypes.nonNegativeInteger, unicode_default=u'0')
    
    paddingBytes_before = property(__paddingBytes_before.value, __paddingBytes_before.set, None, None)

    
    # Attribute encryption uses Python identifier encryption
    __encryption = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'encryption'), 'encryption', '__httpwww_opengis_netswe1_0_CTD_ANON_21_encryption', pyxb.binding.datatypes.anyURI)
    
    encryption = property(__encryption.value, __encryption.set, None, None)

    
    # Attribute paddingBytes-after uses Python identifier paddingBytes_after
    __paddingBytes_after = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'paddingBytes-after'), 'paddingBytes_after', '__httpwww_opengis_netswe1_0_CTD_ANON_21_paddingBytes_after', pyxb.binding.datatypes.nonNegativeInteger, unicode_default=u'0')
    
    paddingBytes_after = property(__paddingBytes_after.value, __paddingBytes_after.set, None, None)

    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ref'), 'ref', '__httpwww_opengis_netswe1_0_CTD_ANON_21_ref', pyxb.binding.datatypes.token, required=True)
    
    ref = property(__ref.value, __ref.set, None, None)

    
    # Attribute compression uses Python identifier compression
    __compression = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'compression'), 'compression', '__httpwww_opengis_netswe1_0_CTD_ANON_21_compression', pyxb.binding.datatypes.anyURI)
    
    compression = property(__compression.value, __compression.set, None, None)

    
    # Attribute byteLength uses Python identifier byteLength
    __byteLength = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'byteLength'), 'byteLength', '__httpwww_opengis_netswe1_0_CTD_ANON_21_byteLength', pyxb.binding.datatypes.positiveInteger)
    
    byteLength = property(__byteLength.value, __byteLength.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __paddingBytes_before.name() : __paddingBytes_before,
        __encryption.name() : __encryption,
        __paddingBytes_after.name() : __paddingBytes_after,
        __ref.name() : __ref,
        __compression.name() : __compression,
        __byteLength.name() : __byteLength
    }



# Complex type EnvelopePropertyType with content type ELEMENT_ONLY
class EnvelopePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'EnvelopePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Envelope uses Python identifier Envelope
    __Envelope = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Envelope'), 'Envelope', '__httpwww_opengis_netswe1_0_EnvelopePropertyType_httpwww_opengis_netswe1_0Envelope', False)

    
    Envelope = property(__Envelope.value, __Envelope.set, None, u'Envelope described using two vectors specifying lower and upper corner points.\n           This is typically use to define rectangular bounding boxes in any coordinate system.')

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_EnvelopePropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_EnvelopePropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_EnvelopePropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_EnvelopePropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_EnvelopePropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_EnvelopePropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_EnvelopePropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_EnvelopePropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")


    _ElementMap = {
        __Envelope.name() : __Envelope
    }
    _AttributeMap = {
        __remoteSchema.name() : __remoteSchema,
        __href.name() : __href,
        __type.name() : __type,
        __role.name() : __role,
        __actuate.name() : __actuate,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __show.name() : __show
    }
Namespace.addCategoryObject('typeBinding', u'EnvelopePropertyType', EnvelopePropertyType)


# Complex type DataBlockDefinitionType with content type ELEMENT_ONLY
class DataBlockDefinitionType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataBlockDefinitionType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}encoding uses Python identifier encoding
    __encoding = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'encoding'), 'encoding', '__httpwww_opengis_netswe1_0_DataBlockDefinitionType_httpwww_opengis_netswe1_0encoding', False)

    
    encoding = property(__encoding.value, __encoding.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}components uses Python identifier components
    __components = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'components'), 'components', '__httpwww_opengis_netswe1_0_DataBlockDefinitionType_httpwww_opengis_netswe1_0components', False)

    
    components = property(__components.value, __components.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'id'), 'id', '__httpwww_opengis_netswe1_0_DataBlockDefinitionType_id', pyxb.binding.datatypes.ID)
    
    id = property(__id.value, __id.set, None, None)


    _ElementMap = {
        __encoding.name() : __encoding,
        __components.name() : __components
    }
    _AttributeMap = {
        __id.name() : __id
    }
Namespace.addCategoryObject('typeBinding', u'DataBlockDefinitionType', DataBlockDefinitionType)


# Complex type AllowedTokensPropertyType with content type ELEMENT_ONLY
class AllowedTokensPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AllowedTokensPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}AllowedTokens uses Python identifier AllowedTokens
    __AllowedTokens = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AllowedTokens'), 'AllowedTokens', '__httpwww_opengis_netswe1_0_AllowedTokensPropertyType_httpwww_opengis_netswe1_0AllowedTokens', False)

    
    AllowedTokens = property(__AllowedTokens.value, __AllowedTokens.set, None, u'Enumeration of allowed values')

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_AllowedTokensPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_AllowedTokensPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_AllowedTokensPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_AllowedTokensPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_AllowedTokensPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_AllowedTokensPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_AllowedTokensPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_AllowedTokensPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)


    _ElementMap = {
        __AllowedTokens.name() : __AllowedTokens
    }
    _AttributeMap = {
        __title.name() : __title,
        __remoteSchema.name() : __remoteSchema,
        __type.name() : __type,
        __arcrole.name() : __arcrole,
        __show.name() : __show,
        __actuate.name() : __actuate,
        __href.name() : __href,
        __role.name() : __role
    }
Namespace.addCategoryObject('typeBinding', u'AllowedTokensPropertyType', AllowedTokensPropertyType)


# Complex type EnvelopeType with content type ELEMENT_ONLY
class EnvelopeType (AbstractVectorType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'EnvelopeType')
    # Base type is AbstractVectorType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}upperCorner uses Python identifier upperCorner
    __upperCorner = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'upperCorner'), 'upperCorner', '__httpwww_opengis_netswe1_0_EnvelopeType_httpwww_opengis_netswe1_0upperCorner', False)

    
    upperCorner = property(__upperCorner.value, __upperCorner.set, None, None)

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}time uses Python identifier time
    __time = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'time'), 'time', '__httpwww_opengis_netswe1_0_EnvelopeType_httpwww_opengis_netswe1_0time', False)

    
    time = property(__time.value, __time.set, None, u'Optionally provides time range during which this bounding envelope applies')

    
    # Element {http://www.opengis.net/swe/1.0}lowerCorner uses Python identifier lowerCorner
    __lowerCorner = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lowerCorner'), 'lowerCorner', '__httpwww_opengis_netswe1_0_EnvelopeType_httpwww_opengis_netswe1_0lowerCorner', False)

    
    lowerCorner = property(__lowerCorner.value, __lowerCorner.set, None, None)

    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute referenceFrame inherited from {http://www.opengis.net/swe/1.0}AbstractVectorType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute localFrame inherited from {http://www.opengis.net/swe/1.0}AbstractVectorType

    _ElementMap = AbstractVectorType._ElementMap.copy()
    _ElementMap.update({
        __upperCorner.name() : __upperCorner,
        __time.name() : __time,
        __lowerCorner.name() : __lowerCorner
    })
    _AttributeMap = AbstractVectorType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'EnvelopeType', EnvelopeType)


# Complex type TimePropertyType with content type ELEMENT_ONLY
class TimePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Time uses Python identifier Time
    __Time = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Time'), 'Time', '__httpwww_opengis_netswe1_0_TimePropertyType_httpwww_opengis_netswe1_0Time', False)

    
    Time = property(__Time.value, __Time.set, None, u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin')


    _ElementMap = {
        __Time.name() : __Time
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TimePropertyType', TimePropertyType)


# Complex type CTD_ANON_22 with content type ELEMENT_ONLY
class CTD_ANON_22 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}QuantityRange uses Python identifier QuantityRange
    __QuantityRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), 'QuantityRange', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netswe1_0QuantityRange', False)

    
    QuantityRange = property(__QuantityRange.value, __QuantityRange.set, None, u'Decimal pair for specifying a quantity range with constraints')

    
    # Element {http://www.opengis.net/swe/1.0}AbstractDataRecord uses Python identifier AbstractDataRecord
    __AbstractDataRecord = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord'), 'AbstractDataRecord', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netswe1_0AbstractDataRecord', False)

    
    AbstractDataRecord = property(__AbstractDataRecord.value, __AbstractDataRecord.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}Category uses Python identifier Category
    __Category = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Category'), 'Category', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netswe1_0Category', False)

    
    Category = property(__Category.value, __Category.set, None, u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value')

    
    # Element {http://www.opengis.net/swe/1.0}Time uses Python identifier Time
    __Time = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Time'), 'Time', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netswe1_0Time', False)

    
    Time = property(__Time.value, __Time.set, None, u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin')

    
    # Element {http://www.opengis.net/swe/1.0}CountRange uses Python identifier CountRange
    __CountRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'CountRange'), 'CountRange', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netswe1_0CountRange', False)

    
    CountRange = property(__CountRange.value, __CountRange.set, None, u'Integer pair used for specifying a count range')

    
    # Element {http://www.opengis.net/swe/1.0}AbstractDataArray uses Python identifier AbstractDataArray
    __AbstractDataArray = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray'), 'AbstractDataArray', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netswe1_0AbstractDataArray', False)

    
    AbstractDataArray = property(__AbstractDataArray.value, __AbstractDataArray.set, None, u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways')

    
    # Element {http://www.opengis.net/swe/1.0}Text uses Python identifier Text
    __Text = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Text'), 'Text', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netswe1_0Text', False)

    
    Text = property(__Text.value, __Text.set, None, u'Free textual component')

    
    # Element {http://www.opengis.net/swe/1.0}Boolean uses Python identifier Boolean
    __Boolean = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), 'Boolean', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netswe1_0Boolean', False)

    
    Boolean = property(__Boolean.value, __Boolean.set, None, u'Scalar component used to express truth: True or False, 0 or 1')

    
    # Element {http://www.opengis.net/swe/1.0}Count uses Python identifier Count
    __Count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Count'), 'Count', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netswe1_0Count', False)

    
    Count = property(__Count.value, __Count.set, None, u'Integer number used for a counting value')

    
    # Element {http://www.opengis.net/swe/1.0}TimeRange uses Python identifier TimeRange
    __TimeRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeRange'), 'TimeRange', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netswe1_0TimeRange', False)

    
    TimeRange = property(__TimeRange.value, __TimeRange.set, None, u'Time value pair for specifying a time range (can be a decimal or ISO 8601)')

    
    # Element {http://www.opengis.net/swe/1.0}Quantity uses Python identifier Quantity
    __Quantity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), 'Quantity', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netswe1_0Quantity', False)

    
    Quantity = property(__Quantity.value, __Quantity.set, None, u'Decimal number with optional unit and constraints')

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_CTD_ANON_22_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_netswe1_0_CTD_ANON_22_name', pyxb.binding.datatypes.token, required=True)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __QuantityRange.name() : __QuantityRange,
        __AbstractDataRecord.name() : __AbstractDataRecord,
        __Category.name() : __Category,
        __Time.name() : __Time,
        __CountRange.name() : __CountRange,
        __AbstractDataArray.name() : __AbstractDataArray,
        __Text.name() : __Text,
        __Boolean.name() : __Boolean,
        __Count.name() : __Count,
        __TimeRange.name() : __TimeRange,
        __Quantity.name() : __Quantity
    }
    _AttributeMap = {
        __remoteSchema.name() : __remoteSchema,
        __role.name() : __role,
        __arcrole.name() : __arcrole,
        __actuate.name() : __actuate,
        __href.name() : __href,
        __title.name() : __title,
        __show.name() : __show,
        __type.name() : __type,
        __name.name() : __name
    }



# Complex type CTD_ANON_23 with content type ELEMENT_ONLY
class CTD_ANON_23 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}high uses Python identifier high
    __high = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'high'), 'high', '__httpwww_opengis_netswe1_0_CTD_ANON_23_httpwww_opengis_netswe1_0high', False)

    
    high = property(__high.value, __high.set, None, None)

    
    # Element {http://www.opengis.net/swe/1.0}low uses Python identifier low
    __low = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'low'), 'low', '__httpwww_opengis_netswe1_0_CTD_ANON_23_httpwww_opengis_netswe1_0low', False)

    
    low = property(__low.value, __low.set, None, None)


    _ElementMap = {
        __high.name() : __high,
        __low.name() : __low
    }
    _AttributeMap = {
        
    }



# Complex type AbstractConditionalType with content type ELEMENT_ONLY
class AbstractConditionalType (AbstractDataRecordType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AbstractConditionalType')
    # Base type is AbstractDataRecordType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}condition uses Python identifier condition
    __condition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'condition'), 'condition', '__httpwww_opengis_netswe1_0_AbstractConditionalType_httpwww_opengis_netswe1_0condition', True)

    
    condition = property(__condition.value, __condition.set, None, u'Specifies one or more conditions for which the given value is valid')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractDataRecordType._ElementMap.copy()
    _ElementMap.update({
        __condition.name() : __condition
    })
    _AttributeMap = AbstractDataRecordType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'AbstractConditionalType', AbstractConditionalType)


# Complex type ConditionalValueType with content type ELEMENT_ONLY
class ConditionalValueType (AbstractConditionalType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ConditionalValueType')
    # Base type is AbstractConditionalType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element condition ({http://www.opengis.net/swe/1.0}condition) inherited from {http://www.opengis.net/swe/1.0}AbstractConditionalType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}data uses Python identifier data
    __data = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'data'), 'data', '__httpwww_opengis_netswe1_0_ConditionalValueType_httpwww_opengis_netswe1_0data', False)

    
    data = property(__data.value, __data.set, None, None)

    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractConditionalType._ElementMap.copy()
    _ElementMap.update({
        __data.name() : __data
    })
    _AttributeMap = AbstractConditionalType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ConditionalValueType', ConditionalValueType)


# Complex type TimeObjectPropertyType with content type ELEMENT_ONLY
class TimeObjectPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeObjectPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/gml}_TimeObject uses Python identifier TimeObject
    __TimeObject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_TimeObject'), 'TimeObject', '__httpwww_opengis_netswe1_0_TimeObjectPropertyType_httpwww_opengis_netgml_TimeObject', False)

    
    TimeObject = property(__TimeObject.value, __TimeObject.set, None, u'This abstract element acts as the head of the substitution group for temporal primitives and complexes.')

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_TimeObjectPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_TimeObjectPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_TimeObjectPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_TimeObjectPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_TimeObjectPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_TimeObjectPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_TimeObjectPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_TimeObjectPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)


    _ElementMap = {
        __TimeObject.name() : __TimeObject
    }
    _AttributeMap = {
        __type.name() : __type,
        __title.name() : __title,
        __remoteSchema.name() : __remoteSchema,
        __actuate.name() : __actuate,
        __show.name() : __show,
        __href.name() : __href,
        __arcrole.name() : __arcrole,
        __role.name() : __role
    }
Namespace.addCategoryObject('typeBinding', u'TimeObjectPropertyType', TimeObjectPropertyType)


# Complex type CurveType with content type ELEMENT_ONLY
class CurveType (AbstractDataArrayType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CurveType')
    # Base type is AbstractDataArrayType
    
    # Element {http://www.opengis.net/swe/1.0}encoding uses Python identifier encoding
    __encoding = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'encoding'), 'encoding', '__httpwww_opengis_netswe1_0_CurveType_httpwww_opengis_netswe1_0encoding', False)

    
    encoding = property(__encoding.value, __encoding.set, None, u'Specifies an encoding for the data structure defined by the enclosing element')

    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element elementCount ({http://www.opengis.net/swe/1.0}elementCount) inherited from {http://www.opengis.net/swe/1.0}AbstractDataArrayType
    
    # Element {http://www.opengis.net/swe/1.0}values uses Python identifier values
    __values = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'values'), 'values', '__httpwww_opengis_netswe1_0_CurveType_httpwww_opengis_netswe1_0values', False)

    
    values = property(__values.value, __values.set, None, u'Carries the block of values encoded as specified by the encoding element')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}elementType uses Python identifier elementType
    __elementType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'elementType'), 'elementType', '__httpwww_opengis_netswe1_0_CurveType_httpwww_opengis_netswe1_0elementType', False)

    
    elementType = property(__elementType.value, __elementType.set, None, None)

    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractDataArrayType._ElementMap.copy()
    _ElementMap.update({
        __encoding.name() : __encoding,
        __values.name() : __values,
        __elementType.name() : __elementType
    })
    _AttributeMap = AbstractDataArrayType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'CurveType', CurveType)


# Complex type AnyScalarPropertyType with content type ELEMENT_ONLY
class AnyScalarPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AnyScalarPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Boolean uses Python identifier Boolean
    __Boolean = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), 'Boolean', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_opengis_netswe1_0Boolean', False)

    
    Boolean = property(__Boolean.value, __Boolean.set, None, u'Scalar component used to express truth: True or False, 0 or 1')

    
    # Element {http://www.opengis.net/swe/1.0}Category uses Python identifier Category
    __Category = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Category'), 'Category', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_opengis_netswe1_0Category', False)

    
    Category = property(__Category.value, __Category.set, None, u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value')

    
    # Element {http://www.opengis.net/swe/1.0}Quantity uses Python identifier Quantity
    __Quantity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), 'Quantity', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_opengis_netswe1_0Quantity', False)

    
    Quantity = property(__Quantity.value, __Quantity.set, None, u'Decimal number with optional unit and constraints')

    
    # Element {http://www.opengis.net/swe/1.0}Text uses Python identifier Text
    __Text = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Text'), 'Text', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_opengis_netswe1_0Text', False)

    
    Text = property(__Text.value, __Text.set, None, u'Free textual component')

    
    # Element {http://www.opengis.net/swe/1.0}Time uses Python identifier Time
    __Time = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Time'), 'Time', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_opengis_netswe1_0Time', False)

    
    Time = property(__Time.value, __Time.set, None, u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin')

    
    # Element {http://www.opengis.net/swe/1.0}Count uses Python identifier Count
    __Count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Count'), 'Count', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_opengis_netswe1_0Count', False)

    
    Count = property(__Count.value, __Count.set, None, u'Integer number used for a counting value')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_name', pyxb.binding.datatypes.token, required=True)
    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_AnyScalarPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")


    _ElementMap = {
        __Boolean.name() : __Boolean,
        __Category.name() : __Category,
        __Quantity.name() : __Quantity,
        __Text.name() : __Text,
        __Time.name() : __Time,
        __Count.name() : __Count
    }
    _AttributeMap = {
        __href.name() : __href,
        __role.name() : __role,
        __remoteSchema.name() : __remoteSchema,
        __type.name() : __type,
        __title.name() : __title,
        __name.name() : __name,
        __arcrole.name() : __arcrole,
        __show.name() : __show,
        __actuate.name() : __actuate
    }
Namespace.addCategoryObject('typeBinding', u'AnyScalarPropertyType', AnyScalarPropertyType)


# Complex type BooleanPropertyType with content type ELEMENT_ONLY
class BooleanPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BooleanPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Boolean uses Python identifier Boolean
    __Boolean = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), 'Boolean', '__httpwww_opengis_netswe1_0_BooleanPropertyType_httpwww_opengis_netswe1_0Boolean', False)

    
    Boolean = property(__Boolean.value, __Boolean.set, None, u'Scalar component used to express truth: True or False, 0 or 1')


    _ElementMap = {
        __Boolean.name() : __Boolean
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'BooleanPropertyType', BooleanPropertyType)


# Complex type TimeInstantGridPropertyType with content type ELEMENT_ONLY
class TimeInstantGridPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeInstantGridPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}TimeInstantGrid uses Python identifier TimeInstantGrid
    __TimeInstantGrid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeInstantGrid'), 'TimeInstantGrid', '__httpwww_opengis_netswe1_0_TimeInstantGridPropertyType_httpwww_opengis_netswe1_0TimeInstantGrid', False)

    
    TimeInstantGrid = property(__TimeInstantGrid.value, __TimeInstantGrid.set, None, u'A set of uniformly spaced time instants described using an implicit notation')

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_TimeInstantGridPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_TimeInstantGridPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_TimeInstantGridPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_TimeInstantGridPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_TimeInstantGridPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_TimeInstantGridPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_TimeInstantGridPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_TimeInstantGridPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)


    _ElementMap = {
        __TimeInstantGrid.name() : __TimeInstantGrid
    }
    _AttributeMap = {
        __arcrole.name() : __arcrole,
        __actuate.name() : __actuate,
        __show.name() : __show,
        __href.name() : __href,
        __remoteSchema.name() : __remoteSchema,
        __role.name() : __role,
        __type.name() : __type,
        __title.name() : __title
    }
Namespace.addCategoryObject('typeBinding', u'TimeInstantGridPropertyType', TimeInstantGridPropertyType)


# Complex type CTD_ANON_24 with content type ELEMENT_ONLY
class CTD_ANON_24 (AbstractVectorType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractVectorType
    
    # Element {http://www.opengis.net/swe/1.0}member uses Python identifier member
    __member = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'member'), 'member', '__httpwww_opengis_netswe1_0_CTD_ANON_24_httpwww_opengis_netswe1_0member', True)

    
    member = property(__member.value, __member.set, None, u'Is this an aggregate geometry?')

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute referenceFrame inherited from {http://www.opengis.net/swe/1.0}AbstractVectorType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute name uses Python identifier name_
    __name_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name_', '__httpwww_opengis_netswe1_0_CTD_ANON_24_name', pyxb.binding.datatypes.token)
    
    name_ = property(__name_.value, __name_.set, None, None)

    
    # Attribute localFrame inherited from {http://www.opengis.net/swe/1.0}AbstractVectorType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractVectorType._ElementMap.copy()
    _ElementMap.update({
        __member.name() : __member
    })
    _AttributeMap = AbstractVectorType._AttributeMap.copy()
    _AttributeMap.update({
        __name_.name() : __name_
    })



# Complex type ScopedNameType with content type SIMPLE
class ScopedNameType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ScopedNameType')
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute codeSpace uses Python identifier codeSpace
    __codeSpace = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'codeSpace'), 'codeSpace', '__httpwww_opengis_netswe1_0_ScopedNameType_codeSpace', pyxb.binding.datatypes.anyURI, required=True)
    
    codeSpace = property(__codeSpace.value, __codeSpace.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __codeSpace.name() : __codeSpace
    }
Namespace.addCategoryObject('typeBinding', u'ScopedNameType', ScopedNameType)


# Complex type CountRangePropertyType with content type ELEMENT_ONLY
class CountRangePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CountRangePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}CountRange uses Python identifier CountRange
    __CountRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'CountRange'), 'CountRange', '__httpwww_opengis_netswe1_0_CountRangePropertyType_httpwww_opengis_netswe1_0CountRange', False)

    
    CountRange = property(__CountRange.value, __CountRange.set, None, u'Integer pair used for specifying a count range')


    _ElementMap = {
        __CountRange.name() : __CountRange
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'CountRangePropertyType', CountRangePropertyType)


# Complex type ConditionalDataType with content type ELEMENT_ONLY
class ConditionalDataType (AbstractDataRecordType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ConditionalDataType')
    # Base type is AbstractDataRecordType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/swe/1.0}case uses Python identifier case
    __case = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'case'), 'case', '__httpwww_opengis_netswe1_0_ConditionalDataType_httpwww_opengis_netswe1_0case', True)

    
    case = property(__case.value, __case.set, None, None)

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractDataRecordType._ElementMap.copy()
    _ElementMap.update({
        __case.name() : __case
    })
    _AttributeMap = AbstractDataRecordType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ConditionalDataType', ConditionalDataType)


# Complex type TypedValueType with content type ELEMENT_ONLY
class TypedValueType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TypedValueType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netswe1_0_TypedValueType_httpwww_opengis_netswe1_0value', False)

    
    value_ = property(__value.value, __value.set, None, u'Implicit xs:anyType')

    
    # Element {http://www.opengis.net/swe/1.0}property uses Python identifier property_
    __property = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'property'), 'property_', '__httpwww_opengis_netswe1_0_TypedValueType_httpwww_opengis_netswe1_0property', False)

    
    property_ = property(__property.value, __property.set, None, u'This element attribute indicates the semantics of the typed value. \n\t\t\t\t\tUsually identifies a property or phenomenon definition. ')


    _ElementMap = {
        __value.name() : __value,
        __property.name() : __property
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TypedValueType', TypedValueType)


# Complex type CountPropertyType with content type ELEMENT_ONLY
class CountPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CountPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Count uses Python identifier Count
    __Count = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Count'), 'Count', '__httpwww_opengis_netswe1_0_CountPropertyType_httpwww_opengis_netswe1_0Count', False)

    
    Count = property(__Count.value, __Count.set, None, u'Integer number used for a counting value')


    _ElementMap = {
        __Count.name() : __Count
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'CountPropertyType', CountPropertyType)


# Complex type AllowedTimesPropertyType with content type ELEMENT_ONLY
class AllowedTimesPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AllowedTimesPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}AllowedTimes uses Python identifier AllowedTimes
    __AllowedTimes = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AllowedTimes'), 'AllowedTimes', '__httpwww_opengis_netswe1_0_AllowedTimesPropertyType_httpwww_opengis_netswe1_0AllowedTimes', False)

    
    AllowedTimes = property(__AllowedTimes.value, __AllowedTimes.set, None, u'List of allowed time values (There is an implicit AND between all members)')

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_AllowedTimesPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_AllowedTimesPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_AllowedTimesPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_AllowedTimesPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_AllowedTimesPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_AllowedTimesPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_AllowedTimesPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_AllowedTimesPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')


    _ElementMap = {
        __AllowedTimes.name() : __AllowedTimes
    }
    _AttributeMap = {
        __role.name() : __role,
        __type.name() : __type,
        __title.name() : __title,
        __href.name() : __href,
        __arcrole.name() : __arcrole,
        __actuate.name() : __actuate,
        __show.name() : __show,
        __remoteSchema.name() : __remoteSchema
    }
Namespace.addCategoryObject('typeBinding', u'AllowedTimesPropertyType', AllowedTimesPropertyType)


# Complex type SimpleDataRecordPropertyType with content type ELEMENT_ONLY
class SimpleDataRecordPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SimpleDataRecordPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}SimpleDataRecord uses Python identifier SimpleDataRecord
    __SimpleDataRecord = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'SimpleDataRecord'), 'SimpleDataRecord', '__httpwww_opengis_netswe1_0_SimpleDataRecordPropertyType_httpwww_opengis_netswe1_0SimpleDataRecord', False)

    
    SimpleDataRecord = property(__SimpleDataRecord.value, __SimpleDataRecord.set, None, u'Implementation of ISO-11404 Record datatype that takes only simple scalars (i.e. no data aggregates)')


    _ElementMap = {
        __SimpleDataRecord.name() : __SimpleDataRecord
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SimpleDataRecordPropertyType', SimpleDataRecordPropertyType)


# Complex type TimeAggregatePropertyType with content type ELEMENT_ONLY
class TimeAggregatePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeAggregatePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}TimeAggregate uses Python identifier TimeAggregate
    __TimeAggregate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeAggregate'), 'TimeAggregate', '__httpwww_opengis_netswe1_0_TimeAggregatePropertyType_httpwww_opengis_netswe1_0TimeAggregate', False)

    
    TimeAggregate = property(__TimeAggregate.value, __TimeAggregate.set, None, u'an arbitrary set of TimeObjects, often TimeInstants and TimePeriods')

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_TimeAggregatePropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_TimeAggregatePropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_TimeAggregatePropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_TimeAggregatePropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_TimeAggregatePropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_TimeAggregatePropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_TimeAggregatePropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_TimeAggregatePropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)


    _ElementMap = {
        __TimeAggregate.name() : __TimeAggregate
    }
    _AttributeMap = {
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __remoteSchema.name() : __remoteSchema,
        __show.name() : __show,
        __actuate.name() : __actuate,
        __href.name() : __href,
        __role.name() : __role,
        __type.name() : __type
    }
Namespace.addCategoryObject('typeBinding', u'TimeAggregatePropertyType', TimeAggregatePropertyType)


# Complex type TimeRangePropertyType with content type ELEMENT_ONLY
class TimeRangePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeRangePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}TimeRange uses Python identifier TimeRange
    __TimeRange = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeRange'), 'TimeRange', '__httpwww_opengis_netswe1_0_TimeRangePropertyType_httpwww_opengis_netswe1_0TimeRange', False)

    
    TimeRange = property(__TimeRange.value, __TimeRange.set, None, u'Time value pair for specifying a time range (can be a decimal or ISO 8601)')


    _ElementMap = {
        __TimeRange.name() : __TimeRange
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TimeRangePropertyType', TimeRangePropertyType)


# Complex type TimeGridEnvelopePropertyType with content type ELEMENT_ONLY
class TimeGridEnvelopePropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeGridEnvelopePropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}TimeGridEnvelope uses Python identifier TimeGridEnvelope
    __TimeGridEnvelope = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeGridEnvelope'), 'TimeGridEnvelope', '__httpwww_opengis_netswe1_0_TimeGridEnvelopePropertyType_httpwww_opengis_netswe1_0TimeGridEnvelope', False)

    
    TimeGridEnvelope = property(__TimeGridEnvelope.value, __TimeGridEnvelope.set, None, u'Grid extent specified in grid coordinates - i.e. 2 integers')


    _ElementMap = {
        __TimeGridEnvelope.name() : __TimeGridEnvelope
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TimeGridEnvelopePropertyType', TimeGridEnvelopePropertyType)


# Complex type IntervalPropertyType with content type ELEMENT_ONLY
class IntervalPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IntervalPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}Interval uses Python identifier Interval
    __Interval = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Interval'), 'Interval', '__httpwww_opengis_netswe1_0_IntervalPropertyType_httpwww_opengis_netswe1_0Interval', False)

    
    Interval = property(__Interval.value, __Interval.set, None, u'A generic interval. The type of the two limits will normally be the same.')


    _ElementMap = {
        __Interval.name() : __Interval
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'IntervalPropertyType', IntervalPropertyType)


# Complex type TimeIntervalGridPropertyType with content type ELEMENT_ONLY
class TimeIntervalGridPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeIntervalGridPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}TimeIntervalGrid uses Python identifier TimeIntervalGrid
    __TimeIntervalGrid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeIntervalGrid'), 'TimeIntervalGrid', '__httpwww_opengis_netswe1_0_TimeIntervalGridPropertyType_httpwww_opengis_netswe1_0TimeIntervalGrid', False)

    
    TimeIntervalGrid = property(__TimeIntervalGrid.value, __TimeIntervalGrid.set, None, u'A set of uniformly spaced time intervals described using an implicit notation')

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_TimeIntervalGridPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_TimeIntervalGridPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_TimeIntervalGridPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_TimeIntervalGridPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_TimeIntervalGridPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_TimeIntervalGridPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_TimeIntervalGridPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_TimeIntervalGridPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)


    _ElementMap = {
        __TimeIntervalGrid.name() : __TimeIntervalGrid
    }
    _AttributeMap = {
        __arcrole.name() : __arcrole,
        __actuate.name() : __actuate,
        __show.name() : __show,
        __href.name() : __href,
        __role.name() : __role,
        __remoteSchema.name() : __remoteSchema,
        __type.name() : __type,
        __title.name() : __title
    }
Namespace.addCategoryObject('typeBinding', u'TimeIntervalGridPropertyType', TimeIntervalGridPropertyType)


# Complex type DataStreamDefinitionPropertyType with content type ELEMENT_ONLY
class DataStreamDefinitionPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataStreamDefinitionPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}DataStreamDefinition uses Python identifier DataStreamDefinition
    __DataStreamDefinition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'DataStreamDefinition'), 'DataStreamDefinition', '__httpwww_opengis_netswe1_0_DataStreamDefinitionPropertyType_httpwww_opengis_netswe1_0DataStreamDefinition', False)

    
    DataStreamDefinition = property(__DataStreamDefinition.value, __DataStreamDefinition.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_DataStreamDefinitionPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_DataStreamDefinitionPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_DataStreamDefinitionPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_DataStreamDefinitionPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_DataStreamDefinitionPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_DataStreamDefinitionPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_DataStreamDefinitionPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_DataStreamDefinitionPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)


    _ElementMap = {
        __DataStreamDefinition.name() : __DataStreamDefinition
    }
    _AttributeMap = {
        __role.name() : __role,
        __type.name() : __type,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __remoteSchema.name() : __remoteSchema,
        __actuate.name() : __actuate,
        __show.name() : __show,
        __href.name() : __href
    }
Namespace.addCategoryObject('typeBinding', u'DataStreamDefinitionPropertyType', DataStreamDefinitionPropertyType)


# Complex type TimeGridPropertyType with content type ELEMENT_ONLY
class TimeGridPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeGridPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}TimeInstantGrid uses Python identifier TimeInstantGrid
    __TimeInstantGrid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeInstantGrid'), 'TimeInstantGrid', '__httpwww_opengis_netswe1_0_TimeGridPropertyType_httpwww_opengis_netswe1_0TimeInstantGrid', False)

    
    TimeInstantGrid = property(__TimeInstantGrid.value, __TimeInstantGrid.set, None, u'A set of uniformly spaced time instants described using an implicit notation')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_TimeGridPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_TimeGridPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_TimeGridPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_TimeGridPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_TimeGridPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_TimeGridPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_TimeGridPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_TimeGridPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')


    _ElementMap = {
        __TimeInstantGrid.name() : __TimeInstantGrid
    }
    _AttributeMap = {
        __href.name() : __href,
        __role.name() : __role,
        __type.name() : __type,
        __show.name() : __show,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __actuate.name() : __actuate,
        __remoteSchema.name() : __remoteSchema
    }
Namespace.addCategoryObject('typeBinding', u'TimeGridPropertyType', TimeGridPropertyType)


# Complex type MultiplexedStreamFormatPropertyType with content type ELEMENT_ONLY
class MultiplexedStreamFormatPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MultiplexedStreamFormatPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/swe/1.0}MultiplexedStreamFormat uses Python identifier MultiplexedStreamFormat
    __MultiplexedStreamFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'MultiplexedStreamFormat'), 'MultiplexedStreamFormat', '__httpwww_opengis_netswe1_0_MultiplexedStreamFormatPropertyType_httpwww_opengis_netswe1_0MultiplexedStreamFormat', False)

    
    MultiplexedStreamFormat = property(__MultiplexedStreamFormat.value, __MultiplexedStreamFormat.set, None, u'Allows specification of the stream/packaging format used (ex: RTP, ASF, AAF, TML...)')

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netswe1_0_MultiplexedStreamFormatPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netswe1_0_MultiplexedStreamFormatPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netswe1_0_MultiplexedStreamFormatPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netswe1_0_MultiplexedStreamFormatPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netswe1_0_MultiplexedStreamFormatPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netswe1_0_MultiplexedStreamFormatPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netswe1_0_MultiplexedStreamFormatPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netswe1_0_MultiplexedStreamFormatPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)


    _ElementMap = {
        __MultiplexedStreamFormat.name() : __MultiplexedStreamFormat
    }
    _AttributeMap = {
        __actuate.name() : __actuate,
        __show.name() : __show,
        __href.name() : __href,
        __role.name() : __role,
        __title.name() : __title,
        __arcrole.name() : __arcrole,
        __remoteSchema.name() : __remoteSchema,
        __type.name() : __type
    }
Namespace.addCategoryObject('typeBinding', u'MultiplexedStreamFormatPropertyType', MultiplexedStreamFormatPropertyType)


# Complex type CTD_ANON_25 with content type ELEMENT_ONLY
class CTD_ANON_25 (AbstractDataComponentType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is AbstractDataComponentType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute fixed inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute definition inherited from {http://www.opengis.net/swe/1.0}AbstractDataComponentType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = AbstractDataComponentType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = AbstractDataComponentType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



Vector = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Vector'), VectorType, documentation=u'A Vector is a special type of DataRecord that takes a list of numerical scalars called coordinates. The Vector has a referenceFrame in which the coordinates are expressed')
Namespace.addCategoryObject('elementBinding', Vector.name().localName(), Vector)

AllowedTokens = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AllowedTokens'), CTD_ANON_5, documentation=u'Enumeration of allowed values')
Namespace.addCategoryObject('elementBinding', AllowedTokens.name().localName(), AllowedTokens)

NormalizedCurve = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NormalizedCurve'), NormalizedCurveType)
Namespace.addCategoryObject('elementBinding', NormalizedCurve.name().localName(), NormalizedCurve)

StandardFormat = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'StandardFormat'), CTD_ANON_6)
Namespace.addCategoryObject('elementBinding', StandardFormat.name().localName(), StandardFormat)

TimeAggregate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeAggregate'), TimeAggregateType, documentation=u'an arbitrary set of TimeObjects, often TimeInstants and TimePeriods')
Namespace.addCategoryObject('elementBinding', TimeAggregate.name().localName(), TimeAggregate)

TimeGeometricComplex = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeGeometricComplex'), TimeGeometricComplexType, documentation=u'Explicit implementation of ISO 19108 TM_GeometricComplex - a self-consistent set of TimeInstants and TimePeriods')
Namespace.addCategoryObject('elementBinding', TimeGeometricComplex.name().localName(), TimeGeometricComplex)

DataRecord = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DataRecord'), DataRecordType, documentation=u'Implementation of ISO-11404 Record datatype. This allows grouping of data components which can themselves be Records, Arrays or Simple Types')
Namespace.addCategoryObject('elementBinding', DataRecord.name().localName(), DataRecord)

Text = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Text'), CTD_ANON_8, documentation=u'Free textual component')
Namespace.addCategoryObject('elementBinding', Text.name().localName(), Text)

Array = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Array'), ArrayType, documentation=u'An array is an indexed set of records of homogeneous type')
Namespace.addCategoryObject('elementBinding', Array.name().localName(), Array)

Time = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Time'), CTD_ANON_9, documentation=u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin')
Namespace.addCategoryObject('elementBinding', Time.name().localName(), Time)

DataArray = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DataArray'), DataArrayType, documentation=u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways')
Namespace.addCategoryObject('elementBinding', DataArray.name().localName(), DataArray)

Item = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Item'), pyxb.binding.datatypes.anyType, documentation=u'An Item is an item of data of any type')
Namespace.addCategoryObject('elementBinding', Item.name().localName(), Item)

CompositePhenomenon = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CompositePhenomenon'), CompositePhenomenonType, documentation=u'A Phenomenon defined as a set of explicitly enumerated components which may or may not be related to one another')
Namespace.addCategoryObject('elementBinding', CompositePhenomenon.name().localName(), CompositePhenomenon)

BinaryBlock = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BinaryBlock'), CTD_ANON_14)
Namespace.addCategoryObject('elementBinding', BinaryBlock.name().localName(), BinaryBlock)

PhenomenonSeries = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'PhenomenonSeries'), PhenomenonSeriesType, documentation=u'A phenomenon defined as a base property convolved with a set of constraints\n      The set of constraints may be either\n      * an explicit set of soft-typed measures, intervals and categories\n      * one or more lists of soft-typed measures, intervals and categories\n      * one or more sequences of soft-typed measures and intervals')
Namespace.addCategoryObject('elementBinding', PhenomenonSeries.name().localName(), PhenomenonSeries)

CountRange = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CountRange'), CTD_ANON_16, documentation=u'Integer pair used for specifying a count range')
Namespace.addCategoryObject('elementBinding', CountRange.name().localName(), CountRange)

TimeInstantGrid = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeInstantGrid'), TimeInstantGridType, documentation=u'A set of uniformly spaced time instants described using an implicit notation')
Namespace.addCategoryObject('elementBinding', TimeInstantGrid.name().localName(), TimeInstantGrid)

AllowedTimes = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AllowedTimes'), CTD_ANON_17, documentation=u'List of allowed time values (There is an implicit AND between all members)')
Namespace.addCategoryObject('elementBinding', AllowedTimes.name().localName(), AllowedTimes)

AbstractDataArray = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray'), AbstractDataArrayType, abstract=pyxb.binding.datatypes.boolean(1), documentation=u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways')
Namespace.addCategoryObject('elementBinding', AbstractDataArray.name().localName(), AbstractDataArray)

TextBlock = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TextBlock'), CTD_ANON_18)
Namespace.addCategoryObject('elementBinding', TextBlock.name().localName(), TextBlock)

MultiplexedStreamFormat = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'MultiplexedStreamFormat'), MultiplexedStreamFormatType, documentation=u'Allows specification of the stream/packaging format used (ex: RTP, ASF, AAF, TML...)')
Namespace.addCategoryObject('elementBinding', MultiplexedStreamFormat.name().localName(), MultiplexedStreamFormat)

SquareMatrix = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SquareMatrix'), SquareMatrixType, documentation=u'This is a square matrix (so the size is the square of one dimension) which is a DataArray of Quantities. \t\tIt has a referenceFrame in which the matrix components are described')
Namespace.addCategoryObject('elementBinding', SquareMatrix.name().localName(), SquareMatrix)

TimeRange = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeRange'), CTD_ANON_19, documentation=u'Time value pair for specifying a time range (can be a decimal or ISO 8601)')
Namespace.addCategoryObject('elementBinding', TimeRange.name().localName(), TimeRange)

DataStreamDefinition = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DataStreamDefinition'), DataStreamDefinitionType)
Namespace.addCategoryObject('elementBinding', DataStreamDefinition.name().localName(), DataStreamDefinition)

Category = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Category'), CTD_ANON_4, documentation=u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value')
Namespace.addCategoryObject('elementBinding', Category.name().localName(), Category)

TimeGrid = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeGrid'), TimeGridType, abstract=pyxb.binding.datatypes.boolean(1), documentation=u'A set of uniformly spaced time instants described using an implicit notation\n\t\t\t      Follow pattern of (ISO 19123) spatial grids: \n  these have (dimension,axisName,extent(,origin,offsetVector))\n  For temporal case, dimension is fixed (1), axisName is fixed ("time")')
Namespace.addCategoryObject('elementBinding', TimeGrid.name().localName(), TimeGrid)

Position = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Position'), PositionType, documentation=u'Position is given as a group of Vectors/Matrices, each of which can specify location, orientation, velocity, angularVelocity, acceleration or angularAcceleration or a combination of those in a composite state Vector. Each Vector can have a separate frame of reference or inherit the frame from the parent Position object.')
Namespace.addCategoryObject('elementBinding', Position.name().localName(), Position)

ConstrainedPhenomenon = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ConstrainedPhenomenon'), ConstrainedPhenomenonType, documentation=u'Description of a scalar Phenomenon defined by adding constraints to a property previously defined elsewhere.')
Namespace.addCategoryObject('elementBinding', ConstrainedPhenomenon.name().localName(), ConstrainedPhenomenon)

QuantityRange = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), CTD_ANON_15, documentation=u'Decimal pair for specifying a quantity range with constraints')
Namespace.addCategoryObject('elementBinding', QuantityRange.name().localName(), QuantityRange)

Phenomenon = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Phenomenon'), PhenomenonType, documentation=u'Basic Phenomenon definition, and head of substitution group of specialized phenomenon defs. ')
Namespace.addCategoryObject('elementBinding', Phenomenon.name().localName(), Phenomenon)

DataBlockDefinition = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DataBlockDefinition'), DataBlockDefinitionType)
Namespace.addCategoryObject('elementBinding', DataBlockDefinition.name().localName(), DataBlockDefinition)

TimeIntervalGrid = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeIntervalGrid'), TimeIntervalGridType, documentation=u'A set of uniformly spaced time intervals described using an implicit notation')
Namespace.addCategoryObject('elementBinding', TimeIntervalGrid.name().localName(), TimeIntervalGrid)

ConditionalValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ConditionalValue'), ConditionalValueType, documentation=u'Qualifies data (scalar or not) with one or more conditions')
Namespace.addCategoryObject('elementBinding', ConditionalValue.name().localName(), ConditionalValue)

Curve = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Curve'), CurveType, documentation=u'Curve describing variations of a parameter vs. another quantity')
Namespace.addCategoryObject('elementBinding', Curve.name().localName(), Curve)

AbstractDataRecord = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord'), AbstractDataRecordType, abstract=pyxb.binding.datatypes.boolean(1))
Namespace.addCategoryObject('elementBinding', AbstractDataRecord.name().localName(), AbstractDataRecord)

Count = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Count'), CTD_ANON_2, documentation=u'Integer number used for a counting value')
Namespace.addCategoryObject('elementBinding', Count.name().localName(), Count)

Boolean = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), CTD_ANON, documentation=u'Scalar component used to express truth: True or False, 0 or 1')
Namespace.addCategoryObject('elementBinding', Boolean.name().localName(), Boolean)

GeoLocationArea = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GeoLocationArea'), CTD_ANON_24, documentation=u'Area used to define bounding boxes')
Namespace.addCategoryObject('elementBinding', GeoLocationArea.name().localName(), GeoLocationArea)

ConditionalData = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ConditionalData'), ConditionalDataType, documentation=u'List of Conditional Values for a property')
Namespace.addCategoryObject('elementBinding', ConditionalData.name().localName(), ConditionalData)

TypedValue = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TypedValue'), TypedValueType, documentation=u'A generic soft-typed value')
Namespace.addCategoryObject('elementBinding', TypedValue.name().localName(), TypedValue)

Envelope = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Envelope'), EnvelopeType, documentation=u'Envelope described using two vectors specifying lower and upper corner points.\n           This is typically use to define rectangular bounding boxes in any coordinate system.')
Namespace.addCategoryObject('elementBinding', Envelope.name().localName(), Envelope)

CompoundPhenomenon = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CompoundPhenomenon'), CompoundPhenomenonType, abstract=pyxb.binding.datatypes.boolean(1), documentation=u'Description of a set of Phenomena.  \n\t  CompoundPhenomenon is the abstract head of a substitution group of specialized compound phenomena')
Namespace.addCategoryObject('elementBinding', CompoundPhenomenon.name().localName(), CompoundPhenomenon)

Record = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Record'), RecordType, documentation=u'A record is a list of fields')
Namespace.addCategoryObject('elementBinding', Record.name().localName(), Record)

XMLBlock = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'XMLBlock'), XMLBlockType, documentation=u'Carries the designator for an element implementing an XML-encoded data-type')
Namespace.addCategoryObject('elementBinding', XMLBlock.name().localName(), XMLBlock)

TypedValueList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TypedValueList'), TypedValueListType, documentation=u'A generic soft-typed list of values')
Namespace.addCategoryObject('elementBinding', TypedValueList.name().localName(), TypedValueList)

SimpleDataRecord = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SimpleDataRecord'), SimpleDataRecordType, documentation=u'Implementation of ISO-11404 Record datatype that takes only simple scalars (i.e. no data aggregates)')
Namespace.addCategoryObject('elementBinding', SimpleDataRecord.name().localName(), SimpleDataRecord)

ObservableProperty = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ObservableProperty'), CTD_ANON_25, documentation=u'ObservableProperty should be used to identify (through reference only) stimuli or measurable property types. The consequence is that it does not have a uom because it has not been measured yet.  This is used to define sensor/detector/actuator inputs and outputs, for instance.')
Namespace.addCategoryObject('elementBinding', ObservableProperty.name().localName(), ObservableProperty)

Quantity = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), CTD_ANON_12, documentation=u'Decimal number with optional unit and constraints')
Namespace.addCategoryObject('elementBinding', Quantity.name().localName(), Quantity)

AllowedValues = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AllowedValues'), CTD_ANON_13, documentation=u'List of allowed values (There is an implicit AND between all members)')
Namespace.addCategoryObject('elementBinding', AllowedValues.name().localName(), AllowedValues)

Interval = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Interval'), IntervalType, documentation=u'A generic interval. The type of the two limits will normally be the same.')
Namespace.addCategoryObject('elementBinding', Interval.name().localName(), Interval)


AbstractDataComponentType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractDataComponentType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AbstractDataComponentType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AbstractDataComponentType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
AbstractDataComponentType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractDataComponentType._GroupModel_3, min_occurs=1, max_occurs=1)
    )
AbstractDataComponentType._ContentModel = pyxb.binding.content.ParticleModel(AbstractDataComponentType._GroupModel_2, min_occurs=1, max_occurs=1)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'quality'), QualityPropertyType, scope=CTD_ANON, documentation=u'The quality property provides an indication of the reliability of estimates of the asociated value'))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.boolean, scope=CTD_ANON, documentation=u'Value is optional, to enable structure to act in a schema for values provided using other encodings'))
CTD_ANON._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel_4, min_occurs=1, max_occurs=1)
    )
CTD_ANON._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'quality')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel_5, min_occurs=1, max_occurs=1)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel_2, min_occurs=1, max_occurs=1)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CountRange'), CTD_ANON_16, scope=CTD_ANON_, documentation=u'Integer pair used for specifying a count range'))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), CTD_ANON, scope=CTD_ANON_, documentation=u'Scalar component used to express truth: True or False, 0 or 1'))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Category'), CTD_ANON_4, scope=CTD_ANON_, documentation=u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value'))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), CTD_ANON_15, scope=CTD_ANON_, documentation=u'Decimal pair for specifying a quantity range with constraints'))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord'), AbstractDataRecordType, abstract=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Time'), CTD_ANON_9, scope=CTD_ANON_, documentation=u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin'))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), CTD_ANON_12, scope=CTD_ANON_, documentation=u'Decimal number with optional unit and constraints'))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray'), AbstractDataArrayType, abstract=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_, documentation=u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways'))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeRange'), CTD_ANON_19, scope=CTD_ANON_, documentation=u'Time value pair for specifying a time range (can be a decimal or ISO 8601)'))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Text'), CTD_ANON_8, scope=CTD_ANON_, documentation=u'Free textual component'))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Count'), CTD_ANON_2, scope=CTD_ANON_, documentation=u'Integer number used for a counting value'))
CTD_ANON_._GroupModel_2 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Count')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Quantity')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Time')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Boolean')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Category')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Text')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_._GroupModel_3 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'CountRange')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeRange')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=0L, max_occurs=1)



PhenomenonPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Phenomenon'), PhenomenonType, scope=PhenomenonPropertyType, documentation=u'Basic Phenomenon definition, and head of substitution group of specialized phenomenon defs. '))
PhenomenonPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PhenomenonPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Phenomenon')), min_occurs=1, max_occurs=1)
    )
PhenomenonPropertyType._ContentModel = pyxb.binding.content.ParticleModel(PhenomenonPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.integer, scope=CTD_ANON_2, documentation=u'Value is optional, to enable structure to act in a schema for values provided using other encodings'))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'quality'), QualityPropertyType, scope=CTD_ANON_2, documentation=u'The quality property provides an indication of the reliability of estimates of the asociated value'))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'constraint'), AllowedValuesPropertyType, scope=CTD_ANON_2, documentation=u'The constraint property defines the permitted values, as a range or enumerated list'))
CTD_ANON_2._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_2._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel_4, min_occurs=1, max_occurs=1)
    )
CTD_ANON_2._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'constraint')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'quality')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_2._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel_5, min_occurs=1, max_occurs=1)
    )
CTD_ANON_2._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel_2, min_occurs=1, max_occurs=1)


AbstractDataRecordType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractDataRecordType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AbstractDataRecordType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AbstractDataRecordType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
AbstractDataRecordType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractDataRecordType._GroupModel_3, min_occurs=1, max_occurs=1)
    )
AbstractDataRecordType._ContentModel = pyxb.binding.content.ParticleModel(AbstractDataRecordType._GroupModel_2, min_occurs=1, max_occurs=1)


AbstractVectorType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractVectorType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AbstractVectorType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AbstractVectorType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
AbstractVectorType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractVectorType._GroupModel_3, min_occurs=1, max_occurs=1)
    )
AbstractVectorType._ContentModel = pyxb.binding.content.ParticleModel(AbstractVectorType._GroupModel_2, min_occurs=1, max_occurs=1)



VectorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'coordinate'), CTD_ANON_20, scope=VectorType))
VectorType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(VectorType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(VectorType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(VectorType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
VectorType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(VectorType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
VectorType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(VectorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'coordinate')), min_occurs=1, max_occurs=None)
    )
VectorType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(VectorType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(VectorType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
VectorType._ContentModel = pyxb.binding.content.ParticleModel(VectorType._GroupModel_2, min_occurs=1, max_occurs=1)



CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ConditionalValue'), ConditionalValueType, scope=CTD_ANON_3, documentation=u'Qualifies data (scalar or not) with one or more conditions'))
CTD_ANON_3._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ConditionalValue')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_3._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_3._GroupModel, min_occurs=1, max_occurs=1)



SimpleDataRecordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'field'), AnyScalarPropertyType, scope=SimpleDataRecordType))
SimpleDataRecordType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SimpleDataRecordType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SimpleDataRecordType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataRecordType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
SimpleDataRecordType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SimpleDataRecordType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
SimpleDataRecordType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SimpleDataRecordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'field')), min_occurs=0L, max_occurs=None)
    )
SimpleDataRecordType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SimpleDataRecordType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataRecordType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
SimpleDataRecordType._ContentModel = pyxb.binding.content.ParticleModel(SimpleDataRecordType._GroupModel_2, min_occurs=1, max_occurs=1)



CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'constraint'), AllowedTokensPropertyType, scope=CTD_ANON_4, documentation=u'The constraint property defines the permitted values, as an enumerated list'))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'quality'), QualityPropertyType, scope=CTD_ANON_4, documentation=u'The quality property provides an indication of the reliability of estimates of the asociated value'))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'codeSpace'), CodeSpacePropertyType, scope=CTD_ANON_4, documentation=u'Provides link to dictionary or rule set to which the value belongs'))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.token, scope=CTD_ANON_4, documentation=u'Value is optional, to enable structure to act in a schema for values provided using other encodings'))
CTD_ANON_4._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_4._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel_4, min_occurs=1, max_occurs=1)
    )
CTD_ANON_4._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'codeSpace')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'constraint')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'quality')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_4._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel_5, min_occurs=1, max_occurs=1)
    )
CTD_ANON_4._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel_2, min_occurs=1, max_occurs=1)



CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'valueList'), tokenList, scope=CTD_ANON_5, documentation=u'List of allowed token values for this component'))
CTD_ANON_5._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueList')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_5._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_5._GroupModel, min_occurs=1, max_occurs=1)



TimeGeometricComplexPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeGeometricComplex'), TimeGeometricComplexType, scope=TimeGeometricComplexPropertyType, documentation=u'Explicit implementation of ISO 19108 TM_GeometricComplex - a self-consistent set of TimeInstants and TimePeriods'))
TimeGeometricComplexPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGeometricComplexPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeGeometricComplex')), min_occurs=1, max_occurs=1)
    )
TimeGeometricComplexPropertyType._ContentModel = pyxb.binding.content.ParticleModel(TimeGeometricComplexPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



NormalizedCurveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'outputBias'), QuantityPropertyType, scope=NormalizedCurveType))

NormalizedCurveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'function'), CurvePropertyType, scope=NormalizedCurveType))

NormalizedCurveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'interpolationMethod'), CategoryPropertyType, scope=NormalizedCurveType))

NormalizedCurveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'inputBias'), QuantityPropertyType, scope=NormalizedCurveType))

NormalizedCurveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'inputGain'), QuantityPropertyType, scope=NormalizedCurveType))

NormalizedCurveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'outputGain'), QuantityPropertyType, scope=NormalizedCurveType))

NormalizedCurveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'extrapolationMethod'), CategoryPropertyType, scope=NormalizedCurveType))
NormalizedCurveType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NormalizedCurveType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(NormalizedCurveType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(NormalizedCurveType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
NormalizedCurveType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NormalizedCurveType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
NormalizedCurveType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NormalizedCurveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'inputGain')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(NormalizedCurveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'inputBias')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(NormalizedCurveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'outputGain')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(NormalizedCurveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'outputBias')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(NormalizedCurveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'interpolationMethod')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(NormalizedCurveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'extrapolationMethod')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(NormalizedCurveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'function')), min_occurs=1, max_occurs=1)
    )
NormalizedCurveType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(NormalizedCurveType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(NormalizedCurveType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
NormalizedCurveType._ContentModel = pyxb.binding.content.ParticleModel(NormalizedCurveType._GroupModel_2, min_occurs=1, max_occurs=1)



QuantityPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), CTD_ANON_12, scope=QuantityPropertyType, documentation=u'Decimal number with optional unit and constraints'))
QuantityPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(QuantityPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Quantity')), min_occurs=1, max_occurs=1)
    )
QuantityPropertyType._ContentModel = pyxb.binding.content.ParticleModel(QuantityPropertyType._GroupModel, min_occurs=1, max_occurs=1)



VectorOrSquareMatrixPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Vector'), VectorType, scope=VectorOrSquareMatrixPropertyType, documentation=u'A Vector is a special type of DataRecord that takes a list of numerical scalars called coordinates. The Vector has a referenceFrame in which the coordinates are expressed'))

VectorOrSquareMatrixPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SquareMatrix'), SquareMatrixType, scope=VectorOrSquareMatrixPropertyType, documentation=u'This is a square matrix (so the size is the square of one dimension) which is a DataArray of Quantities. \t\tIt has a referenceFrame in which the matrix components are described'))
VectorOrSquareMatrixPropertyType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(VectorOrSquareMatrixPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Vector')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(VectorOrSquareMatrixPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SquareMatrix')), min_occurs=1, max_occurs=1)
    )
VectorOrSquareMatrixPropertyType._ContentModel = pyxb.binding.content.ParticleModel(VectorOrSquareMatrixPropertyType._GroupModel, min_occurs=1, max_occurs=1)



TypedValuePropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TypedValue'), TypedValueType, scope=TypedValuePropertyType, documentation=u'A generic soft-typed value'))
TypedValuePropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TypedValuePropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TypedValue')), min_occurs=1, max_occurs=1)
    )
TypedValuePropertyType._ContentModel = pyxb.binding.content.ParticleModel(TypedValuePropertyType._GroupModel, min_occurs=1, max_occurs=1)



CurvePropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Curve'), CurveType, scope=CurvePropertyType, documentation=u'Curve describing variations of a parameter vs. another quantity'))
CurvePropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CurvePropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Curve')), min_occurs=1, max_occurs=1)
    )
CurvePropertyType._ContentModel = pyxb.binding.content.ParticleModel(CurvePropertyType._GroupModel, min_occurs=1, max_occurs=1)



TypedValueListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'property'), ScopedNameType, scope=TypedValueListType, documentation=u'This element attribute indicates the semantics of the typed value. \n\t\t\t\t\tUsually identifies a property or phenomenon definition. '))

TypedValueListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.anyType, scope=TypedValueListType, documentation=u'Implicit xs:anyType'))
TypedValueListType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TypedValueListType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'property')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TypedValueListType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=1, max_occurs=None)
    )
TypedValueListType._ContentModel = pyxb.binding.content.ParticleModel(TypedValueListType._GroupModel, min_occurs=1, max_occurs=1)



TimeAggregateType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'member'), TimeObjectPropertyType, scope=TimeAggregateType))
TimeAggregateType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeAggregateType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(TimeAggregateType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeAggregateType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
TimeAggregateType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeAggregateType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
TimeAggregateType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeAggregateType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'member')), min_occurs=1, max_occurs=None)
    )
TimeAggregateType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeAggregateType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeAggregateType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
TimeAggregateType._ContentModel = pyxb.binding.content.ParticleModel(TimeAggregateType._GroupModel_2, min_occurs=1, max_occurs=1)



CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Component'), CTD_ANON_10, scope=CTD_ANON_7))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Block'), CTD_ANON_21, scope=CTD_ANON_7))
CTD_ANON_7._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Component')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Block')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_7._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_7._GroupModel, min_occurs=1, max_occurs=1)



TimeGeometricComplexType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'primitive'), TimeGeometricPrimitivePropertyType, scope=TimeGeometricComplexType, documentation=u'Reference to an identified time primitive'))
TimeGeometricComplexType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGeometricComplexType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(TimeGeometricComplexType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeGeometricComplexType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
TimeGeometricComplexType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGeometricComplexType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
TimeGeometricComplexType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGeometricComplexType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'primitive')), min_occurs=1, max_occurs=None)
    )
TimeGeometricComplexType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGeometricComplexType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeGeometricComplexType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
TimeGeometricComplexType._ContentModel = pyxb.binding.content.ParticleModel(TimeGeometricComplexType._GroupModel_2, min_occurs=1, max_occurs=1)



CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.string, scope=CTD_ANON_8, documentation=u'Value is optional, to enable structure to act in a schema for values provided using other encodings'))
CTD_ANON_8._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_8._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_8._GroupModel_4, min_occurs=1, max_occurs=1)
    )
CTD_ANON_8._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_8._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_8._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._GroupModel_5, min_occurs=1, max_occurs=1)
    )
CTD_ANON_8._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_8._GroupModel_2, min_occurs=1, max_occurs=1)



CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'constraint'), AllowedTimesPropertyType, scope=CTD_ANON_9, documentation=u'The constraint property defines the permitted values, as a range or enumerated list'))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'quality'), QualityPropertyType, scope=CTD_ANON_9, documentation=u'The quality property provides an indication of the reliability of estimates of the asociated value'))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uom'), UomPropertyType, scope=CTD_ANON_9, documentation=u'Unit of measure'))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), timePositionType, scope=CTD_ANON_9, documentation=u'Value is optional, to enable structure to act in a schema for values provided using other encodings'))
CTD_ANON_9._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_9._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_9._GroupModel_4, min_occurs=1, max_occurs=1)
    )
CTD_ANON_9._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uom')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'constraint')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'quality')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_9._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_9._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._GroupModel_5, min_occurs=1, max_occurs=1)
    )
CTD_ANON_9._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_9._GroupModel_2, min_occurs=1, max_occurs=1)



DataRecordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'field'), DataComponentPropertyType, scope=DataRecordType))
DataRecordType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataRecordType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(DataRecordType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataRecordType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
DataRecordType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataRecordType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
DataRecordType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataRecordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'field')), min_occurs=0L, max_occurs=None)
    )
DataRecordType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataRecordType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataRecordType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
DataRecordType._ContentModel = pyxb.binding.content.ParticleModel(DataRecordType._GroupModel_2, min_occurs=1, max_occurs=1)



XMLDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Item'), pyxb.binding.datatypes.anyType, scope=XMLDataPropertyType, documentation=u'An Item is an item of data of any type'))

XMLDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Record'), RecordType, scope=XMLDataPropertyType, documentation=u'A record is a list of fields'))

XMLDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Array'), ArrayType, scope=XMLDataPropertyType, documentation=u'An array is an indexed set of records of homogeneous type'))
XMLDataPropertyType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(XMLDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Item')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(XMLDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Record')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(XMLDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Array')), min_occurs=1, max_occurs=1)
    )
XMLDataPropertyType._ContentModel = pyxb.binding.content.ParticleModel(XMLDataPropertyType._GroupModel, min_occurs=1, max_occurs=1)



DataArrayPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DataArray'), DataArrayType, scope=DataArrayPropertyType, documentation=u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways'))
DataArrayPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataArrayPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'DataArray')), min_occurs=1, max_occurs=1)
    )
DataArrayPropertyType._ContentModel = pyxb.binding.content.ParticleModel(DataArrayPropertyType._GroupModel, min_occurs=1, max_occurs=1)



ArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'element'), XMLDataPropertyType, scope=ArrayType, documentation=u'An Array/element contains an Item or a Record or an Array'))
ArrayType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'element')), min_occurs=1, max_occurs=None)
    )
ArrayType._ContentModel = pyxb.binding.content.ParticleModel(ArrayType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Count'), CTD_ANON_2, scope=CTD_ANON_11, documentation=u'Integer number used for a counting value'))
CTD_ANON_11._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Count')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_11._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_11._GroupModel, min_occurs=0L, max_occurs=1)



TimeGridType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'origin'), pyxb.bundles.opengis.gml.TimeInstantPropertyType, scope=TimeGridType, documentation=u'Reference to an identified time instant'))

TimeGridType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'duration'), pyxb.binding.datatypes.duration, scope=TimeGridType))

TimeGridType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'offsetDuration'), pyxb.binding.datatypes.duration, scope=TimeGridType, documentation=u'XML Schema built-in simple type for duration: e.g. \n                P1Y (1 year) \n                P1M (1 month) \n                P1DT12H (1 day 12 hours) \n                PT5M (5 minutes) \n                PT0.007S (7 milliseconds)'))

TimeGridType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'originPos'), pyxb.bundles.opengis.gml.TimePositionType, scope=TimeGridType, documentation=u'Simple-content time position'))

TimeGridType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'offsetInterval'), pyxb.bundles.opengis.gml.TimeIntervalLengthType, scope=TimeGridType, documentation=u'representation of the ISO 11404 model of a time interval length: e.g. \n                value=1, unit="year"  \n                value=1, unit="other:month" (or see next)\n                value=1, unit="year" radix="12" factor="1" (1/12 year)\n                value=1.5, unit="day"  \n                value=36, unit="hour" \n                value=5, unit="minute"  \n                value=7, unit="second" radix="10" factor="3" (7 milliseconds)'))

TimeGridType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'extent'), TimeGridEnvelopePropertyType, scope=TimeGridType))
TimeGridType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGridType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(TimeGridType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeGridType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
TimeGridType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGridType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
TimeGridType._GroupModel_6 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(TimeGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'originPos')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'origin')), min_occurs=1, max_occurs=1)
    )
TimeGridType._GroupModel_7 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(TimeGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offsetDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offsetInterval')), min_occurs=1, max_occurs=1)
    )
TimeGridType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'extent')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeGridType._GroupModel_6, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeGridType._GroupModel_7, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'duration')), min_occurs=0L, max_occurs=1)
    )
TimeGridType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGridType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeGridType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
TimeGridType._ContentModel = pyxb.binding.content.ParticleModel(TimeGridType._GroupModel_2, min_occurs=1, max_occurs=1)


TimeInstantGridType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeInstantGridType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(TimeInstantGridType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeInstantGridType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
TimeInstantGridType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeInstantGridType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
TimeInstantGridType._GroupModel_6 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(TimeInstantGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'originPos')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeInstantGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'origin')), min_occurs=1, max_occurs=1)
    )
TimeInstantGridType._GroupModel_7 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(TimeInstantGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offsetDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeInstantGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offsetInterval')), min_occurs=1, max_occurs=1)
    )
TimeInstantGridType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeInstantGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'extent')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeInstantGridType._GroupModel_6, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeInstantGridType._GroupModel_7, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeInstantGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'duration')), min_occurs=0L, max_occurs=1)
    )
TimeInstantGridType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeInstantGridType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeInstantGridType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
TimeInstantGridType._ContentModel = pyxb.binding.content.ParticleModel(TimeInstantGridType._GroupModel_2, min_occurs=1, max_occurs=1)



ArrayPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Array'), ArrayType, scope=ArrayPropertyType, documentation=u'An array is an indexed set of records of homogeneous type'))
ArrayPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ArrayPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Array')), min_occurs=1, max_occurs=1)
    )
ArrayPropertyType._ContentModel = pyxb.binding.content.ParticleModel(ArrayPropertyType._GroupModel, min_occurs=1, max_occurs=1)



DataComponentPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), CTD_ANON_12, scope=DataComponentPropertyType, documentation=u'Decimal number with optional unit and constraints'))

DataComponentPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Time'), CTD_ANON_9, scope=DataComponentPropertyType, documentation=u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin'))

DataComponentPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), CTD_ANON_15, scope=DataComponentPropertyType, documentation=u'Decimal pair for specifying a quantity range with constraints'))

DataComponentPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord'), AbstractDataRecordType, abstract=pyxb.binding.datatypes.boolean(1), scope=DataComponentPropertyType))

DataComponentPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Text'), CTD_ANON_8, scope=DataComponentPropertyType, documentation=u'Free textual component'))

DataComponentPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CountRange'), CTD_ANON_16, scope=DataComponentPropertyType, documentation=u'Integer pair used for specifying a count range'))

DataComponentPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), CTD_ANON, scope=DataComponentPropertyType, documentation=u'Scalar component used to express truth: True or False, 0 or 1'))

DataComponentPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray'), AbstractDataArrayType, abstract=pyxb.binding.datatypes.boolean(1), scope=DataComponentPropertyType, documentation=u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways'))

DataComponentPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Count'), CTD_ANON_2, scope=DataComponentPropertyType, documentation=u'Integer number used for a counting value'))

DataComponentPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeRange'), CTD_ANON_19, scope=DataComponentPropertyType, documentation=u'Time value pair for specifying a time range (can be a decimal or ISO 8601)'))

DataComponentPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Category'), CTD_ANON_4, scope=DataComponentPropertyType, documentation=u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value'))
DataComponentPropertyType._GroupModel_2 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Count')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Quantity')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Time')), min_occurs=1, max_occurs=1)
    )
DataComponentPropertyType._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Boolean')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Category')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Text')), min_occurs=1, max_occurs=1)
    )
DataComponentPropertyType._GroupModel_3 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'CountRange')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeRange')), min_occurs=1, max_occurs=1)
    )
DataComponentPropertyType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataComponentPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray')), min_occurs=1, max_occurs=1)
    )
DataComponentPropertyType._ContentModel = pyxb.binding.content.ParticleModel(DataComponentPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



QualityPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), CTD_ANON_12, scope=QualityPropertyType, documentation=u'Decimal number with optional unit and constraints'))

QualityPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), CTD_ANON_15, scope=QualityPropertyType, documentation=u'Decimal pair for specifying a quantity range with constraints'))

QualityPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Text'), CTD_ANON_8, scope=QualityPropertyType, documentation=u'Free textual component'))

QualityPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Category'), CTD_ANON_4, scope=QualityPropertyType, documentation=u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value'))
QualityPropertyType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(QualityPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Quantity')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(QualityPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(QualityPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Category')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(QualityPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Text')), min_occurs=1, max_occurs=1)
    )
QualityPropertyType._ContentModel = pyxb.binding.content.ParticleModel(QualityPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



IntervalType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'upperBound'), pyxb.binding.datatypes.anyType, scope=IntervalType, documentation=u'Implicit xs:anyType'))

IntervalType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lowerBound'), pyxb.binding.datatypes.anyType, scope=IntervalType, documentation=u'Implicit xs:anyType'))
IntervalType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(IntervalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lowerBound')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(IntervalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'upperBound')), min_occurs=1, max_occurs=1)
    )
IntervalType._ContentModel = pyxb.binding.content.ParticleModel(IntervalType._GroupModel, min_occurs=1, max_occurs=1)


DataValuePropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), min_occurs=0, max_occurs=None)
    )
DataValuePropertyType._ContentModel = pyxb.binding.content.ParticleModel(DataValuePropertyType._GroupModel, min_occurs=1, max_occurs=1)



TextPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Text'), CTD_ANON_8, scope=TextPropertyType, documentation=u'Free textual component'))
TextPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TextPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Text')), min_occurs=1, max_occurs=1)
    )
TextPropertyType._ContentModel = pyxb.binding.content.ParticleModel(TextPropertyType._GroupModel, min_occurs=1, max_occurs=1)



BlockEncodingPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TextBlock'), CTD_ANON_18, scope=BlockEncodingPropertyType))

BlockEncodingPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'XMLBlock'), XMLBlockType, scope=BlockEncodingPropertyType, documentation=u'Carries the designator for an element implementing an XML-encoded data-type'))

BlockEncodingPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'StandardFormat'), CTD_ANON_6, scope=BlockEncodingPropertyType))

BlockEncodingPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BinaryBlock'), CTD_ANON_14, scope=BlockEncodingPropertyType))
BlockEncodingPropertyType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(BlockEncodingPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'StandardFormat')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(BlockEncodingPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'BinaryBlock')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(BlockEncodingPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TextBlock')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(BlockEncodingPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'XMLBlock')), min_occurs=1, max_occurs=1)
    )
BlockEncodingPropertyType._ContentModel = pyxb.binding.content.ParticleModel(BlockEncodingPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



SimpleDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord'), AbstractDataRecordType, abstract=pyxb.binding.datatypes.boolean(1), scope=SimpleDataPropertyType))

SimpleDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CountRange'), CTD_ANON_16, scope=SimpleDataPropertyType, documentation=u'Integer pair used for specifying a count range'))

SimpleDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Count'), CTD_ANON_2, scope=SimpleDataPropertyType, documentation=u'Integer number used for a counting value'))

SimpleDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Category'), CTD_ANON_4, scope=SimpleDataPropertyType, documentation=u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value'))

SimpleDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray'), AbstractDataArrayType, abstract=pyxb.binding.datatypes.boolean(1), scope=SimpleDataPropertyType, documentation=u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways'))

SimpleDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeRange'), CTD_ANON_19, scope=SimpleDataPropertyType, documentation=u'Time value pair for specifying a time range (can be a decimal or ISO 8601)'))

SimpleDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Time'), CTD_ANON_9, scope=SimpleDataPropertyType, documentation=u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin'))

SimpleDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), CTD_ANON_12, scope=SimpleDataPropertyType, documentation=u'Decimal number with optional unit and constraints'))

SimpleDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), CTD_ANON_15, scope=SimpleDataPropertyType, documentation=u'Decimal pair for specifying a quantity range with constraints'))

SimpleDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Text'), CTD_ANON_8, scope=SimpleDataPropertyType, documentation=u'Free textual component'))

SimpleDataPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), CTD_ANON, scope=SimpleDataPropertyType, documentation=u'Scalar component used to express truth: True or False, 0 or 1'))
SimpleDataPropertyType._GroupModel_2 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Count')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Quantity')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Time')), min_occurs=1, max_occurs=1)
    )
SimpleDataPropertyType._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Boolean')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Category')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Text')), min_occurs=1, max_occurs=1)
    )
SimpleDataPropertyType._GroupModel_3 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'CountRange')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeRange')), min_occurs=1, max_occurs=1)
    )
SimpleDataPropertyType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SimpleDataPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray')), min_occurs=1, max_occurs=1)
    )
SimpleDataPropertyType._ContentModel = pyxb.binding.content.ParticleModel(SimpleDataPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



UomPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'UnitDefinition'), pyxb.bundles.opengis.gml.UnitDefinitionType, scope=UomPropertyType))
UomPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(UomPropertyType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'UnitDefinition')), min_occurs=1, max_occurs=1)
    )
UomPropertyType._ContentModel = pyxb.binding.content.ParticleModel(UomPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'quality'), QualityPropertyType, scope=CTD_ANON_12, documentation=u'The quality property provides an indication of the reliability of estimates of the asociated value'))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uom'), UomPropertyType, scope=CTD_ANON_12, documentation=u'Unit of measure'))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.double, scope=CTD_ANON_12, documentation=u'Value is optional, to enable structure to act in a schema for values provided using other encodings'))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'constraint'), AllowedValuesPropertyType, scope=CTD_ANON_12, documentation=u'The constraint property defines the permitted values, as a range or enumerated list'))
CTD_ANON_12._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_12._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_12._GroupModel_4, min_occurs=1, max_occurs=1)
    )
CTD_ANON_12._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uom')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'constraint')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'quality')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_12._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_12._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._GroupModel_5, min_occurs=1, max_occurs=1)
    )
CTD_ANON_12._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_12._GroupModel_2, min_occurs=1, max_occurs=1)



CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'max'), pyxb.binding.datatypes.double, scope=CTD_ANON_13, documentation=u'Specifies maximum allowed value for an open interval (no min)'))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'interval'), decimalPair, scope=CTD_ANON_13, documentation=u'Range of allowed values (closed interval) for this component'))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'min'), pyxb.binding.datatypes.double, scope=CTD_ANON_13, documentation=u'Specifies minimum allowed value for an open interval (no max)'))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'valueList'), decimalList, scope=CTD_ANON_13, documentation=u'List of allowed values for this component'))
CTD_ANON_13._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'min')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'max')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_13._GroupModel_2 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'interval')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueList')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_13._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_13._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._GroupModel_2, min_occurs=1, max_occurs=None)
    )
CTD_ANON_13._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_13._GroupModel, min_occurs=1, max_occurs=1)



AbstractDataArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'elementCount'), CTD_ANON_11, scope=AbstractDataArrayType, documentation=u'Specifies the size of the array (i.e. the number of elements of the defined type it contains)'))
AbstractDataArrayType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractDataArrayType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AbstractDataArrayType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AbstractDataArrayType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
AbstractDataArrayType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractDataArrayType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
AbstractDataArrayType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractDataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'elementCount')), min_occurs=1, max_occurs=1)
    )
AbstractDataArrayType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractDataArrayType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AbstractDataArrayType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
AbstractDataArrayType._ContentModel = pyxb.binding.content.ParticleModel(AbstractDataArrayType._GroupModel_2, min_occurs=1, max_occurs=1)



DataArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'encoding'), BlockEncodingPropertyType, scope=DataArrayType, documentation=u'Specifies an encoding for the data structure defined by the enclosing element'))

DataArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'elementType'), DataComponentPropertyType, scope=DataArrayType))

DataArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'values'), DataValuePropertyType, scope=DataArrayType, documentation=u'Carries the block of values encoded as specified by the encoding element'))
DataArrayType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
DataArrayType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataArrayType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
DataArrayType._GroupModel_6 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'elementCount')), min_occurs=1, max_occurs=1)
    )
DataArrayType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataArrayType._GroupModel_4, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataArrayType._GroupModel_6, min_occurs=1, max_occurs=1)
    )
DataArrayType._GroupModel_8 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'encoding')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=1, max_occurs=1)
    )
DataArrayType._GroupModel_7 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'elementType')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataArrayType._GroupModel_8, min_occurs=0L, max_occurs=1)
    )
DataArrayType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataArrayType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataArrayType._GroupModel_7, min_occurs=1, max_occurs=1)
    )
DataArrayType._ContentModel = pyxb.binding.content.ParticleModel(DataArrayType._GroupModel_2, min_occurs=1, max_occurs=1)



TimeIntervalGridType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'windowInterval'), pyxb.bundles.opengis.gml.TimeIntervalLengthType, scope=TimeIntervalGridType, documentation=u'representation of the ISO 11404 model of a time interval length'))

TimeIntervalGridType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'windowDuration'), pyxb.binding.datatypes.duration, scope=TimeIntervalGridType, documentation=u'XML Schema built-in simple type for duration'))
TimeIntervalGridType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
TimeIntervalGridType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
TimeIntervalGridType._GroupModel_7 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'originPos')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'origin')), min_occurs=1, max_occurs=1)
    )
TimeIntervalGridType._GroupModel_8 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offsetDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offsetInterval')), min_occurs=1, max_occurs=1)
    )
TimeIntervalGridType._GroupModel_6 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'extent')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._GroupModel_7, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._GroupModel_8, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'duration')), min_occurs=0L, max_occurs=1)
    )
TimeIntervalGridType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._GroupModel_4, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._GroupModel_6, min_occurs=1, max_occurs=1)
    )
TimeIntervalGridType._GroupModel_10 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'windowDuration')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'windowInterval')), min_occurs=1, max_occurs=1)
    )
TimeIntervalGridType._GroupModel_9 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._GroupModel_10, min_occurs=1, max_occurs=1)
    )
TimeIntervalGridType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeIntervalGridType._GroupModel_9, min_occurs=1, max_occurs=1)
    )
TimeIntervalGridType._ContentModel = pyxb.binding.content.ParticleModel(TimeIntervalGridType._GroupModel_2, min_occurs=1, max_occurs=1)


PhenomenonType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(PhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(PhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=1, max_occurs=None)
    )
PhenomenonType._ContentModel = pyxb.binding.content.ParticleModel(PhenomenonType._GroupModel_, min_occurs=1, max_occurs=1)


CompoundPhenomenonType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CompoundPhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CompoundPhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CompoundPhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=1, max_occurs=None)
    )
CompoundPhenomenonType._ContentModel = pyxb.binding.content.ParticleModel(CompoundPhenomenonType._GroupModel_, min_occurs=1, max_occurs=1)



CompositePhenomenonType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'component'), PhenomenonPropertyType, scope=CompositePhenomenonType))

CompositePhenomenonType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'base'), PhenomenonPropertyType, scope=CompositePhenomenonType, documentation=u'Optional phenomenon that forms the basis for generating more specialized composite Phenomenon by adding more components'))
CompositePhenomenonType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CompositePhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CompositePhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CompositePhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=1, max_occurs=None)
    )
CompositePhenomenonType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CompositePhenomenonType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'base')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CompositePhenomenonType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'component')), min_occurs=1, max_occurs=None)
    )
CompositePhenomenonType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CompositePhenomenonType._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CompositePhenomenonType._GroupModel_3, min_occurs=1, max_occurs=1)
    )
CompositePhenomenonType._ContentModel = pyxb.binding.content.ParticleModel(CompositePhenomenonType._GroupModel_, min_occurs=1, max_occurs=1)



CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'member'), CTD_ANON_7, scope=CTD_ANON_14))
CTD_ANON_14._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'member')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_14._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_14._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uom'), UomPropertyType, scope=CTD_ANON_15, documentation=u'Unit of measure'))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), decimalPair, scope=CTD_ANON_15, documentation=u'Value is optional, to enable structure to act in a schema for values provided using other encodings'))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'constraint'), AllowedValuesPropertyType, scope=CTD_ANON_15, documentation=u'The constraint property defines the permitted values, as a range or enumerated list'))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'quality'), QualityPropertyType, scope=CTD_ANON_15, documentation=u'The quality property provides an indication of the reliability of estimates of the asociated value'))
CTD_ANON_15._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_15._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_15._GroupModel_4, min_occurs=1, max_occurs=1)
    )
CTD_ANON_15._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uom')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'constraint')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'quality')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_15._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_15._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._GroupModel_5, min_occurs=1, max_occurs=1)
    )
CTD_ANON_15._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_15._GroupModel_2, min_occurs=1, max_occurs=1)



VectorPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Vector'), VectorType, scope=VectorPropertyType, documentation=u'A Vector is a special type of DataRecord that takes a list of numerical scalars called coordinates. The Vector has a referenceFrame in which the coordinates are expressed'))
VectorPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(VectorPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Vector')), min_occurs=1, max_occurs=1)
    )
VectorPropertyType._ContentModel = pyxb.binding.content.ParticleModel(VectorPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



DataRecordPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DataRecord'), DataRecordType, scope=DataRecordPropertyType, documentation=u'Implementation of ISO-11404 Record datatype. This allows grouping of data components which can themselves be Records, Arrays or Simple Types'))
DataRecordPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataRecordPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'DataRecord')), min_occurs=1, max_occurs=1)
    )
DataRecordPropertyType._ContentModel = pyxb.binding.content.ParticleModel(DataRecordPropertyType._GroupModel, min_occurs=1, max_occurs=1)



RecordPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Record'), RecordType, scope=RecordPropertyType, documentation=u'A record is a list of fields'))
RecordPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(RecordPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Record')), min_occurs=1, max_occurs=1)
    )
RecordPropertyType._ContentModel = pyxb.binding.content.ParticleModel(RecordPropertyType._GroupModel, min_occurs=1, max_occurs=1)



TypedValueListPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TypedValueList'), TypedValueListType, scope=TypedValueListPropertyType, documentation=u'A generic soft-typed list of values'))
TypedValueListPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TypedValueListPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TypedValueList')), min_occurs=1, max_occurs=1)
    )
TypedValueListPropertyType._ContentModel = pyxb.binding.content.ParticleModel(TypedValueListPropertyType._GroupModel, min_occurs=1, max_occurs=1)



PhenomenonSeriesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'otherConstraint'), pyxb.binding.datatypes.string, scope=PhenomenonSeriesType, documentation=u'Other constraints are described in text'))

PhenomenonSeriesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'base'), PhenomenonPropertyType, scope=PhenomenonSeriesType, documentation=u'Phenomenon that forms the basis for generating a set of more refined Phenomena; e.g. Chemical Composition, Radiance'))

PhenomenonSeriesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'constraintList'), TypedValueListPropertyType, scope=PhenomenonSeriesType, documentation=u'A set of values of some secondary property that constraints the basePhenomenon to generate a Phenomenon set.  \n\t\t\t\t\t\t\tIf more than one set of constraints are possible, then these are applied simultaneously to generate'))
PhenomenonSeriesType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PhenomenonSeriesType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(PhenomenonSeriesType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(PhenomenonSeriesType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=1, max_occurs=None)
    )
PhenomenonSeriesType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PhenomenonSeriesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'base')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PhenomenonSeriesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'constraintList')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(PhenomenonSeriesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'otherConstraint')), min_occurs=0L, max_occurs=None)
    )
PhenomenonSeriesType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PhenomenonSeriesType._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PhenomenonSeriesType._GroupModel_3, min_occurs=1, max_occurs=1)
    )
PhenomenonSeriesType._ContentModel = pyxb.binding.content.ParticleModel(PhenomenonSeriesType._GroupModel_, min_occurs=1, max_occurs=1)



CategoryPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Category'), CTD_ANON_4, scope=CategoryPropertyType, documentation=u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value'))
CategoryPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CategoryPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Category')), min_occurs=1, max_occurs=1)
    )
CategoryPropertyType._ContentModel = pyxb.binding.content.ParticleModel(CategoryPropertyType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), countPair, scope=CTD_ANON_16, documentation=u'Value is optional, to enable structure to act in a schema for values provided using other encodings'))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'quality'), QualityPropertyType, scope=CTD_ANON_16, documentation=u'The quality property provides an indication of the reliability of estimates of the asociated value'))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'constraint'), AllowedValuesPropertyType, scope=CTD_ANON_16, documentation=u'The constraint property defines the permitted values, as a range or enumerated list'))
CTD_ANON_16._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_16._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_16._GroupModel_4, min_occurs=1, max_occurs=1)
    )
CTD_ANON_16._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'constraint')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'quality')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_16._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_16._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._GroupModel_5, min_occurs=1, max_occurs=1)
    )
CTD_ANON_16._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_16._GroupModel_2, min_occurs=1, max_occurs=1)



QuantityRangePropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), CTD_ANON_15, scope=QuantityRangePropertyType, documentation=u'Decimal pair for specifying a quantity range with constraints'))
QuantityRangePropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(QuantityRangePropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange')), min_occurs=1, max_occurs=1)
    )
QuantityRangePropertyType._ContentModel = pyxb.binding.content.ParticleModel(QuantityRangePropertyType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'interval'), timePair, scope=CTD_ANON_17, documentation=u'Range of allowed time values (closed interval) for this component'))

CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'max'), timePositionType, scope=CTD_ANON_17, documentation=u'Specifies maximum allowed time value for an open interval (no min)'))

CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'min'), timePositionType, scope=CTD_ANON_17, documentation=u'Specifies minimum allowed time value for an open interval (no max)'))

CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'valueList'), timeList, scope=CTD_ANON_17, documentation=u'List of allowed time values for this component'))
CTD_ANON_17._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'min')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'max')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_17._GroupModel_2 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'interval')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueList')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_17._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_17._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_17._GroupModel_2, min_occurs=1, max_occurs=None)
    )
CTD_ANON_17._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_17._GroupModel, min_occurs=1, max_occurs=1)



AllowedValuesPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AllowedValues'), CTD_ANON_13, scope=AllowedValuesPropertyType, documentation=u'List of allowed values (There is an implicit AND between all members)'))
AllowedValuesPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AllowedValuesPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AllowedValues')), min_occurs=1, max_occurs=1)
    )
AllowedValuesPropertyType._ContentModel = pyxb.binding.content.ParticleModel(AllowedValuesPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



TimeGeometricPrimitivePropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_TimeGeometricPrimitive'), pyxb.bundles.opengis.gml.AbstractTimeGeometricPrimitiveType, abstract=pyxb.binding.datatypes.boolean(1), scope=TimeGeometricPrimitivePropertyType, documentation=u'This abstract element acts as the head of the substitution group for temporal geometric primitives.'))
TimeGeometricPrimitivePropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGeometricPrimitivePropertyType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_TimeGeometricPrimitive')), min_occurs=1, max_occurs=1)
    )
TimeGeometricPrimitivePropertyType._ContentModel = pyxb.binding.content.ParticleModel(TimeGeometricPrimitivePropertyType._GroupModel, min_occurs=0L, max_occurs=1)


AbstractMatrixType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractMatrixType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AbstractMatrixType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AbstractMatrixType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
AbstractMatrixType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractMatrixType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
AbstractMatrixType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractMatrixType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'elementCount')), min_occurs=1, max_occurs=1)
    )
AbstractMatrixType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractMatrixType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AbstractMatrixType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
AbstractMatrixType._ContentModel = pyxb.binding.content.ParticleModel(AbstractMatrixType._GroupModel_2, min_occurs=1, max_occurs=1)



SquareMatrixType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'elementType'), QuantityPropertyType, scope=SquareMatrixType))

SquareMatrixType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'values'), DataValuePropertyType, scope=SquareMatrixType, documentation=u'Carries the block of values encoded as specified by the encoding element'))

SquareMatrixType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'encoding'), BlockEncodingPropertyType, scope=SquareMatrixType, documentation=u'Specifies an encoding for the data structure defined by the enclosing element'))
SquareMatrixType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SquareMatrixType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(SquareMatrixType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SquareMatrixType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
SquareMatrixType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SquareMatrixType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
SquareMatrixType._GroupModel_6 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SquareMatrixType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'elementCount')), min_occurs=1, max_occurs=1)
    )
SquareMatrixType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SquareMatrixType._GroupModel_4, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SquareMatrixType._GroupModel_6, min_occurs=1, max_occurs=1)
    )
SquareMatrixType._GroupModel_8 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SquareMatrixType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'encoding')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SquareMatrixType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=1, max_occurs=1)
    )
SquareMatrixType._GroupModel_7 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SquareMatrixType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'elementType')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SquareMatrixType._GroupModel_8, min_occurs=0L, max_occurs=1)
    )
SquareMatrixType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SquareMatrixType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(SquareMatrixType._GroupModel_7, min_occurs=1, max_occurs=1)
    )
SquareMatrixType._ContentModel = pyxb.binding.content.ParticleModel(SquareMatrixType._GroupModel_2, min_occurs=1, max_occurs=1)



CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'quality'), QualityPropertyType, scope=CTD_ANON_19, documentation=u'The quality property provides an indication of the reliability of estimates of the asociated value'))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uom'), UomPropertyType, scope=CTD_ANON_19, documentation=u'Unit of measure'))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), timePair, scope=CTD_ANON_19, documentation=u'Value is optional, to enable structure to act in a schema for values provided using other encodings'))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'constraint'), AllowedTimesPropertyType, scope=CTD_ANON_19, documentation=u'The constraint property defines the permitted values, as a range or enumerated list'))
CTD_ANON_19._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_19._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_19._GroupModel_4, min_occurs=1, max_occurs=1)
    )
CTD_ANON_19._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uom')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'constraint')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'quality')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_19._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_19._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._GroupModel_5, min_occurs=1, max_occurs=1)
    )
CTD_ANON_19._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_19._GroupModel_2, min_occurs=1, max_occurs=1)



DataStreamDefinitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'streamEncoding'), MultiplexedStreamFormatPropertyType, scope=DataStreamDefinitionType))

DataStreamDefinitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'streamComponent'), DataBlockDefinitionPropertyType, scope=DataStreamDefinitionType))
DataStreamDefinitionType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataStreamDefinitionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'streamComponent')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(DataStreamDefinitionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'streamEncoding')), min_occurs=1, max_occurs=1)
    )
DataStreamDefinitionType._ContentModel = pyxb.binding.content.ParticleModel(DataStreamDefinitionType._GroupModel, min_occurs=1, max_occurs=1)



DataBlockDefinitionPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DataBlockDefinition'), DataBlockDefinitionType, scope=DataBlockDefinitionPropertyType))
DataBlockDefinitionPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataBlockDefinitionPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'DataBlockDefinition')), min_occurs=1, max_occurs=1)
    )
DataBlockDefinitionPropertyType._ContentModel = pyxb.binding.content.ParticleModel(DataBlockDefinitionPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



ItemPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Item'), pyxb.binding.datatypes.anyType, scope=ItemPropertyType, documentation=u'An Item is an item of data of any type'))
ItemPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ItemPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Item')), min_occurs=1, max_occurs=1)
    )
ItemPropertyType._ContentModel = pyxb.binding.content.ParticleModel(ItemPropertyType._GroupModel, min_occurs=1, max_occurs=1)



PositionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'location'), VectorPropertyType, scope=PositionType))

PositionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'acceleration'), VectorPropertyType, scope=PositionType))

PositionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'orientation'), VectorOrSquareMatrixPropertyType, scope=PositionType))

PositionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'angularAcceleration'), VectorOrSquareMatrixPropertyType, scope=PositionType))

PositionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'velocity'), VectorPropertyType, scope=PositionType))

PositionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'state'), VectorOrSquareMatrixPropertyType, scope=PositionType))

PositionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'time'), TimePropertyType, scope=PositionType))

PositionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'angularVelocity'), VectorOrSquareMatrixPropertyType, scope=PositionType))
PositionType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PositionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(PositionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(PositionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
PositionType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PositionType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
PositionType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PositionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'time')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(PositionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'location')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(PositionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'orientation')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(PositionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'velocity')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(PositionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'angularVelocity')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(PositionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'acceleration')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(PositionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'angularAcceleration')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(PositionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'state')), min_occurs=0L, max_occurs=1)
    )
PositionType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PositionType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PositionType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
PositionType._ContentModel = pyxb.binding.content.ParticleModel(PositionType._GroupModel_2, min_occurs=1, max_occurs=1)



ConstrainedPhenomenonType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'base'), PhenomenonPropertyType, scope=ConstrainedPhenomenonType, documentation=u'Property that forms the basis for generating a set of more refined Phenomena; e.g. Chemical Composition, Radiance'))

ConstrainedPhenomenonType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'otherConstraint'), pyxb.binding.datatypes.string, scope=ConstrainedPhenomenonType, documentation=u'Constraints that cannot be expressed as values of an orthogonal/helper phenomenon'))

ConstrainedPhenomenonType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'singleConstraint'), TypedValuePropertyType, scope=ConstrainedPhenomenonType, documentation=u'Constraint expressed as a value or range of an orthogonal/helper phenomenon'))
ConstrainedPhenomenonType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConstrainedPhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ConstrainedPhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ConstrainedPhenomenonType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=1, max_occurs=None)
    )
ConstrainedPhenomenonType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConstrainedPhenomenonType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'base')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ConstrainedPhenomenonType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'otherConstraint')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ConstrainedPhenomenonType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'singleConstraint')), min_occurs=0L, max_occurs=None)
    )
ConstrainedPhenomenonType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConstrainedPhenomenonType._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ConstrainedPhenomenonType._GroupModel_3, min_occurs=1, max_occurs=1)
    )
ConstrainedPhenomenonType._ContentModel = pyxb.binding.content.ParticleModel(ConstrainedPhenomenonType._GroupModel_, min_occurs=1, max_occurs=1)



CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Count'), CTD_ANON_2, scope=CTD_ANON_20, documentation=u'Integer number used for a counting value'))

CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Time'), CTD_ANON_9, scope=CTD_ANON_20, documentation=u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin'))

CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), CTD_ANON_12, scope=CTD_ANON_20, documentation=u'Decimal number with optional unit and constraints'))
CTD_ANON_20._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Count')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Quantity')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Time')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_20._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_20._GroupModel, min_occurs=0L, max_occurs=1)



RecordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'field'), ItemPropertyType, scope=RecordType, documentation=u'A Record/field contains an item of data'))
RecordType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(RecordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'field')), min_occurs=1, max_occurs=None)
    )
RecordType._ContentModel = pyxb.binding.content.ParticleModel(RecordType._GroupModel, min_occurs=1, max_occurs=1)



EnvelopePropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Envelope'), EnvelopeType, scope=EnvelopePropertyType, documentation=u'Envelope described using two vectors specifying lower and upper corner points.\n           This is typically use to define rectangular bounding boxes in any coordinate system.'))
EnvelopePropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(EnvelopePropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Envelope')), min_occurs=1, max_occurs=1)
    )
EnvelopePropertyType._ContentModel = pyxb.binding.content.ParticleModel(EnvelopePropertyType._GroupModel, min_occurs=0L, max_occurs=1)



DataBlockDefinitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'encoding'), BlockEncodingPropertyType, scope=DataBlockDefinitionType))

DataBlockDefinitionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'components'), DataComponentPropertyType, scope=DataBlockDefinitionType))
DataBlockDefinitionType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataBlockDefinitionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'components')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataBlockDefinitionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'encoding')), min_occurs=1, max_occurs=1)
    )
DataBlockDefinitionType._ContentModel = pyxb.binding.content.ParticleModel(DataBlockDefinitionType._GroupModel, min_occurs=1, max_occurs=1)



AllowedTokensPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AllowedTokens'), CTD_ANON_5, scope=AllowedTokensPropertyType, documentation=u'Enumeration of allowed values'))
AllowedTokensPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AllowedTokensPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AllowedTokens')), min_occurs=1, max_occurs=1)
    )
AllowedTokensPropertyType._ContentModel = pyxb.binding.content.ParticleModel(AllowedTokensPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



EnvelopeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'upperCorner'), VectorPropertyType, scope=EnvelopeType))

EnvelopeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'time'), TimeRangePropertyType, scope=EnvelopeType, documentation=u'Optionally provides time range during which this bounding envelope applies'))

EnvelopeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lowerCorner'), VectorPropertyType, scope=EnvelopeType))
EnvelopeType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(EnvelopeType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(EnvelopeType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(EnvelopeType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
EnvelopeType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(EnvelopeType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
EnvelopeType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(EnvelopeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'time')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(EnvelopeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lowerCorner')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(EnvelopeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'upperCorner')), min_occurs=1, max_occurs=1)
    )
EnvelopeType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(EnvelopeType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(EnvelopeType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
EnvelopeType._ContentModel = pyxb.binding.content.ParticleModel(EnvelopeType._GroupModel_2, min_occurs=1, max_occurs=1)



TimePropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Time'), CTD_ANON_9, scope=TimePropertyType, documentation=u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin'))
TimePropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimePropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Time')), min_occurs=1, max_occurs=1)
    )
TimePropertyType._ContentModel = pyxb.binding.content.ParticleModel(TimePropertyType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange'), CTD_ANON_15, scope=CTD_ANON_22, documentation=u'Decimal pair for specifying a quantity range with constraints'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord'), AbstractDataRecordType, abstract=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_22))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Category'), CTD_ANON_4, scope=CTD_ANON_22, documentation=u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Time'), CTD_ANON_9, scope=CTD_ANON_22, documentation=u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CountRange'), CTD_ANON_16, scope=CTD_ANON_22, documentation=u'Integer pair used for specifying a count range'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray'), AbstractDataArrayType, abstract=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_22, documentation=u'Implemetation of ISO-11404 Array datatype. This defines an array of identical data components with a elementCount. Values are given as a block and can be encoded in different ways'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Text'), CTD_ANON_8, scope=CTD_ANON_22, documentation=u'Free textual component'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), CTD_ANON, scope=CTD_ANON_22, documentation=u'Scalar component used to express truth: True or False, 0 or 1'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Count'), CTD_ANON_2, scope=CTD_ANON_22, documentation=u'Integer number used for a counting value'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeRange'), CTD_ANON_19, scope=CTD_ANON_22, documentation=u'Time value pair for specifying a time range (can be a decimal or ISO 8601)'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), CTD_ANON_12, scope=CTD_ANON_22, documentation=u'Decimal number with optional unit and constraints'))
CTD_ANON_22._GroupModel_2 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Count')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Quantity')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Time')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_22._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_22._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Boolean')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Category')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Text')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_22._GroupModel_3 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'QuantityRange')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'CountRange')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeRange')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_22._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_22._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataRecord')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AbstractDataArray')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_22._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_22._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'high'), pyxb.binding.datatypes.integer, scope=CTD_ANON_23))

CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'low'), pyxb.binding.datatypes.integer, scope=CTD_ANON_23))
CTD_ANON_23._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'low')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'high')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_23._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_23._GroupModel, min_occurs=1, max_occurs=1)



AbstractConditionalType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'condition'), CTD_ANON_22, scope=AbstractConditionalType, documentation=u'Specifies one or more conditions for which the given value is valid'))
AbstractConditionalType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractConditionalType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AbstractConditionalType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AbstractConditionalType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
AbstractConditionalType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractConditionalType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
AbstractConditionalType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractConditionalType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'condition')), min_occurs=1, max_occurs=None)
    )
AbstractConditionalType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AbstractConditionalType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AbstractConditionalType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
AbstractConditionalType._ContentModel = pyxb.binding.content.ParticleModel(AbstractConditionalType._GroupModel_2, min_occurs=1, max_occurs=1)



ConditionalValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'data'), CTD_ANON_, scope=ConditionalValueType))
ConditionalValueType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConditionalValueType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ConditionalValueType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ConditionalValueType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
ConditionalValueType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConditionalValueType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
ConditionalValueType._GroupModel_6 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConditionalValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'condition')), min_occurs=1, max_occurs=None)
    )
ConditionalValueType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConditionalValueType._GroupModel_4, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ConditionalValueType._GroupModel_6, min_occurs=1, max_occurs=1)
    )
ConditionalValueType._GroupModel_7 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConditionalValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'data')), min_occurs=1, max_occurs=1)
    )
ConditionalValueType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConditionalValueType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ConditionalValueType._GroupModel_7, min_occurs=1, max_occurs=1)
    )
ConditionalValueType._ContentModel = pyxb.binding.content.ParticleModel(ConditionalValueType._GroupModel_2, min_occurs=1, max_occurs=1)



TimeObjectPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_TimeObject'), pyxb.bundles.opengis.gml.AbstractTimeObjectType, abstract=pyxb.binding.datatypes.boolean(1), scope=TimeObjectPropertyType, documentation=u'This abstract element acts as the head of the substitution group for temporal primitives and complexes.'))
TimeObjectPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeObjectPropertyType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_TimeObject')), min_occurs=1, max_occurs=1)
    )
TimeObjectPropertyType._ContentModel = pyxb.binding.content.ParticleModel(TimeObjectPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



CurveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'encoding'), BlockEncodingPropertyType, scope=CurveType, documentation=u'Specifies an encoding for the data structure defined by the enclosing element'))

CurveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'values'), DataValuePropertyType, scope=CurveType, documentation=u'Carries the block of values encoded as specified by the encoding element'))

CurveType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'elementType'), SimpleDataRecordPropertyType, scope=CurveType))
CurveType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CurveType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CurveType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CurveType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CurveType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CurveType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
CurveType._GroupModel_6 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CurveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'elementCount')), min_occurs=1, max_occurs=1)
    )
CurveType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CurveType._GroupModel_4, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CurveType._GroupModel_6, min_occurs=1, max_occurs=1)
    )
CurveType._GroupModel_8 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CurveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'encoding')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CurveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=1, max_occurs=1)
    )
CurveType._GroupModel_7 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CurveType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'elementType')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CurveType._GroupModel_8, min_occurs=0L, max_occurs=1)
    )
CurveType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CurveType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CurveType._GroupModel_7, min_occurs=1, max_occurs=1)
    )
CurveType._ContentModel = pyxb.binding.content.ParticleModel(CurveType._GroupModel_2, min_occurs=1, max_occurs=1)



AnyScalarPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), CTD_ANON, scope=AnyScalarPropertyType, documentation=u'Scalar component used to express truth: True or False, 0 or 1'))

AnyScalarPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Category'), CTD_ANON_4, scope=AnyScalarPropertyType, documentation=u'A simple token identifying a term or category (single spaces allowed); definition attribute should provide dictionary entry useful for interpretation of the value'))

AnyScalarPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Quantity'), CTD_ANON_12, scope=AnyScalarPropertyType, documentation=u'Decimal number with optional unit and constraints'))

AnyScalarPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Text'), CTD_ANON_8, scope=AnyScalarPropertyType, documentation=u'Free textual component'))

AnyScalarPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Time'), CTD_ANON_9, scope=AnyScalarPropertyType, documentation=u'Either ISO 8601 (e.g. 2004-04-18T12:03:04.6Z) or time relative to a time origin'))

AnyScalarPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Count'), CTD_ANON_2, scope=AnyScalarPropertyType, documentation=u'Integer number used for a counting value'))
AnyScalarPropertyType._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(AnyScalarPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Count')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AnyScalarPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Quantity')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AnyScalarPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Time')), min_occurs=1, max_occurs=1)
    )
AnyScalarPropertyType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(AnyScalarPropertyType._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AnyScalarPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Boolean')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AnyScalarPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Category')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AnyScalarPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Text')), min_occurs=1, max_occurs=1)
    )
AnyScalarPropertyType._ContentModel = pyxb.binding.content.ParticleModel(AnyScalarPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



BooleanPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Boolean'), CTD_ANON, scope=BooleanPropertyType, documentation=u'Scalar component used to express truth: True or False, 0 or 1'))
BooleanPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(BooleanPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Boolean')), min_occurs=1, max_occurs=1)
    )
BooleanPropertyType._ContentModel = pyxb.binding.content.ParticleModel(BooleanPropertyType._GroupModel, min_occurs=1, max_occurs=1)



TimeInstantGridPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeInstantGrid'), TimeInstantGridType, scope=TimeInstantGridPropertyType, documentation=u'A set of uniformly spaced time instants described using an implicit notation'))
TimeInstantGridPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeInstantGridPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeInstantGrid')), min_occurs=1, max_occurs=1)
    )
TimeInstantGridPropertyType._ContentModel = pyxb.binding.content.ParticleModel(TimeInstantGridPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'member'), EnvelopePropertyType, scope=CTD_ANON_24, documentation=u'Is this an aggregate geometry?'))
CTD_ANON_24._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_24._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_24._GroupModel_4, min_occurs=1, max_occurs=1)
    )
CTD_ANON_24._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'member')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_24._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_24._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_24._GroupModel_5, min_occurs=1, max_occurs=1)
    )
CTD_ANON_24._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_24._GroupModel_2, min_occurs=1, max_occurs=1)



CountRangePropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CountRange'), CTD_ANON_16, scope=CountRangePropertyType, documentation=u'Integer pair used for specifying a count range'))
CountRangePropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CountRangePropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'CountRange')), min_occurs=1, max_occurs=1)
    )
CountRangePropertyType._ContentModel = pyxb.binding.content.ParticleModel(CountRangePropertyType._GroupModel, min_occurs=1, max_occurs=1)



ConditionalDataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'case'), CTD_ANON_3, scope=ConditionalDataType))
ConditionalDataType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConditionalDataType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ConditionalDataType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ConditionalDataType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
ConditionalDataType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConditionalDataType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
ConditionalDataType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConditionalDataType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'case')), min_occurs=1, max_occurs=None)
    )
ConditionalDataType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ConditionalDataType._GroupModel_3, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ConditionalDataType._GroupModel_5, min_occurs=1, max_occurs=1)
    )
ConditionalDataType._ContentModel = pyxb.binding.content.ParticleModel(ConditionalDataType._GroupModel_2, min_occurs=1, max_occurs=1)



TypedValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.anyType, scope=TypedValueType, documentation=u'Implicit xs:anyType'))

TypedValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'property'), ScopedNameType, scope=TypedValueType, documentation=u'This element attribute indicates the semantics of the typed value. \n\t\t\t\t\tUsually identifies a property or phenomenon definition. '))
TypedValueType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TypedValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'property')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TypedValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=1, max_occurs=1)
    )
TypedValueType._ContentModel = pyxb.binding.content.ParticleModel(TypedValueType._GroupModel, min_occurs=1, max_occurs=1)



CountPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Count'), CTD_ANON_2, scope=CountPropertyType, documentation=u'Integer number used for a counting value'))
CountPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CountPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Count')), min_occurs=1, max_occurs=1)
    )
CountPropertyType._ContentModel = pyxb.binding.content.ParticleModel(CountPropertyType._GroupModel, min_occurs=1, max_occurs=1)



AllowedTimesPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AllowedTimes'), CTD_ANON_17, scope=AllowedTimesPropertyType, documentation=u'List of allowed time values (There is an implicit AND between all members)'))
AllowedTimesPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AllowedTimesPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AllowedTimes')), min_occurs=1, max_occurs=1)
    )
AllowedTimesPropertyType._ContentModel = pyxb.binding.content.ParticleModel(AllowedTimesPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



SimpleDataRecordPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SimpleDataRecord'), SimpleDataRecordType, scope=SimpleDataRecordPropertyType, documentation=u'Implementation of ISO-11404 Record datatype that takes only simple scalars (i.e. no data aggregates)'))
SimpleDataRecordPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SimpleDataRecordPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SimpleDataRecord')), min_occurs=1, max_occurs=1)
    )
SimpleDataRecordPropertyType._ContentModel = pyxb.binding.content.ParticleModel(SimpleDataRecordPropertyType._GroupModel, min_occurs=1, max_occurs=1)



TimeAggregatePropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeAggregate'), TimeAggregateType, scope=TimeAggregatePropertyType, documentation=u'an arbitrary set of TimeObjects, often TimeInstants and TimePeriods'))
TimeAggregatePropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeAggregatePropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeAggregate')), min_occurs=1, max_occurs=1)
    )
TimeAggregatePropertyType._ContentModel = pyxb.binding.content.ParticleModel(TimeAggregatePropertyType._GroupModel, min_occurs=0L, max_occurs=1)



TimeRangePropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeRange'), CTD_ANON_19, scope=TimeRangePropertyType, documentation=u'Time value pair for specifying a time range (can be a decimal or ISO 8601)'))
TimeRangePropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeRangePropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeRange')), min_occurs=1, max_occurs=1)
    )
TimeRangePropertyType._ContentModel = pyxb.binding.content.ParticleModel(TimeRangePropertyType._GroupModel, min_occurs=1, max_occurs=1)



TimeGridEnvelopePropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeGridEnvelope'), CTD_ANON_23, scope=TimeGridEnvelopePropertyType, documentation=u'Grid extent specified in grid coordinates - i.e. 2 integers'))
TimeGridEnvelopePropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGridEnvelopePropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeGridEnvelope')), min_occurs=1, max_occurs=1)
    )
TimeGridEnvelopePropertyType._ContentModel = pyxb.binding.content.ParticleModel(TimeGridEnvelopePropertyType._GroupModel, min_occurs=1, max_occurs=1)



IntervalPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Interval'), IntervalType, scope=IntervalPropertyType, documentation=u'A generic interval. The type of the two limits will normally be the same.'))
IntervalPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(IntervalPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Interval')), min_occurs=1, max_occurs=1)
    )
IntervalPropertyType._ContentModel = pyxb.binding.content.ParticleModel(IntervalPropertyType._GroupModel, min_occurs=1, max_occurs=1)



TimeIntervalGridPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeIntervalGrid'), TimeIntervalGridType, scope=TimeIntervalGridPropertyType, documentation=u'A set of uniformly spaced time intervals described using an implicit notation'))
TimeIntervalGridPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeIntervalGridPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeIntervalGrid')), min_occurs=1, max_occurs=1)
    )
TimeIntervalGridPropertyType._ContentModel = pyxb.binding.content.ParticleModel(TimeIntervalGridPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



DataStreamDefinitionPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DataStreamDefinition'), DataStreamDefinitionType, scope=DataStreamDefinitionPropertyType))
DataStreamDefinitionPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataStreamDefinitionPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'DataStreamDefinition')), min_occurs=1, max_occurs=1)
    )
DataStreamDefinitionPropertyType._ContentModel = pyxb.binding.content.ParticleModel(DataStreamDefinitionPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



TimeGridPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeInstantGrid'), TimeInstantGridType, scope=TimeGridPropertyType, documentation=u'A set of uniformly spaced time instants described using an implicit notation'))
TimeGridPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimeGridPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeInstantGrid')), min_occurs=1, max_occurs=1)
    )
TimeGridPropertyType._ContentModel = pyxb.binding.content.ParticleModel(TimeGridPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



MultiplexedStreamFormatPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'MultiplexedStreamFormat'), MultiplexedStreamFormatType, scope=MultiplexedStreamFormatPropertyType, documentation=u'Allows specification of the stream/packaging format used (ex: RTP, ASF, AAF, TML...)'))
MultiplexedStreamFormatPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MultiplexedStreamFormatPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'MultiplexedStreamFormat')), min_occurs=0L, max_occurs=1)
    )
MultiplexedStreamFormatPropertyType._ContentModel = pyxb.binding.content.ParticleModel(MultiplexedStreamFormatPropertyType._GroupModel, min_occurs=1, max_occurs=1)


CTD_ANON_25._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_25._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_25._GroupModel_3, min_occurs=1, max_occurs=1)
    )
CTD_ANON_25._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_25._GroupModel_2, min_occurs=1, max_occurs=1)

Vector._setSubstitutionGroup(AbstractDataRecord)

NormalizedCurve._setSubstitutionGroup(AbstractDataRecord)

TimeAggregate._setSubstitutionGroup(pyxb.bundles.opengis.gml.TimeObject)

TimeGeometricComplex._setSubstitutionGroup(pyxb.bundles.opengis.gml.TimeComplex)

DataRecord._setSubstitutionGroup(AbstractDataRecord)

DataArray._setSubstitutionGroup(AbstractDataArray)

CompositePhenomenon._setSubstitutionGroup(CompoundPhenomenon)

PhenomenonSeries._setSubstitutionGroup(CompoundPhenomenon)

TimeInstantGrid._setSubstitutionGroup(TimeGrid)

SquareMatrix._setSubstitutionGroup(AbstractDataArray)

TimeGrid._setSubstitutionGroup(pyxb.bundles.opengis.gml.TimeComplex)

Position._setSubstitutionGroup(AbstractDataRecord)

ConstrainedPhenomenon._setSubstitutionGroup(Phenomenon)

Phenomenon._setSubstitutionGroup(pyxb.bundles.opengis.gml.Definition)

TimeIntervalGrid._setSubstitutionGroup(TimeGrid)

ConditionalValue._setSubstitutionGroup(AbstractDataRecord)

Curve._setSubstitutionGroup(AbstractDataArray)

GeoLocationArea._setSubstitutionGroup(AbstractDataRecord)

ConditionalData._setSubstitutionGroup(AbstractDataRecord)

Envelope._setSubstitutionGroup(AbstractDataRecord)

CompoundPhenomenon._setSubstitutionGroup(Phenomenon)

SimpleDataRecord._setSubstitutionGroup(AbstractDataRecord)
