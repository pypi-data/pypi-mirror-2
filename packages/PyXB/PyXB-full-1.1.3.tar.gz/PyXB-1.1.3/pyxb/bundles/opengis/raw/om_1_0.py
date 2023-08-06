# ./pyxb/bundles/opengis/raw/om_1_0.py
# PyXB bindings for NM:c0f4d50579dd9a32da006ca53fd33f552201da56
# Generated 2011-09-09 14:19:06.690887 by PyXB version 1.1.3
# Namespace http://www.opengis.net/om/1.0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:95805ca8-db18-11e0-91bc-001fbc013adc')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.opengis.misc.xlinks
import pyxb.bundles.opengis.gml
import pyxb.bundles.opengis.swe_1_0_1
import pyxb.bundles.opengis.sensorML_1_0_1

Namespace = pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/om/1.0', create_if_missing=True)
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


# Complex type AnyOrReferenceType with content type ELEMENT_ONLY
class AnyOrReferenceType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AnyOrReferenceType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netom1_0_AnyOrReferenceType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netom1_0_AnyOrReferenceType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netom1_0_AnyOrReferenceType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netom1_0_AnyOrReferenceType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netom1_0_AnyOrReferenceType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netom1_0_AnyOrReferenceType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netom1_0_AnyOrReferenceType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netom1_0_AnyOrReferenceType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    _HasWildcardElement = True

    _ElementMap = {
        
    }
    _AttributeMap = {
        __title.name() : __title,
        __remoteSchema.name() : __remoteSchema,
        __type.name() : __type,
        __role.name() : __role,
        __arcrole.name() : __arcrole,
        __show.name() : __show,
        __actuate.name() : __actuate,
        __href.name() : __href
    }
Namespace.addCategoryObject('typeBinding', u'AnyOrReferenceType', AnyOrReferenceType)


# Complex type ObservationType with content type ELEMENT_ONLY
class ObservationType (pyxb.bundles.opengis.gml.AbstractFeatureType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObservationType')
    # Base type is pyxb.bundles.opengis.gml.AbstractFeatureType
    
    # Element {http://www.opengis.net/om/1.0}resultQuality uses Python identifier resultQuality
    __resultQuality = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'resultQuality'), 'resultQuality', '__httpwww_opengis_netom1_0_ObservationType_httpwww_opengis_netom1_0resultQuality', False)

    
    resultQuality = property(__resultQuality.value, __resultQuality.set, None, u'Instance-specific quality assessment or measure. \n\t\t\t\t\t\t\tAllow multiple quality measures if required.\t\t\t\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\tReplace with reference to ISO Metadata entity when GML version 3.2.X has been formally adopted.')

    
    # Element {http://www.opengis.net/om/1.0}parameter uses Python identifier parameter
    __parameter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'parameter'), 'parameter', '__httpwww_opengis_netom1_0_ObservationType_httpwww_opengis_netom1_0parameter', True)

    
    parameter = property(__parameter.value, __parameter.set, None, u'An Observation parameter is a general event-specific parameter. \n\t\t\t\t\t\t\tThis will typically be used to record environmental parameters, or event-specific sampling parameters that are not tightly bound to either the feature-of-interest or the procedure. \n\t\t\t\t\t\t\tNOTE: \tParameters that are tightly bound to the procedure should be recorded as part of the procedure description. For example, the SensorML model associates parameters with specific process elements or stages. \n\t\t\t\t\t\t\tNOTE: \tThe semantics of the parameter must be provided as part of its value. \n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\tIn some applications it is convenient to use a generic or standard procedure, or feature-of-interest, rather than define an event-specific process or feature. \n\t\t\t\t\t\t\tIn this context, event-specific parameters are bound to the Observation act.')

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/om/1.0}resultTime uses Python identifier resultTime
    __resultTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'resultTime'), 'resultTime', '__httpwww_opengis_netom1_0_ObservationType_httpwww_opengis_netom1_0resultTime', False)

    
    resultTime = property(__resultTime.value, __resultTime.set, None, u'The resultTime is the time when the procedure associated with the observation act was applied. \n\t\t\t\t\tFor some observations this is identical to samplingTime, in which case the resultTime may be omitted. \n\t\t\t\t\t\n\t\t\t\t\tExample: \tWhere a measurement is made on a specimen in a laboratory, the samplingTime should record the time the specimen was retrieved from its host, while the resultTime should record the time the laboratory procedure was applied. \n\t\t\t\t\tExample: \tWhere sensor observation results are post-processed, the resultTime is the post-processing time, while the samplingTime preserves the time of initial interaction with the world. \n\t\t\t\t\tExample: \tSimulations are often used to estimate the values for phenomena in the future or past. The samplingTime is the real-world time that the result applies to, while the resultTime is the time that the simulation process was executed.')

    
    # Element boundedBy ({http://www.opengis.net/gml}boundedBy) inherited from {http://www.opengis.net/gml}AbstractFeatureType
    
    # Element {http://www.opengis.net/om/1.0}observedProperty uses Python identifier observedProperty
    __observedProperty = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'observedProperty'), 'observedProperty', '__httpwww_opengis_netom1_0_ObservationType_httpwww_opengis_netom1_0observedProperty', False)

    
    observedProperty = property(__observedProperty.value, __observedProperty.set, None, u'Property-type or phenomenon for which the observation result provides an estimate of its value. \n\t\t\t\t\t\t\tfor example "wavelength", "grass-species", "power", "intensity in the waveband x-y", etc. \n\t\t\t\t\t\t\tIt must be a property associated with the type of the feature of interest. \n\t\t\t\t\t\t\tThis feature-property that provides the (semantic) type of the observation. \n\t\t\t\t\t\t\tThe description of the phenomenon may be quite specific and constrained. \n\n\t\t\t\t\t\t\tThe description of the property-type may be presented using various alternative encodings. \n\t\t\t\t\t\t\tIf shown inline, the swe:Phenomenon schema is required. \n\t\t\t\t\t\t\tIf provided using another encoding (e.g. OWL or SWEET) then the description must be in a remote repository and xlink reference used.')

    
    # Element location ({http://www.opengis.net/gml}location) inherited from {http://www.opengis.net/gml}AbstractFeatureType
    
    # Element {http://www.opengis.net/om/1.0}metadata uses Python identifier metadata
    __metadata = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'metadata'), 'metadata', '__httpwww_opengis_netom1_0_ObservationType_httpwww_opengis_netom1_0metadata', False)

    
    metadata = property(__metadata.value, __metadata.set, None, u'Replace with reference to ISO Metadata entity when GML version 3.2.X has been formally adopted.')

    
    # Element {http://www.opengis.net/om/1.0}result uses Python identifier result
    __result = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'result'), 'result', '__httpwww_opengis_netom1_0_ObservationType_httpwww_opengis_netom1_0result', False)

    
    result = property(__result.value, __result.set, None, u'The result contains the value generated by the procedure. \n\t\t\t\t\t\t\tThe type of the observation result must be consistent with the observed property, and the scale or scope for the value must be consistent with the quantity or category type. \n\t\t\t\t\t\t\tApplication profiles may choose to constrain the type of the result.')

    
    # Element {http://www.opengis.net/om/1.0}procedure uses Python identifier procedure
    __procedure = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'procedure'), 'procedure', '__httpwww_opengis_netom1_0_ObservationType_httpwww_opengis_netom1_0procedure', False)

    
    procedure = property(__procedure.value, __procedure.set, None, u'The procedure is the description of a process used to generate the result. \n\t\t\t\t\t\t\tIt must be suitable for the observed property. \n\t\t\t\t\t\t\tNOTE: \tAt this level we do not distinguish between sensor-observations, \n\t\t\t\t\t\t\testimations made by an observer, or algorithms, simulations, computations and complex processing chains.')

    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/om/1.0}featureOfInterest uses Python identifier featureOfInterest
    __featureOfInterest = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'featureOfInterest'), 'featureOfInterest', '__httpwww_opengis_netom1_0_ObservationType_httpwww_opengis_netom1_0featureOfInterest', False)

    
    featureOfInterest = property(__featureOfInterest.value, __featureOfInterest.set, None, u'The featureOfInterest is a feature of any type (ISO 19109, ISO 19101), which is a representation of the observation target, being the real-world object regarding which the observation is made. \n\t\t\t\t\t\t\tsuch as a specimen, station, tract, mountain, pixel, etc. \n\t\t\t\t\t\t\tThe spatial properties (location) of this feature of interest are typically of most interest for spatial analysis of the observation result.')

    
    # Element {http://www.opengis.net/om/1.0}samplingTime uses Python identifier samplingTime
    __samplingTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'samplingTime'), 'samplingTime', '__httpwww_opengis_netom1_0_ObservationType_httpwww_opengis_netom1_0samplingTime', False)

    
    samplingTime = property(__samplingTime.value, __samplingTime.set, None, u'The samplingTime is the time that the result applies to the feature-of-interest. \n\t\t\t\t\tThis is the time usually required for geospatial analysis of the result.')

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = pyxb.bundles.opengis.gml.AbstractFeatureType._ElementMap.copy()
    _ElementMap.update({
        __resultQuality.name() : __resultQuality,
        __parameter.name() : __parameter,
        __resultTime.name() : __resultTime,
        __observedProperty.name() : __observedProperty,
        __metadata.name() : __metadata,
        __result.name() : __result,
        __procedure.name() : __procedure,
        __featureOfInterest.name() : __featureOfInterest,
        __samplingTime.name() : __samplingTime
    })
    _AttributeMap = pyxb.bundles.opengis.gml.AbstractFeatureType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ObservationType', ObservationType)


# Complex type ProcessPropertyType with content type ELEMENT_ONLY
class ProcessPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ProcessPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/sensorML/1.0.1}_Process uses Python identifier Process_
    __Process_ = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/sensorML/1.0.1'), u'_Process'), 'Process_', '__httpwww_opengis_netom1_0_ProcessPropertyType_httpwww_opengis_netsensorML1_0_1_Process', False)

    
    Process_ = property(__Process_.value, __Process_.set, None, u'base substitution group for all processes')

    
    # Element {http://www.opengis.net/om/1.0}Process uses Python identifier Process
    __Process = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Process'), 'Process', '__httpwww_opengis_netom1_0_ProcessPropertyType_httpwww_opengis_netom1_0Process', False)

    
    Process = property(__Process.value, __Process.set, None, u'This element is xs:anyType so may contain a description of a process provided in any well-formed XML. \n\t\t\t\tIf the process description is namespace qualified, then the namespace must be identified in the instance document.')

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netom1_0_ProcessPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netom1_0_ProcessPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netom1_0_ProcessPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netom1_0_ProcessPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netom1_0_ProcessPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netom1_0_ProcessPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netom1_0_ProcessPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netom1_0_ProcessPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)


    _ElementMap = {
        __Process_.name() : __Process_,
        __Process.name() : __Process
    }
    _AttributeMap = {
        __title.name() : __title,
        __type.name() : __type,
        __actuate.name() : __actuate,
        __arcrole.name() : __arcrole,
        __remoteSchema.name() : __remoteSchema,
        __href.name() : __href,
        __show.name() : __show,
        __role.name() : __role
    }
Namespace.addCategoryObject('typeBinding', u'ProcessPropertyType', ProcessPropertyType)


# Complex type ObservationPropertyType with content type ELEMENT_ONLY
class ObservationPropertyType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObservationPropertyType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/om/1.0}Observation uses Python identifier Observation
    __Observation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'Observation'), 'Observation', '__httpwww_opengis_netom1_0_ObservationPropertyType_httpwww_opengis_netom1_0Observation', False)

    
    Observation = property(__Observation.value, __Observation.set, None, u'Observation is an act ("event"), whose result is an estimate of the value of a property of the feature of interest. \n            The observed property may be any property associated with the type of the feature of interest.')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'href'), 'href', '__httpwww_opengis_netom1_0_ObservationPropertyType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'title'), 'title', '__httpwww_opengis_netom1_0_ObservationPropertyType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'role'), 'role', '__httpwww_opengis_netom1_0_ObservationPropertyType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.anyURI)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'type'), 'type', '__httpwww_opengis_netom1_0_ObservationPropertyType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'simple')
    
    type = property(__type.value, __type.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'arcrole'), 'arcrole', '__httpwww_opengis_netom1_0_ObservationPropertyType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.anyURI)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'show'), 'show', '__httpwww_opengis_netom1_0_ObservationPropertyType_httpwww_w3_org1999xlinkshow', pyxb.bundles.opengis.misc.xlinks.STD_ANON_)
    
    show = property(__show.value, __show.set, None, u"\n        The 'show' attribute is used to communicate the desired presentation \n        of the ending resource on traversal from the starting resource; it's \n        value should be treated as follows: \n        new - load ending resource in a new window, frame, pane, or other \n              presentation context\n        replace - load the resource in the same window, frame, pane, or \n                  other presentation context\n        embed - load ending resource in place of the presentation of the \n                starting resource\n        other - behavior is unconstrained; examine other markup in the \n                link for hints \n        none - behavior is unconstrained \n      ")

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.w3.org/1999/xlink'), u'actuate'), 'actuate', '__httpwww_opengis_netom1_0_ObservationPropertyType_httpwww_w3_org1999xlinkactuate', pyxb.bundles.opengis.misc.xlinks.STD_ANON)
    
    actuate = property(__actuate.value, __actuate.set, None, u"\n        The 'actuate' attribute is used to communicate the desired timing \n        of traversal from the starting resource to the ending resource; \n        it's value should be treated as follows:\n        onLoad - traverse to the ending resource immediately on loading \n                 the starting resource \n        onRequest - traverse from the starting resource to the ending \n                    resource only on a post-loading event triggered for \n                    this purpose \n        other - behavior is unconstrained; examine other markup in link \n                for hints \n        none - behavior is unconstrained\n      ")

    
    # Attribute {http://www.opengis.net/gml}remoteSchema uses Python identifier remoteSchema
    __remoteSchema = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'remoteSchema'), 'remoteSchema', '__httpwww_opengis_netom1_0_ObservationPropertyType_httpwww_opengis_netgmlremoteSchema', pyxb.binding.datatypes.anyURI)
    
    remoteSchema = property(__remoteSchema.value, __remoteSchema.set, None, u'Reference to an XML Schema fragment that specifies the content model of the propertys value. This is in conformance with the XML Schema Section 4.14 Referencing Schemas from Elsewhere.')


    _ElementMap = {
        __Observation.name() : __Observation
    }
    _AttributeMap = {
        __href.name() : __href,
        __title.name() : __title,
        __role.name() : __role,
        __type.name() : __type,
        __arcrole.name() : __arcrole,
        __show.name() : __show,
        __actuate.name() : __actuate,
        __remoteSchema.name() : __remoteSchema
    }
Namespace.addCategoryObject('typeBinding', u'ObservationPropertyType', ObservationPropertyType)


# Complex type ObservationCollectionType with content type ELEMENT_ONLY
class ObservationCollectionType (pyxb.bundles.opengis.gml.AbstractFeatureType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ObservationCollectionType')
    # Base type is pyxb.bundles.opengis.gml.AbstractFeatureType
    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element location ({http://www.opengis.net/gml}location) inherited from {http://www.opengis.net/gml}AbstractFeatureType
    
    # Element {http://www.opengis.net/om/1.0}member uses Python identifier member
    __member = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'member'), 'member', '__httpwww_opengis_netom1_0_ObservationCollectionType_httpwww_opengis_netom1_0member', True)

    
    member = property(__member.value, __member.set, None, None)

    
    # Element boundedBy ({http://www.opengis.net/gml}boundedBy) inherited from {http://www.opengis.net/gml}AbstractFeatureType
    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = pyxb.bundles.opengis.gml.AbstractFeatureType._ElementMap.copy()
    _ElementMap.update({
        __member.name() : __member
    })
    _AttributeMap = pyxb.bundles.opengis.gml.AbstractFeatureType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'ObservationCollectionType', ObservationCollectionType)


ObservationCollection = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ObservationCollection'), ObservationCollectionType, documentation=u'Collection of arbitrary observations')
Namespace.addCategoryObject('elementBinding', ObservationCollection.name().localName(), ObservationCollection)

Observation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Observation'), ObservationType, documentation=u'Observation is an act ("event"), whose result is an estimate of the value of a property of the feature of interest. \n            The observed property may be any property associated with the type of the feature of interest.')
Namespace.addCategoryObject('elementBinding', Observation.name().localName(), Observation)


AnyOrReferenceType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_strict, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), min_occurs=1, max_occurs=1)
    )
AnyOrReferenceType._ContentModel = pyxb.binding.content.ParticleModel(AnyOrReferenceType._GroupModel, min_occurs=0L, max_occurs=1)



ObservationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'resultQuality'), AnyOrReferenceType, scope=ObservationType, documentation=u'Instance-specific quality assessment or measure. \n\t\t\t\t\t\t\tAllow multiple quality measures if required.\t\t\t\n\t\t\t\t\t\t\t\t\t\n\t\t\t\t\tReplace with reference to ISO Metadata entity when GML version 3.2.X has been formally adopted.'))

ObservationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'parameter'), pyxb.bundles.opengis.swe_1_0_1.AnyDataPropertyType, scope=ObservationType, documentation=u'An Observation parameter is a general event-specific parameter. \n\t\t\t\t\t\t\tThis will typically be used to record environmental parameters, or event-specific sampling parameters that are not tightly bound to either the feature-of-interest or the procedure. \n\t\t\t\t\t\t\tNOTE: \tParameters that are tightly bound to the procedure should be recorded as part of the procedure description. For example, the SensorML model associates parameters with specific process elements or stages. \n\t\t\t\t\t\t\tNOTE: \tThe semantics of the parameter must be provided as part of its value. \n\t\t\t\t\t\t\t\n\t\t\t\t\t\t\tIn some applications it is convenient to use a generic or standard procedure, or feature-of-interest, rather than define an event-specific process or feature. \n\t\t\t\t\t\t\tIn this context, event-specific parameters are bound to the Observation act.'))

ObservationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'resultTime'), pyxb.bundles.opengis.swe_1_0_1.TimeObjectPropertyType, scope=ObservationType, documentation=u'The resultTime is the time when the procedure associated with the observation act was applied. \n\t\t\t\t\tFor some observations this is identical to samplingTime, in which case the resultTime may be omitted. \n\t\t\t\t\t\n\t\t\t\t\tExample: \tWhere a measurement is made on a specimen in a laboratory, the samplingTime should record the time the specimen was retrieved from its host, while the resultTime should record the time the laboratory procedure was applied. \n\t\t\t\t\tExample: \tWhere sensor observation results are post-processed, the resultTime is the post-processing time, while the samplingTime preserves the time of initial interaction with the world. \n\t\t\t\t\tExample: \tSimulations are often used to estimate the values for phenomena in the future or past. The samplingTime is the real-world time that the result applies to, while the resultTime is the time that the simulation process was executed.'))

ObservationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'observedProperty'), pyxb.bundles.opengis.swe_1_0_1.PhenomenonPropertyType, scope=ObservationType, documentation=u'Property-type or phenomenon for which the observation result provides an estimate of its value. \n\t\t\t\t\t\t\tfor example "wavelength", "grass-species", "power", "intensity in the waveband x-y", etc. \n\t\t\t\t\t\t\tIt must be a property associated with the type of the feature of interest. \n\t\t\t\t\t\t\tThis feature-property that provides the (semantic) type of the observation. \n\t\t\t\t\t\t\tThe description of the phenomenon may be quite specific and constrained. \n\n\t\t\t\t\t\t\tThe description of the property-type may be presented using various alternative encodings. \n\t\t\t\t\t\t\tIf shown inline, the swe:Phenomenon schema is required. \n\t\t\t\t\t\t\tIf provided using another encoding (e.g. OWL or SWEET) then the description must be in a remote repository and xlink reference used.'))

ObservationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'metadata'), AnyOrReferenceType, scope=ObservationType, documentation=u'Replace with reference to ISO Metadata entity when GML version 3.2.X has been formally adopted.'))

ObservationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'result'), pyxb.binding.datatypes.anyType, scope=ObservationType, documentation=u'The result contains the value generated by the procedure. \n\t\t\t\t\t\t\tThe type of the observation result must be consistent with the observed property, and the scale or scope for the value must be consistent with the quantity or category type. \n\t\t\t\t\t\t\tApplication profiles may choose to constrain the type of the result.'))

ObservationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'procedure'), ProcessPropertyType, scope=ObservationType, documentation=u'The procedure is the description of a process used to generate the result. \n\t\t\t\t\t\t\tIt must be suitable for the observed property. \n\t\t\t\t\t\t\tNOTE: \tAt this level we do not distinguish between sensor-observations, \n\t\t\t\t\t\t\testimations made by an observer, or algorithms, simulations, computations and complex processing chains.'))

ObservationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'featureOfInterest'), pyxb.bundles.opengis.gml.FeaturePropertyType, scope=ObservationType, documentation=u'The featureOfInterest is a feature of any type (ISO 19109, ISO 19101), which is a representation of the observation target, being the real-world object regarding which the observation is made. \n\t\t\t\t\t\t\tsuch as a specimen, station, tract, mountain, pixel, etc. \n\t\t\t\t\t\t\tThe spatial properties (location) of this feature of interest are typically of most interest for spatial analysis of the observation result.'))

ObservationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'samplingTime'), pyxb.bundles.opengis.swe_1_0_1.TimeObjectPropertyType, scope=ObservationType, documentation=u'The samplingTime is the time that the result applies to the feature-of-interest. \n\t\t\t\t\tThis is the time usually required for geospatial analysis of the result.'))
ObservationType._GroupModel_7 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
ObservationType._GroupModel_6 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationType._GroupModel_7, min_occurs=1, max_occurs=1)
    )
ObservationType._GroupModel_8 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'boundedBy')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'location')), min_occurs=0L, max_occurs=1)
    )
ObservationType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationType._GroupModel_6, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationType._GroupModel_8, min_occurs=1, max_occurs=1)
    )
ObservationType._GroupModel_9 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'metadata')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'samplingTime')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'resultTime')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'procedure')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'resultQuality')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'observedProperty')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'featureOfInterest')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'parameter')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObservationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'result')), min_occurs=1, max_occurs=1)
    )
ObservationType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationType._GroupModel_5, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationType._GroupModel_9, min_occurs=1, max_occurs=1)
    )
ObservationType._ContentModel = pyxb.binding.content.ParticleModel(ObservationType._GroupModel_4, min_occurs=1, max_occurs=1)



ProcessPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/sensorML/1.0.1'), u'_Process'), pyxb.bundles.opengis.sensorML_1_0_1.AbstractProcessType, abstract=pyxb.binding.datatypes.boolean(1), scope=ProcessPropertyType, documentation=u'base substitution group for all processes'))

ProcessPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Process'), pyxb.binding.datatypes.anyType, scope=ProcessPropertyType, documentation=u'This element is xs:anyType so may contain a description of a process provided in any well-formed XML. \n\t\t\t\tIf the process description is namespace qualified, then the namespace must be identified in the instance document.'))
ProcessPropertyType._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(ProcessPropertyType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/sensorML/1.0.1'), u'_Process')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ProcessPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Process')), min_occurs=1, max_occurs=1)
    )
ProcessPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ProcessPropertyType._GroupModel_, min_occurs=1, max_occurs=1)
    )
ProcessPropertyType._ContentModel = pyxb.binding.content.ParticleModel(ProcessPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



ObservationPropertyType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'Observation'), ObservationType, scope=ObservationPropertyType, documentation=u'Observation is an act ("event"), whose result is an estimate of the value of a property of the feature of interest. \n            The observed property may be any property associated with the type of the feature of interest.'))
ObservationPropertyType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationPropertyType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'Observation')), min_occurs=1, max_occurs=1)
    )
ObservationPropertyType._ContentModel = pyxb.binding.content.ParticleModel(ObservationPropertyType._GroupModel, min_occurs=0L, max_occurs=1)



ObservationCollectionType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'member'), ObservationPropertyType, scope=ObservationCollectionType))
ObservationCollectionType._GroupModel_7 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ObservationCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
ObservationCollectionType._GroupModel_6 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationCollectionType._GroupModel_7, min_occurs=1, max_occurs=1)
    )
ObservationCollectionType._GroupModel_8 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'boundedBy')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationCollectionType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'location')), min_occurs=0L, max_occurs=1)
    )
ObservationCollectionType._GroupModel_5 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationCollectionType._GroupModel_6, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationCollectionType._GroupModel_8, min_occurs=1, max_occurs=1)
    )
ObservationCollectionType._GroupModel_9 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationCollectionType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'member')), min_occurs=1, max_occurs=None)
    )
ObservationCollectionType._GroupModel_4 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ObservationCollectionType._GroupModel_5, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(ObservationCollectionType._GroupModel_9, min_occurs=1, max_occurs=1)
    )
ObservationCollectionType._ContentModel = pyxb.binding.content.ParticleModel(ObservationCollectionType._GroupModel_4, min_occurs=1, max_occurs=1)

ObservationCollection._setSubstitutionGroup(pyxb.bundles.opengis.gml.Feature)

Observation._setSubstitutionGroup(pyxb.bundles.opengis.gml.Feature)
