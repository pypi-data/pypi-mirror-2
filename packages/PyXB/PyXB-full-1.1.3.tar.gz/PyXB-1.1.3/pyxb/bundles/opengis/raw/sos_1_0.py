# ./pyxb/bundles/opengis/raw/sos_1_0.py
# PyXB bindings for NM:174f2064d4c9c2f52a72ce02f36f6f8f371fe8e0
# Generated 2011-09-09 14:19:08.734200 by PyXB version 1.1.3
# Namespace http://www.opengis.net/sos/1.0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9677b688-db18-11e0-a309-001fbc013adc')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.opengis.filter
import pyxb.bundles.opengis.gml
import pyxb.bundles.opengis.swe_1_0_1
import pyxb.bundles.opengis.ows_1_1
import pyxb.bundles.opengis.om_1_0
import pyxb.bundles.opengis._ogc

Namespace = pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/sos/1.0', create_if_missing=True)
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
class responseModeType (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'responseModeType')
    _Documentation = None
responseModeType._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=responseModeType, enum_prefix=None)
responseModeType.inline = responseModeType._CF_enumeration.addEnumeration(unicode_value=u'inline', tag=u'inline')
responseModeType.attached = responseModeType._CF_enumeration.addEnumeration(unicode_value=u'attached', tag=u'attached')
responseModeType.out_of_band = responseModeType._CF_enumeration.addEnumeration(unicode_value=u'out-of-band', tag=u'out_of_band')
responseModeType.resultTemplate = responseModeType._CF_enumeration.addEnumeration(unicode_value=u'resultTemplate', tag=u'resultTemplate')
responseModeType._InitializeFacetMap(responseModeType._CF_enumeration)
Namespace.addCategoryObject('typeBinding', u'responseModeType', responseModeType)

# Complex type RequestBaseType with content type EMPTY
class RequestBaseType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'RequestBaseType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpwww_opengis_netsos1_0_RequestBaseType_version', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'1.0.0', required=True)
    
    version = property(__version.value, __version.set, None, u'Specification version for SOS version and operation.')

    
    # Attribute service uses Python identifier service
    __service = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpwww_opengis_netsos1_0_RequestBaseType_service', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'SOS', required=True)
    
    service = property(__service.value, __service.set, None, u'Service type identifier. ')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __version.name() : __version,
        __service.name() : __service
    }
Namespace.addCategoryObject('typeBinding', u'RequestBaseType', RequestBaseType)


# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/sos/1.0}FeatureOfInterestId uses Python identifier FeatureOfInterestId
    __FeatureOfInterestId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'FeatureOfInterestId'), 'FeatureOfInterestId', '__httpwww_opengis_netsos1_0_CTD_ANON_httpwww_opengis_netsos1_0FeatureOfInterestId', False)

    
    FeatureOfInterestId = property(__FeatureOfInterestId.value, __FeatureOfInterestId.set, None, u'Identifier of the feature of interest, for which detailed information is requested. These identifiers are usually listed in the Contents section of the service metadata (Capabilities) document. ')

    
    # Attribute version inherited from {http://www.opengis.net/sos/1.0}RequestBaseType
    
    # Attribute service inherited from {http://www.opengis.net/sos/1.0}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __FeatureOfInterestId.name() : __FeatureOfInterestId
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_ with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}spatialOps uses Python identifier spatialOps
    __spatialOps = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'spatialOps'), 'spatialOps', '__httpwww_opengis_netsos1_0_CTD_ANON__httpwww_opengis_netogcspatialOps', False)

    
    spatialOps = property(__spatialOps.value, __spatialOps.set, None, None)

    
    # Element {http://www.opengis.net/sos/1.0}ObjectID uses Python identifier ObjectID
    __ObjectID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ObjectID'), 'ObjectID', '__httpwww_opengis_netsos1_0_CTD_ANON__httpwww_opengis_netsos1_0ObjectID', True)

    
    ObjectID = property(__ObjectID.value, __ObjectID.set, None, u'Unordered list of zero or more object identifiers. These identifiers are usually listed in the Contents section of the service metadata (Capabilities) document. If no ObjectID value is included, and if only one category of objects is allowed for this operation, the server shall return all objects of that category. NOTE: Although retention of this ability is allowed by a specific OWS that uses this operation, such retention is discouraged due to possible problems. Making this ability optional implementation by servers reduces interoperability. Requiring implementation of this ability can require a server to return a huge response, when there are a large number of items in that category. ')


    _ElementMap = {
        __spatialOps.name() : __spatialOps,
        __ObjectID.name() : __ObjectID
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_2 with content type ELEMENT_ONLY
class CTD_ANON_2 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/sos/1.0}eventTime uses Python identifier eventTime
    __eventTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'eventTime'), 'eventTime', '__httpwww_opengis_netsos1_0_CTD_ANON_2_httpwww_opengis_netsos1_0eventTime', True)

    
    eventTime = property(__eventTime.value, __eventTime.set, None, u'Uses modified version of filter.xsd \n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\tAllows a client to request targets from a specific instant, multiple instances or periods of time in the past, present and future. \n\t\t\t\t\t\t\t\tThis is useful for dynamic sensors for which the properties of the target are time-dependent. \n\t\t\t\t\t\t\t\tMultiple time paramters may be indicated so that the client may request details of the observation target at multiple times. \n\t\t\t\t\t\t\t\tThe supported range is listed in the contents section of the service metadata.')

    
    # Element {http://www.opengis.net/sos/1.0}location uses Python identifier location
    __location = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'location'), 'location', '__httpwww_opengis_netsos1_0_CTD_ANON_2_httpwww_opengis_netsos1_0location', False)

    
    location = property(__location.value, __location.set, None, u'Uses modified version of filter.xsd')

    
    # Element {http://www.opengis.net/sos/1.0}FeatureOfInterestId uses Python identifier FeatureOfInterestId
    __FeatureOfInterestId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'FeatureOfInterestId'), 'FeatureOfInterestId', '__httpwww_opengis_netsos1_0_CTD_ANON_2_httpwww_opengis_netsos1_0FeatureOfInterestId', True)

    
    FeatureOfInterestId = property(__FeatureOfInterestId.value, __FeatureOfInterestId.set, None, u'Identifier of the feature of interest, for which detailed information is requested. These identifiers are usually listed in the Contents section of the service metadata (Capabilities) document. ')

    
    # Attribute version inherited from {http://www.opengis.net/sos/1.0}RequestBaseType
    
    # Attribute service inherited from {http://www.opengis.net/sos/1.0}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __eventTime.name() : __eventTime,
        __location.name() : __location,
        __FeatureOfInterestId.name() : __FeatureOfInterestId
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_3 with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/sos/1.0}ObservationOfferingList uses Python identifier ObservationOfferingList
    __ObservationOfferingList = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ObservationOfferingList'), 'ObservationOfferingList', '__httpwww_opengis_netsos1_0_CTD_ANON_3_httpwww_opengis_netsos1_0ObservationOfferingList', False)

    
    ObservationOfferingList = property(__ObservationOfferingList.value, __ObservationOfferingList.set, None, None)


    _ElementMap = {
        __ObservationOfferingList.name() : __ObservationOfferingList
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_4 with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}comparisonOps uses Python identifier comparisonOps
    __comparisonOps = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'comparisonOps'), 'comparisonOps', '__httpwww_opengis_netsos1_0_CTD_ANON_4_httpwww_opengis_netogccomparisonOps', False)

    
    comparisonOps = property(__comparisonOps.value, __comparisonOps.set, None, None)


    _ElementMap = {
        __comparisonOps.name() : __comparisonOps
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_5 with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/sos/1.0}ObservationOffering uses Python identifier ObservationOffering
    __ObservationOffering = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ObservationOffering'), 'ObservationOffering', '__httpwww_opengis_netsos1_0_CTD_ANON_5_httpwww_opengis_netsos1_0ObservationOffering', True)

    
    ObservationOffering = property(__ObservationOffering.value, __ObservationOffering.set, None, None)


    _ElementMap = {
        __ObservationOffering.name() : __ObservationOffering
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_6 with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/sos/1.0}result uses Python identifier result
    __result = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'result'), 'result', '__httpwww_opengis_netsos1_0_CTD_ANON_6_httpwww_opengis_netsos1_0result', False)

    
    result = property(__result.value, __result.set, None, u'RS attribute points to the description of the reference system of the result. The description will contain all information necessary to understand what is provided within the result response. The most simple case would be a single value.')


    _ElementMap = {
        __result.name() : __result
    }
    _AttributeMap = {
        
    }



# Complex type ObservationOfferingBaseType with content type ELEMENT_ONLY
class ObservationOfferingBaseType (pyxb.bundles.opengis.gml.AbstractFeatureType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObservationOfferingBaseType')
    # Base type is pyxb.bundles.opengis.gml.AbstractFeatureType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element boundedBy ({http://www.opengis.net/gml}boundedBy) inherited from {http://www.opengis.net/gml}AbstractFeatureType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = pyxb.bundles.opengis.gml.AbstractFeatureType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = pyxb.bundles.opengis.gml.AbstractFeatureType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ObservationOfferingBaseType', ObservationOfferingBaseType)


# Complex type ObservationOfferingType with content type ELEMENT_ONLY
class ObservationOfferingType (ObservationOfferingBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObservationOfferingType')
    # Base type is ObservationOfferingBaseType
    
    # Element {http://www.opengis.net/sos/1.0}time uses Python identifier time
    __time = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'time'), 'time', '__httpwww_opengis_netsos1_0_ObservationOfferingType_httpwww_opengis_netsos1_0time', False)

    
    time = property(__time.value, __time.set, None, None)

    
    # Element {http://www.opengis.net/sos/1.0}responseFormat uses Python identifier responseFormat
    __responseFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'responseFormat'), 'responseFormat', '__httpwww_opengis_netsos1_0_ObservationOfferingType_httpwww_opengis_netsos1_0responseFormat', True)

    
    responseFormat = property(__responseFormat.value, __responseFormat.set, None, None)

    
    # Element {http://www.opengis.net/sos/1.0}intendedApplication uses Python identifier intendedApplication
    __intendedApplication = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'intendedApplication'), 'intendedApplication', '__httpwww_opengis_netsos1_0_ObservationOfferingType_httpwww_opengis_netsos1_0intendedApplication', True)

    
    intendedApplication = property(__intendedApplication.value, __intendedApplication.set, None, None)

    
    # Element {http://www.opengis.net/sos/1.0}resultModel uses Python identifier resultModel
    __resultModel = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'resultModel'), 'resultModel', '__httpwww_opengis_netsos1_0_ObservationOfferingType_httpwww_opengis_netsos1_0resultModel', True)

    
    resultModel = property(__resultModel.value, __resultModel.set, None, u'\n\t\t\t\t\t\t\tIndicates the qualified name of the observation element that will be returned from a call to GetObservation for this offering.  \n\t\t\t\t\t\t\tThis element must be in the om:AbstractObservation substitution group and is typically the om:Observation or a specialized extension.\n\t\t\t\t\t\t\t')

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/sos/1.0}observedProperty uses Python identifier observedProperty
    __observedProperty = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'observedProperty'), 'observedProperty', '__httpwww_opengis_netsos1_0_ObservationOfferingType_httpwww_opengis_netsos1_0observedProperty', True)

    
    observedProperty = property(__observedProperty.value, __observedProperty.set, None, None)

    
    # Element {http://www.opengis.net/sos/1.0}responseMode uses Python identifier responseMode
    __responseMode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'responseMode'), 'responseMode', '__httpwww_opengis_netsos1_0_ObservationOfferingType_httpwww_opengis_netsos1_0responseMode', True)

    
    responseMode = property(__responseMode.value, __responseMode.set, None, u'This element allows the client to request the form of the response.  The value of resultTemplate is used to retrieve an observation template \n\t\t\t\t\t\t\tthat will later be used in calls to GetResult.  The other options allow results to appear inline in a resultTag (inline), external to the observation element (out-of-band)\n\t\t\t\t\t\t\tor as a MIME attachment (attached)')

    
    # Element {http://www.opengis.net/sos/1.0}procedure uses Python identifier procedure
    __procedure = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'procedure'), 'procedure', '__httpwww_opengis_netsos1_0_ObservationOfferingType_httpwww_opengis_netsos1_0procedure', True)

    
    procedure = property(__procedure.value, __procedure.set, None, None)

    
    # Element {http://www.opengis.net/sos/1.0}featureOfInterest uses Python identifier featureOfInterest
    __featureOfInterest = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'featureOfInterest'), 'featureOfInterest', '__httpwww_opengis_netsos1_0_ObservationOfferingType_httpwww_opengis_netsos1_0featureOfInterest', True)

    
    featureOfInterest = property(__featureOfInterest.value, __featureOfInterest.set, None, None)

    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element boundedBy ({http://www.opengis.net/gml}boundedBy) inherited from {http://www.opengis.net/gml}AbstractFeatureType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = ObservationOfferingBaseType._ElementMap.copy()
    _ElementMap.update({
        __time.name() : __time,
        __responseFormat.name() : __responseFormat,
        __intendedApplication.name() : __intendedApplication,
        __resultModel.name() : __resultModel,
        __observedProperty.name() : __observedProperty,
        __responseMode.name() : __responseMode,
        __procedure.name() : __procedure,
        __featureOfInterest.name() : __featureOfInterest
    })
    _AttributeMap = ObservationOfferingBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ObservationOfferingType', ObservationOfferingType)


# Complex type CTD_ANON_7 with content type ELEMENT_ONLY
class CTD_ANON_7 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/sos/1.0}observedProperty uses Python identifier observedProperty
    __observedProperty = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'observedProperty'), 'observedProperty', '__httpwww_opengis_netsos1_0_CTD_ANON_7_httpwww_opengis_netsos1_0observedProperty', False)

    
    observedProperty = property(__observedProperty.value, __observedProperty.set, None, u'The phenomenon for which the observationType (OM application schema) is requested.')

    
    # Attribute version inherited from {http://www.opengis.net/sos/1.0}RequestBaseType
    
    # Attribute service inherited from {http://www.opengis.net/sos/1.0}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __observedProperty.name() : __observedProperty
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_8 with content type ELEMENT_ONLY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/om/1.0}Observation uses Python identifier Observation
    __Observation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/om/1.0'), u'Observation'), 'Observation', '__httpwww_opengis_netsos1_0_CTD_ANON_8_httpwww_opengis_netom1_0Observation', False)

    
    Observation = property(__Observation.value, __Observation.set, None, u'Observation is an act ("event"), whose result is an estimate of the value of a property of the feature of interest. \n            The observed property may be any property associated with the type of the feature of interest.')


    _ElementMap = {
        __Observation.name() : __Observation
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_9 with content type ELEMENT_ONLY
class CTD_ANON_9 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/sos/1.0}eventTime uses Python identifier eventTime
    __eventTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'eventTime'), 'eventTime', '__httpwww_opengis_netsos1_0_CTD_ANON_9_httpwww_opengis_netsos1_0eventTime', True)

    
    eventTime = property(__eventTime.value, __eventTime.set, None, u'Allows a client to request observations from a specific instant, multiple instances or periods of time in the past, present and future. The supported range is listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.opengis.net/sos/1.0}ObservationTemplateId uses Python identifier ObservationTemplateId
    __ObservationTemplateId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ObservationTemplateId'), 'ObservationTemplateId', '__httpwww_opengis_netsos1_0_CTD_ANON_9_httpwww_opengis_netsos1_0ObservationTemplateId', False)

    
    ObservationTemplateId = property(__ObservationTemplateId.value, __ObservationTemplateId.set, None, u'The gml:id of an previous GetObservation request response indicating observations from a certain sensor for a certain target.\n\t\t\t\t\t\t\t\t')

    
    # Attribute version inherited from {http://www.opengis.net/sos/1.0}RequestBaseType
    
    # Attribute service inherited from {http://www.opengis.net/sos/1.0}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __eventTime.name() : __eventTime,
        __ObservationTemplateId.name() : __ObservationTemplateId
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_10 with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}spatialOps uses Python identifier spatialOps
    __spatialOps = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'spatialOps'), 'spatialOps', '__httpwww_opengis_netsos1_0_CTD_ANON_10_httpwww_opengis_netogcspatialOps', False)

    
    spatialOps = property(__spatialOps.value, __spatialOps.set, None, None)


    _ElementMap = {
        __spatialOps.name() : __spatialOps
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_11 with content type ELEMENT_ONLY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}temporalOps uses Python identifier temporalOps
    __temporalOps = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'temporalOps'), 'temporalOps', '__httpwww_opengis_netsos1_0_CTD_ANON_11_httpwww_opengis_netogctemporalOps', False)

    
    temporalOps = property(__temporalOps.value, __temporalOps.set, None, None)


    _ElementMap = {
        __temporalOps.name() : __temporalOps
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_12 with content type SIMPLE
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute RS uses Python identifier RS
    __RS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'RS'), 'RS', '__httpwww_opengis_netsos1_0_CTD_ANON_12_RS', pyxb.binding.datatypes.anyURI, required=True)
    
    RS = property(__RS.value, __RS.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __RS.name() : __RS
    }



# Complex type CTD_ANON_13 with content type ELEMENT_ONLY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}Id_Capabilities uses Python identifier Id_Capabilities
    __Id_Capabilities = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Id_Capabilities'), 'Id_Capabilities', '__httpwww_opengis_netsos1_0_CTD_ANON_13_httpwww_opengis_netogcId_Capabilities', False)

    
    Id_Capabilities = property(__Id_Capabilities.value, __Id_Capabilities.set, None, None)

    
    # Element {http://www.opengis.net/ogc}Spatial_Capabilities uses Python identifier Spatial_Capabilities
    __Spatial_Capabilities = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Spatial_Capabilities'), 'Spatial_Capabilities', '__httpwww_opengis_netsos1_0_CTD_ANON_13_httpwww_opengis_netogcSpatial_Capabilities', False)

    
    Spatial_Capabilities = property(__Spatial_Capabilities.value, __Spatial_Capabilities.set, None, None)

    
    # Element {http://www.opengis.net/ogc}Scalar_Capabilities uses Python identifier Scalar_Capabilities
    __Scalar_Capabilities = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Scalar_Capabilities'), 'Scalar_Capabilities', '__httpwww_opengis_netsos1_0_CTD_ANON_13_httpwww_opengis_netogcScalar_Capabilities', False)

    
    Scalar_Capabilities = property(__Scalar_Capabilities.value, __Scalar_Capabilities.set, None, None)

    
    # Element {http://www.opengis.net/ogc}Temporal_Capabilities uses Python identifier Temporal_Capabilities
    __Temporal_Capabilities = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Temporal_Capabilities'), 'Temporal_Capabilities', '__httpwww_opengis_netsos1_0_CTD_ANON_13_httpwww_opengis_netogcTemporal_Capabilities', False)

    
    Temporal_Capabilities = property(__Temporal_Capabilities.value, __Temporal_Capabilities.set, None, None)


    _ElementMap = {
        __Id_Capabilities.name() : __Id_Capabilities,
        __Spatial_Capabilities.name() : __Spatial_Capabilities,
        __Scalar_Capabilities.name() : __Scalar_Capabilities,
        __Temporal_Capabilities.name() : __Temporal_Capabilities
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_14 with content type ELEMENT_ONLY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/sos/1.0}AssignedSensorId uses Python identifier AssignedSensorId
    __AssignedSensorId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AssignedSensorId'), 'AssignedSensorId', '__httpwww_opengis_netsos1_0_CTD_ANON_14_httpwww_opengis_netsos1_0AssignedSensorId', False)

    
    AssignedSensorId = property(__AssignedSensorId.value, __AssignedSensorId.set, None, None)


    _ElementMap = {
        __AssignedSensorId.name() : __AssignedSensorId
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_15 with content type ELEMENT_ONLY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}temporalOps uses Python identifier temporalOps
    __temporalOps = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'temporalOps'), 'temporalOps', '__httpwww_opengis_netsos1_0_CTD_ANON_15_httpwww_opengis_netogctemporalOps', False)

    
    temporalOps = property(__temporalOps.value, __temporalOps.set, None, None)


    _ElementMap = {
        __temporalOps.name() : __temporalOps
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_16 with content type ELEMENT_ONLY
class CTD_ANON_16 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/sos/1.0}AssignedSensorId uses Python identifier AssignedSensorId
    __AssignedSensorId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AssignedSensorId'), 'AssignedSensorId', '__httpwww_opengis_netsos1_0_CTD_ANON_16_httpwww_opengis_netsos1_0AssignedSensorId', False)

    
    AssignedSensorId = property(__AssignedSensorId.value, __AssignedSensorId.set, None, u'The id obtained by the registerSensor operation.')

    
    # Element {http://www.opengis.net/om/1.0}Observation uses Python identifier Observation
    __Observation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/om/1.0'), u'Observation'), 'Observation', '__httpwww_opengis_netsos1_0_CTD_ANON_16_httpwww_opengis_netom1_0Observation', False)

    
    Observation = property(__Observation.value, __Observation.set, None, u'Observation is an act ("event"), whose result is an estimate of the value of a property of the feature of interest. \n            The observed property may be any property associated with the type of the feature of interest.')

    
    # Attribute version inherited from {http://www.opengis.net/sos/1.0}RequestBaseType
    
    # Attribute service inherited from {http://www.opengis.net/sos/1.0}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __AssignedSensorId.name() : __AssignedSensorId,
        __Observation.name() : __Observation
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_17 with content type ELEMENT_ONLY
class CTD_ANON_17 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/sos/1.0}ObservationTemplate uses Python identifier ObservationTemplate
    __ObservationTemplate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ObservationTemplate'), 'ObservationTemplate', '__httpwww_opengis_netsos1_0_CTD_ANON_17_httpwww_opengis_netsos1_0ObservationTemplate', False)

    
    ObservationTemplate = property(__ObservationTemplate.value, __ObservationTemplate.set, None, u'A template of the observations that will be inserted into the SOS.')

    
    # Element {http://www.opengis.net/sos/1.0}SensorDescription uses Python identifier SensorDescription
    __SensorDescription = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'SensorDescription'), 'SensorDescription', '__httpwww_opengis_netsos1_0_CTD_ANON_17_httpwww_opengis_netsos1_0SensorDescription', False)

    
    SensorDescription = property(__SensorDescription.value, __SensorDescription.set, None, None)

    
    # Attribute version inherited from {http://www.opengis.net/sos/1.0}RequestBaseType
    
    # Attribute service inherited from {http://www.opengis.net/sos/1.0}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __ObservationTemplate.name() : __ObservationTemplate,
        __SensorDescription.name() : __SensorDescription
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_18 with content type ELEMENT_ONLY
class CTD_ANON_18 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/sos/1.0}ResultName uses Python identifier ResultName
    __ResultName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ResultName'), 'ResultName', '__httpwww_opengis_netsos1_0_CTD_ANON_18_httpwww_opengis_netsos1_0ResultName', False)

    
    ResultName = property(__ResultName.value, __ResultName.set, None, u'Identifier of the type of the result, for which detailed information is requested.')

    
    # Attribute version inherited from {http://www.opengis.net/sos/1.0}RequestBaseType
    
    # Attribute service inherited from {http://www.opengis.net/sos/1.0}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __ResultName.name() : __ResultName
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_19 with content type ELEMENT_ONLY
class CTD_ANON_19 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/sos/1.0}eventTime uses Python identifier eventTime
    __eventTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'eventTime'), 'eventTime', '__httpwww_opengis_netsos1_0_CTD_ANON_19_httpwww_opengis_netsos1_0eventTime', True)

    
    eventTime = property(__eventTime.value, __eventTime.set, None, u'Allows a client to request observations from a specific instant, multiple instances or periods of time in the past, present and future. The supported range is listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.opengis.net/sos/1.0}result uses Python identifier result
    __result = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'result'), 'result', '__httpwww_opengis_netsos1_0_CTD_ANON_19_httpwww_opengis_netsos1_0result', False)

    
    result = property(__result.value, __result.set, None, u'Only report observations where the result matches this expression.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.opengis.net/sos/1.0}responseFormat uses Python identifier responseFormat
    __responseFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'responseFormat'), 'responseFormat', '__httpwww_opengis_netsos1_0_CTD_ANON_19_httpwww_opengis_netsos1_0responseFormat', False)

    
    responseFormat = property(__responseFormat.value, __responseFormat.set, None, u'ID of the output format to be used for the requested data. The supported output formats are listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.opengis.net/sos/1.0}resultModel uses Python identifier resultModel
    __resultModel = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'resultModel'), 'resultModel', '__httpwww_opengis_netsos1_0_CTD_ANON_19_httpwww_opengis_netsos1_0resultModel', False)

    
    resultModel = property(__resultModel.value, __resultModel.set, None, u'Identifier of the result model to be used for the requested data. The resultModel values supported by a SOS server are listed in the contents section of the service metadata, identified as QName values.  If the requested resultModel is not supported by the SOS server, an exception message shall be returned.\n\t\t\t\t\t\t\t')

    
    # Element {http://www.opengis.net/sos/1.0}observedProperty uses Python identifier observedProperty
    __observedProperty = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'observedProperty'), 'observedProperty', '__httpwww_opengis_netsos1_0_CTD_ANON_19_httpwww_opengis_netsos1_0observedProperty', True)

    
    observedProperty = property(__observedProperty.value, __observedProperty.set, None, u'ID of a phenomenon advertised in capabilities document.\n\t\t\t\t\t\t\t\t\tAll possible phenomena are listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.opengis.net/sos/1.0}offering uses Python identifier offering
    __offering = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'offering'), 'offering', '__httpwww_opengis_netsos1_0_CTD_ANON_19_httpwww_opengis_netsos1_0offering', False)

    
    offering = property(__offering.value, __offering.set, None, u'ID of an offering advertised in the capabilities.\n\t\t\t\t\t\t\t\t\tAll following parameters are depending on the selected offering.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.opengis.net/sos/1.0}featureOfInterest uses Python identifier featureOfInterest
    __featureOfInterest = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'featureOfInterest'), 'featureOfInterest', '__httpwww_opengis_netsos1_0_CTD_ANON_19_httpwww_opengis_netsos1_0featureOfInterest', False)

    
    featureOfInterest = property(__featureOfInterest.value, __featureOfInterest.set, None, u'Specifies target feature for which observations are requested. Mostly a hepler for in-situ sensors, since geo-location has to be done on the server side. The supported area should be listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.opengis.net/sos/1.0}responseMode uses Python identifier responseMode
    __responseMode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'responseMode'), 'responseMode', '__httpwww_opengis_netsos1_0_CTD_ANON_19_httpwww_opengis_netsos1_0responseMode', False)

    
    responseMode = property(__responseMode.value, __responseMode.set, None, u'This element allows the client to request the form of the response.  The value of resultTemplate is used to retrieve an observation template \n\t\t\t\t\t\t\tthat will later be used in calls to GetResult.  The other options allow results to appear inline in a resultTag (inline), external to the observation element (out-of-band)\n\t\t\t\t\t\t\tor as a MIME attachment (attached)')

    
    # Element {http://www.opengis.net/sos/1.0}procedure uses Python identifier procedure
    __procedure = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'procedure'), 'procedure', '__httpwww_opengis_netsos1_0_CTD_ANON_19_httpwww_opengis_netsos1_0procedure', True)

    
    procedure = property(__procedure.value, __procedure.set, None, u"Index of a particular sensor if offering procedure is a Sensor Array. Allows client to request data from one or more sensors in the array. The size of the array should be specified in the selected offering capabilities. This is to support scenarios with sensor grids (we don't want to have one offering for each sensor in that case). Note that sensorML can describe Sensor Arrays too. \t\t\t\t\t\t\t\t\t\t")

    
    # Attribute version inherited from {http://www.opengis.net/sos/1.0}RequestBaseType
    
    # Attribute srsName uses Python identifier srsName
    __srsName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'srsName'), 'srsName', '__httpwww_opengis_netsos1_0_CTD_ANON_19_srsName', pyxb.binding.datatypes.anyURI)
    
    srsName = property(__srsName.value, __srsName.set, None, None)

    
    # Attribute service inherited from {http://www.opengis.net/sos/1.0}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __eventTime.name() : __eventTime,
        __result.name() : __result,
        __responseFormat.name() : __responseFormat,
        __resultModel.name() : __resultModel,
        __observedProperty.name() : __observedProperty,
        __offering.name() : __offering,
        __featureOfInterest.name() : __featureOfInterest,
        __responseMode.name() : __responseMode,
        __procedure.name() : __procedure
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        __srsName.name() : __srsName
    })



# Complex type CTD_ANON_20 with content type ELEMENT_ONLY
class CTD_ANON_20 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/ogc}temporalOps uses Python identifier temporalOps
    __temporalOps = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'temporalOps'), 'temporalOps', '__httpwww_opengis_netsos1_0_CTD_ANON_20_httpwww_opengis_netogctemporalOps', False)

    
    temporalOps = property(__temporalOps.value, __temporalOps.set, None, None)


    _ElementMap = {
        __temporalOps.name() : __temporalOps
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_21 with content type ELEMENT_ONLY
class CTD_ANON_21 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/sos/1.0}FeatureId uses Python identifier FeatureId
    __FeatureId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'FeatureId'), 'FeatureId', '__httpwww_opengis_netsos1_0_CTD_ANON_21_httpwww_opengis_netsos1_0FeatureId', False)

    
    FeatureId = property(__FeatureId.value, __FeatureId.set, None, u'Identifier of the feature for which detailed information is requested. These identifiers are usually listed in the Contents section of the service metadata (Capabilities) document. ')

    
    # Attribute version inherited from {http://www.opengis.net/sos/1.0}RequestBaseType
    
    # Attribute service inherited from {http://www.opengis.net/sos/1.0}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __FeatureId.name() : __FeatureId
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_22 with content type ELEMENT_ONLY
class CTD_ANON_22 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/sos/1.0}responseMode uses Python identifier responseMode
    __responseMode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'responseMode'), 'responseMode', '__httpwww_opengis_netsos1_0_CTD_ANON_22_httpwww_opengis_netsos1_0responseMode', False)

    
    responseMode = property(__responseMode.value, __responseMode.set, None, u'This element allows the client to request the form of the response.  The value of resultTemplate is used to retrieve an observation template \n\t\t\t\t\t\t\tthat will later be used in calls to GetResult.  The other options allow results to appear inline in a resultTag (inline), external to the observation element (out-of-band)\n\t\t\t\t\t\t\tor as a MIME attachment (attached)')

    
    # Element {http://www.opengis.net/sos/1.0}resultModel uses Python identifier resultModel
    __resultModel = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'resultModel'), 'resultModel', '__httpwww_opengis_netsos1_0_CTD_ANON_22_httpwww_opengis_netsos1_0resultModel', False)

    
    resultModel = property(__resultModel.value, __resultModel.set, None, None)

    
    # Element {http://www.opengis.net/sos/1.0}responseFormat uses Python identifier responseFormat
    __responseFormat = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'responseFormat'), 'responseFormat', '__httpwww_opengis_netsos1_0_CTD_ANON_22_httpwww_opengis_netsos1_0responseFormat', False)

    
    responseFormat = property(__responseFormat.value, __responseFormat.set, None, u'ID of the output format to be used for the requested data. The supported output formats are listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.opengis.net/sos/1.0}ObservationId uses Python identifier ObservationId
    __ObservationId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ObservationId'), 'ObservationId', '__httpwww_opengis_netsos1_0_CTD_ANON_22_httpwww_opengis_netsos1_0ObservationId', False)

    
    ObservationId = property(__ObservationId.value, __ObservationId.set, None, u'ID of the observation to obtain.  This could have been obtained by the client via a URL in a feed, alert, or some other notification\n\t\t\t\t\t\t\t\t')

    
    # Attribute srsName uses Python identifier srsName
    __srsName = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'srsName'), 'srsName', '__httpwww_opengis_netsos1_0_CTD_ANON_22_srsName', pyxb.binding.datatypes.anyURI)
    
    srsName = property(__srsName.value, __srsName.set, None, None)

    
    # Attribute service inherited from {http://www.opengis.net/sos/1.0}RequestBaseType
    
    # Attribute version inherited from {http://www.opengis.net/sos/1.0}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __responseMode.name() : __responseMode,
        __resultModel.name() : __resultModel,
        __responseFormat.name() : __responseFormat,
        __ObservationId.name() : __ObservationId
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        __srsName.name() : __srsName
    })



# Complex type CTD_ANON_23 with content type ELEMENT_ONLY
class CTD_ANON_23 (pyxb.bundles.opengis.ows_1_1.GetCapabilitiesType):
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
    __service = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'service'), 'service', '__httpwww_opengis_netsos1_0_CTD_ANON_23_service', pyxb.bundles.opengis.ows_1_1.ServiceType, fixed=True, unicode_default=u'SOS', required=True)
    
    service = property(__service.value, __service.set, None, None)


    _ElementMap = pyxb.bundles.opengis.ows_1_1.GetCapabilitiesType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = pyxb.bundles.opengis.ows_1_1.GetCapabilitiesType._AttributeMap.copy()
    _AttributeMap.update({
        __service.name() : __service
    })



# Complex type CTD_ANON_24 with content type ELEMENT_ONLY
class CTD_ANON_24 (RequestBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is RequestBaseType
    
    # Element {http://www.opengis.net/sos/1.0}procedure uses Python identifier procedure
    __procedure = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'procedure'), 'procedure', '__httpwww_opengis_netsos1_0_CTD_ANON_24_httpwww_opengis_netsos1_0procedure', False)

    
    procedure = property(__procedure.value, __procedure.set, None, u'Identifier of the sensor, for which detailed metadata is requested.')

    
    # Attribute version inherited from {http://www.opengis.net/sos/1.0}RequestBaseType
    
    # Attribute outputFormat uses Python identifier outputFormat
    __outputFormat = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'outputFormat'), 'outputFormat', '__httpwww_opengis_netsos1_0_CTD_ANON_24_outputFormat', pyxb.bundles.opengis.ows_1_1.MimeType, required=True)
    
    outputFormat = property(__outputFormat.value, __outputFormat.set, None, u'Identifier of the output format to be used for the requested data. The outputFormats supported by a SOS server are listed in the operations metadata section of the service metadata (capabilities XML). If this attribute is omitted, the outputFormat should be tex/xml;subtype="sensorML/1.0.0". If the requested outputFormat is not supported by the SOS server, an exception message shall be returned.\n\t\t\t\t')

    
    # Attribute service inherited from {http://www.opengis.net/sos/1.0}RequestBaseType

    _ElementMap = RequestBaseType._ElementMap.copy()
    _ElementMap.update({
        __procedure.name() : __procedure
    })
    _AttributeMap = RequestBaseType._AttributeMap.copy()
    _AttributeMap.update({
        __outputFormat.name() : __outputFormat
    })



# Complex type CTD_ANON_25 with content type ELEMENT_ONLY
class CTD_ANON_25 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True

    _ElementMap = {
        
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_26 with content type ELEMENT_ONLY
class CTD_ANON_26 (pyxb.bundles.opengis.ows_1_1.CapabilitiesBaseType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.bundles.opengis.ows_1_1.CapabilitiesBaseType
    
    # Element OperationsMetadata ({http://www.opengis.net/ows/1.1}OperationsMetadata) inherited from {http://www.opengis.net/ows/1.1}CapabilitiesBaseType
    
    # Element ServiceProvider ({http://www.opengis.net/ows/1.1}ServiceProvider) inherited from {http://www.opengis.net/ows/1.1}CapabilitiesBaseType
    
    # Element ServiceIdentification ({http://www.opengis.net/ows/1.1}ServiceIdentification) inherited from {http://www.opengis.net/ows/1.1}CapabilitiesBaseType
    
    # Element {http://www.opengis.net/sos/1.0}Filter_Capabilities uses Python identifier Filter_Capabilities
    __Filter_Capabilities = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Filter_Capabilities'), 'Filter_Capabilities', '__httpwww_opengis_netsos1_0_CTD_ANON_26_httpwww_opengis_netsos1_0Filter_Capabilities', False)

    
    Filter_Capabilities = property(__Filter_Capabilities.value, __Filter_Capabilities.set, None, None)

    
    # Element {http://www.opengis.net/sos/1.0}Contents uses Python identifier Contents
    __Contents = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Contents'), 'Contents', '__httpwww_opengis_netsos1_0_CTD_ANON_26_httpwww_opengis_netsos1_0Contents', False)

    
    Contents = property(__Contents.value, __Contents.set, None, u'Contents section of SOS service metadata (or Capabilites) XML document. For the SOS, these contents are data and functions that the SOS server provides.')

    
    # Attribute updateSequence inherited from {http://www.opengis.net/ows/1.1}CapabilitiesBaseType
    
    # Attribute version inherited from {http://www.opengis.net/ows/1.1}CapabilitiesBaseType

    _ElementMap = pyxb.bundles.opengis.ows_1_1.CapabilitiesBaseType._ElementMap.copy()
    _ElementMap.update({
        __Filter_Capabilities.name() : __Filter_Capabilities,
        __Contents.name() : __Contents
    })
    _AttributeMap = pyxb.bundles.opengis.ows_1_1.CapabilitiesBaseType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_27 with content type ELEMENT_ONLY
class CTD_ANON_27 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/sos/1.0}AssignedObservationId uses Python identifier AssignedObservationId
    __AssignedObservationId = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'AssignedObservationId'), 'AssignedObservationId', '__httpwww_opengis_netsos1_0_CTD_ANON_27_httpwww_opengis_netsos1_0AssignedObservationId', False)

    
    AssignedObservationId = property(__AssignedObservationId.value, __AssignedObservationId.set, None, None)


    _ElementMap = {
        __AssignedObservationId.name() : __AssignedObservationId
    }
    _AttributeMap = {
        
    }



GetFeatureOfInterestTime = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetFeatureOfInterestTime'), CTD_ANON, documentation=u'Request to a SOS to perform the GetTargetTime operation. \n\t\t\tThis operation is designed to request the time that specified target feature instances or target locations are available')
Namespace.addCategoryObject('elementBinding', GetFeatureOfInterestTime.name().localName(), GetFeatureOfInterestTime)

GetFeatureOfInterest = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetFeatureOfInterest'), CTD_ANON_2, documentation=u'Request to a SOS to perform the GetFeatureOfInterest operation. This operation is designed to request target feaure instances')
Namespace.addCategoryObject('elementBinding', GetFeatureOfInterest.name().localName(), GetFeatureOfInterest)

Contents = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Contents'), CTD_ANON_3, documentation=u'Contents section of SOS service metadata (or Capabilites) XML document. For the SOS, these contents are data and functions that the SOS server provides.')
Namespace.addCategoryObject('elementBinding', Contents.name().localName(), Contents)

GetResultResponse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetResultResponse'), CTD_ANON_6, documentation=u'the response of a GetResult operation')
Namespace.addCategoryObject('elementBinding', GetResultResponse.name().localName(), GetResultResponse)

DescribeObservationType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DescribeObservationType'), CTD_ANON_7, documentation=u'Request to a SOS to perform the DescribeObservationTypeoperation. This operation is designed to request detailed information concerning hard typed observation schemas')
Namespace.addCategoryObject('elementBinding', DescribeObservationType.name().localName(), DescribeObservationType)

GetResult = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetResult'), CTD_ANON_9, documentation=u'request to a SOS to perform a GetResult operation. this operation is designed to request sensor data from live sensors. Instead of retriveing the observations as a full OM document, you will get an simple value and a link to the reference system')
Namespace.addCategoryObject('elementBinding', GetResult.name().localName(), GetResult)

srsName = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'srsName'), pyxb.bundles.opengis.gml.CodeType)
Namespace.addCategoryObject('elementBinding', srsName.name().localName(), srsName)

Filter_Capabilities = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Filter_Capabilities'), CTD_ANON_13)
Namespace.addCategoryObject('elementBinding', Filter_Capabilities.name().localName(), Filter_Capabilities)

supportedSensorDescription = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'supportedSensorDescription'), pyxb.binding.datatypes.QName, documentation=u'The QName of the root of a sensor desription that is supported by this service.  Examples are "sml:_Process" and "tml:system"')
Namespace.addCategoryObject('elementBinding', supportedSensorDescription.name().localName(), supportedSensorDescription)

supportedSRS = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'supportedSRS'), pyxb.bundles.opengis.gml.CodeType, documentation=u'The name by which this reference system is identified.')
Namespace.addCategoryObject('elementBinding', supportedSRS.name().localName(), supportedSRS)

ObservationTemplate = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ObservationTemplate'), CTD_ANON_8, documentation=u'A template of the observations that will be inserted into the SOS.')
Namespace.addCategoryObject('elementBinding', ObservationTemplate.name().localName(), ObservationTemplate)

RegisterSensorResponse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'RegisterSensorResponse'), CTD_ANON_14, documentation=u'returns the Id that is used in the insert operation to link the sensor to an Observation')
Namespace.addCategoryObject('elementBinding', RegisterSensorResponse.name().localName(), RegisterSensorResponse)

InsertObservation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InsertObservation'), CTD_ANON_16, documentation=u'Request to a SOS to perform the Insert operation. This operation is designed to insert new observations. The request is constraint by the following parameters: ID obtained by the registerSensor operation (identifying the sensor and the observyationType, and the observation encoded as OM')
Namespace.addCategoryObject('elementBinding', InsertObservation.name().localName(), InsertObservation)

RegisterSensor = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'RegisterSensor'), CTD_ANON_17, documentation=u'Request to a SOS to perform the registerSensor operation. This operation is designed to register new sensors at the SOS.')
Namespace.addCategoryObject('elementBinding', RegisterSensor.name().localName(), RegisterSensor)

DescribeResultModel = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DescribeResultModel'), CTD_ANON_18, documentation=u"Request to a SOS to perform the DescribeResultModel operation. \n\t\t\tThis operation is designed to request detailed information concerning the format of the observation's result")
Namespace.addCategoryObject('elementBinding', DescribeResultModel.name().localName(), DescribeResultModel)

GetObservation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetObservation'), CTD_ANON_19, documentation=u'Request to a SOS to perform the GetObservation operation. This operation is designed to request sensor data from live sensors as well as sensor data archives.')
Namespace.addCategoryObject('elementBinding', GetObservation.name().localName(), GetObservation)

DescribeFeatureType = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DescribeFeatureType'), CTD_ANON_21, documentation=u"Request to a SOS to perform the DescribeFeatureType operation. This operation is designed to request detailed information concerning the observation's target")
Namespace.addCategoryObject('elementBinding', DescribeFeatureType.name().localName(), DescribeFeatureType)

GetObservationById = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetObservationById'), CTD_ANON_22, documentation=u'Request to a SOS to perform the GetObservation operation using an Observation ID.')
Namespace.addCategoryObject('elementBinding', GetObservationById.name().localName(), GetObservationById)

GetCapabilities = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GetCapabilities'), CTD_ANON_23, documentation=u'Request to a SOS to perform the GetCapabilities operation. This operation allows a client to retrieve service metadata (capabilities XML) providing metadata for the specific SOS server. In this XML encoding, no "request" parameter is included, since the element name specifies the specific operation. ')
Namespace.addCategoryObject('elementBinding', GetCapabilities.name().localName(), GetCapabilities)

DescribeSensor = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DescribeSensor'), CTD_ANON_24, documentation=u'Request to a SOS to perform the DescribeSensor operation. This operation is designed to request detailed sensor metadata.\t')
Namespace.addCategoryObject('elementBinding', DescribeSensor.name().localName(), DescribeSensor)

Capabilities = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Capabilities'), CTD_ANON_26, documentation=u'XML encoded SOS GetCapabilities operation response. This document provides clients with service metadata about a specific service instance, including metadata about the tightly-coupled data served. If the server does not implement the updateSequence parameter, the server shall always return the complete Capabilities document, without the updateSequence parameter. When the server implements the updateSequence parameter and the GetCapabilities operation request included the updateSequence parameter with the current value, the server shall return this element with only the "version" and "updateSequence" attributes. Otherwise, all optional elements shall be included or not depending on the actual value of the Sections parameter in the GetCapabilities operation request. ')
Namespace.addCategoryObject('elementBinding', Capabilities.name().localName(), Capabilities)

InsertObservationResponse = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'InsertObservationResponse'), CTD_ANON_27, documentation=u'returns the Id of the Observation assigend by the SOS')
Namespace.addCategoryObject('elementBinding', InsertObservationResponse.name().localName(), InsertObservationResponse)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FeatureOfInterestId'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON, documentation=u'Identifier of the feature of interest, for which detailed information is requested. These identifiers are usually listed in the Contents section of the service metadata (Capabilities) document. '))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'FeatureOfInterestId')), min_occurs=1, max_occurs=1)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'spatialOps'), pyxb.bundles.opengis.filter.SpatialOpsType, abstract=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ObjectID'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_, documentation=u'Unordered list of zero or more object identifiers. These identifiers are usually listed in the Contents section of the service metadata (Capabilities) document. If no ObjectID value is included, and if only one category of objects is allowed for this operation, the server shall return all objects of that category. NOTE: Although retention of this ability is allowed by a specific OWS that uses this operation, such retention is discouraged due to possible problems. Making this ability optional implementation by servers reduces interoperability. Requiring implementation of this ability can require a server to return a huge response, when there are a large number of items in that category. '))
CTD_ANON_._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'spatialOps')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ObjectID')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'eventTime'), CTD_ANON_11, scope=CTD_ANON_2, documentation=u'Uses modified version of filter.xsd \n\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\tAllows a client to request targets from a specific instant, multiple instances or periods of time in the past, present and future. \n\t\t\t\t\t\t\t\tThis is useful for dynamic sensors for which the properties of the target are time-dependent. \n\t\t\t\t\t\t\t\tMultiple time paramters may be indicated so that the client may request details of the observation target at multiple times. \n\t\t\t\t\t\t\t\tThe supported range is listed in the contents section of the service metadata.'))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'location'), CTD_ANON_10, scope=CTD_ANON_2, documentation=u'Uses modified version of filter.xsd'))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FeatureOfInterestId'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_2, documentation=u'Identifier of the feature of interest, for which detailed information is requested. These identifiers are usually listed in the Contents section of the service metadata (Capabilities) document. '))
CTD_ANON_2._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'FeatureOfInterestId')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'location')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_2._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'eventTime')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_2._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ObservationOfferingList'), CTD_ANON_5, scope=CTD_ANON_3))
CTD_ANON_3._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ObservationOfferingList')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_3._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_3._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'comparisonOps'), pyxb.bundles.opengis.filter.ComparisonOpsType, abstract=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_4))
CTD_ANON_4._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'comparisonOps')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_4._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ObservationOffering'), ObservationOfferingType, scope=CTD_ANON_5))
CTD_ANON_5._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ObservationOffering')), min_occurs=1, max_occurs=None)
    )
CTD_ANON_5._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_5._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'result'), CTD_ANON_12, scope=CTD_ANON_6, documentation=u'RS attribute points to the description of the reference system of the result. The description will contain all information necessary to understand what is provided within the result response. The most simple case would be a single value.'))
CTD_ANON_6._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'result')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_6._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_6._GroupModel, min_occurs=1, max_occurs=1)


ObservationOfferingBaseType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationOfferingBaseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObservationOfferingBaseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationOfferingBaseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
ObservationOfferingBaseType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationOfferingBaseType._GroupModel_5, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationOfferingBaseType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'boundedBy')), min_occurs=1, max_occurs=1)
    )
ObservationOfferingBaseType._ContentModel = pyxb.binding.content.ParticleModel(ObservationOfferingBaseType._GroupModel_4, min_occurs=1, max_occurs=1)



ObservationOfferingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'time'), pyxb.bundles.opengis.swe_1_0_1.TimeGeometricPrimitivePropertyType, scope=ObservationOfferingType))

ObservationOfferingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'responseFormat'), pyxb.bundles.opengis.ows_1_1.MimeType, scope=ObservationOfferingType))

ObservationOfferingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'intendedApplication'), pyxb.binding.datatypes.token, scope=ObservationOfferingType))

ObservationOfferingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'resultModel'), pyxb.binding.datatypes.QName, scope=ObservationOfferingType, documentation=u'\n\t\t\t\t\t\t\tIndicates the qualified name of the observation element that will be returned from a call to GetObservation for this offering.  \n\t\t\t\t\t\t\tThis element must be in the om:AbstractObservation substitution group and is typically the om:Observation or a specialized extension.\n\t\t\t\t\t\t\t'))

ObservationOfferingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'observedProperty'), pyxb.bundles.opengis.swe_1_0_1.PhenomenonPropertyType, scope=ObservationOfferingType))

ObservationOfferingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'responseMode'), responseModeType, scope=ObservationOfferingType, documentation=u'This element allows the client to request the form of the response.  The value of resultTemplate is used to retrieve an observation template \n\t\t\t\t\t\t\tthat will later be used in calls to GetResult.  The other options allow results to appear inline in a resultTag (inline), external to the observation element (out-of-band)\n\t\t\t\t\t\t\tor as a MIME attachment (attached)'))

ObservationOfferingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'procedure'), pyxb.bundles.opengis.gml.ReferenceType, scope=ObservationOfferingType))

ObservationOfferingType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'featureOfInterest'), pyxb.bundles.opengis.gml.ReferenceType, scope=ObservationOfferingType))
ObservationOfferingType._GroupModel_6 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
ObservationOfferingType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationOfferingType._GroupModel_6, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'boundedBy')), min_occurs=1, max_occurs=1)
    )
ObservationOfferingType._GroupModel_7 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'intendedApplication')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'time')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'procedure')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'observedProperty')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'featureOfInterest')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'responseFormat')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'resultModel')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObservationOfferingType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'responseMode')), min_occurs=0L, max_occurs=None)
    )
ObservationOfferingType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationOfferingType._GroupModel_5, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationOfferingType._GroupModel_7, min_occurs=1, max_occurs=1)
    )
ObservationOfferingType._ContentModel = pyxb.binding.content.ParticleModel(ObservationOfferingType._GroupModel_4, min_occurs=1, max_occurs=1)



CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'observedProperty'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_7, documentation=u'The phenomenon for which the observationType (OM application schema) is requested.'))
CTD_ANON_7._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'observedProperty')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_7._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_7._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/om/1.0'), u'Observation'), pyxb.bundles.opengis.om_1_0.ObservationType, scope=CTD_ANON_8, documentation=u'Observation is an act ("event"), whose result is an estimate of the value of a property of the feature of interest. \n            The observed property may be any property associated with the type of the feature of interest.'))
CTD_ANON_8._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/om/1.0'), u'Observation')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_8._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_8._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'eventTime'), CTD_ANON_20, scope=CTD_ANON_9, documentation=u'Allows a client to request observations from a specific instant, multiple instances or periods of time in the past, present and future. The supported range is listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ObservationTemplateId'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_9, documentation=u'The gml:id of an previous GetObservation request response indicating observations from a certain sensor for a certain target.\n\t\t\t\t\t\t\t\t'))
CTD_ANON_9._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ObservationTemplateId')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'eventTime')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_9._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_9._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'spatialOps'), pyxb.bundles.opengis.filter.SpatialOpsType, abstract=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_10))
CTD_ANON_10._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'spatialOps')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_10._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_10._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'temporalOps'), pyxb.bundles.opengis._ogc.TemporalOpsType, abstract=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_11))
CTD_ANON_11._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'temporalOps')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_11._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_11._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Id_Capabilities'), pyxb.bundles.opengis.filter.Id_CapabilitiesType, scope=CTD_ANON_13))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Spatial_Capabilities'), pyxb.bundles.opengis.filter.Spatial_CapabilitiesType, scope=CTD_ANON_13))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Scalar_Capabilities'), pyxb.bundles.opengis.filter.Scalar_CapabilitiesType, scope=CTD_ANON_13))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Temporal_Capabilities'), pyxb.bundles.opengis._ogc.Temporal_CapabilitiesType, scope=CTD_ANON_13))
CTD_ANON_13._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Spatial_Capabilities')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Temporal_Capabilities')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Scalar_Capabilities')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'Id_Capabilities')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_13._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_13._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AssignedSensorId'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_14))
CTD_ANON_14._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AssignedSensorId')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_14._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_14._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'temporalOps'), pyxb.bundles.opengis._ogc.TemporalOpsType, abstract=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_15))
CTD_ANON_15._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'temporalOps')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_15._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_15._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AssignedSensorId'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_16, documentation=u'The id obtained by the registerSensor operation.'))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/om/1.0'), u'Observation'), pyxb.bundles.opengis.om_1_0.ObservationType, scope=CTD_ANON_16, documentation=u'Observation is an act ("event"), whose result is an estimate of the value of a property of the feature of interest. \n            The observed property may be any property associated with the type of the feature of interest.'))
CTD_ANON_16._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AssignedSensorId')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/om/1.0'), u'Observation')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_16._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_16._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ObservationTemplate'), CTD_ANON_8, scope=CTD_ANON_17, documentation=u'A template of the observations that will be inserted into the SOS.'))

CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'SensorDescription'), CTD_ANON_25, scope=CTD_ANON_17))
CTD_ANON_17._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'SensorDescription')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ObservationTemplate')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_17._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_17._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ResultName'), pyxb.binding.datatypes.QName, scope=CTD_ANON_18, documentation=u'Identifier of the type of the result, for which detailed information is requested.'))
CTD_ANON_18._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ResultName')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_18._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_18._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'eventTime'), CTD_ANON_15, scope=CTD_ANON_19, documentation=u'Allows a client to request observations from a specific instant, multiple instances or periods of time in the past, present and future. The supported range is listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'result'), CTD_ANON_4, scope=CTD_ANON_19, documentation=u'Only report observations where the result matches this expression.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'responseFormat'), pyxb.bundles.opengis.ows_1_1.MimeType, scope=CTD_ANON_19, documentation=u'ID of the output format to be used for the requested data. The supported output formats are listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'resultModel'), pyxb.binding.datatypes.QName, scope=CTD_ANON_19, documentation=u'Identifier of the result model to be used for the requested data. The resultModel values supported by a SOS server are listed in the contents section of the service metadata, identified as QName values.  If the requested resultModel is not supported by the SOS server, an exception message shall be returned.\n\t\t\t\t\t\t\t'))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'observedProperty'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_19, documentation=u'ID of a phenomenon advertised in capabilities document.\n\t\t\t\t\t\t\t\t\tAll possible phenomena are listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'offering'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_19, documentation=u'ID of an offering advertised in the capabilities.\n\t\t\t\t\t\t\t\t\tAll following parameters are depending on the selected offering.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'featureOfInterest'), CTD_ANON_, scope=CTD_ANON_19, documentation=u'Specifies target feature for which observations are requested. Mostly a hepler for in-situ sensors, since geo-location has to be done on the server side. The supported area should be listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'responseMode'), responseModeType, scope=CTD_ANON_19, documentation=u'This element allows the client to request the form of the response.  The value of resultTemplate is used to retrieve an observation template \n\t\t\t\t\t\t\tthat will later be used in calls to GetResult.  The other options allow results to appear inline in a resultTag (inline), external to the observation element (out-of-band)\n\t\t\t\t\t\t\tor as a MIME attachment (attached)'))

CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'procedure'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_19, documentation=u"Index of a particular sensor if offering procedure is a Sensor Array. Allows client to request data from one or more sensors in the array. The size of the array should be specified in the selected offering capabilities. This is to support scenarios with sensor grids (we don't want to have one offering for each sensor in that case). Note that sensorML can describe Sensor Arrays too. \t\t\t\t\t\t\t\t\t\t"))
CTD_ANON_19._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offering')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'eventTime')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'procedure')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'observedProperty')), min_occurs=1, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'featureOfInterest')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'result')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'responseFormat')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'resultModel')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'responseMode')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_19._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_19._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'temporalOps'), pyxb.bundles.opengis._ogc.TemporalOpsType, abstract=pyxb.binding.datatypes.boolean(1), scope=CTD_ANON_20))
CTD_ANON_20._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ogc'), u'temporalOps')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_20._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_20._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_21._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'FeatureId'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_21, documentation=u'Identifier of the feature for which detailed information is requested. These identifiers are usually listed in the Contents section of the service metadata (Capabilities) document. '))
CTD_ANON_21._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_21._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'FeatureId')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_21._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_21._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'responseMode'), responseModeType, scope=CTD_ANON_22, documentation=u'This element allows the client to request the form of the response.  The value of resultTemplate is used to retrieve an observation template \n\t\t\t\t\t\t\tthat will later be used in calls to GetResult.  The other options allow results to appear inline in a resultTag (inline), external to the observation element (out-of-band)\n\t\t\t\t\t\t\tor as a MIME attachment (attached)'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'resultModel'), pyxb.binding.datatypes.QName, scope=CTD_ANON_22))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'responseFormat'), pyxb.bundles.opengis.ows_1_1.MimeType, scope=CTD_ANON_22, documentation=u'ID of the output format to be used for the requested data. The supported output formats are listed in the selected offering capabilities.\n\t\t\t\t\t\t\t\t'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ObservationId'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_22, documentation=u'ID of the observation to obtain.  This could have been obtained by the client via a URL in a feed, alert, or some other notification\n\t\t\t\t\t\t\t\t'))
CTD_ANON_22._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ObservationId')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'responseFormat')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'resultModel')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'responseMode')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_22._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_22._GroupModel, min_occurs=1, max_occurs=1)


CTD_ANON_23._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'AcceptVersions')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'Sections')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'AcceptFormats')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_23._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_23._GroupModel_, min_occurs=1, max_occurs=1)



CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'procedure'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_24, documentation=u'Identifier of the sensor, for which detailed metadata is requested.'))
CTD_ANON_24._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'procedure')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_24._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_24._GroupModel, min_occurs=1, max_occurs=1)


CTD_ANON_25._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, u'http://www.opengis.net/sos/1.0')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_25._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_25._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_26._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Filter_Capabilities'), CTD_ANON_13, scope=CTD_ANON_26))

CTD_ANON_26._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Contents'), CTD_ANON_3, scope=CTD_ANON_26, documentation=u'Contents section of SOS service metadata (or Capabilites) XML document. For the SOS, these contents are data and functions that the SOS server provides.'))
CTD_ANON_26._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_26._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'ServiceIdentification')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_26._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'ServiceProvider')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_26._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/ows/1.1'), u'OperationsMetadata')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_26._GroupModel_3 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_26._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Filter_Capabilities')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_26._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Contents')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_26._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_26._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_26._GroupModel_3, min_occurs=1, max_occurs=1)
    )
CTD_ANON_26._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_26._GroupModel_, min_occurs=1, max_occurs=1)



CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'AssignedObservationId'), pyxb.binding.datatypes.anyURI, scope=CTD_ANON_27))
CTD_ANON_27._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'AssignedObservationId')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_27._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_27._GroupModel, min_occurs=1, max_occurs=1)

srsName._setSubstitutionGroup(pyxb.bundles.opengis.ows_1_1.AbstractMetaData)

supportedSensorDescription._setSubstitutionGroup(pyxb.bundles.opengis.ows_1_1.AbstractMetaData)

supportedSRS._setSubstitutionGroup(pyxb.bundles.opengis.gml.name)
