# ./pyxb/bundles/opengis/citygml/raw/generics.py
# PyXB bindings for NM:4d50e2a60871b1f7f72bd15af8e2596f999485f1
# Generated 2011-09-09 14:19:23.863421 by PyXB version 1.1.3
# Namespace http://www.opengis.net/citygml/generics/1.0

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9fd276dc-db18-11e0-8926-001fbc013adc')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.opengis.citygml.base
import pyxb.bundles.opengis.gml

Namespace = pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/citygml/generics/1.0', create_if_missing=True)
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


# Complex type AbstractGenericAttributeType with content type EMPTY
class AbstractGenericAttributeType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'AbstractGenericAttributeType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_netcitygmlgenerics1_0_AbstractGenericAttributeType_name', pyxb.binding.datatypes.string, required=True)
    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'AbstractGenericAttributeType', AbstractGenericAttributeType)


# Complex type UriAttributeType with content type ELEMENT_ONLY
class UriAttributeType (AbstractGenericAttributeType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'UriAttributeType')
    # Base type is AbstractGenericAttributeType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netcitygmlgenerics1_0_UriAttributeType_httpwww_opengis_netcitygmlgenerics1_0value', False)

    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute name inherited from {http://www.opengis.net/citygml/generics/1.0}AbstractGenericAttributeType

    _ElementMap = AbstractGenericAttributeType._ElementMap.copy()
    _ElementMap.update({
        __value.name() : __value
    })
    _AttributeMap = AbstractGenericAttributeType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'UriAttributeType', UriAttributeType)


# Complex type IntAttributeType with content type ELEMENT_ONLY
class IntAttributeType (AbstractGenericAttributeType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IntAttributeType')
    # Base type is AbstractGenericAttributeType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netcitygmlgenerics1_0_IntAttributeType_httpwww_opengis_netcitygmlgenerics1_0value', False)

    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute name inherited from {http://www.opengis.net/citygml/generics/1.0}AbstractGenericAttributeType

    _ElementMap = AbstractGenericAttributeType._ElementMap.copy()
    _ElementMap.update({
        __value.name() : __value
    })
    _AttributeMap = AbstractGenericAttributeType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'IntAttributeType', IntAttributeType)


# Complex type StringAttributeType with content type ELEMENT_ONLY
class StringAttributeType (AbstractGenericAttributeType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'StringAttributeType')
    # Base type is AbstractGenericAttributeType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netcitygmlgenerics1_0_StringAttributeType_httpwww_opengis_netcitygmlgenerics1_0value', False)

    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute name inherited from {http://www.opengis.net/citygml/generics/1.0}AbstractGenericAttributeType

    _ElementMap = AbstractGenericAttributeType._ElementMap.copy()
    _ElementMap.update({
        __value.name() : __value
    })
    _AttributeMap = AbstractGenericAttributeType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'StringAttributeType', StringAttributeType)


# Complex type DoubleAttributeType with content type ELEMENT_ONLY
class DoubleAttributeType (AbstractGenericAttributeType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DoubleAttributeType')
    # Base type is AbstractGenericAttributeType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netcitygmlgenerics1_0_DoubleAttributeType_httpwww_opengis_netcitygmlgenerics1_0value', False)

    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute name inherited from {http://www.opengis.net/citygml/generics/1.0}AbstractGenericAttributeType

    _ElementMap = AbstractGenericAttributeType._ElementMap.copy()
    _ElementMap.update({
        __value.name() : __value
    })
    _AttributeMap = AbstractGenericAttributeType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'DoubleAttributeType', DoubleAttributeType)


# Complex type GenericCityObjectType with content type ELEMENT_ONLY
class GenericCityObjectType (pyxb.bundles.opengis.citygml.base.AbstractCityObjectType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'GenericCityObjectType')
    # Base type is pyxb.bundles.opengis.citygml.base.AbstractCityObjectType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod2Geometry uses Python identifier lod2Geometry
    __lod2Geometry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod2Geometry'), 'lod2Geometry', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod2Geometry', False)

    
    lod2Geometry = property(__lod2Geometry.value, __lod2Geometry.set, None, None)

    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod3Geometry uses Python identifier lod3Geometry
    __lod3Geometry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod3Geometry'), 'lod3Geometry', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod3Geometry', False)

    
    lod3Geometry = property(__lod3Geometry.value, __lod3Geometry.set, None, None)

    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod4Geometry uses Python identifier lod4Geometry
    __lod4Geometry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod4Geometry'), 'lod4Geometry', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod4Geometry', False)

    
    lod4Geometry = property(__lod4Geometry.value, __lod4Geometry.set, None, None)

    
    # Element location ({http://www.opengis.net/gml}location) inherited from {http://www.opengis.net/gml}AbstractFeatureType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod0TerrainIntersection uses Python identifier lod0TerrainIntersection
    __lod0TerrainIntersection = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod0TerrainIntersection'), 'lod0TerrainIntersection', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod0TerrainIntersection', False)

    
    lod0TerrainIntersection = property(__lod0TerrainIntersection.value, __lod0TerrainIntersection.set, None, None)

    
    # Element generalizesTo ({http://www.opengis.net/citygml/1.0}generalizesTo) inherited from {http://www.opengis.net/citygml/1.0}AbstractCityObjectType
    
    # Element boundedBy ({http://www.opengis.net/gml}boundedBy) inherited from {http://www.opengis.net/gml}AbstractFeatureType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod1TerrainIntersection uses Python identifier lod1TerrainIntersection
    __lod1TerrainIntersection = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod1TerrainIntersection'), 'lod1TerrainIntersection', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod1TerrainIntersection', False)

    
    lod1TerrainIntersection = property(__lod1TerrainIntersection.value, __lod1TerrainIntersection.set, None, None)

    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod2TerrainIntersection uses Python identifier lod2TerrainIntersection
    __lod2TerrainIntersection = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod2TerrainIntersection'), 'lod2TerrainIntersection', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod2TerrainIntersection', False)

    
    lod2TerrainIntersection = property(__lod2TerrainIntersection.value, __lod2TerrainIntersection.set, None, None)

    
    # Element creationDate ({http://www.opengis.net/citygml/1.0}creationDate) inherited from {http://www.opengis.net/citygml/1.0}AbstractCityObjectType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod3TerrainIntersection uses Python identifier lod3TerrainIntersection
    __lod3TerrainIntersection = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod3TerrainIntersection'), 'lod3TerrainIntersection', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod3TerrainIntersection', False)

    
    lod3TerrainIntersection = property(__lod3TerrainIntersection.value, __lod3TerrainIntersection.set, None, None)

    
    # Element metaDataProperty ({http://www.opengis.net/gml}metaDataProperty) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod4TerrainIntersection uses Python identifier lod4TerrainIntersection
    __lod4TerrainIntersection = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod4TerrainIntersection'), 'lod4TerrainIntersection', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod4TerrainIntersection', False)

    
    lod4TerrainIntersection = property(__lod4TerrainIntersection.value, __lod4TerrainIntersection.set, None, None)

    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod0ImplicitRepresentation uses Python identifier lod0ImplicitRepresentation
    __lod0ImplicitRepresentation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod0ImplicitRepresentation'), 'lod0ImplicitRepresentation', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod0ImplicitRepresentation', False)

    
    lod0ImplicitRepresentation = property(__lod0ImplicitRepresentation.value, __lod0ImplicitRepresentation.set, None, None)

    
    # Element GenericApplicationPropertyOfCityObject ({http://www.opengis.net/citygml/1.0}_GenericApplicationPropertyOfCityObject) inherited from {http://www.opengis.net/citygml/1.0}AbstractCityObjectType
    
    # Element externalReference ({http://www.opengis.net/citygml/1.0}externalReference) inherited from {http://www.opengis.net/citygml/1.0}AbstractCityObjectType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod1ImplicitRepresentation uses Python identifier lod1ImplicitRepresentation
    __lod1ImplicitRepresentation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod1ImplicitRepresentation'), 'lod1ImplicitRepresentation', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod1ImplicitRepresentation', False)

    
    lod1ImplicitRepresentation = property(__lod1ImplicitRepresentation.value, __lod1ImplicitRepresentation.set, None, None)

    
    # Element {http://www.opengis.net/citygml/generics/1.0}class uses Python identifier class_
    __class = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'class'), 'class_', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0class', False)

    
    class_ = property(__class.value, __class.set, None, None)

    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod2ImplicitRepresentation uses Python identifier lod2ImplicitRepresentation
    __lod2ImplicitRepresentation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod2ImplicitRepresentation'), 'lod2ImplicitRepresentation', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod2ImplicitRepresentation', False)

    
    lod2ImplicitRepresentation = property(__lod2ImplicitRepresentation.value, __lod2ImplicitRepresentation.set, None, None)

    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod3ImplicitRepresentation uses Python identifier lod3ImplicitRepresentation
    __lod3ImplicitRepresentation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod3ImplicitRepresentation'), 'lod3ImplicitRepresentation', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod3ImplicitRepresentation', False)

    
    lod3ImplicitRepresentation = property(__lod3ImplicitRepresentation.value, __lod3ImplicitRepresentation.set, None, None)

    
    # Element {http://www.opengis.net/citygml/generics/1.0}function uses Python identifier function
    __function = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'function'), 'function', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0function', True)

    
    function = property(__function.value, __function.set, None, None)

    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod4ImplicitRepresentation uses Python identifier lod4ImplicitRepresentation
    __lod4ImplicitRepresentation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod4ImplicitRepresentation'), 'lod4ImplicitRepresentation', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod4ImplicitRepresentation', False)

    
    lod4ImplicitRepresentation = property(__lod4ImplicitRepresentation.value, __lod4ImplicitRepresentation.set, None, None)

    
    # Element {http://www.opengis.net/citygml/generics/1.0}usage uses Python identifier usage
    __usage = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'usage'), 'usage', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0usage', True)

    
    usage = property(__usage.value, __usage.set, None, None)

    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod0Geometry uses Python identifier lod0Geometry
    __lod0Geometry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod0Geometry'), 'lod0Geometry', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod0Geometry', False)

    
    lod0Geometry = property(__lod0Geometry.value, __lod0Geometry.set, None, None)

    
    # Element name ({http://www.opengis.net/gml}name) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Element terminationDate ({http://www.opengis.net/citygml/1.0}terminationDate) inherited from {http://www.opengis.net/citygml/1.0}AbstractCityObjectType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}lod1Geometry uses Python identifier lod1Geometry
    __lod1Geometry = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'lod1Geometry'), 'lod1Geometry', '__httpwww_opengis_netcitygmlgenerics1_0_GenericCityObjectType_httpwww_opengis_netcitygmlgenerics1_0lod1Geometry', False)

    
    lod1Geometry = property(__lod1Geometry.value, __lod1Geometry.set, None, None)

    
    # Element description ({http://www.opengis.net/gml}description) inherited from {http://www.opengis.net/gml}AbstractGMLType
    
    # Attribute id inherited from {http://www.opengis.net/gml}AbstractGMLType

    _ElementMap = pyxb.bundles.opengis.citygml.base.AbstractCityObjectType._ElementMap.copy()
    _ElementMap.update({
        __lod2Geometry.name() : __lod2Geometry,
        __lod3Geometry.name() : __lod3Geometry,
        __lod4Geometry.name() : __lod4Geometry,
        __lod0TerrainIntersection.name() : __lod0TerrainIntersection,
        __lod1TerrainIntersection.name() : __lod1TerrainIntersection,
        __lod2TerrainIntersection.name() : __lod2TerrainIntersection,
        __lod3TerrainIntersection.name() : __lod3TerrainIntersection,
        __lod4TerrainIntersection.name() : __lod4TerrainIntersection,
        __lod0ImplicitRepresentation.name() : __lod0ImplicitRepresentation,
        __lod1ImplicitRepresentation.name() : __lod1ImplicitRepresentation,
        __class.name() : __class,
        __lod2ImplicitRepresentation.name() : __lod2ImplicitRepresentation,
        __lod3ImplicitRepresentation.name() : __lod3ImplicitRepresentation,
        __function.name() : __function,
        __lod4ImplicitRepresentation.name() : __lod4ImplicitRepresentation,
        __usage.name() : __usage,
        __lod0Geometry.name() : __lod0Geometry,
        __lod1Geometry.name() : __lod1Geometry
    })
    _AttributeMap = pyxb.bundles.opengis.citygml.base.AbstractCityObjectType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'GenericCityObjectType', GenericCityObjectType)


# Complex type DateAttributeType with content type ELEMENT_ONLY
class DateAttributeType (AbstractGenericAttributeType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DateAttributeType')
    # Base type is AbstractGenericAttributeType
    
    # Element {http://www.opengis.net/citygml/generics/1.0}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_netcitygmlgenerics1_0_DateAttributeType_httpwww_opengis_netcitygmlgenerics1_0value', False)

    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute name inherited from {http://www.opengis.net/citygml/generics/1.0}AbstractGenericAttributeType

    _ElementMap = AbstractGenericAttributeType._ElementMap.copy()
    _ElementMap.update({
        __value.name() : __value
    })
    _AttributeMap = AbstractGenericAttributeType._AttributeMap.copy()
    _AttributeMap.update({
        
    })
Namespace.addCategoryObject('typeBinding', u'DateAttributeType', DateAttributeType)


genericAttribute = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'_genericAttribute'), AbstractGenericAttributeType, abstract=pyxb.binding.datatypes.boolean(1))
Namespace.addCategoryObject('elementBinding', genericAttribute.name().localName(), genericAttribute)

uriAttribute = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uriAttribute'), UriAttributeType)
Namespace.addCategoryObject('elementBinding', uriAttribute.name().localName(), uriAttribute)

intAttribute = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'intAttribute'), IntAttributeType)
Namespace.addCategoryObject('elementBinding', intAttribute.name().localName(), intAttribute)

stringAttribute = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'stringAttribute'), StringAttributeType)
Namespace.addCategoryObject('elementBinding', stringAttribute.name().localName(), stringAttribute)

doubleAttribute = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'doubleAttribute'), DoubleAttributeType)
Namespace.addCategoryObject('elementBinding', doubleAttribute.name().localName(), doubleAttribute)

GenericCityObject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'GenericCityObject'), GenericCityObjectType)
Namespace.addCategoryObject('elementBinding', GenericCityObject.name().localName(), GenericCityObject)

dateAttribute = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dateAttribute'), DateAttributeType)
Namespace.addCategoryObject('elementBinding', dateAttribute.name().localName(), dateAttribute)



UriAttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.anyURI, scope=UriAttributeType))
UriAttributeType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(UriAttributeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=1, max_occurs=1)
    )
UriAttributeType._ContentModel = pyxb.binding.content.ParticleModel(UriAttributeType._GroupModel, min_occurs=1, max_occurs=1)



IntAttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.integer, scope=IntAttributeType))
IntAttributeType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(IntAttributeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=1, max_occurs=1)
    )
IntAttributeType._ContentModel = pyxb.binding.content.ParticleModel(IntAttributeType._GroupModel, min_occurs=1, max_occurs=1)



StringAttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.string, scope=StringAttributeType))
StringAttributeType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(StringAttributeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=1, max_occurs=1)
    )
StringAttributeType._ContentModel = pyxb.binding.content.ParticleModel(StringAttributeType._GroupModel, min_occurs=1, max_occurs=1)



DoubleAttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.double, scope=DoubleAttributeType))
DoubleAttributeType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DoubleAttributeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=1, max_occurs=1)
    )
DoubleAttributeType._ContentModel = pyxb.binding.content.ParticleModel(DoubleAttributeType._GroupModel, min_occurs=1, max_occurs=1)



GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod2Geometry'), pyxb.bundles.opengis.gml.GeometryPropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod3Geometry'), pyxb.bundles.opengis.gml.GeometryPropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod4Geometry'), pyxb.bundles.opengis.gml.GeometryPropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod0TerrainIntersection'), pyxb.bundles.opengis.gml.MultiCurvePropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod1TerrainIntersection'), pyxb.bundles.opengis.gml.MultiCurvePropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod2TerrainIntersection'), pyxb.bundles.opengis.gml.MultiCurvePropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod3TerrainIntersection'), pyxb.bundles.opengis.gml.MultiCurvePropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod4TerrainIntersection'), pyxb.bundles.opengis.gml.MultiCurvePropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod0ImplicitRepresentation'), pyxb.bundles.opengis.citygml.base.ImplicitRepresentationPropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod1ImplicitRepresentation'), pyxb.bundles.opengis.citygml.base.ImplicitRepresentationPropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'class'), pyxb.binding.datatypes.string, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod2ImplicitRepresentation'), pyxb.bundles.opengis.citygml.base.ImplicitRepresentationPropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod3ImplicitRepresentation'), pyxb.bundles.opengis.citygml.base.ImplicitRepresentationPropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'function'), pyxb.binding.datatypes.string, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod4ImplicitRepresentation'), pyxb.bundles.opengis.citygml.base.ImplicitRepresentationPropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'usage'), pyxb.binding.datatypes.string, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod0Geometry'), pyxb.bundles.opengis.gml.GeometryPropertyType, scope=GenericCityObjectType))

GenericCityObjectType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'lod1Geometry'), pyxb.bundles.opengis.gml.GeometryPropertyType, scope=GenericCityObjectType))
GenericCityObjectType._GroupModel_14 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'metaDataProperty')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'name')), min_occurs=0L, max_occurs=None)
    )
GenericCityObjectType._GroupModel_13 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GenericCityObjectType._GroupModel_14, min_occurs=1, max_occurs=1)
    )
GenericCityObjectType._GroupModel_15 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'boundedBy')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/gml'), u'location')), min_occurs=0L, max_occurs=1)
    )
GenericCityObjectType._GroupModel_12 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GenericCityObjectType._GroupModel_13, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._GroupModel_15, min_occurs=1, max_occurs=1)
    )
GenericCityObjectType._GroupModel_16 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/citygml/1.0'), u'creationDate')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/citygml/1.0'), u'terminationDate')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/citygml/1.0'), u'externalReference')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/citygml/1.0'), u'generalizesTo')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/citygml/1.0'), u'_GenericApplicationPropertyOfCityObject')), min_occurs=0L, max_occurs=None)
    )
GenericCityObjectType._GroupModel_11 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GenericCityObjectType._GroupModel_12, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._GroupModel_16, min_occurs=1, max_occurs=1)
    )
GenericCityObjectType._GroupModel_17 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'class')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'function')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'usage')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod0Geometry')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod1Geometry')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod2Geometry')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod3Geometry')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod4Geometry')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod0TerrainIntersection')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod1TerrainIntersection')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod2TerrainIntersection')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod3TerrainIntersection')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod4TerrainIntersection')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod0ImplicitRepresentation')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod1ImplicitRepresentation')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod2ImplicitRepresentation')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod3ImplicitRepresentation')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'lod4ImplicitRepresentation')), min_occurs=0L, max_occurs=1)
    )
GenericCityObjectType._GroupModel_10 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(GenericCityObjectType._GroupModel_11, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(GenericCityObjectType._GroupModel_17, min_occurs=1, max_occurs=1)
    )
GenericCityObjectType._ContentModel = pyxb.binding.content.ParticleModel(GenericCityObjectType._GroupModel_10, min_occurs=1, max_occurs=1)



DateAttributeType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), pyxb.binding.datatypes.date, scope=DateAttributeType))
DateAttributeType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DateAttributeType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=1, max_occurs=1)
    )
DateAttributeType._ContentModel = pyxb.binding.content.ParticleModel(DateAttributeType._GroupModel, min_occurs=1, max_occurs=1)

genericAttribute._setSubstitutionGroup(pyxb.bundles.opengis.citygml.base.GenericApplicationPropertyOfCityObject)

uriAttribute._setSubstitutionGroup(genericAttribute)

intAttribute._setSubstitutionGroup(genericAttribute)

stringAttribute._setSubstitutionGroup(genericAttribute)

doubleAttribute._setSubstitutionGroup(genericAttribute)

GenericCityObject._setSubstitutionGroup(pyxb.bundles.opengis.citygml.base.CityObject)

dateAttribute._setSubstitutionGroup(genericAttribute)
