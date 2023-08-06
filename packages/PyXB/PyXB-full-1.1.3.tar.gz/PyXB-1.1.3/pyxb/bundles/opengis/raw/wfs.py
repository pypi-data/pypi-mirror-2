# ./pyxb/bundles/opengis/raw/wfs.py
# PyXB bindings for NM:eac7f5293585184de4c856df1b5ca308e1a93caf
# Generated 2011-09-09 14:19:13.671893 by PyXB version 1.1.3
# Namespace http://www.opengis.net/wfs

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:99d09f52-db18-11e0-9fd2-001fbc013adc')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.opengis.ows
import pyxb.bundles.opengis.filter
import pyxb.bundles.opengis.gml

Namespace = pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/wfs', create_if_missing=True)
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
class Base_TypeNameListType (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.QName."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'Base_TypeNameListType')
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.QName
Base_TypeNameListType._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', u'Base_TypeNameListType', Base_TypeNameListType)

# List SimpleTypeDefinition
# superclasses Base_TypeNameListType
class TypeNameListType (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.QName."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TypeNameListType')
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.QName
TypeNameListType._CF_pattern = pyxb.binding.facets.CF_pattern()
TypeNameListType._CF_pattern.addPattern(pattern=u'((\\w:)?\\w(=\\w)?){1,}')
TypeNameListType._InitializeFacetMap(TypeNameListType._CF_pattern)
Namespace.addCategoryObject('typeBinding', u'TypeNameListType', TypeNameListType)

# Atomic SimpleTypeDefinition
class AllSomeType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AllSomeType')
    _Documentation = None
AllSomeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=AllSomeType, enum_prefix=None)
AllSomeType.ALL = AllSomeType._CF_enumeration.addEnumeration(unicode_value=u'ALL', tag=u'ALL')
AllSomeType.SOME = AllSomeType._CF_enumeration.addEnumeration(unicode_value=u'SOME', tag=u'SOME')
AllSomeType._InitializeFacetMap(AllSomeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'AllSomeType', AllSomeType)

# Atomic SimpleTypeDefinition
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.textxml = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'text/xml', tag=u'textxml')
STD_ANON.texthtml = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'text/html', tag=u'texthtml')
STD_ANON.textsgml = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'text/sgml', tag=u'textsgml')
STD_ANON.textplain = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'text/plain', tag=u'textplain')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic SimpleTypeDefinition
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.TC211 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'TC211', tag=u'TC211')
STD_ANON_.FGDC = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'FGDC', tag=u'FGDC')
STD_ANON_.n19115 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'19115', tag=u'n19115')
STD_ANON_.n19139 = STD_ANON_._CF_enumeration.addEnumeration(unicode_value=u'19139', tag=u'n19139')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Atomic SimpleTypeDefinition
class IdentifierGenerationOptionType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IdentifierGenerationOptionType')
    _Documentation = None
IdentifierGenerationOptionType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=IdentifierGenerationOptionType, enum_prefix=None)
IdentifierGenerationOptionType.UseExisting = IdentifierGenerationOptionType._CF_enumeration.addEnumeration(unicode_value=u'UseExisting', tag=u'UseExisting')
IdentifierGenerationOptionType.ReplaceDuplicate = IdentifierGenerationOptionType._CF_enumeration.addEnumeration(unicode_value=u'ReplaceDuplicate', tag=u'ReplaceDuplicate')
IdentifierGenerationOptionType.GenerateNew = IdentifierGenerationOptionType._CF_enumeration.addEnumeration(unicode_value=u'GenerateNew', tag=u'GenerateNew')
IdentifierGenerationOptionType._InitializeFacetMap(IdentifierGenerationOptionType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'IdentifierGenerationOptionType', IdentifierGenerationOptionType)

# Atomic SimpleTypeDefinition
class OperationType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'OperationType')
    _Documentation = None
OperationType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=OperationType, enum_prefix=None)
OperationType.Insert = OperationType._CF_enumeration.addEnumeration(unicode_value=u'Insert', tag=u'Insert')
OperationType.Update = OperationType._CF_enumeration.addEnumeration(unicode_value=u'Update', tag=u'Update')
OperationType.Delete = OperationType._CF_enumeration.addEnumeration(unicode_value=u'Delete', tag=u'Delete')
OperationType.Query = OperationType._CF_enumeration.addEnumeration(unicode_value=u'Query', tag=u'Query')
OperationType.Lock = OperationType._CF_enumeration.addEnumeration(unicode_value=u'Lock', tag=u'Lock')
OperationType.GetGmlObject = OperationType._CF_enumeration.addEnumeration(unicode_value=u'GetGmlObject', tag=u'GetGmlObject')
OperationType._InitializeFacetMap(OperationType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'OperationType', OperationType)

# Atomic SimpleTypeDefinition
class ResultTypeType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ResultTypeType')
    _Documentation = None
ResultTypeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ResultTypeType, enum_prefix=None)
ResultTypeType.results = ResultTypeType._CF_enumeration.addEnumeration(unicode_value=u'results', tag=u'results')
ResultTypeType.hits = ResultTypeType._CF_enumeration.addEnumeration(unicode_value=u'hits', tag=u'hits')
ResultTypeType._InitializeFacetMap(ResultTypeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'ResultTypeType', ResultTypeType)

# Complex type BaseRequestType with content type EMPTY
class BaseRequestType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BaseRequestType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute handle uses Python identifier handle
    __handle = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'handle'), 'handle', '__httpwww_opengis_netwfs_BaseRequestType_handle', pyxb.binding.datatypes.string)
    
    handle = property(__handle.value, __handle.set, None, u'\n               The handle attribute allows a client application\n               to assign a client-generated request identifier\n               to a WFS request.  The handle is included to\n               facilitate error reporting.  A WFS may report the\n               handle in an exception report to identify the\n               offending request or action.  If the handle is not\n               present, then the WFS may employ other means to\n               localize the error (e.g. line numbers).\n            ')

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpwww_opengis_netwfs_BaseRequestType_version', pyxb.binding.datatypes.string, unicode_default=u'1.1.0')
    
    version = property(__version.value, __version.set, None, u'\n               The version attribute is used to indicate the version of the\n               WFS specification that a request conforms to.  All requests in\n               this schema conform to V1.1 of the WFS specification.\n               For WFS implementations that support more than one version of\n               a WFS sepcification ... if the version attribute is not \n               specified then the service should assume that the request\n               conforms to greatest available specification version.\n           ')

    
    # Attribute service uses Python identifier service
    __service = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpwww_opengis_netwfs_BaseRequestType_service', pyxb.bundles.opengis.ows.ServiceType, unicode_default=u'WFS')
    
    service = property(__service.value, __service.set, None, u'\n              The service attribute is included to support service \n              endpoints that implement more than one OGC service.\n              For example, a single CGI that implements WMS, WFS\n              and WCS services. \n              The endpoint can inspect the value of this attribute \n              to figure out which service should process the request.\n              The value WFS indicates that a web feature service should\n              process the request.\n              This parameter is somewhat redundant in the XML encoding\n              since the request namespace can be used to determine\n              which service should process any give request.  For example,\n              wfs:GetCapabilities and easily be distinguished from\n              wcs:GetCapabilities using the namespaces.\n           ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __handle.name() : __handle,
        __version.name() : __version,
        __service.name() : __service
    }
Namespace.addCategoryObject('typeBinding', u'BaseRequestType', BaseRequestType)


# Complex type GetGmlObjectType with content type ELEMENT_ONLY
class GetGmlObjectType (BaseRequestType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'GetGmlObjectType')
    # Base type is BaseRequestType
    
    # Element {http://www.opengis.net/ogc}GmlObjectId uses Python identifier GmlObjectId
    __GmlObjectId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'GmlObjectId'), 'GmlObjectId', '__httpwww_opengis_netwfs_GetGmlObjectType_httpwww_opengis_netogcGmlObjectId', False)

    
    GmlObjectId = property(__GmlObjectId.value, __GmlObjectId.set, None, None)

    
    # Attribute traverseXlinkExpiry uses Python identifier traverseXlinkExpiry
    __traverseXlinkExpiry = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'traverseXlinkExpiry'), 'traverseXlinkExpiry', '__httpwww_opengis_netwfs_GetGmlObjectType_traverseXlinkExpiry', pyxb.binding.datatypes.positiveInteger)
    
    traverseXlinkExpiry = property(__traverseXlinkExpiry.value, __traverseXlinkExpiry.set, None, u'\n                     The traverseXlinkExpiry attribute value is specified\n                     in minutes.  It indicates how long a Web Feature Service\n                     should wait to receive a response to a nested GetGmlObject\n                     request.\t\n                  ')

    
    # Attribute service inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute handle inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute outputFormat uses Python identifier outputFormat
    __outputFormat = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'outputFormat'), 'outputFormat', '__httpwww_opengis_netwfs_GetGmlObjectType_outputFormat', pyxb.binding.datatypes.string, unicode_default=u'GML3')
    
    outputFormat = property(__outputFormat.value, __outputFormat.set, None, None)

    
    # Attribute traverseXlinkDepth uses Python identifier traverseXlinkDepth
    __traverseXlinkDepth = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'traverseXlinkDepth'), 'traverseXlinkDepth', '__httpwww_opengis_netwfs_GetGmlObjectType_traverseXlinkDepth', pyxb.binding.datatypes.string, required=True)
    
    traverseXlinkDepth = property(__traverseXlinkDepth.value, __traverseXlinkDepth.set, None, u'\n                     This attribute indicates the depth to which nested\n                     property XLink linking element locator attribute\n                     (href) XLinks are traversed and resolved if possible.\n                     A value of "1" indicates that one linking element\n                     locator attribute (href) XLink will be traversed\n                     and the referenced element returned if possible, but\n                     nested property XLink linking element locator attribute\n                     (href) XLinks in the returned element are not traversed.\n                     A value of "*" indicates that all nested property XLink\n                     linking element locator attribute (href) XLinks will be\n                     traversed and the referenced elements returned if\n                     possible.  The range of valid values for this attribute\n                     consists of positive integers plus "*".\n                  ')

    
    # Attribute version inherited from {http://www.opengis.net/wfs}BaseRequestType

    _ElementMap = BaseRequestType._ElementMap.copy()
    _ElementMap.update({
        __GmlObjectId.name() : __GmlObjectId
    })
    _AttributeMap = BaseRequestType._AttributeMap.copy()
    _AttributeMap.update({
        __traverseXlinkExpiry.name() : __traverseXlinkExpiry,
        __outputFormat.name() : __outputFormat,
        __traverseXlinkDepth.name() : __traverseXlinkDepth
    })
Namespace.addCategoryObject('typeBinding', u'GetGmlObjectType', GetGmlObjectType)


# Complex type GMLObjectTypeListType with content type ELEMENT_ONLY
class GMLObjectTypeListType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'GMLObjectTypeListType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}GMLObjectType uses Python identifier GMLObjectType
    __GMLObjectType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'GMLObjectType'), 'GMLObjectType', '__httpwww_opengis_netwfs_GMLObjectTypeListType_httpwww_opengis_netwfsGMLObjectType', True)

    
    GMLObjectType = property(__GMLObjectType.value, __GMLObjectType.set, None, u'\n                  Name of this GML object type, including any namespace prefix\n               ')


    _ElementMap = {
        __GMLObjectType.name() : __GMLObjectType
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'GMLObjectTypeListType', GMLObjectTypeListType)


# Complex type QueryType with content type ELEMENT_ONLY
class QueryType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'QueryType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}SortBy uses Python identifier SortBy
    __SortBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'SortBy'), 'SortBy', '__httpwww_opengis_netwfs_QueryType_httpwww_opengis_netogcSortBy', False)

    
    SortBy = property(__SortBy.value, __SortBy.set, None, None)

    
    # Element {http://www.opengis.net/ogc}Filter uses Python identifier Filter
    __Filter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter'), 'Filter', '__httpwww_opengis_netwfs_QueryType_httpwww_opengis_netogcFilter', False)

    
    Filter = property(__Filter.value, __Filter.set, None, None)

    
    # Element {http://www.opengis.net/wfs}XlinkPropertyName uses Python identifier XlinkPropertyName
    __XlinkPropertyName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'XlinkPropertyName'), 'XlinkPropertyName', '__httpwww_opengis_netwfs_QueryType_httpwww_opengis_netwfsXlinkPropertyName', True)

    
    XlinkPropertyName = property(__XlinkPropertyName.value, __XlinkPropertyName.set, None, u'\n            This element may be used in place of an wfs:PropertyName element\n            in a wfs:Query element in a wfs:GetFeature element to selectively\n            request the traversal of nested XLinks in the returned element for\n            the named property. This element may not be used in other requests\n            -- GetFeatureWithLock, LockFeature, Insert, Update, Delete -- in\n            this version of the WFS specification.\n         ')

    
    # Element {http://www.opengis.net/ogc}Function uses Python identifier Function
    __Function = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Function'), 'Function', '__httpwww_opengis_netwfs_QueryType_httpwww_opengis_netogcFunction', True)

    
    Function = property(__Function.value, __Function.set, None, None)

    
    # Element {http://www.opengis.net/wfs}PropertyName uses Python identifier PropertyName
    __PropertyName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'PropertyName'), 'PropertyName', '__httpwww_opengis_netwfs_QueryType_httpwww_opengis_netwfsPropertyName', True)

    
    PropertyName = property(__PropertyName.value, __PropertyName.set, None, u'\n            The Property element is used to specify one or more\n            properties of a feature whose values are to be retrieved\n            by a Web Feature Service.\n\n            While a Web Feature Service should endeavour to satisfy\n            the exact request specified, in some instance this may\n            not be possible.  Specifically, a Web Feature Service\n            must generate a valid GML3 response to a Query operation.\n            The schema used to generate the output may include\n            properties that are mandatory.  In order that the output\n            validates, these mandatory properties must be specified\n            in the request.  If they are not, a Web Feature Service\n            may add them automatically to the Query before processing\n            it.  Thus a client application should, in general, be\n            prepared to receive more properties than it requested.\n\n            Of course, using the DescribeFeatureType request, a client\n            application can determine which properties are mandatory\n            and request them in the first place.\n         ')

    
    # Attribute featureVersion uses Python identifier featureVersion
    __featureVersion = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'featureVersion'), 'featureVersion', '__httpwww_opengis_netwfs_QueryType_featureVersion', pyxb.binding.datatypes.string)
    
    featureVersion = property(__featureVersion.value, __featureVersion.set, None, u"\n              For systems that implement versioning, the featureVersion\n              attribute is used to specify which version of a particular\n              feature instance is to be retrieved.  A value of ALL means\n              that all versions should be retrieved.  An integer value\n              'i', means that the ith version should be retrieve if it\n              exists or the most recent version otherwise.\n           ")

    
    # Attribute srsName uses Python identifier srsName
    __srsName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'srsName'), 'srsName', '__httpwww_opengis_netwfs_QueryType_srsName', pyxb.binding.datatypes.anyURI)
    
    srsName = property(__srsName.value, __srsName.set, None, u'\n              This attribute is used to specify a specific WFS-supported SRS\n              that should be used for returned feature geometries.  The value\n              may be the WFS StorageSRS value, DefaultRetrievalSRS value, or\n              one of AdditionalSRS values.  If no srsName value is supplied,\n              then the features will be returned using either the\n              DefaultRetrievalSRS, if specified, and StorageSRS otherwise.\n              For feature types with no spatial properties, this attribute\n              must not be specified or ignored if it is specified.\n           ')

    
    # Attribute typeName uses Python identifier typeName
    __typeName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'typeName'), 'typeName', '__httpwww_opengis_netwfs_QueryType_typeName', TypeNameListType, required=True)
    
    typeName = property(__typeName.value, __typeName.set, None, u"\n              The typeName attribute is a list of one or more\n              feature type names that indicate which types \n              of feature instances should be included in the\n              reponse set.  Specifying more than one typename\n              indicates that a join operation is being performed.\n              All the names in the typeName list must be valid\n              types that belong to this query's feature content\n              as defined by the GML Application Schema.\n           ")

    
    # Attribute handle uses Python identifier handle
    __handle = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'handle'), 'handle', '__httpwww_opengis_netwfs_QueryType_handle', pyxb.binding.datatypes.string)
    
    handle = property(__handle.value, __handle.set, None, u'\n               The handle attribute allows a client application\n               to assign a client-generated identifier for the \n               Query.  The handle is included to facilitate error\n               reporting.  If one Query in a GetFeature request\n               causes an exception, a WFS may report the handle\n               to indicate which query element failed.  If the a\n               handle is not present, the WFS may use other means\n               to localize the error (e.g. line numbers).\n            ')


    _ElementMap = {
        __SortBy.name() : __SortBy,
        __Filter.name() : __Filter,
        __XlinkPropertyName.name() : __XlinkPropertyName,
        __Function.name() : __Function,
        __PropertyName.name() : __PropertyName
    }
    _AttributeMap = {
        __featureVersion.name() : __featureVersion,
        __srsName.name() : __srsName,
        __typeName.name() : __typeName,
        __handle.name() : __handle
    }
Namespace.addCategoryObject('typeBinding', u'QueryType', QueryType)


# Complex type TransactionType with content type ELEMENT_ONLY
class TransactionType (BaseRequestType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TransactionType')
    # Base type is BaseRequestType
    
    # Element {http://www.opengis.net/wfs}Delete uses Python identifier Delete
    __Delete = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Delete'), 'Delete', '__httpwww_opengis_netwfs_TransactionType_httpwww_opengis_netwfsDelete', True)

    
    Delete = property(__Delete.value, __Delete.set, None, u'\n            The Delete element is used to indicate that one or more\n            feature instances should be removed from the feature\n            repository.\n         ')

    
    # Element {http://www.opengis.net/wfs}Insert uses Python identifier Insert
    __Insert = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Insert'), 'Insert', '__httpwww_opengis_netwfs_TransactionType_httpwww_opengis_netwfsInsert', True)

    
    Insert = property(__Insert.value, __Insert.set, None, u'\n            The Insert element is used to indicate that the Web Feature\n            Service should create a new instance of a feature type.  The\n            feature instance is specified using GML3 and one or more \n            feature instances to be created can be contained inside the\n            Insert element.\n         ')

    
    # Element {http://www.opengis.net/wfs}Update uses Python identifier Update
    __Update = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Update'), 'Update', '__httpwww_opengis_netwfs_TransactionType_httpwww_opengis_netwfsUpdate', True)

    
    Update = property(__Update.value, __Update.set, None, u'\n            One or more existing feature instances can be changed by\n            using the Update element.\n         ')

    
    # Element {http://www.opengis.net/wfs}Native uses Python identifier Native
    __Native = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Native'), 'Native', '__httpwww_opengis_netwfs_TransactionType_httpwww_opengis_netwfsNative', True)

    
    Native = property(__Native.value, __Native.set, None, u'\n            Many times, a Web Feature Service interacts with a repository\n            that may have special vendor specific capabilities.  The native\n            element allows vendor specific command to be passed to the\n            repository via the Web Feature Service.\n         ')

    
    # Element {http://www.opengis.net/wfs}LockId uses Python identifier LockId
    __LockId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'LockId'), 'LockId', '__httpwww_opengis_netwfs_TransactionType_httpwww_opengis_netwfsLockId', False)

    
    LockId = property(__LockId.value, __LockId.set, None, u'\n            The LockId element contains the value of the lock identifier\n            obtained by a client application from a previous GetFeatureWithLock\n            or LockFeature request.\n         ')

    
    # Attribute releaseAction uses Python identifier releaseAction
    __releaseAction = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'releaseAction'), 'releaseAction', '__httpwww_opengis_netwfs_TransactionType_releaseAction', AllSomeType)
    
    releaseAction = property(__releaseAction.value, __releaseAction.set, None, u'\n                     The releaseAction attribute is used to control how a Web\n                     Feature service releases locks on feature instances after\n                     a Transaction request has been processed.\n\n                     Valid values are ALL or SOME.\n\n                     A value of ALL means that the Web Feature Service should\n                     release the locks of all feature instances locked with the\n                     specified lockId regardless or whether or not the features\n                     were actually modified.\n\n                     A value of SOME means that the Web Feature Service will \n                     only release the locks held on feature instances that \n                     were actually operated upon by the transaction.  The\n                     lockId that the client application obtained shall remain\n                     valid and the other, unmodified, feature instances shall\n                     remain locked.\n                    \n                     If the expiry attribute was specified in the original\n                     operation that locked the feature instances, then the\n                     expiry counter will be reset to give the client\n                     application that same amount of time to post subsequent\n                     transactions against the locked features.\n                  ')

    
    # Attribute service inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute version inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute handle inherited from {http://www.opengis.net/wfs}BaseRequestType

    _ElementMap = BaseRequestType._ElementMap.copy()
    _ElementMap.update({
        __Delete.name() : __Delete,
        __Insert.name() : __Insert,
        __Update.name() : __Update,
        __Native.name() : __Native,
        __LockId.name() : __LockId
    })
    _AttributeMap = BaseRequestType._AttributeMap.copy()
    _AttributeMap.update({
        __releaseAction.name() : __releaseAction
    })
Namespace.addCategoryObject('typeBinding', u'TransactionType', TransactionType)


# Complex type DeleteElementType with content type ELEMENT_ONLY
class DeleteElementType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DeleteElementType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}Filter uses Python identifier Filter
    __Filter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter'), 'Filter', '__httpwww_opengis_netwfs_DeleteElementType_httpwww_opengis_netogcFilter', False)

    
    Filter = property(__Filter.value, __Filter.set, None, None)

    
    # Attribute typeName uses Python identifier typeName
    __typeName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'typeName'), 'typeName', '__httpwww_opengis_netwfs_DeleteElementType_typeName', pyxb.binding.datatypes.QName, required=True)
    
    typeName = property(__typeName.value, __typeName.set, None, u'\n              The value of the typeName attribute is the name \n              of the feature type to be updated. The name\n              specified must be a valid type that belongs to\n              the feature content as defined by the GML\n              Application Schema.\n           ')

    
    # Attribute handle uses Python identifier handle
    __handle = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'handle'), 'handle', '__httpwww_opengis_netwfs_DeleteElementType_handle', pyxb.binding.datatypes.string)
    
    handle = property(__handle.value, __handle.set, None, u'\n               The handle attribute allows a client application\n               to assign a client-generated request identifier\n               to an Insert action.  The handle is included to\n               facilitate error reporting.  If a Delete action\n               in a Transaction request fails, then a WFS may\n               include the handle in an exception report to localize\n               the error.  If no handle is included of the offending\n               Insert element then a WFS may employee other means of\n               localizing the error (e.g. line number).\n            ')


    _ElementMap = {
        __Filter.name() : __Filter
    }
    _AttributeMap = {
        __typeName.name() : __typeName,
        __handle.name() : __handle
    }
Namespace.addCategoryObject('typeBinding', u'DeleteElementType', DeleteElementType)


# Complex type TransactionSummaryType with content type ELEMENT_ONLY
class TransactionSummaryType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TransactionSummaryType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}totalDeleted uses Python identifier totalDeleted
    __totalDeleted = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'totalDeleted'), 'totalDeleted', '__httpwww_opengis_netwfs_TransactionSummaryType_httpwww_opengis_netwfstotalDeleted', False)

    
    totalDeleted = property(__totalDeleted.value, __totalDeleted.set, None, None)

    
    # Element {http://www.opengis.net/wfs}totalUpdated uses Python identifier totalUpdated
    __totalUpdated = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'totalUpdated'), 'totalUpdated', '__httpwww_opengis_netwfs_TransactionSummaryType_httpwww_opengis_netwfstotalUpdated', False)

    
    totalUpdated = property(__totalUpdated.value, __totalUpdated.set, None, None)

    
    # Element {http://www.opengis.net/wfs}totalInserted uses Python identifier totalInserted
    __totalInserted = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'totalInserted'), 'totalInserted', '__httpwww_opengis_netwfs_TransactionSummaryType_httpwww_opengis_netwfstotalInserted', False)

    
    totalInserted = property(__totalInserted.value, __totalInserted.set, None, None)


    _ElementMap = {
        __totalDeleted.name() : __totalDeleted,
        __totalUpdated.name() : __totalUpdated,
        __totalInserted.name() : __totalInserted
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TransactionSummaryType', TransactionSummaryType)


# Complex type LockType with content type ELEMENT_ONLY
class LockType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LockType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}Filter uses Python identifier Filter
    __Filter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter'), 'Filter', '__httpwww_opengis_netwfs_LockType_httpwww_opengis_netogcFilter', False)

    
    Filter = property(__Filter.value, __Filter.set, None, None)

    
    # Attribute typeName uses Python identifier typeName
    __typeName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'typeName'), 'typeName', '__httpwww_opengis_netwfs_LockType_typeName', pyxb.binding.datatypes.QName, required=True)
    
    typeName = property(__typeName.value, __typeName.set, None, u'\n              The value of the typeName attribute is the name \n              of the feature type to be updated. The name\n              specified must be a valid type that belongs to\n              the feature content as defined by the GML\n              Application Schema.\n           ')

    
    # Attribute handle uses Python identifier handle
    __handle = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'handle'), 'handle', '__httpwww_opengis_netwfs_LockType_handle', pyxb.binding.datatypes.string)
    
    handle = property(__handle.value, __handle.set, None, u'\n               The handle attribute allows a client application\n               to assign a client-generated request identifier\n               to a Lock action.  The handle is included to \n               facilitate error reporting.  If one of a set of\n               Lock actions failed while processing a LockFeature\n               request, a WFS may report the handle in an exception\n               report to localize the error.  If a handle is not\n               present then a WFS may employ some other means of \n               localizing the error (e.g. line number).\n            ')


    _ElementMap = {
        __Filter.name() : __Filter
    }
    _AttributeMap = {
        __typeName.name() : __typeName,
        __handle.name() : __handle
    }
Namespace.addCategoryObject('typeBinding', u'LockType', LockType)


# Complex type MetadataURLType with content type SIMPLE
class MetadataURLType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'MetadataURLType')
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute format uses Python identifier format
    __format = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'format'), 'format', '__httpwww_opengis_netwfs_MetadataURLType_format', STD_ANON, required=True)
    
    format = property(__format.value, __format.set, None, None)

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'type'), 'type', '__httpwww_opengis_netwfs_MetadataURLType_type', STD_ANON_, required=True)
    
    type = property(__type.value, __type.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __format.name() : __format,
        __type.name() : __type
    }
Namespace.addCategoryObject('typeBinding', u'MetadataURLType', MetadataURLType)


# Complex type GMLObjectTypeType with content type ELEMENT_ONLY
class GMLObjectTypeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'GMLObjectTypeType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ows}Keywords uses Python identifier Keywords
    __Keywords = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'Keywords'), 'Keywords', '__httpwww_opengis_netwfs_GMLObjectTypeType_httpwww_opengis_netowsKeywords', True)

    
    Keywords = property(__Keywords.value, __Keywords.set, None, None)

    
    # Element {http://www.opengis.net/wfs}OutputFormats uses Python identifier OutputFormats
    __OutputFormats = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'OutputFormats'), 'OutputFormats', '__httpwww_opengis_netwfs_GMLObjectTypeType_httpwww_opengis_netwfsOutputFormats', False)

    
    OutputFormats = property(__OutputFormats.value, __OutputFormats.set, None, None)

    
    # Element {http://www.opengis.net/wfs}Title uses Python identifier Title
    __Title = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Title'), 'Title', '__httpwww_opengis_netwfs_GMLObjectTypeType_httpwww_opengis_netwfsTitle', False)

    
    Title = property(__Title.value, __Title.set, None, u'\n                  Title of this GML Object type, normally used for display\n                  to a human.\n               ')

    
    # Element {http://www.opengis.net/wfs}Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Name'), 'Name', '__httpwww_opengis_netwfs_GMLObjectTypeType_httpwww_opengis_netwfsName', False)

    
    Name = property(__Name.value, __Name.set, None, u'\n                  Name of this GML Object type, including any namespace prefix.\n               ')

    
    # Element {http://www.opengis.net/wfs}Abstract uses Python identifier Abstract
    __Abstract = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Abstract'), 'Abstract', '__httpwww_opengis_netwfs_GMLObjectTypeType_httpwww_opengis_netwfsAbstract', False)

    
    Abstract = property(__Abstract.value, __Abstract.set, None, u'\n                  Brief narrative description of this GML Object type, normally\n                  used for display to a human.\n               ')


    _ElementMap = {
        __Keywords.name() : __Keywords,
        __OutputFormats.name() : __OutputFormats,
        __Title.name() : __Title,
        __Name.name() : __Name,
        __Abstract.name() : __Abstract
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'GMLObjectTypeType', GMLObjectTypeType)


# Complex type InsertResultsType with content type ELEMENT_ONLY
class InsertResultsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'InsertResultsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}Feature uses Python identifier Feature
    __Feature = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Feature'), 'Feature', '__httpwww_opengis_netwfs_InsertResultsType_httpwww_opengis_netwfsFeature', True)

    
    Feature = property(__Feature.value, __Feature.set, None, None)


    _ElementMap = {
        __Feature.name() : __Feature
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'InsertResultsType', InsertResultsType)


# Complex type NativeType with content type EMPTY
class NativeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'NativeType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute safeToIgnore uses Python identifier safeToIgnore
    __safeToIgnore = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'safeToIgnore'), 'safeToIgnore', '__httpwww_opengis_netwfs_NativeType_safeToIgnore', pyxb.binding.datatypes.boolean, required=True)
    
    safeToIgnore = property(__safeToIgnore.value, __safeToIgnore.set, None, u'\n               In the event that a Web Feature Service does not recognize\n               the vendorId or does not recognize the vendor specific command,\n               the safeToIgnore attribute is used to indicate whether the \n               exception can be safely ignored.  A value of TRUE means that\n               the Web Feature Service may ignore the command.  A value of\n               FALSE means that a Web Feature Service cannot ignore the\n               command and an exception should be raised if a problem is \n               encountered.\n            ')

    
    # Attribute vendorId uses Python identifier vendorId
    __vendorId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'vendorId'), 'vendorId', '__httpwww_opengis_netwfs_NativeType_vendorId', pyxb.binding.datatypes.string, required=True)
    
    vendorId = property(__vendorId.value, __vendorId.set, None, u"\n               The vendorId attribute is used to specify the name of\n               vendor who's vendor specific command the client\n               application wishes to execute.\n            ")


    _ElementMap = {
        
    }
    _AttributeMap = {
        __safeToIgnore.name() : __safeToIgnore,
        __vendorId.name() : __vendorId
    }
Namespace.addCategoryObject('typeBinding', u'NativeType', NativeType)


# Complex type LockFeatureResponseType with content type ELEMENT_ONLY
class LockFeatureResponseType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LockFeatureResponseType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}FeaturesNotLocked uses Python identifier FeaturesNotLocked
    __FeaturesNotLocked = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'FeaturesNotLocked'), 'FeaturesNotLocked', '__httpwww_opengis_netwfs_LockFeatureResponseType_httpwww_opengis_netwfsFeaturesNotLocked', False)

    
    FeaturesNotLocked = property(__FeaturesNotLocked.value, __FeaturesNotLocked.set, None, u'\n                  In contrast to the FeaturesLocked element, the\n                  FeaturesNotLocked element contains a list of \n                  ogc:Filter elements identifying feature instances\n                  that a WFS did not manage to lock because they were\n                  already locked by another process.\n               ')

    
    # Element {http://www.opengis.net/wfs}FeaturesLocked uses Python identifier FeaturesLocked
    __FeaturesLocked = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'FeaturesLocked'), 'FeaturesLocked', '__httpwww_opengis_netwfs_LockFeatureResponseType_httpwww_opengis_netwfsFeaturesLocked', False)

    
    FeaturesLocked = property(__FeaturesLocked.value, __FeaturesLocked.set, None, u'\n                  The LockFeature or GetFeatureWithLock operations\n                  identify and attempt to lock a set of feature \n                  instances that satisfy the constraints specified \n                  in the request.  In the event that the lockAction\n                  attribute (on the LockFeature or GetFeatureWithLock\n                  elements) is set to SOME, a Web Feature Service will\n                  attempt to lock as many of the feature instances from\n                  the result set as possible.\n\n                  The FeaturesLocked element contains list of ogc:FeatureId\n                  elements enumerating the feature instances that a WFS\n                  actually managed to lock.\n               ')

    
    # Element {http://www.opengis.net/wfs}LockId uses Python identifier LockId
    __LockId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'LockId'), 'LockId', '__httpwww_opengis_netwfs_LockFeatureResponseType_httpwww_opengis_netwfsLockId', False)

    
    LockId = property(__LockId.value, __LockId.set, None, u'\n            The LockId element contains the value of the lock identifier\n            obtained by a client application from a previous GetFeatureWithLock\n            or LockFeature request.\n         ')


    _ElementMap = {
        __FeaturesNotLocked.name() : __FeaturesNotLocked,
        __FeaturesLocked.name() : __FeaturesLocked,
        __LockId.name() : __LockId
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'LockFeatureResponseType', LockFeatureResponseType)


# Complex type InsertElementType with content type ELEMENT_ONLY
class InsertElementType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'InsertElementType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/gml}_Feature uses Python identifier Feature
    __Feature = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_Feature'), 'Feature', '__httpwww_opengis_netwfs_InsertElementType_httpwww_opengis_netgml_Feature', True)

    
    Feature = property(__Feature.value, __Feature.set, None, None)

    
    # Attribute idgen uses Python identifier idgen
    __idgen = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'idgen'), 'idgen', '__httpwww_opengis_netwfs_InsertElementType_idgen', IdentifierGenerationOptionType, unicode_default=u'GenerateNew')
    
    idgen = property(__idgen.value, __idgen.set, None, u'\n               The idgen attribute control how a WFS generates identifiers\n               from newly created feature instances using the Insert action.\n               The default action is to have the WFS generate a new id for\n               the features.  This is also backward compatible with WFS 1.0\n               where the only action was for the WFS to generate an new id.\n            ')

    
    # Attribute inputFormat uses Python identifier inputFormat
    __inputFormat = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'inputFormat'), 'inputFormat', '__httpwww_opengis_netwfs_InsertElementType_inputFormat', pyxb.binding.datatypes.string, unicode_default=u'text/xml; subtype=gml/3.1.1')
    
    inputFormat = property(__inputFormat.value, __inputFormat.set, None, u"\n               This inputFormat attribute is used to indicate \n               the format used to encode a feature instance in\n               an Insert element.  The default value of\n               'text/xml; subtype=gml/3.1.1' is used to indicate\n               that feature encoding is GML3.  Another example\n               might be 'text/xml; subtype=gml/2.1.2' indicating\n               that the feature us encoded in GML2.  A WFS must\n               declare in the capabilities document, using a \n               Parameter element, which version of GML it supports.\n            ")

    
    # Attribute srsName uses Python identifier srsName
    __srsName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'srsName'), 'srsName', '__httpwww_opengis_netwfs_InsertElementType_srsName', pyxb.binding.datatypes.anyURI)
    
    srsName = property(__srsName.value, __srsName.set, None, u"\n              ===== PAV 12NOV2004 ====\n              WHY IS THIS HERE? WOULDN'T WE KNOW THE INCOMING SRS FROM THE \n              GML GEOMETRY ELEMENTS?   I ASSUME THAT IF THE INCOMING SRS\n              DOES NOT MATCH ONE OF THE STORAGE SRS(s) THEN THE WFS WOULD\n              EITHER PROJECT INTO THE STORAGE SRS OR RAISE AN EXCEPTION.\n           ")

    
    # Attribute handle uses Python identifier handle
    __handle = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'handle'), 'handle', '__httpwww_opengis_netwfs_InsertElementType_handle', pyxb.binding.datatypes.string)
    
    handle = property(__handle.value, __handle.set, None, u'\n               The handle attribute allows a client application\n               to assign a client-generated request identifier\n               to an Insert action.  The handle is included to\n               facilitate error reporting.  If an Insert action\n               in a Transaction request fails, then a WFS may\n               include the handle in an exception report to localize\n               the error.  If no handle is included of the offending\n               Insert element then a WFS may employee other means of\n               localizing the error (e.g. line number).\n            ')


    _ElementMap = {
        __Feature.name() : __Feature
    }
    _AttributeMap = {
        __idgen.name() : __idgen,
        __inputFormat.name() : __inputFormat,
        __srsName.name() : __srsName,
        __handle.name() : __handle
    }
Namespace.addCategoryObject('typeBinding', u'InsertElementType', InsertElementType)


# Complex type FeatureTypeType with content type ELEMENT_ONLY
class FeatureTypeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FeatureTypeType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}OutputFormats uses Python identifier OutputFormats
    __OutputFormats = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'OutputFormats'), 'OutputFormats', '__httpwww_opengis_netwfs_FeatureTypeType_httpwww_opengis_netwfsOutputFormats', False)

    
    OutputFormats = property(__OutputFormats.value, __OutputFormats.set, None, None)

    
    # Element {http://www.opengis.net/wfs}DefaultSRS uses Python identifier DefaultSRS
    __DefaultSRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'DefaultSRS'), 'DefaultSRS', '__httpwww_opengis_netwfs_FeatureTypeType_httpwww_opengis_netwfsDefaultSRS', False)

    
    DefaultSRS = property(__DefaultSRS.value, __DefaultSRS.set, None, u'\n                        The DefaultSRS element indicated which spatial\n                        reference system shall be used by a WFS to\n                        express the state of a spatial feature if not\n                        otherwise explicitly identified within a query\n                        or transaction request.  The SRS may be indicated\n                        using either the EPSG form (EPSG:posc code) or\n                        the URL form defined in subclause 4.3.2 of\n                        refernce[2].\n                     ')

    
    # Element {http://www.opengis.net/wfs}OtherSRS uses Python identifier OtherSRS
    __OtherSRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'OtherSRS'), 'OtherSRS', '__httpwww_opengis_netwfs_FeatureTypeType_httpwww_opengis_netwfsOtherSRS', True)

    
    OtherSRS = property(__OtherSRS.value, __OtherSRS.set, None, u'\n                        The OtherSRS element is used to indicate other \n                        supported SRSs within query and transaction \n                        operations.  A supported SRS means that the \n                        WFS supports the transformation of spatial\n                        properties between the OtherSRS and the internal\n                        storage SRS.  The effects of such transformations \n                        must be considered when determining and declaring \n                        the guaranteed data accuracy.\n                     ')

    
    # Element {http://www.opengis.net/ows}WGS84BoundingBox uses Python identifier WGS84BoundingBox
    __WGS84BoundingBox = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'WGS84BoundingBox'), 'WGS84BoundingBox', '__httpwww_opengis_netwfs_FeatureTypeType_httpwww_opengis_netowsWGS84BoundingBox', True)

    
    WGS84BoundingBox = property(__WGS84BoundingBox.value, __WGS84BoundingBox.set, None, None)

    
    # Element {http://www.opengis.net/wfs}Abstract uses Python identifier Abstract
    __Abstract = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Abstract'), 'Abstract', '__httpwww_opengis_netwfs_FeatureTypeType_httpwww_opengis_netwfsAbstract', False)

    
    Abstract = property(__Abstract.value, __Abstract.set, None, u'\n                  Brief narrative description of this feature type, normally\n                  used for display to a human.\n               ')

    
    # Element {http://www.opengis.net/wfs}Operations uses Python identifier Operations
    __Operations = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Operations'), 'Operations', '__httpwww_opengis_netwfs_FeatureTypeType_httpwww_opengis_netwfsOperations', False)

    
    Operations = property(__Operations.value, __Operations.set, None, None)

    
    # Element {http://www.opengis.net/wfs}NoSRS uses Python identifier NoSRS
    __NoSRS = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'NoSRS'), 'NoSRS', '__httpwww_opengis_netwfs_FeatureTypeType_httpwww_opengis_netwfsNoSRS', False)

    
    NoSRS = property(__NoSRS.value, __NoSRS.set, None, None)

    
    # Element {http://www.opengis.net/wfs}MetadataURL uses Python identifier MetadataURL
    __MetadataURL = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'MetadataURL'), 'MetadataURL', '__httpwww_opengis_netwfs_FeatureTypeType_httpwww_opengis_netwfsMetadataURL', True)

    
    MetadataURL = property(__MetadataURL.value, __MetadataURL.set, None, None)

    
    # Element {http://www.opengis.net/wfs}Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Name'), 'Name', '__httpwww_opengis_netwfs_FeatureTypeType_httpwww_opengis_netwfsName', False)

    
    Name = property(__Name.value, __Name.set, None, u'\n                  Name of this feature type, including any namespace prefix\n               ')

    
    # Element {http://www.opengis.net/ows}Keywords uses Python identifier Keywords
    __Keywords = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'Keywords'), 'Keywords', '__httpwww_opengis_netwfs_FeatureTypeType_httpwww_opengis_netowsKeywords', True)

    
    Keywords = property(__Keywords.value, __Keywords.set, None, None)

    
    # Element {http://www.opengis.net/wfs}Title uses Python identifier Title
    __Title = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Title'), 'Title', '__httpwww_opengis_netwfs_FeatureTypeType_httpwww_opengis_netwfsTitle', False)

    
    Title = property(__Title.value, __Title.set, None, u'\n                  Title of this feature type, normally used for display\n                  to a human.\n               ')


    _ElementMap = {
        __OutputFormats.name() : __OutputFormats,
        __DefaultSRS.name() : __DefaultSRS,
        __OtherSRS.name() : __OtherSRS,
        __WGS84BoundingBox.name() : __WGS84BoundingBox,
        __Abstract.name() : __Abstract,
        __Operations.name() : __Operations,
        __NoSRS.name() : __NoSRS,
        __MetadataURL.name() : __MetadataURL,
        __Name.name() : __Name,
        __Keywords.name() : __Keywords,
        __Title.name() : __Title
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'FeatureTypeType', FeatureTypeType)


# Complex type UpdateElementType with content type ELEMENT_ONLY
class UpdateElementType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'UpdateElementType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}Property uses Python identifier Property
    __Property = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Property'), 'Property', '__httpwww_opengis_netwfs_UpdateElementType_httpwww_opengis_netwfsProperty', True)

    
    Property = property(__Property.value, __Property.set, None, u'\n            The Property element is used to specify the new\n            value of a feature property inside an Update\n            element.\n         ')

    
    # Element {http://www.opengis.net/ogc}Filter uses Python identifier Filter
    __Filter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter'), 'Filter', '__httpwww_opengis_netwfs_UpdateElementType_httpwww_opengis_netogcFilter', False)

    
    Filter = property(__Filter.value, __Filter.set, None, None)

    
    # Attribute handle uses Python identifier handle
    __handle = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'handle'), 'handle', '__httpwww_opengis_netwfs_UpdateElementType_handle', pyxb.binding.datatypes.string)
    
    handle = property(__handle.value, __handle.set, None, u'\n               The handle attribute allows a client application\n               to assign a client-generated request identifier\n               to an Insert action.  The handle is included to\n               facilitate error reporting.  If an Update action\n               in a Transaction request fails, then a WFS may\n               include the handle in an exception report to localize\n               the error.  If no handle is included of the offending\n               Insert element then a WFS may employee other means of\n               localizing the error (e.g. line number).\n            ')

    
    # Attribute inputFormat uses Python identifier inputFormat
    __inputFormat = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'inputFormat'), 'inputFormat', '__httpwww_opengis_netwfs_UpdateElementType_inputFormat', pyxb.binding.datatypes.string, unicode_default=u'x-application/gml:3')
    
    inputFormat = property(__inputFormat.value, __inputFormat.set, None, u"\n               This inputFormat attribute is used to indicate \n               the format used to encode a feature instance in\n               an Insert element.  The default value of\n               'text/xml; subtype=gml/3.1.1' is used to indicate\n               that feature encoding is GML3.  Another example\n               might be 'text/xml; subtype=gml/2.1.2' indicating\n               that the feature us encoded in GML2.  A WFS must\n               declare in the capabilities document, using a \n               Parameter element, which version of GML it supports.\n            ")

    
    # Attribute srsName uses Python identifier srsName
    __srsName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'srsName'), 'srsName', '__httpwww_opengis_netwfs_UpdateElementType_srsName', pyxb.binding.datatypes.anyURI)
    
    srsName = property(__srsName.value, __srsName.set, None, u'\n               DO WE NEED THIS HERE?\n           ')

    
    # Attribute typeName uses Python identifier typeName
    __typeName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'typeName'), 'typeName', '__httpwww_opengis_netwfs_UpdateElementType_typeName', pyxb.binding.datatypes.QName, required=True)
    
    typeName = property(__typeName.value, __typeName.set, None, u'\n              The value of the typeName attribute is the name \n              of the feature type to be updated. The name\n              specified must be a valid type that belongs to\n              the feature content as defined by the GML\n              Application Schema.\n           ')


    _ElementMap = {
        __Property.name() : __Property,
        __Filter.name() : __Filter
    }
    _AttributeMap = {
        __handle.name() : __handle,
        __inputFormat.name() : __inputFormat,
        __srsName.name() : __srsName,
        __typeName.name() : __typeName
    }
Namespace.addCategoryObject('typeBinding', u'UpdateElementType', UpdateElementType)


# Complex type DescribeFeatureTypeType with content type ELEMENT_ONLY
class DescribeFeatureTypeType (BaseRequestType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DescribeFeatureTypeType')
    # Base type is BaseRequestType
    
    # Element {http://www.opengis.net/wfs}TypeName uses Python identifier TypeName
    __TypeName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TypeName'), 'TypeName', '__httpwww_opengis_netwfs_DescribeFeatureTypeType_httpwww_opengis_netwfsTypeName', True)

    
    TypeName = property(__TypeName.value, __TypeName.set, None, u'\n                        The TypeName element is used to enumerate the\n                        feature types to be described.  If no TypeName\n                        elements are specified then all features should\n                        be described.  The name must be a valid type\n                        that belongs to the feature content as defined\n                        by the GML Application Schema.\n                     ')

    
    # Attribute outputFormat uses Python identifier outputFormat
    __outputFormat = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'outputFormat'), 'outputFormat', '__httpwww_opengis_netwfs_DescribeFeatureTypeType_outputFormat', pyxb.binding.datatypes.string, unicode_default=u'text/xml; subtype=gml/3.1.1')
    
    outputFormat = property(__outputFormat.value, __outputFormat.set, None, u"\n                     The outputFormat attribute is used to specify what schema\n                     description language should be used to describe features.\n                     The default value of 'text/xml; subtype=3.1.1' means that\n                     the WFS must generate a GML3 application schema that can\n                     be used to validate the GML3 output of a GetFeature\n                     request or feature instances specified in Transaction\n                     operations.\n                     For the purposes of experimentation, vendor extension,\n                     or even extensions that serve a specific community of\n                     interest, other acceptable output format values may be\n                     advertised by a WFS service in the capabilities document.\n                     The meaning of such values in not defined in the WFS \n                     specification.  The only proviso is such cases is that\n                     clients may safely ignore outputFormat values that do\n                     not recognize.\n                  ")

    
    # Attribute service inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute version inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute handle inherited from {http://www.opengis.net/wfs}BaseRequestType

    _ElementMap = BaseRequestType._ElementMap.copy()
    _ElementMap.update({
        __TypeName.name() : __TypeName
    })
    _AttributeMap = BaseRequestType._AttributeMap.copy()
    _AttributeMap.update({
        __outputFormat.name() : __outputFormat
    })
Namespace.addCategoryObject('typeBinding', u'DescribeFeatureTypeType', DescribeFeatureTypeType)


# Complex type InsertedFeatureType with content type ELEMENT_ONLY
class InsertedFeatureType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'InsertedFeatureType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}FeatureId uses Python identifier FeatureId
    __FeatureId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'FeatureId'), 'FeatureId', '__httpwww_opengis_netwfs_InsertedFeatureType_httpwww_opengis_netogcFeatureId', True)

    
    FeatureId = property(__FeatureId.value, __FeatureId.set, None, None)

    
    # Attribute handle uses Python identifier handle
    __handle = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'handle'), 'handle', '__httpwww_opengis_netwfs_InsertedFeatureType_handle', pyxb.binding.datatypes.string)
    
    handle = property(__handle.value, __handle.set, None, u'\n               If the insert element that generated this feature \n               had a value for the "handle" attribute then a WFS\n               may report it using this attribute to correlate\n               the feature created with the action that created it.\n            ')


    _ElementMap = {
        __FeatureId.name() : __FeatureId
    }
    _AttributeMap = {
        __handle.name() : __handle
    }
Namespace.addCategoryObject('typeBinding', u'InsertedFeatureType', InsertedFeatureType)


# Complex type FeaturesNotLockedType with content type ELEMENT_ONLY
class FeaturesNotLockedType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FeaturesNotLockedType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}FeatureId uses Python identifier FeatureId
    __FeatureId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'FeatureId'), 'FeatureId', '__httpwww_opengis_netwfs_FeaturesNotLockedType_httpwww_opengis_netogcFeatureId', True)

    
    FeatureId = property(__FeatureId.value, __FeatureId.set, None, None)


    _ElementMap = {
        __FeatureId.name() : __FeatureId
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'FeaturesNotLockedType', FeaturesNotLockedType)


# Complex type LockFeatureType with content type ELEMENT_ONLY
class LockFeatureType (BaseRequestType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'LockFeatureType')
    # Base type is BaseRequestType
    
    # Element {http://www.opengis.net/wfs}Lock uses Python identifier Lock
    __Lock = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Lock'), 'Lock', '__httpwww_opengis_netwfs_LockFeatureType_httpwww_opengis_netwfsLock', True)

    
    Lock = property(__Lock.value, __Lock.set, None, u'\n                        The lock element is used to indicate which feature \n                        instances of particular type are to be locked.\n                     ')

    
    # Attribute handle inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute service inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute version inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute expiry uses Python identifier expiry
    __expiry = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'expiry'), 'expiry', '__httpwww_opengis_netwfs_LockFeatureType_expiry', pyxb.binding.datatypes.positiveInteger, unicode_default=u'5')
    
    expiry = property(__expiry.value, __expiry.set, None, u'\n                     The expiry attribute is used to set the length\n                     of time (expressed in minutes) that features will\n                     remain locked as a result of a LockFeature\n                     request.  After the expiry period elapses, the\n                     locked resources must be released.  If the \n                     expiry attribute is not set, then the default\n                     value of 5 minutes will be enforced.\n                  ')

    
    # Attribute lockAction uses Python identifier lockAction
    __lockAction = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'lockAction'), 'lockAction', '__httpwww_opengis_netwfs_LockFeatureType_lockAction', AllSomeType, unicode_default=u'ALL')
    
    lockAction = property(__lockAction.value, __lockAction.set, None, u'\n                     The lockAction attribute is used to indicate what\n                     a Web Feature Service should do when it encounters\n                     a feature instance that has already been locked by\n                     another client application.\n      \n                     Valid values are ALL or SOME.\n      \n                     ALL means that the Web Feature Service must acquire\n                     locks on all the requested feature instances.  If it\n                     cannot acquire those locks then the request should\n                     fail.  In this instance, all locks acquired by the\n                     operation should be released.\n       \n                     SOME means that the Web Feature Service should lock\n                     as many of the requested features as it can.\n                  ')


    _ElementMap = BaseRequestType._ElementMap.copy()
    _ElementMap.update({
        __Lock.name() : __Lock
    })
    _AttributeMap = BaseRequestType._AttributeMap.copy()
    _AttributeMap.update({
        __expiry.name() : __expiry,
        __lockAction.name() : __lockAction
    })
Namespace.addCategoryObject('typeBinding', u'LockFeatureType', LockFeatureType)


# Complex type GetCapabilitiesType with content type ELEMENT_ONLY
class GetCapabilitiesType (pyxb.bundles.opengis.ows.GetCapabilitiesType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'GetCapabilitiesType')
    # Base type is pyxb.bundles.opengis.ows.GetCapabilitiesType
    
    # Element AcceptFormats ({http://www.opengis.net/ows}AcceptFormats) inherited from {http://www.opengis.net/ows}GetCapabilitiesType
    
    # Element Sections ({http://www.opengis.net/ows}Sections) inherited from {http://www.opengis.net/ows}GetCapabilitiesType
    
    # Element AcceptVersions ({http://www.opengis.net/ows}AcceptVersions) inherited from {http://www.opengis.net/ows}GetCapabilitiesType
    
    # Attribute updateSequence inherited from {http://www.opengis.net/ows}GetCapabilitiesType
    
    # Attribute service uses Python identifier service
    __service = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpwww_opengis_netwfs_GetCapabilitiesType_service', pyxb.bundles.opengis.ows.ServiceType, unicode_default=u'WFS')
    
    service = property(__service.value, __service.set, None, None)


    _ElementMap = pyxb.bundles.opengis.ows.GetCapabilitiesType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = pyxb.bundles.opengis.ows.GetCapabilitiesType._AttributeMap.copy()
    _AttributeMap.update({
        __service.name() : __service
    })
Namespace.addCategoryObject('typeBinding', u'GetCapabilitiesType', GetCapabilitiesType)


# Complex type TransactionResultsType with content type ELEMENT_ONLY
class TransactionResultsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TransactionResultsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}Action uses Python identifier Action
    __Action = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Action'), 'Action', '__httpwww_opengis_netwfs_TransactionResultsType_httpwww_opengis_netwfsAction', True)

    
    Action = property(__Action.value, __Action.set, None, u'\n                  The Action element reports an exception code\n                  and exception message indicating why the\n                  corresponding action of a transaction request\n                  failed.\n               ')


    _ElementMap = {
        __Action.name() : __Action
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'TransactionResultsType', TransactionResultsType)


# Complex type PropertyType with content type ELEMENT_ONLY
class PropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'PropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}Name uses Python identifier Name
    __Name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Name'), 'Name', '__httpwww_opengis_netwfs_PropertyType_httpwww_opengis_netwfsName', False)

    
    Name = property(__Name.value, __Name.set, None, u'\n                  The Name element contains the name of a feature property\n                  to be updated.\n               ')

    
    # Element {http://www.opengis.net/wfs}Value uses Python identifier Value
    __Value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Value'), 'Value', '__httpwww_opengis_netwfs_PropertyType_httpwww_opengis_netwfsValue', False)

    
    Value = property(__Value.value, __Value.set, None, u'\n                  The Value element contains the replacement value for the\n                  named property.\n               ')


    _ElementMap = {
        __Name.name() : __Name,
        __Value.name() : __Value
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'PropertyType', PropertyType)


# Complex type OperationsType with content type ELEMENT_ONLY
class OperationsType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'OperationsType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}Operation uses Python identifier Operation
    __Operation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Operation'), 'Operation', '__httpwww_opengis_netwfs_OperationsType_httpwww_opengis_netwfsOperation', True)

    
    Operation = property(__Operation.value, __Operation.set, None, None)


    _ElementMap = {
        __Operation.name() : __Operation
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'OperationsType', OperationsType)


# Complex type CTD_ANON with content type EMPTY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }



# Complex type WFS_CapabilitiesType with content type ELEMENT_ONLY
class WFS_CapabilitiesType (pyxb.bundles.opengis.ows.CapabilitiesBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'WFS_CapabilitiesType')
    # Base type is pyxb.bundles.opengis.ows.CapabilitiesBaseType
    
    # Element ServiceIdentification ({http://www.opengis.net/ows}ServiceIdentification) inherited from {http://www.opengis.net/ows}CapabilitiesBaseType
    
    # Element {http://www.opengis.net/wfs}ServesGMLObjectTypeList uses Python identifier ServesGMLObjectTypeList
    __ServesGMLObjectTypeList = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ServesGMLObjectTypeList'), 'ServesGMLObjectTypeList', '__httpwww_opengis_netwfs_WFS_CapabilitiesType_httpwww_opengis_netwfsServesGMLObjectTypeList', False)

    
    ServesGMLObjectTypeList = property(__ServesGMLObjectTypeList.value, __ServesGMLObjectTypeList.set, None, u'\n            List of GML Object types available for GetGmlObject requests\n         ')

    
    # Element OperationsMetadata ({http://www.opengis.net/ows}OperationsMetadata) inherited from {http://www.opengis.net/ows}CapabilitiesBaseType
    
    # Element {http://www.opengis.net/wfs}SupportsGMLObjectTypeList uses Python identifier SupportsGMLObjectTypeList
    __SupportsGMLObjectTypeList = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'SupportsGMLObjectTypeList'), 'SupportsGMLObjectTypeList', '__httpwww_opengis_netwfs_WFS_CapabilitiesType_httpwww_opengis_netwfsSupportsGMLObjectTypeList', False)

    
    SupportsGMLObjectTypeList = property(__SupportsGMLObjectTypeList.value, __SupportsGMLObjectTypeList.set, None, u'\n            List of GML Object types that WFS is capable of serving, either\n            directly, or as validly derived types defined in a GML application\n            schema.\n         ')

    
    # Element ServiceProvider ({http://www.opengis.net/ows}ServiceProvider) inherited from {http://www.opengis.net/ows}CapabilitiesBaseType
    
    # Element {http://www.opengis.net/wfs}FeatureTypeList uses Python identifier FeatureTypeList
    __FeatureTypeList = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'FeatureTypeList'), 'FeatureTypeList', '__httpwww_opengis_netwfs_WFS_CapabilitiesType_httpwww_opengis_netwfsFeatureTypeList', False)

    
    FeatureTypeList = property(__FeatureTypeList.value, __FeatureTypeList.set, None, None)

    
    # Element {http://www.opengis.net/ogc}Filter_Capabilities uses Python identifier Filter_Capabilities
    __Filter_Capabilities = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter_Capabilities'), 'Filter_Capabilities', '__httpwww_opengis_netwfs_WFS_CapabilitiesType_httpwww_opengis_netogcFilter_Capabilities', False)

    
    Filter_Capabilities = property(__Filter_Capabilities.value, __Filter_Capabilities.set, None, None)

    
    # Attribute updateSequence inherited from {http://www.opengis.net/ows}CapabilitiesBaseType
    
    # Attribute version inherited from {http://www.opengis.net/ows}CapabilitiesBaseType

    _ElementMap = pyxb.bundles.opengis.ows.CapabilitiesBaseType._ElementMap.copy()
    _ElementMap.update({
        __ServesGMLObjectTypeList.name() : __ServesGMLObjectTypeList,
        __SupportsGMLObjectTypeList.name() : __SupportsGMLObjectTypeList,
        __FeatureTypeList.name() : __FeatureTypeList,
        __Filter_Capabilities.name() : __Filter_Capabilities
    })
    _AttributeMap = pyxb.bundles.opengis.ows.CapabilitiesBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'WFS_CapabilitiesType', WFS_CapabilitiesType)


# Complex type TransactionResponseType with content type ELEMENT_ONLY
class TransactionResponseType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TransactionResponseType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}TransactionResults uses Python identifier TransactionResults
    __TransactionResults = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TransactionResults'), 'TransactionResults', '__httpwww_opengis_netwfs_TransactionResponseType_httpwww_opengis_netwfsTransactionResults', False)

    
    TransactionResults = property(__TransactionResults.value, __TransactionResults.set, None, u'\n                  For systems that do not support atomic transactions,\n                  the TransactionResults element may be used to report\n                  exception codes and messages for all actions of a\n                  transaction that failed to execute successfully.\n               ')

    
    # Element {http://www.opengis.net/wfs}InsertResults uses Python identifier InsertResults
    __InsertResults = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'InsertResults'), 'InsertResults', '__httpwww_opengis_netwfs_TransactionResponseType_httpwww_opengis_netwfsInsertResults', False)

    
    InsertResults = property(__InsertResults.value, __InsertResults.set, None, u'\n                  A transaction is a collection of Insert,Update and Delete\n                  actions.  The Update and Delete actions modify features\n                  that already exist.  The Insert action, however, creates\n                  new features.  The InsertResults element is used to\n                  report the identifiers of the newly created features.\n               ')

    
    # Element {http://www.opengis.net/wfs}TransactionSummary uses Python identifier TransactionSummary
    __TransactionSummary = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'TransactionSummary'), 'TransactionSummary', '__httpwww_opengis_netwfs_TransactionResponseType_httpwww_opengis_netwfsTransactionSummary', False)

    
    TransactionSummary = property(__TransactionSummary.value, __TransactionSummary.set, None, u'\n                  The TransactionSummary element is used to summarize\n                  the number of feature instances affected by the \n                  transaction.\n               ')

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpwww_opengis_netwfs_TransactionResponseType_version', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'1.1.0', required=True)
    
    version = property(__version.value, __version.set, None, u'\n               The version attribute contains the version of the request\n               that generated this response.  So a V1.1.0 transaction\n               request generates a V1.1.0 transaction response.\n            ')


    _ElementMap = {
        __TransactionResults.name() : __TransactionResults,
        __InsertResults.name() : __InsertResults,
        __TransactionSummary.name() : __TransactionSummary
    }
    _AttributeMap = {
        __version.name() : __version
    }
Namespace.addCategoryObject('typeBinding', u'TransactionResponseType', TransactionResponseType)


# Complex type FeaturesLockedType with content type ELEMENT_ONLY
class FeaturesLockedType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FeaturesLockedType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}FeatureId uses Python identifier FeatureId
    __FeatureId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'FeatureId'), 'FeatureId', '__httpwww_opengis_netwfs_FeaturesLockedType_httpwww_opengis_netogcFeatureId', True)

    
    FeatureId = property(__FeatureId.value, __FeatureId.set, None, None)


    _ElementMap = {
        __FeatureId.name() : __FeatureId
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'FeaturesLockedType', FeaturesLockedType)


# Complex type GetFeatureWithLockType with content type ELEMENT_ONLY
class GetFeatureWithLockType (BaseRequestType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'GetFeatureWithLockType')
    # Base type is BaseRequestType
    
    # Element {http://www.opengis.net/wfs}Query uses Python identifier Query
    __Query = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Query'), 'Query', '__httpwww_opengis_netwfs_GetFeatureWithLockType_httpwww_opengis_netwfsQuery', True)

    
    Query = property(__Query.value, __Query.set, None, u'\n            The Query element is used to describe a single query.\n            One or more Query elements can be specified inside a\n            GetFeature element so that multiple queries can be \n            executed in one request.  The output from the various\n            queries are combined in a wfs:FeatureCollection element\n            to form the response document.\n         ')

    
    # Attribute traverseXlinkDepth uses Python identifier traverseXlinkDepth
    __traverseXlinkDepth = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'traverseXlinkDepth'), 'traverseXlinkDepth', '__httpwww_opengis_netwfs_GetFeatureWithLockType_traverseXlinkDepth', pyxb.binding.datatypes.string)
    
    traverseXlinkDepth = property(__traverseXlinkDepth.value, __traverseXlinkDepth.set, None, u'\n                     See definition of wfs:GetFeatureType.\n                  ')

    
    # Attribute outputFormat uses Python identifier outputFormat
    __outputFormat = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'outputFormat'), 'outputFormat', '__httpwww_opengis_netwfs_GetFeatureWithLockType_outputFormat', pyxb.binding.datatypes.string, unicode_default=u'text/xml; subtype=gml/3.1.1')
    
    outputFormat = property(__outputFormat.value, __outputFormat.set, None, u'\n                     See definition of wfs:GetFeatureType.\n                  ')

    
    # Attribute expiry uses Python identifier expiry
    __expiry = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'expiry'), 'expiry', '__httpwww_opengis_netwfs_GetFeatureWithLockType_expiry', pyxb.binding.datatypes.positiveInteger, unicode_default=u'5')
    
    expiry = property(__expiry.value, __expiry.set, None, u'\n                     The expiry attribute is used to set the length\n                     of time (expressed in minutes) that features will\n                     remain locked as a result of a GetFeatureWithLock\n                     request.  After the expiry period elapses, the\n                     locked resources must be released.  If the \n                     expiry attribute is not set, then the default\n                     value of 5 minutes will be enforced.\n                  ')

    
    # Attribute traverseXlinkExpiry uses Python identifier traverseXlinkExpiry
    __traverseXlinkExpiry = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'traverseXlinkExpiry'), 'traverseXlinkExpiry', '__httpwww_opengis_netwfs_GetFeatureWithLockType_traverseXlinkExpiry', pyxb.binding.datatypes.positiveInteger)
    
    traverseXlinkExpiry = property(__traverseXlinkExpiry.value, __traverseXlinkExpiry.set, None, u'\n                     See definition of wfs:GetFeatureType.\n                  ')

    
    # Attribute service inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute maxFeatures uses Python identifier maxFeatures
    __maxFeatures = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'maxFeatures'), 'maxFeatures', '__httpwww_opengis_netwfs_GetFeatureWithLockType_maxFeatures', pyxb.binding.datatypes.positiveInteger)
    
    maxFeatures = property(__maxFeatures.value, __maxFeatures.set, None, u'\n                     See definition of wfs:GetFeatureType.\n                  ')

    
    # Attribute handle inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute resultType uses Python identifier resultType
    __resultType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'resultType'), 'resultType', '__httpwww_opengis_netwfs_GetFeatureWithLockType_resultType', ResultTypeType, unicode_default=u'results')
    
    resultType = property(__resultType.value, __resultType.set, None, u'\n                     See definition of wfs:GetFeatureType.\n                  ')

    
    # Attribute version inherited from {http://www.opengis.net/wfs}BaseRequestType

    _ElementMap = BaseRequestType._ElementMap.copy()
    _ElementMap.update({
        __Query.name() : __Query
    })
    _AttributeMap = BaseRequestType._AttributeMap.copy()
    _AttributeMap.update({
        __traverseXlinkDepth.name() : __traverseXlinkDepth,
        __outputFormat.name() : __outputFormat,
        __expiry.name() : __expiry,
        __traverseXlinkExpiry.name() : __traverseXlinkExpiry,
        __maxFeatures.name() : __maxFeatures,
        __resultType.name() : __resultType
    })
Namespace.addCategoryObject('typeBinding', u'GetFeatureWithLockType', GetFeatureWithLockType)


# Complex type OutputFormatListType with content type ELEMENT_ONLY
class OutputFormatListType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'OutputFormatListType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}Format uses Python identifier Format
    __Format = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Format'), 'Format', '__httpwww_opengis_netwfs_OutputFormatListType_httpwww_opengis_netwfsFormat', True)

    
    Format = property(__Format.value, __Format.set, None, None)


    _ElementMap = {
        __Format.name() : __Format
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'OutputFormatListType', OutputFormatListType)


# Complex type GetFeatureType with content type ELEMENT_ONLY
class GetFeatureType (BaseRequestType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'GetFeatureType')
    # Base type is BaseRequestType
    
    # Element {http://www.opengis.net/wfs}Query uses Python identifier Query
    __Query = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Query'), 'Query', '__httpwww_opengis_netwfs_GetFeatureType_httpwww_opengis_netwfsQuery', True)

    
    Query = property(__Query.value, __Query.set, None, u'\n            The Query element is used to describe a single query.\n            One or more Query elements can be specified inside a\n            GetFeature element so that multiple queries can be \n            executed in one request.  The output from the various\n            queries are combined in a wfs:FeatureCollection element\n            to form the response document.\n         ')

    
    # Attribute traverseXlinkExpiry uses Python identifier traverseXlinkExpiry
    __traverseXlinkExpiry = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'traverseXlinkExpiry'), 'traverseXlinkExpiry', '__httpwww_opengis_netwfs_GetFeatureType_traverseXlinkExpiry', pyxb.binding.datatypes.positiveInteger)
    
    traverseXlinkExpiry = property(__traverseXlinkExpiry.value, __traverseXlinkExpiry.set, None, u'\n                     The traverseXlinkExpiry attribute value is specified in\n                     minutes.  It indicates how long a Web Feature Service\n                     should wait to receive a response to a nested GetGmlObject\n                     request.\t\n                     This attribute is only relevant if a value is specified \n                     for the traverseXlinkDepth attribute.\n                  ')

    
    # Attribute service inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute maxFeatures uses Python identifier maxFeatures
    __maxFeatures = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'maxFeatures'), 'maxFeatures', '__httpwww_opengis_netwfs_GetFeatureType_maxFeatures', pyxb.binding.datatypes.positiveInteger)
    
    maxFeatures = property(__maxFeatures.value, __maxFeatures.set, None, u'\n                     The maxFeatures attribute is used to specify the maximum\n                     number of features that a GetFeature operation should\n                     generate (regardless of the actual number of query hits).\n                  ')

    
    # Attribute version inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute resultType uses Python identifier resultType
    __resultType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'resultType'), 'resultType', '__httpwww_opengis_netwfs_GetFeatureType_resultType', ResultTypeType, unicode_default=u'results')
    
    resultType = property(__resultType.value, __resultType.set, None, u'\n                     The resultType attribute is used to indicate\n                     what response a WFS should return to user once\n                     a GetFeature request is processed.\n                     Possible values are:\n                        results - meaning that the full response set\n                                  (i.e. all the feature instances) \n                                  should be returned.\n                        hits    - meaning that an empty response set\n                                  should be returned (i.e. no feature\n                                  instances should be returned) but\n                                  the "numberOfFeatures" attribute\n                                  should be set to the number of feature\n                                  instances that would be returned.\n                  ')

    
    # Attribute traverseXlinkDepth uses Python identifier traverseXlinkDepth
    __traverseXlinkDepth = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'traverseXlinkDepth'), 'traverseXlinkDepth', '__httpwww_opengis_netwfs_GetFeatureType_traverseXlinkDepth', pyxb.binding.datatypes.string)
    
    traverseXlinkDepth = property(__traverseXlinkDepth.value, __traverseXlinkDepth.set, None, u'\n                     This attribute indicates the depth to which nested property\n                     XLink linking element locator attribute (href) XLinks are\n                     traversed and resolved if possible.  A value of "1"\n                     indicates that one linking element locator attribute\n                     (href) Xlink will be traversed and the referenced element\n                     returned if possible, but nested property XLink linking\n                     element locator attribute (href) XLinks in the returned\n                     element are not traversed.  A value of "*" indicates that\n                     all nested property XLink linking element locator attribute\n                     (href) XLinks will be traversed and the referenced elements\n                     returned if possible.  The range of valid values for this\n                     attribute consists of positive integers plus "*".\n                     If this attribute is not specified then no xlinks shall be \n                     resolved and the value of traverseXlinkExpiry attribute (if\n                     it specified) may be ignored.\n                  ')

    
    # Attribute handle inherited from {http://www.opengis.net/wfs}BaseRequestType
    
    # Attribute outputFormat uses Python identifier outputFormat
    __outputFormat = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'outputFormat'), 'outputFormat', '__httpwww_opengis_netwfs_GetFeatureType_outputFormat', pyxb.binding.datatypes.string, unicode_default=u'text/xml; subtype=gml/3.1.1')
    
    outputFormat = property(__outputFormat.value, __outputFormat.set, None, u"\n                     The outputFormat attribute is used to specify the output\n                     format that the Web Feature Service should generate in\n                     response to a GetFeature or GetFeatureWithLock element.\n                     The default value of 'text/xml; subtype=gml/3.1.1'\n                     indicates that the output is an XML document that\n                     conforms to the Geography Markup Language (GML)\n                     Implementation Specification V3.1.1.\n                     For the purposes of experimentation, vendor extension,\n                     or even extensions that serve a specific community of\n                     interest, other acceptable output format values may be\n                     used to specify other formats as long as those values\n                     are advertised in the capabilities document.\n                     For example, the value WKB may be used to indicate that a \n                     Well Known Binary format be used to encode the output.\n                  ")


    _ElementMap = BaseRequestType._ElementMap.copy()
    _ElementMap.update({
        __Query.name() : __Query
    })
    _AttributeMap = BaseRequestType._AttributeMap.copy()
    _AttributeMap.update({
        __traverseXlinkExpiry.name() : __traverseXlinkExpiry,
        __maxFeatures.name() : __maxFeatures,
        __resultType.name() : __resultType,
        __traverseXlinkDepth.name() : __traverseXlinkDepth,
        __outputFormat.name() : __outputFormat
    })
Namespace.addCategoryObject('typeBinding', u'GetFeatureType', GetFeatureType)


# Complex type CTD_ANON_ with content type SIMPLE
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute traverseXlinkExpiry uses Python identifier traverseXlinkExpiry
    __traverseXlinkExpiry = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'traverseXlinkExpiry'), 'traverseXlinkExpiry', '__httpwww_opengis_netwfs_CTD_ANON__traverseXlinkExpiry', pyxb.binding.datatypes.positiveInteger)
    
    traverseXlinkExpiry = property(__traverseXlinkExpiry.value, __traverseXlinkExpiry.set, None, u'\n                  The traverseXlinkExpiry attribute value is specified in\n                  minutes It indicates how long a Web Feature Service should\n                  wait to receive a response to a nested GetGmlObject request.\t\n                     ')

    
    # Attribute traverseXlinkDepth uses Python identifier traverseXlinkDepth
    __traverseXlinkDepth = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'traverseXlinkDepth'), 'traverseXlinkDepth', '__httpwww_opengis_netwfs_CTD_ANON__traverseXlinkDepth', pyxb.binding.datatypes.string, required=True)
    
    traverseXlinkDepth = property(__traverseXlinkDepth.value, __traverseXlinkDepth.set, None, u'\n                  This attribute indicates the depth to which nested property\n                  XLink linking element locator attribute (href) XLinks are\n                  traversed and resolved if possible.  A value of "1" indicates\n                  that one linking element locator attribute (href) Xlink\n                  will be traversed and the referenced element returned if\n                  possible, but nested property XLink linking element locator\n                  attribute (href) XLinks in the returned element are not\n                  traversed.  A value of  "*" indicates that all nested property\n                  XLink linking element locator attribute (href) XLinks will be\n                  traversed and the referenced elements returned if possible.\n                  The range of valid values for this attribute consists of\n                  positive integers plus "*".\n                     ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __traverseXlinkExpiry.name() : __traverseXlinkExpiry,
        __traverseXlinkDepth.name() : __traverseXlinkDepth
    }



# Complex type ActionType with content type ELEMENT_ONLY
class ActionType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ActionType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}Message uses Python identifier Message
    __Message = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Message'), 'Message', '__httpwww_opengis_netwfs_ActionType_httpwww_opengis_netwfsMessage', False)

    
    Message = property(__Message.value, __Message.set, None, u'\n                  If an action fails, the message element may be used\n                  to supply an exception message.\n               ')

    
    # Attribute locator uses Python identifier locator
    __locator = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'locator'), 'locator', '__httpwww_opengis_netwfs_ActionType_locator', pyxb.binding.datatypes.string, required=True)
    
    locator = property(__locator.value, __locator.set, None, u'\n               The locator attribute is used to locate an action \n               within a <Transaction> element.  The value\n               of the locator attribute is either a string that\n               is equal to the value of the handle attribute\n               specified on an  <Insert>, <Update>\n               or <Delete> action.  If a value is not \n               specified for the handle attribute then a WFS \n               may employ some other means of locating the \n               action.  For example, the value of the locator\n               attribute may be an integer indicating the order\n               of the action (i.e. 1=First action, 2=Second action,\n               etc.).\n            ')

    
    # Attribute code uses Python identifier code
    __code = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'code'), 'code', '__httpwww_opengis_netwfs_ActionType_code', pyxb.binding.datatypes.string)
    
    code = property(__code.value, __code.set, None, u'\n               The code attribute may be used to specify an \n               exception code indicating why an action failed.\n            ')


    _ElementMap = {
        __Message.name() : __Message
    }
    _AttributeMap = {
        __locator.name() : __locator,
        __code.name() : __code
    }
Namespace.addCategoryObject('typeBinding', u'ActionType', ActionType)


# Complex type FeatureCollectionType with content type ELEMENT_ONLY
class FeatureCollectionType (pyxb.bundles.opengis.gml.AbstractFeatureCollectionType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FeatureCollectionType')
    # Base type is pyxb.bundles.opengis.gml.AbstractFeatureCollectionType
    
    # Element featureMember ({http://www.opengis.net/gml}featureMember) inherited from {http://www.opengis.net/gml}AbstractFeatureCollectionType
    
    # Element featureMembers ({http://www.opengis.net/gml}featureMembers) inherited from {http://www.opengis.net/gml}AbstractFeatureCollectionType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element location ({http://www.opengis.net/gml}location) inherited from {http://www.opengis.net/gml}AbstractFeatureType
    
    # Element boundedBy ({http://www.opengis.net/gml}boundedBy) inherited from {http://www.opengis.net/gml}AbstractFeatureType
    
    # Attribute timeStamp uses Python identifier timeStamp
    __timeStamp = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'timeStamp'), 'timeStamp', '__httpwww_opengis_netwfs_FeatureCollectionType_timeStamp', pyxb.binding.datatypes.dateTime)
    
    timeStamp = property(__timeStamp.value, __timeStamp.set, None, u'\n                  The timeStamp attribute should contain the date and time\n                  that the response was generated.\n               ')

    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute lockId uses Python identifier lockId
    __lockId = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'lockId'), 'lockId', '__httpwww_opengis_netwfs_FeatureCollectionType_lockId', pyxb.binding.datatypes.string)
    
    lockId = property(__lockId.value, __lockId.set, None, u'\n                  The value of the lockId attribute is an identifier\n                  that a Web Feature Service generates when responding\n                  to a GetFeatureWithLock request.  A client application\n                  can use this value in subsequent operations (such as a\n                  Transaction request) to reference the set of locked\n                  features.\n               ')

    
    # Attribute numberOfFeatures uses Python identifier numberOfFeatures
    __numberOfFeatures = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'numberOfFeatures'), 'numberOfFeatures', '__httpwww_opengis_netwfs_FeatureCollectionType_numberOfFeatures', pyxb.binding.datatypes.nonNegativeInteger)
    
    numberOfFeatures = property(__numberOfFeatures.value, __numberOfFeatures.set, None, u'\n                  The numberOfFeatures attribute should contain a\n                  count of the number of features in the response.\n                  That is a count of all features elements dervied\n                  from gml:AbstractFeatureType.\n               ')


    _ElementMap = pyxb.bundles.opengis.gml.AbstractFeatureCollectionType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = pyxb.bundles.opengis.gml.AbstractFeatureCollectionType._AttributeMap.copy()
    _AttributeMap.update({
        __timeStamp.name() : __timeStamp,
        __lockId.name() : __lockId,
        __numberOfFeatures.name() : __numberOfFeatures
    })
Namespace.addCategoryObject('typeBinding', u'FeatureCollectionType', FeatureCollectionType)


# Complex type FeatureTypeListType with content type ELEMENT_ONLY
class FeatureTypeListType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'FeatureTypeListType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/wfs}FeatureType uses Python identifier FeatureType
    __FeatureType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'FeatureType'), 'FeatureType', '__httpwww_opengis_netwfs_FeatureTypeListType_httpwww_opengis_netwfsFeatureType', True)

    
    FeatureType = property(__FeatureType.value, __FeatureType.set, None, None)

    
    # Element {http://www.opengis.net/wfs}Operations uses Python identifier Operations
    __Operations = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Operations'), 'Operations', '__httpwww_opengis_netwfs_FeatureTypeListType_httpwww_opengis_netwfsOperations', False)

    
    Operations = property(__Operations.value, __Operations.set, None, None)


    _ElementMap = {
        __FeatureType.name() : __FeatureType,
        __Operations.name() : __Operations
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'FeatureTypeListType', FeatureTypeListType)


PropertyName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'PropertyName'), pyxb.binding.datatypes.string, documentation=u'\n            The Property element is used to specify one or more\n            properties of a feature whose values are to be retrieved\n            by a Web Feature Service.\n\n            While a Web Feature Service should endeavour to satisfy\n            the exact request specified, in some instance this may\n            not be possible.  Specifically, a Web Feature Service\n            must generate a valid GML3 response to a Query operation.\n            The schema used to generate the output may include\n            properties that are mandatory.  In order that the output\n            validates, these mandatory properties must be specified\n            in the request.  If they are not, a Web Feature Service\n            may add them automatically to the Query before processing\n            it.  Thus a client application should, in general, be\n            prepared to receive more properties than it requested.\n\n            Of course, using the DescribeFeatureType request, a client\n            application can determine which properties are mandatory\n            and request them in the first place.\n         ')
Namespace.addCategoryObject('elementBinding', PropertyName.name().localName(), PropertyName)

GetGmlObject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetGmlObject'), GetGmlObjectType, documentation=u'\n            The GetGmlObject element is used to request that a Web Feature\n            Service return an element with a gml:id attribute value specified\n            by an ogc:GmlObjectId.\n         ')
Namespace.addCategoryObject('elementBinding', GetGmlObject.name().localName(), GetGmlObject)

ServesGMLObjectTypeList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ServesGMLObjectTypeList'), GMLObjectTypeListType, documentation=u'\n            List of GML Object types available for GetGmlObject requests\n         ')
Namespace.addCategoryObject('elementBinding', ServesGMLObjectTypeList.name().localName(), ServesGMLObjectTypeList)

Transaction = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Transaction'), TransactionType, documentation=u'\n            This is the root element for a Transaction request.\n            A transaction request allows insert, update and \n            delete operations to be performed to create, change\n            or remove feature instances.\n         ')
Namespace.addCategoryObject('elementBinding', Transaction.name().localName(), Transaction)

Query = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Query'), QueryType, documentation=u'\n            The Query element is used to describe a single query.\n            One or more Query elements can be specified inside a\n            GetFeature element so that multiple queries can be \n            executed in one request.  The output from the various\n            queries are combined in a wfs:FeatureCollection element\n            to form the response document.\n         ')
Namespace.addCategoryObject('elementBinding', Query.name().localName(), Query)

Delete = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Delete'), DeleteElementType, documentation=u'\n            The Delete element is used to indicate that one or more\n            feature instances should be removed from the feature\n            repository.\n         ')
Namespace.addCategoryObject('elementBinding', Delete.name().localName(), Delete)

LockFeatureResponse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'LockFeatureResponse'), LockFeatureResponseType, documentation=u'\n            The LockFeatureResponse element contains a report\n            about the completion status of a LockFeature request.\n         ')
Namespace.addCategoryObject('elementBinding', LockFeatureResponse.name().localName(), LockFeatureResponse)

DescribeFeatureType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DescribeFeatureType'), DescribeFeatureTypeType, documentation=u'\n            The DescribeFeatureType element is used to request that a Web\n            Feature Service generate a document describing one or more \n            feature types.\n         ')
Namespace.addCategoryObject('elementBinding', DescribeFeatureType.name().localName(), DescribeFeatureType)

LockFeature = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'LockFeature'), LockFeatureType, documentation=u'\n            This is the root element for a LockFeature request.\n            The LockFeature request can be used to lock one or\n            more feature instances.\n         ')
Namespace.addCategoryObject('elementBinding', LockFeature.name().localName(), LockFeature)

GetCapabilities = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetCapabilities'), GetCapabilitiesType)
Namespace.addCategoryObject('elementBinding', GetCapabilities.name().localName(), GetCapabilities)

Property = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Property'), PropertyType, documentation=u'\n            The Property element is used to specify the new\n            value of a feature property inside an Update\n            element.\n         ')
Namespace.addCategoryObject('elementBinding', Property.name().localName(), Property)

Native = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Native'), NativeType, documentation=u'\n            Many times, a Web Feature Service interacts with a repository\n            that may have special vendor specific capabilities.  The native\n            element allows vendor specific command to be passed to the\n            repository via the Web Feature Service.\n         ')
Namespace.addCategoryObject('elementBinding', Native.name().localName(), Native)

WFS_Capabilities = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'WFS_Capabilities'), WFS_CapabilitiesType)
Namespace.addCategoryObject('elementBinding', WFS_Capabilities.name().localName(), WFS_Capabilities)

TransactionResponse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TransactionResponse'), TransactionResponseType, documentation=u'\n            The TransactionResponse element contains a report\n            about the completion status of a Transaction operation.  \n         ')
Namespace.addCategoryObject('elementBinding', TransactionResponse.name().localName(), TransactionResponse)

GetFeatureWithLock = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetFeatureWithLock'), GetFeatureWithLockType, documentation=u'\n            This is the root element for the GetFeatureWithLock request.\n            The GetFeatureWithLock operation performs identically to a\n            GetFeature request except that the GetFeatureWithLock request\n            locks all the feature instances in the result set and returns\n            a lock identifier to a client application in the response.\n            The lock identifier is returned to the client application \n            using the lockId attribute define on the wfs:FeatureCollection\n            element.\n         ')
Namespace.addCategoryObject('elementBinding', GetFeatureWithLock.name().localName(), GetFeatureWithLock)

GetFeature = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetFeature'), GetFeatureType, documentation=u'\n            The GetFeature element is used to request that a Web Feature\n            Service return feature type instances of one or more feature\n            types.\n         ')
Namespace.addCategoryObject('elementBinding', GetFeature.name().localName(), GetFeature)

LockId = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'LockId'), pyxb.binding.datatypes.string, documentation=u'\n            The LockId element contains the value of the lock identifier\n            obtained by a client application from a previous GetFeatureWithLock\n            or LockFeature request.\n         ')
Namespace.addCategoryObject('elementBinding', LockId.name().localName(), LockId)

SupportsGMLObjectTypeList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SupportsGMLObjectTypeList'), GMLObjectTypeListType, documentation=u'\n            List of GML Object types that WFS is capable of serving, either\n            directly, or as validly derived types defined in a GML application\n            schema.\n         ')
Namespace.addCategoryObject('elementBinding', SupportsGMLObjectTypeList.name().localName(), SupportsGMLObjectTypeList)

FeatureCollection = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FeatureCollection'), FeatureCollectionType, documentation=u'\n            This element is a container for the response to a GetFeature\n            or GetFeatureWithLock (WFS-transaction.xsd) request.\n         ')
Namespace.addCategoryObject('elementBinding', FeatureCollection.name().localName(), FeatureCollection)

XlinkPropertyName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'XlinkPropertyName'), CTD_ANON_, documentation=u'\n            This element may be used in place of an wfs:PropertyName element\n            in a wfs:Query element in a wfs:GetFeature element to selectively\n            request the traversal of nested XLinks in the returned element for\n            the named property. This element may not be used in other requests\n            -- GetFeatureWithLock, LockFeature, Insert, Update, Delete -- in\n            this version of the WFS specification.\n         ')
Namespace.addCategoryObject('elementBinding', XlinkPropertyName.name().localName(), XlinkPropertyName)

Update = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Update'), UpdateElementType, documentation=u'\n            One or more existing feature instances can be changed by\n            using the Update element.\n         ')
Namespace.addCategoryObject('elementBinding', Update.name().localName(), Update)

FeatureTypeList = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FeatureTypeList'), FeatureTypeListType)
Namespace.addCategoryObject('elementBinding', FeatureTypeList.name().localName(), FeatureTypeList)

Insert = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Insert'), InsertElementType, documentation=u'\n            The Insert element is used to indicate that the Web Feature\n            Service should create a new instance of a feature type.  The\n            feature instance is specified using GML3 and one or more \n            feature instances to be created can be contained inside the\n            Insert element.\n         ')
Namespace.addCategoryObject('elementBinding', Insert.name().localName(), Insert)



GetGmlObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'GmlObjectId'), pyxb.bundles.opengis.filter.GmlObjectIdType, scope=GetGmlObjectType))
GetGmlObjectType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GetGmlObjectType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'GmlObjectId')), min_occurs=1, max_occurs=1)
    )
GetGmlObjectType._ContentModel = pyxb.binding.content.ParticleModel(GetGmlObjectType._GroupModel, min_occurs=1, max_occurs=1)



GMLObjectTypeListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GMLObjectType'), GMLObjectTypeType, scope=GMLObjectTypeListType, documentation=u'\n                  Name of this GML object type, including any namespace prefix\n               '))
GMLObjectTypeListType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GMLObjectTypeListType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'GMLObjectType')), min_occurs=1, max_occurs=None)
    )
GMLObjectTypeListType._ContentModel = pyxb.binding.content.ParticleModel(GMLObjectTypeListType._GroupModel, min_occurs=1, max_occurs=1)



QueryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'SortBy'), pyxb.bundles.opengis.filter.SortByType, scope=QueryType))

QueryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter'), pyxb.bundles.opengis.filter.FilterType, scope=QueryType))

QueryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'XlinkPropertyName'), CTD_ANON_, scope=QueryType, documentation=u'\n            This element may be used in place of an wfs:PropertyName element\n            in a wfs:Query element in a wfs:GetFeature element to selectively\n            request the traversal of nested XLinks in the returned element for\n            the named property. This element may not be used in other requests\n            -- GetFeatureWithLock, LockFeature, Insert, Update, Delete -- in\n            this version of the WFS specification.\n         '))

QueryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Function'), pyxb.bundles.opengis.filter.FunctionType, scope=QueryType))

QueryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'PropertyName'), pyxb.binding.datatypes.string, scope=QueryType, documentation=u'\n            The Property element is used to specify one or more\n            properties of a feature whose values are to be retrieved\n            by a Web Feature Service.\n\n            While a Web Feature Service should endeavour to satisfy\n            the exact request specified, in some instance this may\n            not be possible.  Specifically, a Web Feature Service\n            must generate a valid GML3 response to a Query operation.\n            The schema used to generate the output may include\n            properties that are mandatory.  In order that the output\n            validates, these mandatory properties must be specified\n            in the request.  If they are not, a Web Feature Service\n            may add them automatically to the Query before processing\n            it.  Thus a client application should, in general, be\n            prepared to receive more properties than it requested.\n\n            Of course, using the DescribeFeatureType request, a client\n            application can determine which properties are mandatory\n            and request them in the first place.\n         '))
QueryType._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(QueryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'PropertyName')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(QueryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'XlinkPropertyName')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(QueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Function')), min_occurs=1, max_occurs=1)
    )
QueryType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(QueryType._GroupModel_, min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(QueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter')), min_occurs=0L, max_occurs=1L),
    pyxb.binding.content.ParticleModel(QueryType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'SortBy')), min_occurs=0L, max_occurs=1L)
    )
QueryType._ContentModel = pyxb.binding.content.ParticleModel(QueryType._GroupModel, min_occurs=1, max_occurs=1)



TransactionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Delete'), DeleteElementType, scope=TransactionType, documentation=u'\n            The Delete element is used to indicate that one or more\n            feature instances should be removed from the feature\n            repository.\n         '))

TransactionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Insert'), InsertElementType, scope=TransactionType, documentation=u'\n            The Insert element is used to indicate that the Web Feature\n            Service should create a new instance of a feature type.  The\n            feature instance is specified using GML3 and one or more \n            feature instances to be created can be contained inside the\n            Insert element.\n         '))

TransactionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Update'), UpdateElementType, scope=TransactionType, documentation=u'\n            One or more existing feature instances can be changed by\n            using the Update element.\n         '))

TransactionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Native'), NativeType, scope=TransactionType, documentation=u'\n            Many times, a Web Feature Service interacts with a repository\n            that may have special vendor specific capabilities.  The native\n            element allows vendor specific command to be passed to the\n            repository via the Web Feature Service.\n         '))

TransactionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'LockId'), pyxb.binding.datatypes.string, scope=TransactionType, documentation=u'\n            The LockId element contains the value of the lock identifier\n            obtained by a client application from a previous GetFeatureWithLock\n            or LockFeature request.\n         '))
TransactionType._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(TransactionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Insert')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TransactionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Update')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TransactionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Delete')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TransactionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Native')), min_occurs=1, max_occurs=1)
    )
TransactionType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TransactionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'LockId')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TransactionType._GroupModel_, min_occurs=0L, max_occurs=None)
    )
TransactionType._ContentModel = pyxb.binding.content.ParticleModel(TransactionType._GroupModel, min_occurs=1, max_occurs=1)



DeleteElementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter'), pyxb.bundles.opengis.filter.FilterType, scope=DeleteElementType))
DeleteElementType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DeleteElementType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter')), min_occurs=1L, max_occurs=1L)
    )
DeleteElementType._ContentModel = pyxb.binding.content.ParticleModel(DeleteElementType._GroupModel, min_occurs=1, max_occurs=1)



TransactionSummaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'totalDeleted'), pyxb.binding.datatypes.nonNegativeInteger, scope=TransactionSummaryType))

TransactionSummaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'totalUpdated'), pyxb.binding.datatypes.nonNegativeInteger, scope=TransactionSummaryType))

TransactionSummaryType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'totalInserted'), pyxb.binding.datatypes.nonNegativeInteger, scope=TransactionSummaryType))
TransactionSummaryType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TransactionSummaryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'totalInserted')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TransactionSummaryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'totalUpdated')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TransactionSummaryType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'totalDeleted')), min_occurs=0L, max_occurs=1)
    )
TransactionSummaryType._ContentModel = pyxb.binding.content.ParticleModel(TransactionSummaryType._GroupModel, min_occurs=1, max_occurs=1)



LockType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter'), pyxb.bundles.opengis.filter.FilterType, scope=LockType))
LockType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(LockType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter')), min_occurs=0L, max_occurs=1L)
    )
LockType._ContentModel = pyxb.binding.content.ParticleModel(LockType._GroupModel, min_occurs=1, max_occurs=1)



GMLObjectTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'Keywords'), pyxb.bundles.opengis.ows.KeywordsType, scope=GMLObjectTypeType))

GMLObjectTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OutputFormats'), OutputFormatListType, scope=GMLObjectTypeType))

GMLObjectTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Title'), pyxb.binding.datatypes.string, scope=GMLObjectTypeType, documentation=u'\n                  Title of this GML Object type, normally used for display\n                  to a human.\n               '))

GMLObjectTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Name'), pyxb.binding.datatypes.QName, scope=GMLObjectTypeType, documentation=u'\n                  Name of this GML Object type, including any namespace prefix.\n               '))

GMLObjectTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Abstract'), pyxb.binding.datatypes.string, scope=GMLObjectTypeType, documentation=u'\n                  Brief narrative description of this GML Object type, normally\n                  used for display to a human.\n               '))
GMLObjectTypeType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GMLObjectTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Name')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(GMLObjectTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Title')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GMLObjectTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Abstract')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GMLObjectTypeType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'Keywords')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(GMLObjectTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'OutputFormats')), min_occurs=0L, max_occurs=1)
    )
GMLObjectTypeType._ContentModel = pyxb.binding.content.ParticleModel(GMLObjectTypeType._GroupModel, min_occurs=1, max_occurs=1)



InsertResultsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Feature'), InsertedFeatureType, scope=InsertResultsType))
InsertResultsType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(InsertResultsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Feature')), min_occurs=1, max_occurs=None)
    )
InsertResultsType._ContentModel = pyxb.binding.content.ParticleModel(InsertResultsType._GroupModel, min_occurs=1, max_occurs=1)



LockFeatureResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FeaturesNotLocked'), FeaturesNotLockedType, scope=LockFeatureResponseType, documentation=u'\n                  In contrast to the FeaturesLocked element, the\n                  FeaturesNotLocked element contains a list of \n                  ogc:Filter elements identifying feature instances\n                  that a WFS did not manage to lock because they were\n                  already locked by another process.\n               '))

LockFeatureResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FeaturesLocked'), FeaturesLockedType, scope=LockFeatureResponseType, documentation=u'\n                  The LockFeature or GetFeatureWithLock operations\n                  identify and attempt to lock a set of feature \n                  instances that satisfy the constraints specified \n                  in the request.  In the event that the lockAction\n                  attribute (on the LockFeature or GetFeatureWithLock\n                  elements) is set to SOME, a Web Feature Service will\n                  attempt to lock as many of the feature instances from\n                  the result set as possible.\n\n                  The FeaturesLocked element contains list of ogc:FeatureId\n                  elements enumerating the feature instances that a WFS\n                  actually managed to lock.\n               '))

LockFeatureResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'LockId'), pyxb.binding.datatypes.string, scope=LockFeatureResponseType, documentation=u'\n            The LockId element contains the value of the lock identifier\n            obtained by a client application from a previous GetFeatureWithLock\n            or LockFeature request.\n         '))
LockFeatureResponseType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(LockFeatureResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'LockId')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(LockFeatureResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'FeaturesLocked')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(LockFeatureResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'FeaturesNotLocked')), min_occurs=0L, max_occurs=1)
    )
LockFeatureResponseType._ContentModel = pyxb.binding.content.ParticleModel(LockFeatureResponseType._GroupModel, min_occurs=1, max_occurs=1)



InsertElementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_Feature'), pyxb.bundles.opengis.gml.AbstractFeatureType, abstract=pyxb.binding.datatypes.boolean(1), scope=InsertElementType))
InsertElementType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(InsertElementType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'_Feature')), min_occurs=1, max_occurs=None)
    )
InsertElementType._ContentModel = pyxb.binding.content.ParticleModel(InsertElementType._GroupModel, min_occurs=1, max_occurs=1)



FeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OutputFormats'), OutputFormatListType, scope=FeatureTypeType))

FeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DefaultSRS'), pyxb.binding.datatypes.anyURI, scope=FeatureTypeType, documentation=u'\n                        The DefaultSRS element indicated which spatial\n                        reference system shall be used by a WFS to\n                        express the state of a spatial feature if not\n                        otherwise explicitly identified within a query\n                        or transaction request.  The SRS may be indicated\n                        using either the EPSG form (EPSG:posc code) or\n                        the URL form defined in subclause 4.3.2 of\n                        refernce[2].\n                     '))

FeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'OtherSRS'), pyxb.binding.datatypes.anyURI, scope=FeatureTypeType, documentation=u'\n                        The OtherSRS element is used to indicate other \n                        supported SRSs within query and transaction \n                        operations.  A supported SRS means that the \n                        WFS supports the transformation of spatial\n                        properties between the OtherSRS and the internal\n                        storage SRS.  The effects of such transformations \n                        must be considered when determining and declaring \n                        the guaranteed data accuracy.\n                     '))

FeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'WGS84BoundingBox'), pyxb.bundles.opengis.ows.WGS84BoundingBoxType, scope=FeatureTypeType))

FeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Abstract'), pyxb.binding.datatypes.string, scope=FeatureTypeType, documentation=u'\n                  Brief narrative description of this feature type, normally\n                  used for display to a human.\n               '))

FeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Operations'), OperationsType, scope=FeatureTypeType))

FeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'NoSRS'), CTD_ANON, scope=FeatureTypeType))

FeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'MetadataURL'), MetadataURLType, scope=FeatureTypeType))

FeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Name'), pyxb.binding.datatypes.QName, scope=FeatureTypeType, documentation=u'\n                  Name of this feature type, including any namespace prefix\n               '))

FeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'Keywords'), pyxb.bundles.opengis.ows.KeywordsType, scope=FeatureTypeType))

FeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Title'), pyxb.binding.datatypes.string, scope=FeatureTypeType, documentation=u'\n                  Title of this feature type, normally used for display\n                  to a human.\n               '))
FeatureTypeType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'DefaultSRS')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'OtherSRS')), min_occurs=0L, max_occurs=None)
    )
FeatureTypeType._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(FeatureTypeType._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'NoSRS')), min_occurs=1, max_occurs=1)
    )
FeatureTypeType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Name')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Title')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Abstract')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'Keywords')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(FeatureTypeType._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Operations')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'OutputFormats')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'WGS84BoundingBox')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(FeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'MetadataURL')), min_occurs=0L, max_occurs=None)
    )
FeatureTypeType._ContentModel = pyxb.binding.content.ParticleModel(FeatureTypeType._GroupModel, min_occurs=1, max_occurs=1)



UpdateElementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Property'), PropertyType, scope=UpdateElementType, documentation=u'\n            The Property element is used to specify the new\n            value of a feature property inside an Update\n            element.\n         '))

UpdateElementType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter'), pyxb.bundles.opengis.filter.FilterType, scope=UpdateElementType))
UpdateElementType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(UpdateElementType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Property')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(UpdateElementType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter')), min_occurs=0L, max_occurs=1L)
    )
UpdateElementType._ContentModel = pyxb.binding.content.ParticleModel(UpdateElementType._GroupModel, min_occurs=1, max_occurs=1)



DescribeFeatureTypeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TypeName'), pyxb.binding.datatypes.QName, scope=DescribeFeatureTypeType, documentation=u'\n                        The TypeName element is used to enumerate the\n                        feature types to be described.  If no TypeName\n                        elements are specified then all features should\n                        be described.  The name must be a valid type\n                        that belongs to the feature content as defined\n                        by the GML Application Schema.\n                     '))
DescribeFeatureTypeType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DescribeFeatureTypeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TypeName')), min_occurs=0L, max_occurs=None)
    )
DescribeFeatureTypeType._ContentModel = pyxb.binding.content.ParticleModel(DescribeFeatureTypeType._GroupModel, min_occurs=1, max_occurs=1)



InsertedFeatureType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'FeatureId'), pyxb.bundles.opengis.filter.FeatureIdType, scope=InsertedFeatureType))
InsertedFeatureType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(InsertedFeatureType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'FeatureId')), min_occurs=1, max_occurs=None)
    )
InsertedFeatureType._ContentModel = pyxb.binding.content.ParticleModel(InsertedFeatureType._GroupModel, min_occurs=1, max_occurs=1)



FeaturesNotLockedType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'FeatureId'), pyxb.bundles.opengis.filter.FeatureIdType, scope=FeaturesNotLockedType))
FeaturesNotLockedType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FeaturesNotLockedType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'FeatureId')), min_occurs=1, max_occurs=1)
    )
FeaturesNotLockedType._ContentModel = pyxb.binding.content.ParticleModel(FeaturesNotLockedType._GroupModel, min_occurs=1, max_occurs=None)



LockFeatureType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Lock'), LockType, scope=LockFeatureType, documentation=u'\n                        The lock element is used to indicate which feature \n                        instances of particular type are to be locked.\n                     '))
LockFeatureType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(LockFeatureType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Lock')), min_occurs=1, max_occurs=None)
    )
LockFeatureType._ContentModel = pyxb.binding.content.ParticleModel(LockFeatureType._GroupModel, min_occurs=1, max_occurs=1)


GetCapabilitiesType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GetCapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'AcceptVersions')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GetCapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'Sections')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GetCapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'AcceptFormats')), min_occurs=0L, max_occurs=1)
    )
GetCapabilitiesType._ContentModel = pyxb.binding.content.ParticleModel(GetCapabilitiesType._GroupModel_, min_occurs=1, max_occurs=1)



TransactionResultsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Action'), ActionType, scope=TransactionResultsType, documentation=u'\n                  The Action element reports an exception code\n                  and exception message indicating why the\n                  corresponding action of a transaction request\n                  failed.\n               '))
TransactionResultsType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TransactionResultsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Action')), min_occurs=0L, max_occurs=None)
    )
TransactionResultsType._ContentModel = pyxb.binding.content.ParticleModel(TransactionResultsType._GroupModel, min_occurs=1, max_occurs=1)



PropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Name'), pyxb.binding.datatypes.QName, scope=PropertyType, documentation=u'\n                  The Name element contains the name of a feature property\n                  to be updated.\n               '))

PropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Value'), pyxb.binding.datatypes.anyType, scope=PropertyType, documentation=u'\n                  The Value element contains the replacement value for the\n                  named property.\n               '))
PropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(PropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Name')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(PropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Value')), min_occurs=0L, max_occurs=1)
    )
PropertyType._ContentModel = pyxb.binding.content.ParticleModel(PropertyType._GroupModel, min_occurs=1, max_occurs=1)



OperationsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Operation'), OperationType, scope=OperationsType))
OperationsType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(OperationsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Operation')), min_occurs=1, max_occurs=None)
    )
OperationsType._ContentModel = pyxb.binding.content.ParticleModel(OperationsType._GroupModel, min_occurs=1, max_occurs=1)



WFS_CapabilitiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ServesGMLObjectTypeList'), GMLObjectTypeListType, scope=WFS_CapabilitiesType, documentation=u'\n            List of GML Object types available for GetGmlObject requests\n         '))

WFS_CapabilitiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SupportsGMLObjectTypeList'), GMLObjectTypeListType, scope=WFS_CapabilitiesType, documentation=u'\n            List of GML Object types that WFS is capable of serving, either\n            directly, or as validly derived types defined in a GML application\n            schema.\n         '))

WFS_CapabilitiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FeatureTypeList'), FeatureTypeListType, scope=WFS_CapabilitiesType))

WFS_CapabilitiesType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter_Capabilities'), pyxb.bundles.opengis.filter.CTD_ANON_3, scope=WFS_CapabilitiesType))
WFS_CapabilitiesType._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(WFS_CapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'ServiceIdentification')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(WFS_CapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'ServiceProvider')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(WFS_CapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows'), u'OperationsMetadata')), min_occurs=0L, max_occurs=1)
    )
WFS_CapabilitiesType._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(WFS_CapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'FeatureTypeList')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(WFS_CapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ServesGMLObjectTypeList')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(WFS_CapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SupportsGMLObjectTypeList')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(WFS_CapabilitiesType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Filter_Capabilities')), min_occurs=1, max_occurs=1)
    )
WFS_CapabilitiesType._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(WFS_CapabilitiesType._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(WFS_CapabilitiesType._GroupModel_3, min_occurs=1, max_occurs=1)
    )
WFS_CapabilitiesType._ContentModel = pyxb.binding.content.ParticleModel(WFS_CapabilitiesType._GroupModel_, min_occurs=1, max_occurs=1)



TransactionResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TransactionResults'), TransactionResultsType, scope=TransactionResponseType, documentation=u'\n                  For systems that do not support atomic transactions,\n                  the TransactionResults element may be used to report\n                  exception codes and messages for all actions of a\n                  transaction that failed to execute successfully.\n               '))

TransactionResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InsertResults'), InsertResultsType, scope=TransactionResponseType, documentation=u'\n                  A transaction is a collection of Insert,Update and Delete\n                  actions.  The Update and Delete actions modify features\n                  that already exist.  The Insert action, however, creates\n                  new features.  The InsertResults element is used to\n                  report the identifiers of the newly created features.\n               '))

TransactionResponseType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'TransactionSummary'), TransactionSummaryType, scope=TransactionResponseType, documentation=u'\n                  The TransactionSummary element is used to summarize\n                  the number of feature instances affected by the \n                  transaction.\n               '))
TransactionResponseType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TransactionResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TransactionSummary')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(TransactionResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'TransactionResults')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TransactionResponseType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'InsertResults')), min_occurs=0L, max_occurs=1)
    )
TransactionResponseType._ContentModel = pyxb.binding.content.ParticleModel(TransactionResponseType._GroupModel, min_occurs=1, max_occurs=1)



FeaturesLockedType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'FeatureId'), pyxb.bundles.opengis.filter.FeatureIdType, scope=FeaturesLockedType))
FeaturesLockedType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FeaturesLockedType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'FeatureId')), min_occurs=1, max_occurs=1)
    )
FeaturesLockedType._ContentModel = pyxb.binding.content.ParticleModel(FeaturesLockedType._GroupModel, min_occurs=1, max_occurs=None)



GetFeatureWithLockType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Query'), QueryType, scope=GetFeatureWithLockType, documentation=u'\n            The Query element is used to describe a single query.\n            One or more Query elements can be specified inside a\n            GetFeature element so that multiple queries can be \n            executed in one request.  The output from the various\n            queries are combined in a wfs:FeatureCollection element\n            to form the response document.\n         '))
GetFeatureWithLockType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GetFeatureWithLockType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Query')), min_occurs=1, max_occurs=None)
    )
GetFeatureWithLockType._ContentModel = pyxb.binding.content.ParticleModel(GetFeatureWithLockType._GroupModel, min_occurs=1, max_occurs=1)



OutputFormatListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Format'), pyxb.binding.datatypes.string, scope=OutputFormatListType))
OutputFormatListType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(OutputFormatListType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Format')), min_occurs=1, max_occurs=1)
    )
OutputFormatListType._ContentModel = pyxb.binding.content.ParticleModel(OutputFormatListType._GroupModel, min_occurs=1, max_occurs=None)



GetFeatureType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Query'), QueryType, scope=GetFeatureType, documentation=u'\n            The Query element is used to describe a single query.\n            One or more Query elements can be specified inside a\n            GetFeature element so that multiple queries can be \n            executed in one request.  The output from the various\n            queries are combined in a wfs:FeatureCollection element\n            to form the response document.\n         '))
GetFeatureType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GetFeatureType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Query')), min_occurs=1, max_occurs=None)
    )
GetFeatureType._ContentModel = pyxb.binding.content.ParticleModel(GetFeatureType._GroupModel, min_occurs=1, max_occurs=1)



ActionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Message'), pyxb.binding.datatypes.string, scope=ActionType, documentation=u'\n                  If an action fails, the message element may be used\n                  to supply an exception message.\n               '))
ActionType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ActionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Message')), min_occurs=0L, max_occurs=1L)
    )
ActionType._ContentModel = pyxb.binding.content.ParticleModel(ActionType._GroupModel, min_occurs=1, max_occurs=1)


FeatureCollectionType._GroupModel_9 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FeatureCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(FeatureCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
FeatureCollectionType._GroupModel_8 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FeatureCollectionType._GroupModel_9, min_occurs=1, max_occurs=1)
    )
FeatureCollectionType._GroupModel_10 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FeatureCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'boundedBy')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'location')), min_occurs=0L, max_occurs=1)
    )
FeatureCollectionType._GroupModel_7 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FeatureCollectionType._GroupModel_8, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureCollectionType._GroupModel_10, min_occurs=1, max_occurs=1)
    )
FeatureCollectionType._GroupModel_11 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FeatureCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'featureMember')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(FeatureCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'featureMembers')), min_occurs=0L, max_occurs=1)
    )
FeatureCollectionType._GroupModel_6 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FeatureCollectionType._GroupModel_7, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureCollectionType._GroupModel_11, min_occurs=1, max_occurs=1)
    )
FeatureCollectionType._ContentModel = pyxb.binding.content.ParticleModel(FeatureCollectionType._GroupModel_6, min_occurs=1, max_occurs=1)



FeatureTypeListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FeatureType'), FeatureTypeType, scope=FeatureTypeListType))

FeatureTypeListType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Operations'), OperationsType, scope=FeatureTypeListType))
FeatureTypeListType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(FeatureTypeListType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Operations')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(FeatureTypeListType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'FeatureType')), min_occurs=1, max_occurs=None)
    )
FeatureTypeListType._ContentModel = pyxb.binding.content.ParticleModel(FeatureTypeListType._GroupModel, min_occurs=1, max_occurs=1)

FeatureCollection._setSubstitutionGroup(pyxb.bundles.opengis.gml.FeatureCollection_)
