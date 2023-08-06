# ./pyxb/bundles/opengis/raw/wcs_1_1.py
# PyXB bindings for NM:22a469f3e316cf44da81d828959bab128bf769b5
# Generated 2011-09-09 14:19:15.147682 by PyXB version 1.1.3
# Namespace http://www.opengis.net/wcs/1.1

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9ab77558-db18-11e0-add6-001fbc013adc')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.opengis.ows_1_1
import pyxb.bundles.opengis.gml
import pyxb.bundles.opengis.misc.xlinks

Namespace = pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/wcs/1.1', create_if_missing=True)
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
class IdentifierType (pyxb.binding.datatypes.string):

    """Unambiguous identifier. Although there is no formal restriction on characters included, these identifiers shall be directly usable in GetCoverage operation requests for the specific server, whether those requests are encoded in KVP or XML. Each of these encodings requires that certain characters be avoided, encoded, or escaped (TBR). """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IdentifierType')
    _Documentation = u'Unambiguous identifier. Although there is no formal restriction on characters included, these identifiers shall be directly usable in GetCoverage operation requests for the specific server, whether those requests are encoded in KVP or XML. Each of these encodings requires that certain characters be avoided, encoded, or escaped (TBR). '
IdentifierType._CF_pattern = pyxb.binding.facets.CF_pattern()
IdentifierType._CF_pattern.addPattern(pattern=u'.+')
IdentifierType._InitializeFacetMap(IdentifierType._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'IdentifierType', IdentifierType)

# Atomic SimpleTypeDefinition
class STD_ANON (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON._InitializeFacetMap()

# Union SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class TimeDurationType (pyxb.binding.basis.STD_union):

    """
      Base type for describing temporal length or distance. The value space is further 
      constrained by subtypes that conform to the ISO 8601 or ISO 11404 standards.
      """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeDurationType')
    _Documentation = u'\n      Base type for describing temporal length or distance. The value space is further \n      constrained by subtypes that conform to the ISO 8601 or ISO 11404 standards.\n      '

    _MemberTypes = ( pyxb.binding.datatypes.duration, pyxb.binding.datatypes.decimal, )
TimeDurationType._CF_pattern = pyxb.binding.facets.CF_pattern()
TimeDurationType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=TimeDurationType)
TimeDurationType._InitializeFacetMap(TimeDurationType._CF_pattern,
   TimeDurationType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'TimeDurationType', TimeDurationType)

# Complex type RangeType with content type ELEMENT_ONLY
class RangeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RangeType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}Field uses Python identifier Field
    __Field = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Field'), 'Field', '__httpwww_opengis_netwcs1_1_RangeType_httpwww_opengis_netwcs1_1Field', True)

    
    Field = property(__Field.value, __Field.set, None, u'Unordered list of the Fields in the Range of a coverage. ')


    _ElementMap = {
        __Field.name() : __Field
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'RangeType', RangeType)


# Complex type InterpolationMethodBaseType with content type SIMPLE
class InterpolationMethodBaseType (pyxb.bundles.opengis.ows_1_1.CodeType):
    _TypeDefinition = STD_ANON
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'InterpolationMethodBaseType')
    # Base type is pyxb.bundles.opengis.ows_1_1.CodeType
    
    # Attribute codeSpace is restricted from parent
    
    # Attribute codeSpace uses Python identifier codeSpace
    __codeSpace = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'codeSpace'), 'codeSpace', '__httpwww_opengis_netows1_1_CodeType_codeSpace', pyxb.binding.datatypes.anyURI, unicode_default=u'http://schemas.opengis.net/wcs/1.1.0/interpolationMethods.xml')
    
    codeSpace = property(__codeSpace.value, __codeSpace.set, None, u'Reference to a dictionary that specifies allowed values for interpolation method identifier strings and nullResistance identifier strings. This reference defaults to the standard interpolation methods dictionary specified in WCS 1.1.0. ')


    _ElementMap = pyxb.bundles.opengis.ows_1_1.CodeType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = pyxb.bundles.opengis.ows_1_1.CodeType._AttributeMap.copy()
    _AttributeMap.update({
        __codeSpace.name() : __codeSpace
    })
Namespace.addCategoryObject('typeBinding', u'InterpolationMethodBaseType', InterpolationMethodBaseType)


# Complex type InterpolationMethodType with content type SIMPLE
class InterpolationMethodType (InterpolationMethodBaseType):
    _TypeDefinition = STD_ANON
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'InterpolationMethodType')
    # Base type is InterpolationMethodBaseType
    
    # Attribute codeSpace_ inherited from {http://www.opengis.net/wcs/1.1}InterpolationMethodBaseType
    
    # Attribute nullResistance uses Python identifier nullResistance
    __nullResistance = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'nullResistance'), 'nullResistance', '__httpwww_opengis_netwcs1_1_InterpolationMethodType_nullResistance', pyxb.binding.datatypes.string)
    
    nullResistance = property(__nullResistance.value, __nullResistance.set, None, u'Identifier of how the server handles null values when spatially interpolating values in this field using this interpolation method. This identifier shall be selected from the referenced dictionary. This parameter shall be omitted when the rule for handling nulls is unknown. ')


    _ElementMap = InterpolationMethodBaseType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = InterpolationMethodBaseType._AttributeMap.copy()
    _AttributeMap.update({
        __nullResistance.name() : __nullResistance
    })
Namespace.addCategoryObject('typeBinding', u'InterpolationMethodType', InterpolationMethodType)


# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}Key uses Python identifier Key
    __Key = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Key'), 'Key', '__httpwww_opengis_netwcs1_1_CTD_ANON_httpwww_opengis_netwcs1_1Key', True)

    
    Key = property(__Key.value, __Key.set, None, u'Valid key value for this axis. There will normally be more than one key value for an axis, but one is allowed for special circumstances. ')


    _ElementMap = {
        __Key.name() : __Key
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_ with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}InterpolationMethod uses Python identifier InterpolationMethod
    __InterpolationMethod = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'InterpolationMethod'), 'InterpolationMethod', '__httpwww_opengis_netwcs1_1_CTD_ANON__httpwww_opengis_netwcs1_1InterpolationMethod', True)

    
    InterpolationMethod = property(__InterpolationMethod.value, __InterpolationMethod.set, None, u'Unordered list of identifiers of all other supported spatial interpolation methods. ')

    
    # Element {http://www.opengis.net/wcs/1.1}Default uses Python identifier Default
    __Default = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Default'), 'Default', '__httpwww_opengis_netwcs1_1_CTD_ANON__httpwww_opengis_netwcs1_1Default', False)

    
    Default = property(__Default.value, __Default.set, None, u'Identifier of interpolation method that will be used if the client does not specify one. ')


    _ElementMap = {
        __InterpolationMethod.name() : __InterpolationMethod,
        __Default.name() : __Default
    }
    _AttributeMap = {
        
    }



# Complex type SpatialDomainType with content type ELEMENT_ONLY
class SpatialDomainType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SpatialDomainType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/gml}Polygon uses Python identifier Polygon
    __Polygon = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'Polygon'), 'Polygon', '__httpwww_opengis_netwcs1_1_SpatialDomainType_httpwww_opengis_netgmlPolygon', True)

    
    Polygon = property(__Polygon.value, __Polygon.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}ImageCRS uses Python identifier ImageCRS
    __ImageCRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ImageCRS'), 'ImageCRS', '__httpwww_opengis_netwcs1_1_SpatialDomainType_httpwww_opengis_netwcs1_1ImageCRS', False)

    
    ImageCRS = property(__ImageCRS.value, __ImageCRS.set, None, u'Association to ImageCRS of an unrectified offered coverage. The ImageCRS shall be referenced in the SpatialDomain when the offered coverage does not have a known GridCRS. Such a coverage is always unrectified, but an unrectified coverage may have a GridCRS instead of an ImageCRS. This ImageCRS applies to this offered coverage, but does not (normally) specify its spatial resolution. The ImageCRS and the GridCRS shall be mutually exclusive in this SpatialDomain. ')

    
    # Element {http://www.opengis.net/ows/1.1}BoundingBox uses Python identifier BoundingBox
    __BoundingBox = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'BoundingBox'), 'BoundingBox', '__httpwww_opengis_netwcs1_1_SpatialDomainType_httpwww_opengis_netows1_1BoundingBox', True)

    
    BoundingBox = property(__BoundingBox.value, __BoundingBox.set, None, None)

    
    # Element {http://www.opengis.net/gml}_CoordinateOperation uses Python identifier CoordinateOperation
    __CoordinateOperation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_CoordinateOperation'), 'CoordinateOperation', '__httpwww_opengis_netwcs1_1_SpatialDomainType_httpwww_opengis_netgml_CoordinateOperation', False)

    
    CoordinateOperation = property(__CoordinateOperation.value, __CoordinateOperation.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}GridCRS uses Python identifier GridCRS
    __GridCRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'GridCRS'), 'GridCRS', '__httpwww_opengis_netwcs1_1_SpatialDomainType_httpwww_opengis_netwcs1_1GridCRS', False)

    
    GridCRS = property(__GridCRS.value, __GridCRS.set, None, None)


    _ElementMap = {
        __Polygon.name() : __Polygon,
        __ImageCRS.name() : __ImageCRS,
        __BoundingBox.name() : __BoundingBox,
        __CoordinateOperation.name() : __CoordinateOperation,
        __GridCRS.name() : __GridCRS
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SpatialDomainType', SpatialDomainType)


# Complex type CTD_ANON_2 with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}CoverageSummary uses Python identifier CoverageSummary
    __CoverageSummary = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'CoverageSummary'), 'CoverageSummary', '__httpwww_opengis_netwcs1_1_CTD_ANON_2_httpwww_opengis_netwcs1_1CoverageSummary', True)

    
    CoverageSummary = property(__CoverageSummary.value, __CoverageSummary.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}SupportedFormat uses Python identifier SupportedFormat
    __SupportedFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'SupportedFormat'), 'SupportedFormat', '__httpwww_opengis_netwcs1_1_CTD_ANON_2_httpwww_opengis_netwcs1_1SupportedFormat', True)

    
    SupportedFormat = property(__SupportedFormat.value, __SupportedFormat.set, None, u'Unordered list of identifiers of formats in which GetCoverage operation response may be encoded. This list of SupportedFormats shall be the union of all of the supported formats in all of the nested CoverageSummaries. Servers should include this list since it reduces the work clients need to do to determine that they can interoperate with the server. There may be a dependency of SupportedCRS on SupportedFormat, as described in clause 10.3.5. The full list of formats supported by a coverage shall be the union of the CoverageSummary\u2019s own SupportedFormats and those supported by all its ancestor CoverageSummaries. ')

    
    # Element {http://www.opengis.net/wcs/1.1}OtherSource uses Python identifier OtherSource
    __OtherSource = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'OtherSource'), 'OtherSource', '__httpwww_opengis_netwcs1_1_CTD_ANON_2_httpwww_opengis_netwcs1_1OtherSource', True)

    
    OtherSource = property(__OtherSource.value, __OtherSource.set, None, u'Unordered list of references to other sources of coverage metadata. This list shall be included unless one or more CoverageSummaries are included. ')

    
    # Element {http://www.opengis.net/wcs/1.1}SupportedCRS uses Python identifier SupportedCRS
    __SupportedCRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'SupportedCRS'), 'SupportedCRS', '__httpwww_opengis_netwcs1_1_CTD_ANON_2_httpwww_opengis_netwcs1_1SupportedCRS', True)

    
    SupportedCRS = property(__SupportedCRS.value, __SupportedCRS.set, None, u'Unordered list of references to GridBaseCRSs in which GetCoverage operation requests and responses may be expressed. This list of SupportedCRSs shall be the union of all of the supported CRSs in all of the nested CoverageSummaries. Servers should include this list since it reduces the work clients need to do to determine that they can interoperate with the server. There may be a dependency of SupportedCRS on SupportedFormat, as described in Subclause 10.3.5. The full list of GridBaseCRSs supported by a coverage shall be the union of the CoverageSummary\u2019s own SupportedCRSs and those supported by all its ancestor CoverageSummaries. This full list shall be an exact copy of the equivalent parameters in the CoverageDescription, and shall include zero or more SupportedCRS elements. ')


    _ElementMap = {
        __CoverageSummary.name() : __CoverageSummary,
        __SupportedFormat.name() : __SupportedFormat,
        __OtherSource.name() : __OtherSource,
        __SupportedCRS.name() : __SupportedCRS
    }
    _AttributeMap = {
        
    }



# Complex type CoverageSummaryType with content type ELEMENT_ONLY
class CoverageSummaryType (pyxb.bundles.opengis.ows_1_1.DescriptionType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CoverageSummaryType')
    # Base type is pyxb.bundles.opengis.ows_1_1.DescriptionType
    
    # Element {http://www.opengis.net/wcs/1.1}SupportedFormat uses Python identifier SupportedFormat
    __SupportedFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'SupportedFormat'), 'SupportedFormat', '__httpwww_opengis_netwcs1_1_CoverageSummaryType_httpwww_opengis_netwcs1_1SupportedFormat', True)

    
    SupportedFormat = property(__SupportedFormat.value, __SupportedFormat.set, None, u'Unordered list of identifiers of formats in which GetCoverage operation responses may be encoded. These formats shall also apply to all lower-level CoverageSummaries under this CoverageSummary, in addition to any other formats identified. When included in a CoverageSummary with an Identifier, this list, including all values inherited from ancestor coverages, shall be an exact copy of the list of SupportedFormat parameters in the corresponding CoverageDescription. Each CoverageSummary shall list or inherit at least one SupportedFormat. ')

    
    # Element {http://www.opengis.net/ows/1.1}Metadata uses Python identifier Metadata
    __Metadata = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Metadata'), 'Metadata', '__httpwww_opengis_netwcs1_1_CoverageSummaryType_httpwww_opengis_netows1_1Metadata', True)

    
    Metadata = property(__Metadata.value, __Metadata.set, None, None)

    
    # Element Keywords ({http://www.opengis.net/ows/1.1}Keywords) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element {http://www.opengis.net/wcs/1.1}Identifier uses Python identifier Identifier
    __Identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), 'Identifier', '__httpwww_opengis_netwcs1_1_CoverageSummaryType_httpwww_opengis_netwcs1_1Identifier', False)

    
    Identifier = property(__Identifier.value, __Identifier.set, None, None)

    
    # Element Abstract ({http://www.opengis.net/ows/1.1}Abstract) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element {http://www.opengis.net/wcs/1.1}CoverageSummary uses Python identifier CoverageSummary
    __CoverageSummary = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'CoverageSummary'), 'CoverageSummary', '__httpwww_opengis_netwcs1_1_CoverageSummaryType_httpwww_opengis_netwcs1_1CoverageSummary', True)

    
    CoverageSummary = property(__CoverageSummary.value, __CoverageSummary.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}SupportedCRS uses Python identifier SupportedCRS
    __SupportedCRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'SupportedCRS'), 'SupportedCRS', '__httpwww_opengis_netwcs1_1_CoverageSummaryType_httpwww_opengis_netwcs1_1SupportedCRS', True)

    
    SupportedCRS = property(__SupportedCRS.value, __SupportedCRS.set, None, u'Unordered list of references to CRSs that may be referenced as a GridBaseCRS of a GridCRS in the Output part of a GetCoverage request. These CRSs shall also apply to all lower-level CoverageSummaries under this CoverageSummary, in addition to any other CRSs referenced. When included in a CoverageSummary with an Identifier, this list, including all values inherited from ancestor coverages, shall be an exact copy of the list of SupportedCRS parameters in the corresponding CoverageDescription. Each CoverageSummary shall list or inherit at least one SupportedCRS. ')

    
    # Element Title ({http://www.opengis.net/ows/1.1}Title) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element {http://www.opengis.net/ows/1.1}WGS84BoundingBox uses Python identifier WGS84BoundingBox
    __WGS84BoundingBox = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'WGS84BoundingBox'), 'WGS84BoundingBox', '__httpwww_opengis_netwcs1_1_CoverageSummaryType_httpwww_opengis_netows1_1WGS84BoundingBox', True)

    
    WGS84BoundingBox = property(__WGS84BoundingBox.value, __WGS84BoundingBox.set, None, None)


    _ElementMap = pyxb.bundles.opengis.ows_1_1.DescriptionType._ElementMap.copy()
    _ElementMap.update({
        __SupportedFormat.name() : __SupportedFormat,
        __Metadata.name() : __Metadata,
        __Identifier.name() : __Identifier,
        __CoverageSummary.name() : __CoverageSummary,
        __SupportedCRS.name() : __SupportedCRS,
        __WGS84BoundingBox.name() : __WGS84BoundingBox
    })
    _AttributeMap = pyxb.bundles.opengis.ows_1_1.DescriptionType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'CoverageSummaryType', CoverageSummaryType)


# Complex type ImageCRSRefType with content type ELEMENT_ONLY
class ImageCRSRefType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ImageCRSRefType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/gml}ImageCRS uses Python identifier ImageCRS
    __ImageCRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'ImageCRS'), 'ImageCRS', '__httpwww_opengis_netwcs1_1_ImageCRSRefType_httpwww_opengis_netgmlImageCRS', False)

    
    ImageCRS = property(__ImageCRS.value, __ImageCRS.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netwcs1_1_ImageCRSRefType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netwcs1_1_ImageCRSRefType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netwcs1_1_ImageCRSRefType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netwcs1_1_ImageCRSRefType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netwcs1_1_ImageCRSRefType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netwcs1_1_ImageCRSRefType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netwcs1_1_ImageCRSRefType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netwcs1_1_ImageCRSRefType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)


    _ElementMap = {
        __ImageCRS.name() : __ImageCRS
    }
    _AttributeMap = {
        __actuate.name() : __actuate,
        __show.name() : __show,
        __role.name() : __role,
        __href.name() : __href,
        __title.name() : __title,
        __type.name() : __type,
        __remoteSchema.name() : __remoteSchema,
        __arcrole.name() : __arcrole
    }
Namespace.addCategoryObject('typeBinding', u'ImageCRSRefType', ImageCRSRefType)


# Complex type TimeSequenceType with content type ELEMENT_ONLY
class TimeSequenceType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimeSequenceType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}TimePeriod uses Python identifier TimePeriod
    __TimePeriod = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimePeriod'), 'TimePeriod', '__httpwww_opengis_netwcs1_1_TimeSequenceType_httpwww_opengis_netwcs1_1TimePeriod', True)

    
    TimePeriod = property(__TimePeriod.value, __TimePeriod.set, None, None)

    
    # Element {http://www.opengis.net/gml}timePosition uses Python identifier timePosition
    __timePosition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'timePosition'), 'timePosition', '__httpwww_opengis_netwcs1_1_TimeSequenceType_httpwww_opengis_netgmltimePosition', True)

    
    timePosition = property(__timePosition.value, __timePosition.set, None, u'Direct representation of a temporal position')


    _ElementMap = {
        __TimePeriod.name() : __TimePeriod,
        __timePosition.name() : __timePosition
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TimeSequenceType', TimeSequenceType)


# Complex type FieldType with content type ELEMENT_ONLY
class FieldType (pyxb.bundles.opengis.ows_1_1.DescriptionType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FieldType')
    # Base type is pyxb.bundles.opengis.ows_1_1.DescriptionType
    
    # Element {http://www.opengis.net/wcs/1.1}Axis uses Python identifier Axis
    __Axis = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Axis'), 'Axis', '__httpwww_opengis_netwcs1_1_FieldType_httpwww_opengis_netwcs1_1Axis', True)

    
    Axis = property(__Axis.value, __Axis.set, None, u'Unordered list of the axes in a vector field for which there are Field values. This list shall be included when this Field has a vector of values. Notice that the axes can be listed here in any order; however, the axis order listed here shall be used in the KVP encoding of a GetCoverage operation request. ')

    
    # Element {http://www.opengis.net/wcs/1.1}Definition uses Python identifier Definition
    __Definition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Definition'), 'Definition', '__httpwww_opengis_netwcs1_1_FieldType_httpwww_opengis_netwcs1_1Definition', False)

    
    Definition = property(__Definition.value, __Definition.set, None, u'Further definition of this field, including meaning, units, etc. In this Definition, the AllowedValues should be used to encode the extent of possible values for this field, excluding the Null Value. If the range is not known, AnyValue should be used. ')

    
    # Element Keywords ({http://www.opengis.net/ows/1.1}Keywords) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element Title ({http://www.opengis.net/ows/1.1}Title) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element {http://www.opengis.net/wcs/1.1}NullValue uses Python identifier NullValue
    __NullValue = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'NullValue'), 'NullValue', '__httpwww_opengis_netwcs1_1_FieldType_httpwww_opengis_netwcs1_1NullValue', True)

    
    NullValue = property(__NullValue.value, __NullValue.set, None, u'Unordered list of the values used when valid Field values are not available for whatever reason. The coverage encoding itself may specify a fixed value for null (e.g. \u201c\u201399999\u201d or \u201cN/A\u201d), but often the choice is up to the provider and must be communicated to the client outside the coverage itself. Each null value shall be encoded as a string. The optional codeSpace attribute can reference a definition of the reason why this value is null. ')

    
    # Element {http://www.opengis.net/wcs/1.1}Identifier uses Python identifier Identifier
    __Identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), 'Identifier', '__httpwww_opengis_netwcs1_1_FieldType_httpwww_opengis_netwcs1_1Identifier', False)

    
    Identifier = property(__Identifier.value, __Identifier.set, None, None)

    
    # Element Abstract ({http://www.opengis.net/ows/1.1}Abstract) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element {http://www.opengis.net/wcs/1.1}InterpolationMethods uses Python identifier InterpolationMethods
    __InterpolationMethods = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'InterpolationMethods'), 'InterpolationMethods', '__httpwww_opengis_netwcs1_1_FieldType_httpwww_opengis_netwcs1_1InterpolationMethods', False)

    
    InterpolationMethods = property(__InterpolationMethods.value, __InterpolationMethods.set, None, u'List of the interpolation method(s) that may be used when continuous grid coverage resampling is needed. ')


    _ElementMap = pyxb.bundles.opengis.ows_1_1.DescriptionType._ElementMap.copy()
    _ElementMap.update({
        __Axis.name() : __Axis,
        __Definition.name() : __Definition,
        __NullValue.name() : __NullValue,
        __Identifier.name() : __Identifier,
        __InterpolationMethods.name() : __InterpolationMethods
    })
    _AttributeMap = pyxb.bundles.opengis.ows_1_1.DescriptionType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'FieldType', FieldType)


# Complex type RequestBaseType with content type EMPTY
class RequestBaseType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RequestBaseType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpwww_opengis_netwcs1_1_RequestBaseType_version', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'1.1.2', required=True)
    
    version = property(__version.value, __version.set, None, u'Specification version for WCS version and operation. See Version parameter Subclause 7.3.1 of OWS Common for more information. ')

    
    # Attribute service uses Python identifier service
    __service = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpwww_opengis_netwcs1_1_RequestBaseType_service', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'WCS', required=True)
    
    service = property(__service.value, __service.set, None, u'Service type identifier, where the value is the OWS type abbreviation. For WCS operation requests, the value is "WCS". ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __version.name() : __version,
        __service.name() : __service
    }
Namespace.addCategoryObject('typeBinding', u'RequestBaseType', RequestBaseType)


# Complex type CTD_ANON_3 with content type ELEMENT_ONLY
class CTD_ANON_3 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/wcs/1.1}Identifier uses Python identifier Identifier
    __Identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), 'Identifier', '__httpwww_opengis_netwcs1_1_CTD_ANON_3_httpwww_opengis_netwcs1_1Identifier', True)

    
    Identifier = property(__Identifier.value, __Identifier.set, None, None)

    
    # Attribute version inherited from {http://www.opengis.net/wcs/1.1}RequestBaseType
    
    # Attribute service inherited from {http://www.opengis.net/wcs/1.1}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __Identifier.name() : __Identifier
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_4 with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}CoverageDescription uses Python identifier CoverageDescription
    __CoverageDescription = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'CoverageDescription'), 'CoverageDescription', '__httpwww_opengis_netwcs1_1_CTD_ANON_4_httpwww_opengis_netwcs1_1CoverageDescription', True)

    
    CoverageDescription = property(__CoverageDescription.value, __CoverageDescription.set, None, None)


    _ElementMap = {
        __CoverageDescription.name() : __CoverageDescription
    }
    _AttributeMap = {
        
    }



# Complex type RangeSubsetType with content type ELEMENT_ONLY
class RangeSubsetType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RangeSubsetType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}FieldSubset uses Python identifier FieldSubset
    __FieldSubset = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'FieldSubset'), 'FieldSubset', '__httpwww_opengis_netwcs1_1_RangeSubsetType_httpwww_opengis_netwcs1_1FieldSubset', True)

    
    FieldSubset = property(__FieldSubset.value, __FieldSubset.set, None, u'Unordered list of one or more desired subsets of range fields. TBD. ')


    _ElementMap = {
        __FieldSubset.name() : __FieldSubset
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'RangeSubsetType', RangeSubsetType)


# Complex type CoverageDescriptionType with content type ELEMENT_ONLY
class CoverageDescriptionType (pyxb.bundles.opengis.ows_1_1.DescriptionType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CoverageDescriptionType')
    # Base type is pyxb.bundles.opengis.ows_1_1.DescriptionType
    
    # Element {http://www.opengis.net/ows/1.1}Metadata uses Python identifier Metadata
    __Metadata = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Metadata'), 'Metadata', '__httpwww_opengis_netwcs1_1_CoverageDescriptionType_httpwww_opengis_netows1_1Metadata', True)

    
    Metadata = property(__Metadata.value, __Metadata.set, None, None)

    
    # Element Abstract ({http://www.opengis.net/ows/1.1}Abstract) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element Keywords ({http://www.opengis.net/ows/1.1}Keywords) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element {http://www.opengis.net/wcs/1.1}Identifier uses Python identifier Identifier
    __Identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), 'Identifier', '__httpwww_opengis_netwcs1_1_CoverageDescriptionType_httpwww_opengis_netwcs1_1Identifier', False)

    
    Identifier = property(__Identifier.value, __Identifier.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}SupportedFormat uses Python identifier SupportedFormat
    __SupportedFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'SupportedFormat'), 'SupportedFormat', '__httpwww_opengis_netwcs1_1_CoverageDescriptionType_httpwww_opengis_netwcs1_1SupportedFormat', True)

    
    SupportedFormat = property(__SupportedFormat.value, __SupportedFormat.set, None, u'Unordered list of identifiers of all the formats in which GetCoverage operation responses can be encoded for this coverage. ')

    
    # Element {http://www.opengis.net/wcs/1.1}SupportedCRS uses Python identifier SupportedCRS
    __SupportedCRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'SupportedCRS'), 'SupportedCRS', '__httpwww_opengis_netwcs1_1_CoverageDescriptionType_httpwww_opengis_netwcs1_1SupportedCRS', True)

    
    SupportedCRS = property(__SupportedCRS.value, __SupportedCRS.set, None, u'Unordered list of references to all the coordinate reference systems that may be referenced as the GridBaseCRS of a GridCRS specified in the Output part of a GetCoverage operation request. The GridBaseCRS of the GridCRS of a georectified offered coverage shall be listed as a SupportedCRS. An ImageCRS for an unrectified offered image shall be listed as a SupportedCRS, so that it may be referenced as the GridBaseCRS of a GridCRS. This ImageCRS shall be the ImageCRS of that unrectified offered image, or the ImageCRS that is referenced as the GridBaseCRS of the GridCRS that is used by that unrectified offered image  In addition, the GetCoverage operation output may be expressed in the ImageCRS or GridCRS of an unrectified offered coverage, instead of in a specified GridCRS. These Supported\xacCRSs can also be referenced in the BoundingBox in the DomainSubset part of a GetCoverage request. ')

    
    # Element {http://www.opengis.net/wcs/1.1}Range uses Python identifier Range
    __Range = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Range'), 'Range', '__httpwww_opengis_netwcs1_1_CoverageDescriptionType_httpwww_opengis_netwcs1_1Range', False)

    
    Range = property(__Range.value, __Range.set, None, None)

    
    # Element Title ({http://www.opengis.net/ows/1.1}Title) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element {http://www.opengis.net/wcs/1.1}Domain uses Python identifier Domain
    __Domain = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Domain'), 'Domain', '__httpwww_opengis_netwcs1_1_CoverageDescriptionType_httpwww_opengis_netwcs1_1Domain', False)

    
    Domain = property(__Domain.value, __Domain.set, None, None)


    _ElementMap = pyxb.bundles.opengis.ows_1_1.DescriptionType._ElementMap.copy()
    _ElementMap.update({
        __Metadata.name() : __Metadata,
        __Identifier.name() : __Identifier,
        __SupportedFormat.name() : __SupportedFormat,
        __SupportedCRS.name() : __SupportedCRS,
        __Range.name() : __Range,
        __Domain.name() : __Domain
    })
    _AttributeMap = pyxb.bundles.opengis.ows_1_1.DescriptionType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'CoverageDescriptionType', CoverageDescriptionType)


# Complex type CTD_ANON_5 with content type ELEMENT_ONLY
class CTD_ANON_5 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/ows/1.1}Identifier uses Python identifier Identifier
    __Identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Identifier'), 'Identifier', '__httpwww_opengis_netwcs1_1_CTD_ANON_5_httpwww_opengis_netows1_1Identifier', False)

    
    Identifier = property(__Identifier.value, __Identifier.set, None, u'Unique identifier or name of this dataset. ')

    
    # Element {http://www.opengis.net/wcs/1.1}Output uses Python identifier Output
    __Output = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Output'), 'Output', '__httpwww_opengis_netwcs1_1_CTD_ANON_5_httpwww_opengis_netwcs1_1Output', False)

    
    Output = property(__Output.value, __Output.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}DomainSubset uses Python identifier DomainSubset
    __DomainSubset = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'DomainSubset'), 'DomainSubset', '__httpwww_opengis_netwcs1_1_CTD_ANON_5_httpwww_opengis_netwcs1_1DomainSubset', False)

    
    DomainSubset = property(__DomainSubset.value, __DomainSubset.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}RangeSubset uses Python identifier RangeSubset
    __RangeSubset = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'RangeSubset'), 'RangeSubset', '__httpwww_opengis_netwcs1_1_CTD_ANON_5_httpwww_opengis_netwcs1_1RangeSubset', False)

    
    RangeSubset = property(__RangeSubset.value, __RangeSubset.set, None, u"Optional selection of a subset of the coverage's range. ")

    
    # Attribute version inherited from {http://www.opengis.net/wcs/1.1}RequestBaseType
    
    # Attribute service inherited from {http://www.opengis.net/wcs/1.1}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __Identifier.name() : __Identifier,
        __Output.name() : __Output,
        __DomainSubset.name() : __DomainSubset,
        __RangeSubset.name() : __RangeSubset
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type TimePeriodType with content type ELEMENT_ONLY
class TimePeriodType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TimePeriodType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}TimeResolution uses Python identifier TimeResolution
    __TimeResolution = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TimeResolution'), 'TimeResolution', '__httpwww_opengis_netwcs1_1_TimePeriodType_httpwww_opengis_netwcs1_1TimeResolution', False)

    
    TimeResolution = property(__TimeResolution.value, __TimeResolution.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}EndPosition uses Python identifier EndPosition
    __EndPosition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'EndPosition'), 'EndPosition', '__httpwww_opengis_netwcs1_1_TimePeriodType_httpwww_opengis_netwcs1_1EndPosition', False)

    
    EndPosition = property(__EndPosition.value, __EndPosition.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}BeginPosition uses Python identifier BeginPosition
    __BeginPosition = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'BeginPosition'), 'BeginPosition', '__httpwww_opengis_netwcs1_1_TimePeriodType_httpwww_opengis_netwcs1_1BeginPosition', False)

    
    BeginPosition = property(__BeginPosition.value, __BeginPosition.set, None, None)

    
    # Attribute frame uses Python identifier frame
    __frame = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'frame'), 'frame', '__httpwww_opengis_netwcs1_1_TimePeriodType_frame', pyxb.binding.datatypes.anyURI, unicode_default=u'#ISO-8601')
    
    frame = property(__frame.value, __frame.set, None, None)


    _ElementMap = {
        __TimeResolution.name() : __TimeResolution,
        __EndPosition.name() : __EndPosition,
        __BeginPosition.name() : __BeginPosition
    }
    _AttributeMap = {
        __frame.name() : __frame
    }
Namespace.addCategoryObject('typeBinding', u'TimePeriodType', TimePeriodType)


# Complex type DomainSubsetType with content type ELEMENT_ONLY
class DomainSubsetType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DomainSubsetType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows/1.1}BoundingBox uses Python identifier BoundingBox
    __BoundingBox = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'BoundingBox'), 'BoundingBox', '__httpwww_opengis_netwcs1_1_DomainSubsetType_httpwww_opengis_netows1_1BoundingBox', False)

    
    BoundingBox = property(__BoundingBox.value, __BoundingBox.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}TemporalSubset uses Python identifier TemporalSubset
    __TemporalSubset = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TemporalSubset'), 'TemporalSubset', '__httpwww_opengis_netwcs1_1_DomainSubsetType_httpwww_opengis_netwcs1_1TemporalSubset', False)

    
    TemporalSubset = property(__TemporalSubset.value, __TemporalSubset.set, None, u'Definition of subset of coverage temporal domain. ')


    _ElementMap = {
        __BoundingBox.name() : __BoundingBox,
        __TemporalSubset.name() : __TemporalSubset
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'DomainSubsetType', DomainSubsetType)


# Complex type CTD_ANON_6 with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}Identifier uses Python identifier Identifier
    __Identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), 'Identifier', '__httpwww_opengis_netwcs1_1_CTD_ANON_6_httpwww_opengis_netwcs1_1Identifier', False)

    
    Identifier = property(__Identifier.value, __Identifier.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}Key uses Python identifier Key
    __Key = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Key'), 'Key', '__httpwww_opengis_netwcs1_1_CTD_ANON_6_httpwww_opengis_netwcs1_1Key', True)

    
    Key = property(__Key.value, __Key.set, None, u'Unordered list of (at least one) Key, to be used for selecting values in a range vector field. The Keys within this list shall be unique. ')


    _ElementMap = {
        __Identifier.name() : __Identifier,
        __Key.name() : __Key
    }
    _AttributeMap = {
        
    }



# Complex type GridCrsType with content type ELEMENT_ONLY
class GridCrsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'GridCrsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}GridType uses Python identifier GridType
    __GridType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'GridType'), 'GridType', '__httpwww_opengis_netwcs1_1_GridCrsType_httpwww_opengis_netwcs1_1GridType', False)

    
    GridType = property(__GridType.value, __GridType.set, None, u'Association to the OperationMethod used to define this Grid CRS. This association defaults to an association to the most commonly used method, which is referenced by the URN "urn:ogc:def:method:WCS:1.1:2dSimpleGrid". For a GridCRS, this association is limited to a remote definition of a grid definition Method (not encoded in-line) that encodes a variation on the method implied by the CV_RectifiedGrid class in ISO 19123, without the inheritance from CV_Grid. ')

    
    # Element {http://www.opengis.net/gml}srsName uses Python identifier srsName
    __srsName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'srsName'), 'srsName', '__httpwww_opengis_netwcs1_1_GridCrsType_httpwww_opengis_netgmlsrsName', False)

    
    srsName = property(__srsName.value, __srsName.set, None, u'The name by which this reference system is identified.')

    
    # Element {http://www.opengis.net/wcs/1.1}GridCS uses Python identifier GridCS
    __GridCS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'GridCS'), 'GridCS', '__httpwww_opengis_netwcs1_1_GridCrsType_httpwww_opengis_netwcs1_1GridCS', False)

    
    GridCS = property(__GridCS.value, __GridCS.set, None, u'Association to the (Cartesian) grid coordinate system used by this Grid CRS. In this use of a (Cartesian) grid coordinate system, the grid positions shall be in the centers of the image or other grid coverage values (not between the grid values), as specified in ISO 19123. Also, the grid point indices at the origin shall be 0, 0 (not 1,1), as specified in ISO 19123. This GridCS defaults to the most commonly used grid coordinate system, which is referenced by the URN "urn:ogc:def:cs:OGC:0.0:Grid2dSquareCS". For a GridCRS, this association is limited to a remote definition of the GridCS (not encoded in-line). ')

    
    # Element {http://www.opengis.net/wcs/1.1}GridOrigin uses Python identifier GridOrigin
    __GridOrigin = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'GridOrigin'), 'GridOrigin', '__httpwww_opengis_netwcs1_1_GridCrsType_httpwww_opengis_netwcs1_1GridOrigin', False)

    
    GridOrigin = property(__GridOrigin.value, __GridOrigin.set, None, u'Coordinates of the grid origin position in the GridBaseCRS of this GridCRS. This origin defaults be the most commonly used origin in a GridCRS used in the output part of a GetCapabilities operation request, namely "0 0". This element is adapted from gml:pos. ')

    
    # Element {http://www.opengis.net/wcs/1.1}GridBaseCRS uses Python identifier GridBaseCRS
    __GridBaseCRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'GridBaseCRS'), 'GridBaseCRS', '__httpwww_opengis_netwcs1_1_GridCrsType_httpwww_opengis_netwcs1_1GridBaseCRS', False)

    
    GridBaseCRS = property(__GridBaseCRS.value, __GridBaseCRS.set, None, u'Association to the coordinate reference system (CRS) in which this Grid CRS is specified. A GridCRS can use any type of GridBaseCRS, including GeographicCRS, ProjectedCRS, ImageCRS, or a different GridCRS. For a GridCRS, this association is limited to a remote definition of the GridBaseCRS (not encoded in-line). ')

    
    # Element {http://www.opengis.net/wcs/1.1}GridOffsets uses Python identifier GridOffsets
    __GridOffsets = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'GridOffsets'), 'GridOffsets', '__httpwww_opengis_netwcs1_1_GridCrsType_httpwww_opengis_netwcs1_1GridOffsets', False)

    
    GridOffsets = property(__GridOffsets.value, __GridOffsets.set, None, u'Two or more grid position offsets from the grid origin in the GridBaseCRS of this GridCRS. Example: For the grid2dIn2dCRS OperationMethod, this Offsets element shall contain four values, the first two values shall specify the grid offset for the first grid axis in the 2D base CRS, and the second pair of values shall specify the grid offset for the second grid axis. In this case, the middle two values are zero for un-rotated and un-skewed grids. ')

    
    # Attribute {http://www.opengis.net/gml}id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'id'), 'id', '__httpwww_opengis_netwcs1_1_GridCrsType_httpwww_opengis_netgmlid', pyxb.binding.datatypes.ID)
    
    id = property(__id.value, __id.set, None, u'Database handle for the object.  It is of XML type ID, so is constrained to be unique in the XML document within which it occurs.  An external identifier for the object in the form of a URI may be constructed using standard XML and XPointer methods.  This is done by concatenating the URI for the document, a fragment separator, and the value of the id attribute.')


    _ElementMap = {
        __GridType.name() : __GridType,
        __srsName.name() : __srsName,
        __GridCS.name() : __GridCS,
        __GridOrigin.name() : __GridOrigin,
        __GridBaseCRS.name() : __GridBaseCRS,
        __GridOffsets.name() : __GridOffsets
    }
    _AttributeMap = {
        __id.name() : __id
    }
Namespace.addCategoryObject('typeBinding', u'GridCrsType', GridCrsType)


# Complex type OutputType with content type ELEMENT_ONLY
class OutputType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'OutputType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}GridCRS uses Python identifier GridCRS
    __GridCRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'GridCRS'), 'GridCRS', '__httpwww_opengis_netwcs1_1_OutputType_httpwww_opengis_netwcs1_1GridCRS', False)

    
    GridCRS = property(__GridCRS.value, __GridCRS.set, None, None)

    
    # Attribute store uses Python identifier store
    __store = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'store'), 'store', '__httpwww_opengis_netwcs1_1_OutputType_store', pyxb.binding.datatypes.boolean, unicode_default=u'false')
    
    store = property(__store.value, __store.set, None, u'Specifies if the output coverage should be stored, remotely from the client at a network URL, instead of being returned with the operation response. This parameter should be included only if this operation parameter is supported by server, as encoded in the OperationsMetadata section of the Capabilities document. ')

    
    # Attribute format uses Python identifier format
    __format = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'format'), 'format', '__httpwww_opengis_netwcs1_1_OutputType_format', pyxb.bundles.opengis.ows_1_1.MimeType, required=True)
    
    format = property(__format.value, __format.set, None, u'Identifier of the format in which GetCoverage response shall be encoded. This identifier value shall be among those listed as SupportedFormats in the DescribeCoverage operation response. ')


    _ElementMap = {
        __GridCRS.name() : __GridCRS
    }
    _AttributeMap = {
        __store.name() : __store,
        __format.name() : __format
    }
Namespace.addCategoryObject('typeBinding', u'OutputType', OutputType)


# Complex type AxisType with content type ELEMENT_ONLY
class AxisType (pyxb.bundles.opengis.ows_1_1.DescriptionType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AxisType')
    # Base type is pyxb.bundles.opengis.ows_1_1.DescriptionType
    
    # Element {http://www.opengis.net/ows/1.1}UOM uses Python identifier UOM
    __UOM = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'UOM'), 'UOM', '__httpwww_opengis_netwcs1_1_AxisType_httpwww_opengis_netows1_1UOM', False)

    
    UOM = property(__UOM.value, __UOM.set, None, u'Definition of the unit of measure of this set of values. In this case, the xlink:href attribute can reference a URN for a well-known unit of measure (uom). For example, such a URN could be a UOM identification URN defined in the "ogc" URN namespace. ')

    
    # Element {http://www.opengis.net/ows/1.1}DataType uses Python identifier DataType
    __DataType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'DataType'), 'DataType', '__httpwww_opengis_netwcs1_1_AxisType_httpwww_opengis_netows1_1DataType', False)

    
    DataType = property(__DataType.value, __DataType.set, None, u'Definition of the data type of this set of values. In this case, the xlink:href attribute can reference a URN for a well-known data type. For example, such a URN could be a data type identification URN defined in the "ogc" URN namespace. ')

    
    # Element Title ({http://www.opengis.net/ows/1.1}Title) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element {http://www.opengis.net/ows/1.1}ReferenceSystem uses Python identifier ReferenceSystem
    __ReferenceSystem = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'ReferenceSystem'), 'ReferenceSystem', '__httpwww_opengis_netwcs1_1_AxisType_httpwww_opengis_netows1_1ReferenceSystem', False)

    
    ReferenceSystem = property(__ReferenceSystem.value, __ReferenceSystem.set, None, u'Definition of the reference system used by this set of values, including the unit of measure whenever applicable (as is normal). In this case, the xlink:href attribute can reference a URN for a well-known reference system, such as for a coordinate reference system (CRS). For example, such a URN could be a CRS identification URN defined in the "ogc" URN namespace. ')

    
    # Element {http://www.opengis.net/wcs/1.1}AvailableKeys uses Python identifier AvailableKeys
    __AvailableKeys = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AvailableKeys'), 'AvailableKeys', '__httpwww_opengis_netwcs1_1_AxisType_httpwww_opengis_netwcs1_1AvailableKeys', False)

    
    AvailableKeys = property(__AvailableKeys.value, __AvailableKeys.set, None, u'List of all the available (valid) key values for this axis. For numeric keys, signed values should be ordered from negative infinity to positive infinity. ')

    
    # Element {http://www.opengis.net/ows/1.1}Metadata uses Python identifier Metadata
    __Metadata = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Metadata'), 'Metadata', '__httpwww_opengis_netwcs1_1_AxisType_httpwww_opengis_netows1_1Metadata', True)

    
    Metadata = property(__Metadata.value, __Metadata.set, None, None)

    
    # Element Keywords ({http://www.opengis.net/ows/1.1}Keywords) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element Abstract ({http://www.opengis.net/ows/1.1}Abstract) inherited from {http://www.opengis.net/ows/1.1}DescriptionType
    
    # Element {http://www.opengis.net/ows/1.1}Meaning uses Python identifier Meaning
    __Meaning = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Meaning'), 'Meaning', '__httpwww_opengis_netwcs1_1_AxisType_httpwww_opengis_netows1_1Meaning', False)

    
    Meaning = property(__Meaning.value, __Meaning.set, None, u'Definition of the meaning or semantics of this set of values. This Meaning can provide more specific, complete, precise, machine accessible, and machine understandable semantics about this quantity, relative to other available semantic information. For example, other semantic information is often provided in "documentation" elements in XML Schemas or "description" elements in GML objects. ')

    
    # Attribute identifier uses Python identifier identifier
    __identifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'identifier'), 'identifier', '__httpwww_opengis_netwcs1_1_AxisType_identifier', IdentifierType, required=True)
    
    identifier = property(__identifier.value, __identifier.set, None, u'Name or identifier of this axis. ')


    _ElementMap = pyxb.bundles.opengis.ows_1_1.DescriptionType._ElementMap.copy()
    _ElementMap.update({
        __UOM.name() : __UOM,
        __DataType.name() : __DataType,
        __ReferenceSystem.name() : __ReferenceSystem,
        __AvailableKeys.name() : __AvailableKeys,
        __Metadata.name() : __Metadata,
        __Meaning.name() : __Meaning
    })
    _AttributeMap = pyxb.bundles.opengis.ows_1_1.DescriptionType._AttributeMap.copy()
    _AttributeMap.update({
        __identifier.name() : __identifier
    })
Namespace.addCategoryObject('typeBinding', u'AxisType', AxisType)


# Complex type CTD_ANON_7 with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}AxisSubset uses Python identifier AxisSubset
    __AxisSubset = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AxisSubset'), 'AxisSubset', '__httpwww_opengis_netwcs1_1_CTD_ANON_7_httpwww_opengis_netwcs1_1AxisSubset', True)

    
    AxisSubset = property(__AxisSubset.value, __AxisSubset.set, None, u'List of selected Keys for this axis, to be used for selecting values in a vector range field. TBD. ')

    
    # Element {http://www.opengis.net/wcs/1.1}InterpolationType uses Python identifier InterpolationType
    __InterpolationType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'InterpolationType'), 'InterpolationType', '__httpwww_opengis_netwcs1_1_CTD_ANON_7_httpwww_opengis_netwcs1_1InterpolationType', False)

    
    InterpolationType = property(__InterpolationType.value, __InterpolationType.set, None, u'Optional identifier of the spatial interpolation type to be applied to this range field. This interpolation type shall be one that is identified for this Field in the CoverageDescription. When this parameter is omitted, the interpolation method used shall be the default method specified for this Field, if any. ')

    
    # Element {http://www.opengis.net/ows/1.1}Identifier uses Python identifier Identifier
    __Identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Identifier'), 'Identifier', '__httpwww_opengis_netwcs1_1_CTD_ANON_7_httpwww_opengis_netows1_1Identifier', False)

    
    Identifier = property(__Identifier.value, __Identifier.set, None, u'Unique identifier or name of this dataset. ')


    _ElementMap = {
        __AxisSubset.name() : __AxisSubset,
        __InterpolationType.name() : __InterpolationType,
        __Identifier.name() : __Identifier
    }
    _AttributeMap = {
        
    }



# Complex type CoveragesType with content type ELEMENT_ONLY
class CoveragesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CoveragesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}Coverage uses Python identifier Coverage
    __Coverage = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Coverage'), 'Coverage', '__httpwww_opengis_netwcs1_1_CoveragesType_httpwww_opengis_netwcs1_1Coverage', True)

    
    Coverage = property(__Coverage.value, __Coverage.set, None, u'Complete data for one coverage, referencing each coverage file either remotely or locally in the same message. ')


    _ElementMap = {
        __Coverage.name() : __Coverage
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'CoveragesType', CoveragesType)


# Complex type CTD_ANON_8 with content type ELEMENT_ONLY
class CTD_ANON_8 (pyxb.bundles.opengis.ows_1_1.GetCapabilitiesType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.bundles.opengis.ows_1_1.GetCapabilitiesType
    
    # Element Sections ({http://www.opengis.net/ows/1.1}Sections) inherited from {http://www.opengis.net/ows/1.1}GetCapabilitiesType
    
    # Element AcceptFormats ({http://www.opengis.net/ows/1.1}AcceptFormats) inherited from {http://www.opengis.net/ows/1.1}GetCapabilitiesType
    
    # Element AcceptVersions ({http://www.opengis.net/ows/1.1}AcceptVersions) inherited from {http://www.opengis.net/ows/1.1}GetCapabilitiesType
    
    # Attribute updateSequence inherited from {http://www.opengis.net/ows/1.1}GetCapabilitiesType
    
    # Attribute service uses Python identifier service
    __service = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpwww_opengis_netwcs1_1_CTD_ANON_8_service', pyxb.bundles.opengis.ows_1_1.ServiceType, fixed=True, unicode_default=u'WCS', required=True)
    
    service = property(__service.value, __service.set, None, None)


    _ElementMap = pyxb.bundles.opengis.ows_1_1.GetCapabilitiesType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = pyxb.bundles.opengis.ows_1_1.GetCapabilitiesType._AttributeMap.copy()
    _AttributeMap.update({
        __service.name() : __service
    })



# Complex type CTD_ANON_9 with content type ELEMENT_ONLY
class CTD_ANON_9 (pyxb.bundles.opengis.ows_1_1.CapabilitiesBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.bundles.opengis.ows_1_1.CapabilitiesBaseType
    
    # Element ServiceIdentification ({http://www.opengis.net/ows/1.1}ServiceIdentification) inherited from {http://www.opengis.net/ows/1.1}CapabilitiesBaseType
    
    # Element {http://www.opengis.net/wcs/1.1}Contents uses Python identifier Contents
    __Contents = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Contents'), 'Contents', '__httpwww_opengis_netwcs1_1_CTD_ANON_9_httpwww_opengis_netwcs1_1Contents', False)

    
    Contents = property(__Contents.value, __Contents.set, None, u'Contents section of WCS service metadata (or Capabilities) XML document. For the WCS, these contents are brief metadata about the coverages available from this server, or a reference to another source from which this metadata is available. ')

    
    # Element ServiceProvider ({http://www.opengis.net/ows/1.1}ServiceProvider) inherited from {http://www.opengis.net/ows/1.1}CapabilitiesBaseType
    
    # Element OperationsMetadata ({http://www.opengis.net/ows/1.1}OperationsMetadata) inherited from {http://www.opengis.net/ows/1.1}CapabilitiesBaseType
    
    # Attribute updateSequence inherited from {http://www.opengis.net/ows/1.1}CapabilitiesBaseType
    
    # Attribute version inherited from {http://www.opengis.net/ows/1.1}CapabilitiesBaseType

    _ElementMap = pyxb.bundles.opengis.ows_1_1.CapabilitiesBaseType._ElementMap.copy()
    _ElementMap.update({
        __Contents.name() : __Contents
    })
    _AttributeMap = pyxb.bundles.opengis.ows_1_1.CapabilitiesBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CoverageDomainType with content type ELEMENT_ONLY
class CoverageDomainType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CoverageDomainType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wcs/1.1}SpatialDomain uses Python identifier SpatialDomain
    __SpatialDomain = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'SpatialDomain'), 'SpatialDomain', '__httpwww_opengis_netwcs1_1_CoverageDomainType_httpwww_opengis_netwcs1_1SpatialDomain', False)

    
    SpatialDomain = property(__SpatialDomain.value, __SpatialDomain.set, None, None)

    
    # Element {http://www.opengis.net/wcs/1.1}TemporalDomain uses Python identifier TemporalDomain
    __TemporalDomain = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TemporalDomain'), 'TemporalDomain', '__httpwww_opengis_netwcs1_1_CoverageDomainType_httpwww_opengis_netwcs1_1TemporalDomain', False)

    
    TemporalDomain = property(__TemporalDomain.value, __TemporalDomain.set, None, u'Definition of the temporal domain of a coverage, the times for which valid data are available. The times should to be ordered from the oldest to the newest. ')


    _ElementMap = {
        __SpatialDomain.name() : __SpatialDomain,
        __TemporalDomain.name() : __TemporalDomain
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'CoverageDomainType', CoverageDomainType)


AvailableKeys = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AvailableKeys'), CTD_ANON, documentation=u'List of all the available (valid) key values for this axis. For numeric keys, signed values should be ordered from negative infinity to positive infinity. ')
Namespace.addCategoryObject('elementBinding', AvailableKeys.name().localName(), AvailableKeys)

Contents = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Contents'), CTD_ANON_2, documentation=u'Contents section of WCS service metadata (or Capabilities) XML document. For the WCS, these contents are brief metadata about the coverages available from this server, or a reference to another source from which this metadata is available. ')
Namespace.addCategoryObject('elementBinding', Contents.name().localName(), Contents)

Transformation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Transformation'), pyxb.bundles.opengis.gml.AbstractCoordinateOperationType, documentation=u'Georeferencing coordinate transformation for unrectified coverage. This georeferencing transformation can be specified as a Transformation, or a ConcatenatedOperation that includes at least one Transformation. ')
Namespace.addCategoryObject('elementBinding', Transformation.name().localName(), Transformation)

GridType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridType'), pyxb.binding.datatypes.anyURI, documentation=u'Association to the OperationMethod used to define this Grid CRS. This association defaults to an association to the most commonly used method, which is referenced by the URN "urn:ogc:def:method:WCS:1.1:2dSimpleGrid". For a GridCRS, this association is limited to a remote definition of a grid definition Method (not encoded in-line) that encodes a variation on the method implied by the CV_RectifiedGrid class in ISO 19123, without the inheritance from CV_Grid. ')
Namespace.addCategoryObject('elementBinding', GridType.name().localName(), GridType)

InterpolationMethods = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InterpolationMethods'), CTD_ANON_, documentation=u'List of the interpolation method(s) that may be used when continuous grid coverage resampling is needed. ')
Namespace.addCategoryObject('elementBinding', InterpolationMethods.name().localName(), InterpolationMethods)

TemporalDomain = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TemporalDomain'), TimeSequenceType, documentation=u'Definition of the temporal domain of a coverage, the times for which valid data are available. The times should to be ordered from the oldest to the newest. ')
Namespace.addCategoryObject('elementBinding', TemporalDomain.name().localName(), TemporalDomain)

GridOrigin = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridOrigin'), pyxb.bundles.opengis.gml.doubleList, documentation=u'Coordinates of the grid origin position in the GridBaseCRS of this GridCRS. This origin defaults be the most commonly used origin in a GridCRS used in the output part of a GetCapabilities operation request, namely "0 0". This element is adapted from gml:pos. ')
Namespace.addCategoryObject('elementBinding', GridOrigin.name().localName(), GridOrigin)

DescribeCoverage = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DescribeCoverage'), CTD_ANON_3, documentation=u'Request to a WCS to perform the DescribeCoverage operation. This operation allows a client to retrieve descriptions of one or more coverages. In this XML encoding, no "request" parameter is included, since the element name specifies the specific operation. ')
Namespace.addCategoryObject('elementBinding', DescribeCoverage.name().localName(), DescribeCoverage)

CoverageDescriptions = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CoverageDescriptions'), CTD_ANON_4, documentation=u'Response from a WCS DescribeCoverage operation, containing one or more coverage descriptions. ')
Namespace.addCategoryObject('elementBinding', CoverageDescriptions.name().localName(), CoverageDescriptions)

Identifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), IdentifierType)
Namespace.addCategoryObject('elementBinding', Identifier.name().localName(), Identifier)

GetCoverage = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetCoverage'), CTD_ANON_5, documentation=u'Request to a WCS to perform the GetCoverage operation. This operation allows a client to retrieve a subset of one coverage. In this XML encoding, no "request" parameter is included, since the element name specifies the specific operation. ')
Namespace.addCategoryObject('elementBinding', GetCoverage.name().localName(), GetCoverage)

GridBaseCRS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridBaseCRS'), pyxb.binding.datatypes.anyURI, documentation=u'Association to the coordinate reference system (CRS) in which this Grid CRS is specified. A GridCRS can use any type of GridBaseCRS, including GeographicCRS, ProjectedCRS, ImageCRS, or a different GridCRS. For a GridCRS, this association is limited to a remote definition of the GridBaseCRS (not encoded in-line). ')
Namespace.addCategoryObject('elementBinding', GridBaseCRS.name().localName(), GridBaseCRS)

GridCRS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridCRS'), GridCrsType)
Namespace.addCategoryObject('elementBinding', GridCRS.name().localName(), GridCRS)

TemporalSubset = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TemporalSubset'), TimeSequenceType, documentation=u'Definition of subset of coverage temporal domain. ')
Namespace.addCategoryObject('elementBinding', TemporalSubset.name().localName(), TemporalSubset)

GridOffsets = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridOffsets'), pyxb.bundles.opengis.gml.doubleList, documentation=u'Two or more grid position offsets from the grid origin in the GridBaseCRS of this GridCRS. Example: For the grid2dIn2dCRS OperationMethod, this Offsets element shall contain four values, the first two values shall specify the grid offset for the first grid axis in the 2D base CRS, and the second pair of values shall specify the grid offset for the second grid axis. In this case, the middle two values are zero for un-rotated and un-skewed grids. ')
Namespace.addCategoryObject('elementBinding', GridOffsets.name().localName(), GridOffsets)

CoverageSummary = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CoverageSummary'), CoverageSummaryType)
Namespace.addCategoryObject('elementBinding', CoverageSummary.name().localName(), CoverageSummary)

GridCS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridCS'), pyxb.binding.datatypes.anyURI, documentation=u'Association to the (Cartesian) grid coordinate system used by this Grid CRS. In this use of a (Cartesian) grid coordinate system, the grid positions shall be in the centers of the image or other grid coverage values (not between the grid values), as specified in ISO 19123. Also, the grid point indices at the origin shall be 0, 0 (not 1,1), as specified in ISO 19123. This GridCS defaults to the most commonly used grid coordinate system, which is referenced by the URN "urn:ogc:def:cs:OGC:0.0:Grid2dSquareCS". For a GridCRS, this association is limited to a remote definition of the GridCS (not encoded in-line). ')
Namespace.addCategoryObject('elementBinding', GridCS.name().localName(), GridCS)

Coverage = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Coverage'), pyxb.bundles.opengis.ows_1_1.ReferenceGroupType, documentation=u'Complete data for one coverage, referencing each coverage file either remotely or locally in the same message. ')
Namespace.addCategoryObject('elementBinding', Coverage.name().localName(), Coverage)

Coverages = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Coverages'), CoveragesType)
Namespace.addCategoryObject('elementBinding', Coverages.name().localName(), Coverages)

AxisSubset = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AxisSubset'), CTD_ANON_6, documentation=u'List of selected Keys for this axis, to be used for selecting values in a vector range field. TBD. ')
Namespace.addCategoryObject('elementBinding', AxisSubset.name().localName(), AxisSubset)

GetCapabilities = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetCapabilities'), CTD_ANON_8, documentation=u'Request to a WCS server to perform the GetCapabilities operation. This operation allows a client to retrieve a Capabilities XML document providing metadata for the specific WCS server. In this XML encoding, no "request" parameter is included, since the element name specifies the specific operation. ')
Namespace.addCategoryObject('elementBinding', GetCapabilities.name().localName(), GetCapabilities)

Capabilities = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Capabilities'), CTD_ANON_9, documentation=u'XML encoded WCS GetCapabilities operation response. The Capabilities document provides clients with service metadata about a specific service instance, including metadata about the coverages served. If the server does not implement the updateSequence parameter, the server shall always return the Capabilities document, without the updateSequence parameter. When the server implements the updateSequence parameter and the GetCapabilities operation request included the updateSequence parameter with the current value, the server shall return this element with only the "version" and "updateSequence" attributes. Otherwise, all optional sections shall be included or not depending on the actual value of the Contents parameter in the GetCapabilities operation request. ')
Namespace.addCategoryObject('elementBinding', Capabilities.name().localName(), Capabilities)



RangeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Field'), FieldType, scope=RangeType, documentation=u'Unordered list of the Fields in the Range of a coverage. '))
RangeType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(RangeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Field')), min_occurs=1, max_occurs=None)
    )
RangeType._ContentModel = pyxb.binding.content.ParticleModel(RangeType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Key'), IdentifierType, scope=CTD_ANON, documentation=u'Valid key value for this axis. There will normally be more than one key value for an axis, but one is allowed for special circumstances. '))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Key')), min_occurs=1, max_occurs=None)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InterpolationMethod'), InterpolationMethodType, scope=CTD_ANON_, documentation=u'Unordered list of identifiers of all other supported spatial interpolation methods. '))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Default'), pyxb.binding.datatypes.string, scope=CTD_ANON_, documentation=u'Identifier of interpolation method that will be used if the client does not specify one. '))
CTD_ANON_._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'InterpolationMethod')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Default')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=1, max_occurs=1)



SpatialDomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'Polygon'), pyxb.bundles.opengis.gml.PolygonType, scope=SpatialDomainType))

SpatialDomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ImageCRS'), ImageCRSRefType, scope=SpatialDomainType, documentation=u'Association to ImageCRS of an unrectified offered coverage. The ImageCRS shall be referenced in the SpatialDomain when the offered coverage does not have a known GridCRS. Such a coverage is always unrectified, but an unrectified coverage may have a GridCRS instead of an ImageCRS. This ImageCRS applies to this offered coverage, but does not (normally) specify its spatial resolution. The ImageCRS and the GridCRS shall be mutually exclusive in this SpatialDomain. '))

SpatialDomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'BoundingBox'), pyxb.bundles.opengis.ows_1_1.BoundingBoxType, scope=SpatialDomainType))

SpatialDomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_CoordinateOperation'), pyxb.bundles.opengis.gml.AbstractCoordinateOperationType, abstract=pyxb.binding.datatypes.boolean(1), scope=SpatialDomainType))

SpatialDomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridCRS'), GridCrsType, scope=SpatialDomainType))
SpatialDomainType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SpatialDomainType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'BoundingBox')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(SpatialDomainType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'GridCRS')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SpatialDomainType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_CoordinateOperation')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SpatialDomainType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ImageCRS')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SpatialDomainType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'Polygon')), min_occurs=0L, max_occurs=None)
    )
SpatialDomainType._ContentModel = pyxb.binding.content.ParticleModel(SpatialDomainType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CoverageSummary'), CoverageSummaryType, scope=CTD_ANON_2))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SupportedFormat'), pyxb.bundles.opengis.ows_1_1.MimeType, scope=CTD_ANON_2, documentation=u'Unordered list of identifiers of formats in which GetCoverage operation response may be encoded. This list of SupportedFormats shall be the union of all of the supported formats in all of the nested CoverageSummaries. Servers should include this list since it reduces the work clients need to do to determine that they can interoperate with the server. There may be a dependency of SupportedCRS on SupportedFormat, as described in clause 10.3.5. The full list of formats supported by a coverage shall be the union of the CoverageSummary\u2019s own SupportedFormats and those supported by all its ancestor CoverageSummaries. '))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OtherSource'), pyxb.bundles.opengis.ows_1_1.OnlineResourceType, scope=CTD_ANON_2, documentation=u'Unordered list of references to other sources of coverage metadata. This list shall be included unless one or more CoverageSummaries are included. '))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SupportedCRS'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_2, documentation=u'Unordered list of references to GridBaseCRSs in which GetCoverage operation requests and responses may be expressed. This list of SupportedCRSs shall be the union of all of the supported CRSs in all of the nested CoverageSummaries. Servers should include this list since it reduces the work clients need to do to determine that they can interoperate with the server. There may be a dependency of SupportedCRS on SupportedFormat, as described in Subclause 10.3.5. The full list of GridBaseCRSs supported by a coverage shall be the union of the CoverageSummary\u2019s own SupportedCRSs and those supported by all its ancestor CoverageSummaries. This full list shall be an exact copy of the equivalent parameters in the CoverageDescription, and shall include zero or more SupportedCRS elements. '))
CTD_ANON_2._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'CoverageSummary')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SupportedCRS')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SupportedFormat')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'OtherSource')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_2._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel, min_occurs=1, max_occurs=1)



CoverageSummaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SupportedFormat'), pyxb.bundles.opengis.ows_1_1.MimeType, scope=CoverageSummaryType, documentation=u'Unordered list of identifiers of formats in which GetCoverage operation responses may be encoded. These formats shall also apply to all lower-level CoverageSummaries under this CoverageSummary, in addition to any other formats identified. When included in a CoverageSummary with an Identifier, this list, including all values inherited from ancestor coverages, shall be an exact copy of the list of SupportedFormat parameters in the corresponding CoverageDescription. Each CoverageSummary shall list or inherit at least one SupportedFormat. '))

CoverageSummaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Metadata'), pyxb.bundles.opengis.ows_1_1.MetadataType, scope=CoverageSummaryType))

CoverageSummaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), IdentifierType, scope=CoverageSummaryType))

CoverageSummaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CoverageSummary'), CoverageSummaryType, scope=CoverageSummaryType))

CoverageSummaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SupportedCRS'), pyxb.binding.datatypes.anyURI, scope=CoverageSummaryType, documentation=u'Unordered list of references to CRSs that may be referenced as a GridBaseCRS of a GridCRS in the Output part of a GetCoverage request. These CRSs shall also apply to all lower-level CoverageSummaries under this CoverageSummary, in addition to any other CRSs referenced. When included in a CoverageSummary with an Identifier, this list, including all values inherited from ancestor coverages, shall be an exact copy of the list of SupportedCRS parameters in the corresponding CoverageDescription. Each CoverageSummary shall list or inherit at least one SupportedCRS. '))

CoverageSummaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'WGS84BoundingBox'), pyxb.bundles.opengis.ows_1_1.WGS84BoundingBoxType, scope=CoverageSummaryType))
CoverageSummaryType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CoverageSummaryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Title')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CoverageSummaryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Abstract')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CoverageSummaryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Keywords')), min_occurs=0L, max_occurs=None)
    )
CoverageSummaryType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CoverageSummaryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'CoverageSummary')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(CoverageSummaryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Identifier')), min_occurs=0L, max_occurs=1)
    )
CoverageSummaryType._GroupModel_4 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CoverageSummaryType._GroupModel_5, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CoverageSummaryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Identifier')), min_occurs=1, max_occurs=1)
    )
CoverageSummaryType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CoverageSummaryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Metadata')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CoverageSummaryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'WGS84BoundingBox')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CoverageSummaryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SupportedCRS')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CoverageSummaryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SupportedFormat')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CoverageSummaryType._GroupModel_4, min_occurs=1, max_occurs=1)
    )
CoverageSummaryType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CoverageSummaryType._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CoverageSummaryType._GroupModel_3, min_occurs=1, max_occurs=1)
    )
CoverageSummaryType._ContentModel = pyxb.binding.content.ParticleModel(CoverageSummaryType._GroupModel_, min_occurs=1, max_occurs=1)



ImageCRSRefType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'ImageCRS'), pyxb.bundles.opengis.gml.ImageCRSType, scope=ImageCRSRefType))
ImageCRSRefType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ImageCRSRefType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'ImageCRS')), min_occurs=0L, max_occurs=1)
    )
ImageCRSRefType._ContentModel = pyxb.binding.content.ParticleModel(ImageCRSRefType._GroupModel, min_occurs=1, max_occurs=1)



TimeSequenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimePeriod'), TimePeriodType, scope=TimeSequenceType))

TimeSequenceType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'timePosition'), pyxb.bundles.opengis.gml.TimePositionType, scope=TimeSequenceType, documentation=u'Direct representation of a temporal position'))
TimeSequenceType._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(TimeSequenceType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'timePosition')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimeSequenceType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimePeriod')), min_occurs=1, max_occurs=1)
    )
TimeSequenceType._ContentModel = pyxb.binding.content.ParticleModel(TimeSequenceType._GroupModel, min_occurs=1, max_occurs=None)



FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Axis'), AxisType, scope=FieldType, documentation=u'Unordered list of the axes in a vector field for which there are Field values. This list shall be included when this Field has a vector of values. Notice that the axes can be listed here in any order; however, the axis order listed here shall be used in the KVP encoding of a GetCoverage operation request. '))

FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Definition'), pyxb.bundles.opengis.ows_1_1.UnNamedDomainType, scope=FieldType, documentation=u'Further definition of this field, including meaning, units, etc. In this Definition, the AllowedValues should be used to encode the extent of possible values for this field, excluding the Null Value. If the range is not known, AnyValue should be used. '))

FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NullValue'), pyxb.bundles.opengis.ows_1_1.CodeType, scope=FieldType, documentation=u'Unordered list of the values used when valid Field values are not available for whatever reason. The coverage encoding itself may specify a fixed value for null (e.g. \u201c\u201399999\u201d or \u201cN/A\u201d), but often the choice is up to the provider and must be communicated to the client outside the coverage itself. Each null value shall be encoded as a string. The optional codeSpace attribute can reference a definition of the reason why this value is null. '))

FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), IdentifierType, scope=FieldType))

FieldType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InterpolationMethods'), CTD_ANON_, scope=FieldType, documentation=u'List of the interpolation method(s) that may be used when continuous grid coverage resampling is needed. '))
FieldType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FieldType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Title')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(FieldType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Abstract')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(FieldType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Keywords')), min_occurs=0L, max_occurs=None)
    )
FieldType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Identifier')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Definition')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'NullValue')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'InterpolationMethods')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(FieldType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Axis')), min_occurs=0L, max_occurs=None)
    )
FieldType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FieldType._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(FieldType._GroupModel_3, min_occurs=1, max_occurs=1)
    )
FieldType._ContentModel = pyxb.binding.content.ParticleModel(FieldType._GroupModel_, min_occurs=1, max_occurs=1)



CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), IdentifierType, scope=CTD_ANON_3))
CTD_ANON_3._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Identifier')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_3._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_3._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'CoverageDescription'), CoverageDescriptionType, scope=CTD_ANON_4))
CTD_ANON_4._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'CoverageDescription')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_4._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel, min_occurs=1, max_occurs=1)



RangeSubsetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FieldSubset'), CTD_ANON_7, scope=RangeSubsetType, documentation=u'Unordered list of one or more desired subsets of range fields. TBD. '))
RangeSubsetType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(RangeSubsetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'FieldSubset')), min_occurs=1, max_occurs=None)
    )
RangeSubsetType._ContentModel = pyxb.binding.content.ParticleModel(RangeSubsetType._GroupModel, min_occurs=1, max_occurs=1)



CoverageDescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Metadata'), pyxb.bundles.opengis.ows_1_1.MetadataType, scope=CoverageDescriptionType))

CoverageDescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), IdentifierType, scope=CoverageDescriptionType))

CoverageDescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SupportedFormat'), pyxb.bundles.opengis.ows_1_1.MimeType, scope=CoverageDescriptionType, documentation=u'Unordered list of identifiers of all the formats in which GetCoverage operation responses can be encoded for this coverage. '))

CoverageDescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SupportedCRS'), pyxb.binding.datatypes.anyURI, scope=CoverageDescriptionType, documentation=u'Unordered list of references to all the coordinate reference systems that may be referenced as the GridBaseCRS of a GridCRS specified in the Output part of a GetCoverage operation request. The GridBaseCRS of the GridCRS of a georectified offered coverage shall be listed as a SupportedCRS. An ImageCRS for an unrectified offered image shall be listed as a SupportedCRS, so that it may be referenced as the GridBaseCRS of a GridCRS. This ImageCRS shall be the ImageCRS of that unrectified offered image, or the ImageCRS that is referenced as the GridBaseCRS of the GridCRS that is used by that unrectified offered image  In addition, the GetCoverage operation output may be expressed in the ImageCRS or GridCRS of an unrectified offered coverage, instead of in a specified GridCRS. These Supported\xacCRSs can also be referenced in the BoundingBox in the DomainSubset part of a GetCoverage request. '))

CoverageDescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Range'), RangeType, scope=CoverageDescriptionType))

CoverageDescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Domain'), CoverageDomainType, scope=CoverageDescriptionType))
CoverageDescriptionType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CoverageDescriptionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Title')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CoverageDescriptionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Abstract')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CoverageDescriptionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Keywords')), min_occurs=0L, max_occurs=None)
    )
CoverageDescriptionType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CoverageDescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Identifier')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CoverageDescriptionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Metadata')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CoverageDescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Domain')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CoverageDescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Range')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CoverageDescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SupportedCRS')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CoverageDescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SupportedFormat')), min_occurs=1, max_occurs=None)
    )
CoverageDescriptionType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CoverageDescriptionType._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CoverageDescriptionType._GroupModel_3, min_occurs=1, max_occurs=1)
    )
CoverageDescriptionType._ContentModel = pyxb.binding.content.ParticleModel(CoverageDescriptionType._GroupModel_, min_occurs=1, max_occurs=1)



CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Identifier'), pyxb.bundles.opengis.ows_1_1.CodeType, scope=CTD_ANON_5, documentation=u'Unique identifier or name of this dataset. '))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Output'), OutputType, scope=CTD_ANON_5))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DomainSubset'), DomainSubsetType, scope=CTD_ANON_5))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'RangeSubset'), RangeSubsetType, scope=CTD_ANON_5, documentation=u"Optional selection of a subset of the coverage's range. "))
CTD_ANON_5._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Identifier')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'DomainSubset')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'RangeSubset')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Output')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_5._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_5._GroupModel, min_occurs=1, max_occurs=1)



TimePeriodType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TimeResolution'), TimeDurationType, scope=TimePeriodType))

TimePeriodType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'EndPosition'), pyxb.bundles.opengis.gml.TimePositionType, scope=TimePeriodType))

TimePeriodType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BeginPosition'), pyxb.bundles.opengis.gml.TimePositionType, scope=TimePeriodType))
TimePeriodType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TimePeriodType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'BeginPosition')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimePeriodType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'EndPosition')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TimePeriodType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TimeResolution')), min_occurs=0L, max_occurs=1)
    )
TimePeriodType._ContentModel = pyxb.binding.content.ParticleModel(TimePeriodType._GroupModel, min_occurs=1, max_occurs=1)



DomainSubsetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'BoundingBox'), pyxb.bundles.opengis.ows_1_1.BoundingBoxType, scope=DomainSubsetType))

DomainSubsetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TemporalSubset'), TimeSequenceType, scope=DomainSubsetType, documentation=u'Definition of subset of coverage temporal domain. '))
DomainSubsetType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DomainSubsetType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'BoundingBox')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DomainSubsetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TemporalSubset')), min_occurs=0L, max_occurs=1)
    )
DomainSubsetType._ContentModel = pyxb.binding.content.ParticleModel(DomainSubsetType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), IdentifierType, scope=CTD_ANON_6))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Key'), IdentifierType, scope=CTD_ANON_6, documentation=u'Unordered list of (at least one) Key, to be used for selecting values in a range vector field. The Keys within this list shall be unique. '))
CTD_ANON_6._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Identifier')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Key')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_6._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_6._GroupModel, min_occurs=1, max_occurs=1)



GridCrsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridType'), pyxb.binding.datatypes.anyURI, scope=GridCrsType, documentation=u'Association to the OperationMethod used to define this Grid CRS. This association defaults to an association to the most commonly used method, which is referenced by the URN "urn:ogc:def:method:WCS:1.1:2dSimpleGrid". For a GridCRS, this association is limited to a remote definition of a grid definition Method (not encoded in-line) that encodes a variation on the method implied by the CV_RectifiedGrid class in ISO 19123, without the inheritance from CV_Grid. '))

GridCrsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'srsName'), pyxb.bundles.opengis.gml.CodeType, scope=GridCrsType, documentation=u'The name by which this reference system is identified.'))

GridCrsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridCS'), pyxb.binding.datatypes.anyURI, scope=GridCrsType, documentation=u'Association to the (Cartesian) grid coordinate system used by this Grid CRS. In this use of a (Cartesian) grid coordinate system, the grid positions shall be in the centers of the image or other grid coverage values (not between the grid values), as specified in ISO 19123. Also, the grid point indices at the origin shall be 0, 0 (not 1,1), as specified in ISO 19123. This GridCS defaults to the most commonly used grid coordinate system, which is referenced by the URN "urn:ogc:def:cs:OGC:0.0:Grid2dSquareCS". For a GridCRS, this association is limited to a remote definition of the GridCS (not encoded in-line). '))

GridCrsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridOrigin'), pyxb.bundles.opengis.gml.doubleList, scope=GridCrsType, documentation=u'Coordinates of the grid origin position in the GridBaseCRS of this GridCRS. This origin defaults be the most commonly used origin in a GridCRS used in the output part of a GetCapabilities operation request, namely "0 0". This element is adapted from gml:pos. '))

GridCrsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridBaseCRS'), pyxb.binding.datatypes.anyURI, scope=GridCrsType, documentation=u'Association to the coordinate reference system (CRS) in which this Grid CRS is specified. A GridCRS can use any type of GridBaseCRS, including GeographicCRS, ProjectedCRS, ImageCRS, or a different GridCRS. For a GridCRS, this association is limited to a remote definition of the GridBaseCRS (not encoded in-line). '))

GridCrsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridOffsets'), pyxb.bundles.opengis.gml.doubleList, scope=GridCrsType, documentation=u'Two or more grid position offsets from the grid origin in the GridBaseCRS of this GridCRS. Example: For the grid2dIn2dCRS OperationMethod, this Offsets element shall contain four values, the first two values shall specify the grid offset for the first grid axis in the 2D base CRS, and the second pair of values shall specify the grid offset for the second grid axis. In this case, the middle two values are zero for un-rotated and un-skewed grids. '))
GridCrsType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GridCrsType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'srsName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GridCrsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'GridBaseCRS')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(GridCrsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'GridType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GridCrsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'GridOrigin')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GridCrsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'GridOffsets')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(GridCrsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'GridCS')), min_occurs=0L, max_occurs=1)
    )
GridCrsType._ContentModel = pyxb.binding.content.ParticleModel(GridCrsType._GroupModel, min_occurs=1, max_occurs=1)



OutputType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GridCRS'), GridCrsType, scope=OutputType))
OutputType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(OutputType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'GridCRS')), min_occurs=0L, max_occurs=1)
    )
OutputType._ContentModel = pyxb.binding.content.ParticleModel(OutputType._GroupModel, min_occurs=1, max_occurs=1)



AxisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'UOM'), pyxb.bundles.opengis.ows_1_1.DomainMetadataType, scope=AxisType, documentation=u'Definition of the unit of measure of this set of values. In this case, the xlink:href attribute can reference a URN for a well-known unit of measure (uom). For example, such a URN could be a UOM identification URN defined in the "ogc" URN namespace. '))

AxisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'DataType'), pyxb.bundles.opengis.ows_1_1.DomainMetadataType, scope=AxisType, documentation=u'Definition of the data type of this set of values. In this case, the xlink:href attribute can reference a URN for a well-known data type. For example, such a URN could be a data type identification URN defined in the "ogc" URN namespace. '))

AxisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'ReferenceSystem'), pyxb.bundles.opengis.ows_1_1.DomainMetadataType, scope=AxisType, documentation=u'Definition of the reference system used by this set of values, including the unit of measure whenever applicable (as is normal). In this case, the xlink:href attribute can reference a URN for a well-known reference system, such as for a coordinate reference system (CRS). For example, such a URN could be a CRS identification URN defined in the "ogc" URN namespace. '))

AxisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AvailableKeys'), CTD_ANON, scope=AxisType, documentation=u'List of all the available (valid) key values for this axis. For numeric keys, signed values should be ordered from negative infinity to positive infinity. '))

AxisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Metadata'), pyxb.bundles.opengis.ows_1_1.MetadataType, scope=AxisType))

AxisType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Meaning'), pyxb.bundles.opengis.ows_1_1.DomainMetadataType, scope=AxisType, documentation=u'Definition of the meaning or semantics of this set of values. This Meaning can provide more specific, complete, precise, machine accessible, and machine understandable semantics about this quantity, relative to other available semantic information. For example, other semantic information is often provided in "documentation" elements in XML Schemas or "description" elements in GML objects. '))
AxisType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AxisType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Title')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AxisType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Abstract')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AxisType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Keywords')), min_occurs=0L, max_occurs=None)
    )
AxisType._GroupModel_4 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(AxisType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'UOM')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AxisType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'ReferenceSystem')), min_occurs=1, max_occurs=1)
    )
AxisType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AxisType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AvailableKeys')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AxisType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Meaning')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AxisType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'DataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AxisType._GroupModel_4, min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AxisType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Metadata')), min_occurs=0L, max_occurs=None)
    )
AxisType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AxisType._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(AxisType._GroupModel_3, min_occurs=1, max_occurs=1)
    )
AxisType._ContentModel = pyxb.binding.content.ParticleModel(AxisType._GroupModel_, min_occurs=1, max_occurs=1)



CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AxisSubset'), CTD_ANON_6, scope=CTD_ANON_7, documentation=u'List of selected Keys for this axis, to be used for selecting values in a vector range field. TBD. '))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InterpolationType'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, documentation=u'Optional identifier of the spatial interpolation type to be applied to this range field. This interpolation type shall be one that is identified for this Field in the CoverageDescription. When this parameter is omitted, the interpolation method used shall be the default method specified for this Field, if any. '))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Identifier'), pyxb.bundles.opengis.ows_1_1.CodeType, scope=CTD_ANON_7, documentation=u'Unique identifier or name of this dataset. '))
CTD_ANON_7._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Identifier')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'InterpolationType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AxisSubset')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_7._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_7._GroupModel, min_occurs=1, max_occurs=1)



CoveragesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Coverage'), pyxb.bundles.opengis.ows_1_1.ReferenceGroupType, scope=CoveragesType, documentation=u'Complete data for one coverage, referencing each coverage file either remotely or locally in the same message. '))
CoveragesType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CoveragesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Coverage')), min_occurs=1, max_occurs=None)
    )
CoveragesType._ContentModel = pyxb.binding.content.ParticleModel(CoveragesType._GroupModel, min_occurs=1, max_occurs=1)


CTD_ANON_8._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'AcceptVersions')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Sections')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'AcceptFormats')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_8._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_8._GroupModel_, min_occurs=1, max_occurs=1)



CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Contents'), CTD_ANON_2, scope=CTD_ANON_9, documentation=u'Contents section of WCS service metadata (or Capabilities) XML document. For the WCS, these contents are brief metadata about the coverages available from this server, or a reference to another source from which this metadata is available. '))
CTD_ANON_9._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'ServiceIdentification')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'ServiceProvider')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'OperationsMetadata')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_9._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Contents')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_9._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_9._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._GroupModel_3, min_occurs=1, max_occurs=1)
    )
CTD_ANON_9._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_9._GroupModel_, min_occurs=1, max_occurs=1)



CoverageDomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SpatialDomain'), SpatialDomainType, scope=CoverageDomainType))

CoverageDomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TemporalDomain'), TimeSequenceType, scope=CoverageDomainType, documentation=u'Definition of the temporal domain of a coverage, the times for which valid data are available. The times should to be ordered from the oldest to the newest. '))
CoverageDomainType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CoverageDomainType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SpatialDomain')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CoverageDomainType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TemporalDomain')), min_occurs=0L, max_occurs=1)
    )
CoverageDomainType._ContentModel = pyxb.binding.content.ParticleModel(CoverageDomainType._GroupModel, min_occurs=1, max_occurs=1)

Transformation._setSubstitutionGroup(pyxb.bundles.opengis.gml.CoordinateOperation)

Coverage._setSubstitutionGroup(pyxb.bundles.opengis.ows_1_1.ReferenceGroup)
