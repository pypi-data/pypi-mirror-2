# ./pyxb/bundles/opengis/raw/ows.py
# PyXB bindings for NM:0eaa86ae32cb3080e2342e92c025f322bb8eca15
# Generated 2011-09-09 14:19:04.414326 by PyXB version 1.1.3
# Namespace http://www.opengis.net/ows

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:94c2cdbe-db18-11e0-bdcb-001fbc013adc')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.opengis.misc.xlinks

Namespace = pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows', create_if_missing=True)
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


# List SimpleTypeDefinition
# superclasses pyxb.binding.datatypes.anySimpleType
class PositionType (pyxb.binding.basis.STD_list):

    """Position instances hold the coordinates of a position in a coordinate reference system (CRS) referenced by the related "crs" attribute or elsewhere. For an angular coordinate axis that is physically continuous for multiple revolutions, but whose recorded values can be discontinuous, special conditions apply when the bounding box is continuous across the value discontinuity:
a)  If the bounding box is continuous clear around this angular axis, then ordinate values of minus and plus infinity shall be used.
b)  If the bounding box is continuous across the value discontinuity but is not continuous clear around this angular axis, then some non-normal value can be used if specified for a specific OWS use of the BoundingBoxType. For more information, see Subclauses 10.2.5 and C.13. This type is adapted from DirectPositionType and doubleList of GML 3.1. The adaptations include omission of all the attributes, since the needed information is included in the BoundingBoxType. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PositionType')
    _Documentation = u'Position instances hold the coordinates of a position in a coordinate reference system (CRS) referenced by the related "crs" attribute or elsewhere. For an angular coordinate axis that is physically continuous for multiple revolutions, but whose recorded values can be discontinuous, special conditions apply when the bounding box is continuous across the value discontinuity:\na)  If the bounding box is continuous clear around this angular axis, then ordinate values of minus and plus infinity shall be used.\nb)  If the bounding box is continuous across the value discontinuity but is not continuous clear around this angular axis, then some non-normal value can be used if specified for a specific OWS use of the BoundingBoxType. For more information, see Subclauses 10.2.5 and C.13. This type is adapted from DirectPositionType and doubleList of GML 3.1. The adaptations include omission of all the attributes, since the needed information is included in the BoundingBoxType. '

    _ItemType = pyxb.binding.datatypes.double
PositionType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'PositionType', PositionType)

# List SimpleTypeDefinition
# superclasses PositionType
class PositionType2D (pyxb.binding.basis.STD_list):

    """Two-dimensional position instances hold the longitude and latitude coordinates of a position in the 2D WGS 84 coordinate reference system. The longitude value shall be listed first, followed by the latitude value, both in decimal degrees. Latitude values shall range from -90 to +90 degrees, and longitude values shall normally range from -180 to +180 degrees. For the longitude axis, special conditions apply when the bounding box is continuous across the +/- 180 degrees meridian longitude value discontinuity:
a)  If the bounding box is continuous clear around the Earth, then longitude values of minus and plus infinity shall be used.
b)  If the bounding box is continuous across the value discontinuity but is not continuous clear around the Earth, then some non-normal value can be used if specified for a specific OWS use of the WGS84BoundingBoxType. For more information, see Subclauses 10.4.5 and C.13. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PositionType2D')
    _Documentation = u'Two-dimensional position instances hold the longitude and latitude coordinates of a position in the 2D WGS 84 coordinate reference system. The longitude value shall be listed first, followed by the latitude value, both in decimal degrees. Latitude values shall range from -90 to +90 degrees, and longitude values shall normally range from -180 to +180 degrees. For the longitude axis, special conditions apply when the bounding box is continuous across the +/- 180 degrees meridian longitude value discontinuity:\na)  If the bounding box is continuous clear around the Earth, then longitude values of minus and plus infinity shall be used.\nb)  If the bounding box is continuous across the value discontinuity but is not continuous clear around the Earth, then some non-normal value can be used if specified for a specific OWS use of the WGS84BoundingBoxType. For more information, see Subclauses 10.4.5 and C.13. '

    _ItemType = pyxb.binding.datatypes.double
PositionType2D._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(2L))
PositionType2D._InitializeFacetMap(PositionType2D._CF_length)
Namespace.addCategoryObject('typeBinding', u'PositionType2D', PositionType2D)

# Atomic SimpleTypeDefinition
class MimeType (pyxb.binding.datatypes.string):

    """XML encoded identifier of a standard MIME type, possibly a parameterized MIME type. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MimeType')
    _Documentation = u'XML encoded identifier of a standard MIME type, possibly a parameterized MIME type. '
MimeType._CF_pattern = pyxb.binding.facets.CF_pattern()
MimeType._CF_pattern.addPattern(pattern=u'(application|audio|image|text|video|message|multipart|model)/.+(;\\s*.+=.+)*')
MimeType._InitializeFacetMap(MimeType._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'MimeType', MimeType)

# Atomic SimpleTypeDefinition
class VersionType (pyxb.binding.datatypes.string):

    """Specification version for OWS operation. The string value shall contain one x.y.z "version" value (e.g., "2.1.3"). A version number shall contain three non-negative integers separated by decimal points, in the form "x.y.z". The integers y and z shall not exceed 99. Each version shall be for the Implementation Specification (document) and the associated XML Schemas to which requested operations will conform. An Implementation Specification version normally specifies XML Schemas against which an XML encoded operation response must conform and should be validated. See Version negotiation subclause for more information. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'VersionType')
    _Documentation = u'Specification version for OWS operation. The string value shall contain one x.y.z "version" value (e.g., "2.1.3"). A version number shall contain three non-negative integers separated by decimal points, in the form "x.y.z". The integers y and z shall not exceed 99. Each version shall be for the Implementation Specification (document) and the associated XML Schemas to which requested operations will conform. An Implementation Specification version normally specifies XML Schemas against which an XML encoded operation response must conform and should be validated. See Version negotiation subclause for more information. '
VersionType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'VersionType', VersionType)

# Atomic SimpleTypeDefinition
class UpdateSequenceType (pyxb.binding.datatypes.string):

    """Service metadata document version, having values that are "increased" whenever any change is made in service metadata document. Values are selected by each server, and are always opaque to clients. See updateSequence parameter use subclause for more information. """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'UpdateSequenceType')
    _Documentation = u'Service metadata document version, having values that are "increased" whenever any change is made in service metadata document. Values are selected by each server, and are always opaque to clients. See updateSequence parameter use subclause for more information. '
UpdateSequenceType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'UpdateSequenceType', UpdateSequenceType)

# Atomic SimpleTypeDefinition
class ServiceType (pyxb.binding.datatypes.string):

    """Service type identifier, where the string value is the OWS type abbreviation, such as "WMS" or "WFS". """

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ServiceType')
    _Documentation = u'Service type identifier, where the string value is the OWS type abbreviation, such as "WMS" or "WFS". '
ServiceType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'ServiceType', ServiceType)

# Complex type CodeType with content type SIMPLE
class CodeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CodeType')
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute codeSpace uses Python identifier codeSpace
    __codeSpace = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'codeSpace'), 'codeSpace', '__httpwww_opengis_netows_CodeType_codeSpace', pyxb.binding.datatypes.anyURI)
    
    codeSpace = property(__codeSpace.value, __codeSpace.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __codeSpace.name() : __codeSpace
    }
Namespace.addCategoryObject('typeBinding', u'CodeType', CodeType)


# Complex type BoundingBoxType with content type ELEMENT_ONLY
class BoundingBoxType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BoundingBoxType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}UpperCorner uses Python identifier UpperCorner
    __UpperCorner = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'UpperCorner'), 'UpperCorner', '__httpwww_opengis_netows_BoundingBoxType_httpwww_opengis_netowsUpperCorner', False)

    
    UpperCorner = property(__UpperCorner.value, __UpperCorner.set, None, u'Position of the bounding box corner at which the value of each coordinate normally is the algebraic maximum within this bounding box. In some cases, this position is normally displayed at the bottom, such as the bottom right for some image coordinates. For more information, see Subclauses 10.2.5 and C.13. ')

    
    # Element {http://www.opengis.net/ows}LowerCorner uses Python identifier LowerCorner
    __LowerCorner = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'LowerCorner'), 'LowerCorner', '__httpwww_opengis_netows_BoundingBoxType_httpwww_opengis_netowsLowerCorner', False)

    
    LowerCorner = property(__LowerCorner.value, __LowerCorner.set, None, u'Position of the bounding box corner at which the value of each coordinate normally is the algebraic minimum within this bounding box. In some cases, this position is normally displayed at the top, such as the top left for some image coordinates. For more information, see Subclauses 10.2.5 and C.13. ')

    
    # Attribute dimensions uses Python identifier dimensions
    __dimensions = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dimensions'), 'dimensions', '__httpwww_opengis_netows_BoundingBoxType_dimensions', pyxb.binding.datatypes.positiveInteger)
    
    dimensions = property(__dimensions.value, __dimensions.set, None, u'The number of dimensions in this CRS (the length of a coordinate sequence in this use of the PositionType). This number is specified by the CRS definition, but can also be specified here. ')

    
    # Attribute crs uses Python identifier crs
    __crs = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'crs'), 'crs', '__httpwww_opengis_netows_BoundingBoxType_crs', pyxb.binding.datatypes.anyURI)
    
    crs = property(__crs.value, __crs.set, None, u'Usually references the definition of a CRS, as specified in [OGC Topic 2]. Such a CRS definition can be XML encoded using the gml:CoordinateReferenceSystemType in [GML 3.1]. For well known references, it is not required that a CRS definition exist at the location the URI points to. If no anyURI value is included, the applicable CRS must be either:\na)\tSpecified outside the bounding box, but inside a data structure that includes this bounding box, as specified for a specific OWS use of this bounding box type.\nb)\tFixed and specified in the Implementation Specification for a specific OWS use of the bounding box type. ')


    _ElementMap = {
        __UpperCorner.name() : __UpperCorner,
        __LowerCorner.name() : __LowerCorner
    }
    _AttributeMap = {
        __dimensions.name() : __dimensions,
        __crs.name() : __crs
    }
Namespace.addCategoryObject('typeBinding', u'BoundingBoxType', BoundingBoxType)


# Complex type MetadataType with content type ELEMENT_ONLY
class MetadataType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MetadataType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}AbstractMetaData uses Python identifier AbstractMetaData
    __AbstractMetaData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AbstractMetaData'), 'AbstractMetaData', '__httpwww_opengis_netows_MetadataType_httpwww_opengis_netowsAbstractMetaData', False)

    
    AbstractMetaData = property(__AbstractMetaData.value, __AbstractMetaData.set, None, u'Abstract element containing more metadata about the element that includes the containing "metadata" element. A specific server implementation, or an Implementation Specification, can define concrete elements in the AbstractMetaData substitution group. ')

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netows_MetadataType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute about uses Python identifier about
    __about = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'about'), 'about', '__httpwww_opengis_netows_MetadataType_about', pyxb.binding.datatypes.anyURI)
    
    about = property(__about.value, __about.set, None, u'Optional reference to the aspect of the element which includes this "metadata" element that this metadata provides more information about. ')

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netows_MetadataType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netows_MetadataType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netows_MetadataType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netows_MetadataType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netows_MetadataType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netows_MetadataType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)


    _ElementMap = {
        __AbstractMetaData.name() : __AbstractMetaData
    }
    _AttributeMap = {
        __type.name() : __type,
        __about.name() : __about,
        __arcrole.name() : __arcrole,
        __show.name() : __show,
        __title.name() : __title,
        __actuate.name() : __actuate,
        __role.name() : __role,
        __href.name() : __href
    }
Namespace.addCategoryObject('typeBinding', u'MetadataType', MetadataType)


# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}ProviderSite uses Python identifier ProviderSite
    __ProviderSite = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ProviderSite'), 'ProviderSite', '__httpwww_opengis_netows_CTD_ANON_httpwww_opengis_netowsProviderSite', False)

    
    ProviderSite = property(__ProviderSite.value, __ProviderSite.set, None, u'Reference to the most relevant web site of the service provider. ')

    
    # Element {http://www.opengis.net/ows}ServiceContact uses Python identifier ServiceContact
    __ServiceContact = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ServiceContact'), 'ServiceContact', '__httpwww_opengis_netows_CTD_ANON_httpwww_opengis_netowsServiceContact', False)

    
    ServiceContact = property(__ServiceContact.value, __ServiceContact.set, None, u'Information for contacting the service provider. The OnlineResource element within this ServiceContact element should not be used to reference a web site of the service provider. ')

    
    # Element {http://www.opengis.net/ows}ProviderName uses Python identifier ProviderName
    __ProviderName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ProviderName'), 'ProviderName', '__httpwww_opengis_netows_CTD_ANON_httpwww_opengis_netowsProviderName', False)

    
    ProviderName = property(__ProviderName.value, __ProviderName.set, None, u'A unique identifier for the service provider organization. ')


    _ElementMap = {
        __ProviderSite.name() : __ProviderSite,
        __ServiceContact.name() : __ServiceContact,
        __ProviderName.name() : __ProviderName
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
    
    # Element {http://www.opengis.net/ows}ExtendedCapabilities uses Python identifier ExtendedCapabilities
    __ExtendedCapabilities = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ExtendedCapabilities'), 'ExtendedCapabilities', '__httpwww_opengis_netows_CTD_ANON__httpwww_opengis_netowsExtendedCapabilities', False)

    
    ExtendedCapabilities = property(__ExtendedCapabilities.value, __ExtendedCapabilities.set, None, u'Individual software vendors and servers can use this element to provide metadata about any additional server abilities. ')

    
    # Element {http://www.opengis.net/ows}Constraint uses Python identifier Constraint
    __Constraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Constraint'), 'Constraint', '__httpwww_opengis_netows_CTD_ANON__httpwww_opengis_netowsConstraint', True)

    
    Constraint = property(__Constraint.value, __Constraint.set, None, u'Optional unordered list of valid domain constraints on non-parameter quantities that each apply to this server. The list of required and optional constraints shall be specified in the Implementation Specification for this service. ')

    
    # Element {http://www.opengis.net/ows}Parameter uses Python identifier Parameter
    __Parameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Parameter'), 'Parameter', '__httpwww_opengis_netows_CTD_ANON__httpwww_opengis_netowsParameter', True)

    
    Parameter = property(__Parameter.value, __Parameter.set, None, u'Optional unordered list of parameter valid domains that each apply to one or more operations which this server interface implements. The list of required and optional parameter domain limitations shall be specified in the Implementation Specification for this service. ')

    
    # Element {http://www.opengis.net/ows}Operation uses Python identifier Operation
    __Operation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Operation'), 'Operation', '__httpwww_opengis_netows_CTD_ANON__httpwww_opengis_netowsOperation', True)

    
    Operation = property(__Operation.value, __Operation.set, None, u'Metadata for one operation that this server implements. ')


    _ElementMap = {
        __ExtendedCapabilities.name() : __ExtendedCapabilities,
        __Constraint.name() : __Constraint,
        __Parameter.name() : __Parameter,
        __Operation.name() : __Operation
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_2 with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Metadata uses Python identifier Metadata
    __Metadata = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Metadata'), 'Metadata', '__httpwww_opengis_netows_CTD_ANON_2_httpwww_opengis_netowsMetadata', True)

    
    Metadata = property(__Metadata.value, __Metadata.set, None, None)

    
    # Element {http://www.opengis.net/ows}Constraint uses Python identifier Constraint
    __Constraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Constraint'), 'Constraint', '__httpwww_opengis_netows_CTD_ANON_2_httpwww_opengis_netowsConstraint', True)

    
    Constraint = property(__Constraint.value, __Constraint.set, None, u'Optional unordered list of valid domain constraints on non-parameter quantities that each apply to this operation. If one of these Constraint elements has the same "name" attribute as a Constraint element in the OperationsMetadata element, this Constraint element shall override the other one for this operation. The list of required and optional constraints for this operation shall be specified in the Implementation Specification for this service. ')

    
    # Element {http://www.opengis.net/ows}Parameter uses Python identifier Parameter
    __Parameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Parameter'), 'Parameter', '__httpwww_opengis_netows_CTD_ANON_2_httpwww_opengis_netowsParameter', True)

    
    Parameter = property(__Parameter.value, __Parameter.set, None, u'Optional unordered list of parameter domains that each apply to this operation which this server implements. If one of these Parameter elements has the same "name" attribute as a Parameter element in the OperationsMetadata element, this Parameter element shall override the other one for this operation. The list of required and optional parameter domain limitations for this operation shall be specified in the Implementation Specification for this service. ')

    
    # Element {http://www.opengis.net/ows}DCP uses Python identifier DCP
    __DCP = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'DCP'), 'DCP', '__httpwww_opengis_netows_CTD_ANON_2_httpwww_opengis_netowsDCP', True)

    
    DCP = property(__DCP.value, __DCP.set, None, u'Information for one distributed Computing Platform (DCP) supported for this operation. At present, only the HTTP DCP is defined, so this element only includes the HTTP element.\n')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_netows_CTD_ANON_2_name', pyxb.binding.datatypes.string, required=True)
    
    name = property(__name.value, __name.set, None, u'Name or identifier of this operation (request) (for example, GetCapabilities). The list of required and optional operations implemented shall be specified in the Implementation Specification for this service. ')


    _ElementMap = {
        __Metadata.name() : __Metadata,
        __Constraint.name() : __Constraint,
        __Parameter.name() : __Parameter,
        __DCP.name() : __DCP
    }
    _AttributeMap = {
        __name.name() : __name
    }



# Complex type DomainType with content type ELEMENT_ONLY
class DomainType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DomainType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Value uses Python identifier Value
    __Value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Value'), 'Value', '__httpwww_opengis_netows_DomainType_httpwww_opengis_netowsValue', True)

    
    Value = property(__Value.value, __Value.set, None, u'Unordered list of all the valid values for this parameter or other quantity. For those parameters that contain a list or sequence of values, these values shall be for individual values in the list. The allowed set of values and the allowed server restrictions on that set of values shall be specified in the Implementation Specification for this service. ')

    
    # Element {http://www.opengis.net/ows}Metadata uses Python identifier Metadata
    __Metadata = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Metadata'), 'Metadata', '__httpwww_opengis_netows_DomainType_httpwww_opengis_netowsMetadata', True)

    
    Metadata = property(__Metadata.value, __Metadata.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_netows_DomainType_name', pyxb.binding.datatypes.string, required=True)
    
    name = property(__name.value, __name.set, None, u'Name or identifier of this parameter or other quantity. ')


    _ElementMap = {
        __Value.name() : __Value,
        __Metadata.name() : __Metadata
    }
    _AttributeMap = {
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'DomainType', DomainType)


# Complex type KeywordsType with content type ELEMENT_ONLY
class KeywordsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'KeywordsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Type uses Python identifier Type
    __Type = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Type'), 'Type', '__httpwww_opengis_netows_KeywordsType_httpwww_opengis_netowsType', False)

    
    Type = property(__Type.value, __Type.set, None, None)

    
    # Element {http://www.opengis.net/ows}Keyword uses Python identifier Keyword
    __Keyword = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Keyword'), 'Keyword', '__httpwww_opengis_netows_KeywordsType_httpwww_opengis_netowsKeyword', True)

    
    Keyword = property(__Keyword.value, __Keyword.set, None, None)


    _ElementMap = {
        __Type.name() : __Type,
        __Keyword.name() : __Keyword
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'KeywordsType', KeywordsType)


# Complex type ExceptionType with content type ELEMENT_ONLY
class ExceptionType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ExceptionType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}ExceptionText uses Python identifier ExceptionText
    __ExceptionText = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ExceptionText'), 'ExceptionText', '__httpwww_opengis_netows_ExceptionType_httpwww_opengis_netowsExceptionText', True)

    
    ExceptionText = property(__ExceptionText.value, __ExceptionText.set, None, u'Ordered sequence of text strings that describe this specific exception or error. The contents of these strings are left open to definition by each server implementation. A server is strongly encouraged to include at least one ExceptionText value, to provide more information about the detected error than provided by the exceptionCode. When included, multiple ExceptionText values shall provide hierarchical information about one detected error, with the most significant information listed first. ')

    
    # Attribute locator uses Python identifier locator
    __locator = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'locator'), 'locator', '__httpwww_opengis_netows_ExceptionType_locator', pyxb.binding.datatypes.string)
    
    locator = property(__locator.value, __locator.set, None, u"When included, this locator shall indicate to the client where an exception was encountered in servicing the client's operation request. This locator should be included whenever meaningful information can be provided by the server. The contents of this locator will depend on the specific exceptionCode and OWS service, and shall be specified in the OWS Implementation Specification. ")

    
    # Attribute exceptionCode uses Python identifier exceptionCode
    __exceptionCode = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'exceptionCode'), 'exceptionCode', '__httpwww_opengis_netows_ExceptionType_exceptionCode', pyxb.binding.datatypes.string, required=True)
    
    exceptionCode = property(__exceptionCode.value, __exceptionCode.set, None, u'A code representing the type of this exception, which shall be selected from a set of exceptionCode values specified for the specific service operation and server. ')


    _ElementMap = {
        __ExceptionText.name() : __ExceptionText
    }
    _AttributeMap = {
        __locator.name() : __locator,
        __exceptionCode.name() : __exceptionCode
    }
Namespace.addCategoryObject('typeBinding', u'ExceptionType', ExceptionType)


# Complex type ContactType with content type ELEMENT_ONLY
class ContactType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ContactType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}ContactInstructions uses Python identifier ContactInstructions
    __ContactInstructions = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ContactInstructions'), 'ContactInstructions', '__httpwww_opengis_netows_ContactType_httpwww_opengis_netowsContactInstructions', False)

    
    ContactInstructions = property(__ContactInstructions.value, __ContactInstructions.set, None, u'Supplemental instructions on how or when to contact the individual or organization. ')

    
    # Element {http://www.opengis.net/ows}Address uses Python identifier Address
    __Address = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Address'), 'Address', '__httpwww_opengis_netows_ContactType_httpwww_opengis_netowsAddress', False)

    
    Address = property(__Address.value, __Address.set, None, u'Physical and email address at which the organization or individual may be contacted. ')

    
    # Element {http://www.opengis.net/ows}HoursOfService uses Python identifier HoursOfService
    __HoursOfService = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'HoursOfService'), 'HoursOfService', '__httpwww_opengis_netows_ContactType_httpwww_opengis_netowsHoursOfService', False)

    
    HoursOfService = property(__HoursOfService.value, __HoursOfService.set, None, u'Time period (including time zone) when individuals can contact the organization or individual. ')

    
    # Element {http://www.opengis.net/ows}Phone uses Python identifier Phone
    __Phone = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Phone'), 'Phone', '__httpwww_opengis_netows_ContactType_httpwww_opengis_netowsPhone', False)

    
    Phone = property(__Phone.value, __Phone.set, None, u'Telephone numbers at which the organization or individual may be contacted. ')

    
    # Element {http://www.opengis.net/ows}OnlineResource uses Python identifier OnlineResource
    __OnlineResource = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'OnlineResource'), 'OnlineResource', '__httpwww_opengis_netows_ContactType_httpwww_opengis_netowsOnlineResource', False)

    
    OnlineResource = property(__OnlineResource.value, __OnlineResource.set, None, u'On-line information that can be used to contact the individual or organization. OWS specifics: The xlink:href attribute in the xlink:simpleLink attribute group shall be used to reference this resource. Whenever practical, the xlink:href attribute with type anyURI should be a URL from which more contact information can be electronically retrieved. The xlink:title attribute with type "string" can be used to name this set of information. The other attributes in the xlink:simpleLink attribute group should not be used. ')


    _ElementMap = {
        __ContactInstructions.name() : __ContactInstructions,
        __Address.name() : __Address,
        __HoursOfService.name() : __HoursOfService,
        __Phone.name() : __Phone,
        __OnlineResource.name() : __OnlineResource
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ContactType', ContactType)


# Complex type OnlineResourceType with content type EMPTY
class OnlineResourceType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'OnlineResourceType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netows_OnlineResourceType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netows_OnlineResourceType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netows_OnlineResourceType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netows_OnlineResourceType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netows_OnlineResourceType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netows_OnlineResourceType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netows_OnlineResourceType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __href.name() : __href,
        __title.name() : __title,
        __type.name() : __type,
        __actuate.name() : __actuate,
        __arcrole.name() : __arcrole,
        __show.name() : __show,
        __role.name() : __role
    }
Namespace.addCategoryObject('typeBinding', u'OnlineResourceType', OnlineResourceType)


# Complex type ResponsiblePartySubsetType with content type ELEMENT_ONLY
class ResponsiblePartySubsetType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ResponsiblePartySubsetType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Role uses Python identifier Role
    __Role = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Role'), 'Role', '__httpwww_opengis_netows_ResponsiblePartySubsetType_httpwww_opengis_netowsRole', False)

    
    Role = property(__Role.value, __Role.set, None, u'Function performed by the responsible party. Possible values of this Role shall include the values and the meanings listed in Subclause B.5.5 of ISO 19115:2003. ')

    
    # Element {http://www.opengis.net/ows}IndividualName uses Python identifier IndividualName
    __IndividualName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'IndividualName'), 'IndividualName', '__httpwww_opengis_netows_ResponsiblePartySubsetType_httpwww_opengis_netowsIndividualName', False)

    
    IndividualName = property(__IndividualName.value, __IndividualName.set, None, u'Name of the responsible person: surname, given name, title separated by a delimiter. ')

    
    # Element {http://www.opengis.net/ows}ContactInfo uses Python identifier ContactInfo
    __ContactInfo = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ContactInfo'), 'ContactInfo', '__httpwww_opengis_netows_ResponsiblePartySubsetType_httpwww_opengis_netowsContactInfo', False)

    
    ContactInfo = property(__ContactInfo.value, __ContactInfo.set, None, u'Address of the responsible party. ')

    
    # Element {http://www.opengis.net/ows}PositionName uses Python identifier PositionName
    __PositionName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'PositionName'), 'PositionName', '__httpwww_opengis_netows_ResponsiblePartySubsetType_httpwww_opengis_netowsPositionName', False)

    
    PositionName = property(__PositionName.value, __PositionName.set, None, u'Role or position of the responsible person. ')


    _ElementMap = {
        __Role.name() : __Role,
        __IndividualName.name() : __IndividualName,
        __ContactInfo.name() : __ContactInfo,
        __PositionName.name() : __PositionName
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ResponsiblePartySubsetType', ResponsiblePartySubsetType)


# Complex type ResponsiblePartyType with content type ELEMENT_ONLY
class ResponsiblePartyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ResponsiblePartyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}OrganisationName uses Python identifier OrganisationName
    __OrganisationName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'OrganisationName'), 'OrganisationName', '__httpwww_opengis_netows_ResponsiblePartyType_httpwww_opengis_netowsOrganisationName', False)

    
    OrganisationName = property(__OrganisationName.value, __OrganisationName.set, None, u'Name of the responsible organization. ')

    
    # Element {http://www.opengis.net/ows}PositionName uses Python identifier PositionName
    __PositionName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'PositionName'), 'PositionName', '__httpwww_opengis_netows_ResponsiblePartyType_httpwww_opengis_netowsPositionName', False)

    
    PositionName = property(__PositionName.value, __PositionName.set, None, u'Role or position of the responsible person. ')

    
    # Element {http://www.opengis.net/ows}ContactInfo uses Python identifier ContactInfo
    __ContactInfo = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ContactInfo'), 'ContactInfo', '__httpwww_opengis_netows_ResponsiblePartyType_httpwww_opengis_netowsContactInfo', False)

    
    ContactInfo = property(__ContactInfo.value, __ContactInfo.set, None, u'Address of the responsible party. ')

    
    # Element {http://www.opengis.net/ows}Role uses Python identifier Role
    __Role = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Role'), 'Role', '__httpwww_opengis_netows_ResponsiblePartyType_httpwww_opengis_netowsRole', False)

    
    Role = property(__Role.value, __Role.set, None, u'Function performed by the responsible party. Possible values of this Role shall include the values and the meanings listed in Subclause B.5.5 of ISO 19115:2003. ')

    
    # Element {http://www.opengis.net/ows}IndividualName uses Python identifier IndividualName
    __IndividualName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'IndividualName'), 'IndividualName', '__httpwww_opengis_netows_ResponsiblePartyType_httpwww_opengis_netowsIndividualName', False)

    
    IndividualName = property(__IndividualName.value, __IndividualName.set, None, u'Name of the responsible person: surname, given name, title separated by a delimiter. ')


    _ElementMap = {
        __OrganisationName.name() : __OrganisationName,
        __PositionName.name() : __PositionName,
        __ContactInfo.name() : __ContactInfo,
        __Role.name() : __Role,
        __IndividualName.name() : __IndividualName
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'ResponsiblePartyType', ResponsiblePartyType)


# Complex type CapabilitiesBaseType with content type ELEMENT_ONLY
class CapabilitiesBaseType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'CapabilitiesBaseType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}ServiceProvider uses Python identifier ServiceProvider
    __ServiceProvider = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ServiceProvider'), 'ServiceProvider', '__httpwww_opengis_netows_CapabilitiesBaseType_httpwww_opengis_netowsServiceProvider', False)

    
    ServiceProvider = property(__ServiceProvider.value, __ServiceProvider.set, None, u'Metadata about the organization that provides this specific service instance or server. ')

    
    # Element {http://www.opengis.net/ows}OperationsMetadata uses Python identifier OperationsMetadata
    __OperationsMetadata = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'OperationsMetadata'), 'OperationsMetadata', '__httpwww_opengis_netows_CapabilitiesBaseType_httpwww_opengis_netowsOperationsMetadata', False)

    
    OperationsMetadata = property(__OperationsMetadata.value, __OperationsMetadata.set, None, u'Metadata about the operations and related abilities specified by this service and implemented by this server, including the URLs for operation requests. The basic contents of this section shall be the same for all OWS types, but individual services can add elements and/or change the optionality of optional elements. ')

    
    # Element {http://www.opengis.net/ows}ServiceIdentification uses Python identifier ServiceIdentification
    __ServiceIdentification = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ServiceIdentification'), 'ServiceIdentification', '__httpwww_opengis_netows_CapabilitiesBaseType_httpwww_opengis_netowsServiceIdentification', False)

    
    ServiceIdentification = property(__ServiceIdentification.value, __ServiceIdentification.set, None, u'General metadata for this specific server. This XML Schema of this section shall be the same for all OWS. ')

    
    # Attribute updateSequence uses Python identifier updateSequence
    __updateSequence = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'updateSequence'), 'updateSequence', '__httpwww_opengis_netows_CapabilitiesBaseType_updateSequence', UpdateSequenceType)
    
    updateSequence = property(__updateSequence.value, __updateSequence.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpwww_opengis_netows_CapabilitiesBaseType_version', VersionType, required=True)
    
    version = property(__version.value, __version.set, None, None)


    _ElementMap = {
        __ServiceProvider.name() : __ServiceProvider,
        __OperationsMetadata.name() : __OperationsMetadata,
        __ServiceIdentification.name() : __ServiceIdentification
    }
    _AttributeMap = {
        __updateSequence.name() : __updateSequence,
        __version.name() : __version
    }
Namespace.addCategoryObject('typeBinding', u'CapabilitiesBaseType', CapabilitiesBaseType)


# Complex type CTD_ANON_3 with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}HTTP uses Python identifier HTTP
    __HTTP = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'HTTP'), 'HTTP', '__httpwww_opengis_netows_CTD_ANON_3_httpwww_opengis_netowsHTTP', False)

    
    HTTP = property(__HTTP.value, __HTTP.set, None, u'Connect point URLs for the HTTP Distributed Computing Platform (DCP). Normally, only one Get and/or one Post is included in this element. More than one Get and/or Post is allowed to support including alternative URLs for uses such as load balancing or backup. ')


    _ElementMap = {
        __HTTP.name() : __HTTP
    }
    _AttributeMap = {
        
    }



# Complex type WGS84BoundingBoxType with content type ELEMENT_ONLY
class WGS84BoundingBoxType (BoundingBoxType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'WGS84BoundingBoxType')
    # Base type is BoundingBoxType
    
    # Element UpperCorner ({http://www.opengis.net/ows}UpperCorner) inherited from {http://www.opengis.net/ows}BoundingBoxType
    
    # Element LowerCorner ({http://www.opengis.net/ows}LowerCorner) inherited from {http://www.opengis.net/ows}BoundingBoxType
    
    # Attribute crs is restricted from parent
    
    # Attribute crs uses Python identifier crs
    __crs = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'crs'), 'crs', '__httpwww_opengis_netows_BoundingBoxType_crs', pyxb.binding.datatypes.anyURI, fixed=True, unicode_default=u'urn:ogc:def:crs:OGC:2:84')
    
    crs = property(__crs.value, __crs.set, None, u'This attribute can be included when considered useful. When included, this attribute shall reference the 2D WGS 84 coordinate reference system with longitude before latitude and decimal values of longitude and latitude. ')

    
    # Attribute dimensions is restricted from parent
    
    # Attribute dimensions uses Python identifier dimensions
    __dimensions = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dimensions'), 'dimensions', '__httpwww_opengis_netows_BoundingBoxType_dimensions', pyxb.binding.datatypes.positiveInteger, fixed=True, unicode_default=u'2')
    
    dimensions = property(__dimensions.value, __dimensions.set, None, u'The number of dimensions in this CRS (the length of a coordinate sequence in this use of the PositionType). This number is specified by the CRS definition, but can also be specified here. ')


    _ElementMap = BoundingBoxType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BoundingBoxType._AttributeMap.copy()
    _AttributeMap.update({
        __crs.name() : __crs,
        __dimensions.name() : __dimensions
    })
Namespace.addCategoryObject('typeBinding', u'WGS84BoundingBoxType', WGS84BoundingBoxType)


# Complex type CTD_ANON_4 with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Exception uses Python identifier Exception
    __Exception = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Exception'), 'Exception', '__httpwww_opengis_netows_CTD_ANON_4_httpwww_opengis_netowsException', True)

    
    Exception = property(__Exception.value, __Exception.set, None, None)

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpwww_opengis_netows_CTD_ANON_4_version', pyxb.binding.datatypes.string, required=True)
    
    version = property(__version.value, __version.set, None, u'Specification version for OWS operation. The string value shall contain one x.y.z "version" value (e.g., "2.1.3"). A version number shall contain three non-negative integers separated by decimal points, in the form "x.y.z". The integers y and z shall not exceed 99. Each version shall be for the Implementation Specification (document) and the associated XML Schemas to which requested operations will conform. An Implementation Specification version normally specifies XML Schemas against which an XML encoded operation response must conform and should be validated. See Version negotiation subclause for more information. ')

    
    # Attribute language uses Python identifier language
    __language = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'language'), 'language', '__httpwww_opengis_netows_CTD_ANON_4_language', pyxb.binding.datatypes.language)
    
    language = property(__language.value, __language.set, None, u'Identifier of the language used by all included exception text values. These language identifiers shall be as specified in IETF RFC 1766. When this attribute is omitted, the language used is not identified. ')


    _ElementMap = {
        __Exception.name() : __Exception
    }
    _AttributeMap = {
        __version.name() : __version,
        __language.name() : __language
    }



# Complex type DescriptionType with content type ELEMENT_ONLY
class DescriptionType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DescriptionType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Abstract uses Python identifier Abstract
    __Abstract = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Abstract'), 'Abstract', '__httpwww_opengis_netows_DescriptionType_httpwww_opengis_netowsAbstract', False)

    
    Abstract = property(__Abstract.value, __Abstract.set, None, u'Brief narrative description of this resource, normally used for display to a human. ')

    
    # Element {http://www.opengis.net/ows}Keywords uses Python identifier Keywords
    __Keywords = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Keywords'), 'Keywords', '__httpwww_opengis_netows_DescriptionType_httpwww_opengis_netowsKeywords', True)

    
    Keywords = property(__Keywords.value, __Keywords.set, None, None)

    
    # Element {http://www.opengis.net/ows}Title uses Python identifier Title
    __Title = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Title'), 'Title', '__httpwww_opengis_netows_DescriptionType_httpwww_opengis_netowsTitle', False)

    
    Title = property(__Title.value, __Title.set, None, u'Title of this resource, normally used for display to a human. ')


    _ElementMap = {
        __Abstract.name() : __Abstract,
        __Keywords.name() : __Keywords,
        __Title.name() : __Title
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'DescriptionType', DescriptionType)


# Complex type IdentificationType with content type ELEMENT_ONLY
class IdentificationType (DescriptionType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IdentificationType')
    # Base type is DescriptionType
    
    # Element {http://www.opengis.net/ows}OutputFormat uses Python identifier OutputFormat
    __OutputFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'OutputFormat'), 'OutputFormat', '__httpwww_opengis_netows_IdentificationType_httpwww_opengis_netowsOutputFormat', True)

    
    OutputFormat = property(__OutputFormat.value, __OutputFormat.set, None, u'Reference to a format in which this data can be encoded and transferred. More specific parameter names should be used by specific OWS specifications wherever applicable. More than one such parameter can be included for different purposes. ')

    
    # Element Abstract ({http://www.opengis.net/ows}Abstract) inherited from {http://www.opengis.net/ows}DescriptionType
    
    # Element {http://www.opengis.net/ows}Identifier uses Python identifier Identifier
    __Identifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), 'Identifier', '__httpwww_opengis_netows_IdentificationType_httpwww_opengis_netowsIdentifier', False)

    
    Identifier = property(__Identifier.value, __Identifier.set, None, u'Unique identifier or name of this dataset. ')

    
    # Element Title ({http://www.opengis.net/ows}Title) inherited from {http://www.opengis.net/ows}DescriptionType
    
    # Element {http://www.opengis.net/ows}AvailableCRS uses Python identifier AvailableCRS
    __AvailableCRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AvailableCRS'), 'AvailableCRS', '__httpwww_opengis_netows_IdentificationType_httpwww_opengis_netowsAvailableCRS', True)

    
    AvailableCRS = property(__AvailableCRS.value, __AvailableCRS.set, None, None)

    
    # Element Keywords ({http://www.opengis.net/ows}Keywords) inherited from {http://www.opengis.net/ows}DescriptionType
    
    # Element {http://www.opengis.net/ows}BoundingBox uses Python identifier BoundingBox
    __BoundingBox = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'BoundingBox'), 'BoundingBox', '__httpwww_opengis_netows_IdentificationType_httpwww_opengis_netowsBoundingBox', True)

    
    BoundingBox = property(__BoundingBox.value, __BoundingBox.set, None, None)

    
    # Element {http://www.opengis.net/ows}Metadata uses Python identifier Metadata
    __Metadata = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Metadata'), 'Metadata', '__httpwww_opengis_netows_IdentificationType_httpwww_opengis_netowsMetadata', True)

    
    Metadata = property(__Metadata.value, __Metadata.set, None, None)


    _ElementMap = DescriptionType._ElementMap.copy()
    _ElementMap.update({
        __OutputFormat.name() : __OutputFormat,
        __Identifier.name() : __Identifier,
        __AvailableCRS.name() : __AvailableCRS,
        __BoundingBox.name() : __BoundingBox,
        __Metadata.name() : __Metadata
    })
    _AttributeMap = DescriptionType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'IdentificationType', IdentificationType)


# Complex type GetCapabilitiesType with content type ELEMENT_ONLY
class GetCapabilitiesType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'GetCapabilitiesType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Sections uses Python identifier Sections
    __Sections = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Sections'), 'Sections', '__httpwww_opengis_netows_GetCapabilitiesType_httpwww_opengis_netowsSections', False)

    
    Sections = property(__Sections.value, __Sections.set, None, u'When omitted or not supported by server, server shall return complete service metadata (Capabilities) document. ')

    
    # Element {http://www.opengis.net/ows}AcceptFormats uses Python identifier AcceptFormats
    __AcceptFormats = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AcceptFormats'), 'AcceptFormats', '__httpwww_opengis_netows_GetCapabilitiesType_httpwww_opengis_netowsAcceptFormats', False)

    
    AcceptFormats = property(__AcceptFormats.value, __AcceptFormats.set, None, u'When omitted or not supported by server, server shall return service metadata document using the MIME type "text/xml". ')

    
    # Element {http://www.opengis.net/ows}AcceptVersions uses Python identifier AcceptVersions
    __AcceptVersions = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AcceptVersions'), 'AcceptVersions', '__httpwww_opengis_netows_GetCapabilitiesType_httpwww_opengis_netowsAcceptVersions', False)

    
    AcceptVersions = property(__AcceptVersions.value, __AcceptVersions.set, None, u'When omitted, server shall return latest supported version. ')

    
    # Attribute updateSequence uses Python identifier updateSequence
    __updateSequence = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'updateSequence'), 'updateSequence', '__httpwww_opengis_netows_GetCapabilitiesType_updateSequence', UpdateSequenceType)
    
    updateSequence = property(__updateSequence.value, __updateSequence.set, None, u'When omitted or not supported by server, server shall return latest complete service metadata document. ')


    _ElementMap = {
        __Sections.name() : __Sections,
        __AcceptFormats.name() : __AcceptFormats,
        __AcceptVersions.name() : __AcceptVersions
    }
    _AttributeMap = {
        __updateSequence.name() : __updateSequence
    }
Namespace.addCategoryObject('typeBinding', u'GetCapabilitiesType', GetCapabilitiesType)


# Complex type CTD_ANON_5 with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Post uses Python identifier Post
    __Post = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Post'), 'Post', '__httpwww_opengis_netows_CTD_ANON_5_httpwww_opengis_netowsPost', True)

    
    Post = property(__Post.value, __Post.set, None, u'Connect point URL and any constraints for the HTTP "Post" request method for this operation request. ')

    
    # Element {http://www.opengis.net/ows}Get uses Python identifier Get
    __Get = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Get'), 'Get', '__httpwww_opengis_netows_CTD_ANON_5_httpwww_opengis_netowsGet', True)

    
    Get = property(__Get.value, __Get.set, None, u'Connect point URL prefix and any constraints for the HTTP "Get" request method for this operation request. ')


    _ElementMap = {
        __Post.name() : __Post,
        __Get.name() : __Get
    }
    _AttributeMap = {
        
    }



# Complex type TelephoneType with content type ELEMENT_ONLY
class TelephoneType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TelephoneType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Facsimile uses Python identifier Facsimile
    __Facsimile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Facsimile'), 'Facsimile', '__httpwww_opengis_netows_TelephoneType_httpwww_opengis_netowsFacsimile', True)

    
    Facsimile = property(__Facsimile.value, __Facsimile.set, None, u'Telephone number of a facsimile machine for the responsible\norganization or individual. ')

    
    # Element {http://www.opengis.net/ows}Voice uses Python identifier Voice
    __Voice = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Voice'), 'Voice', '__httpwww_opengis_netows_TelephoneType_httpwww_opengis_netowsVoice', True)

    
    Voice = property(__Voice.value, __Voice.set, None, u'Telephone number by which individuals can speak to the responsible organization or individual. ')


    _ElementMap = {
        __Facsimile.name() : __Facsimile,
        __Voice.name() : __Voice
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TelephoneType', TelephoneType)


# Complex type AddressType with content type ELEMENT_ONLY
class AddressType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AddressType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}AdministrativeArea uses Python identifier AdministrativeArea
    __AdministrativeArea = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AdministrativeArea'), 'AdministrativeArea', '__httpwww_opengis_netows_AddressType_httpwww_opengis_netowsAdministrativeArea', False)

    
    AdministrativeArea = property(__AdministrativeArea.value, __AdministrativeArea.set, None, u'State or province of the location. ')

    
    # Element {http://www.opengis.net/ows}DeliveryPoint uses Python identifier DeliveryPoint
    __DeliveryPoint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'DeliveryPoint'), 'DeliveryPoint', '__httpwww_opengis_netows_AddressType_httpwww_opengis_netowsDeliveryPoint', True)

    
    DeliveryPoint = property(__DeliveryPoint.value, __DeliveryPoint.set, None, u'Address line for the location. ')

    
    # Element {http://www.opengis.net/ows}ElectronicMailAddress uses Python identifier ElectronicMailAddress
    __ElectronicMailAddress = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ElectronicMailAddress'), 'ElectronicMailAddress', '__httpwww_opengis_netows_AddressType_httpwww_opengis_netowsElectronicMailAddress', True)

    
    ElectronicMailAddress = property(__ElectronicMailAddress.value, __ElectronicMailAddress.set, None, u'Address of the electronic mailbox of the responsible organization or individual. ')

    
    # Element {http://www.opengis.net/ows}PostalCode uses Python identifier PostalCode
    __PostalCode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'PostalCode'), 'PostalCode', '__httpwww_opengis_netows_AddressType_httpwww_opengis_netowsPostalCode', False)

    
    PostalCode = property(__PostalCode.value, __PostalCode.set, None, u'ZIP or other postal code. ')

    
    # Element {http://www.opengis.net/ows}City uses Python identifier City
    __City = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'City'), 'City', '__httpwww_opengis_netows_AddressType_httpwww_opengis_netowsCity', False)

    
    City = property(__City.value, __City.set, None, u'City of the location. ')

    
    # Element {http://www.opengis.net/ows}Country uses Python identifier Country
    __Country = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Country'), 'Country', '__httpwww_opengis_netows_AddressType_httpwww_opengis_netowsCountry', False)

    
    Country = property(__Country.value, __Country.set, None, u'Country of the physical address. ')


    _ElementMap = {
        __AdministrativeArea.name() : __AdministrativeArea,
        __DeliveryPoint.name() : __DeliveryPoint,
        __ElectronicMailAddress.name() : __ElectronicMailAddress,
        __PostalCode.name() : __PostalCode,
        __City.name() : __City,
        __Country.name() : __Country
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AddressType', AddressType)


# Complex type SectionsType with content type ELEMENT_ONLY
class SectionsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SectionsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Section uses Python identifier Section
    __Section = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Section'), 'Section', '__httpwww_opengis_netows_SectionsType_httpwww_opengis_netowsSection', True)

    
    Section = property(__Section.value, __Section.set, None, None)


    _ElementMap = {
        __Section.name() : __Section
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'SectionsType', SectionsType)


# Complex type AcceptFormatsType with content type ELEMENT_ONLY
class AcceptFormatsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AcceptFormatsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}OutputFormat uses Python identifier OutputFormat
    __OutputFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'OutputFormat'), 'OutputFormat', '__httpwww_opengis_netows_AcceptFormatsType_httpwww_opengis_netowsOutputFormat', True)

    
    OutputFormat = property(__OutputFormat.value, __OutputFormat.set, None, None)


    _ElementMap = {
        __OutputFormat.name() : __OutputFormat
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AcceptFormatsType', AcceptFormatsType)


# Complex type RequestMethodType with content type ELEMENT_ONLY
class RequestMethodType (OnlineResourceType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RequestMethodType')
    # Base type is OnlineResourceType
    
    # Element {http://www.opengis.net/ows}Constraint uses Python identifier Constraint
    __Constraint = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Constraint'), 'Constraint', '__httpwww_opengis_netows_RequestMethodType_httpwww_opengis_netowsConstraint', True)

    
    Constraint = property(__Constraint.value, __Constraint.set, None, u'Optional unordered list of valid domain constraints on non-parameter quantities that each apply to this request method for this operation. If one of these Constraint elements has the same "name" attribute as a Constraint element in the OperationsMetadata or Operation element, this Constraint element shall override the other one for this operation. The list of required and optional constraints for this request method for this operation shall be specified in the Implementation Specification for this service. ')

    
    # Attribute href inherited from {http://www.opengis.net/ows}OnlineResourceType
    
    # Attribute title inherited from {http://www.opengis.net/ows}OnlineResourceType
    
    # Attribute type inherited from {http://www.opengis.net/ows}OnlineResourceType
    
    # Attribute actuate inherited from {http://www.opengis.net/ows}OnlineResourceType
    
    # Attribute arcrole inherited from {http://www.opengis.net/ows}OnlineResourceType
    
    # Attribute show inherited from {http://www.opengis.net/ows}OnlineResourceType
    
    # Attribute role inherited from {http://www.opengis.net/ows}OnlineResourceType

    _ElementMap = OnlineResourceType._ElementMap.copy()
    _ElementMap.update({
        __Constraint.name() : __Constraint
    })
    _AttributeMap = OnlineResourceType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'RequestMethodType', RequestMethodType)


# Complex type CTD_ANON_6 with content type ELEMENT_ONLY
class CTD_ANON_6 (DescriptionType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is DescriptionType
    
    # Element Abstract ({http://www.opengis.net/ows}Abstract) inherited from {http://www.opengis.net/ows}DescriptionType
    
    # Element {http://www.opengis.net/ows}AccessConstraints uses Python identifier AccessConstraints
    __AccessConstraints = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AccessConstraints'), 'AccessConstraints', '__httpwww_opengis_netows_CTD_ANON_6_httpwww_opengis_netowsAccessConstraints', True)

    
    AccessConstraints = property(__AccessConstraints.value, __AccessConstraints.set, None, u'Access constraint applied to assure the protection of privacy or intellectual property, or any other restrictions on retrieving or using data from or otherwise using this server. The reserved value NONE (case insensitive) shall be used to mean no access constraints are imposed. ')

    
    # Element {http://www.opengis.net/ows}Fees uses Python identifier Fees
    __Fees = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Fees'), 'Fees', '__httpwww_opengis_netows_CTD_ANON_6_httpwww_opengis_netowsFees', False)

    
    Fees = property(__Fees.value, __Fees.set, None, u'Fees and terms for retrieving data from or otherwise using this server, including the monetary units as specified in ISO 4217. The reserved value NONE (case insensitive) shall be used to mean no fees or terms. ')

    
    # Element Keywords ({http://www.opengis.net/ows}Keywords) inherited from {http://www.opengis.net/ows}DescriptionType
    
    # Element {http://www.opengis.net/ows}ServiceTypeVersion uses Python identifier ServiceTypeVersion
    __ServiceTypeVersion = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ServiceTypeVersion'), 'ServiceTypeVersion', '__httpwww_opengis_netows_CTD_ANON_6_httpwww_opengis_netowsServiceTypeVersion', True)

    
    ServiceTypeVersion = property(__ServiceTypeVersion.value, __ServiceTypeVersion.set, None, u'Unordered list of one or more versions of this service type implemented by this server. This information is not adequate for version negotiation, and shall not be used for that purpose. ')

    
    # Element {http://www.opengis.net/ows}ServiceType uses Python identifier ServiceType
    __ServiceType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ServiceType'), 'ServiceType', '__httpwww_opengis_netows_CTD_ANON_6_httpwww_opengis_netowsServiceType', False)

    
    ServiceType = property(__ServiceType.value, __ServiceType.set, None, u'A service type name from a registry of services. For example, the values of the codeSpace URI and name and code string may be "OGC" and "catalogue." This type name is normally used for machine-to-machine communication. ')

    
    # Element Title ({http://www.opengis.net/ows}Title) inherited from {http://www.opengis.net/ows}DescriptionType

    _ElementMap = DescriptionType._ElementMap.copy()
    _ElementMap.update({
        __AccessConstraints.name() : __AccessConstraints,
        __Fees.name() : __Fees,
        __ServiceTypeVersion.name() : __ServiceTypeVersion,
        __ServiceType.name() : __ServiceType
    })
    _AttributeMap = DescriptionType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type AcceptVersionsType with content type ELEMENT_ONLY
class AcceptVersionsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AcceptVersionsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Version uses Python identifier Version
    __Version = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Version'), 'Version', '__httpwww_opengis_netows_AcceptVersionsType_httpwww_opengis_netowsVersion', True)

    
    Version = property(__Version.value, __Version.set, None, None)


    _ElementMap = {
        __Version.name() : __Version
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'AcceptVersionsType', AcceptVersionsType)


Metadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Metadata'), MetadataType)
Namespace.addCategoryObject('elementBinding', Metadata.name().localName(), Metadata)

OperationsMetadata = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OperationsMetadata'), CTD_ANON_, documentation=u'Metadata about the operations and related abilities specified by this service and implemented by this server, including the URLs for operation requests. The basic contents of this section shall be the same for all OWS types, but individual services can add elements and/or change the optionality of optional elements. ')
Namespace.addCategoryObject('elementBinding', OperationsMetadata.name().localName(), OperationsMetadata)

Title = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Title'), pyxb.binding.datatypes.string, documentation=u'Title of this resource, normally used for display to a human. ')
Namespace.addCategoryObject('elementBinding', Title.name().localName(), Title)

SupportedCRS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SupportedCRS'), pyxb.binding.datatypes.anyURI, documentation=u'Coordinate reference system in which data from this data(set) or resource is available or supported. More specific parameter names should be used by specific OWS specifications wherever applicable. More than one such parameter can be included for different purposes. ')
Namespace.addCategoryObject('elementBinding', SupportedCRS.name().localName(), SupportedCRS)

AbstractMetaData = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractMetaData'), pyxb.binding.datatypes.anyType, abstract=pyxb.binding.datatypes.boolean(1), documentation=u'Abstract element containing more metadata about the element that includes the containing "metadata" element. A specific server implementation, or an Implementation Specification, can define concrete elements in the AbstractMetaData substitution group. ')
Namespace.addCategoryObject('elementBinding', AbstractMetaData.name().localName(), AbstractMetaData)

BoundingBox = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BoundingBox'), BoundingBoxType)
Namespace.addCategoryObject('elementBinding', BoundingBox.name().localName(), BoundingBox)

AccessConstraints = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AccessConstraints'), pyxb.binding.datatypes.string, documentation=u'Access constraint applied to assure the protection of privacy or intellectual property, or any other restrictions on retrieving or using data from or otherwise using this server. The reserved value NONE (case insensitive) shall be used to mean no access constraints are imposed. ')
Namespace.addCategoryObject('elementBinding', AccessConstraints.name().localName(), AccessConstraints)

PointOfContact = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'PointOfContact'), ResponsiblePartyType, documentation=u'Identification of, and means of communication with, person(s) responsible for the resource(s). For OWS use in the ServiceProvider section of a service metadata document, the optional organizationName element was removed, since this type is always used with the ProviderName element which provides that information. The optional individualName element was made mandatory, since either the organizationName or individualName element is mandatory. The mandatory "role" element was changed to optional, since no clear use of this information is known in the ServiceProvider section. ')
Namespace.addCategoryObject('elementBinding', PointOfContact.name().localName(), PointOfContact)

Exception = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Exception'), ExceptionType)
Namespace.addCategoryObject('elementBinding', Exception.name().localName(), Exception)

DCP = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DCP'), CTD_ANON_3, documentation=u'Information for one distributed Computing Platform (DCP) supported for this operation. At present, only the HTTP DCP is defined, so this element only includes the HTTP element.\n')
Namespace.addCategoryObject('elementBinding', DCP.name().localName(), DCP)

WGS84BoundingBox = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'WGS84BoundingBox'), WGS84BoundingBoxType)
Namespace.addCategoryObject('elementBinding', WGS84BoundingBox.name().localName(), WGS84BoundingBox)

ExceptionReport = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ExceptionReport'), CTD_ANON_4, documentation=u'Report message returned to the client that requested any OWS operation when the server detects an error while processing that operation request. ')
Namespace.addCategoryObject('elementBinding', ExceptionReport.name().localName(), ExceptionReport)

IndividualName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IndividualName'), pyxb.binding.datatypes.string, documentation=u'Name of the responsible person: surname, given name, title separated by a delimiter. ')
Namespace.addCategoryObject('elementBinding', IndividualName.name().localName(), IndividualName)

OrganisationName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OrganisationName'), pyxb.binding.datatypes.string, documentation=u'Name of the responsible organization. ')
Namespace.addCategoryObject('elementBinding', OrganisationName.name().localName(), OrganisationName)

Role = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Role'), CodeType, documentation=u'Function performed by the responsible party. Possible values of this Role shall include the values and the meanings listed in Subclause B.5.5 of ISO 19115:2003. ')
Namespace.addCategoryObject('elementBinding', Role.name().localName(), Role)

PositionName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'PositionName'), pyxb.binding.datatypes.string, documentation=u'Role or position of the responsible person. ')
Namespace.addCategoryObject('elementBinding', PositionName.name().localName(), PositionName)

ExtendedCapabilities = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ExtendedCapabilities'), pyxb.binding.datatypes.anyType, documentation=u'Individual software vendors and servers can use this element to provide metadata about any additional server abilities. ')
Namespace.addCategoryObject('elementBinding', ExtendedCapabilities.name().localName(), ExtendedCapabilities)

ContactInfo = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ContactInfo'), ContactType, documentation=u'Address of the responsible party. ')
Namespace.addCategoryObject('elementBinding', ContactInfo.name().localName(), ContactInfo)

Operation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Operation'), CTD_ANON_2, documentation=u'Metadata for one operation that this server implements. ')
Namespace.addCategoryObject('elementBinding', Operation.name().localName(), Operation)

GetCapabilities = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetCapabilities'), GetCapabilitiesType)
Namespace.addCategoryObject('elementBinding', GetCapabilities.name().localName(), GetCapabilities)

Identifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), CodeType, documentation=u'Unique identifier or name of this dataset. ')
Namespace.addCategoryObject('elementBinding', Identifier.name().localName(), Identifier)

AvailableCRS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AvailableCRS'), pyxb.binding.datatypes.anyURI)
Namespace.addCategoryObject('elementBinding', AvailableCRS.name().localName(), AvailableCRS)

OutputFormat = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OutputFormat'), MimeType, documentation=u'Reference to a format in which this data can be encoded and transferred. More specific parameter names should be used by specific OWS specifications wherever applicable. More than one such parameter can be included for different purposes. ')
Namespace.addCategoryObject('elementBinding', OutputFormat.name().localName(), OutputFormat)

Fees = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Fees'), pyxb.binding.datatypes.string, documentation=u'Fees and terms for retrieving data from or otherwise using this server, including the monetary units as specified in ISO 4217. The reserved value NONE (case insensitive) shall be used to mean no fees or terms. ')
Namespace.addCategoryObject('elementBinding', Fees.name().localName(), Fees)

HTTP = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'HTTP'), CTD_ANON_5, documentation=u'Connect point URLs for the HTTP Distributed Computing Platform (DCP). Normally, only one Get and/or one Post is included in this element. More than one Get and/or Post is allowed to support including alternative URLs for uses such as load balancing or backup. ')
Namespace.addCategoryObject('elementBinding', HTTP.name().localName(), HTTP)

Language = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Language'), pyxb.binding.datatypes.language, documentation=u'Identifier of a language used by the data(set) contents. This language identifier shall be as specified in IETF RFC 1766. When this element is omitted, the language used is not identified. ')
Namespace.addCategoryObject('elementBinding', Language.name().localName(), Language)

Abstract = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Abstract'), pyxb.binding.datatypes.string, documentation=u'Brief narrative description of this resource, normally used for display to a human. ')
Namespace.addCategoryObject('elementBinding', Abstract.name().localName(), Abstract)

Keywords = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Keywords'), KeywordsType)
Namespace.addCategoryObject('elementBinding', Keywords.name().localName(), Keywords)

ServiceProvider = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ServiceProvider'), CTD_ANON, documentation=u'Metadata about the organization that provides this specific service instance or server. ')
Namespace.addCategoryObject('elementBinding', ServiceProvider.name().localName(), ServiceProvider)

ServiceIdentification = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ServiceIdentification'), CTD_ANON_6, documentation=u'General metadata for this specific server. This XML Schema of this section shall be the same for all OWS. ')
Namespace.addCategoryObject('elementBinding', ServiceIdentification.name().localName(), ServiceIdentification)



BoundingBoxType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'UpperCorner'), PositionType, scope=BoundingBoxType, documentation=u'Position of the bounding box corner at which the value of each coordinate normally is the algebraic maximum within this bounding box. In some cases, this position is normally displayed at the bottom, such as the bottom right for some image coordinates. For more information, see Subclauses 10.2.5 and C.13. '))

BoundingBoxType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'LowerCorner'), PositionType, scope=BoundingBoxType, documentation=u'Position of the bounding box corner at which the value of each coordinate normally is the algebraic minimum within this bounding box. In some cases, this position is normally displayed at the top, such as the top left for some image coordinates. For more information, see Subclauses 10.2.5 and C.13. '))
BoundingBoxType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(BoundingBoxType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'LowerCorner')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(BoundingBoxType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'UpperCorner')), min_occurs=1, max_occurs=1)
    )
BoundingBoxType._ContentModel = pyxb.binding.content.ParticleModel(BoundingBoxType._GroupModel, min_occurs=1, max_occurs=1)



MetadataType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AbstractMetaData'), pyxb.binding.datatypes.anyType, abstract=pyxb.binding.datatypes.boolean(1), scope=MetadataType, documentation=u'Abstract element containing more metadata about the element that includes the containing "metadata" element. A specific server implementation, or an Implementation Specification, can define concrete elements in the AbstractMetaData substitution group. '))
MetadataType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(MetadataType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AbstractMetaData')), min_occurs=0L, max_occurs=1)
    )
MetadataType._ContentModel = pyxb.binding.content.ParticleModel(MetadataType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ProviderSite'), OnlineResourceType, scope=CTD_ANON, documentation=u'Reference to the most relevant web site of the service provider. '))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ServiceContact'), ResponsiblePartySubsetType, scope=CTD_ANON, documentation=u'Information for contacting the service provider. The OnlineResource element within this ServiceContact element should not be used to reference a web site of the service provider. '))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ProviderName'), pyxb.binding.datatypes.string, scope=CTD_ANON, documentation=u'A unique identifier for the service provider organization. '))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ProviderName')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ProviderSite')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ServiceContact')), min_occurs=1, max_occurs=1)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ExtendedCapabilities'), pyxb.binding.datatypes.anyType, scope=CTD_ANON_, documentation=u'Individual software vendors and servers can use this element to provide metadata about any additional server abilities. '))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Constraint'), DomainType, scope=CTD_ANON_, documentation=u'Optional unordered list of valid domain constraints on non-parameter quantities that each apply to this server. The list of required and optional constraints shall be specified in the Implementation Specification for this service. '))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Parameter'), DomainType, scope=CTD_ANON_, documentation=u'Optional unordered list of parameter valid domains that each apply to one or more operations which this server interface implements. The list of required and optional parameter domain limitations shall be specified in the Implementation Specification for this service. '))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Operation'), CTD_ANON_2, scope=CTD_ANON_, documentation=u'Metadata for one operation that this server implements. '))
CTD_ANON_._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Operation')), min_occurs=2L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Parameter')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Constraint')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ExtendedCapabilities')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Metadata'), MetadataType, scope=CTD_ANON_2))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Constraint'), DomainType, scope=CTD_ANON_2, documentation=u'Optional unordered list of valid domain constraints on non-parameter quantities that each apply to this operation. If one of these Constraint elements has the same "name" attribute as a Constraint element in the OperationsMetadata element, this Constraint element shall override the other one for this operation. The list of required and optional constraints for this operation shall be specified in the Implementation Specification for this service. '))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Parameter'), DomainType, scope=CTD_ANON_2, documentation=u'Optional unordered list of parameter domains that each apply to this operation which this server implements. If one of these Parameter elements has the same "name" attribute as a Parameter element in the OperationsMetadata element, this Parameter element shall override the other one for this operation. The list of required and optional parameter domain limitations for this operation shall be specified in the Implementation Specification for this service. '))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DCP'), CTD_ANON_3, scope=CTD_ANON_2, documentation=u'Information for one distributed Computing Platform (DCP) supported for this operation. At present, only the HTTP DCP is defined, so this element only includes the HTTP element.\n'))
CTD_ANON_2._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'DCP')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Parameter')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Constraint')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Metadata')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_2._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel, min_occurs=1, max_occurs=1)



DomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Value'), pyxb.binding.datatypes.string, scope=DomainType, documentation=u'Unordered list of all the valid values for this parameter or other quantity. For those parameters that contain a list or sequence of values, these values shall be for individual values in the list. The allowed set of values and the allowed server restrictions on that set of values shall be specified in the Implementation Specification for this service. '))

DomainType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Metadata'), MetadataType, scope=DomainType))
DomainType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DomainType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Value')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(DomainType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Metadata')), min_occurs=0L, max_occurs=None)
    )
DomainType._ContentModel = pyxb.binding.content.ParticleModel(DomainType._GroupModel, min_occurs=1, max_occurs=1)



KeywordsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Type'), CodeType, scope=KeywordsType))

KeywordsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Keyword'), pyxb.binding.datatypes.string, scope=KeywordsType))
KeywordsType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(KeywordsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Keyword')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(KeywordsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Type')), min_occurs=0L, max_occurs=1)
    )
KeywordsType._ContentModel = pyxb.binding.content.ParticleModel(KeywordsType._GroupModel, min_occurs=1, max_occurs=1)



ExceptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ExceptionText'), pyxb.binding.datatypes.string, scope=ExceptionType, documentation=u'Ordered sequence of text strings that describe this specific exception or error. The contents of these strings are left open to definition by each server implementation. A server is strongly encouraged to include at least one ExceptionText value, to provide more information about the detected error than provided by the exceptionCode. When included, multiple ExceptionText values shall provide hierarchical information about one detected error, with the most significant information listed first. '))
ExceptionType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ExceptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ExceptionText')), min_occurs=0L, max_occurs=None)
    )
ExceptionType._ContentModel = pyxb.binding.content.ParticleModel(ExceptionType._GroupModel, min_occurs=1, max_occurs=1)



ContactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ContactInstructions'), pyxb.binding.datatypes.string, scope=ContactType, documentation=u'Supplemental instructions on how or when to contact the individual or organization. '))

ContactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Address'), AddressType, scope=ContactType, documentation=u'Physical and email address at which the organization or individual may be contacted. '))

ContactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'HoursOfService'), pyxb.binding.datatypes.string, scope=ContactType, documentation=u'Time period (including time zone) when individuals can contact the organization or individual. '))

ContactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Phone'), TelephoneType, scope=ContactType, documentation=u'Telephone numbers at which the organization or individual may be contacted. '))

ContactType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OnlineResource'), OnlineResourceType, scope=ContactType, documentation=u'On-line information that can be used to contact the individual or organization. OWS specifics: The xlink:href attribute in the xlink:simpleLink attribute group shall be used to reference this resource. Whenever practical, the xlink:href attribute with type anyURI should be a URL from which more contact information can be electronically retrieved. The xlink:title attribute with type "string" can be used to name this set of information. The other attributes in the xlink:simpleLink attribute group should not be used. '))
ContactType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ContactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Phone')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ContactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Address')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ContactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'OnlineResource')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ContactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'HoursOfService')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ContactType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ContactInstructions')), min_occurs=0L, max_occurs=1)
    )
ContactType._ContentModel = pyxb.binding.content.ParticleModel(ContactType._GroupModel, min_occurs=1, max_occurs=1)



ResponsiblePartySubsetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Role'), CodeType, scope=ResponsiblePartySubsetType, documentation=u'Function performed by the responsible party. Possible values of this Role shall include the values and the meanings listed in Subclause B.5.5 of ISO 19115:2003. '))

ResponsiblePartySubsetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IndividualName'), pyxb.binding.datatypes.string, scope=ResponsiblePartySubsetType, documentation=u'Name of the responsible person: surname, given name, title separated by a delimiter. '))

ResponsiblePartySubsetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ContactInfo'), ContactType, scope=ResponsiblePartySubsetType, documentation=u'Address of the responsible party. '))

ResponsiblePartySubsetType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'PositionName'), pyxb.binding.datatypes.string, scope=ResponsiblePartySubsetType, documentation=u'Role or position of the responsible person. '))
ResponsiblePartySubsetType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ResponsiblePartySubsetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'IndividualName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ResponsiblePartySubsetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'PositionName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ResponsiblePartySubsetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ContactInfo')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ResponsiblePartySubsetType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Role')), min_occurs=0L, max_occurs=1)
    )
ResponsiblePartySubsetType._ContentModel = pyxb.binding.content.ParticleModel(ResponsiblePartySubsetType._GroupModel, min_occurs=1, max_occurs=1)



ResponsiblePartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OrganisationName'), pyxb.binding.datatypes.string, scope=ResponsiblePartyType, documentation=u'Name of the responsible organization. '))

ResponsiblePartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'PositionName'), pyxb.binding.datatypes.string, scope=ResponsiblePartyType, documentation=u'Role or position of the responsible person. '))

ResponsiblePartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ContactInfo'), ContactType, scope=ResponsiblePartyType, documentation=u'Address of the responsible party. '))

ResponsiblePartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Role'), CodeType, scope=ResponsiblePartyType, documentation=u'Function performed by the responsible party. Possible values of this Role shall include the values and the meanings listed in Subclause B.5.5 of ISO 19115:2003. '))

ResponsiblePartyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'IndividualName'), pyxb.binding.datatypes.string, scope=ResponsiblePartyType, documentation=u'Name of the responsible person: surname, given name, title separated by a delimiter. '))
ResponsiblePartyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ResponsiblePartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'IndividualName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ResponsiblePartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'OrganisationName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ResponsiblePartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'PositionName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ResponsiblePartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ContactInfo')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ResponsiblePartyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Role')), min_occurs=1, max_occurs=1)
    )
ResponsiblePartyType._ContentModel = pyxb.binding.content.ParticleModel(ResponsiblePartyType._GroupModel, min_occurs=1, max_occurs=1)



CapabilitiesBaseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ServiceProvider'), CTD_ANON, scope=CapabilitiesBaseType, documentation=u'Metadata about the organization that provides this specific service instance or server. '))

CapabilitiesBaseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OperationsMetadata'), CTD_ANON_, scope=CapabilitiesBaseType, documentation=u'Metadata about the operations and related abilities specified by this service and implemented by this server, including the URLs for operation requests. The basic contents of this section shall be the same for all OWS types, but individual services can add elements and/or change the optionality of optional elements. '))

CapabilitiesBaseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ServiceIdentification'), CTD_ANON_6, scope=CapabilitiesBaseType, documentation=u'General metadata for this specific server. This XML Schema of this section shall be the same for all OWS. '))
CapabilitiesBaseType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CapabilitiesBaseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ServiceIdentification')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CapabilitiesBaseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ServiceProvider')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CapabilitiesBaseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'OperationsMetadata')), min_occurs=0L, max_occurs=1)
    )
CapabilitiesBaseType._ContentModel = pyxb.binding.content.ParticleModel(CapabilitiesBaseType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'HTTP'), CTD_ANON_5, scope=CTD_ANON_3, documentation=u'Connect point URLs for the HTTP Distributed Computing Platform (DCP). Normally, only one Get and/or one Post is included in this element. More than one Get and/or Post is allowed to support including alternative URLs for uses such as load balancing or backup. '))
CTD_ANON_3._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'HTTP')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_3._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_3._GroupModel, min_occurs=1, max_occurs=1)


WGS84BoundingBoxType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(WGS84BoundingBoxType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'LowerCorner')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(WGS84BoundingBoxType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'UpperCorner')), min_occurs=1, max_occurs=1)
    )
WGS84BoundingBoxType._ContentModel = pyxb.binding.content.ParticleModel(WGS84BoundingBoxType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Exception'), ExceptionType, scope=CTD_ANON_4))
CTD_ANON_4._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Exception')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_4._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel, min_occurs=1, max_occurs=1)



DescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Abstract'), pyxb.binding.datatypes.string, scope=DescriptionType, documentation=u'Brief narrative description of this resource, normally used for display to a human. '))

DescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Keywords'), KeywordsType, scope=DescriptionType))

DescriptionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Title'), pyxb.binding.datatypes.string, scope=DescriptionType, documentation=u'Title of this resource, normally used for display to a human. '))
DescriptionType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Title')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(DescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Abstract')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(DescriptionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Keywords')), min_occurs=0L, max_occurs=None)
    )
DescriptionType._ContentModel = pyxb.binding.content.ParticleModel(DescriptionType._GroupModel, min_occurs=1, max_occurs=1)



IdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OutputFormat'), MimeType, scope=IdentificationType, documentation=u'Reference to a format in which this data can be encoded and transferred. More specific parameter names should be used by specific OWS specifications wherever applicable. More than one such parameter can be included for different purposes. '))

IdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Identifier'), CodeType, scope=IdentificationType, documentation=u'Unique identifier or name of this dataset. '))

IdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AvailableCRS'), pyxb.binding.datatypes.anyURI, scope=IdentificationType))

IdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'BoundingBox'), BoundingBoxType, scope=IdentificationType))

IdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Metadata'), MetadataType, scope=IdentificationType))
IdentificationType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Title')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Abstract')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Keywords')), min_occurs=0L, max_occurs=None)
    )
IdentificationType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Identifier')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'BoundingBox')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'OutputFormat')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AvailableCRS')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Metadata')), min_occurs=0L, max_occurs=None)
    )
IdentificationType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(IdentificationType._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(IdentificationType._GroupModel_2, min_occurs=1, max_occurs=1)
    )
IdentificationType._ContentModel = pyxb.binding.content.ParticleModel(IdentificationType._GroupModel, min_occurs=1, max_occurs=1)



GetCapabilitiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Sections'), SectionsType, scope=GetCapabilitiesType, documentation=u'When omitted or not supported by server, server shall return complete service metadata (Capabilities) document. '))

GetCapabilitiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AcceptFormats'), AcceptFormatsType, scope=GetCapabilitiesType, documentation=u'When omitted or not supported by server, server shall return service metadata document using the MIME type "text/xml". '))

GetCapabilitiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AcceptVersions'), AcceptVersionsType, scope=GetCapabilitiesType, documentation=u'When omitted, server shall return latest supported version. '))
GetCapabilitiesType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GetCapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AcceptVersions')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GetCapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Sections')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GetCapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AcceptFormats')), min_occurs=0L, max_occurs=1)
    )
GetCapabilitiesType._ContentModel = pyxb.binding.content.ParticleModel(GetCapabilitiesType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Post'), RequestMethodType, scope=CTD_ANON_5, documentation=u'Connect point URL and any constraints for the HTTP "Post" request method for this operation request. '))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Get'), RequestMethodType, scope=CTD_ANON_5, documentation=u'Connect point URL prefix and any constraints for the HTTP "Get" request method for this operation request. '))
CTD_ANON_5._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Get')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Post')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_5._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_5._GroupModel, min_occurs=1, max_occurs=None)



TelephoneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Facsimile'), pyxb.binding.datatypes.string, scope=TelephoneType, documentation=u'Telephone number of a facsimile machine for the responsible\norganization or individual. '))

TelephoneType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Voice'), pyxb.binding.datatypes.string, scope=TelephoneType, documentation=u'Telephone number by which individuals can speak to the responsible organization or individual. '))
TelephoneType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TelephoneType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Voice')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(TelephoneType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Facsimile')), min_occurs=0L, max_occurs=None)
    )
TelephoneType._ContentModel = pyxb.binding.content.ParticleModel(TelephoneType._GroupModel, min_occurs=1, max_occurs=1)



AddressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AdministrativeArea'), pyxb.binding.datatypes.string, scope=AddressType, documentation=u'State or province of the location. '))

AddressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DeliveryPoint'), pyxb.binding.datatypes.string, scope=AddressType, documentation=u'Address line for the location. '))

AddressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ElectronicMailAddress'), pyxb.binding.datatypes.string, scope=AddressType, documentation=u'Address of the electronic mailbox of the responsible organization or individual. '))

AddressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'PostalCode'), pyxb.binding.datatypes.string, scope=AddressType, documentation=u'ZIP or other postal code. '))

AddressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'City'), pyxb.binding.datatypes.string, scope=AddressType, documentation=u'City of the location. '))

AddressType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Country'), pyxb.binding.datatypes.string, scope=AddressType, documentation=u'Country of the physical address. '))
AddressType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AddressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'DeliveryPoint')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(AddressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'City')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AddressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AdministrativeArea')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AddressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'PostalCode')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AddressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Country')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(AddressType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ElectronicMailAddress')), min_occurs=0L, max_occurs=None)
    )
AddressType._ContentModel = pyxb.binding.content.ParticleModel(AddressType._GroupModel, min_occurs=1, max_occurs=1)



SectionsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Section'), pyxb.binding.datatypes.string, scope=SectionsType))
SectionsType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SectionsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Section')), min_occurs=0L, max_occurs=None)
    )
SectionsType._ContentModel = pyxb.binding.content.ParticleModel(SectionsType._GroupModel, min_occurs=1, max_occurs=1)



AcceptFormatsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OutputFormat'), MimeType, scope=AcceptFormatsType))
AcceptFormatsType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AcceptFormatsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'OutputFormat')), min_occurs=0L, max_occurs=None)
    )
AcceptFormatsType._ContentModel = pyxb.binding.content.ParticleModel(AcceptFormatsType._GroupModel, min_occurs=1, max_occurs=1)



RequestMethodType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Constraint'), DomainType, scope=RequestMethodType, documentation=u'Optional unordered list of valid domain constraints on non-parameter quantities that each apply to this request method for this operation. If one of these Constraint elements has the same "name" attribute as a Constraint element in the OperationsMetadata or Operation element, this Constraint element shall override the other one for this operation. The list of required and optional constraints for this request method for this operation shall be specified in the Implementation Specification for this service. '))
RequestMethodType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(RequestMethodType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Constraint')), min_occurs=0L, max_occurs=None)
    )
RequestMethodType._ContentModel = pyxb.binding.content.ParticleModel(RequestMethodType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AccessConstraints'), pyxb.binding.datatypes.string, scope=CTD_ANON_6, documentation=u'Access constraint applied to assure the protection of privacy or intellectual property, or any other restrictions on retrieving or using data from or otherwise using this server. The reserved value NONE (case insensitive) shall be used to mean no access constraints are imposed. '))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Fees'), pyxb.binding.datatypes.string, scope=CTD_ANON_6, documentation=u'Fees and terms for retrieving data from or otherwise using this server, including the monetary units as specified in ISO 4217. The reserved value NONE (case insensitive) shall be used to mean no fees or terms. '))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ServiceTypeVersion'), VersionType, scope=CTD_ANON_6, documentation=u'Unordered list of one or more versions of this service type implemented by this server. This information is not adequate for version negotiation, and shall not be used for that purpose. '))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ServiceType'), CodeType, scope=CTD_ANON_6, documentation=u'A service type name from a registry of services. For example, the values of the codeSpace URI and name and code string may be "OGC" and "catalogue." This type name is normally used for machine-to-machine communication. '))
CTD_ANON_6._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Title')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Abstract')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Keywords')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_6._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ServiceType')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ServiceTypeVersion')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Fees')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AccessConstraints')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_6._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_6._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._GroupModel_2, min_occurs=1, max_occurs=1)
    )
CTD_ANON_6._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_6._GroupModel, min_occurs=1, max_occurs=1)



AcceptVersionsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Version'), VersionType, scope=AcceptVersionsType))
AcceptVersionsType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(AcceptVersionsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Version')), min_occurs=1, max_occurs=None)
    )
AcceptVersionsType._ContentModel = pyxb.binding.content.ParticleModel(AcceptVersionsType._GroupModel, min_occurs=1, max_occurs=1)

SupportedCRS._setSubstitutionGroup(AvailableCRS)

WGS84BoundingBox._setSubstitutionGroup(BoundingBox)
