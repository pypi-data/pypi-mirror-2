# ./pyxb/bundles/opengis/raw/tml.py
# PyXB bindings for NM:ac607835b9362956c931ec92a7b6c78e5903799b
# Generated 2011-09-09 14:19:11.868104 by PyXB version 1.1.3
# Namespace http://www.opengis.net/tml

import pyxb
import pyxb.binding
import pyxb.binding.saxer
import StringIO
import pyxb.utils.utility
import pyxb.utils.domutils
import sys

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:9903a10a-db18-11e0-ba5a-001fbc013adc')

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import pyxb.bundles.opengis.ic_ism_2_1

Namespace = pyxb.namespace.NamespaceForURI(u'http://www.opengis.net/tml', create_if_missing=True)
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
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.exp = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'exp', tag=u'exp')
STD_ANON.imp = STD_ANON._CF_enumeration.addEnumeration(unicode_value=u'imp', tag=u'imp')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Complex type CTD_ANON with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}validatedBy uses Python identifier validatedBy
    __validatedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'validatedBy'), 'validatedBy', '__httpwww_opengis_nettml_CTD_ANON_httpwww_opengis_nettmlvalidatedBy', False)

    
    validatedBy = property(__validatedBy.value, __validatedBy.set, None, None)

    
    # Element {http://www.opengis.net/tml}characterizedBy uses Python identifier characterizedBy
    __characterizedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'characterizedBy'), 'characterizedBy', '__httpwww_opengis_nettml_CTD_ANON_httpwww_opengis_nettmlcharacterizedBy', False)

    
    characterizedBy = property(__characterizedBy.value, __characterizedBy.set, None, None)


    _ElementMap = {
        __validatedBy.name() : __validatedBy,
        __characterizedBy.name() : __characterizedBy
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
    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON__httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'uid of input')

    
    # Element {http://www.opengis.net/tml}description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'description'), 'description', '__httpwww_opengis_nettml_CTD_ANON__httpwww_opengis_nettmldescription', False)

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON__httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __uid.name() : __uid,
        __description.name() : __description,
        __name.name() : __name
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
    
    # Element {http://www.opengis.net/tml}email uses Python identifier email
    __email = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'email'), 'email', '__httpwww_opengis_nettml_CTD_ANON_2_httpwww_opengis_nettmlemail', False)

    
    email = property(__email.value, __email.set, None, None)

    
    # Element {http://www.opengis.net/tml}organization uses Python identifier organization
    __organization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'organization'), 'organization', '__httpwww_opengis_nettml_CTD_ANON_2_httpwww_opengis_nettmlorganization', False)

    
    organization = property(__organization.value, __organization.set, None, None)

    
    # Element {http://www.opengis.net/tml}date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'date'), 'date', '__httpwww_opengis_nettml_CTD_ANON_2_httpwww_opengis_nettmldate', False)

    
    date = property(__date.value, __date.set, None, u'ISO8601 dateTime stamp')

    
    # Element {http://www.opengis.net/tml}phone uses Python identifier phone
    __phone = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'phone'), 'phone', '__httpwww_opengis_nettml_CTD_ANON_2_httpwww_opengis_nettmlphone', False)

    
    phone = property(__phone.value, __phone.set, None, None)

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_2_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __email.name() : __email,
        __organization.name() : __organization,
        __date.name() : __date,
        __phone.name() : __phone,
        __name.name() : __name
    }
    _AttributeMap = {
        
    }



# Complex type ValueType with content type ELEMENT_ONLY
class ValueType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ValueType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}values uses Python identifier values
    __values = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'values'), 'values', '__httpwww_opengis_nettml_ValueType_httpwww_opengis_nettmlvalues', False)

    
    values = property(__values.value, __values.set, None, u'values can contain a single value or a string of values separated by a comma.  Each value can contain text,  number, or a range of numbers. Each range value shall contain two numbers separated by three decimal points (...), the first number identifies the closed end of the range and the second number identifies the open end of the range.  Values in the range may be integer or real numbers. Reals may use E for exponent.   In addition to numbers in the range the text -inf and inf can be used to represent -infinity and plus infinity respectively.  For arrayType of function interpolation between values should be handled as indicated in the fcnInterpolate element.')

    
    # Element {http://www.opengis.net/tml}fcnInterpol uses Python identifier fcnInterpol
    __fcnInterpol = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol'), 'fcnInterpol', '__httpwww_opengis_nettml_ValueType_httpwww_opengis_nettmlfcnInterpol', False)

    
    fcnInterpol = property(__fcnInterpol.value, __fcnInterpol.set, None, u'Allowed Values: continuous, discrete, lastValue, returnToZero, ')

    
    # Element {http://www.opengis.net/tml}accuracy uses Python identifier accuracy
    __accuracy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'accuracy'), 'accuracy', '__httpwww_opengis_nettml_ValueType_httpwww_opengis_nettmlaccuracy', True)

    
    accuracy = property(__accuracy.value, __accuracy.set, None, u'accuracy is in terms of the data value before adjustment by mult and offset.   if a characteristic frame (i.e. number of values) of values of accuracy, then each value corresponds to the corresponding Characteristic Frame  position or interval')

    
    # Element {http://www.opengis.net/tml}mult uses Python identifier mult
    __mult = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'mult'), 'mult', '__httpwww_opengis_nettml_ValueType_httpwww_opengis_nettmlmult', True)

    
    mult = property(__mult.value, __mult.set, None, u'default 1. if multiple values of mult, then each value corresponds to the corresponding Characteristic Frame position or interval. Can have a set of mult or offset equalization values and a sensor modifying those values through a bindUID.  The bindUID sensor value will multiply with the values in the mult element.')

    
    # Element {http://www.opengis.net/tml}numValues uses Python identifier numValues
    __numValues = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numValues'), 'numValues', '__httpwww_opengis_nettml_ValueType_httpwww_opengis_nettmlnumValues', False)

    
    numValues = property(__numValues.value, __numValues.set, None, u'number of points, or ranges in values element.   Allowed values: positive integer. Default is 0.')

    
    # Element {http://www.opengis.net/tml}valueDataType uses Python identifier valueDataType
    __valueDataType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'valueDataType'), 'valueDataType', '__httpwww_opengis_nettml_ValueType_httpwww_opengis_nettmlvalueDataType', False)

    
    valueDataType = property(__valueDataType.value, __valueDataType.set, None, u'data type of the value. Allowed values: text, number.  Default number')

    
    # Element {http://www.opengis.net/tml}offset uses Python identifier offset
    __offset = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'offset'), 'offset', '__httpwww_opengis_nettml_ValueType_httpwww_opengis_nettmloffset', True)

    
    offset = property(__offset.value, __offset.set, None, u'default 0. if multiple values of offset, then each value corresponds to the corresponding Characteristic Frame  position or interval.  Can have a set of mult or offset equalization values and a sensor modifying those values through a bindUID.  The bindUID sensor value will add with the values in the offset element.')

    
    # Element {http://www.opengis.net/tml}arrayType uses Python identifier arrayType
    __arrayType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'arrayType'), 'arrayType', '__httpwww_opengis_nettml_ValueType_httpwww_opengis_nettmlarrayType', False)

    
    arrayType = property(__arrayType.value, __arrayType.set, None, u'Allowed Values: fcn, charFrame. singleValue.  Default is fcn.   the value element can contain one or multiple values. ')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_ValueType_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_ValueType_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_ValueType_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __values.name() : __values,
        __fcnInterpol.name() : __fcnInterpol,
        __accuracy.name() : __accuracy,
        __mult.name() : __mult,
        __numValues.name() : __numValues,
        __valueDataType.name() : __valueDataType,
        __offset.name() : __offset,
        __arrayType.name() : __arrayType
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __uid.name() : __uid,
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'ValueType', ValueType)


# Complex type CTD_ANON_3 with content type ELEMENT_ONLY
class CTD_ANON_3 (ValueType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is ValueType
    
    # Element values ({http://www.opengis.net/tml}values) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element fcnInterpol ({http://www.opengis.net/tml}fcnInterpol) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element accuracy ({http://www.opengis.net/tml}accuracy) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element mult ({http://www.opengis.net/tml}mult) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element numValues ({http://www.opengis.net/tml}numValues) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element valueDataType ({http://www.opengis.net/tml}valueDataType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element offset ({http://www.opengis.net/tml}offset) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element arrayType ({http://www.opengis.net/tml}arrayType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uidRef inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uid inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute name inherited from {http://www.opengis.net/tml}ValueType

    _ElementMap = ValueType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ValueType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type BindType with content type SIMPLE
class BindType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'BindType')
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute bindUidRef uses Python identifier bindUidRef
    __bindUidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'bindUidRef'), 'bindUidRef', '__httpwww_opengis_nettml_BindType_bindUidRef', pyxb.binding.datatypes.string)
    
    bindUidRef = property(__bindUidRef.value, __bindUidRef.set, None, None)

    
    # Attribute bindUid uses Python identifier bindUid
    __bindUid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'bindUid'), 'bindUid', '__httpwww_opengis_nettml_BindType_bindUid', pyxb.binding.datatypes.string)
    
    bindUid = property(__bindUid.value, __bindUid.set, None, None)


    _ElementMap = {
        
    }
    _AttributeMap = {
        __bindUidRef.name() : __bindUidRef,
        __bindUid.name() : __bindUid
    }
Namespace.addCategoryObject('typeBinding', u'BindType', BindType)


# Complex type CTD_ANON_4 with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}frequency uses Python identifier frequency
    __frequency = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'frequency'), 'frequency', '__httpwww_opengis_nettml_CTD_ANON_4_httpwww_opengis_nettmlfrequency', False)

    
    frequency = property(__frequency.value, __frequency.set, None, u'Set of point coordinates describing frequency independent axis')

    
    # Element {http://www.opengis.net/tml}phase uses Python identifier phase
    __phase = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'phase'), 'phase', '__httpwww_opengis_nettml_CTD_ANON_4_httpwww_opengis_nettmlphase', False)

    
    phase = property(__phase.value, __phase.set, None, u'Set of point coordinates describing phase dependent axis')

    
    # Element {http://www.opengis.net/tml}freqRespType uses Python identifier freqRespType
    __freqRespType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'freqRespType'), 'freqRespType', '__httpwww_opengis_nettml_CTD_ANON_4_httpwww_opengis_nettmlfreqRespType', False)

    
    freqRespType = property(__freqRespType.value, __freqRespType.set, None, u'Allowed values: carried, modulation, PSD  (pwrSpectralDensity).  default carrier')

    
    # Element {http://www.opengis.net/tml}dataUidRef uses Python identifier dataUidRef
    __dataUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), 'dataUidRef', '__httpwww_opengis_nettml_CTD_ANON_4_httpwww_opengis_nettmldataUidRef', False)

    
    dataUidRef = property(__dataUidRef.value, __dataUidRef.set, None, u'same as uidRef in attributes')

    
    # Element {http://www.opengis.net/tml}amplitude uses Python identifier amplitude
    __amplitude = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'amplitude'), 'amplitude', '__httpwww_opengis_nettml_CTD_ANON_4_httpwww_opengis_nettmlamplitude', False)

    
    amplitude = property(__amplitude.value, __amplitude.set, None, u'Set of point coordinates describing amplitude dependent axis')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_4_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_4_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_4_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __frequency.name() : __frequency,
        __phase.name() : __phase,
        __freqRespType.name() : __freqRespType,
        __dataUidRef.name() : __dataUidRef,
        __amplitude.name() : __amplitude
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __uid.name() : __uid,
        __name.name() : __name
    }



# Complex type CTD_ANON_5 with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}email uses Python identifier email
    __email = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'email'), 'email', '__httpwww_opengis_nettml_CTD_ANON_5_httpwww_opengis_nettmlemail', False)

    
    email = property(__email.value, __email.set, None, None)

    
    # Element {http://www.opengis.net/tml}phone uses Python identifier phone
    __phone = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'phone'), 'phone', '__httpwww_opengis_nettml_CTD_ANON_5_httpwww_opengis_nettmlphone', False)

    
    phone = property(__phone.value, __phone.set, None, None)

    
    # Element {http://www.opengis.net/tml}date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'date'), 'date', '__httpwww_opengis_nettml_CTD_ANON_5_httpwww_opengis_nettmldate', False)

    
    date = property(__date.value, __date.set, None, u'ISO8601 dateTime stamp')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_5_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {http://www.opengis.net/tml}organization uses Python identifier organization
    __organization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'organization'), 'organization', '__httpwww_opengis_nettml_CTD_ANON_5_httpwww_opengis_nettmlorganization', False)

    
    organization = property(__organization.value, __organization.set, None, None)


    _ElementMap = {
        __email.name() : __email,
        __phone.name() : __phone,
        __date.name() : __date,
        __name.name() : __name,
        __organization.name() : __organization
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_6 with content type ELEMENT_ONLY
class CTD_ANON_6 (ValueType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is ValueType
    
    # Element values ({http://www.opengis.net/tml}values) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element fcnInterpol ({http://www.opengis.net/tml}fcnInterpol) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element accuracy ({http://www.opengis.net/tml}accuracy) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element mult ({http://www.opengis.net/tml}mult) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element numValues ({http://www.opengis.net/tml}numValues) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element valueDataType ({http://www.opengis.net/tml}valueDataType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element offset ({http://www.opengis.net/tml}offset) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element arrayType ({http://www.opengis.net/tml}arrayType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uidRef inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uid inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute name inherited from {http://www.opengis.net/tml}ValueType

    _ElementMap = ValueType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ValueType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_7 with content type ELEMENT_ONLY
class CTD_ANON_7 (ValueType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is ValueType
    
    # Element values ({http://www.opengis.net/tml}values) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element fcnInterpol ({http://www.opengis.net/tml}fcnInterpol) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element accuracy ({http://www.opengis.net/tml}accuracy) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element mult ({http://www.opengis.net/tml}mult) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element numValues ({http://www.opengis.net/tml}numValues) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element valueDataType ({http://www.opengis.net/tml}valueDataType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element offset ({http://www.opengis.net/tml}offset) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element arrayType ({http://www.opengis.net/tml}arrayType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uidRef inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uid inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute name inherited from {http://www.opengis.net/tml}ValueType

    _ElementMap = ValueType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ValueType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_8 with content type ELEMENT_ONLY
class CTD_ANON_8 (ValueType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is ValueType
    
    # Element values ({http://www.opengis.net/tml}values) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element fcnInterpol ({http://www.opengis.net/tml}fcnInterpol) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element accuracy ({http://www.opengis.net/tml}accuracy) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element mult ({http://www.opengis.net/tml}mult) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element numValues ({http://www.opengis.net/tml}numValues) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element valueDataType ({http://www.opengis.net/tml}valueDataType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element offset ({http://www.opengis.net/tml}offset) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element arrayType ({http://www.opengis.net/tml}arrayType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uidRef inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uid inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute name inherited from {http://www.opengis.net/tml}ValueType

    _ElementMap = ValueType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ValueType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_9 with content type ELEMENT_ONLY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}data uses Python identifier data
    __data = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'data'), 'data', '__httpwww_opengis_nettml_CTD_ANON_9_httpwww_opengis_nettmldata', True)

    
    data = property(__data.value, __data.set, None, u'this element carries the date to or from transducer systems.  The data element will carry a single instance or a continuous stream of a condition or set of synchronous conditions time tag to the precise instant of creation.   There is no XML markup of data within the data tag.  A system description will describe the decoding and understanding of the data within the data tag.')

    
    # Element {http://www.opengis.net/tml}system uses Python identifier system
    __system = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'system'), 'system', '__httpwww_opengis_nettml_CTD_ANON_9_httpwww_opengis_nettmlsystem', True)

    
    system = property(__system.value, __system.set, None, u'An empty system tag (with id) in a data stream indicates that the system is no longer available in the stream, or if system was not previously part of the parent system it will be added to the parent system.')

    
    # Element {http://www.opengis.net/tml}extSysRelations uses Python identifier extSysRelations
    __extSysRelations = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'extSysRelations'), 'extSysRelations', '__httpwww_opengis_nettml_CTD_ANON_9_httpwww_opengis_nettmlextSysRelations', True)

    
    extSysRelations = property(__extSysRelations.value, __extSysRelations.set, None, u'for relating external subject to external  subject or transducer data to external subject.  An external subject (object) is external to the system.')

    
    # Element {http://www.opengis.net/tml}process uses Python identifier process
    __process = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'process'), 'process', '__httpwww_opengis_nettml_CTD_ANON_9_httpwww_opengis_nettmlprocess', True)

    
    process = property(__process.value, __process.set, None, u'A transducer can be a stand alone object or part of a system. Describes derivation of output dataUnits relative to input dataUnits or constants.  An empty process tag in a data stream indicates that this process is no longer a part of the system')

    
    # Element {http://www.opengis.net/tml}subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'subject'), 'subject', '__httpwww_opengis_nettml_CTD_ANON_9_httpwww_opengis_nettmlsubject', True)

    
    subject = property(__subject.value, __subject.set, None, u'This is the subject (object, thing) that relates to the phenomenon (property) that is affected or detected by the transducer. The relation between a subject and transducer data or subject and subject is described in the relationship element. An empty subject tag in a data stream indicates that this object is no longer a part of the system')

    
    # Element {http://www.opengis.net/tml}transducer uses Python identifier transducer
    __transducer = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'transducer'), 'transducer', '__httpwww_opengis_nettml_CTD_ANON_9_httpwww_opengis_nettmltransducer', True)

    
    transducer = property(__transducer.value, __transducer.set, None, u'A transducer can be a stand alone object or part of a system.  An empty transducer tag in a data stream indicates that this transducer is no longer a part of the system')

    
    # Attribute {urn:us:gov:ic:ism:v2}derivedFrom uses Python identifier derivedFrom
    __derivedFrom = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivedFrom'), 'derivedFrom', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2derivedFrom', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_13)
    
    derivedFrom = property(__derivedFrom.value, __derivedFrom.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A citation of the authoritative source or reference to multiple sources of the classification markings used in a classified resource.\n        \n        It is manifested only in the 'Derived From' line of a document's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}SCIcontrols uses Python identifier SCIcontrols
    __SCIcontrols = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SCIcontrols'), 'SCIcontrols', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2SCIcontrols', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_6)
    
    SCIcontrols = property(__SCIcontrols.value, __SCIcontrols.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying sensitive compartmented information control system(s).\n        \n        It is manifested in portion marks and security banners.                 \n                    \n                    For the "SI-ECI-XXX" permissible value, "XXX" is a placeholder for ECI program designator alphabetic trigraphs, which are classified and are therefore not included here. Additional classified and unpublished SCI control system abbreviations are not included here.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        SCI Control System Markings - Authorized Portion Markings\n      ')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_9_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute {urn:us:gov:ic:ism:v2}SARIdentifier uses Python identifier SARIdentifier
    __SARIdentifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SARIdentifier'), 'SARIdentifier', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2SARIdentifier', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_5)
    
    SARIdentifier = property(__SARIdentifier.value, __SARIdentifier.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the defense or intelligence programs for which special access is required. \n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Special Access Program Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassDate uses Python identifier declassDate
    __declassDate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassDate'), 'declassDate', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2declassDate', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_)
    
    declassDate = property(__declassDate.value, __declassDate.set, None, u"\n         This attribute is used primarily at the resource level.\n         \n         A specific year, month, and day upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n         \n         It is manifested in the 'Declassify On' line of a resource's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}disseminationControls uses Python identifier disseminationControls
    __disseminationControls = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'disseminationControls'), 'disseminationControls', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2disseminationControls', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_9)
    
    disseminationControls = property(__disseminationControls.value, __disseminationControls.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the expansion or limitation on the distribution of information.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n         Dissemination Control Markings - Authorized Portion Markings\n        ')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_9_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute {urn:us:gov:ic:ism:v2}ownerProducer uses Python identifier ownerProducer
    __ownerProducer = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'ownerProducer'), 'ownerProducer', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2ownerProducer', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_8)
    
    ownerProducer = property(__ownerProducer.value, __ownerProducer.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the national government or international organization that have purview over the classification marking of an information resource or portion therein.  This element is always used in conjunction with the Classification element.  Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint). \n        \n        Within protected internal organizational spaces this element may include one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        Specifically, under these specific circumstances, when data are moved to the shared spaces, the non-disclosable owner(s) and/or producer(s) listed in this data element\u2019s value should be removed and replaced with "FGI".\n        \n        The attribute value may be manifested in portion marks or security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraphs Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassManualReview uses Python identifier declassManualReview
    __declassManualReview = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassManualReview'), 'declassManualReview', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2declassManualReview', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_2)
    
    declassManualReview = property(__declassManualReview.value, __declassManualReview.set, None, u'\n        This attribute is used primarily at the resource level.\n        \n        A single indicator of a requirement for manual review prior to declassification, over and above the usual programmatic determinations.\n        \n        The ability to indicate manual review was rescinded as of 1 February 2008 with complete removal from automated systems required by 31 March 2009 at which time this element will be deprecated.\n \n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}releasableTo uses Python identifier releasableTo
    __releasableTo = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'releasableTo'), 'releasableTo', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2releasableTo', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_15)
    
    releasableTo = property(__releasableTo.value, __releasableTo.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the country or countries and/or international organization(s) to which classified information may be released based on the determination of an originator in accordance with established foreign disclosure procedures.  This element is used in conjunction with the Dissemination Controls element.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassEvent uses Python identifier declassEvent
    __declassEvent = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassEvent'), 'declassEvent', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2declassEvent', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_3)
    
    declassEvent = property(__declassEvent.value, __declassEvent.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A description of an event upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}declassException uses Python identifier declassException
    __declassException = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassException'), 'declassException', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2declassException', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_14)
    
    declassException = property(__declassException.value, __declassException.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A single indicator describing an exemption to the nominal 25-year point for automatic declassification.  This element is used in conjunction with the Declassification Date or Declassification Event.\n        \n        It is manifested in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n        \n        This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Exemption from 25-Year Automatic Declassification Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}derivativelyClassifiedBy uses Python identifier derivativelyClassifiedBy
    __derivativelyClassifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivativelyClassifiedBy'), 'derivativelyClassifiedBy', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2derivativelyClassifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON)
    
    derivativelyClassifiedBy = property(__derivativelyClassifiedBy.value, __derivativelyClassifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        \n        The identity, by name or personal identifier, of the derivative classification authority.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}nonICmarkings uses Python identifier nonICmarkings
    __nonICmarkings = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'nonICmarkings'), 'nonICmarkings', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2nonICmarkings', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_12)
    
    nonICmarkings = property(__nonICmarkings.value, __nonICmarkings.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators of the expansion or limitation on the distribution of an information resource or portion within the domain of information originating from non-intelligence components.\n        \n        It is manifested in portion marks and security banners.\n        \n        LAW ENFORCEMENT SENSITIVE (LES) is not an authorized IC classification and control marking in the CAPCO Register. However, CAPCO has published interim marking guidance concerning the incorporation of LES information into IC products. "LES" has been included as a permissible value for attribute "nonICmarkings" in IC ISM in order to facilitate compliance with the CAPCO interim marking guidance in XML-based products.\n\n        PERMISSIBLE VALUES\n        1) The value "LES" is permited as described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Non-IC Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceProtected uses Python identifier FGIsourceProtected
    __FGIsourceProtected = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceProtected'), 'FGIsourceProtected', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2FGIsourceProtected', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_16)
    
    FGIsourceProtected = property(__FGIsourceProtected.value, __FGIsourceProtected.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        This attribute has unique specific rules concerning its usage. \n        \n        A single indicator that information qualifies as foreign government information for which the source(s) of the information must be concealed.\n        \n        Within protected internal organizational spaces this element may be used to maintain a record of the one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        An indication that information qualifies as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the information is disseminated in shared spaces\n        \n        This data element has a dual purpose. Within shared spaces, the data element serves only to indicate the presence of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information is concealed, in which case, this data element\u2019s value will always be "FGI". The data element may also be employed in this manner within protected internal organizational spaces. However, within protected internal organizational spaces this data element may alternatively be used to maintain a formal record of the foreign country or countries and/or registered international organization(s) that are the non-disclosable owner(s) and/or producer(s) of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the resource is disseminated to shared spaces. If the data element is employed in this manner, then additional measures must be taken prior to dissemination of the resource to shared spaces so that any indications of the non-disclosable owner(s) and/or producer(s) of information within the resource are eliminated.\n\n        In all cases, the corresponding portion marking or banner marking should be compliant with CAPCO guidelines for FGI when the source must be concealed. In other words, even if the data element is being employed within protected internal organizational spaces to maintain a formal record of the non-disclosable owner(s) and/or producer(s) within an XML resource, if the resource is rendered for display within the protected internal organizational spaces in any format by a stylesheet or as a result of any other transformation process, then the non-disclosable owner(s) and/or producer(s) should not be included in the corresponding portion marking or banner marking.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute version uses Python identifier version
    __version = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'version'), 'version', '__httpwww_opengis_nettml_CTD_ANON_9_version', pyxb.binding.datatypes.string, fixed=True, unicode_default=u'1.0', required=True)
    
    version = property(__version.value, __version.set, None, u'fixed version 1.0')

    
    # Attribute {urn:us:gov:ic:ism:v2}classification uses Python identifier classification
    __classification = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classification'), 'classification', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2classification', pyxb.bundles.opengis.ic_ism_2_1.ClassificationType)
    
    classification = property(__classification.value, __classification.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        A single indicator of the highest level of classification applicable to an information resource or portion within the domain of classified national security information.  The Classification element is always used in conjunction with the Owner Producer element. Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint).\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set: \n\n        US Classification Markings - Authorized Portion Markings\n        NATO Classification Markings - Authorized Portion Markings\n\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceOpen uses Python identifier FGIsourceOpen
    __FGIsourceOpen = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceOpen'), 'FGIsourceOpen', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2FGIsourceOpen', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_11)
    
    FGIsourceOpen = property(__FGIsourceOpen.value, __FGIsourceOpen.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        One or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information is not concealed.\n        \n        The attribute can indicate that the source of information of foreign origin is unknown.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "UNKNOWN" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}typeOfExemptedSource uses Python identifier typeOfExemptedSource
    __typeOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'typeOfExemptedSource'), 'typeOfExemptedSource', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2typeOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_4)
    
    typeOfExemptedSource = property(__typeOfExemptedSource.value, __typeOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A declassification marking of a source document that causes the current, derivative document to be exempted from automatic declassification.  This element is always used in conjunction with the Date Of Exempted Source element.\n        \n       It is manifested only in the 'Declassify On' line of a document's classification/declassification block.\n       \n       This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Source Document Declassification Instruction Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}classificationReason uses Python identifier classificationReason
    __classificationReason = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classificationReason'), 'classificationReason', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2classificationReason', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_7)
    
    classificationReason = property(__classificationReason.value, __classificationReason.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        One or more reason indicators or explanatory text describing the basis for an original classification decision.\n        \n        It is manifested only in the 'Reason' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_9_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute {urn:us:gov:ic:ism:v2}classifiedBy uses Python identifier classifiedBy
    __classifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classifiedBy'), 'classifiedBy', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2classifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_17)
    
    classifiedBy = property(__classifiedBy.value, __classifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        The identity, by name or personal identifier, and position title of the original classification authority for a resource.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}dateOfExemptedSource uses Python identifier dateOfExemptedSource
    __dateOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'dateOfExemptedSource'), 'dateOfExemptedSource', '__httpwww_opengis_nettml_CTD_ANON_9_urnusgovicismv2dateOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_10)
    
    dateOfExemptedSource = property(__dateOfExemptedSource.value, __dateOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A specific year, month, and day of publication or release of a source document, or the most recent source document, that was itself marked with a declassification constraint.  This element is always used in conjunction with the Type Of Exempted Source element.  \n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s Classification/Declassification block.\n      ")


    _ElementMap = {
        __data.name() : __data,
        __system.name() : __system,
        __extSysRelations.name() : __extSysRelations,
        __process.name() : __process,
        __subject.name() : __subject,
        __transducer.name() : __transducer
    }
    _AttributeMap = {
        __derivedFrom.name() : __derivedFrom,
        __SCIcontrols.name() : __SCIcontrols,
        __uid.name() : __uid,
        __SARIdentifier.name() : __SARIdentifier,
        __declassDate.name() : __declassDate,
        __disseminationControls.name() : __disseminationControls,
        __name.name() : __name,
        __ownerProducer.name() : __ownerProducer,
        __declassManualReview.name() : __declassManualReview,
        __releasableTo.name() : __releasableTo,
        __declassEvent.name() : __declassEvent,
        __declassException.name() : __declassException,
        __derivativelyClassifiedBy.name() : __derivativelyClassifiedBy,
        __nonICmarkings.name() : __nonICmarkings,
        __FGIsourceProtected.name() : __FGIsourceProtected,
        __version.name() : __version,
        __classification.name() : __classification,
        __FGIsourceOpen.name() : __FGIsourceOpen,
        __typeOfExemptedSource.name() : __typeOfExemptedSource,
        __classificationReason.name() : __classificationReason,
        __uidRef.name() : __uidRef,
        __classifiedBy.name() : __classifiedBy,
        __dateOfExemptedSource.name() : __dateOfExemptedSource
    }



# Complex type CTD_ANON_10 with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}subSampleCfIndexPts uses Python identifier subSampleCfIndexPts
    __subSampleCfIndexPts = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'subSampleCfIndexPts'), 'subSampleCfIndexPts', '__httpwww_opengis_nettml_CTD_ANON_10_httpwww_opengis_nettmlsubSampleCfIndexPts', False)

    
    subSampleCfIndexPts = property(__subSampleCfIndexPts.value, __subSampleCfIndexPts.set, None, u'use same rules as points under value')

    
    # Element {http://www.opengis.net/tml}cfStructComp uses Python identifier cfStructComp
    __cfStructComp = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'cfStructComp'), 'cfStructComp', '__httpwww_opengis_nettml_CTD_ANON_10_httpwww_opengis_nettmlcfStructComp', False)

    
    cfStructComp = property(__cfStructComp.value, __cfStructComp.set, None, u'Allowed values: column, row, plane.  default is column.  One cfSubSampling element for each cfStructComp required.')

    
    # Element {http://www.opengis.net/tml}numOfSubSampleIndexPoints uses Python identifier numOfSubSampleIndexPoints
    __numOfSubSampleIndexPoints = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numOfSubSampleIndexPoints'), 'numOfSubSampleIndexPoints', '__httpwww_opengis_nettml_CTD_ANON_10_httpwww_opengis_nettmlnumOfSubSampleIndexPoints', False)

    
    numOfSubSampleIndexPoints = property(__numOfSubSampleIndexPoints.value, __numOfSubSampleIndexPoints.set, None, u'Allowed values: positive integers from 1 to the number of columns, rows, or planes in the data structure.  This number indicates the number of samples in the cfSubSampleIndexPts.')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_10_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_10_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_10_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __subSampleCfIndexPts.name() : __subSampleCfIndexPts,
        __cfStructComp.name() : __cfStructComp,
        __numOfSubSampleIndexPoints.name() : __numOfSubSampleIndexPoints
    }
    _AttributeMap = {
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    }



# Complex type CTD_ANON_11 with content type ELEMENT_ONLY
class CTD_ANON_11 (ValueType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is ValueType
    
    # Element values ({http://www.opengis.net/tml}values) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element fcnInterpol ({http://www.opengis.net/tml}fcnInterpol) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element accuracy ({http://www.opengis.net/tml}accuracy) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element mult ({http://www.opengis.net/tml}mult) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element numValues ({http://www.opengis.net/tml}numValues) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element valueDataType ({http://www.opengis.net/tml}valueDataType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element offset ({http://www.opengis.net/tml}offset) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element arrayType ({http://www.opengis.net/tml}arrayType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uidRef inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uid inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute name inherited from {http://www.opengis.net/tml}ValueType

    _ElementMap = ValueType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = ValueType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_12 with content type ELEMENT_ONLY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}clusterProperties uses Python identifier clusterProperties
    __clusterProperties = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'clusterProperties'), 'clusterProperties', '__httpwww_opengis_nettml_CTD_ANON_12_httpwww_opengis_nettmlclusterProperties', False)

    
    clusterProperties = property(__clusterProperties.value, __clusterProperties.set, None, None)

    
    # Element {http://www.opengis.net/tml}binHeaderEncode uses Python identifier binHeaderEncode
    __binHeaderEncode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'binHeaderEncode'), 'binHeaderEncode', '__httpwww_opengis_nettml_CTD_ANON_12_httpwww_opengis_nettmlbinHeaderEncode', False)

    
    binHeaderEncode = property(__binHeaderEncode.value, __binHeaderEncode.set, None, u'If cluster type is binary this field describes the encoding of the header attributes. binary files will contain only the contents of the attributes and not the attribute tag.  The binary header will not contain the left carrot and the letters "data" at the beginning of the header either, nor the right carrot at the end of the header.')

    
    # Element {http://www.opengis.net/tml}dataUnitEncoding uses Python identifier dataUnitEncoding
    __dataUnitEncoding = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUnitEncoding'), 'dataUnitEncoding', '__httpwww_opengis_nettml_CTD_ANON_12_httpwww_opengis_nettmldataUnitEncoding', True)

    
    dataUnitEncoding = property(__dataUnitEncoding.value, __dataUnitEncoding.set, None, u'This unit describes the encoding of the dataUnit identified in the dataUnitUidRef child element.  Some clusters which represent only an event from a source or a trigger are empty and may not contain any dataUnits.')

    
    # Element {http://www.opengis.net/tml}transSeq uses Python identifier transSeq
    __transSeq = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'transSeq'), 'transSeq', '__httpwww_opengis_nettml_CTD_ANON_12_httpwww_opengis_nettmltransSeq', True)

    
    transSeq = property(__transSeq.value, __transSeq.set, None, u'This is the order in which data is sent in the cluster or CF (whichever is larger) relative to the logical data structure.  The order of structure components are listed from lowest freq to highest frequency order.   If transport sequence is blank then the sequence is the same as the logical order (sequence) for that structure component.')

    
    # Element {http://www.opengis.net/tml}idMapping uses Python identifier idMapping
    __idMapping = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'idMapping'), 'idMapping', '__httpwww_opengis_nettml_CTD_ANON_12_httpwww_opengis_nettmlidMapping', False)

    
    idMapping = property(__idMapping.value, __idMapping.set, None, None)

    
    # Element {http://www.opengis.net/tml}description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'description'), 'description', '__httpwww_opengis_nettml_CTD_ANON_12_httpwww_opengis_nettmldescription', False)

    
    description = property(__description.value, __description.set, None, u'description of the data cluster')

    
    # Element {http://www.opengis.net/tml}timeTag uses Python identifier timeTag
    __timeTag = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'timeTag'), 'timeTag', '__httpwww_opengis_nettml_CTD_ANON_12_httpwww_opengis_nettmltimeTag', False)

    
    timeTag = property(__timeTag.value, __timeTag.set, None, u'describes what time tag is used for the cluster.  Useful when parent systems normalize clocks from child components.  This element also describes how accurately the sysClk value is applied to the cluster start instant.  This is different from the accuracy of the system clock.')

    
    # Element {http://www.opengis.net/tml}numCfInCluster uses Python identifier numCfInCluster
    __numCfInCluster = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numCfInCluster'), 'numCfInCluster', '__httpwww_opengis_nettml_CTD_ANON_12_httpwww_opengis_nettmlnumCfInCluster', False)

    
    numCfInCluster = property(__numCfInCluster.value, __numCfInCluster.set, None, u'number of characteristic frames in a cluster or the number of clusters which comprise a large characteristic frame.  default = 1.  example: 2 means 2 CF per cluster, -2 means 2 clusters per CF.  Allowed values: signed integer.  zero not allowed.')

    
    # Attribute {urn:us:gov:ic:ism:v2}SCIcontrols uses Python identifier SCIcontrols
    __SCIcontrols = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SCIcontrols'), 'SCIcontrols', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2SCIcontrols', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_6)
    
    SCIcontrols = property(__SCIcontrols.value, __SCIcontrols.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying sensitive compartmented information control system(s).\n        \n        It is manifested in portion marks and security banners.                 \n                    \n                    For the "SI-ECI-XXX" permissible value, "XXX" is a placeholder for ECI program designator alphabetic trigraphs, which are classified and are therefore not included here. Additional classified and unpublished SCI control system abbreviations are not included here.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        SCI Control System Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceOpen uses Python identifier FGIsourceOpen
    __FGIsourceOpen = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceOpen'), 'FGIsourceOpen', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2FGIsourceOpen', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_11)
    
    FGIsourceOpen = property(__FGIsourceOpen.value, __FGIsourceOpen.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        One or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information is not concealed.\n        \n        The attribute can indicate that the source of information of foreign origin is unknown.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "UNKNOWN" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_12_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute {urn:us:gov:ic:ism:v2}SARIdentifier uses Python identifier SARIdentifier
    __SARIdentifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SARIdentifier'), 'SARIdentifier', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2SARIdentifier', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_5)
    
    SARIdentifier = property(__SARIdentifier.value, __SARIdentifier.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the defense or intelligence programs for which special access is required. \n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Special Access Program Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassDate uses Python identifier declassDate
    __declassDate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassDate'), 'declassDate', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2declassDate', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_)
    
    declassDate = property(__declassDate.value, __declassDate.set, None, u"\n         This attribute is used primarily at the resource level.\n         \n         A specific year, month, and day upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n         \n         It is manifested in the 'Declassify On' line of a resource's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}disseminationControls uses Python identifier disseminationControls
    __disseminationControls = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'disseminationControls'), 'disseminationControls', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2disseminationControls', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_9)
    
    disseminationControls = property(__disseminationControls.value, __disseminationControls.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the expansion or limitation on the distribution of information.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n         Dissemination Control Markings - Authorized Portion Markings\n        ')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_12_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassManualReview uses Python identifier declassManualReview
    __declassManualReview = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassManualReview'), 'declassManualReview', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2declassManualReview', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_2)
    
    declassManualReview = property(__declassManualReview.value, __declassManualReview.set, None, u'\n        This attribute is used primarily at the resource level.\n        \n        A single indicator of a requirement for manual review prior to declassification, over and above the usual programmatic determinations.\n        \n        The ability to indicate manual review was rescinded as of 1 February 2008 with complete removal from automated systems required by 31 March 2009 at which time this element will be deprecated.\n \n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassEvent uses Python identifier declassEvent
    __declassEvent = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassEvent'), 'declassEvent', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2declassEvent', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_3)
    
    declassEvent = property(__declassEvent.value, __declassEvent.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A description of an event upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}ownerProducer uses Python identifier ownerProducer
    __ownerProducer = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'ownerProducer'), 'ownerProducer', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2ownerProducer', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_8)
    
    ownerProducer = property(__ownerProducer.value, __ownerProducer.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the national government or international organization that have purview over the classification marking of an information resource or portion therein.  This element is always used in conjunction with the Classification element.  Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint). \n        \n        Within protected internal organizational spaces this element may include one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        Specifically, under these specific circumstances, when data are moved to the shared spaces, the non-disclosable owner(s) and/or producer(s) listed in this data element\u2019s value should be removed and replaced with "FGI".\n        \n        The attribute value may be manifested in portion marks or security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraphs Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassException uses Python identifier declassException
    __declassException = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassException'), 'declassException', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2declassException', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_14)
    
    declassException = property(__declassException.value, __declassException.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A single indicator describing an exemption to the nominal 25-year point for automatic declassification.  This element is used in conjunction with the Declassification Date or Declassification Event.\n        \n        It is manifested in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n        \n        This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Exemption from 25-Year Automatic Declassification Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceProtected uses Python identifier FGIsourceProtected
    __FGIsourceProtected = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceProtected'), 'FGIsourceProtected', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2FGIsourceProtected', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_16)
    
    FGIsourceProtected = property(__FGIsourceProtected.value, __FGIsourceProtected.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        This attribute has unique specific rules concerning its usage. \n        \n        A single indicator that information qualifies as foreign government information for which the source(s) of the information must be concealed.\n        \n        Within protected internal organizational spaces this element may be used to maintain a record of the one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        An indication that information qualifies as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the information is disseminated in shared spaces\n        \n        This data element has a dual purpose. Within shared spaces, the data element serves only to indicate the presence of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information is concealed, in which case, this data element\u2019s value will always be "FGI". The data element may also be employed in this manner within protected internal organizational spaces. However, within protected internal organizational spaces this data element may alternatively be used to maintain a formal record of the foreign country or countries and/or registered international organization(s) that are the non-disclosable owner(s) and/or producer(s) of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the resource is disseminated to shared spaces. If the data element is employed in this manner, then additional measures must be taken prior to dissemination of the resource to shared spaces so that any indications of the non-disclosable owner(s) and/or producer(s) of information within the resource are eliminated.\n\n        In all cases, the corresponding portion marking or banner marking should be compliant with CAPCO guidelines for FGI when the source must be concealed. In other words, even if the data element is being employed within protected internal organizational spaces to maintain a formal record of the non-disclosable owner(s) and/or producer(s) within an XML resource, if the resource is rendered for display within the protected internal organizational spaces in any format by a stylesheet or as a result of any other transformation process, then the non-disclosable owner(s) and/or producer(s) should not be included in the corresponding portion marking or banner marking.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}nonICmarkings uses Python identifier nonICmarkings
    __nonICmarkings = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'nonICmarkings'), 'nonICmarkings', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2nonICmarkings', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_12)
    
    nonICmarkings = property(__nonICmarkings.value, __nonICmarkings.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators of the expansion or limitation on the distribution of an information resource or portion within the domain of information originating from non-intelligence components.\n        \n        It is manifested in portion marks and security banners.\n        \n        LAW ENFORCEMENT SENSITIVE (LES) is not an authorized IC classification and control marking in the CAPCO Register. However, CAPCO has published interim marking guidance concerning the incorporation of LES information into IC products. "LES" has been included as a permissible value for attribute "nonICmarkings" in IC ISM in order to facilitate compliance with the CAPCO interim marking guidance in XML-based products.\n\n        PERMISSIBLE VALUES\n        1) The value "LES" is permited as described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Non-IC Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}releasableTo uses Python identifier releasableTo
    __releasableTo = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'releasableTo'), 'releasableTo', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2releasableTo', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_15)
    
    releasableTo = property(__releasableTo.value, __releasableTo.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the country or countries and/or international organization(s) to which classified information may be released based on the determination of an originator in accordance with established foreign disclosure procedures.  This element is used in conjunction with the Dissemination Controls element.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}classification uses Python identifier classification
    __classification = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classification'), 'classification', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2classification', pyxb.bundles.opengis.ic_ism_2_1.ClassificationType)
    
    classification = property(__classification.value, __classification.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        A single indicator of the highest level of classification applicable to an information resource or portion within the domain of classified national security information.  The Classification element is always used in conjunction with the Owner Producer element. Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint).\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set: \n\n        US Classification Markings - Authorized Portion Markings\n        NATO Classification Markings - Authorized Portion Markings\n\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}derivativelyClassifiedBy uses Python identifier derivativelyClassifiedBy
    __derivativelyClassifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivativelyClassifiedBy'), 'derivativelyClassifiedBy', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2derivativelyClassifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON)
    
    derivativelyClassifiedBy = property(__derivativelyClassifiedBy.value, __derivativelyClassifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        \n        The identity, by name or personal identifier, of the derivative classification authority.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}typeOfExemptedSource uses Python identifier typeOfExemptedSource
    __typeOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'typeOfExemptedSource'), 'typeOfExemptedSource', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2typeOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_4)
    
    typeOfExemptedSource = property(__typeOfExemptedSource.value, __typeOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A declassification marking of a source document that causes the current, derivative document to be exempted from automatic declassification.  This element is always used in conjunction with the Date Of Exempted Source element.\n        \n       It is manifested only in the 'Declassify On' line of a document's classification/declassification block.\n       \n       This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Source Document Declassification Instruction Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}classificationReason uses Python identifier classificationReason
    __classificationReason = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classificationReason'), 'classificationReason', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2classificationReason', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_7)
    
    classificationReason = property(__classificationReason.value, __classificationReason.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        One or more reason indicators or explanatory text describing the basis for an original classification decision.\n        \n        It is manifested only in the 'Reason' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_12_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute {urn:us:gov:ic:ism:v2}classifiedBy uses Python identifier classifiedBy
    __classifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classifiedBy'), 'classifiedBy', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2classifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_17)
    
    classifiedBy = property(__classifiedBy.value, __classifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        The identity, by name or personal identifier, and position title of the original classification authority for a resource.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}dateOfExemptedSource uses Python identifier dateOfExemptedSource
    __dateOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'dateOfExemptedSource'), 'dateOfExemptedSource', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2dateOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_10)
    
    dateOfExemptedSource = property(__dateOfExemptedSource.value, __dateOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A specific year, month, and day of publication or release of a source document, or the most recent source document, that was itself marked with a declassification constraint.  This element is always used in conjunction with the Type Of Exempted Source element.  \n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}derivedFrom uses Python identifier derivedFrom
    __derivedFrom = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivedFrom'), 'derivedFrom', '__httpwww_opengis_nettml_CTD_ANON_12_urnusgovicismv2derivedFrom', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_13)
    
    derivedFrom = property(__derivedFrom.value, __derivedFrom.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A citation of the authoritative source or reference to multiple sources of the classification markings used in a classified resource.\n        \n        It is manifested only in the 'Derived From' line of a document's classification/declassification block.\n      ")


    _ElementMap = {
        __clusterProperties.name() : __clusterProperties,
        __binHeaderEncode.name() : __binHeaderEncode,
        __dataUnitEncoding.name() : __dataUnitEncoding,
        __transSeq.name() : __transSeq,
        __idMapping.name() : __idMapping,
        __description.name() : __description,
        __timeTag.name() : __timeTag,
        __numCfInCluster.name() : __numCfInCluster
    }
    _AttributeMap = {
        __SCIcontrols.name() : __SCIcontrols,
        __FGIsourceOpen.name() : __FGIsourceOpen,
        __uid.name() : __uid,
        __SARIdentifier.name() : __SARIdentifier,
        __declassDate.name() : __declassDate,
        __disseminationControls.name() : __disseminationControls,
        __name.name() : __name,
        __declassManualReview.name() : __declassManualReview,
        __declassEvent.name() : __declassEvent,
        __ownerProducer.name() : __ownerProducer,
        __declassException.name() : __declassException,
        __FGIsourceProtected.name() : __FGIsourceProtected,
        __nonICmarkings.name() : __nonICmarkings,
        __releasableTo.name() : __releasableTo,
        __classification.name() : __classification,
        __derivativelyClassifiedBy.name() : __derivativelyClassifiedBy,
        __typeOfExemptedSource.name() : __typeOfExemptedSource,
        __classificationReason.name() : __classificationReason,
        __uidRef.name() : __uidRef,
        __classifiedBy.name() : __classifiedBy,
        __dateOfExemptedSource.name() : __dateOfExemptedSource,
        __derivedFrom.name() : __derivedFrom
    }



# Complex type CTD_ANON_13 with content type ELEMENT_ONLY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}validatedBy uses Python identifier validatedBy
    __validatedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'validatedBy'), 'validatedBy', '__httpwww_opengis_nettml_CTD_ANON_13_httpwww_opengis_nettmlvalidatedBy', True)

    
    validatedBy = property(__validatedBy.value, __validatedBy.set, None, None)

    
    # Element {http://www.opengis.net/tml}calibratedBy uses Python identifier calibratedBy
    __calibratedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'calibratedBy'), 'calibratedBy', '__httpwww_opengis_nettml_CTD_ANON_13_httpwww_opengis_nettmlcalibratedBy', True)

    
    calibratedBy = property(__calibratedBy.value, __calibratedBy.set, None, None)


    _ElementMap = {
        __validatedBy.name() : __validatedBy,
        __calibratedBy.name() : __calibratedBy
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
    
    # Element {http://www.opengis.net/tml}ambiguitySpace uses Python identifier ambiguitySpace
    __ambiguitySpace = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ambiguitySpace'), 'ambiguitySpace', '__httpwww_opengis_nettml_CTD_ANON_14_httpwww_opengis_nettmlambiguitySpace', True)

    
    ambiguitySpace = property(__ambiguitySpace.value, __ambiguitySpace.set, None, u'Multiple AS are combined as spatial intersections.  e.g. one for columns and one for rows.  Typically every cell within a multiple cell CF will share the same shape but have unique positions.')

    
    # Element {http://www.opengis.net/tml}cfSubSampling uses Python identifier cfSubSampling
    __cfSubSampling = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling'), 'cfSubSampling', '__httpwww_opengis_nettml_CTD_ANON_14_httpwww_opengis_nettmlcfSubSampling', True)

    
    cfSubSampling = property(__cfSubSampling.value, __cfSubSampling.set, None, u'the CFSubSampling can be used for chipping part of a large dataArry out and for reducing the number of points within an array for which to associate modeling parameters.  there is one sub sampling element set of points for each component structure (col, row, plane).    index numbers of col, row or plane position within the CFs are listed for which corresponding modeling points will be associated.  sample points are separated by commas, ranges are indicated by ... between numbers which indicates a continuous interval for a single sample. interpolation between samples uses logical structure.  ')

    
    # Element {http://www.opengis.net/tml}dataUidRef uses Python identifier dataUidRef
    __dataUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), 'dataUidRef', '__httpwww_opengis_nettml_CTD_ANON_14_httpwww_opengis_nettmldataUidRef', False)

    
    dataUidRef = property(__dataUidRef.value, __dataUidRef.set, None, u'corresponding UID of dataUnit, dataSet,  or data Array.  If data array then all subordinate data structures share same model (row, col, or plane), if dataSet then all data units share same model (cf), if dataUnit then only that units model is described (cf). ')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_14_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_14_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_14_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')


    _ElementMap = {
        __ambiguitySpace.name() : __ambiguitySpace,
        __cfSubSampling.name() : __cfSubSampling,
        __dataUidRef.name() : __dataUidRef
    }
    _AttributeMap = {
        __name.name() : __name,
        __uidRef.name() : __uidRef,
        __uid.name() : __uid
    }



# Complex type CTD_ANON_15 with content type ELEMENT_ONLY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}position uses Python identifier position
    __position = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'position'), 'position', '__httpwww_opengis_nettml_CTD_ANON_15_httpwww_opengis_nettmlposition', True)

    
    position = property(__position.value, __position.set, None, u'location and attitude of ambiguity shape')

    
    # Element {http://www.opengis.net/tml}shape uses Python identifier shape
    __shape = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'shape'), 'shape', '__httpwww_opengis_nettml_CTD_ANON_15_httpwww_opengis_nettmlshape', True)

    
    shape = property(__shape.value, __shape.set, None, u'This is the shape of the AS for the power profile indicated.  May also have multiple shapes to define multiple lobes of energy fields.  Multiple shapes within an AS are combined as a spatial unions.   The position elements defines the position of each shape.')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_15_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_15_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_15_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')


    _ElementMap = {
        __position.name() : __position,
        __shape.name() : __shape
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __name.name() : __name,
        __uid.name() : __uid
    }



# Complex type IdentificationType with content type ELEMENT_ONLY
class IdentificationType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'IdentificationType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}calibration uses Python identifier calibration
    __calibration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'calibration'), 'calibration', '__httpwww_opengis_nettml_IdentificationType_httpwww_opengis_nettmlcalibration', False)

    
    calibration = property(__calibration.value, __calibration.set, None, u'Do the TML descriptions accurately reflect actual performance specifications')

    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_IdentificationType_httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'uid of registry object')

    
    # Element {http://www.opengis.net/tml}characterization uses Python identifier characterization
    __characterization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'characterization'), 'characterization', '__httpwww_opengis_nettml_IdentificationType_httpwww_opengis_nettmlcharacterization', False)

    
    characterization = property(__characterization.value, __characterization.set, None, u'Do the tml descriptions comply with the TML Compliance Rules')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_IdentificationType_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {http://www.opengis.net/tml}description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'description'), 'description', '__httpwww_opengis_nettml_IdentificationType_httpwww_opengis_nettmldescription', False)

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {http://www.opengis.net/tml}complexity uses Python identifier complexity
    __complexity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'complexity'), 'complexity', '__httpwww_opengis_nettml_IdentificationType_httpwww_opengis_nettmlcomplexity', False)

    
    complexity = property(__complexity.value, __complexity.set, None, u'indication of the complexity of handling this data. Allowed Values: 1A - 1F, 2A -2F, 3A - 3F, 4A - 4F, 5A - 5F.  default 1A')


    _ElementMap = {
        __calibration.name() : __calibration,
        __uid.name() : __uid,
        __characterization.name() : __characterization,
        __name.name() : __name,
        __description.name() : __description,
        __complexity.name() : __complexity
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'IdentificationType', IdentificationType)


# Complex type CTD_ANON_16 with content type ELEMENT_ONLY
class CTD_ANON_16 (IdentificationType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is IdentificationType
    
    # Element calibration ({http://www.opengis.net/tml}calibration) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element uid ({http://www.opengis.net/tml}uid) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element characterization ({http://www.opengis.net/tml}characterization) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element {http://www.opengis.net/tml}serialNumber uses Python identifier serialNumber
    __serialNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'serialNumber'), 'serialNumber', '__httpwww_opengis_nettml_CTD_ANON_16_httpwww_opengis_nettmlserialNumber', False)

    
    serialNumber = property(__serialNumber.value, __serialNumber.set, None, None)

    
    # Element name ({http://www.opengis.net/tml}name) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element {http://www.opengis.net/tml}modelNumber uses Python identifier modelNumber
    __modelNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'modelNumber'), 'modelNumber', '__httpwww_opengis_nettml_CTD_ANON_16_httpwww_opengis_nettmlmodelNumber', False)

    
    modelNumber = property(__modelNumber.value, __modelNumber.set, None, None)

    
    # Element {http://www.opengis.net/tml}owner uses Python identifier owner
    __owner = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'owner'), 'owner', '__httpwww_opengis_nettml_CTD_ANON_16_httpwww_opengis_nettmlowner', False)

    
    owner = property(__owner.value, __owner.set, None, None)

    
    # Element description ({http://www.opengis.net/tml}description) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element {http://www.opengis.net/tml}manufacture uses Python identifier manufacture
    __manufacture = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'manufacture'), 'manufacture', '__httpwww_opengis_nettml_CTD_ANON_16_httpwww_opengis_nettmlmanufacture', False)

    
    manufacture = property(__manufacture.value, __manufacture.set, None, None)

    
    # Element complexity ({http://www.opengis.net/tml}complexity) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element {http://www.opengis.net/tml}operator uses Python identifier operator
    __operator = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'operator'), 'operator', '__httpwww_opengis_nettml_CTD_ANON_16_httpwww_opengis_nettmloperator', False)

    
    operator = property(__operator.value, __operator.set, None, None)


    _ElementMap = IdentificationType._ElementMap.copy()
    _ElementMap.update({
        __serialNumber.name() : __serialNumber,
        __modelNumber.name() : __modelNumber,
        __owner.name() : __owner,
        __manufacture.name() : __manufacture,
        __operator.name() : __operator
    })
    _AttributeMap = IdentificationType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_17 with content type SIMPLE
class CTD_ANON_17 (BindType):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is BindType
    
    # Attribute bindUid inherited from {http://www.opengis.net/tml}BindType
    
    # Attribute bindUidRef inherited from {http://www.opengis.net/tml}BindType

    _ElementMap = BindType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BindType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_18 with content type ELEMENT_ONLY
class CTD_ANON_18 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_18_httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'uid of dataSet. ')

    
    # Element {http://www.opengis.net/tml}numObjInSet uses Python identifier numObjInSet
    __numObjInSet = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numObjInSet'), 'numObjInSet', '__httpwww_opengis_nettml_CTD_ANON_18_httpwww_opengis_nettmlnumObjInSet', False)

    
    numObjInSet = property(__numObjInSet.value, __numObjInSet.set, None, u'number of subordinate sets and/or arrays.  default 1')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_18_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, u'name of dataSet')

    
    # Element {http://www.opengis.net/tml}dataUnit uses Python identifier dataUnit
    __dataUnit = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUnit'), 'dataUnit', '__httpwww_opengis_nettml_CTD_ANON_18_httpwww_opengis_nettmldataUnit', True)

    
    dataUnit = property(__dataUnit.value, __dataUnit.set, None, u'an elemental unit of data.  one description for each unit')

    
    # Element {http://www.opengis.net/tml}variableName uses Python identifier variableName
    __variableName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'variableName'), 'variableName', '__httpwww_opengis_nettml_CTD_ANON_18_httpwww_opengis_nettmlvariableName', False)

    
    variableName = property(__variableName.value, __variableName.set, None, u'Name of mathematical term used in the transformation equations.  Index of component is the order in the sequence in the LDS structure.')

    
    # Element {http://www.opengis.net/tml}dataArray uses Python identifier dataArray
    __dataArray = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataArray'), 'dataArray', '__httpwww_opengis_nettml_CTD_ANON_18_httpwww_opengis_nettmldataArray', True)

    
    dataArray = property(__dataArray.value, __dataArray.set, None, None)

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_18_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name_
    __name_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name_', '__httpwww_opengis_nettml_CTD_ANON_18_name', pyxb.binding.datatypes.string)
    
    name_ = property(__name_.value, __name_.set, None, u'short descriptive name of element')

    
    # Attribute uid uses Python identifier uid_
    __uid_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid_', '__httpwww_opengis_nettml_CTD_ANON_18_uid', pyxb.binding.datatypes.anyURI)
    
    uid_ = property(__uid_.value, __uid_.set, None, u'unique ID for this element')


    _ElementMap = {
        __uid.name() : __uid,
        __numObjInSet.name() : __numObjInSet,
        __name.name() : __name,
        __dataUnit.name() : __dataUnit,
        __variableName.name() : __variableName,
        __dataArray.name() : __dataArray
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __name_.name() : __name_,
        __uid_.name() : __uid_
    }



# Complex type CTD_ANON_19 with content type ELEMENT_ONLY
class CTD_ANON_19 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}process uses Python identifier process
    __process = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'process'), 'process', '__httpwww_opengis_nettml_CTD_ANON_19_httpwww_opengis_nettmlprocess', True)

    
    process = property(__process.value, __process.set, None, u'A transducer can be a stand alone object or part of a system. Describes derivation of output dataUnits relative to input dataUnits or constants.  An empty process tag in a data stream indicates that this process is no longer a part of the system')


    _ElementMap = {
        __process.name() : __process
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_20 with content type ELEMENT_ONLY
class CTD_ANON_20 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}type uses Python identifier type
    __type = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'type'), 'type', '__httpwww_opengis_nettml_CTD_ANON_20_httpwww_opengis_nettmltype', False)

    
    type = property(__type.value, __type.set, None, u'Allowed values: relative, absolute, systematic, random. default is absolute')

    
    # Element {http://www.opengis.net/tml}factor uses Python identifier factor
    __factor = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'factor'), 'factor', '__httpwww_opengis_nettml_CTD_ANON_20_httpwww_opengis_nettmlfactor', False)

    
    factor = property(__factor.value, __factor.set, None, u'allowed values: 1sigma, 2sigma, 3sigma, 4sigma, 5sigma, 6sigma, percent, range. RMS, RSS, Default is 1sigma')

    
    # Element {http://www.opengis.net/tml}errorDistribution uses Python identifier errorDistribution
    __errorDistribution = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'errorDistribution'), 'errorDistribution', '__httpwww_opengis_nettml_CTD_ANON_20_httpwww_opengis_nettmlerrorDistribution', False)

    
    errorDistribution = property(__errorDistribution.value, __errorDistribution.set, None, u'Allowed Values: gaussian, chi, chi2, possion,  gamma.  default is gaussian')

    
    # Element {http://www.opengis.net/tml}accyValues uses Python identifier accyValues
    __accyValues = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'accyValues'), 'accyValues', '__httpwww_opengis_nettml_CTD_ANON_20_httpwww_opengis_nettmlaccyValues', False)

    
    accyValues = property(__accyValues.value, __accyValues.set, None, u'A single accyValue relates to whole range of parent coordinates (e.g. data or prop). If accyValue is variable over the parent coordinates then there shall be a one-to-one correspondence between the accyValues and the parent coordinates.  use mult and offset to describe variances over CF')


    _ElementMap = {
        __type.name() : __type,
        __factor.name() : __factor,
        __errorDistribution.name() : __errorDistribution,
        __accyValues.name() : __accyValues
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_21 with content type ELEMENT_ONLY
class CTD_ANON_21 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}sysClkUidRef uses Python identifier sysClkUidRef
    __sysClkUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'sysClkUidRef'), 'sysClkUidRef', '__httpwww_opengis_nettml_CTD_ANON_21_httpwww_opengis_nettmlsysClkUidRef', False)

    
    sysClkUidRef = property(__sysClkUidRef.value, __sysClkUidRef.set, None, u'if clk is used in the start tag and multiple clocks are used in a system.  Default is the first parent system clock')

    
    # Element {http://www.opengis.net/tml}accuracy uses Python identifier accuracy
    __accuracy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'accuracy'), 'accuracy', '__httpwww_opengis_nettml_CTD_ANON_21_httpwww_opengis_nettmlaccuracy', False)

    
    accuracy = property(__accuracy.value, __accuracy.set, None, u'accuracy is in terms of the data value before adjustment by mult and offset.   if a characteristic frame (i.e. number of values) of values of accuracy, then each value corresponds to the corresponding Characteristic Frame  position or interval')


    _ElementMap = {
        __sysClkUidRef.name() : __sysClkUidRef,
        __accuracy.name() : __accuracy
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_22 with content type ELEMENT_ONLY
class CTD_ANON_22 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}relationDescription uses Python identifier relationDescription
    __relationDescription = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'relationDescription'), 'relationDescription', '__httpwww_opengis_nettml_CTD_ANON_22_httpwww_opengis_nettmlrelationDescription', False)

    
    relationDescription = property(__relationDescription.value, __relationDescription.set, None, u'description of the  relation')

    
    # Element {http://www.opengis.net/tml}object uses Python identifier object
    __object = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'object'), 'object', '__httpwww_opengis_nettml_CTD_ANON_22_httpwww_opengis_nettmlobject', True)

    
    object = property(__object.value, __object.set, None, u'many objects can be related to a many objects.  probabilities can be assigned to each relation')

    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_22_httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'uid of the relationship')

    
    # Element {http://www.opengis.net/tml}confidence uses Python identifier confidence
    __confidence = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'confidence'), 'confidence', '__httpwww_opengis_nettml_CTD_ANON_22_httpwww_opengis_nettmlconfidence', False)

    
    confidence = property(__confidence.value, __confidence.set, None, u'confidence of relationship (-1 to 1). -1 is 100% no confidence. confidence values match same sequence as logical data structure (if multiple values in data structure)')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassEvent uses Python identifier declassEvent
    __declassEvent = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassEvent'), 'declassEvent', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2declassEvent', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_3)
    
    declassEvent = property(__declassEvent.value, __declassEvent.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A description of an event upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}declassManualReview uses Python identifier declassManualReview
    __declassManualReview = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassManualReview'), 'declassManualReview', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2declassManualReview', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_2)
    
    declassManualReview = property(__declassManualReview.value, __declassManualReview.set, None, u'\n        This attribute is used primarily at the resource level.\n        \n        A single indicator of a requirement for manual review prior to declassification, over and above the usual programmatic determinations.\n        \n        The ability to indicate manual review was rescinded as of 1 February 2008 with complete removal from automated systems required by 31 March 2009 at which time this element will be deprecated.\n \n      ')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_22_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute {urn:us:gov:ic:ism:v2}ownerProducer uses Python identifier ownerProducer
    __ownerProducer = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'ownerProducer'), 'ownerProducer', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2ownerProducer', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_8)
    
    ownerProducer = property(__ownerProducer.value, __ownerProducer.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the national government or international organization that have purview over the classification marking of an information resource or portion therein.  This element is always used in conjunction with the Classification element.  Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint). \n        \n        Within protected internal organizational spaces this element may include one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        Specifically, under these specific circumstances, when data are moved to the shared spaces, the non-disclosable owner(s) and/or producer(s) listed in this data element\u2019s value should be removed and replaced with "FGI".\n        \n        The attribute value may be manifested in portion marks or security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraphs Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}classificationReason uses Python identifier classificationReason
    __classificationReason = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classificationReason'), 'classificationReason', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2classificationReason', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_7)
    
    classificationReason = property(__classificationReason.value, __classificationReason.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        One or more reason indicators or explanatory text describing the basis for an original classification decision.\n        \n        It is manifested only in the 'Reason' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceProtected uses Python identifier FGIsourceProtected
    __FGIsourceProtected = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceProtected'), 'FGIsourceProtected', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2FGIsourceProtected', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_16)
    
    FGIsourceProtected = property(__FGIsourceProtected.value, __FGIsourceProtected.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        This attribute has unique specific rules concerning its usage. \n        \n        A single indicator that information qualifies as foreign government information for which the source(s) of the information must be concealed.\n        \n        Within protected internal organizational spaces this element may be used to maintain a record of the one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        An indication that information qualifies as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the information is disseminated in shared spaces\n        \n        This data element has a dual purpose. Within shared spaces, the data element serves only to indicate the presence of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information is concealed, in which case, this data element\u2019s value will always be "FGI". The data element may also be employed in this manner within protected internal organizational spaces. However, within protected internal organizational spaces this data element may alternatively be used to maintain a formal record of the foreign country or countries and/or registered international organization(s) that are the non-disclosable owner(s) and/or producer(s) of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the resource is disseminated to shared spaces. If the data element is employed in this manner, then additional measures must be taken prior to dissemination of the resource to shared spaces so that any indications of the non-disclosable owner(s) and/or producer(s) of information within the resource are eliminated.\n\n        In all cases, the corresponding portion marking or banner marking should be compliant with CAPCO guidelines for FGI when the source must be concealed. In other words, even if the data element is being employed within protected internal organizational spaces to maintain a formal record of the non-disclosable owner(s) and/or producer(s) within an XML resource, if the resource is rendered for display within the protected internal organizational spaces in any format by a stylesheet or as a result of any other transformation process, then the non-disclosable owner(s) and/or producer(s) should not be included in the corresponding portion marking or banner marking.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}classification uses Python identifier classification
    __classification = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classification'), 'classification', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2classification', pyxb.bundles.opengis.ic_ism_2_1.ClassificationType)
    
    classification = property(__classification.value, __classification.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        A single indicator of the highest level of classification applicable to an information resource or portion within the domain of classified national security information.  The Classification element is always used in conjunction with the Owner Producer element. Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint).\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set: \n\n        US Classification Markings - Authorized Portion Markings\n        NATO Classification Markings - Authorized Portion Markings\n\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}releasableTo uses Python identifier releasableTo
    __releasableTo = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'releasableTo'), 'releasableTo', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2releasableTo', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_15)
    
    releasableTo = property(__releasableTo.value, __releasableTo.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the country or countries and/or international organization(s) to which classified information may be released based on the determination of an originator in accordance with established foreign disclosure procedures.  This element is used in conjunction with the Dissemination Controls element.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}typeOfExemptedSource uses Python identifier typeOfExemptedSource
    __typeOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'typeOfExemptedSource'), 'typeOfExemptedSource', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2typeOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_4)
    
    typeOfExemptedSource = property(__typeOfExemptedSource.value, __typeOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A declassification marking of a source document that causes the current, derivative document to be exempted from automatic declassification.  This element is always used in conjunction with the Date Of Exempted Source element.\n        \n       It is manifested only in the 'Declassify On' line of a document's classification/declassification block.\n       \n       This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Source Document Declassification Instruction Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}derivativelyClassifiedBy uses Python identifier derivativelyClassifiedBy
    __derivativelyClassifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivativelyClassifiedBy'), 'derivativelyClassifiedBy', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2derivativelyClassifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON)
    
    derivativelyClassifiedBy = property(__derivativelyClassifiedBy.value, __derivativelyClassifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        \n        The identity, by name or personal identifier, of the derivative classification authority.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}disseminationControls uses Python identifier disseminationControls
    __disseminationControls = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'disseminationControls'), 'disseminationControls', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2disseminationControls', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_9)
    
    disseminationControls = property(__disseminationControls.value, __disseminationControls.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the expansion or limitation on the distribution of information.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n         Dissemination Control Markings - Authorized Portion Markings\n        ')

    
    # Attribute {urn:us:gov:ic:ism:v2}nonICmarkings uses Python identifier nonICmarkings
    __nonICmarkings = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'nonICmarkings'), 'nonICmarkings', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2nonICmarkings', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_12)
    
    nonICmarkings = property(__nonICmarkings.value, __nonICmarkings.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators of the expansion or limitation on the distribution of an information resource or portion within the domain of information originating from non-intelligence components.\n        \n        It is manifested in portion marks and security banners.\n        \n        LAW ENFORCEMENT SENSITIVE (LES) is not an authorized IC classification and control marking in the CAPCO Register. However, CAPCO has published interim marking guidance concerning the incorporation of LES information into IC products. "LES" has been included as a permissible value for attribute "nonICmarkings" in IC ISM in order to facilitate compliance with the CAPCO interim marking guidance in XML-based products.\n\n        PERMISSIBLE VALUES\n        1) The value "LES" is permited as described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Non-IC Markings - Authorized Portion Markings\n      ')

    
    # Attribute uid uses Python identifier uid_
    __uid_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid_', '__httpwww_opengis_nettml_CTD_ANON_22_uid', pyxb.binding.datatypes.anyURI)
    
    uid_ = property(__uid_.value, __uid_.set, None, u'unique ID for this element')

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceOpen uses Python identifier FGIsourceOpen
    __FGIsourceOpen = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceOpen'), 'FGIsourceOpen', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2FGIsourceOpen', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_11)
    
    FGIsourceOpen = property(__FGIsourceOpen.value, __FGIsourceOpen.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        One or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information is not concealed.\n        \n        The attribute can indicate that the source of information of foreign origin is unknown.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "UNKNOWN" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}classifiedBy uses Python identifier classifiedBy
    __classifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classifiedBy'), 'classifiedBy', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2classifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_17)
    
    classifiedBy = property(__classifiedBy.value, __classifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        The identity, by name or personal identifier, and position title of the original classification authority for a resource.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}dateOfExemptedSource uses Python identifier dateOfExemptedSource
    __dateOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'dateOfExemptedSource'), 'dateOfExemptedSource', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2dateOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_10)
    
    dateOfExemptedSource = property(__dateOfExemptedSource.value, __dateOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A specific year, month, and day of publication or release of a source document, or the most recent source document, that was itself marked with a declassification constraint.  This element is always used in conjunction with the Type Of Exempted Source element.  \n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}derivedFrom uses Python identifier derivedFrom
    __derivedFrom = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivedFrom'), 'derivedFrom', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2derivedFrom', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_13)
    
    derivedFrom = property(__derivedFrom.value, __derivedFrom.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A citation of the authoritative source or reference to multiple sources of the classification markings used in a classified resource.\n        \n        It is manifested only in the 'Derived From' line of a document's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}SCIcontrols uses Python identifier SCIcontrols
    __SCIcontrols = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SCIcontrols'), 'SCIcontrols', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2SCIcontrols', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_6)
    
    SCIcontrols = property(__SCIcontrols.value, __SCIcontrols.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying sensitive compartmented information control system(s).\n        \n        It is manifested in portion marks and security banners.                 \n                    \n                    For the "SI-ECI-XXX" permissible value, "XXX" is a placeholder for ECI program designator alphabetic trigraphs, which are classified and are therefore not included here. Additional classified and unpublished SCI control system abbreviations are not included here.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        SCI Control System Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassDate uses Python identifier declassDate
    __declassDate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassDate'), 'declassDate', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2declassDate', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_)
    
    declassDate = property(__declassDate.value, __declassDate.set, None, u"\n         This attribute is used primarily at the resource level.\n         \n         A specific year, month, and day upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n         \n         It is manifested in the 'Declassify On' line of a resource's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}SARIdentifier uses Python identifier SARIdentifier
    __SARIdentifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SARIdentifier'), 'SARIdentifier', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2SARIdentifier', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_5)
    
    SARIdentifier = property(__SARIdentifier.value, __SARIdentifier.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the defense or intelligence programs for which special access is required. \n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Special Access Program Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassException uses Python identifier declassException
    __declassException = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassException'), 'declassException', '__httpwww_opengis_nettml_CTD_ANON_22_urnusgovicismv2declassException', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_14)
    
    declassException = property(__declassException.value, __declassException.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A single indicator describing an exemption to the nominal 25-year point for automatic declassification.  This element is used in conjunction with the Declassification Date or Declassification Event.\n        \n        It is manifested in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n        \n        This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Exemption from 25-Year Automatic Declassification Markings\n\n      ")

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_22_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')


    _ElementMap = {
        __relationDescription.name() : __relationDescription,
        __object.name() : __object,
        __uid.name() : __uid,
        __confidence.name() : __confidence
    }
    _AttributeMap = {
        __declassEvent.name() : __declassEvent,
        __declassManualReview.name() : __declassManualReview,
        __name.name() : __name,
        __ownerProducer.name() : __ownerProducer,
        __classificationReason.name() : __classificationReason,
        __FGIsourceProtected.name() : __FGIsourceProtected,
        __classification.name() : __classification,
        __releasableTo.name() : __releasableTo,
        __typeOfExemptedSource.name() : __typeOfExemptedSource,
        __derivativelyClassifiedBy.name() : __derivativelyClassifiedBy,
        __disseminationControls.name() : __disseminationControls,
        __nonICmarkings.name() : __nonICmarkings,
        __uid_.name() : __uid_,
        __FGIsourceOpen.name() : __FGIsourceOpen,
        __classifiedBy.name() : __classifiedBy,
        __dateOfExemptedSource.name() : __dateOfExemptedSource,
        __derivedFrom.name() : __derivedFrom,
        __SCIcontrols.name() : __SCIcontrols,
        __declassDate.name() : __declassDate,
        __SARIdentifier.name() : __SARIdentifier,
        __declassException.name() : __declassException,
        __uidRef.name() : __uidRef
    }



# Complex type CTD_ANON_23 with content type ELEMENT_ONLY
class CTD_ANON_23 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}dataUidRef uses Python identifier dataUidRef
    __dataUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), 'dataUidRef', '__httpwww_opengis_nettml_CTD_ANON_23_httpwww_opengis_nettmldataUidRef', False)

    
    dataUidRef = property(__dataUidRef.value, __dataUidRef.set, None, u'UID of the data reference.  Archived data streams will have a UID indicative of the data source, time, and clk count of the start. ')

    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_23_httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'connection or node UID of the connection signal data or property relationship')

    
    # Element {http://www.opengis.net/tml}object uses Python identifier object
    __object = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'object'), 'object', '__httpwww_opengis_nettml_CTD_ANON_23_httpwww_opengis_nettmlobject', True)

    
    object = property(__object.value, __object.set, None, u'Object can be a single transducer (dangle relation), a single dataUID, or many subjects can be related to a single data unit.  probabilities can be assigned to each relation.')

    
    # Element {http://www.opengis.net/tml}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_nettml_CTD_ANON_23_httpwww_opengis_nettmlvalue', False)

    
    value_ = property(__value.value, __value.set, None, None)

    
    # Element {http://www.opengis.net/tml}relationDescription uses Python identifier relationDescription
    __relationDescription = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'relationDescription'), 'relationDescription', '__httpwww_opengis_nettml_CTD_ANON_23_httpwww_opengis_nettmlrelationDescription', False)

    
    relationDescription = property(__relationDescription.value, __relationDescription.set, None, u'description of the signal or the property relation')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_23_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceOpen uses Python identifier FGIsourceOpen
    __FGIsourceOpen = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceOpen'), 'FGIsourceOpen', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2FGIsourceOpen', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_11)
    
    FGIsourceOpen = property(__FGIsourceOpen.value, __FGIsourceOpen.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        One or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information is not concealed.\n        \n        The attribute can indicate that the source of information of foreign origin is unknown.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "UNKNOWN" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}SCIcontrols uses Python identifier SCIcontrols
    __SCIcontrols = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SCIcontrols'), 'SCIcontrols', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2SCIcontrols', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_6)
    
    SCIcontrols = property(__SCIcontrols.value, __SCIcontrols.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying sensitive compartmented information control system(s).\n        \n        It is manifested in portion marks and security banners.                 \n                    \n                    For the "SI-ECI-XXX" permissible value, "XXX" is a placeholder for ECI program designator alphabetic trigraphs, which are classified and are therefore not included here. Additional classified and unpublished SCI control system abbreviations are not included here.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        SCI Control System Markings - Authorized Portion Markings\n      ')

    
    # Attribute uid uses Python identifier uid_
    __uid_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid_', '__httpwww_opengis_nettml_CTD_ANON_23_uid', pyxb.binding.datatypes.anyURI)
    
    uid_ = property(__uid_.value, __uid_.set, None, u'unique ID for this element')

    
    # Attribute {urn:us:gov:ic:ism:v2}SARIdentifier uses Python identifier SARIdentifier
    __SARIdentifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SARIdentifier'), 'SARIdentifier', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2SARIdentifier', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_5)
    
    SARIdentifier = property(__SARIdentifier.value, __SARIdentifier.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the defense or intelligence programs for which special access is required. \n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Special Access Program Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassDate uses Python identifier declassDate
    __declassDate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassDate'), 'declassDate', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2declassDate', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_)
    
    declassDate = property(__declassDate.value, __declassDate.set, None, u"\n         This attribute is used primarily at the resource level.\n         \n         A specific year, month, and day upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n         \n         It is manifested in the 'Declassify On' line of a resource's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}disseminationControls uses Python identifier disseminationControls
    __disseminationControls = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'disseminationControls'), 'disseminationControls', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2disseminationControls', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_9)
    
    disseminationControls = property(__disseminationControls.value, __disseminationControls.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the expansion or limitation on the distribution of information.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n         Dissemination Control Markings - Authorized Portion Markings\n        ')

    
    # Attribute name uses Python identifier name_
    __name_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name_', '__httpwww_opengis_nettml_CTD_ANON_23_name', pyxb.binding.datatypes.string)
    
    name_ = property(__name_.value, __name_.set, None, u'short descriptive name of element')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassManualReview uses Python identifier declassManualReview
    __declassManualReview = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassManualReview'), 'declassManualReview', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2declassManualReview', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_2)
    
    declassManualReview = property(__declassManualReview.value, __declassManualReview.set, None, u'\n        This attribute is used primarily at the resource level.\n        \n        A single indicator of a requirement for manual review prior to declassification, over and above the usual programmatic determinations.\n        \n        The ability to indicate manual review was rescinded as of 1 February 2008 with complete removal from automated systems required by 31 March 2009 at which time this element will be deprecated.\n \n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassEvent uses Python identifier declassEvent
    __declassEvent = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassEvent'), 'declassEvent', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2declassEvent', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_3)
    
    declassEvent = property(__declassEvent.value, __declassEvent.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A description of an event upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}ownerProducer uses Python identifier ownerProducer
    __ownerProducer = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'ownerProducer'), 'ownerProducer', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2ownerProducer', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_8)
    
    ownerProducer = property(__ownerProducer.value, __ownerProducer.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the national government or international organization that have purview over the classification marking of an information resource or portion therein.  This element is always used in conjunction with the Classification element.  Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint). \n        \n        Within protected internal organizational spaces this element may include one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        Specifically, under these specific circumstances, when data are moved to the shared spaces, the non-disclosable owner(s) and/or producer(s) listed in this data element\u2019s value should be removed and replaced with "FGI".\n        \n        The attribute value may be manifested in portion marks or security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraphs Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassException uses Python identifier declassException
    __declassException = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassException'), 'declassException', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2declassException', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_14)
    
    declassException = property(__declassException.value, __declassException.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A single indicator describing an exemption to the nominal 25-year point for automatic declassification.  This element is used in conjunction with the Declassification Date or Declassification Event.\n        \n        It is manifested in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n        \n        This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Exemption from 25-Year Automatic Declassification Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceProtected uses Python identifier FGIsourceProtected
    __FGIsourceProtected = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceProtected'), 'FGIsourceProtected', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2FGIsourceProtected', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_16)
    
    FGIsourceProtected = property(__FGIsourceProtected.value, __FGIsourceProtected.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        This attribute has unique specific rules concerning its usage. \n        \n        A single indicator that information qualifies as foreign government information for which the source(s) of the information must be concealed.\n        \n        Within protected internal organizational spaces this element may be used to maintain a record of the one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        An indication that information qualifies as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the information is disseminated in shared spaces\n        \n        This data element has a dual purpose. Within shared spaces, the data element serves only to indicate the presence of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information is concealed, in which case, this data element\u2019s value will always be "FGI". The data element may also be employed in this manner within protected internal organizational spaces. However, within protected internal organizational spaces this data element may alternatively be used to maintain a formal record of the foreign country or countries and/or registered international organization(s) that are the non-disclosable owner(s) and/or producer(s) of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the resource is disseminated to shared spaces. If the data element is employed in this manner, then additional measures must be taken prior to dissemination of the resource to shared spaces so that any indications of the non-disclosable owner(s) and/or producer(s) of information within the resource are eliminated.\n\n        In all cases, the corresponding portion marking or banner marking should be compliant with CAPCO guidelines for FGI when the source must be concealed. In other words, even if the data element is being employed within protected internal organizational spaces to maintain a formal record of the non-disclosable owner(s) and/or producer(s) within an XML resource, if the resource is rendered for display within the protected internal organizational spaces in any format by a stylesheet or as a result of any other transformation process, then the non-disclosable owner(s) and/or producer(s) should not be included in the corresponding portion marking or banner marking.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}nonICmarkings uses Python identifier nonICmarkings
    __nonICmarkings = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'nonICmarkings'), 'nonICmarkings', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2nonICmarkings', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_12)
    
    nonICmarkings = property(__nonICmarkings.value, __nonICmarkings.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators of the expansion or limitation on the distribution of an information resource or portion within the domain of information originating from non-intelligence components.\n        \n        It is manifested in portion marks and security banners.\n        \n        LAW ENFORCEMENT SENSITIVE (LES) is not an authorized IC classification and control marking in the CAPCO Register. However, CAPCO has published interim marking guidance concerning the incorporation of LES information into IC products. "LES" has been included as a permissible value for attribute "nonICmarkings" in IC ISM in order to facilitate compliance with the CAPCO interim marking guidance in XML-based products.\n\n        PERMISSIBLE VALUES\n        1) The value "LES" is permited as described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Non-IC Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}releasableTo uses Python identifier releasableTo
    __releasableTo = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'releasableTo'), 'releasableTo', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2releasableTo', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_15)
    
    releasableTo = property(__releasableTo.value, __releasableTo.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the country or countries and/or international organization(s) to which classified information may be released based on the determination of an originator in accordance with established foreign disclosure procedures.  This element is used in conjunction with the Dissemination Controls element.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}classification uses Python identifier classification
    __classification = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classification'), 'classification', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2classification', pyxb.bundles.opengis.ic_ism_2_1.ClassificationType)
    
    classification = property(__classification.value, __classification.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        A single indicator of the highest level of classification applicable to an information resource or portion within the domain of classified national security information.  The Classification element is always used in conjunction with the Owner Producer element. Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint).\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set: \n\n        US Classification Markings - Authorized Portion Markings\n        NATO Classification Markings - Authorized Portion Markings\n\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}derivativelyClassifiedBy uses Python identifier derivativelyClassifiedBy
    __derivativelyClassifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivativelyClassifiedBy'), 'derivativelyClassifiedBy', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2derivativelyClassifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON)
    
    derivativelyClassifiedBy = property(__derivativelyClassifiedBy.value, __derivativelyClassifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        \n        The identity, by name or personal identifier, of the derivative classification authority.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}typeOfExemptedSource uses Python identifier typeOfExemptedSource
    __typeOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'typeOfExemptedSource'), 'typeOfExemptedSource', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2typeOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_4)
    
    typeOfExemptedSource = property(__typeOfExemptedSource.value, __typeOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A declassification marking of a source document that causes the current, derivative document to be exempted from automatic declassification.  This element is always used in conjunction with the Date Of Exempted Source element.\n        \n       It is manifested only in the 'Declassify On' line of a document's classification/declassification block.\n       \n       This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Source Document Declassification Instruction Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}classificationReason uses Python identifier classificationReason
    __classificationReason = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classificationReason'), 'classificationReason', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2classificationReason', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_7)
    
    classificationReason = property(__classificationReason.value, __classificationReason.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        One or more reason indicators or explanatory text describing the basis for an original classification decision.\n        \n        It is manifested only in the 'Reason' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_23_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute {urn:us:gov:ic:ism:v2}classifiedBy uses Python identifier classifiedBy
    __classifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classifiedBy'), 'classifiedBy', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2classifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_17)
    
    classifiedBy = property(__classifiedBy.value, __classifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        The identity, by name or personal identifier, and position title of the original classification authority for a resource.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}dateOfExemptedSource uses Python identifier dateOfExemptedSource
    __dateOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'dateOfExemptedSource'), 'dateOfExemptedSource', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2dateOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_10)
    
    dateOfExemptedSource = property(__dateOfExemptedSource.value, __dateOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A specific year, month, and day of publication or release of a source document, or the most recent source document, that was itself marked with a declassification constraint.  This element is always used in conjunction with the Type Of Exempted Source element.  \n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}derivedFrom uses Python identifier derivedFrom
    __derivedFrom = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivedFrom'), 'derivedFrom', '__httpwww_opengis_nettml_CTD_ANON_23_urnusgovicismv2derivedFrom', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_13)
    
    derivedFrom = property(__derivedFrom.value, __derivedFrom.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A citation of the authoritative source or reference to multiple sources of the classification markings used in a classified resource.\n        \n        It is manifested only in the 'Derived From' line of a document's classification/declassification block.\n      ")


    _ElementMap = {
        __dataUidRef.name() : __dataUidRef,
        __uid.name() : __uid,
        __object.name() : __object,
        __value.name() : __value,
        __relationDescription.name() : __relationDescription,
        __name.name() : __name
    }
    _AttributeMap = {
        __FGIsourceOpen.name() : __FGIsourceOpen,
        __SCIcontrols.name() : __SCIcontrols,
        __uid_.name() : __uid_,
        __SARIdentifier.name() : __SARIdentifier,
        __declassDate.name() : __declassDate,
        __disseminationControls.name() : __disseminationControls,
        __name_.name() : __name_,
        __declassManualReview.name() : __declassManualReview,
        __declassEvent.name() : __declassEvent,
        __ownerProducer.name() : __ownerProducer,
        __declassException.name() : __declassException,
        __FGIsourceProtected.name() : __FGIsourceProtected,
        __nonICmarkings.name() : __nonICmarkings,
        __releasableTo.name() : __releasableTo,
        __classification.name() : __classification,
        __derivativelyClassifiedBy.name() : __derivativelyClassifiedBy,
        __typeOfExemptedSource.name() : __typeOfExemptedSource,
        __classificationReason.name() : __classificationReason,
        __uidRef.name() : __uidRef,
        __classifiedBy.name() : __classifiedBy,
        __dateOfExemptedSource.name() : __dateOfExemptedSource,
        __derivedFrom.name() : __derivedFrom
    }



# Complex type CTD_ANON_24 with content type ELEMENT_ONLY
class CTD_ANON_24 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}dataUnitFieldSize uses Python identifier dataUnitFieldSize
    __dataUnitFieldSize = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUnitFieldSize'), 'dataUnitFieldSize', '__httpwww_opengis_nettml_CTD_ANON_24_httpwww_opengis_nettmldataUnitFieldSize', False)

    
    dataUnitFieldSize = property(__dataUnitFieldSize.value, __dataUnitFieldSize.set, None, None)

    
    # Element {http://www.opengis.net/tml}numBase uses Python identifier numBase
    __numBase = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numBase'), 'numBase', '__httpwww_opengis_nettml_CTD_ANON_24_httpwww_opengis_nettmlnumBase', False)

    
    numBase = property(__numBase.value, __numBase.set, None, u'when numbers are encoded as text the number base must be understood.  Allowed values: 2, 8, 10, 16, 32, 64, 128.  default 10')

    
    # Element {http://www.opengis.net/tml}dataUnitUidRef uses Python identifier dataUnitUidRef
    __dataUnitUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUnitUidRef'), 'dataUnitUidRef', '__httpwww_opengis_nettml_CTD_ANON_24_httpwww_opengis_nettmldataUnitUidRef', False)

    
    dataUnitUidRef = property(__dataUnitUidRef.value, __dataUnitUidRef.set, None, u'UID of the dataUnit from the logical structure.  ')

    
    # Element {http://www.opengis.net/tml}endian uses Python identifier endian
    __endian = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'endian'), 'endian', '__httpwww_opengis_nettml_CTD_ANON_24_httpwww_opengis_nettmlendian', False)

    
    endian = property(__endian.value, __endian.set, None, u'Allowed values: big, little.  default little')

    
    # Element {http://www.opengis.net/tml}handleAsType uses Python identifier handleAsType
    __handleAsType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'handleAsType'), 'handleAsType', '__httpwww_opengis_nettml_CTD_ANON_24_httpwww_opengis_nettmlhandleAsType', False)

    
    handleAsType = property(__handleAsType.value, __handleAsType.set, None, u'how should the text or number be handled in the client application.  Allowed values: anuURI, boolean, byte, double, float, short, string, int, integer, long, nonNegativeInteger, nonPositiveInteger, positiveInteger,  unsignedByte, unsignedInt, unsignedShort, unsignedLong.')

    
    # Element {http://www.opengis.net/tml}dataType uses Python identifier dataType
    __dataType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataType'), 'dataType', '__httpwww_opengis_nettml_CTD_ANON_24_httpwww_opengis_nettmldataType', False)

    
    dataType = property(__dataType.value, __dataType.set, None, u'Allowed values: text, number, binBlob.  Default is text. ')

    
    # Element {http://www.opengis.net/tml}encode uses Python identifier encode
    __encode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'encode'), 'encode', '__httpwww_opengis_nettml_CTD_ANON_24_httpwww_opengis_nettmlencode', False)

    
    encode = property(__encode.value, __encode.set, None, u'Allowed values: ucs16, utf8, signInt, unsignInt, real, complex, bcd.  default utf8.  When clusterType is not binary only utf8 is allowed in cluster.  All types are allowed when clusterType is binary. Complex values are exchanged as two phenomenon (mag and phase or real and imaginary components) or as a single complex number.')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_24_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_24_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_24_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __dataUnitFieldSize.name() : __dataUnitFieldSize,
        __numBase.name() : __numBase,
        __dataUnitUidRef.name() : __dataUnitUidRef,
        __endian.name() : __endian,
        __handleAsType.name() : __handleAsType,
        __dataType.name() : __dataType,
        __encode.name() : __encode
    }
    _AttributeMap = {
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    }



# Complex type DataArrayType with content type ELEMENT_ONLY
class DataArrayType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'DataArrayType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}dataArray uses Python identifier dataArray
    __dataArray = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataArray'), 'dataArray', '__httpwww_opengis_nettml_DataArrayType_httpwww_opengis_nettmldataArray', False)

    
    dataArray = property(__dataArray.value, __dataArray.set, None, u'a dataArray contains a homogeneous collection of one or more dataSets or dataArrays')

    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_DataArrayType_httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'uid of dataArray')

    
    # Element {http://www.opengis.net/tml}dataSet uses Python identifier dataSet
    __dataSet = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataSet'), 'dataSet', '__httpwww_opengis_nettml_DataArrayType_httpwww_opengis_nettmldataSet', False)

    
    dataSet = property(__dataSet.value, __dataSet.set, None, u'data Sets contain a heterogeneous collection of one or more dataUnits')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_DataArrayType_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, u'name of dataArray')

    
    # Element {http://www.opengis.net/tml}numObjInArray uses Python identifier numObjInArray
    __numObjInArray = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numObjInArray'), 'numObjInArray', '__httpwww_opengis_nettml_DataArrayType_httpwww_opengis_nettmlnumObjInArray', False)

    
    numObjInArray = property(__numObjInArray.value, __numObjInArray.set, None, u'The chosen object (dataSet or dataArray) repeats this many time.   default 1')

    
    # Element {http://www.opengis.net/tml}arrayOf uses Python identifier arrayOf
    __arrayOf = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'arrayOf'), 'arrayOf', '__httpwww_opengis_nettml_DataArrayType_httpwww_opengis_nettmlarrayOf', False)

    
    arrayOf = property(__arrayOf.value, __arrayOf.set, None, u'Allowed values: columns, rows, planes default is columns')

    
    # Element {http://www.opengis.net/tml}variableName uses Python identifier variableName
    __variableName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'variableName'), 'variableName', '__httpwww_opengis_nettml_DataArrayType_httpwww_opengis_nettmlvariableName', False)

    
    variableName = property(__variableName.value, __variableName.set, None, u'Name of mathematical term used in the transformation equations.  Index of component is same as order sequence in the lds.')

    
    # Attribute uid uses Python identifier uid_
    __uid_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid_', '__httpwww_opengis_nettml_DataArrayType_uid', pyxb.binding.datatypes.anyURI)
    
    uid_ = property(__uid_.value, __uid_.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_DataArrayType_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name_
    __name_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name_', '__httpwww_opengis_nettml_DataArrayType_name', pyxb.binding.datatypes.string)
    
    name_ = property(__name_.value, __name_.set, None, u'short descriptive name of element')


    _ElementMap = {
        __dataArray.name() : __dataArray,
        __uid.name() : __uid,
        __dataSet.name() : __dataSet,
        __name.name() : __name,
        __numObjInArray.name() : __numObjInArray,
        __arrayOf.name() : __arrayOf,
        __variableName.name() : __variableName
    }
    _AttributeMap = {
        __uid_.name() : __uid_,
        __uidRef.name() : __uidRef,
        __name_.name() : __name_
    }
Namespace.addCategoryObject('typeBinding', u'DataArrayType', DataArrayType)


# Complex type CTD_ANON_25 with content type ELEMENT_ONLY
class CTD_ANON_25 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}endTextDelimiter uses Python identifier endTextDelimiter
    __endTextDelimiter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'endTextDelimiter'), 'endTextDelimiter', '__httpwww_opengis_nettml_CTD_ANON_25_httpwww_opengis_nettmlendTextDelimiter', False)

    
    endTextDelimiter = property(__endTextDelimiter.value, __endTextDelimiter.set, None, u'default delimiter is none. Empty tag means none.')

    
    # Element {http://www.opengis.net/tml}justification uses Python identifier justification
    __justification = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'justification'), 'justification', '__httpwww_opengis_nettml_CTD_ANON_25_httpwww_opengis_nettmljustification', False)

    
    justification = property(__justification.value, __justification.set, None, u'if numSigBits is less than numBits this element indicates how sigbit are justified.  Allowed values: left, right. Default: right')

    
    # Element {http://www.opengis.net/tml}beginTextDelimiter uses Python identifier beginTextDelimiter
    __beginTextDelimiter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'beginTextDelimiter'), 'beginTextDelimiter', '__httpwww_opengis_nettml_CTD_ANON_25_httpwww_opengis_nettmlbeginTextDelimiter', False)

    
    beginTextDelimiter = property(__beginTextDelimiter.value, __beginTextDelimiter.set, None, u'delimiter used to separate variable size dataUnits in cluster when encode is text (utf or ucs). default delimiter is none.  Empty tag means none.')

    
    # Element {http://www.opengis.net/tml}numBits uses Python identifier numBits
    __numBits = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numBits'), 'numBits', '__httpwww_opengis_nettml_CTD_ANON_25_httpwww_opengis_nettmlnumBits', False)

    
    numBits = property(__numBits.value, __numBits.set, None, u'default  8')

    
    # Element {http://www.opengis.net/tml}numSigBits uses Python identifier numSigBits
    __numSigBits = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numSigBits'), 'numSigBits', '__httpwww_opengis_nettml_CTD_ANON_25_httpwww_opengis_nettmlnumSigBits', False)

    
    numSigBits = property(__numSigBits.value, __numSigBits.set, None, u'default')


    _ElementMap = {
        __endTextDelimiter.name() : __endTextDelimiter,
        __justification.name() : __justification,
        __beginTextDelimiter.name() : __beginTextDelimiter,
        __numBits.name() : __numBits,
        __numSigBits.name() : __numSigBits
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_26 with content type SIMPLE
class CTD_ANON_26 (BindType):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is BindType
    
    # Attribute bindUidRef inherited from {http://www.opengis.net/tml}BindType
    
    # Attribute bindUid inherited from {http://www.opengis.net/tml}BindType
    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_26_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_26_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_26_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = BindType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BindType._AttributeMap.copy()
    _AttributeMap.update({
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    })



# Complex type CTD_ANON_27 with content type ELEMENT_ONLY
class CTD_ANON_27 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}logicalDataStructure uses Python identifier logicalDataStructure
    __logicalDataStructure = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'logicalDataStructure'), 'logicalDataStructure', '__httpwww_opengis_nettml_CTD_ANON_27_httpwww_opengis_nettmllogicalDataStructure', True)

    
    logicalDataStructure = property(__logicalDataStructure.value, __logicalDataStructure.set, None, u'the logical structure of data (i.e. of the characteristic frame).  This is not necessarily the structure or order that data is communicated in.  The transmission order is defined in the cluster description.  The transmission order is defined relative to the logical order.')

    
    # Element {http://www.opengis.net/tml}temporalModel uses Python identifier temporalModel
    __temporalModel = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'temporalModel'), 'temporalModel', '__httpwww_opengis_nettml_CTD_ANON_27_httpwww_opengis_nettmltemporalModel', False)

    
    temporalModel = property(__temporalModel.value, __temporalModel.set, None, None)

    
    # Element {http://www.opengis.net/tml}other uses Python identifier other
    __other = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'other'), 'other', '__httpwww_opengis_nettml_CTD_ANON_27_httpwww_opengis_nettmlother', False)

    
    other = property(__other.value, __other.set, None, None)

    
    # Element {http://www.opengis.net/tml}responseModels uses Python identifier responseModels
    __responseModels = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'responseModels'), 'responseModels', '__httpwww_opengis_nettml_CTD_ANON_27_httpwww_opengis_nettmlresponseModels', False)

    
    responseModels = property(__responseModels.value, __responseModels.set, None, None)

    
    # Element {http://www.opengis.net/tml}outputIdent uses Python identifier outputIdent
    __outputIdent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'outputIdent'), 'outputIdent', '__httpwww_opengis_nettml_CTD_ANON_27_httpwww_opengis_nettmloutputIdent', False)

    
    outputIdent = property(__outputIdent.value, __outputIdent.set, None, None)

    
    # Element {http://www.opengis.net/tml}spatialModel uses Python identifier spatialModel
    __spatialModel = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'spatialModel'), 'spatialModel', '__httpwww_opengis_nettml_CTD_ANON_27_httpwww_opengis_nettmlspatialModel', True)

    
    spatialModel = property(__spatialModel.value, __spatialModel.set, None, None)

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_27_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_27_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_27_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __logicalDataStructure.name() : __logicalDataStructure,
        __temporalModel.name() : __temporalModel,
        __other.name() : __other,
        __responseModels.name() : __responseModels,
        __outputIdent.name() : __outputIdent,
        __spatialModel.name() : __spatialModel
    }
    _AttributeMap = {
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    }



# Complex type CTD_ANON_28 with content type SIMPLE
class CTD_ANON_28 (BindType):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is BindType
    
    # Attribute bindUid inherited from {http://www.opengis.net/tml}BindType
    
    # Attribute bindUidRef inherited from {http://www.opengis.net/tml}BindType

    _ElementMap = BindType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BindType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type SystemType with content type ELEMENT_ONLY
class SystemType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SystemType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}identification uses Python identifier identification
    __identification = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'identification'), 'identification', '__httpwww_opengis_nettml_SystemType_httpwww_opengis_nettmlidentification', False)

    
    identification = property(__identification.value, __identification.set, None, u'Identification of the system')

    
    # Element {http://www.opengis.net/tml}transducers uses Python identifier transducers
    __transducers = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'transducers'), 'transducers', '__httpwww_opengis_nettml_SystemType_httpwww_opengis_nettmltransducers', False)

    
    transducers = property(__transducers.value, __transducers.set, None, None)

    
    # Element {http://www.opengis.net/tml}subjects uses Python identifier subjects
    __subjects = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'subjects'), 'subjects', '__httpwww_opengis_nettml_SystemType_httpwww_opengis_nettmlsubjects', False)

    
    subjects = property(__subjects.value, __subjects.set, None, None)

    
    # Element {http://www.opengis.net/tml}systems uses Python identifier systems
    __systems = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'systems'), 'systems', '__httpwww_opengis_nettml_SystemType_httpwww_opengis_nettmlsystems', False)

    
    systems = property(__systems.value, __systems.set, None, None)

    
    # Element {http://www.opengis.net/tml}otherProperties uses Python identifier otherProperties
    __otherProperties = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'otherProperties'), 'otherProperties', '__httpwww_opengis_nettml_SystemType_httpwww_opengis_nettmlotherProperties', False)

    
    otherProperties = property(__otherProperties.value, __otherProperties.set, None, None)

    
    # Element {http://www.opengis.net/tml}sysClk uses Python identifier sysClk
    __sysClk = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'sysClk'), 'sysClk', '__httpwww_opengis_nettml_SystemType_httpwww_opengis_nettmlsysClk', False)

    
    sysClk = property(__sysClk.value, __sysClk.set, None, u'clock counter.  ')

    
    # Element {http://www.opengis.net/tml}clusterDescriptions uses Python identifier clusterDescriptions
    __clusterDescriptions = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'clusterDescriptions'), 'clusterDescriptions', '__httpwww_opengis_nettml_SystemType_httpwww_opengis_nettmlclusterDescriptions', False)

    
    clusterDescriptions = property(__clusterDescriptions.value, __clusterDescriptions.set, None, None)

    
    # Element {http://www.opengis.net/tml}processes uses Python identifier processes
    __processes = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'processes'), 'processes', '__httpwww_opengis_nettml_SystemType_httpwww_opengis_nettmlprocesses', False)

    
    processes = property(__processes.value, __processes.set, None, None)

    
    # Element {http://www.opengis.net/tml}relations uses Python identifier relations
    __relations = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'relations'), 'relations', '__httpwww_opengis_nettml_SystemType_httpwww_opengis_nettmlrelations', False)

    
    relations = property(__relations.value, __relations.set, None, u'relationships of objects within the system.  characterized at the time of the system characterization.')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_SystemType_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute {urn:us:gov:ic:ism:v2}classifiedBy uses Python identifier classifiedBy
    __classifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classifiedBy'), 'classifiedBy', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2classifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_17)
    
    classifiedBy = property(__classifiedBy.value, __classifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        The identity, by name or personal identifier, and position title of the original classification authority for a resource.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}dateOfExemptedSource uses Python identifier dateOfExemptedSource
    __dateOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'dateOfExemptedSource'), 'dateOfExemptedSource', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2dateOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_10)
    
    dateOfExemptedSource = property(__dateOfExemptedSource.value, __dateOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A specific year, month, and day of publication or release of a source document, or the most recent source document, that was itself marked with a declassification constraint.  This element is always used in conjunction with the Type Of Exempted Source element.  \n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceOpen uses Python identifier FGIsourceOpen
    __FGIsourceOpen = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceOpen'), 'FGIsourceOpen', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2FGIsourceOpen', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_11)
    
    FGIsourceOpen = property(__FGIsourceOpen.value, __FGIsourceOpen.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        One or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information is not concealed.\n        \n        The attribute can indicate that the source of information of foreign origin is unknown.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "UNKNOWN" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}derivedFrom uses Python identifier derivedFrom
    __derivedFrom = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivedFrom'), 'derivedFrom', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2derivedFrom', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_13)
    
    derivedFrom = property(__derivedFrom.value, __derivedFrom.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A citation of the authoritative source or reference to multiple sources of the classification markings used in a classified resource.\n        \n        It is manifested only in the 'Derived From' line of a document's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}SCIcontrols uses Python identifier SCIcontrols
    __SCIcontrols = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SCIcontrols'), 'SCIcontrols', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2SCIcontrols', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_6)
    
    SCIcontrols = property(__SCIcontrols.value, __SCIcontrols.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying sensitive compartmented information control system(s).\n        \n        It is manifested in portion marks and security banners.                 \n                    \n                    For the "SI-ECI-XXX" permissible value, "XXX" is a placeholder for ECI program designator alphabetic trigraphs, which are classified and are therefore not included here. Additional classified and unpublished SCI control system abbreviations are not included here.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        SCI Control System Markings - Authorized Portion Markings\n      ')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_SystemType_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute {urn:us:gov:ic:ism:v2}SARIdentifier uses Python identifier SARIdentifier
    __SARIdentifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SARIdentifier'), 'SARIdentifier', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2SARIdentifier', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_5)
    
    SARIdentifier = property(__SARIdentifier.value, __SARIdentifier.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the defense or intelligence programs for which special access is required. \n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Special Access Program Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassDate uses Python identifier declassDate
    __declassDate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassDate'), 'declassDate', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2declassDate', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_)
    
    declassDate = property(__declassDate.value, __declassDate.set, None, u"\n         This attribute is used primarily at the resource level.\n         \n         A specific year, month, and day upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n         \n         It is manifested in the 'Declassify On' line of a resource's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}disseminationControls uses Python identifier disseminationControls
    __disseminationControls = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'disseminationControls'), 'disseminationControls', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2disseminationControls', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_9)
    
    disseminationControls = property(__disseminationControls.value, __disseminationControls.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the expansion or limitation on the distribution of information.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n         Dissemination Control Markings - Authorized Portion Markings\n        ')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_SystemType_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassManualReview uses Python identifier declassManualReview
    __declassManualReview = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassManualReview'), 'declassManualReview', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2declassManualReview', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_2)
    
    declassManualReview = property(__declassManualReview.value, __declassManualReview.set, None, u'\n        This attribute is used primarily at the resource level.\n        \n        A single indicator of a requirement for manual review prior to declassification, over and above the usual programmatic determinations.\n        \n        The ability to indicate manual review was rescinded as of 1 February 2008 with complete removal from automated systems required by 31 March 2009 at which time this element will be deprecated.\n \n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassEvent uses Python identifier declassEvent
    __declassEvent = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassEvent'), 'declassEvent', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2declassEvent', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_3)
    
    declassEvent = property(__declassEvent.value, __declassEvent.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A description of an event upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}ownerProducer uses Python identifier ownerProducer
    __ownerProducer = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'ownerProducer'), 'ownerProducer', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2ownerProducer', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_8)
    
    ownerProducer = property(__ownerProducer.value, __ownerProducer.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the national government or international organization that have purview over the classification marking of an information resource or portion therein.  This element is always used in conjunction with the Classification element.  Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint). \n        \n        Within protected internal organizational spaces this element may include one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        Specifically, under these specific circumstances, when data are moved to the shared spaces, the non-disclosable owner(s) and/or producer(s) listed in this data element\u2019s value should be removed and replaced with "FGI".\n        \n        The attribute value may be manifested in portion marks or security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraphs Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassException uses Python identifier declassException
    __declassException = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassException'), 'declassException', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2declassException', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_14)
    
    declassException = property(__declassException.value, __declassException.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A single indicator describing an exemption to the nominal 25-year point for automatic declassification.  This element is used in conjunction with the Declassification Date or Declassification Event.\n        \n        It is manifested in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n        \n        This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Exemption from 25-Year Automatic Declassification Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceProtected uses Python identifier FGIsourceProtected
    __FGIsourceProtected = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceProtected'), 'FGIsourceProtected', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2FGIsourceProtected', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_16)
    
    FGIsourceProtected = property(__FGIsourceProtected.value, __FGIsourceProtected.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        This attribute has unique specific rules concerning its usage. \n        \n        A single indicator that information qualifies as foreign government information for which the source(s) of the information must be concealed.\n        \n        Within protected internal organizational spaces this element may be used to maintain a record of the one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        An indication that information qualifies as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the information is disseminated in shared spaces\n        \n        This data element has a dual purpose. Within shared spaces, the data element serves only to indicate the presence of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information is concealed, in which case, this data element\u2019s value will always be "FGI". The data element may also be employed in this manner within protected internal organizational spaces. However, within protected internal organizational spaces this data element may alternatively be used to maintain a formal record of the foreign country or countries and/or registered international organization(s) that are the non-disclosable owner(s) and/or producer(s) of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the resource is disseminated to shared spaces. If the data element is employed in this manner, then additional measures must be taken prior to dissemination of the resource to shared spaces so that any indications of the non-disclosable owner(s) and/or producer(s) of information within the resource are eliminated.\n\n        In all cases, the corresponding portion marking or banner marking should be compliant with CAPCO guidelines for FGI when the source must be concealed. In other words, even if the data element is being employed within protected internal organizational spaces to maintain a formal record of the non-disclosable owner(s) and/or producer(s) within an XML resource, if the resource is rendered for display within the protected internal organizational spaces in any format by a stylesheet or as a result of any other transformation process, then the non-disclosable owner(s) and/or producer(s) should not be included in the corresponding portion marking or banner marking.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}nonICmarkings uses Python identifier nonICmarkings
    __nonICmarkings = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'nonICmarkings'), 'nonICmarkings', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2nonICmarkings', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_12)
    
    nonICmarkings = property(__nonICmarkings.value, __nonICmarkings.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators of the expansion or limitation on the distribution of an information resource or portion within the domain of information originating from non-intelligence components.\n        \n        It is manifested in portion marks and security banners.\n        \n        LAW ENFORCEMENT SENSITIVE (LES) is not an authorized IC classification and control marking in the CAPCO Register. However, CAPCO has published interim marking guidance concerning the incorporation of LES information into IC products. "LES" has been included as a permissible value for attribute "nonICmarkings" in IC ISM in order to facilitate compliance with the CAPCO interim marking guidance in XML-based products.\n\n        PERMISSIBLE VALUES\n        1) The value "LES" is permited as described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Non-IC Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}releasableTo uses Python identifier releasableTo
    __releasableTo = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'releasableTo'), 'releasableTo', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2releasableTo', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_15)
    
    releasableTo = property(__releasableTo.value, __releasableTo.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the country or countries and/or international organization(s) to which classified information may be released based on the determination of an originator in accordance with established foreign disclosure procedures.  This element is used in conjunction with the Dissemination Controls element.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}classification uses Python identifier classification
    __classification = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classification'), 'classification', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2classification', pyxb.bundles.opengis.ic_ism_2_1.ClassificationType)
    
    classification = property(__classification.value, __classification.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        A single indicator of the highest level of classification applicable to an information resource or portion within the domain of classified national security information.  The Classification element is always used in conjunction with the Owner Producer element. Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint).\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set: \n\n        US Classification Markings - Authorized Portion Markings\n        NATO Classification Markings - Authorized Portion Markings\n\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}derivativelyClassifiedBy uses Python identifier derivativelyClassifiedBy
    __derivativelyClassifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivativelyClassifiedBy'), 'derivativelyClassifiedBy', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2derivativelyClassifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON)
    
    derivativelyClassifiedBy = property(__derivativelyClassifiedBy.value, __derivativelyClassifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        \n        The identity, by name or personal identifier, of the derivative classification authority.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}typeOfExemptedSource uses Python identifier typeOfExemptedSource
    __typeOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'typeOfExemptedSource'), 'typeOfExemptedSource', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2typeOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_4)
    
    typeOfExemptedSource = property(__typeOfExemptedSource.value, __typeOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A declassification marking of a source document that causes the current, derivative document to be exempted from automatic declassification.  This element is always used in conjunction with the Date Of Exempted Source element.\n        \n       It is manifested only in the 'Declassify On' line of a document's classification/declassification block.\n       \n       This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Source Document Declassification Instruction Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}classificationReason uses Python identifier classificationReason
    __classificationReason = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classificationReason'), 'classificationReason', '__httpwww_opengis_nettml_SystemType_urnusgovicismv2classificationReason', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_7)
    
    classificationReason = property(__classificationReason.value, __classificationReason.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        One or more reason indicators or explanatory text describing the basis for an original classification decision.\n        \n        It is manifested only in the 'Reason' line of a resource\u2019s Classification/Declassification block.\n      ")


    _ElementMap = {
        __identification.name() : __identification,
        __transducers.name() : __transducers,
        __subjects.name() : __subjects,
        __systems.name() : __systems,
        __otherProperties.name() : __otherProperties,
        __sysClk.name() : __sysClk,
        __clusterDescriptions.name() : __clusterDescriptions,
        __processes.name() : __processes,
        __relations.name() : __relations
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __classifiedBy.name() : __classifiedBy,
        __dateOfExemptedSource.name() : __dateOfExemptedSource,
        __FGIsourceOpen.name() : __FGIsourceOpen,
        __derivedFrom.name() : __derivedFrom,
        __SCIcontrols.name() : __SCIcontrols,
        __uid.name() : __uid,
        __SARIdentifier.name() : __SARIdentifier,
        __declassDate.name() : __declassDate,
        __disseminationControls.name() : __disseminationControls,
        __name.name() : __name,
        __declassManualReview.name() : __declassManualReview,
        __declassEvent.name() : __declassEvent,
        __ownerProducer.name() : __ownerProducer,
        __declassException.name() : __declassException,
        __FGIsourceProtected.name() : __FGIsourceProtected,
        __nonICmarkings.name() : __nonICmarkings,
        __releasableTo.name() : __releasableTo,
        __classification.name() : __classification,
        __derivativelyClassifiedBy.name() : __derivativelyClassifiedBy,
        __typeOfExemptedSource.name() : __typeOfExemptedSource,
        __classificationReason.name() : __classificationReason
    }
Namespace.addCategoryObject('typeBinding', u'SystemType', SystemType)


# Complex type CTD_ANON_29 with content type ELEMENT_ONLY
class CTD_ANON_29 (ValueType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is ValueType
    
    # Element {http://www.opengis.net/tml}calibData uses Python identifier calibData
    __calibData = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'calibData'), 'calibData', '__httpwww_opengis_nettml_CTD_ANON_29_httpwww_opengis_nettmlcalibData', True)

    
    calibData = property(__calibData.value, __calibData.set, None, u'data resulting from calibrated source. or bindUID points to sensor measurement measuring calib source. Default: none')

    
    # Element values ({http://www.opengis.net/tml}values) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element {http://www.opengis.net/tml}dataUidRef uses Python identifier dataUidRef
    __dataUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), 'dataUidRef', '__httpwww_opengis_nettml_CTD_ANON_29_httpwww_opengis_nettmldataUidRef', True)

    
    dataUidRef = property(__dataUidRef.value, __dataUidRef.set, None, u'uid of the data form the logical data structure (dataUnit) to which this response model corresponds')

    
    # Element mult ({http://www.opengis.net/tml}mult) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element accuracy ({http://www.opengis.net/tml}accuracy) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element numValues ({http://www.opengis.net/tml}numValues) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element {http://www.opengis.net/tml}variableName uses Python identifier variableName
    __variableName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'variableName'), 'variableName', '__httpwww_opengis_nettml_CTD_ANON_29_httpwww_opengis_nettmlvariableName', True)

    
    variableName = property(__variableName.value, __variableName.set, None, u'Name of mathematical term used in the transformation equations.  ')

    
    # Element fcnInterpol ({http://www.opengis.net/tml}fcnInterpol) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element offset ({http://www.opengis.net/tml}offset) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element arrayType ({http://www.opengis.net/tml}arrayType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element {http://www.opengis.net/tml}inputOutput uses Python identifier inputOutput
    __inputOutput = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'inputOutput'), 'inputOutput', '__httpwww_opengis_nettml_CTD_ANON_29_httpwww_opengis_nettmlinputOutput', True)

    
    inputOutput = property(__inputOutput.value, __inputOutput.set, None, u'Is the data an input or an output for this dataUnit.  Allowed values: input, output.  Default: output')

    
    # Element valueDataType ({http://www.opengis.net/tml}valueDataType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uidRef inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uid inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute name inherited from {http://www.opengis.net/tml}ValueType

    _ElementMap = ValueType._ElementMap.copy()
    _ElementMap.update({
        __calibData.name() : __calibData,
        __dataUidRef.name() : __dataUidRef,
        __variableName.name() : __variableName,
        __inputOutput.name() : __inputOutput
    })
    _AttributeMap = ValueType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type ProcessType with content type ELEMENT_ONLY
class ProcessType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'ProcessType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}identification uses Python identifier identification
    __identification = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'identification'), 'identification', '__httpwww_opengis_nettml_ProcessType_httpwww_opengis_nettmlidentification', False)

    
    identification = property(__identification.value, __identification.set, None, u'contains security of process description')

    
    # Element {http://www.opengis.net/tml}otherProperties uses Python identifier otherProperties
    __otherProperties = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'otherProperties'), 'otherProperties', '__httpwww_opengis_nettml_ProcessType_httpwww_opengis_nettmlotherProperties', False)

    
    otherProperties = property(__otherProperties.value, __otherProperties.set, None, None)

    
    # Element {http://www.opengis.net/tml}output uses Python identifier output
    __output = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'output'), 'output', '__httpwww_opengis_nettml_ProcessType_httpwww_opengis_nettmloutput', True)

    
    output = property(__output.value, __output.set, None, u'a process can have one or more outputs.  This describes a single output processing cycle, initiated by an output trigger ')

    
    # Element {http://www.opengis.net/tml}input uses Python identifier input
    __input = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'input'), 'input', '__httpwww_opengis_nettml_ProcessType_httpwww_opengis_nettmlinput', True)

    
    input = property(__input.value, __input.set, None, u'a process can have zero or more inputs. This describes a single input process cycle, initiated by an input trigger')

    
    # Attribute {urn:us:gov:ic:ism:v2}SARIdentifier uses Python identifier SARIdentifier
    __SARIdentifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SARIdentifier'), 'SARIdentifier', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2SARIdentifier', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_5)
    
    SARIdentifier = property(__SARIdentifier.value, __SARIdentifier.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the defense or intelligence programs for which special access is required. \n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Special Access Program Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassDate uses Python identifier declassDate
    __declassDate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassDate'), 'declassDate', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2declassDate', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_)
    
    declassDate = property(__declassDate.value, __declassDate.set, None, u"\n         This attribute is used primarily at the resource level.\n         \n         A specific year, month, and day upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n         \n         It is manifested in the 'Declassify On' line of a resource's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceOpen uses Python identifier FGIsourceOpen
    __FGIsourceOpen = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceOpen'), 'FGIsourceOpen', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2FGIsourceOpen', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_11)
    
    FGIsourceOpen = property(__FGIsourceOpen.value, __FGIsourceOpen.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        One or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information is not concealed.\n        \n        The attribute can indicate that the source of information of foreign origin is unknown.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "UNKNOWN" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}disseminationControls uses Python identifier disseminationControls
    __disseminationControls = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'disseminationControls'), 'disseminationControls', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2disseminationControls', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_9)
    
    disseminationControls = property(__disseminationControls.value, __disseminationControls.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the expansion or limitation on the distribution of information.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n         Dissemination Control Markings - Authorized Portion Markings\n        ')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_ProcessType_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassManualReview uses Python identifier declassManualReview
    __declassManualReview = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassManualReview'), 'declassManualReview', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2declassManualReview', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_2)
    
    declassManualReview = property(__declassManualReview.value, __declassManualReview.set, None, u'\n        This attribute is used primarily at the resource level.\n        \n        A single indicator of a requirement for manual review prior to declassification, over and above the usual programmatic determinations.\n        \n        The ability to indicate manual review was rescinded as of 1 February 2008 with complete removal from automated systems required by 31 March 2009 at which time this element will be deprecated.\n \n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassEvent uses Python identifier declassEvent
    __declassEvent = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassEvent'), 'declassEvent', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2declassEvent', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_3)
    
    declassEvent = property(__declassEvent.value, __declassEvent.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A description of an event upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}ownerProducer uses Python identifier ownerProducer
    __ownerProducer = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'ownerProducer'), 'ownerProducer', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2ownerProducer', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_8)
    
    ownerProducer = property(__ownerProducer.value, __ownerProducer.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the national government or international organization that have purview over the classification marking of an information resource or portion therein.  This element is always used in conjunction with the Classification element.  Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint). \n        \n        Within protected internal organizational spaces this element may include one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        Specifically, under these specific circumstances, when data are moved to the shared spaces, the non-disclosable owner(s) and/or producer(s) listed in this data element\u2019s value should be removed and replaced with "FGI".\n        \n        The attribute value may be manifested in portion marks or security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraphs Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassException uses Python identifier declassException
    __declassException = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassException'), 'declassException', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2declassException', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_14)
    
    declassException = property(__declassException.value, __declassException.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A single indicator describing an exemption to the nominal 25-year point for automatic declassification.  This element is used in conjunction with the Declassification Date or Declassification Event.\n        \n        It is manifested in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n        \n        This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Exemption from 25-Year Automatic Declassification Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceProtected uses Python identifier FGIsourceProtected
    __FGIsourceProtected = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceProtected'), 'FGIsourceProtected', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2FGIsourceProtected', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_16)
    
    FGIsourceProtected = property(__FGIsourceProtected.value, __FGIsourceProtected.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        This attribute has unique specific rules concerning its usage. \n        \n        A single indicator that information qualifies as foreign government information for which the source(s) of the information must be concealed.\n        \n        Within protected internal organizational spaces this element may be used to maintain a record of the one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        An indication that information qualifies as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the information is disseminated in shared spaces\n        \n        This data element has a dual purpose. Within shared spaces, the data element serves only to indicate the presence of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information is concealed, in which case, this data element\u2019s value will always be "FGI". The data element may also be employed in this manner within protected internal organizational spaces. However, within protected internal organizational spaces this data element may alternatively be used to maintain a formal record of the foreign country or countries and/or registered international organization(s) that are the non-disclosable owner(s) and/or producer(s) of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the resource is disseminated to shared spaces. If the data element is employed in this manner, then additional measures must be taken prior to dissemination of the resource to shared spaces so that any indications of the non-disclosable owner(s) and/or producer(s) of information within the resource are eliminated.\n\n        In all cases, the corresponding portion marking or banner marking should be compliant with CAPCO guidelines for FGI when the source must be concealed. In other words, even if the data element is being employed within protected internal organizational spaces to maintain a formal record of the non-disclosable owner(s) and/or producer(s) within an XML resource, if the resource is rendered for display within the protected internal organizational spaces in any format by a stylesheet or as a result of any other transformation process, then the non-disclosable owner(s) and/or producer(s) should not be included in the corresponding portion marking or banner marking.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}nonICmarkings uses Python identifier nonICmarkings
    __nonICmarkings = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'nonICmarkings'), 'nonICmarkings', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2nonICmarkings', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_12)
    
    nonICmarkings = property(__nonICmarkings.value, __nonICmarkings.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators of the expansion or limitation on the distribution of an information resource or portion within the domain of information originating from non-intelligence components.\n        \n        It is manifested in portion marks and security banners.\n        \n        LAW ENFORCEMENT SENSITIVE (LES) is not an authorized IC classification and control marking in the CAPCO Register. However, CAPCO has published interim marking guidance concerning the incorporation of LES information into IC products. "LES" has been included as a permissible value for attribute "nonICmarkings" in IC ISM in order to facilitate compliance with the CAPCO interim marking guidance in XML-based products.\n\n        PERMISSIBLE VALUES\n        1) The value "LES" is permited as described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Non-IC Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}releasableTo uses Python identifier releasableTo
    __releasableTo = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'releasableTo'), 'releasableTo', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2releasableTo', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_15)
    
    releasableTo = property(__releasableTo.value, __releasableTo.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the country or countries and/or international organization(s) to which classified information may be released based on the determination of an originator in accordance with established foreign disclosure procedures.  This element is used in conjunction with the Dissemination Controls element.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}classification uses Python identifier classification
    __classification = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classification'), 'classification', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2classification', pyxb.bundles.opengis.ic_ism_2_1.ClassificationType)
    
    classification = property(__classification.value, __classification.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        A single indicator of the highest level of classification applicable to an information resource or portion within the domain of classified national security information.  The Classification element is always used in conjunction with the Owner Producer element. Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint).\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set: \n\n        US Classification Markings - Authorized Portion Markings\n        NATO Classification Markings - Authorized Portion Markings\n\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}derivativelyClassifiedBy uses Python identifier derivativelyClassifiedBy
    __derivativelyClassifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivativelyClassifiedBy'), 'derivativelyClassifiedBy', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2derivativelyClassifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON)
    
    derivativelyClassifiedBy = property(__derivativelyClassifiedBy.value, __derivativelyClassifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        \n        The identity, by name or personal identifier, of the derivative classification authority.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}typeOfExemptedSource uses Python identifier typeOfExemptedSource
    __typeOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'typeOfExemptedSource'), 'typeOfExemptedSource', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2typeOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_4)
    
    typeOfExemptedSource = property(__typeOfExemptedSource.value, __typeOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A declassification marking of a source document that causes the current, derivative document to be exempted from automatic declassification.  This element is always used in conjunction with the Date Of Exempted Source element.\n        \n       It is manifested only in the 'Declassify On' line of a document's classification/declassification block.\n       \n       This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Source Document Declassification Instruction Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}classificationReason uses Python identifier classificationReason
    __classificationReason = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classificationReason'), 'classificationReason', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2classificationReason', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_7)
    
    classificationReason = property(__classificationReason.value, __classificationReason.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        One or more reason indicators or explanatory text describing the basis for an original classification decision.\n        \n        It is manifested only in the 'Reason' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_ProcessType_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute {urn:us:gov:ic:ism:v2}classifiedBy uses Python identifier classifiedBy
    __classifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classifiedBy'), 'classifiedBy', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2classifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_17)
    
    classifiedBy = property(__classifiedBy.value, __classifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        The identity, by name or personal identifier, and position title of the original classification authority for a resource.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}dateOfExemptedSource uses Python identifier dateOfExemptedSource
    __dateOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'dateOfExemptedSource'), 'dateOfExemptedSource', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2dateOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_10)
    
    dateOfExemptedSource = property(__dateOfExemptedSource.value, __dateOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A specific year, month, and day of publication or release of a source document, or the most recent source document, that was itself marked with a declassification constraint.  This element is always used in conjunction with the Type Of Exempted Source element.  \n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}derivedFrom uses Python identifier derivedFrom
    __derivedFrom = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivedFrom'), 'derivedFrom', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2derivedFrom', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_13)
    
    derivedFrom = property(__derivedFrom.value, __derivedFrom.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A citation of the authoritative source or reference to multiple sources of the classification markings used in a classified resource.\n        \n        It is manifested only in the 'Derived From' line of a document's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}SCIcontrols uses Python identifier SCIcontrols
    __SCIcontrols = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SCIcontrols'), 'SCIcontrols', '__httpwww_opengis_nettml_ProcessType_urnusgovicismv2SCIcontrols', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_6)
    
    SCIcontrols = property(__SCIcontrols.value, __SCIcontrols.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying sensitive compartmented information control system(s).\n        \n        It is manifested in portion marks and security banners.                 \n                    \n                    For the "SI-ECI-XXX" permissible value, "XXX" is a placeholder for ECI program designator alphabetic trigraphs, which are classified and are therefore not included here. Additional classified and unpublished SCI control system abbreviations are not included here.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        SCI Control System Markings - Authorized Portion Markings\n      ')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_ProcessType_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')


    _ElementMap = {
        __identification.name() : __identification,
        __otherProperties.name() : __otherProperties,
        __output.name() : __output,
        __input.name() : __input
    }
    _AttributeMap = {
        __SARIdentifier.name() : __SARIdentifier,
        __declassDate.name() : __declassDate,
        __FGIsourceOpen.name() : __FGIsourceOpen,
        __disseminationControls.name() : __disseminationControls,
        __name.name() : __name,
        __declassManualReview.name() : __declassManualReview,
        __declassEvent.name() : __declassEvent,
        __ownerProducer.name() : __ownerProducer,
        __declassException.name() : __declassException,
        __FGIsourceProtected.name() : __FGIsourceProtected,
        __nonICmarkings.name() : __nonICmarkings,
        __releasableTo.name() : __releasableTo,
        __classification.name() : __classification,
        __derivativelyClassifiedBy.name() : __derivativelyClassifiedBy,
        __typeOfExemptedSource.name() : __typeOfExemptedSource,
        __classificationReason.name() : __classificationReason,
        __uidRef.name() : __uidRef,
        __classifiedBy.name() : __classifiedBy,
        __dateOfExemptedSource.name() : __dateOfExemptedSource,
        __derivedFrom.name() : __derivedFrom,
        __SCIcontrols.name() : __SCIcontrols,
        __uid.name() : __uid
    }
Namespace.addCategoryObject('typeBinding', u'ProcessType', ProcessType)


# Complex type TransducerType with content type ELEMENT_ONLY
class TransducerType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'TransducerType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}logicalDataStructure uses Python identifier logicalDataStructure
    __logicalDataStructure = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'logicalDataStructure'), 'logicalDataStructure', '__httpwww_opengis_nettml_TransducerType_httpwww_opengis_nettmllogicalDataStructure', True)

    
    logicalDataStructure = property(__logicalDataStructure.value, __logicalDataStructure.set, None, u'the logical structure of data (i.e. of the characteristic frame).  This is not necessarily the structure or order that data is communicated in.  The transmission order is defined in the cluster description.  The transmission order is defined relative to the logical order.')

    
    # Element {http://www.opengis.net/tml}temporalModel uses Python identifier temporalModel
    __temporalModel = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'temporalModel'), 'temporalModel', '__httpwww_opengis_nettml_TransducerType_httpwww_opengis_nettmltemporalModel', True)

    
    temporalModel = property(__temporalModel.value, __temporalModel.set, None, None)

    
    # Element {http://www.opengis.net/tml}transducerClass uses Python identifier transducerClass
    __transducerClass = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'transducerClass'), 'transducerClass', '__httpwww_opengis_nettml_TransducerType_httpwww_opengis_nettmltransducerClass', False)

    
    transducerClass = property(__transducerClass.value, __transducerClass.set, None, u'Top level transducer classification')

    
    # Element {http://www.opengis.net/tml}identification uses Python identifier identification
    __identification = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'identification'), 'identification', '__httpwww_opengis_nettml_TransducerType_httpwww_opengis_nettmlidentification', False)

    
    identification = property(__identification.value, __identification.set, None, u'bind types on most elements enables the description of transducers in the initialization data stream of data elements.  ')

    
    # Element {http://www.opengis.net/tml}responseModels uses Python identifier responseModels
    __responseModels = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'responseModels'), 'responseModels', '__httpwww_opengis_nettml_TransducerType_httpwww_opengis_nettmlresponseModels', False)

    
    responseModels = property(__responseModels.value, __responseModels.set, None, None)

    
    # Element {http://www.opengis.net/tml}otherProperties uses Python identifier otherProperties
    __otherProperties = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'otherProperties'), 'otherProperties', '__httpwww_opengis_nettml_TransducerType_httpwww_opengis_nettmlotherProperties', False)

    
    otherProperties = property(__otherProperties.value, __otherProperties.set, None, None)

    
    # Element {http://www.opengis.net/tml}spatialModel uses Python identifier spatialModel
    __spatialModel = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'spatialModel'), 'spatialModel', '__httpwww_opengis_nettml_TransducerType_httpwww_opengis_nettmlspatialModel', True)

    
    spatialModel = property(__spatialModel.value, __spatialModel.set, None, None)

    
    # Attribute {urn:us:gov:ic:ism:v2}declassException uses Python identifier declassException
    __declassException = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassException'), 'declassException', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2declassException', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_14)
    
    declassException = property(__declassException.value, __declassException.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A single indicator describing an exemption to the nominal 25-year point for automatic declassification.  This element is used in conjunction with the Declassification Date or Declassification Event.\n        \n        It is manifested in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n        \n        This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Exemption from 25-Year Automatic Declassification Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceProtected uses Python identifier FGIsourceProtected
    __FGIsourceProtected = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceProtected'), 'FGIsourceProtected', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2FGIsourceProtected', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_16)
    
    FGIsourceProtected = property(__FGIsourceProtected.value, __FGIsourceProtected.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        This attribute has unique specific rules concerning its usage. \n        \n        A single indicator that information qualifies as foreign government information for which the source(s) of the information must be concealed.\n        \n        Within protected internal organizational spaces this element may be used to maintain a record of the one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        An indication that information qualifies as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the information is disseminated in shared spaces\n        \n        This data element has a dual purpose. Within shared spaces, the data element serves only to indicate the presence of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information is concealed, in which case, this data element\u2019s value will always be "FGI". The data element may also be employed in this manner within protected internal organizational spaces. However, within protected internal organizational spaces this data element may alternatively be used to maintain a formal record of the foreign country or countries and/or registered international organization(s) that are the non-disclosable owner(s) and/or producer(s) of information which is categorized as foreign government information according to CAPCO guidelines for which the source(s) of the information must be concealed when the resource is disseminated to shared spaces. If the data element is employed in this manner, then additional measures must be taken prior to dissemination of the resource to shared spaces so that any indications of the non-disclosable owner(s) and/or producer(s) of information within the resource are eliminated.\n\n        In all cases, the corresponding portion marking or banner marking should be compliant with CAPCO guidelines for FGI when the source must be concealed. In other words, even if the data element is being employed within protected internal organizational spaces to maintain a formal record of the non-disclosable owner(s) and/or producer(s) within an XML resource, if the resource is rendered for display within the protected internal organizational spaces in any format by a stylesheet or as a result of any other transformation process, then the non-disclosable owner(s) and/or producer(s) should not be included in the corresponding portion marking or banner marking.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}nonICmarkings uses Python identifier nonICmarkings
    __nonICmarkings = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'nonICmarkings'), 'nonICmarkings', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2nonICmarkings', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_12)
    
    nonICmarkings = property(__nonICmarkings.value, __nonICmarkings.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators of the expansion or limitation on the distribution of an information resource or portion within the domain of information originating from non-intelligence components.\n        \n        It is manifested in portion marks and security banners.\n        \n        LAW ENFORCEMENT SENSITIVE (LES) is not an authorized IC classification and control marking in the CAPCO Register. However, CAPCO has published interim marking guidance concerning the incorporation of LES information into IC products. "LES" has been included as a permissible value for attribute "nonICmarkings" in IC ISM in order to facilitate compliance with the CAPCO interim marking guidance in XML-based products.\n\n        PERMISSIBLE VALUES\n        1) The value "LES" is permited as described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Non-IC Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}releasableTo uses Python identifier releasableTo
    __releasableTo = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'releasableTo'), 'releasableTo', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2releasableTo', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_15)
    
    releasableTo = property(__releasableTo.value, __releasableTo.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the country or countries and/or international organization(s) to which classified information may be released based on the determination of an originator in accordance with established foreign disclosure procedures.  This element is used in conjunction with the Dissemination Controls element.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}classification uses Python identifier classification
    __classification = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classification'), 'classification', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2classification', pyxb.bundles.opengis.ic_ism_2_1.ClassificationType)
    
    classification = property(__classification.value, __classification.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        A single indicator of the highest level of classification applicable to an information resource or portion within the domain of classified national security information.  The Classification element is always used in conjunction with the Owner Producer element. Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint).\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set: \n\n        US Classification Markings - Authorized Portion Markings\n        NATO Classification Markings - Authorized Portion Markings\n\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}derivativelyClassifiedBy uses Python identifier derivativelyClassifiedBy
    __derivativelyClassifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivativelyClassifiedBy'), 'derivativelyClassifiedBy', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2derivativelyClassifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON)
    
    derivativelyClassifiedBy = property(__derivativelyClassifiedBy.value, __derivativelyClassifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        \n        The identity, by name or personal identifier, of the derivative classification authority.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}typeOfExemptedSource uses Python identifier typeOfExemptedSource
    __typeOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'typeOfExemptedSource'), 'typeOfExemptedSource', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2typeOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_4)
    
    typeOfExemptedSource = property(__typeOfExemptedSource.value, __typeOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A declassification marking of a source document that causes the current, derivative document to be exempted from automatic declassification.  This element is always used in conjunction with the Date Of Exempted Source element.\n        \n       It is manifested only in the 'Declassify On' line of a document's classification/declassification block.\n       \n       This element is defined as NMTOKENS but ISOO has stated it should be a SINGLE value giving the longest protection.\n\n        PERMISSIBLE VALUE\n\n        The permissible value for this attribute is defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Source Document Declassification Instruction Markings\n\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}classificationReason uses Python identifier classificationReason
    __classificationReason = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classificationReason'), 'classificationReason', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2classificationReason', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_7)
    
    classificationReason = property(__classificationReason.value, __classificationReason.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        One or more reason indicators or explanatory text describing the basis for an original classification decision.\n        \n        It is manifested only in the 'Reason' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_TransducerType_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute {urn:us:gov:ic:ism:v2}classifiedBy uses Python identifier classifiedBy
    __classifiedBy = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'classifiedBy'), 'classifiedBy', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2classifiedBy', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_17)
    
    classifiedBy = property(__classifiedBy.value, __classifiedBy.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        The identity, by name or personal identifier, and position title of the original classification authority for a resource.\n        \n        It is manifested only in the 'Classified By' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}dateOfExemptedSource uses Python identifier dateOfExemptedSource
    __dateOfExemptedSource = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'dateOfExemptedSource'), 'dateOfExemptedSource', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2dateOfExemptedSource', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_10)
    
    dateOfExemptedSource = property(__dateOfExemptedSource.value, __dateOfExemptedSource.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A specific year, month, and day of publication or release of a source document, or the most recent source document, that was itself marked with a declassification constraint.  This element is always used in conjunction with the Type Of Exempted Source element.  \n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s Classification/Declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}derivedFrom uses Python identifier derivedFrom
    __derivedFrom = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'derivedFrom'), 'derivedFrom', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2derivedFrom', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_13)
    
    derivedFrom = property(__derivedFrom.value, __derivedFrom.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A citation of the authoritative source or reference to multiple sources of the classification markings used in a classified resource.\n        \n        It is manifested only in the 'Derived From' line of a document's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}SCIcontrols uses Python identifier SCIcontrols
    __SCIcontrols = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SCIcontrols'), 'SCIcontrols', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2SCIcontrols', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_6)
    
    SCIcontrols = property(__SCIcontrols.value, __SCIcontrols.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying sensitive compartmented information control system(s).\n        \n        It is manifested in portion marks and security banners.                 \n                    \n                    For the "SI-ECI-XXX" permissible value, "XXX" is a placeholder for ECI program designator alphabetic trigraphs, which are classified and are therefore not included here. Additional classified and unpublished SCI control system abbreviations are not included here.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        SCI Control System Markings - Authorized Portion Markings\n      ')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_TransducerType_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute {urn:us:gov:ic:ism:v2}SARIdentifier uses Python identifier SARIdentifier
    __SARIdentifier = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'SARIdentifier'), 'SARIdentifier', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2SARIdentifier', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_5)
    
    SARIdentifier = property(__SARIdentifier.value, __SARIdentifier.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the defense or intelligence programs for which special access is required. \n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n        Special Access Program Markings - Authorized Portion Markings\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassDate uses Python identifier declassDate
    __declassDate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassDate'), 'declassDate', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2declassDate', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_)
    
    declassDate = property(__declassDate.value, __declassDate.set, None, u"\n         This attribute is used primarily at the resource level.\n         \n         A specific year, month, and day upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n         \n         It is manifested in the 'Declassify On' line of a resource's classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}disseminationControls uses Python identifier disseminationControls
    __disseminationControls = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'disseminationControls'), 'disseminationControls', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2disseminationControls', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_9)
    
    disseminationControls = property(__disseminationControls.value, __disseminationControls.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the expansion or limitation on the distribution of information.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        The permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value set:\n\n         Dissemination Control Markings - Authorized Portion Markings\n        ')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_TransducerType_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassManualReview uses Python identifier declassManualReview
    __declassManualReview = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassManualReview'), 'declassManualReview', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2declassManualReview', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_2)
    
    declassManualReview = property(__declassManualReview.value, __declassManualReview.set, None, u'\n        This attribute is used primarily at the resource level.\n        \n        A single indicator of a requirement for manual review prior to declassification, over and above the usual programmatic determinations.\n        \n        The ability to indicate manual review was rescinded as of 1 February 2008 with complete removal from automated systems required by 31 March 2009 at which time this element will be deprecated.\n \n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}declassEvent uses Python identifier declassEvent
    __declassEvent = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'declassEvent'), 'declassEvent', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2declassEvent', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_3)
    
    declassEvent = property(__declassEvent.value, __declassEvent.set, None, u"\n        This attribute is used primarily at the resource level.\n        \n        A description of an event upon which the information shall be automatically declassified if not properly exempted from automatic declassification.\n        \n        It is manifested only in the 'Declassify On' line of a resource\u2019s classification/declassification block.\n      ")

    
    # Attribute {urn:us:gov:ic:ism:v2}ownerProducer uses Python identifier ownerProducer
    __ownerProducer = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'ownerProducer'), 'ownerProducer', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2ownerProducer', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_8)
    
    ownerProducer = property(__ownerProducer.value, __ownerProducer.set, None, u'\n        This attribute is used at both the resource and the portion levels.\n        \n        One or more indicators identifying the national government or international organization that have purview over the classification marking of an information resource or portion therein.  This element is always used in conjunction with the Classification element.  Taken together, the two elements specify the classification category and the type of classification (US, non-US, or Joint). \n        \n        Within protected internal organizational spaces this element may include one or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information must be concealed.  Measures must be taken prior to dissemination of the information to conceal the source(s) of the foreign government information.\n        \n        Specifically, under these specific circumstances, when data are moved to the shared spaces, the non-disclosable owner(s) and/or producer(s) listed in this data element\u2019s value should be removed and replaced with "FGI".\n        \n        The attribute value may be manifested in portion marks or security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "FGI" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraphs Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')

    
    # Attribute {urn:us:gov:ic:ism:v2}FGIsourceOpen uses Python identifier FGIsourceOpen
    __FGIsourceOpen = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(pyxb.namespace.NamespaceForURI(u'urn:us:gov:ic:ism:v2'), u'FGIsourceOpen'), 'FGIsourceOpen', '__httpwww_opengis_nettml_TransducerType_urnusgovicismv2FGIsourceOpen', pyxb.bundles.opengis.ic_ism_2_1.STD_ANON_11)
    
    FGIsourceOpen = property(__FGIsourceOpen.value, __FGIsourceOpen.set, None, u'\n        This attribute is used at both the resource and the portion levels. \n        \n        One or more indicators identifying information which qualifies as foreign government information for which the source(s) of the information is not concealed.\n        \n        The attribute can indicate that the source of information of foreign origin is unknown.\n        \n        It is manifested in portion marks and security banners.\n\n        PERMISSIBLE VALUES\n\n        1) The value "UNKNOWN" is permited under the circumstances described above.\n\n        2) Other permissible values for this attribute are defined in the Implementation Profile Supplement: Value Enumerations in the value sets:\n\n        ISO 3166-1 Country Trigraph Codes\n        Registered International Organizations and Alliances Tetragraphs\n      ')


    _ElementMap = {
        __logicalDataStructure.name() : __logicalDataStructure,
        __temporalModel.name() : __temporalModel,
        __transducerClass.name() : __transducerClass,
        __identification.name() : __identification,
        __responseModels.name() : __responseModels,
        __otherProperties.name() : __otherProperties,
        __spatialModel.name() : __spatialModel
    }
    _AttributeMap = {
        __declassException.name() : __declassException,
        __FGIsourceProtected.name() : __FGIsourceProtected,
        __nonICmarkings.name() : __nonICmarkings,
        __releasableTo.name() : __releasableTo,
        __classification.name() : __classification,
        __derivativelyClassifiedBy.name() : __derivativelyClassifiedBy,
        __typeOfExemptedSource.name() : __typeOfExemptedSource,
        __classificationReason.name() : __classificationReason,
        __uidRef.name() : __uidRef,
        __classifiedBy.name() : __classifiedBy,
        __dateOfExemptedSource.name() : __dateOfExemptedSource,
        __derivedFrom.name() : __derivedFrom,
        __SCIcontrols.name() : __SCIcontrols,
        __uid.name() : __uid,
        __SARIdentifier.name() : __SARIdentifier,
        __declassDate.name() : __declassDate,
        __disseminationControls.name() : __disseminationControls,
        __name.name() : __name,
        __declassManualReview.name() : __declassManualReview,
        __declassEvent.name() : __declassEvent,
        __ownerProducer.name() : __ownerProducer,
        __FGIsourceOpen.name() : __FGIsourceOpen
    }
Namespace.addCategoryObject('typeBinding', u'TransducerType', TransducerType)


# Complex type CTD_ANON_30 with content type ELEMENT_ONLY
class CTD_ANON_30 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}listing uses Python identifier listing
    __listing = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'listing'), 'listing', '__httpwww_opengis_nettml_CTD_ANON_30_httpwww_opengis_nettmllisting', False)

    
    listing = property(__listing.value, __listing.set, None, u'Listing of code. Base64 encoded executable or source code with unallowed XML characters escaped out')

    
    # Element {http://www.opengis.net/tml}properties uses Python identifier properties
    __properties = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'properties'), 'properties', '__httpwww_opengis_nettml_CTD_ANON_30_httpwww_opengis_nettmlproperties', False)

    
    properties = property(__properties.value, __properties.set, None, None)

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_30_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_30_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_30_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')


    _ElementMap = {
        __listing.name() : __listing,
        __properties.name() : __properties
    }
    _AttributeMap = {
        __name.name() : __name,
        __uidRef.name() : __uidRef,
        __uid.name() : __uid
    }



# Complex type SpatialCoordType with content type ELEMENT_ONLY
class SpatialCoordType (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SpatialCoordType')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}refObjUidRef uses Python identifier refObjUidRef
    __refObjUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'refObjUidRef'), 'refObjUidRef', '__httpwww_opengis_nettml_SpatialCoordType_httpwww_opengis_nettmlrefObjUidRef', False)

    
    refObjUidRef = property(__refObjUidRef.value, __refObjUidRef.set, None, u'If the spaceRefSystem element is a transducer or a Sunbect, then this element will identify the particular Transducer or Subject.  This is the UID reference of the object which position coordinates are referenced (relative) to.')

    
    # Element {http://www.opengis.net/tml}spaceCoordSystem uses Python identifier spaceCoordSystem
    __spaceCoordSystem = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'spaceCoordSystem'), 'spaceCoordSystem', '__httpwww_opengis_nettml_SpatialCoordType_httpwww_opengis_nettmlspaceCoordSystem', False)

    
    spaceCoordSystem = property(__spaceCoordSystem.value, __spaceCoordSystem.set, None, u'Allowed values: spherical,  rectangular, cylindrical, wgs84elliptical.  default is spherical.')

    
    # Element {http://www.opengis.net/tml}spaceCoords uses Python identifier spaceCoords
    __spaceCoords = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'spaceCoords'), 'spaceCoords', '__httpwww_opengis_nettml_SpatialCoordType_httpwww_opengis_nettmlspaceCoords', True)

    
    spaceCoords = property(__spaceCoords.value, __spaceCoords.set, None, u'TCF set of positional (translations and rotations) coordinates for each shape,  space separated real numbers.  Order of coordinates shall be from lowest frequency to highest frequency, same as lds. Default locations and orientations are zero')

    
    # Element {http://www.opengis.net/tml}spaceRefSystem uses Python identifier spaceRefSystem
    __spaceRefSystem = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'spaceRefSystem'), 'spaceRefSystem', '__httpwww_opengis_nettml_SpatialCoordType_httpwww_opengis_nettmlspaceRefSystem', False)

    
    spaceRefSystem = property(__spaceRefSystem.value, __spaceRefSystem.set, None, u'which spatial reference system (i.e. spatial datum) are spatial coordinates referenced (relative) to.   Allowed values: transducer, earthCentered, earthLocal, subject. If ref system is transducer or subject then the uid of the transducer or subject must be identified in the refObjUidRef element.')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_SpatialCoordType_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_SpatialCoordType_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_SpatialCoordType_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __refObjUidRef.name() : __refObjUidRef,
        __spaceCoordSystem.name() : __spaceCoordSystem,
        __spaceCoords.name() : __spaceCoords,
        __spaceRefSystem.name() : __spaceRefSystem
    }
    _AttributeMap = {
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    }
Namespace.addCategoryObject('typeBinding', u'SpatialCoordType', SpatialCoordType)


# Complex type CTD_ANON_31 with content type ELEMENT_ONLY
class CTD_ANON_31 (SpatialCoordType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is SpatialCoordType
    
    # Element refObjUidRef ({http://www.opengis.net/tml}refObjUidRef) inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Element spaceCoordSystem ({http://www.opengis.net/tml}spaceCoordSystem) inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Element {http://www.opengis.net/tml}objUidRef uses Python identifier objUidRef
    __objUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'objUidRef'), 'objUidRef', '__httpwww_opengis_nettml_CTD_ANON_31_httpwww_opengis_nettmlobjUidRef', True)

    
    objUidRef = property(__objUidRef.value, __objUidRef.set, None, u'uid of the obj being positioned. multiples allowed if in same position and orientation')

    
    # Element spaceRefSystem ({http://www.opengis.net/tml}spaceRefSystem) inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Element spaceCoords ({http://www.opengis.net/tml}spaceCoords) inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Attribute uid inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Attribute uidRef inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Attribute name inherited from {http://www.opengis.net/tml}SpatialCoordType

    _ElementMap = SpatialCoordType._ElementMap.copy()
    _ElementMap.update({
        __objUidRef.name() : __objUidRef
    })
    _AttributeMap = SpatialCoordType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_32 with content type MIXED
class CTD_ANON_32 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_32_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_32_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_32_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any)
    _HasWildcardElement = True

    _ElementMap = {
        
    }
    _AttributeMap = {
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    }



# Complex type CTD_ANON_33 with content type ELEMENT_ONLY
class CTD_ANON_33 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}codeType uses Python identifier codeType
    __codeType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'codeType'), 'codeType', '__httpwww_opengis_nettml_CTD_ANON_33_httpwww_opengis_nettmlcodeType', False)

    
    codeType = property(__codeType.value, __codeType.set, None, u'Allowed Values: source, exe default: source')

    
    # Element {http://www.opengis.net/tml}codeLanguage uses Python identifier codeLanguage
    __codeLanguage = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'codeLanguage'), 'codeLanguage', '__httpwww_opengis_nettml_CTD_ANON_33_httpwww_opengis_nettmlcodeLanguage', False)

    
    codeLanguage = property(__codeLanguage.value, __codeLanguage.set, None, u'Allowed Values: C, C++, Java, Fortran, C Sharp, Basic, Visual Basic. Default: C')


    _ElementMap = {
        __codeType.name() : __codeType,
        __codeLanguage.name() : __codeLanguage
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_34 with content type ELEMENT_ONLY
class CTD_ANON_34 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}description uses Python identifier description
    __description = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'description'), 'description', '__httpwww_opengis_nettml_CTD_ANON_34_httpwww_opengis_nettmldescription', False)

    
    description = property(__description.value, __description.set, None, None)

    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_34_httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'uid of output')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_34_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __description.name() : __description,
        __uid.name() : __uid,
        __name.name() : __name
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_35 with content type SIMPLE
class CTD_ANON_35 (BindType):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is BindType
    
    # Attribute bindUid inherited from {http://www.opengis.net/tml}BindType
    
    # Attribute bindUidRef inherited from {http://www.opengis.net/tml}BindType

    _ElementMap = BindType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BindType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_36 with content type ELEMENT_ONLY
class CTD_ANON_36 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}dataUidRef uses Python identifier dataUidRef
    __dataUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), 'dataUidRef', '__httpwww_opengis_nettml_CTD_ANON_36_httpwww_opengis_nettmldataUidRef', False)

    
    dataUidRef = property(__dataUidRef.value, __dataUidRef.set, None, u'same as uidRef in attributes')

    
    # Element {http://www.opengis.net/tml}time uses Python identifier time
    __time = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'time'), 'time', '__httpwww_opengis_nettml_CTD_ANON_36_httpwww_opengis_nettmltime', False)

    
    time = property(__time.value, __time.set, None, u'time domain independent axis.')

    
    # Element {http://www.opengis.net/tml}freqTime uses Python identifier freqTime
    __freqTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'freqTime'), 'freqTime', '__httpwww_opengis_nettml_CTD_ANON_36_httpwww_opengis_nettmlfreqTime', False)

    
    freqTime = property(__freqTime.value, __freqTime.set, None, u'Allowed values: freq, time.  default is time.  indicates if frequency of time domain descriptions.  ')

    
    # Element {http://www.opengis.net/tml}frequency uses Python identifier frequency
    __frequency = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'frequency'), 'frequency', '__httpwww_opengis_nettml_CTD_ANON_36_httpwww_opengis_nettmlfrequency', False)

    
    frequency = property(__frequency.value, __frequency.set, None, u'frequency domain independent axis.')

    
    # Element {http://www.opengis.net/tml}amplitude uses Python identifier amplitude
    __amplitude = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'amplitude'), 'amplitude', '__httpwww_opengis_nettml_CTD_ANON_36_httpwww_opengis_nettmlamplitude', False)

    
    amplitude = property(__amplitude.value, __amplitude.set, None, u'amplitude dependent axis.')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_36_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_36_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_36_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __dataUidRef.name() : __dataUidRef,
        __time.name() : __time,
        __freqTime.name() : __freqTime,
        __frequency.name() : __frequency,
        __amplitude.name() : __amplitude
    }
    _AttributeMap = {
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    }



# Complex type CTD_ANON_37 with content type ELEMENT_ONLY
class CTD_ANON_37 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}objUidRef uses Python identifier objUidRef
    __objUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'objUidRef'), 'objUidRef', '__httpwww_opengis_nettml_CTD_ANON_37_httpwww_opengis_nettmlobjUidRef', False)

    
    objUidRef = property(__objUidRef.value, __objUidRef.set, None, u'UID of the object (subject or transducer, or probable subject).  local id of the subject if multiple ids are used to associate with each cell of  the logical structure.  ')

    
    # Element {http://www.opengis.net/tml}cfSubSampling uses Python identifier cfSubSampling
    __cfSubSampling = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling'), 'cfSubSampling', '__httpwww_opengis_nettml_CTD_ANON_37_httpwww_opengis_nettmlcfSubSampling', False)

    
    cfSubSampling = property(__cfSubSampling.value, __cfSubSampling.set, None, u'the CFSubSampling can be used for chipping part of a large dataArry out and for reducing the number of points within an array for which to associate modeling parameters.  there is one sub sampling element set of points for each component structure (col, row, plane).    index numbers of col, row or plane position within the CFs are listed for which corresponding modeling points will be associated.  sample points are separated by commas, ranges are indicated by ... between numbers which indicates a continuous interval for a single sample. interpolation between samples uses logical structure.  ')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_37_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, u'name of the object')

    
    # Element {http://www.opengis.net/tml}objLocalID uses Python identifier objLocalID
    __objLocalID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'objLocalID'), 'objLocalID', '__httpwww_opengis_nettml_CTD_ANON_37_httpwww_opengis_nettmlobjLocalID', False)

    
    objLocalID = property(__objLocalID.value, __objLocalID.set, None, u'if localId assigned to objUidRef for building CF of obj to data (i.e.CF) relationships. Sequence of values is the same as the sequence in the data (logical data structure or subsampled data structure, if present)')

    
    # Element {http://www.opengis.net/tml}objType uses Python identifier objType
    __objType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'objType'), 'objType', '__httpwww_opengis_nettml_CTD_ANON_37_httpwww_opengis_nettmlobjType', False)

    
    objType = property(__objType.value, __objType.set, None, u'identify object as a transducer or a subject. Allowed Values: subject, transducer. Default: subject')

    
    # Element {http://www.opengis.net/tml}confidence uses Python identifier confidence
    __confidence = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'confidence'), 'confidence', '__httpwww_opengis_nettml_CTD_ANON_37_httpwww_opengis_nettmlconfidence', False)

    
    confidence = property(__confidence.value, __confidence.set, None, u'Value range -1 to 1.  -1 is 100% no confidence.  confidence values match same sequence as logical data structure or subsampled data structure, if present (if multiple objects in data structure)')

    
    # Attribute name uses Python identifier name_
    __name_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name_', '__httpwww_opengis_nettml_CTD_ANON_37_name', pyxb.binding.datatypes.string)
    
    name_ = property(__name_.value, __name_.set, None, u'short descriptive name of element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_37_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_37_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')


    _ElementMap = {
        __objUidRef.name() : __objUidRef,
        __cfSubSampling.name() : __cfSubSampling,
        __name.name() : __name,
        __objLocalID.name() : __objLocalID,
        __objType.name() : __objType,
        __confidence.name() : __confidence
    }
    _AttributeMap = {
        __name_.name() : __name_,
        __uidRef.name() : __uidRef,
        __uid.name() : __uid
    }



# Complex type CTD_ANON_38 with content type ELEMENT_ONLY
class CTD_ANON_38 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}property uses Python identifier property_
    __property = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'property'), 'property_', '__httpwww_opengis_nettml_CTD_ANON_38_httpwww_opengis_nettmlproperty', True)

    
    property_ = property(__property.value, __property.set, None, None)


    _ElementMap = {
        __property.name() : __property
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_39 with content type SIMPLE
class CTD_ANON_39 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute clk uses Python identifier clk
    __clk = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'clk'), 'clk', '__httpwww_opengis_nettml_CTD_ANON_39_clk', pyxb.binding.datatypes.integer)
    
    clk = property(__clk.value, __clk.set, None, u'sys clock state at trigger point to data cluster.  For low sampling frequency transducers this high frequency clock state may not be required.  A full dateTime attribute may suffice for time synchronization of data.')

    
    # Attribute total uses Python identifier total
    __total = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'total'), 'total', '__httpwww_opengis_nettml_CTD_ANON_39_total', pyxb.binding.datatypes.integer)
    
    total = property(__total.value, __total.set, None, u'total in sequence e.g. 1 of 4, 2 of 4.  1 and 2 being the seq number and 4 being the total')

    
    # Attribute contents uses Python identifier contents
    __contents = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'contents'), 'contents', '__httpwww_opengis_nettml_CTD_ANON_39_contents', STD_ANON)
    
    contents = property(__contents.value, __contents.set, None, u'If a binary stream header does not contain a contents field then the data cluster is by default explicit data.  This field is encoded as a binary (2-bits) "00" in a binary file if the field is contained.')

    
    # Attribute reference uses Python identifier reference
    __reference = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'reference'), 'reference', '__httpwww_opengis_nettml_CTD_ANON_39_reference', pyxb.binding.datatypes.anyURI)
    
    reference = property(__reference.value, __reference.set, None, u'this is the full UID reference to the cluster description')

    
    # Attribute ismclass uses Python identifier ismclass
    __ismclass = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ismclass'), 'ismclass', '__httpwww_opengis_nettml_CTD_ANON_39_ismclass', pyxb.bundles.opengis.ic_ism_2_1.ClassificationType)
    
    ismclass = property(__ismclass.value, __ismclass.set, None, u'security classification of each data cluster. Overall data classification of  transducer data in clusterDescription.  Overall classification of file or stream in tml start tag.')

    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'ref'), 'ref', '__httpwww_opengis_nettml_CTD_ANON_39_ref', pyxb.binding.datatypes.string)
    
    ref = property(__ref.value, __ref.set, None, u'alias or short id reference of transducer or process producing this data')

    
    # Attribute seq uses Python identifier seq
    __seq = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'seq'), 'seq', '__httpwww_opengis_nettml_CTD_ANON_39_seq', pyxb.binding.datatypes.integer)
    
    seq = property(__seq.value, __seq.set, None, u'if no "total" attribute exist then this attribute can be used to number the data elements like a count, this enables the receipt end to determine if any data clusters were lost.')

    
    # Attribute dateTime uses Python identifier dateTime
    __dateTime = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'dateTime'), 'dateTime', '__httpwww_opengis_nettml_CTD_ANON_39_dateTime', pyxb.binding.datatypes.dateTime)
    
    dateTime = property(__dateTime.value, __dateTime.set, None, u'Full qualified date and time of transducer or process producing this data. For low sampling frequency transducers this high frequency clock state may not be required.  A full dateTime attribute may suffice for time synchronization of data.')


    _ElementMap = {
        
    }
    _AttributeMap = {
        __clk.name() : __clk,
        __total.name() : __total,
        __contents.name() : __contents,
        __reference.name() : __reference,
        __ismclass.name() : __ismclass,
        __ref.name() : __ref,
        __seq.name() : __seq,
        __dateTime.name() : __dateTime
    }



# Complex type CTD_ANON_40 with content type ELEMENT_ONLY
class CTD_ANON_40 (IdentificationType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is IdentificationType
    
    # Element calibration ({http://www.opengis.net/tml}calibration) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element {http://www.opengis.net/tml}serialNumber uses Python identifier serialNumber
    __serialNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'serialNumber'), 'serialNumber', '__httpwww_opengis_nettml_CTD_ANON_40_httpwww_opengis_nettmlserialNumber', False)

    
    serialNumber = property(__serialNumber.value, __serialNumber.set, None, None)

    
    # Element characterization ({http://www.opengis.net/tml}characterization) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element {http://www.opengis.net/tml}ownedBy uses Python identifier ownedBy
    __ownedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ownedBy'), 'ownedBy', '__httpwww_opengis_nettml_CTD_ANON_40_httpwww_opengis_nettmlownedBy', True)

    
    ownedBy = property(__ownedBy.value, __ownedBy.set, None, None)

    
    # Element complexity ({http://www.opengis.net/tml}complexity) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element name ({http://www.opengis.net/tml}name) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element {http://www.opengis.net/tml}manufacture uses Python identifier manufacture
    __manufacture = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'manufacture'), 'manufacture', '__httpwww_opengis_nettml_CTD_ANON_40_httpwww_opengis_nettmlmanufacture', False)

    
    manufacture = property(__manufacture.value, __manufacture.set, None, None)

    
    # Element description ({http://www.opengis.net/tml}description) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element {http://www.opengis.net/tml}modelNumber uses Python identifier modelNumber
    __modelNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'modelNumber'), 'modelNumber', '__httpwww_opengis_nettml_CTD_ANON_40_httpwww_opengis_nettmlmodelNumber', False)

    
    modelNumber = property(__modelNumber.value, __modelNumber.set, None, None)

    
    # Element uid ({http://www.opengis.net/tml}uid) inherited from {http://www.opengis.net/tml}IdentificationType

    _ElementMap = IdentificationType._ElementMap.copy()
    _ElementMap.update({
        __serialNumber.name() : __serialNumber,
        __ownedBy.name() : __ownedBy,
        __manufacture.name() : __manufacture,
        __modelNumber.name() : __modelNumber
    })
    _AttributeMap = IdentificationType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_41 with content type ELEMENT_ONLY
class CTD_ANON_41 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}email uses Python identifier email
    __email = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'email'), 'email', '__httpwww_opengis_nettml_CTD_ANON_41_httpwww_opengis_nettmlemail', False)

    
    email = property(__email.value, __email.set, None, None)

    
    # Element {http://www.opengis.net/tml}phone uses Python identifier phone
    __phone = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'phone'), 'phone', '__httpwww_opengis_nettml_CTD_ANON_41_httpwww_opengis_nettmlphone', False)

    
    phone = property(__phone.value, __phone.set, None, None)

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_41_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {http://www.opengis.net/tml}date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'date'), 'date', '__httpwww_opengis_nettml_CTD_ANON_41_httpwww_opengis_nettmldate', False)

    
    date = property(__date.value, __date.set, None, u'ISO8601 dateTime stamp')

    
    # Element {http://www.opengis.net/tml}organization uses Python identifier organization
    __organization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'organization'), 'organization', '__httpwww_opengis_nettml_CTD_ANON_41_httpwww_opengis_nettmlorganization', False)

    
    organization = property(__organization.value, __organization.set, None, None)


    _ElementMap = {
        __email.name() : __email,
        __phone.name() : __phone,
        __name.name() : __name,
        __date.name() : __date,
        __organization.name() : __organization
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_42 with content type ELEMENT_ONLY
class CTD_ANON_42 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}cfDataArray uses Python identifier cfDataArray
    __cfDataArray = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'cfDataArray'), 'cfDataArray', '__httpwww_opengis_nettml_CTD_ANON_42_httpwww_opengis_nettmlcfDataArray', False)

    
    cfDataArray = property(__cfDataArray.value, __cfDataArray.set, None, u'logical data structure of the characteristic frame.  Lowest frequency array first.')

    
    # Element {http://www.opengis.net/tml}ldsDimensionality uses Python identifier ldsDimensionality
    __ldsDimensionality = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ldsDimensionality'), 'ldsDimensionality', '__httpwww_opengis_nettml_CTD_ANON_42_httpwww_opengis_nettmlldsDimensionality', False)

    
    ldsDimensionality = property(__ldsDimensionality.value, __ldsDimensionality.set, None, u'Allowed values: 0, 1, 2, 3.  Default is 0.  dimensionality of the logical data structure (lds).  number of structure components used for giving hints for data representation.  0 dim is a single value, 1 dim is a series of columns, rows or planes, 2 dim is any order of  two structure components (col-row, col-plane, or row-plane), and a 3 dim is any order of three structure components col-row-plane')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_42_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, u'name of lds')

    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_42_httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'uid of lds')

    
    # Element {http://www.opengis.net/tml}numOfDataSetsInCf uses Python identifier numOfDataSetsInCf
    __numOfDataSetsInCf = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numOfDataSetsInCf'), 'numOfDataSetsInCf', '__httpwww_opengis_nettml_CTD_ANON_42_httpwww_opengis_nettmlnumOfDataSetsInCf', False)

    
    numOfDataSetsInCf = property(__numOfDataSetsInCf.value, __numOfDataSetsInCf.set, None, u'Number of dataSets or dataArrays in the Characteristic Frame.  Allowed Value: positive integer.  Default:1')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_42_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name_
    __name_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name_', '__httpwww_opengis_nettml_CTD_ANON_42_name', pyxb.binding.datatypes.string)
    
    name_ = property(__name_.value, __name_.set, None, u'short descriptive name of element')

    
    # Attribute uid uses Python identifier uid_
    __uid_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid_', '__httpwww_opengis_nettml_CTD_ANON_42_uid', pyxb.binding.datatypes.anyURI)
    
    uid_ = property(__uid_.value, __uid_.set, None, u'unique ID for this element')


    _ElementMap = {
        __cfDataArray.name() : __cfDataArray,
        __ldsDimensionality.name() : __ldsDimensionality,
        __name.name() : __name,
        __uid.name() : __uid,
        __numOfDataSetsInCf.name() : __numOfDataSetsInCf
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __name_.name() : __name_,
        __uid_.name() : __uid_
    }



# Complex type CTD_ANON_43 with content type ELEMENT_ONLY
class CTD_ANON_43 (IdentificationType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is IdentificationType
    
    # Element {http://www.opengis.net/tml}serialNumber uses Python identifier serialNumber
    __serialNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'serialNumber'), 'serialNumber', '__httpwww_opengis_nettml_CTD_ANON_43_httpwww_opengis_nettmlserialNumber', False)

    
    serialNumber = property(__serialNumber.value, __serialNumber.set, None, None)

    
    # Element {http://www.opengis.net/tml}ownedBy uses Python identifier ownedBy
    __ownedBy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ownedBy'), 'ownedBy', '__httpwww_opengis_nettml_CTD_ANON_43_httpwww_opengis_nettmlownedBy', True)

    
    ownedBy = property(__ownedBy.value, __ownedBy.set, None, None)

    
    # Element description ({http://www.opengis.net/tml}description) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element uid ({http://www.opengis.net/tml}uid) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element calibration ({http://www.opengis.net/tml}calibration) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element {http://www.opengis.net/tml}processVersion uses Python identifier processVersion
    __processVersion = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'processVersion'), 'processVersion', '__httpwww_opengis_nettml_CTD_ANON_43_httpwww_opengis_nettmlprocessVersion', False)

    
    processVersion = property(__processVersion.value, __processVersion.set, None, None)

    
    # Element {http://www.opengis.net/tml}manufacture uses Python identifier manufacture
    __manufacture = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'manufacture'), 'manufacture', '__httpwww_opengis_nettml_CTD_ANON_43_httpwww_opengis_nettmlmanufacture', False)

    
    manufacture = property(__manufacture.value, __manufacture.set, None, None)

    
    # Element name ({http://www.opengis.net/tml}name) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element characterization ({http://www.opengis.net/tml}characterization) inherited from {http://www.opengis.net/tml}IdentificationType
    
    # Element {http://www.opengis.net/tml}modelNumber uses Python identifier modelNumber
    __modelNumber = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'modelNumber'), 'modelNumber', '__httpwww_opengis_nettml_CTD_ANON_43_httpwww_opengis_nettmlmodelNumber', False)

    
    modelNumber = property(__modelNumber.value, __modelNumber.set, None, None)

    
    # Element complexity ({http://www.opengis.net/tml}complexity) inherited from {http://www.opengis.net/tml}IdentificationType

    _ElementMap = IdentificationType._ElementMap.copy()
    _ElementMap.update({
        __serialNumber.name() : __serialNumber,
        __ownedBy.name() : __ownedBy,
        __processVersion.name() : __processVersion,
        __manufacture.name() : __manufacture,
        __modelNumber.name() : __modelNumber
    })
    _AttributeMap = IdentificationType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_44 with content type ELEMENT_ONLY
class CTD_ANON_44 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}frequencyResponse uses Python identifier frequencyResponse
    __frequencyResponse = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'frequencyResponse'), 'frequencyResponse', '__httpwww_opengis_nettml_CTD_ANON_44_httpwww_opengis_nettmlfrequencyResponse', True)

    
    frequencyResponse = property(__frequencyResponse.value, __frequencyResponse.set, None, u'one for each dataUnit and for each type of freqResp (carrier, modulation, and powerSpectrialDensity) and each type of plot amp vs freq and phase vs freq (can combine plots onto one as well)')

    
    # Element {http://www.opengis.net/tml}impulseResponse uses Python identifier impulseResponse
    __impulseResponse = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'impulseResponse'), 'impulseResponse', '__httpwww_opengis_nettml_CTD_ANON_44_httpwww_opengis_nettmlimpulseResponse', True)

    
    impulseResponse = property(__impulseResponse.value, __impulseResponse.set, None, u'time domain or frequency domain impulse characteristics for linear time invariant transforms. May have a separate response for each dataUnit and for each type (freq and time).  Or dataUnits within a data Set may share the same response.')

    
    # Element {http://www.opengis.net/tml}steadyStateResponse uses Python identifier steadyStateResponse
    __steadyStateResponse = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'steadyStateResponse'), 'steadyStateResponse', '__httpwww_opengis_nettml_CTD_ANON_44_httpwww_opengis_nettmlsteadyStateResponse', True)

    
    steadyStateResponse = property(__steadyStateResponse.value, __steadyStateResponse.set, None, u'input to output  mapping.  one or more mappings for each dataUnit.  Can have property-property, property-data, or data-property mappings.  property-property-property and property-property-data mappings are also allowed as long as independent property values can be found somewhere.  Separate mappings can be used for different hystersis directions or for non-continuous or broken functions.')

    
    # Element {http://www.opengis.net/tml}cfSubSampling uses Python identifier cfSubSampling
    __cfSubSampling = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling'), 'cfSubSampling', '__httpwww_opengis_nettml_CTD_ANON_44_httpwww_opengis_nettmlcfSubSampling', False)

    
    cfSubSampling = property(__cfSubSampling.value, __cfSubSampling.set, None, u'the CFSubSampling can be used for chipping part of a large dataArry out and for reducing the number of points within an array for which to associate modeling parameters.  there is one sub sampling element set of points for each component structure (col, row, plane).    index numbers of col, row or plane position within the CFs are listed for which corresponding modeling points will be associated.  sample points are separated by commas, ranges are indicated by ... between numbers which indicates a continuous interval for a single sample. interpolation between samples uses logical structure.  ')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_44_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_44_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_44_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')


    _ElementMap = {
        __frequencyResponse.name() : __frequencyResponse,
        __impulseResponse.name() : __impulseResponse,
        __steadyStateResponse.name() : __steadyStateResponse,
        __cfSubSampling.name() : __cfSubSampling
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __name.name() : __name,
        __uid.name() : __uid
    }



# Complex type CTD_ANON_45 with content type ELEMENT_ONLY
class CTD_ANON_45 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}latencyTime uses Python identifier latencyTime
    __latencyTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'latencyTime'), 'latencyTime', '__httpwww_opengis_nettml_CTD_ANON_45_httpwww_opengis_nettmllatencyTime', False)

    
    latencyTime = property(__latencyTime.value, __latencyTime.set, None, u'latency time in seconds (real number).  Time between the input and the output.  Transducer time tags should be corrected to reflect correct input time for receivers and output time for transmitters.  Latency for processes reflects the process delay.  Latency time does not vary over the CF.  Only one value. ')

    
    # Element {http://www.opengis.net/tml}ambiguityTime uses Python identifier ambiguityTime
    __ambiguityTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'ambiguityTime'), 'ambiguityTime', '__httpwww_opengis_nettml_CTD_ANON_45_httpwww_opengis_nettmlambiguityTime', True)

    
    ambiguityTime = property(__ambiguityTime.value, __ambiguityTime.set, None, u'data integration time for each sample in the CF. Each dataunit may have a different time.   This element contains the number of samples in a CF or the number indicated by the noOfSubSampledIndexPoints element in the CFsubSamplingSequence or just one time.  If just one time then the same time applies to all sample in the CF.')

    
    # Element {http://www.opengis.net/tml}cfDuration uses Python identifier cfDuration
    __cfDuration = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'cfDuration'), 'cfDuration', '__httpwww_opengis_nettml_CTD_ANON_45_httpwww_opengis_nettmlcfDuration', False)

    
    cfDuration = property(__cfDuration.value, __cfDuration.set, None, u'time duration of the CF in seconds.  Can also be determined by the CF offset time values by subtracting the smallest offset time from the largest offset time.  Duration does not vary over the CF.  Only one value.')

    
    # Element {http://www.opengis.net/tml}cfTrigger uses Python identifier cfTrigger
    __cfTrigger = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'cfTrigger'), 'cfTrigger', '__httpwww_opengis_nettml_CTD_ANON_45_httpwww_opengis_nettmlcfTrigger', False)

    
    cfTrigger = property(__cfTrigger.value, __cfTrigger.set, None, None)

    
    # Element {http://www.opengis.net/tml}cfOffsetTime uses Python identifier cfOffsetTime
    __cfOffsetTime = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'cfOffsetTime'), 'cfOffsetTime', '__httpwww_opengis_nettml_CTD_ANON_45_httpwww_opengis_nettmlcfOffsetTime', True)

    
    cfOffsetTime = property(__cfOffsetTime.value, __cfOffsetTime.set, None, u'cfOffSetTime contains time offsets for each dataUnit or dataSet in the CF relative to the clock attribute (clk or dateTime) in the data start tag.  contains the number of time values indicated by the numSubSampledIndexPoints in the cfSubSampling child element. or num')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_45_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_45_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_45_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __latencyTime.name() : __latencyTime,
        __ambiguityTime.name() : __ambiguityTime,
        __cfDuration.name() : __cfDuration,
        __cfTrigger.name() : __cfTrigger,
        __cfOffsetTime.name() : __cfOffsetTime
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __uid.name() : __uid,
        __name.name() : __name
    }



# Complex type CTD_ANON_46 with content type ELEMENT_ONLY
class CTD_ANON_46 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}email uses Python identifier email
    __email = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'email'), 'email', '__httpwww_opengis_nettml_CTD_ANON_46_httpwww_opengis_nettmlemail', False)

    
    email = property(__email.value, __email.set, None, None)

    
    # Element {http://www.opengis.net/tml}date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'date'), 'date', '__httpwww_opengis_nettml_CTD_ANON_46_httpwww_opengis_nettmldate', False)

    
    date = property(__date.value, __date.set, None, u'ISO8601 dateTime stamp')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_46_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {http://www.opengis.net/tml}organization uses Python identifier organization
    __organization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'organization'), 'organization', '__httpwww_opengis_nettml_CTD_ANON_46_httpwww_opengis_nettmlorganization', False)

    
    organization = property(__organization.value, __organization.set, None, None)

    
    # Element {http://www.opengis.net/tml}phone uses Python identifier phone
    __phone = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'phone'), 'phone', '__httpwww_opengis_nettml_CTD_ANON_46_httpwww_opengis_nettmlphone', False)

    
    phone = property(__phone.value, __phone.set, None, None)


    _ElementMap = {
        __email.name() : __email,
        __date.name() : __date,
        __name.name() : __name,
        __organization.name() : __organization,
        __phone.name() : __phone
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_47 with content type ELEMENT_ONLY
class CTD_ANON_47 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_47_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, u'name of the object')

    
    # Element {http://www.opengis.net/tml}dirIndirSubj uses Python identifier dirIndirSubj
    __dirIndirSubj = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dirIndirSubj'), 'dirIndirSubj', '__httpwww_opengis_nettml_CTD_ANON_47_httpwww_opengis_nettmldirIndirSubj', False)

    
    dirIndirSubj = property(__dirIndirSubj.value, __dirIndirSubj.set, None, u'if objType is subject then identify if direct or indirect subject.  Allowed values: direct, indirect.  Default is direct.')

    
    # Element {http://www.opengis.net/tml}objType uses Python identifier objType
    __objType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'objType'), 'objType', '__httpwww_opengis_nettml_CTD_ANON_47_httpwww_opengis_nettmlobjType', False)

    
    objType = property(__objType.value, __objType.set, None, u'identify object as a transducer or a subject. Allowed Values: subject, transducer. Default: subject')

    
    # Element {http://www.opengis.net/tml}objUidRef uses Python identifier objUidRef
    __objUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'objUidRef'), 'objUidRef', '__httpwww_opengis_nettml_CTD_ANON_47_httpwww_opengis_nettmlobjUidRef', False)

    
    objUidRef = property(__objUidRef.value, __objUidRef.set, None, u'UID of the subject (or probable subject).  local id of the subject if multiple ids are used to associate with each cell of  the logical structure.  Sequence of values is the same as the sequence in the data (logical data structure)')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_47_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name_
    __name_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name_', '__httpwww_opengis_nettml_CTD_ANON_47_name', pyxb.binding.datatypes.string)
    
    name_ = property(__name_.value, __name_.set, None, u'short descriptive name of element')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_47_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')


    _ElementMap = {
        __name.name() : __name,
        __dirIndirSubj.name() : __dirIndirSubj,
        __objType.name() : __objType,
        __objUidRef.name() : __objUidRef
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __name_.name() : __name_,
        __uid.name() : __uid
    }



# Complex type CTD_ANON_48 with content type ELEMENT_ONLY
class CTD_ANON_48 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}headerAttrib uses Python identifier headerAttrib
    __headerAttrib = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'headerAttrib'), 'headerAttrib', '__httpwww_opengis_nettml_CTD_ANON_48_httpwww_opengis_nettmlheaderAttrib', True)

    
    headerAttrib = property(__headerAttrib.value, __headerAttrib.set, None, u'ref, reference, dateTime, contents and ismClass attributes will be encoded and handled as "string" type')


    _ElementMap = {
        __headerAttrib.name() : __headerAttrib
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_49 with content type ELEMENT_ONLY
class CTD_ANON_49 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}dataValue uses Python identifier dataValue
    __dataValue = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataValue'), 'dataValue', '__httpwww_opengis_nettml_CTD_ANON_49_httpwww_opengis_nettmldataValue', False)

    
    dataValue = property(__dataValue.value, __dataValue.set, None, u'fixed or forced input value not.  single value or array defined by logical data structure ')

    
    # Element {http://www.opengis.net/tml}inputIdent uses Python identifier inputIdent
    __inputIdent = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'inputIdent'), 'inputIdent', '__httpwww_opengis_nettml_CTD_ANON_49_httpwww_opengis_nettmlinputIdent', False)

    
    inputIdent = property(__inputIdent.value, __inputIdent.set, None, None)

    
    # Element {http://www.opengis.net/tml}logicalDataStructure uses Python identifier logicalDataStructure
    __logicalDataStructure = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'logicalDataStructure'), 'logicalDataStructure', '__httpwww_opengis_nettml_CTD_ANON_49_httpwww_opengis_nettmllogicalDataStructure', True)

    
    logicalDataStructure = property(__logicalDataStructure.value, __logicalDataStructure.set, None, u'the logical structure of data (i.e. of the characteristic frame).  This is not necessarily the structure or order that data is communicated in.  The transmission order is defined in the cluster description.  The transmission order is defined relative to the logical order.')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_49_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_49_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_49_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __dataValue.name() : __dataValue,
        __inputIdent.name() : __inputIdent,
        __logicalDataStructure.name() : __logicalDataStructure
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __uid.name() : __uid,
        __name.name() : __name
    }



# Complex type CTD_ANON_50 with content type ELEMENT_ONLY
class CTD_ANON_50 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}subject uses Python identifier subject
    __subject = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'subject'), 'subject', '__httpwww_opengis_nettml_CTD_ANON_50_httpwww_opengis_nettmlsubject', True)

    
    subject = property(__subject.value, __subject.set, None, u'This is the subject (object, thing) that relates to the phenomenon (property) that is affected or detected by the transducer. The relation between a subject and transducer data or subject and subject is described in the relationship element. An empty subject tag in a data stream indicates that this object is no longer a part of the system')


    _ElementMap = {
        __subject.name() : __subject
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_51 with content type ELEMENT_ONLY
class CTD_ANON_51 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}transducer uses Python identifier transducer
    __transducer = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'transducer'), 'transducer', '__httpwww_opengis_nettml_CTD_ANON_51_httpwww_opengis_nettmltransducer', True)

    
    transducer = property(__transducer.value, __transducer.set, None, u'A transducer can be a stand alone object or part of a system.  An empty transducer tag in a data stream indicates that this transducer is no longer a part of the system')


    _ElementMap = {
        __transducer.name() : __transducer
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_52 with content type ELEMENT_ONLY
class CTD_ANON_52 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_52_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {http://www.opengis.net/tml}dataUidRef uses Python identifier dataUidRef
    __dataUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), 'dataUidRef', '__httpwww_opengis_nettml_CTD_ANON_52_httpwww_opengis_nettmldataUidRef', False)

    
    dataUidRef = property(__dataUidRef.value, __dataUidRef.set, None, u'UID of the data (live or archived).  Archived data streams will have a UID indicative of the data source, time, and clk count of the start. ')

    
    # Element {http://www.opengis.net/tml}value uses Python identifier value_
    __value = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'value'), 'value_', '__httpwww_opengis_nettml_CTD_ANON_52_httpwww_opengis_nettmlvalue', False)

    
    value_ = property(__value.value, __value.set, None, None)

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_52_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name_
    __name_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name_', '__httpwww_opengis_nettml_CTD_ANON_52_name', pyxb.binding.datatypes.string)
    
    name_ = property(__name_.value, __name_.set, None, u'short descriptive name of element')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_52_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')


    _ElementMap = {
        __name.name() : __name,
        __dataUidRef.name() : __dataUidRef,
        __value.name() : __value
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __name_.name() : __name_,
        __uid.name() : __uid
    }



# Complex type CTD_ANON_53 with content type ELEMENT_ONLY
class CTD_ANON_53 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}code uses Python identifier code
    __code = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'code'), 'code', '__httpwww_opengis_nettml_CTD_ANON_53_httpwww_opengis_nettmlcode', False)

    
    code = property(__code.value, __code.set, None, u'computer code of the transfer process from input to output')

    
    # Element {http://www.opengis.net/tml}propValues uses Python identifier propValues
    __propValues = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'propValues'), 'propValues', '__httpwww_opengis_nettml_CTD_ANON_53_httpwww_opengis_nettmlpropValues', True)

    
    propValues = property(__propValues.value, __propValues.set, None, u'values for the physical property (phenomenon) axis of the input output transfer function')

    
    # Element {http://www.opengis.net/tml}responseParameters uses Python identifier responseParameters
    __responseParameters = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'responseParameters'), 'responseParameters', '__httpwww_opengis_nettml_CTD_ANON_53_httpwww_opengis_nettmlresponseParameters', False)

    
    responseParameters = property(__responseParameters.value, __responseParameters.set, None, None)

    
    # Element {http://www.opengis.net/tml}dataValues uses Python identifier dataValues
    __dataValues = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataValues'), 'dataValues', '__httpwww_opengis_nettml_CTD_ANON_53_httpwww_opengis_nettmldataValues', True)

    
    dataValues = property(__dataValues.value, __dataValues.set, None, u'values for the data axis of the input output transfer function')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_53_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_53_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_53_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')


    _ElementMap = {
        __code.name() : __code,
        __propValues.name() : __propValues,
        __responseParameters.name() : __responseParameters,
        __dataValues.name() : __dataValues
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __name.name() : __name,
        __uid.name() : __uid
    }



# Complex type CTD_ANON_54 with content type ELEMENT_ONLY
class CTD_ANON_54 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}tapPointUidRef uses Python identifier tapPointUidRef
    __tapPointUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'tapPointUidRef'), 'tapPointUidRef', '__httpwww_opengis_nettml_CTD_ANON_54_httpwww_opengis_nettmltapPointUidRef', True)

    
    tapPointUidRef = property(__tapPointUidRef.value, __tapPointUidRef.set, None, u'dataUidRef of the tap point in the system to which this cluster corresponds.  UID of the transducer, process input process output, or connection node from which or to which this cluster relates.  This is the UID used in the data header (i.e. reference attribute in data start tag).  Is some cases a data in a single cluster may come from multiple dataUid tap points.')

    
    # Element {http://www.opengis.net/tml}localID uses Python identifier localID
    __localID = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'localID'), 'localID', '__httpwww_opengis_nettml_CTD_ANON_54_httpwww_opengis_nettmllocalID', False)

    
    localID = property(__localID.value, __localID.set, None, u'short ID used in the data header (i.e. ref attribute in data start tag)')


    _ElementMap = {
        __tapPointUidRef.name() : __tapPointUidRef,
        __localID.name() : __localID
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_55 with content type ELEMENT_ONLY
class CTD_ANON_55 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}intraCfInterpolate uses Python identifier intraCfInterpolate
    __intraCfInterpolate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'intraCfInterpolate'), 'intraCfInterpolate', '__httpwww_opengis_nettml_CTD_ANON_55_httpwww_opengis_nettmlintraCfInterpolate', False)

    
    intraCfInterpolate = property(__intraCfInterpolate.value, __intraCfInterpolate.set, None, u'Allowed values: continuous, discrete, lastValue, returnToZero.  how to interpolate between data values within a CF.  default continuous')

    
    # Element {http://www.opengis.net/tml}proportional uses Python identifier proportional
    __proportional = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'proportional'), 'proportional', '__httpwww_opengis_nettml_CTD_ANON_55_httpwww_opengis_nettmlproportional', False)

    
    proportional = property(__proportional.value, __proportional.set, None, u'For uncalibrated responses is the output proportional to the input? true of false. Mult factors can also reflect prop or inversely prop for calibrated responses. Default: true.')

    
    # Element {http://www.opengis.net/tml}codePlot uses Python identifier codePlot
    __codePlot = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'codePlot'), 'codePlot', '__httpwww_opengis_nettml_CTD_ANON_55_httpwww_opengis_nettmlcodePlot', False)

    
    codePlot = property(__codePlot.value, __codePlot.set, None, u'Allowed values code, plot. Default: plot')

    
    # Element {http://www.opengis.net/tml}linear uses Python identifier linear
    __linear = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'linear'), 'linear', '__httpwww_opengis_nettml_CTD_ANON_55_httpwww_opengis_nettmllinear', False)

    
    linear = property(__linear.value, __linear.set, None, u'allowed values: true or false.  do not need explicit Phen plot values if linear is true. Phen and data mult and offset can be used if there are no limits.  default true')

    
    # Element {http://www.opengis.net/tml}hysteresisDirection uses Python identifier hysteresisDirection
    __hysteresisDirection = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'hysteresisDirection'), 'hysteresisDirection', '__httpwww_opengis_nettml_CTD_ANON_55_httpwww_opengis_nettmlhysteresisDirection', False)

    
    hysteresisDirection = property(__hysteresisDirection.value, __hysteresisDirection.set, None, u'allowed values: increasing, decreasing, both.  default both')

    
    # Element {http://www.opengis.net/tml}invertability uses Python identifier invertability
    __invertability = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'invertability'), 'invertability', '__httpwww_opengis_nettml_CTD_ANON_55_httpwww_opengis_nettmlinvertability', False)

    
    invertability = property(__invertability.value, __invertability.set, None, u'a process input can be determined from its output. Allowed Values: true, false.  default true')

    
    # Element {http://www.opengis.net/tml}interCfInterpolate uses Python identifier interCfInterpolate
    __interCfInterpolate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'interCfInterpolate'), 'interCfInterpolate', '__httpwww_opengis_nettml_CTD_ANON_55_httpwww_opengis_nettmlinterCfInterpolate', False)

    
    interCfInterpolate = property(__interCfInterpolate.value, __interCfInterpolate.set, None, u"Allowed values: continuous, discrete, lastValue, returnToZero.  how to interpolate between corresponding data values between adjacent CF's.  default is continuous")

    
    # Element {http://www.opengis.net/tml}calibrated uses Python identifier calibrated
    __calibrated = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'calibrated'), 'calibrated', '__httpwww_opengis_nettml_CTD_ANON_55_httpwww_opengis_nettmlcalibrated', False)

    
    calibrated = property(__calibrated.value, __calibrated.set, None, u'Is response calibrated, or is response a relative reading? true of false. Default: true')

    
    # Element {http://www.opengis.net/tml}timeInvariant uses Python identifier timeInvariant
    __timeInvariant = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'timeInvariant'), 'timeInvariant', '__httpwww_opengis_nettml_CTD_ANON_55_httpwww_opengis_nettmltimeInvariant', False)

    
    timeInvariant = property(__timeInvariant.value, __timeInvariant.set, None, u'a time shift in the input only results in a time shift in the output. Allowed Values: true, false.  default true')


    _ElementMap = {
        __intraCfInterpolate.name() : __intraCfInterpolate,
        __proportional.name() : __proportional,
        __codePlot.name() : __codePlot,
        __linear.name() : __linear,
        __hysteresisDirection.name() : __hysteresisDirection,
        __invertability.name() : __invertability,
        __interCfInterpolate.name() : __interCfInterpolate,
        __calibrated.name() : __calibrated,
        __timeInvariant.name() : __timeInvariant
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_56 with content type ELEMENT_ONLY
class CTD_ANON_56 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}propToPropRelation uses Python identifier propToPropRelation
    __propToPropRelation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'propToPropRelation'), 'propToPropRelation', '__httpwww_opengis_nettml_CTD_ANON_56_httpwww_opengis_nettmlpropToPropRelation', True)

    
    propToPropRelation = property(__propToPropRelation.value, __propToPropRelation.set, None, u'Property to property relation or phenomenon to phenomenon relation. transmitter to receiver, Ambient to receiver, Example: thermal to voltage transducer connected to a voltage to data transducer.  example optical filter on the front of an optical camera lens')

    
    # Element {http://www.opengis.net/tml}positionRelation uses Python identifier positionRelation
    __positionRelation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'positionRelation'), 'positionRelation', '__httpwww_opengis_nettml_CTD_ANON_56_httpwww_opengis_nettmlpositionRelation', True)

    
    positionRelation = property(__positionRelation.value, __positionRelation.set, None, u'For describing positional relations of subjects external to a system.  An empty posRelation tag in a data indicates that this uidRef relation is no longer exist')

    
    # Element {http://www.opengis.net/tml}objToObjRelation uses Python identifier objToObjRelation
    __objToObjRelation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'objToObjRelation'), 'objToObjRelation', '__httpwww_opengis_nettml_CTD_ANON_56_httpwww_opengis_nettmlobjToObjRelation', True)

    
    objToObjRelation = property(__objToObjRelation.value, __objToObjRelation.set, None, u'This relation describes object to object relations. Attaching a transducer to an object (object is a subject or a transducer) (i.e. dangle, where the only thing the transducer interfaces to is that subject. (cant different individual data many measures with many individual subjects, see objToData). The transducer to transducers relation does not include phenomenon to phenomenon connections, see dataToData')

    
    # Element {http://www.opengis.net/tml}timeRelation uses Python identifier timeRelation
    __timeRelation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'timeRelation'), 'timeRelation', '__httpwww_opengis_nettml_CTD_ANON_56_httpwww_opengis_nettmltimeRelation', True)

    
    timeRelation = property(__timeRelation.value, __timeRelation.set, None, u'Identifies the absolute time reference for each sysClk.  Default is any time reference in a cluster represents absolute time relating to the corresponding clock value.  An empty timeRelation tag in a data stream indicates that this uidRef relation is no longer a part of the system')

    
    # Element {http://www.opengis.net/tml}objToDataRelation uses Python identifier objToDataRelation
    __objToDataRelation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'objToDataRelation'), 'objToDataRelation', '__httpwww_opengis_nettml_CTD_ANON_56_httpwww_opengis_nettmlobjToDataRelation', True)

    
    objToDataRelation = property(__objToDataRelation.value, __objToDataRelation.set, None, u'Connects transducer to bindUids.  Associate transducer data to a (remote) object.  This may occur after data acquisition. An object is either a transducer, subject or their properties.    Many subjects may be related to data in a dataArray. The objects can be related to data units, sets and arrays to subjects.  ')

    
    # Element {http://www.opengis.net/tml}dataToDataRelation uses Python identifier dataToDataRelation
    __dataToDataRelation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataToDataRelation'), 'dataToDataRelation', '__httpwww_opengis_nettml_CTD_ANON_56_httpwww_opengis_nettmldataToDataRelation', True)

    
    dataToDataRelation = property(__dataToDataRelation.value, __dataToDataRelation.set, None, u'Connects bindUIDs to processes. connects outputs to inputs. transducer data to processes and processes to processes.  An empty connect tag in a data stream indicates that this UID relation is no longer a part of the system. Example of data to data relation.  attaching a process to monitor the state of the gain parameter on the steady state response through a bindUID point.  ')


    _ElementMap = {
        __propToPropRelation.name() : __propToPropRelation,
        __positionRelation.name() : __positionRelation,
        __objToObjRelation.name() : __objToObjRelation,
        __timeRelation.name() : __timeRelation,
        __objToDataRelation.name() : __objToDataRelation,
        __dataToDataRelation.name() : __dataToDataRelation
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_57 with content type ELEMENT_ONLY
class CTD_ANON_57 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_57_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {http://www.opengis.net/tml}phone uses Python identifier phone
    __phone = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'phone'), 'phone', '__httpwww_opengis_nettml_CTD_ANON_57_httpwww_opengis_nettmlphone', False)

    
    phone = property(__phone.value, __phone.set, None, None)

    
    # Element {http://www.opengis.net/tml}date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'date'), 'date', '__httpwww_opengis_nettml_CTD_ANON_57_httpwww_opengis_nettmldate', False)

    
    date = property(__date.value, __date.set, None, u'ISO8601 dateTime stamp')

    
    # Element {http://www.opengis.net/tml}email uses Python identifier email
    __email = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'email'), 'email', '__httpwww_opengis_nettml_CTD_ANON_57_httpwww_opengis_nettmlemail', False)

    
    email = property(__email.value, __email.set, None, None)

    
    # Element {http://www.opengis.net/tml}organization uses Python identifier organization
    __organization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'organization'), 'organization', '__httpwww_opengis_nettml_CTD_ANON_57_httpwww_opengis_nettmlorganization', False)

    
    organization = property(__organization.value, __organization.set, None, None)


    _ElementMap = {
        __name.name() : __name,
        __phone.name() : __phone,
        __date.name() : __date,
        __email.name() : __email,
        __organization.name() : __organization
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_58 with content type ELEMENT_ONLY
class CTD_ANON_58 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}clusterSize uses Python identifier clusterSize
    __clusterSize = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'clusterSize'), 'clusterSize', '__httpwww_opengis_nettml_CTD_ANON_58_httpwww_opengis_nettmlclusterSize', False)

    
    clusterSize = property(__clusterSize.value, __clusterSize.set, None, u'Integer number of bytes in Cluster')

    
    # Element {http://www.opengis.net/tml}direction uses Python identifier direction
    __direction = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'direction'), 'direction', '__httpwww_opengis_nettml_CTD_ANON_58_httpwww_opengis_nettmldirection', False)

    
    direction = property(__direction.value, __direction.set, None, u'Allowed Values: fromSystem, toSystem.  default fromSystem')

    
    # Element {http://www.opengis.net/tml}complexity uses Python identifier complexity
    __complexity = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'complexity'), 'complexity', '__httpwww_opengis_nettml_CTD_ANON_58_httpwww_opengis_nettmlcomplexity', False)

    
    complexity = property(__complexity.value, __complexity.set, None, u'indication of the complexity of handling this data. Allowed Values: 1A - 1F, 2A -2F, 3A - 3F, 4A - 4F, 5A - 5F.  default 1A')

    
    # Element {http://www.opengis.net/tml}clusterType uses Python identifier clusterType
    __clusterType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'clusterType'), 'clusterType', '__httpwww_opengis_nettml_CTD_ANON_58_httpwww_opengis_nettmlclusterType', False)

    
    clusterType = property(__clusterType.value, __clusterType.set, None, u'Allowed values: binary, packedXML.  verboseXML. default binary')


    _ElementMap = {
        __clusterSize.name() : __clusterSize,
        __direction.name() : __direction,
        __complexity.name() : __complexity,
        __clusterType.name() : __clusterType
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_59 with content type ELEMENT_ONLY
class CTD_ANON_59 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}dataUidRef uses Python identifier dataUidRef
    __dataUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), 'dataUidRef', '__httpwww_opengis_nettml_CTD_ANON_59_httpwww_opengis_nettmldataUidRef', False)

    
    dataUidRef = property(__dataUidRef.value, __dataUidRef.set, None, u'UID of the data reference.  Archived data streams will have a UID indicative of the data source, time, and clk count of the start. ')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_59_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_59_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_59_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute name uses Python identifier name_
    __name_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name_', '__httpwww_opengis_nettml_CTD_ANON_59_name', pyxb.binding.datatypes.string)
    
    name_ = property(__name_.value, __name_.set, None, u'short descriptive name of element')


    _ElementMap = {
        __dataUidRef.name() : __dataUidRef,
        __name.name() : __name
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __uid.name() : __uid,
        __name_.name() : __name_
    }



# Complex type CTD_ANON_60 with content type ELEMENT_ONLY
class CTD_ANON_60 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}timeCoordinate uses Python identifier timeCoordinate
    __timeCoordinate = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'timeCoordinate'), 'timeCoordinate', '__httpwww_opengis_nettml_CTD_ANON_60_httpwww_opengis_nettmltimeCoordinate', True)

    
    timeCoordinate = property(__timeCoordinate.value, __timeCoordinate.set, None, None)

    
    # Element {http://www.opengis.net/tml}timeReference uses Python identifier timeReference
    __timeReference = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'timeReference'), 'timeReference', '__httpwww_opengis_nettml_CTD_ANON_60_httpwww_opengis_nettmltimeReference', False)

    
    timeReference = property(__timeReference.value, __timeReference.set, None, u'time Datum.  Allowed Values: UTC, other,  Default UTC.')

    
    # Element {http://www.opengis.net/tml}sysClkUidRef uses Python identifier sysClkUidRef
    __sysClkUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'sysClkUidRef'), 'sysClkUidRef', '__httpwww_opengis_nettml_CTD_ANON_60_httpwww_opengis_nettmlsysClkUidRef', False)

    
    sysClkUidRef = property(__sysClkUidRef.value, __sysClkUidRef.set, None, u'UID of the sysClk.  Default: Uid of system clock which transducer is contained in.')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_60_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_60_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_60_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __timeCoordinate.name() : __timeCoordinate,
        __timeReference.name() : __timeReference,
        __sysClkUidRef.name() : __sysClkUidRef
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __uid.name() : __uid,
        __name.name() : __name
    }



# Complex type CTD_ANON_61 with content type SIMPLE
class CTD_ANON_61 (BindType):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is BindType
    
    # Attribute bindUid inherited from {http://www.opengis.net/tml}BindType
    
    # Attribute bindUidRef inherited from {http://www.opengis.net/tml}BindType

    _ElementMap = BindType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BindType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_62 with content type ELEMENT_ONLY
class CTD_ANON_62 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}propagationMedium uses Python identifier propagationMedium
    __propagationMedium = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'propagationMedium'), 'propagationMedium', '__httpwww_opengis_nettml_CTD_ANON_62_httpwww_opengis_nettmlpropagationMedium', True)

    
    propagationMedium = property(__propagationMedium.value, __propagationMedium.set, None, u'If the P-to-P interface has a distance between them, then this describes the medium in which the energy propagates.  Allowed values: vacuum, air, water.  default air')

    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_62_httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'connection or node UID of the property relationship')

    
    # Element {http://www.opengis.net/tml}relationDescription uses Python identifier relationDescription
    __relationDescription = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'relationDescription'), 'relationDescription', '__httpwww_opengis_nettml_CTD_ANON_62_httpwww_opengis_nettmlrelationDescription', False)

    
    relationDescription = property(__relationDescription.value, __relationDescription.set, None, u'longer description of  the property relation')

    
    # Element {http://www.opengis.net/tml}propagationMechanism uses Python identifier propagationMechanism
    __propagationMechanism = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'propagationMechanism'), 'propagationMechanism', '__httpwww_opengis_nettml_CTD_ANON_62_httpwww_opengis_nettmlpropagationMechanism', True)

    
    propagationMechanism = property(__propagationMechanism.value, __propagationMechanism.set, None, u'If the P-to-P interface has a distance between them, then this describes the mechanism in which the energy propagates.  Allowed values: radiation, conduction, convection, osmosis.  default radiation')

    
    # Element {http://www.opengis.net/tml}propUidRef uses Python identifier propUidRef
    __propUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'propUidRef'), 'propUidRef', '__httpwww_opengis_nettml_CTD_ANON_62_httpwww_opengis_nettmlpropUidRef', True)

    
    propUidRef = property(__propUidRef.value, __propUidRef.set, None, u'uidRef of the property or phenomenon')

    
    # Attribute uid uses Python identifier uid_
    __uid_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid_', '__httpwww_opengis_nettml_CTD_ANON_62_uid', pyxb.binding.datatypes.anyURI)
    
    uid_ = property(__uid_.value, __uid_.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_62_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_62_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __propagationMedium.name() : __propagationMedium,
        __uid.name() : __uid,
        __relationDescription.name() : __relationDescription,
        __propagationMechanism.name() : __propagationMechanism,
        __propUidRef.name() : __propUidRef
    }
    _AttributeMap = {
        __uid_.name() : __uid_,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    }



# Complex type CTD_ANON_63 with content type ELEMENT_ONLY
class CTD_ANON_63 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}otherRelations uses Python identifier otherRelations
    __otherRelations = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'otherRelations'), 'otherRelations', '__httpwww_opengis_nettml_CTD_ANON_63_httpwww_opengis_nettmlotherRelations', True)

    
    otherRelations = property(__otherRelations.value, __otherRelations.set, None, None)

    
    # Element {http://www.opengis.net/tml}objToObjRelation uses Python identifier objToObjRelation
    __objToObjRelation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'objToObjRelation'), 'objToObjRelation', '__httpwww_opengis_nettml_CTD_ANON_63_httpwww_opengis_nettmlobjToObjRelation', True)

    
    objToObjRelation = property(__objToObjRelation.value, __objToObjRelation.set, None, u'This relation describes object to object relations. Attaching a transducer to an object (object is a subject or a transducer) (i.e. dangle, where the only thing the transducer interfaces to is that subject. (cant different individual data many measures with many individual subjects, see objToData). The transducer to transducers relation does not include phenomenon to phenomenon connections, see dataToData')

    
    # Element {http://www.opengis.net/tml}objToDataRelation uses Python identifier objToDataRelation
    __objToDataRelation = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'objToDataRelation'), 'objToDataRelation', '__httpwww_opengis_nettml_CTD_ANON_63_httpwww_opengis_nettmlobjToDataRelation', True)

    
    objToDataRelation = property(__objToDataRelation.value, __objToDataRelation.set, None, u'Connects transducer to bindUids.  Associate transducer data to a (remote) object.  This may occur after data acquisition. An object is either a transducer, subject or their properties.    Many subjects may be related to data in a dataArray. The objects can be related to data units, sets and arrays to subjects.  ')


    _ElementMap = {
        __otherRelations.name() : __otherRelations,
        __objToObjRelation.name() : __objToObjRelation,
        __objToDataRelation.name() : __objToDataRelation
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_64 with content type ELEMENT_ONLY
class CTD_ANON_64 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}dataType uses Python identifier dataType
    __dataType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataType'), 'dataType', '__httpwww_opengis_nettml_CTD_ANON_64_httpwww_opengis_nettmldataType', False)

    
    dataType = property(__dataType.value, __dataType.set, None, u'Allowed values: text, number.  Default is number. ')

    
    # Element {http://www.opengis.net/tml}encode uses Python identifier encode
    __encode = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'encode'), 'encode', '__httpwww_opengis_nettml_CTD_ANON_64_httpwww_opengis_nettmlencode', False)

    
    encode = property(__encode.value, __encode.set, None, u'Allowed values: ucs16, utf8, signInt, unsignInt, real,  bcd.  default unsignInt. ')

    
    # Element {http://www.opengis.net/tml}dataUnitFieldSize uses Python identifier dataUnitFieldSize
    __dataUnitFieldSize = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUnitFieldSize'), 'dataUnitFieldSize', '__httpwww_opengis_nettml_CTD_ANON_64_httpwww_opengis_nettmldataUnitFieldSize', False)

    
    dataUnitFieldSize = property(__dataUnitFieldSize.value, __dataUnitFieldSize.set, None, None)

    
    # Element {http://www.opengis.net/tml}numBase uses Python identifier numBase
    __numBase = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numBase'), 'numBase', '__httpwww_opengis_nettml_CTD_ANON_64_httpwww_opengis_nettmlnumBase', False)

    
    numBase = property(__numBase.value, __numBase.set, None, u'when numbers are encoded as text the number base must be understood.  Allowed values: 2, 8, 10, 16, 32, 64, 128.  default 10')

    
    # Element {http://www.opengis.net/tml}headerAttribName uses Python identifier headerAttribName
    __headerAttribName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'headerAttribName'), 'headerAttribName', '__httpwww_opengis_nettml_CTD_ANON_64_httpwww_opengis_nettmlheaderAttribName', False)

    
    headerAttribName = property(__headerAttribName.value, __headerAttribName.set, None, u'Allowed values: ref, clk, reference, dateTime, contents, seq, total, ismClass. Default ref')

    
    # Element {http://www.opengis.net/tml}endian uses Python identifier endian
    __endian = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'endian'), 'endian', '__httpwww_opengis_nettml_CTD_ANON_64_httpwww_opengis_nettmlendian', False)

    
    endian = property(__endian.value, __endian.set, None, u'Allowed values: big, little.  default little')

    
    # Element {http://www.opengis.net/tml}handleAsType uses Python identifier handleAsType
    __handleAsType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'handleAsType'), 'handleAsType', '__httpwww_opengis_nettml_CTD_ANON_64_httpwww_opengis_nettmlhandleAsType', False)

    
    handleAsType = property(__handleAsType.value, __handleAsType.set, None, u'how should the text or number be handled in the client application.  Allowed values: anuURI, boolean, byte, double, float, short, string, int, integer, long, nonNegativeInteger, nonPositiveInteger, positiveInteger,  unsignedByte, unsignedInt, unsignedShort, unsignedLong.')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_64_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_64_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_64_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __dataType.name() : __dataType,
        __encode.name() : __encode,
        __dataUnitFieldSize.name() : __dataUnitFieldSize,
        __numBase.name() : __numBase,
        __headerAttribName.name() : __headerAttribName,
        __endian.name() : __endian,
        __handleAsType.name() : __handleAsType
    }
    _AttributeMap = {
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    }



# Complex type CTD_ANON_65 with content type ELEMENT_ONLY
class CTD_ANON_65 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}absTimeUidRef uses Python identifier absTimeUidRef
    __absTimeUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'absTimeUidRef'), 'absTimeUidRef', '__httpwww_opengis_nettml_CTD_ANON_65_httpwww_opengis_nettmlabsTimeUidRef', True)

    
    absTimeUidRef = property(__absTimeUidRef.value, __absTimeUidRef.set, None, u'dataUid reference of the sensor measurements providing the absolute time reference.')

    
    # Element {http://www.opengis.net/tml}timeCoordType uses Python identifier timeCoordType
    __timeCoordType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'timeCoordType'), 'timeCoordType', '__httpwww_opengis_nettml_CTD_ANON_65_httpwww_opengis_nettmltimeCoordType', False)

    
    timeCoordType = property(__timeCoordType.value, __timeCoordType.set, None, u'Allowed values: dateTime,  year, mo, day, hour, min, sec. Default: dateTime (ISO 8601)')


    _ElementMap = {
        __absTimeUidRef.name() : __absTimeUidRef,
        __timeCoordType.name() : __timeCoordType
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_66 with content type ELEMENT_ONLY
class CTD_ANON_66 (ValueType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is ValueType
    
    # Element {http://www.opengis.net/tml}direction uses Python identifier direction
    __direction = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'direction'), 'direction', '__httpwww_opengis_nettml_CTD_ANON_66_httpwww_opengis_nettmldirection', True)

    
    direction = property(__direction.value, __direction.set, None, u'if the physical property (phenomenon) had a direction associated with it such as torque or force. direction relative to the transducer reference system.  Allowed Values: horizontal, vertical, +xTranslation, -xTranslation, +yTranslation, -yTranslation, +zTranslation, -zTranslation, +alpha, -alpha, +beta, -beta, +rhoTranslation, -rhoTranslation, +latTranslation, -latTranslation, +longTranslation\n-longTranslation, +altTranslation, -altTranslation, +omegaRotation, -omegaRotation, +phiRotation, -phiRotation, +kappaRotation, -kappaRotation, none Default: none')

    
    # Element {http://www.opengis.net/tml}propQualifier uses Python identifier propQualifier
    __propQualifier = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'propQualifier'), 'propQualifier', '__httpwww_opengis_nettml_CTD_ANON_66_httpwww_opengis_nettmlpropQualifier', True)

    
    propQualifier = property(__propQualifier.value, __propQualifier.set, None, u'Qualifier for the property.  From Qualifier Dictionary.  e.g. aveValue, rmsValue, rssValue, instValue, accumulatedValue, rateOfChange, range, min, max...')

    
    # Element values ({http://www.opengis.net/tml}values) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element fcnInterpol ({http://www.opengis.net/tml}fcnInterpol) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element {http://www.opengis.net/tml}variableName uses Python identifier variableName
    __variableName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'variableName'), 'variableName', '__httpwww_opengis_nettml_CTD_ANON_66_httpwww_opengis_nettmlvariableName', True)

    
    variableName = property(__variableName.value, __variableName.set, None, u'Name of mathematical term used in the transformation equations.  ')

    
    # Element mult ({http://www.opengis.net/tml}mult) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element {http://www.opengis.net/tml}propName uses Python identifier propName
    __propName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'propName'), 'propName', '__httpwww_opengis_nettml_CTD_ANON_66_httpwww_opengis_nettmlpropName', True)

    
    propName = property(__propName.value, __propName.set, None, u'from Physical Property (Phenomenon) Dictionary')

    
    # Element {http://www.opengis.net/tml}UOM uses Python identifier UOM
    __UOM = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'UOM'), 'UOM', '__httpwww_opengis_nettml_CTD_ANON_66_httpwww_opengis_nettmlUOM', True)

    
    UOM = property(__UOM.value, __UOM.set, None, u'From Units Of Measure Dictionary (SI Units)')

    
    # Element valueDataType ({http://www.opengis.net/tml}valueDataType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element {http://www.opengis.net/tml}calibProp uses Python identifier calibProp
    __calibProp = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'calibProp'), 'calibProp', '__httpwww_opengis_nettml_CTD_ANON_66_httpwww_opengis_nettmlcalibProp', True)

    
    calibProp = property(__calibProp.value, __calibProp.set, None, u'If a calibrated source is available this elements identifies the calibration level or points (bindUID) to the calibrated sensor measuring the source.  This is used for post correcting relative readings Default: none')

    
    # Element offset ({http://www.opengis.net/tml}offset) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element accuracy ({http://www.opengis.net/tml}accuracy) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element numValues ({http://www.opengis.net/tml}numValues) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element arrayType ({http://www.opengis.net/tml}arrayType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element {http://www.opengis.net/tml}inputOutput uses Python identifier inputOutput
    __inputOutput = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'inputOutput'), 'inputOutput', '__httpwww_opengis_nettml_CTD_ANON_66_httpwww_opengis_nettmlinputOutput', True)

    
    inputOutput = property(__inputOutput.value, __inputOutput.set, None, u'Is the physical property (phenomenon) the input or output for this dataUnit.  Allowed values: input, output.  Default: input')

    
    # Attribute uidRef inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uid inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute name inherited from {http://www.opengis.net/tml}ValueType

    _ElementMap = ValueType._ElementMap.copy()
    _ElementMap.update({
        __direction.name() : __direction,
        __propQualifier.name() : __propQualifier,
        __variableName.name() : __variableName,
        __propName.name() : __propName,
        __UOM.name() : __UOM,
        __calibProp.name() : __calibProp,
        __inputOutput.name() : __inputOutput
    })
    _AttributeMap = ValueType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_67 with content type ELEMENT_ONLY
class CTD_ANON_67 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}beginTextDelimiter uses Python identifier beginTextDelimiter
    __beginTextDelimiter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'beginTextDelimiter'), 'beginTextDelimiter', '__httpwww_opengis_nettml_CTD_ANON_67_httpwww_opengis_nettmlbeginTextDelimiter', False)

    
    beginTextDelimiter = property(__beginTextDelimiter.value, __beginTextDelimiter.set, None, u'delimiter used to separate variable size dataUnits in cluster when encode is text (utf or ucs). default delimiter is none. empty tag means none.')

    
    # Element {http://www.opengis.net/tml}numSigBits uses Python identifier numSigBits
    __numSigBits = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numSigBits'), 'numSigBits', '__httpwww_opengis_nettml_CTD_ANON_67_httpwww_opengis_nettmlnumSigBits', False)

    
    numSigBits = property(__numSigBits.value, __numSigBits.set, None, u'number of significant bits. default 8')

    
    # Element {http://www.opengis.net/tml}justification uses Python identifier justification
    __justification = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'justification'), 'justification', '__httpwww_opengis_nettml_CTD_ANON_67_httpwww_opengis_nettmljustification', False)

    
    justification = property(__justification.value, __justification.set, None, u'if numSigBits is less than numBits this element indicates how sigbit are justified.  Allowed values: left, right. Default: right')

    
    # Element {http://www.opengis.net/tml}endTextDelimiter uses Python identifier endTextDelimiter
    __endTextDelimiter = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'endTextDelimiter'), 'endTextDelimiter', '__httpwww_opengis_nettml_CTD_ANON_67_httpwww_opengis_nettmlendTextDelimiter', False)

    
    endTextDelimiter = property(__endTextDelimiter.value, __endTextDelimiter.set, None, u'delimiter used to separate variable size dataUnits in cluster when encode is text (utf or ucs). default delimiter is none. Empty tag means none')

    
    # Element {http://www.opengis.net/tml}numBits uses Python identifier numBits
    __numBits = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'numBits'), 'numBits', '__httpwww_opengis_nettml_CTD_ANON_67_httpwww_opengis_nettmlnumBits', False)

    
    numBits = property(__numBits.value, __numBits.set, None, u'number of bits. default 8 ')


    _ElementMap = {
        __beginTextDelimiter.name() : __beginTextDelimiter,
        __numSigBits.name() : __numSigBits,
        __justification.name() : __justification,
        __endTextDelimiter.name() : __endTextDelimiter,
        __numBits.name() : __numBits
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_68 with content type SIMPLE
class CTD_ANON_68 (BindType):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is BindType
    
    # Attribute bindUidRef inherited from {http://www.opengis.net/tml}BindType
    
    # Attribute bindUid inherited from {http://www.opengis.net/tml}BindType
    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_68_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_68_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_68_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')


    _ElementMap = BindType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BindType._AttributeMap.copy()
    _AttributeMap.update({
        __uid.name() : __uid,
        __name.name() : __name,
        __uidRef.name() : __uidRef
    })



# Complex type CTD_ANON_69 with content type ELEMENT_ONLY
class CTD_ANON_69 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}clusterDesc uses Python identifier clusterDesc
    __clusterDesc = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'clusterDesc'), 'clusterDesc', '__httpwww_opengis_nettml_CTD_ANON_69_httpwww_opengis_nettmlclusterDesc', True)

    
    clusterDesc = property(__clusterDesc.value, __clusterDesc.set, None, u'An empty clusterdesc tag in a data stream indicates that this cluster is no longer contained in the data stream.')


    _ElementMap = {
        __clusterDesc.name() : __clusterDesc
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_70 with content type ELEMENT_ONLY
class CTD_ANON_70 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}relationDescription uses Python identifier relationDescription
    __relationDescription = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'relationDescription'), 'relationDescription', '__httpwww_opengis_nettml_CTD_ANON_70_httpwww_opengis_nettmlrelationDescription', False)

    
    relationDescription = property(__relationDescription.value, __relationDescription.set, None, u'longer description of the signal or the property relation')

    
    # Element {http://www.opengis.net/tml}dataSource uses Python identifier dataSource
    __dataSource = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataSource'), 'dataSource', '__httpwww_opengis_nettml_CTD_ANON_70_httpwww_opengis_nettmldataSource', False)

    
    dataSource = property(__dataSource.value, __dataSource.set, None, u'data source')

    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_70_httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'connection or node UID of the connection signal data relationship')

    
    # Element {http://www.opengis.net/tml}dataSink uses Python identifier dataSink
    __dataSink = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataSink'), 'dataSink', '__httpwww_opengis_nettml_CTD_ANON_70_httpwww_opengis_nettmldataSink', True)

    
    dataSink = property(__dataSink.value, __dataSink.set, None, u'data sink')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_70_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_70_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid_
    __uid_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid_', '__httpwww_opengis_nettml_CTD_ANON_70_uid', pyxb.binding.datatypes.anyURI)
    
    uid_ = property(__uid_.value, __uid_.set, None, u'unique ID for this element')


    _ElementMap = {
        __relationDescription.name() : __relationDescription,
        __dataSource.name() : __dataSource,
        __uid.name() : __uid,
        __dataSink.name() : __dataSink
    }
    _AttributeMap = {
        __name.name() : __name,
        __uidRef.name() : __uidRef,
        __uid_.name() : __uid_
    }



# Complex type CTD_ANON_71 with content type ELEMENT_ONLY
class CTD_ANON_71 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}spaceLocCoords uses Python identifier spaceLocCoords
    __spaceLocCoords = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'spaceLocCoords'), 'spaceLocCoords', '__httpwww_opengis_nettml_CTD_ANON_71_httpwww_opengis_nettmlspaceLocCoords', True)

    
    spaceLocCoords = property(__spaceLocCoords.value, __spaceLocCoords.set, None, u'one set of coordinates for each spatial axes.  Each shape is defined relative to an arbitrary data spatial reference system. ')

    
    # Element {http://www.opengis.net/tml}spaceCoordSystem uses Python identifier spaceCoordSystem
    __spaceCoordSystem = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'spaceCoordSystem'), 'spaceCoordSystem', '__httpwww_opengis_nettml_CTD_ANON_71_httpwww_opengis_nettmlspaceCoordSystem', False)

    
    spaceCoordSystem = property(__spaceCoordSystem.value, __spaceCoordSystem.set, None, u'Allowed values: spherical,  rectangular, cylindrical, wgs84elliptical.  default is spherical.')

    
    # Element {http://www.opengis.net/tml}pwrProfile uses Python identifier pwrProfile
    __pwrProfile = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'pwrProfile'), 'pwrProfile', '__httpwww_opengis_nettml_CTD_ANON_71_httpwww_opengis_nettmlpwrProfile', False)

    
    pwrProfile = property(__pwrProfile.value, __pwrProfile.set, None, u'The equi-power surface power level compared to the point of transmission or reception.   default is -3db beam pattern, pwrProfile="-3".')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_71_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_71_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_71_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __spaceLocCoords.name() : __spaceLocCoords,
        __spaceCoordSystem.name() : __spaceCoordSystem,
        __pwrProfile.name() : __pwrProfile
    }
    _AttributeMap = {
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    }



# Complex type CTD_ANON_72 with content type ELEMENT_ONLY
class CTD_ANON_72 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}property uses Python identifier property_
    __property = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'property'), 'property_', '__httpwww_opengis_nettml_CTD_ANON_72_httpwww_opengis_nettmlproperty', True)

    
    property_ = property(__property.value, __property.set, None, None)


    _ElementMap = {
        __property.name() : __property
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_73 with content type ELEMENT_ONLY
class CTD_ANON_73 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'date'), 'date', '__httpwww_opengis_nettml_CTD_ANON_73_httpwww_opengis_nettmldate', False)

    
    date = property(__date.value, __date.set, None, u'ISO8601 dateTime stamp')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_73_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {http://www.opengis.net/tml}organization uses Python identifier organization
    __organization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'organization'), 'organization', '__httpwww_opengis_nettml_CTD_ANON_73_httpwww_opengis_nettmlorganization', False)

    
    organization = property(__organization.value, __organization.set, None, None)

    
    # Element {http://www.opengis.net/tml}email uses Python identifier email
    __email = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'email'), 'email', '__httpwww_opengis_nettml_CTD_ANON_73_httpwww_opengis_nettmlemail', False)

    
    email = property(__email.value, __email.set, None, None)

    
    # Element {http://www.opengis.net/tml}phone uses Python identifier phone
    __phone = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'phone'), 'phone', '__httpwww_opengis_nettml_CTD_ANON_73_httpwww_opengis_nettmlphone', False)

    
    phone = property(__phone.value, __phone.set, None, None)


    _ElementMap = {
        __date.name() : __date,
        __name.name() : __name,
        __organization.name() : __organization,
        __email.name() : __email,
        __phone.name() : __phone
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_74 with content type SIMPLE
class CTD_ANON_74 (BindType):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is BindType
    
    # Attribute bindUid inherited from {http://www.opengis.net/tml}BindType
    
    # Attribute bindUidRef inherited from {http://www.opengis.net/tml}BindType

    _ElementMap = BindType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BindType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_75 with content type ELEMENT_ONLY
class CTD_ANON_75 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}insituRemote uses Python identifier insituRemote
    __insituRemote = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'insituRemote'), 'insituRemote', '__httpwww_opengis_nettml_CTD_ANON_75_httpwww_opengis_nettmlinsituRemote', False)

    
    insituRemote = property(__insituRemote.value, __insituRemote.set, None, u'allowed values: insitu, remote.  Default is insitu.')

    
    # Element {http://www.opengis.net/tml}spatialDependancy uses Python identifier spatialDependancy
    __spatialDependancy = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'spatialDependancy'), 'spatialDependancy', '__httpwww_opengis_nettml_CTD_ANON_75_httpwww_opengis_nettmlspatialDependancy', False)

    
    spatialDependancy = property(__spatialDependancy.value, __spatialDependancy.set, None, u'Allowed values: attitudeIndependent (default), locationIndependent, positionalIndependent, positionalDependent')

    
    # Element {http://www.opengis.net/tml}transmitterReceiver uses Python identifier transmitterReceiver
    __transmitterReceiver = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'transmitterReceiver'), 'transmitterReceiver', '__httpwww_opengis_nettml_CTD_ANON_75_httpwww_opengis_nettmltransmitterReceiver', False)

    
    transmitterReceiver = property(__transmitterReceiver.value, __transmitterReceiver.set, None, u'allowed values: transmitter, receiver, transceiver.  default is receiver.')


    _ElementMap = {
        __insituRemote.name() : __insituRemote,
        __spatialDependancy.name() : __spatialDependancy,
        __transmitterReceiver.name() : __transmitterReceiver
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_76 with content type ELEMENT_ONLY
class CTD_ANON_76 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}coordName uses Python identifier coordName
    __coordName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'coordName'), 'coordName', '__httpwww_opengis_nettml_CTD_ANON_76_httpwww_opengis_nettmlcoordName', False)

    
    coordName = property(__coordName.value, __coordName.set, None, u'Allowed values: x, y, z, alpha, beta, rho.  ')

    
    # Element {http://www.opengis.net/tml}coords uses Python identifier coords
    __coords = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'coords'), 'coords', '__httpwww_opengis_nettml_CTD_ANON_76_httpwww_opengis_nettmlcoords', False)

    
    coords = property(__coords.value, __coords.set, None, u'values contains a string of real numbers.  The mult and offset are single values, unless the shape varies over the Characteristic Frame then the mult and offset may contain a Characteristic Frame array of values. simple IFOV alpha=0, beta=0.  (ray where rho is infinite)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_76_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_76_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_76_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')


    _ElementMap = {
        __coordName.name() : __coordName,
        __coords.name() : __coords
    }
    _AttributeMap = {
        __name.name() : __name,
        __uidRef.name() : __uidRef,
        __uid.name() : __uid
    }



# Complex type CTD_ANON_77 with content type ELEMENT_ONLY
class CTD_ANON_77 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_77_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, u'name of dataUnit')

    
    # Element {http://www.opengis.net/tml}variableName uses Python identifier variableName
    __variableName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'variableName'), 'variableName', '__httpwww_opengis_nettml_CTD_ANON_77_httpwww_opengis_nettmlvariableName', False)

    
    variableName = property(__variableName.value, __variableName.set, None, u'Name of mathematical term used in the transformation equations.  Index of component is the order in the sequence in the LDS structure.')

    
    # Element {http://www.opengis.net/tml}dataType uses Python identifier dataType
    __dataType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataType'), 'dataType', '__httpwww_opengis_nettml_CTD_ANON_77_httpwww_opengis_nettmldataType', False)

    
    dataType = property(__dataType.value, __dataType.set, None, u'Allowed values: number, complexNumber, text, or binaryBlob.  default is number')

    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_77_httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'uid of dataUnit')

    
    # Element {http://www.opengis.net/tml}bytesInBlob uses Python identifier bytesInBlob
    __bytesInBlob = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'bytesInBlob'), 'bytesInBlob', '__httpwww_opengis_nettml_CTD_ANON_77_httpwww_opengis_nettmlbytesInBlob', False)

    
    bytesInBlob = property(__bytesInBlob.value, __bytesInBlob.set, None, u'If dataType is binaryBlob then number of bytes in the binary blob.  Not used for transducer structures, only for process structures.')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_77_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute uid uses Python identifier uid_
    __uid_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid_', '__httpwww_opengis_nettml_CTD_ANON_77_uid', pyxb.binding.datatypes.anyURI)
    
    uid_ = property(__uid_.value, __uid_.set, None, u'unique ID for this element')

    
    # Attribute name uses Python identifier name_
    __name_ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name_', '__httpwww_opengis_nettml_CTD_ANON_77_name', pyxb.binding.datatypes.string)
    
    name_ = property(__name_.value, __name_.set, None, u'short descriptive name of element')


    _ElementMap = {
        __name.name() : __name,
        __variableName.name() : __variableName,
        __dataType.name() : __dataType,
        __uid.name() : __uid,
        __bytesInBlob.name() : __bytesInBlob
    }
    _AttributeMap = {
        __uidRef.name() : __uidRef,
        __uid_.name() : __uid_,
        __name_.name() : __name_
    }



# Complex type CTD_ANON_78 with content type ELEMENT_ONLY
class CTD_ANON_78 (SpatialCoordType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is SpatialCoordType
    
    # Element refObjUidRef ({http://www.opengis.net/tml}refObjUidRef) inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Element spaceCoordSystem ({http://www.opengis.net/tml}spaceCoordSystem) inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Element spaceCoords ({http://www.opengis.net/tml}spaceCoords) inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Element spaceRefSystem ({http://www.opengis.net/tml}spaceRefSystem) inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Attribute uid inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Attribute uidRef inherited from {http://www.opengis.net/tml}SpatialCoordType
    
    # Attribute name inherited from {http://www.opengis.net/tml}SpatialCoordType

    _ElementMap = SpatialCoordType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = SpatialCoordType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_79 with content type SIMPLE
class CTD_ANON_79 (BindType):
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    # Base type is BindType
    
    # Attribute bindUidRef inherited from {http://www.opengis.net/tml}BindType
    
    # Attribute bindUid inherited from {http://www.opengis.net/tml}BindType
    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_79_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_79_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_79_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = BindType._ElementMap.copy()
    _ElementMap.update({
        
    })
    _AttributeMap = BindType._AttributeMap.copy()
    _AttributeMap.update({
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    })



# Complex type CTD_ANON_80 with content type ELEMENT_ONLY
class CTD_ANON_80 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}coordName uses Python identifier coordName
    __coordName = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'coordName'), 'coordName', '__httpwww_opengis_nettml_CTD_ANON_80_httpwww_opengis_nettmlcoordName', False)

    
    coordName = property(__coordName.value, __coordName.set, None, u'Allowed Values: x, y, z, Alpha, beta, rho, latitude, longitude, altitude, omega, phi, kappa,')

    
    # Element {http://www.opengis.net/tml}coords uses Python identifier coords
    __coords = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'coords'), 'coords', '__httpwww_opengis_nettml_CTD_ANON_80_httpwww_opengis_nettmlcoords', False)

    
    coords = property(__coords.value, __coords.set, None, None)

    
    # Element {http://www.opengis.net/tml}posVelAccel uses Python identifier posVelAccel
    __posVelAccel = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'posVelAccel'), 'posVelAccel', '__httpwww_opengis_nettml_CTD_ANON_80_httpwww_opengis_nettmlposVelAccel', False)

    
    posVelAccel = property(__posVelAccel.value, __posVelAccel.set, None, u'Allowed Values: pos, vel, accel,  Default is pos.')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_80_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_80_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_80_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __coordName.name() : __coordName,
        __coords.name() : __coords,
        __posVelAccel.name() : __posVelAccel
    }
    _AttributeMap = {
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    }



# Complex type CTD_ANON_81 with content type ELEMENT_ONLY
class CTD_ANON_81 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}period uses Python identifier period
    __period = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'period'), 'period', '__httpwww_opengis_nettml_CTD_ANON_81_httpwww_opengis_nettmlperiod', False)

    
    period = property(__period.value, __period.set, None, u'if private trigger is periodic then,  trigger period in seconds')

    
    # Element {http://www.opengis.net/tml}publicTrigger uses Python identifier publicTrigger
    __publicTrigger = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'publicTrigger'), 'publicTrigger', '__httpwww_opengis_nettml_CTD_ANON_81_httpwww_opengis_nettmlpublicTrigger', False)

    
    publicTrigger = property(__publicTrigger.value, __publicTrigger.set, None, u'if trigger is public then this identifies the uidRef of trigger source (command).  Whenever a data cluster is sent to this UID or to the uid of a process that is bound to this uid then this transducer or process cycle will trigger.  The bindUid enables late binding of the trigger source')

    
    # Element {http://www.opengis.net/tml}trigType uses Python identifier trigType
    __trigType = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'trigType'), 'trigType', '__httpwww_opengis_nettml_CTD_ANON_81_httpwww_opengis_nettmltrigType', False)

    
    trigType = property(__trigType.value, __trigType.set, None, u'Allowed Values: private, privateOnDataRecipt, privateOnInputTrig, pvtOnChgOutput.   publicOnTrigReciept.   public trigger: controllable by external commands. private trigger: uncontrollable by external commands.  Virtual trig sensor puts sysClk time in data tag.  If public a bindUid is made available.  default trigger is privatePeriodic.')

    
    # Attribute uid uses Python identifier uid
    __uid = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_81_uid', pyxb.binding.datatypes.anyURI)
    
    uid = property(__uid.value, __uid.set, None, u'unique ID for this element')

    
    # Attribute uidRef uses Python identifier uidRef
    __uidRef = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'uidRef'), 'uidRef', '__httpwww_opengis_nettml_CTD_ANON_81_uidRef', pyxb.binding.datatypes.anyURI)
    
    uidRef = property(__uidRef.value, __uidRef.set, None, u'the contents of this element are exactly the same as the contents of the uidRef element. no need repeating it. (similar to xlink)')

    
    # Attribute name uses Python identifier name
    __name = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_81_name', pyxb.binding.datatypes.string)
    
    name = property(__name.value, __name.set, None, u'short descriptive name of element')


    _ElementMap = {
        __period.name() : __period,
        __publicTrigger.name() : __publicTrigger,
        __trigType.name() : __trigType
    }
    _AttributeMap = {
        __uid.name() : __uid,
        __uidRef.name() : __uidRef,
        __name.name() : __name
    }



# Complex type CTD_ANON_82 with content type ELEMENT_ONLY
class CTD_ANON_82 (ValueType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is ValueType
    
    # Element values ({http://www.opengis.net/tml}values) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element arrayType ({http://www.opengis.net/tml}arrayType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element fcnInterpol ({http://www.opengis.net/tml}fcnInterpol) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element accuracy ({http://www.opengis.net/tml}accuracy) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element mult ({http://www.opengis.net/tml}mult) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element numValues ({http://www.opengis.net/tml}numValues) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element valueDataType ({http://www.opengis.net/tml}valueDataType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element offset ({http://www.opengis.net/tml}offset) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element {http://www.opengis.net/tml}cfSubSampling uses Python identifier cfSubSampling
    __cfSubSampling = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling'), 'cfSubSampling', '__httpwww_opengis_nettml_CTD_ANON_82_httpwww_opengis_nettmlcfSubSampling', True)

    
    cfSubSampling = property(__cfSubSampling.value, __cfSubSampling.set, None, u'the CFSubSampling can be used for chipping part of a large dataArry out and for reducing the number of points within an array for which to associate modeling parameters.  there is one sub sampling element set of points for each component structure (col, row, plane).    index numbers of col, row or plane position within the CFs are listed for which corresponding modeling points will be associated.  sample points are separated by commas, ranges are indicated by ... between numbers which indicates a continuous interval for a single sample. interpolation between samples uses logical structure.  ')

    
    # Element {http://www.opengis.net/tml}dataUidRef uses Python identifier dataUidRef
    __dataUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), 'dataUidRef', '__httpwww_opengis_nettml_CTD_ANON_82_httpwww_opengis_nettmldataUidRef', True)

    
    dataUidRef = property(__dataUidRef.value, __dataUidRef.set, None, u'corresponding UID of dataUnit or dataSet. Duplicate of uid in identification element Default: Uid of dataSet')

    
    # Attribute uidRef inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uid inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute name inherited from {http://www.opengis.net/tml}ValueType

    _ElementMap = ValueType._ElementMap.copy()
    _ElementMap.update({
        __cfSubSampling.name() : __cfSubSampling,
        __dataUidRef.name() : __dataUidRef
    })
    _AttributeMap = ValueType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_83 with content type ELEMENT_ONLY
class CTD_ANON_83 (ValueType):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is ValueType
    
    # Element values ({http://www.opengis.net/tml}values) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element {http://www.opengis.net/tml}dataUidRef uses Python identifier dataUidRef
    __dataUidRef = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), 'dataUidRef', '__httpwww_opengis_nettml_CTD_ANON_83_httpwww_opengis_nettmldataUidRef', True)

    
    dataUidRef = property(__dataUidRef.value, __dataUidRef.set, None, u'corresponding UID of dataUnit or dataSet. Duplicate of uid in identification element Default: Uid of dataSet')

    
    # Element accuracy ({http://www.opengis.net/tml}accuracy) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element mult ({http://www.opengis.net/tml}mult) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element numValues ({http://www.opengis.net/tml}numValues) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element {http://www.opengis.net/tml}cfSubSampling uses Python identifier cfSubSampling
    __cfSubSampling = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling'), 'cfSubSampling', '__httpwww_opengis_nettml_CTD_ANON_83_httpwww_opengis_nettmlcfSubSampling', True)

    
    cfSubSampling = property(__cfSubSampling.value, __cfSubSampling.set, None, u'the CFSubSampling can be used for chipping part of a large dataArry out and for reducing the number of points within an array for which to associate modeling parameters.  there is one sub sampling element set of points for each component structure (col, row, plane).    index numbers of col, row or plane position within the CFs are listed for which corresponding modeling points will be associated.  sample points are separated by commas, ranges are indicated by ... between numbers which indicates a continuous interval for a single sample. interpolation between samples uses logical structure.  ')

    
    # Element fcnInterpol ({http://www.opengis.net/tml}fcnInterpol) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element offset ({http://www.opengis.net/tml}offset) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element arrayType ({http://www.opengis.net/tml}arrayType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Element valueDataType ({http://www.opengis.net/tml}valueDataType) inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uidRef inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute uid inherited from {http://www.opengis.net/tml}ValueType
    
    # Attribute name inherited from {http://www.opengis.net/tml}ValueType

    _ElementMap = ValueType._ElementMap.copy()
    _ElementMap.update({
        __dataUidRef.name() : __dataUidRef,
        __cfSubSampling.name() : __cfSubSampling
    })
    _AttributeMap = ValueType._AttributeMap.copy()
    _AttributeMap.update({
        
    })



# Complex type CTD_ANON_84 with content type ELEMENT_ONLY
class CTD_ANON_84 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'date'), 'date', '__httpwww_opengis_nettml_CTD_ANON_84_httpwww_opengis_nettmldate', False)

    
    date = property(__date.value, __date.set, None, u'ISO8601 dateTime stamp')

    
    # Element {http://www.opengis.net/tml}phone uses Python identifier phone
    __phone = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'phone'), 'phone', '__httpwww_opengis_nettml_CTD_ANON_84_httpwww_opengis_nettmlphone', False)

    
    phone = property(__phone.value, __phone.set, None, None)

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_84_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {http://www.opengis.net/tml}email uses Python identifier email
    __email = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'email'), 'email', '__httpwww_opengis_nettml_CTD_ANON_84_httpwww_opengis_nettmlemail', False)

    
    email = property(__email.value, __email.set, None, None)

    
    # Element {http://www.opengis.net/tml}organization uses Python identifier organization
    __organization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'organization'), 'organization', '__httpwww_opengis_nettml_CTD_ANON_84_httpwww_opengis_nettmlorganization', False)

    
    organization = property(__organization.value, __organization.set, None, None)


    _ElementMap = {
        __date.name() : __date,
        __phone.name() : __phone,
        __name.name() : __name,
        __email.name() : __email,
        __organization.name() : __organization
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_85 with content type ELEMENT_ONLY
class CTD_ANON_85 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}organization uses Python identifier organization
    __organization = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'organization'), 'organization', '__httpwww_opengis_nettml_CTD_ANON_85_httpwww_opengis_nettmlorganization', False)

    
    organization = property(__organization.value, __organization.set, None, None)

    
    # Element {http://www.opengis.net/tml}phone uses Python identifier phone
    __phone = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'phone'), 'phone', '__httpwww_opengis_nettml_CTD_ANON_85_httpwww_opengis_nettmlphone', False)

    
    phone = property(__phone.value, __phone.set, None, None)

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_85_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)

    
    # Element {http://www.opengis.net/tml}date uses Python identifier date
    __date = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'date'), 'date', '__httpwww_opengis_nettml_CTD_ANON_85_httpwww_opengis_nettmldate', False)

    
    date = property(__date.value, __date.set, None, u'ISO8601 dateTime stamp')

    
    # Element {http://www.opengis.net/tml}email uses Python identifier email
    __email = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'email'), 'email', '__httpwww_opengis_nettml_CTD_ANON_85_httpwww_opengis_nettmlemail', False)

    
    email = property(__email.value, __email.set, None, None)


    _ElementMap = {
        __organization.name() : __organization,
        __phone.name() : __phone,
        __name.name() : __name,
        __date.name() : __date,
        __email.name() : __email
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_86 with content type ELEMENT_ONLY
class CTD_ANON_86 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}sequence uses Python identifier sequence
    __sequence = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'sequence'), 'sequence', '__httpwww_opengis_nettml_CTD_ANON_86_httpwww_opengis_nettmlsequence', False)

    
    sequence = property(__sequence.value, __sequence.set, None, u'Allowed values; The sequence shall contain a string of value separated by a comma.  Each value can be a positive integer or a range.  ranges shall be indicated by two integer numbers separated by three sequential decimal points (....) to indicate a run from the first number to the second')

    
    # Element {http://www.opengis.net/tml}inThisDataStruct uses Python identifier inThisDataStruct
    __inThisDataStruct = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'inThisDataStruct'), 'inThisDataStruct', '__httpwww_opengis_nettml_CTD_ANON_86_httpwww_opengis_nettmlinThisDataStruct', True)

    
    inThisDataStruct = property(__inThisDataStruct.value, __inThisDataStruct.set, None, u'Sequence of the data structure components identified in the previous element (seqOfThisDataStruct) in the data structure identified in this element (inThisDataStruct). seqOfBitsInUnit,  seqOfUnitsInSets, seqOfSetsInCf, seqOfCfInClust. Identify the dataStructComponent in this element by dataUidRef.  dataUid of the cluster is "cluster"')

    
    # Element {http://www.opengis.net/tml}seqOfThisDataStruct uses Python identifier seqOfThisDataStruct
    __seqOfThisDataStruct = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'seqOfThisDataStruct'), 'seqOfThisDataStruct', '__httpwww_opengis_nettml_CTD_ANON_86_httpwww_opengis_nettmlseqOfThisDataStruct', True)

    
    seqOfThisDataStruct = property(__seqOfThisDataStruct.value, __seqOfThisDataStruct.set, None, u'Sequence of (in this element - seqOfThisDataStruct) in the data structure identified in the next element (inThisDataStruct). seqOfBitsInUnit,  seqOfUnitsInSets, seqOfSetsInCf, seqOfCfInClust. Identify the dataStructComponent in this element by dataUidRef.  dataUid of the cluster is "cluster"')


    _ElementMap = {
        __sequence.name() : __sequence,
        __inThisDataStruct.name() : __inThisDataStruct,
        __seqOfThisDataStruct.name() : __seqOfThisDataStruct
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_87 with content type ELEMENT_ONLY
class CTD_ANON_87 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}period uses Python identifier period
    __period = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'period'), 'period', '__httpwww_opengis_nettml_CTD_ANON_87_httpwww_opengis_nettmlperiod', False)

    
    period = property(__period.value, __period.set, None, u'Period in seconds')

    
    # Element {http://www.opengis.net/tml}max uses Python identifier max
    __max = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'max'), 'max', '__httpwww_opengis_nettml_CTD_ANON_87_httpwww_opengis_nettmlmax', False)

    
    max = property(__max.value, __max.set, None, u'max counter count which roll over occurs')

    
    # Element {http://www.opengis.net/tml}uid uses Python identifier uid
    __uid = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'uid'), 'uid', '__httpwww_opengis_nettml_CTD_ANON_87_httpwww_opengis_nettmluid', False)

    
    uid = property(__uid.value, __uid.set, None, u'sysClk UID same as the system UID.  There is only one clock per system.  Subsystems may have clocks')

    
    # Element {http://www.opengis.net/tml}countNumBase uses Python identifier countNumBase
    __countNumBase = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'countNumBase'), 'countNumBase', '__httpwww_opengis_nettml_CTD_ANON_87_httpwww_opengis_nettmlcountNumBase', False)

    
    countNumBase = property(__countNumBase.value, __countNumBase.set, None, u'number base in which clock characters increment.  Allowed values are: 2, 8, 10, 16.  Default is 10')

    
    # Element {http://www.opengis.net/tml}min uses Python identifier min
    __min = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'min'), 'min', '__httpwww_opengis_nettml_CTD_ANON_87_httpwww_opengis_nettmlmin', False)

    
    min = property(__min.value, __min.set, None, u'counter starting point after rollover.  default 0')

    
    # Element {http://www.opengis.net/tml}name uses Python identifier name
    __name = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'name'), 'name', '__httpwww_opengis_nettml_CTD_ANON_87_httpwww_opengis_nettmlname', False)

    
    name = property(__name.value, __name.set, None, None)


    _ElementMap = {
        __period.name() : __period,
        __max.name() : __max,
        __uid.name() : __uid,
        __countNumBase.name() : __countNumBase,
        __min.name() : __min,
        __name.name() : __name
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_88 with content type ELEMENT_ONLY
class CTD_ANON_88 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}property uses Python identifier property_
    __property = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'property'), 'property_', '__httpwww_opengis_nettml_CTD_ANON_88_httpwww_opengis_nettmlproperty', True)

    
    property_ = property(__property.value, __property.set, None, None)


    _ElementMap = {
        __property.name() : __property
    }
    _AttributeMap = {
        
    }



# Complex type CTD_ANON_89 with content type ELEMENT_ONLY
class CTD_ANON_89 (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.opengis.net/tml}system uses Python identifier system
    __system = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'system'), 'system', '__httpwww_opengis_nettml_CTD_ANON_89_httpwww_opengis_nettmlsystem', True)

    
    system = property(__system.value, __system.set, None, u'An empty system tag (with id) in a data stream indicates that the system is no longer available in the stream, or if system was not previously part of the parent system it will be added to the parent system.')


    _ElementMap = {
        __system.name() : __system
    }
    _AttributeMap = {
        
    }



tml = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'tml'), CTD_ANON_9, documentation=u'Root Element.  Also contains attributes to indicate the overall security classification of this TML stream or file.  If needed individual data clusters can be labeled with a security class.')
Namespace.addCategoryObject('elementBinding', tml.name().localName(), tml)

clusterDesc = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'clusterDesc'), CTD_ANON_12, documentation=u'An empty clusterdesc tag in a data stream indicates that this cluster is no longer contained in the data stream.')
Namespace.addCategoryObject('elementBinding', clusterDesc.name().localName(), clusterDesc)

spaceCoordSystem = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'spaceCoordSystem'), BindType, documentation=u'Allowed values: spherical,  rectangular, cylindrical, wgs84elliptical.  default is spherical.')
Namespace.addCategoryObject('elementBinding', spaceCoordSystem.name().localName(), spaceCoordSystem)

spatialModel = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'spatialModel'), CTD_ANON_14)
Namespace.addCategoryObject('elementBinding', spatialModel.name().localName(), spatialModel)

cfSubSampling = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling'), CTD_ANON_10, documentation=u'the CFSubSampling can be used for chipping part of a large dataArry out and for reducing the number of points within an array for which to associate modeling parameters.  there is one sub sampling element set of points for each component structure (col, row, plane).    index numbers of col, row or plane position within the CFs are listed for which corresponding modeling points will be associated.  sample points are separated by commas, ranges are indicated by ... between numbers which indicates a continuous interval for a single sample. interpolation between samples uses logical structure.  ')
Namespace.addCategoryObject('elementBinding', cfSubSampling.name().localName(), cfSubSampling)

process = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'process'), ProcessType, documentation=u'A transducer can be a stand alone object or part of a system. Describes derivation of output dataUnits relative to input dataUnits or constants.  An empty process tag in a data stream indicates that this process is no longer a part of the system')
Namespace.addCategoryObject('elementBinding', process.name().localName(), process)

responseModels = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'responseModels'), CTD_ANON_44)
Namespace.addCategoryObject('elementBinding', responseModels.name().localName(), responseModels)

transducer = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'transducer'), TransducerType, documentation=u'A transducer can be a stand alone object or part of a system.  An empty transducer tag in a data stream indicates that this transducer is no longer a part of the system')
Namespace.addCategoryObject('elementBinding', transducer.name().localName(), transducer)

complexity = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'complexity'), BindType, documentation=u'indication of the complexity of handling this data. Allowed Values: 1A - 1F, 2A -2F, 3A - 3F, 4A - 4F, 5A - 5F.  default 1A')
Namespace.addCategoryObject('elementBinding', complexity.name().localName(), complexity)

objToObjRelation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objToObjRelation'), CTD_ANON_22, documentation=u'This relation describes object to object relations. Attaching a transducer to an object (object is a subject or a transducer) (i.e. dangle, where the only thing the transducer interfaces to is that subject. (cant different individual data many measures with many individual subjects, see objToData). The transducer to transducers relation does not include phenomenon to phenomenon connections, see dataToData')
Namespace.addCategoryObject('elementBinding', objToObjRelation.name().localName(), objToObjRelation)

logicalDataStructure = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'logicalDataStructure'), CTD_ANON_42, documentation=u'the logical structure of data (i.e. of the characteristic frame).  This is not necessarily the structure or order that data is communicated in.  The transmission order is defined in the cluster description.  The transmission order is defined relative to the logical order.')
Namespace.addCategoryObject('elementBinding', logicalDataStructure.name().localName(), logicalDataStructure)

objToDataRelation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objToDataRelation'), CTD_ANON_23, documentation=u'Connects transducer to bindUids.  Associate transducer data to a (remote) object.  This may occur after data acquisition. An object is either a transducer, subject or their properties.    Many subjects may be related to data in a dataArray. The objects can be related to data units, sets and arrays to subjects.  ')
Namespace.addCategoryObject('elementBinding', objToDataRelation.name().localName(), objToDataRelation)

subject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subject'), CTD_ANON_32, documentation=u'This is the subject (object, thing) that relates to the phenomenon (property) that is affected or detected by the transducer. The relation between a subject and transducer data or subject and subject is described in the relationship element. An empty subject tag in a data stream indicates that this object is no longer a part of the system')
Namespace.addCategoryObject('elementBinding', subject.name().localName(), subject)

system = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'system'), SystemType, documentation=u'An empty system tag (with id) in a data stream indicates that the system is no longer available in the stream, or if system was not previously part of the parent system it will be added to the parent system.')
Namespace.addCategoryObject('elementBinding', system.name().localName(), system)

temporalModel = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'temporalModel'), CTD_ANON_45)
Namespace.addCategoryObject('elementBinding', temporalModel.name().localName(), temporalModel)

accuracy = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'accuracy'), CTD_ANON_20, documentation=u'accuracy is in terms of the data value before adjustment by mult and offset.   if a characteristic frame (i.e. number of values) of values of accuracy, then each value corresponds to the corresponding Characteristic Frame  position or interval')
Namespace.addCategoryObject('elementBinding', accuracy.name().localName(), accuracy)

data = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'data'), CTD_ANON_39, documentation=u'this element carries the date to or from transducer systems.  The data element will carry a single instance or a continuous stream of a condition or set of synchronous conditions time tag to the precise instant of creation.   There is no XML markup of data within the data tag.  A system description will describe the decoding and understanding of the data within the data tag.')
Namespace.addCategoryObject('elementBinding', data.name().localName(), data)

dataUnit = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUnit'), CTD_ANON_77, documentation=u'an elemental unit of data.  one description for each unit')
Namespace.addCategoryObject('elementBinding', dataUnit.name().localName(), dataUnit)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'validatedBy'), CTD_ANON_5, scope=CTD_ANON))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'characterizedBy'), CTD_ANON_2, scope=CTD_ANON))
CTD_ANON._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'characterizedBy')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'validatedBy')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=CTD_ANON_, documentation=u'uid of input'))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'description'), BindType, scope=CTD_ANON_))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_))
CTD_ANON_._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'description')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'email'), BindType, scope=CTD_ANON_2))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'organization'), BindType, scope=CTD_ANON_2))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'date'), BindType, scope=CTD_ANON_2, documentation=u'ISO8601 dateTime stamp'))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'phone'), BindType, scope=CTD_ANON_2))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_2))
CTD_ANON_2._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'organization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'email')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'phone')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'date')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_2._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_2._GroupModel, min_occurs=1, max_occurs=1)



ValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'values'), BindType, scope=ValueType, documentation=u'values can contain a single value or a string of values separated by a comma.  Each value can contain text,  number, or a range of numbers. Each range value shall contain two numbers separated by three decimal points (...), the first number identifies the closed end of the range and the second number identifies the open end of the range.  Values in the range may be integer or real numbers. Reals may use E for exponent.   In addition to numbers in the range the text -inf and inf can be used to represent -infinity and plus infinity respectively.  For arrayType of function interpolation between values should be handled as indicated in the fcnInterpolate element.'))

ValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol'), BindType, scope=ValueType, documentation=u'Allowed Values: continuous, discrete, lastValue, returnToZero, '))

ValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'accuracy'), CTD_ANON_20, scope=ValueType, documentation=u'accuracy is in terms of the data value before adjustment by mult and offset.   if a characteristic frame (i.e. number of values) of values of accuracy, then each value corresponds to the corresponding Characteristic Frame  position or interval'))

ValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'mult'), BindType, scope=ValueType, documentation=u'default 1. if multiple values of mult, then each value corresponds to the corresponding Characteristic Frame position or interval. Can have a set of mult or offset equalization values and a sensor modifying those values through a bindUID.  The bindUID sensor value will multiply with the values in the mult element.'))

ValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numValues'), BindType, scope=ValueType, documentation=u'number of points, or ranges in values element.   Allowed values: positive integer. Default is 0.'))

ValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'valueDataType'), BindType, scope=ValueType, documentation=u'data type of the value. Allowed values: text, number.  Default number'))

ValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'offset'), BindType, scope=ValueType, documentation=u'default 0. if multiple values of offset, then each value corresponds to the corresponding Characteristic Frame  position or interval.  Can have a set of mult or offset equalization values and a sensor modifying those values through a bindUID.  The bindUID sensor value will add with the values in the offset element.'))

ValueType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'arrayType'), BindType, scope=ValueType, documentation=u'Allowed Values: fcn, charFrame. singleValue.  Default is fcn.   the value element can contain one or multiple values. '))
ValueType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numValues')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'arrayType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueDataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mult')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offset')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ValueType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accuracy')), min_occurs=0L, max_occurs=None)
    )
ValueType._ContentModel = pyxb.binding.content.ParticleModel(ValueType._GroupModel, min_occurs=0L, max_occurs=1)


CTD_ANON_3._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numValues')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'arrayType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueDataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mult')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offset')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accuracy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_3._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_3._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'frequency'), CTD_ANON_11, scope=CTD_ANON_4, documentation=u'Set of point coordinates describing frequency independent axis'))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'phase'), CTD_ANON_8, scope=CTD_ANON_4, documentation=u'Set of point coordinates describing phase dependent axis'))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'freqRespType'), BindType, scope=CTD_ANON_4, documentation=u'Allowed values: carried, modulation, PSD  (pwrSpectralDensity).  default carrier'))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), BindType, scope=CTD_ANON_4, documentation=u'same as uidRef in attributes'))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'amplitude'), CTD_ANON_6, scope=CTD_ANON_4, documentation=u'Set of point coordinates describing amplitude dependent axis'))
CTD_ANON_4._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'freqRespType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'amplitude')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'phase')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'frequency')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_4._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_4._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'email'), BindType, scope=CTD_ANON_5))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'phone'), BindType, scope=CTD_ANON_5))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'date'), BindType, scope=CTD_ANON_5, documentation=u'ISO8601 dateTime stamp'))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_5))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'organization'), BindType, scope=CTD_ANON_5))
CTD_ANON_5._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'organization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'email')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'phone')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'date')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_5._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_5._GroupModel, min_occurs=1, max_occurs=1)


CTD_ANON_6._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numValues')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'arrayType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueDataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mult')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offset')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accuracy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_6._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_6._GroupModel, min_occurs=0L, max_occurs=1)


CTD_ANON_7._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numValues')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'arrayType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueDataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mult')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offset')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accuracy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_7._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_7._GroupModel, min_occurs=0L, max_occurs=1)


CTD_ANON_8._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numValues')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'arrayType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueDataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mult')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offset')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accuracy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_8._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_8._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'data'), CTD_ANON_39, scope=CTD_ANON_9, documentation=u'this element carries the date to or from transducer systems.  The data element will carry a single instance or a continuous stream of a condition or set of synchronous conditions time tag to the precise instant of creation.   There is no XML markup of data within the data tag.  A system description will describe the decoding and understanding of the data within the data tag.'))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'system'), SystemType, scope=CTD_ANON_9, documentation=u'An empty system tag (with id) in a data stream indicates that the system is no longer available in the stream, or if system was not previously part of the parent system it will be added to the parent system.'))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'extSysRelations'), CTD_ANON_63, scope=CTD_ANON_9, documentation=u'for relating external subject to external  subject or transducer data to external subject.  An external subject (object) is external to the system.'))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'process'), ProcessType, scope=CTD_ANON_9, documentation=u'A transducer can be a stand alone object or part of a system. Describes derivation of output dataUnits relative to input dataUnits or constants.  An empty process tag in a data stream indicates that this process is no longer a part of the system'))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subject'), CTD_ANON_32, scope=CTD_ANON_9, documentation=u'This is the subject (object, thing) that relates to the phenomenon (property) that is affected or detected by the transducer. The relation between a subject and transducer data or subject and subject is described in the relationship element. An empty subject tag in a data stream indicates that this object is no longer a part of the system'))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'transducer'), TransducerType, scope=CTD_ANON_9, documentation=u'A transducer can be a stand alone object or part of a system.  An empty transducer tag in a data stream indicates that this transducer is no longer a part of the system'))
CTD_ANON_9._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'system')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'subject')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'transducer')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'process')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'extSysRelations')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'data')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_9._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_9._GroupModel, min_occurs=0L, max_occurs=None)



CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subSampleCfIndexPts'), BindType, scope=CTD_ANON_10, documentation=u'use same rules as points under value'))

CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'cfStructComp'), BindType, scope=CTD_ANON_10, documentation=u'Allowed values: column, row, plane.  default is column.  One cfSubSampling element for each cfStructComp required.'))

CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numOfSubSampleIndexPoints'), BindType, scope=CTD_ANON_10, documentation=u'Allowed values: positive integers from 1 to the number of columns, rows, or planes in the data structure.  This number indicates the number of samples in the cfSubSampleIndexPts.'))
CTD_ANON_10._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'cfStructComp')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numOfSubSampleIndexPoints')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'subSampleCfIndexPts')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_10._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_10._GroupModel, min_occurs=1, max_occurs=1)


CTD_ANON_11._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numValues')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'arrayType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueDataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mult')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offset')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accuracy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_11._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_11._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'clusterProperties'), CTD_ANON_58, scope=CTD_ANON_12))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'binHeaderEncode'), CTD_ANON_48, scope=CTD_ANON_12, documentation=u'If cluster type is binary this field describes the encoding of the header attributes. binary files will contain only the contents of the attributes and not the attribute tag.  The binary header will not contain the left carrot and the letters "data" at the beginning of the header either, nor the right carrot at the end of the header.'))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUnitEncoding'), CTD_ANON_24, scope=CTD_ANON_12, documentation=u'This unit describes the encoding of the dataUnit identified in the dataUnitUidRef child element.  Some clusters which represent only an event from a source or a trigger are empty and may not contain any dataUnits.'))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'transSeq'), CTD_ANON_86, scope=CTD_ANON_12, documentation=u'This is the order in which data is sent in the cluster or CF (whichever is larger) relative to the logical data structure.  The order of structure components are listed from lowest freq to highest frequency order.   If transport sequence is blank then the sequence is the same as the logical order (sequence) for that structure component.'))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'idMapping'), CTD_ANON_54, scope=CTD_ANON_12))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'description'), BindType, scope=CTD_ANON_12, documentation=u'description of the data cluster'))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'timeTag'), CTD_ANON_21, scope=CTD_ANON_12, documentation=u'describes what time tag is used for the cluster.  Useful when parent systems normalize clocks from child components.  This element also describes how accurately the sysClk value is applied to the cluster start instant.  This is different from the accuracy of the system clock.'))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numCfInCluster'), BindType, scope=CTD_ANON_12, documentation=u'number of characteristic frames in a cluster or the number of clusters which comprise a large characteristic frame.  default = 1.  example: 2 means 2 CF per cluster, -2 means 2 clusters per CF.  Allowed values: signed integer.  zero not allowed.'))
CTD_ANON_12._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'idMapping')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'clusterProperties')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'binHeaderEncode')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'timeTag')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUnitEncoding')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numCfInCluster')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'transSeq')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_12._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_12._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'validatedBy'), CTD_ANON_73, scope=CTD_ANON_13))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'calibratedBy'), CTD_ANON_57, scope=CTD_ANON_13))
CTD_ANON_13._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'calibratedBy')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'validatedBy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_13._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_13._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ambiguitySpace'), CTD_ANON_15, scope=CTD_ANON_14, documentation=u'Multiple AS are combined as spatial intersections.  e.g. one for columns and one for rows.  Typically every cell within a multiple cell CF will share the same shape but have unique positions.'))

CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling'), CTD_ANON_10, scope=CTD_ANON_14, documentation=u'the CFSubSampling can be used for chipping part of a large dataArry out and for reducing the number of points within an array for which to associate modeling parameters.  there is one sub sampling element set of points for each component structure (col, row, plane).    index numbers of col, row or plane position within the CFs are listed for which corresponding modeling points will be associated.  sample points are separated by commas, ranges are indicated by ... between numbers which indicates a continuous interval for a single sample. interpolation between samples uses logical structure.  '))

CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), BindType, scope=CTD_ANON_14, documentation=u'corresponding UID of dataUnit, dataSet,  or data Array.  If data array then all subordinate data structures share same model (row, col, or plane), if dataSet then all data units share same model (cf), if dataUnit then only that units model is described (cf). '))
CTD_ANON_14._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ambiguitySpace')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_14._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_14._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'position'), CTD_ANON_78, scope=CTD_ANON_15, documentation=u'location and attitude of ambiguity shape'))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'shape'), CTD_ANON_71, scope=CTD_ANON_15, documentation=u'This is the shape of the AS for the power profile indicated.  May also have multiple shapes to define multiple lobes of energy fields.  Multiple shapes within an AS are combined as a spatial unions.   The position elements defines the position of each shape.'))
CTD_ANON_15._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'shape')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'position')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_15._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_15._GroupModel, min_occurs=1, max_occurs=1)



IdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'calibration'), CTD_ANON_13, scope=IdentificationType, documentation=u'Do the TML descriptions accurately reflect actual performance specifications'))

IdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=IdentificationType, documentation=u'uid of registry object'))

IdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'characterization'), CTD_ANON, scope=IdentificationType, documentation=u'Do the tml descriptions comply with the TML Compliance Rules'))

IdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=IdentificationType))

IdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'description'), BindType, scope=IdentificationType))

IdentificationType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'complexity'), BindType, scope=IdentificationType, documentation=u'indication of the complexity of handling this data. Allowed Values: 1A - 1F, 2A -2F, 3A - 3F, 4A - 4F, 5A - 5F.  default 1A'))
IdentificationType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'complexity')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'characterization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(IdentificationType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'calibration')), min_occurs=0L, max_occurs=1)
    )
IdentificationType._ContentModel = pyxb.binding.content.ParticleModel(IdentificationType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'serialNumber'), BindType, scope=CTD_ANON_16))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'modelNumber'), BindType, scope=CTD_ANON_16))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'owner'), CTD_ANON_84, scope=CTD_ANON_16))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'manufacture'), BindType, scope=CTD_ANON_16))

CTD_ANON_16._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'operator'), CTD_ANON_85, scope=CTD_ANON_16))
CTD_ANON_16._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'complexity')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'characterization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'calibration')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_16._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'manufacture')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'modelNumber')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'serialNumber')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'owner')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'operator')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_16._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_16._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_16._GroupModel_2, min_occurs=1, max_occurs=1)
    )
CTD_ANON_16._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_16._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=CTD_ANON_18, documentation=u'uid of dataSet. '))

CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numObjInSet'), BindType, scope=CTD_ANON_18, documentation=u'number of subordinate sets and/or arrays.  default 1'))

CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_18, documentation=u'name of dataSet'))

CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUnit'), CTD_ANON_77, scope=CTD_ANON_18, documentation=u'an elemental unit of data.  one description for each unit'))

CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'variableName'), BindType, scope=CTD_ANON_18, documentation=u'Name of mathematical term used in the transformation equations.  Index of component is the order in the sequence in the LDS structure.'))

CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataArray'), DataArrayType, scope=CTD_ANON_18))
CTD_ANON_18._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUnit')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataArray')), min_occurs=1, max_occurs=1)
    )
CTD_ANON_18._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'variableName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numObjInSet')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_18._GroupModel_, min_occurs=0L, max_occurs=None)
    )
CTD_ANON_18._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_18._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'process'), ProcessType, scope=CTD_ANON_19, documentation=u'A transducer can be a stand alone object or part of a system. Describes derivation of output dataUnits relative to input dataUnits or constants.  An empty process tag in a data stream indicates that this process is no longer a part of the system'))
CTD_ANON_19._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'process')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_19._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_19._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'type'), BindType, scope=CTD_ANON_20, documentation=u'Allowed values: relative, absolute, systematic, random. default is absolute'))

CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'factor'), BindType, scope=CTD_ANON_20, documentation=u'allowed values: 1sigma, 2sigma, 3sigma, 4sigma, 5sigma, 6sigma, percent, range. RMS, RSS, Default is 1sigma'))

CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'errorDistribution'), BindType, scope=CTD_ANON_20, documentation=u'Allowed Values: gaussian, chi, chi2, possion,  gamma.  default is gaussian'))

CTD_ANON_20._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'accyValues'), BindType, scope=CTD_ANON_20, documentation=u'A single accyValue relates to whole range of parent coordinates (e.g. data or prop). If accyValue is variable over the parent coordinates then there shall be a one-to-one correspondence between the accyValues and the parent coordinates.  use mult and offset to describe variances over CF'))
CTD_ANON_20._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'type')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'errorDistribution')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'factor')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_20._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accyValues')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_20._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_20._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_21._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'sysClkUidRef'), BindType, scope=CTD_ANON_21, documentation=u'if clk is used in the start tag and multiple clocks are used in a system.  Default is the first parent system clock'))

CTD_ANON_21._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'accuracy'), CTD_ANON_20, scope=CTD_ANON_21, documentation=u'accuracy is in terms of the data value before adjustment by mult and offset.   if a characteristic frame (i.e. number of values) of values of accuracy, then each value corresponds to the corresponding Characteristic Frame  position or interval'))
CTD_ANON_21._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_21._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'sysClkUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_21._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accuracy')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_21._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_21._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'relationDescription'), BindType, scope=CTD_ANON_22, documentation=u'description of the  relation'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'object'), CTD_ANON_47, scope=CTD_ANON_22, documentation=u'many objects can be related to a many objects.  probabilities can be assigned to each relation'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=CTD_ANON_22, documentation=u'uid of the relationship'))

CTD_ANON_22._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'confidence'), BindType, scope=CTD_ANON_22, documentation=u'confidence of relationship (-1 to 1). -1 is 100% no confidence. confidence values match same sequence as logical data structure (if multiple values in data structure)'))
CTD_ANON_22._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'relationDescription')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'object')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_22._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'confidence')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_22._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_22._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), BindType, scope=CTD_ANON_23, documentation=u'UID of the data reference.  Archived data streams will have a UID indicative of the data source, time, and clk count of the start. '))

CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=CTD_ANON_23, documentation=u'connection or node UID of the connection signal data or property relationship'))

CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'object'), CTD_ANON_37, scope=CTD_ANON_23, documentation=u'Object can be a single transducer (dangle relation), a single dataUID, or many subjects can be related to a single data unit.  probabilities can be assigned to each relation.'))

CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), BindType, scope=CTD_ANON_23))

CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'relationDescription'), CTD_ANON_74, scope=CTD_ANON_23, documentation=u'description of the signal or the property relation'))

CTD_ANON_23._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_23))
CTD_ANON_23._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_23._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_23._GroupModel_2, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_23._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'relationDescription')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_23._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'object')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_23._GroupModel_, min_occurs=1, max_occurs=1)
    )
CTD_ANON_23._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_23._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUnitFieldSize'), CTD_ANON_25, scope=CTD_ANON_24))

CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numBase'), BindType, scope=CTD_ANON_24, documentation=u'when numbers are encoded as text the number base must be understood.  Allowed values: 2, 8, 10, 16, 32, 64, 128.  default 10'))

CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUnitUidRef'), BindType, scope=CTD_ANON_24, documentation=u'UID of the dataUnit from the logical structure.  '))

CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'endian'), BindType, scope=CTD_ANON_24, documentation=u'Allowed values: big, little.  default little'))

CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'handleAsType'), BindType, scope=CTD_ANON_24, documentation=u'how should the text or number be handled in the client application.  Allowed values: anuURI, boolean, byte, double, float, short, string, int, integer, long, nonNegativeInteger, nonPositiveInteger, positiveInteger,  unsignedByte, unsignedInt, unsignedShort, unsignedLong.'))

CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataType'), BindType, scope=CTD_ANON_24, documentation=u'Allowed values: text, number, binBlob.  Default is text. '))

CTD_ANON_24._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'encode'), BindType, scope=CTD_ANON_24, documentation=u'Allowed values: ucs16, utf8, signInt, unsignInt, real, complex, bcd.  default utf8.  When clusterType is not binary only utf8 is allowed in cluster.  All types are allowed when clusterType is binary. Complex values are exchanged as two phenomenon (mag and phase or real and imaginary components) or as a single complex number.'))
CTD_ANON_24._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUnitUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUnitFieldSize')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'endian')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'encode')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numBase')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_24._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'handleAsType')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_24._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_24._GroupModel, min_occurs=1, max_occurs=1)



DataArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataArray'), DataArrayType, scope=DataArrayType, documentation=u'a dataArray contains a homogeneous collection of one or more dataSets or dataArrays'))

DataArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=DataArrayType, documentation=u'uid of dataArray'))

DataArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataSet'), CTD_ANON_18, scope=DataArrayType, documentation=u'data Sets contain a heterogeneous collection of one or more dataUnits'))

DataArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=DataArrayType, documentation=u'name of dataArray'))

DataArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numObjInArray'), BindType, scope=DataArrayType, documentation=u'The chosen object (dataSet or dataArray) repeats this many time.   default 1'))

DataArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'arrayOf'), BindType, scope=DataArrayType, documentation=u'Allowed values: columns, rows, planes default is columns'))

DataArrayType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'variableName'), BindType, scope=DataArrayType, documentation=u'Name of mathematical term used in the transformation equations.  Index of component is same as order sequence in the lds.'))
DataArrayType._GroupModel_ = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataSet')), min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataArray')), min_occurs=1, max_occurs=1)
    )
DataArrayType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'variableName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'arrayOf')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataArrayType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numObjInArray')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(DataArrayType._GroupModel_, min_occurs=0L, max_occurs=1)
    )
DataArrayType._ContentModel = pyxb.binding.content.ParticleModel(DataArrayType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_25._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'endTextDelimiter'), BindType, scope=CTD_ANON_25, documentation=u'default delimiter is none. Empty tag means none.'))

CTD_ANON_25._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'justification'), BindType, scope=CTD_ANON_25, documentation=u'if numSigBits is less than numBits this element indicates how sigbit are justified.  Allowed values: left, right. Default: right'))

CTD_ANON_25._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'beginTextDelimiter'), BindType, scope=CTD_ANON_25, documentation=u'delimiter used to separate variable size dataUnits in cluster when encode is text (utf or ucs). default delimiter is none.  Empty tag means none.'))

CTD_ANON_25._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numBits'), BindType, scope=CTD_ANON_25, documentation=u'default  8'))

CTD_ANON_25._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numSigBits'), BindType, scope=CTD_ANON_25, documentation=u'default'))
CTD_ANON_25._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numBits')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numSigBits')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'justification')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_25._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'beginTextDelimiter')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_25._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'endTextDelimiter')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_25._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_25._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_25._GroupModel_2, min_occurs=1, max_occurs=1)
    )
CTD_ANON_25._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_25._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'logicalDataStructure'), CTD_ANON_42, scope=CTD_ANON_27, documentation=u'the logical structure of data (i.e. of the characteristic frame).  This is not necessarily the structure or order that data is communicated in.  The transmission order is defined in the cluster description.  The transmission order is defined relative to the logical order.'))

CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'temporalModel'), CTD_ANON_45, scope=CTD_ANON_27))

CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'other'), pyxb.binding.datatypes.anyType, scope=CTD_ANON_27))

CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'responseModels'), CTD_ANON_44, scope=CTD_ANON_27))

CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'outputIdent'), CTD_ANON_34, scope=CTD_ANON_27))

CTD_ANON_27._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'spatialModel'), CTD_ANON_14, scope=CTD_ANON_27))
CTD_ANON_27._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'outputIdent')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'logicalDataStructure')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'responseModels')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spatialModel')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'temporalModel')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_27._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'other')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_27._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_27._GroupModel, min_occurs=1, max_occurs=1)



SystemType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'identification'), CTD_ANON_16, scope=SystemType, documentation=u'Identification of the system'))

SystemType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'transducers'), CTD_ANON_51, scope=SystemType))

SystemType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subjects'), CTD_ANON_50, scope=SystemType))

SystemType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'systems'), CTD_ANON_89, scope=SystemType))

SystemType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'otherProperties'), CTD_ANON_38, scope=SystemType))

SystemType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'sysClk'), CTD_ANON_87, scope=SystemType, documentation=u'clock counter.  '))

SystemType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'clusterDescriptions'), CTD_ANON_69, scope=SystemType))

SystemType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'processes'), CTD_ANON_19, scope=SystemType))

SystemType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'relations'), CTD_ANON_56, scope=SystemType, documentation=u'relationships of objects within the system.  characterized at the time of the system characterization.'))
SystemType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SystemType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'identification')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'sysClk')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'systems')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'subjects')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'transducers')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'processes')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'relations')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'clusterDescriptions')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SystemType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'otherProperties')), min_occurs=0L, max_occurs=1)
    )
SystemType._ContentModel = pyxb.binding.content.ParticleModel(SystemType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_29._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'calibData'), BindType, scope=CTD_ANON_29, documentation=u'data resulting from calibrated source. or bindUID points to sensor measurement measuring calib source. Default: none'))

CTD_ANON_29._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), BindType, scope=CTD_ANON_29, documentation=u'uid of the data form the logical data structure (dataUnit) to which this response model corresponds'))

CTD_ANON_29._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'variableName'), BindType, scope=CTD_ANON_29, documentation=u'Name of mathematical term used in the transformation equations.  '))

CTD_ANON_29._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'inputOutput'), BindType, scope=CTD_ANON_29, documentation=u'Is the data an input or an output for this dataUnit.  Allowed values: input, output.  Default: output'))
CTD_ANON_29._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numValues')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'arrayType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueDataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mult')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offset')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accuracy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_29._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'inputOutput')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'variableName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'calibData')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_29._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_29._GroupModel_, min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_29._GroupModel_2, min_occurs=1, max_occurs=1)
    )
CTD_ANON_29._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_29._GroupModel, min_occurs=0L, max_occurs=None)



ProcessType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'identification'), CTD_ANON_43, scope=ProcessType, documentation=u'contains security of process description'))

ProcessType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'otherProperties'), CTD_ANON_72, scope=ProcessType))

ProcessType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'output'), CTD_ANON_27, scope=ProcessType, documentation=u'a process can have one or more outputs.  This describes a single output processing cycle, initiated by an output trigger '))

ProcessType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'input'), CTD_ANON_49, scope=ProcessType, documentation=u'a process can have zero or more inputs. This describes a single input process cycle, initiated by an input trigger'))
ProcessType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(ProcessType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'identification')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(ProcessType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'input')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ProcessType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'output')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(ProcessType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'otherProperties')), min_occurs=0L, max_occurs=1)
    )
ProcessType._ContentModel = pyxb.binding.content.ParticleModel(ProcessType._GroupModel, min_occurs=1, max_occurs=1)



TransducerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'logicalDataStructure'), CTD_ANON_42, scope=TransducerType, documentation=u'the logical structure of data (i.e. of the characteristic frame).  This is not necessarily the structure or order that data is communicated in.  The transmission order is defined in the cluster description.  The transmission order is defined relative to the logical order.'))

TransducerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'temporalModel'), CTD_ANON_45, scope=TransducerType))

TransducerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'transducerClass'), CTD_ANON_75, scope=TransducerType, documentation=u'Top level transducer classification'))

TransducerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'identification'), CTD_ANON_40, scope=TransducerType, documentation=u'bind types on most elements enables the description of transducers in the initialization data stream of data elements.  '))

TransducerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'responseModels'), CTD_ANON_44, scope=TransducerType))

TransducerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'otherProperties'), CTD_ANON_88, scope=TransducerType))

TransducerType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'spatialModel'), CTD_ANON_14, scope=TransducerType))
TransducerType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(TransducerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'identification')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TransducerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'transducerClass')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TransducerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'logicalDataStructure')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(TransducerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'responseModels')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(TransducerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spatialModel')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(TransducerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'temporalModel')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(TransducerType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'otherProperties')), min_occurs=0L, max_occurs=1)
    )
TransducerType._ContentModel = pyxb.binding.content.ParticleModel(TransducerType._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_30._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'listing'), CTD_ANON_35, scope=CTD_ANON_30, documentation=u'Listing of code. Base64 encoded executable or source code with unallowed XML characters escaped out'))

CTD_ANON_30._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'properties'), CTD_ANON_33, scope=CTD_ANON_30))
CTD_ANON_30._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_30._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'properties')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_30._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'listing')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_30._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_30._GroupModel, min_occurs=1, max_occurs=1)



SpatialCoordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'refObjUidRef'), BindType, scope=SpatialCoordType, documentation=u'If the spaceRefSystem element is a transducer or a Sunbect, then this element will identify the particular Transducer or Subject.  This is the UID reference of the object which position coordinates are referenced (relative) to.'))

SpatialCoordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'spaceCoordSystem'), BindType, scope=SpatialCoordType, documentation=u'Allowed values: spherical,  rectangular, cylindrical, wgs84elliptical.  default is spherical.'))

SpatialCoordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'spaceCoords'), CTD_ANON_80, scope=SpatialCoordType, documentation=u'TCF set of positional (translations and rotations) coordinates for each shape,  space separated real numbers.  Order of coordinates shall be from lowest frequency to highest frequency, same as lds. Default locations and orientations are zero'))

SpatialCoordType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'spaceRefSystem'), BindType, scope=SpatialCoordType, documentation=u'which spatial reference system (i.e. spatial datum) are spatial coordinates referenced (relative) to.   Allowed values: transducer, earthCentered, earthLocal, subject. If ref system is transducer or subject then the uid of the transducer or subject must be identified in the refObjUidRef element.'))
SpatialCoordType._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(SpatialCoordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spaceCoordSystem')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SpatialCoordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spaceRefSystem')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SpatialCoordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'refObjUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(SpatialCoordType._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spaceCoords')), min_occurs=0L, max_occurs=None)
    )
SpatialCoordType._ContentModel = pyxb.binding.content.ParticleModel(SpatialCoordType._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_31._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objUidRef'), BindType, scope=CTD_ANON_31, documentation=u'uid of the obj being positioned. multiples allowed if in same position and orientation'))
CTD_ANON_31._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_31._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spaceCoordSystem')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_31._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spaceRefSystem')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_31._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'refObjUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_31._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spaceCoords')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_31._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_31._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'objUidRef')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_31._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_31._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_31._GroupModel_2, min_occurs=1, max_occurs=1)
    )
CTD_ANON_31._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_31._GroupModel, min_occurs=0L, max_occurs=None)


CTD_ANON_32._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), min_occurs=0, max_occurs=None)
    )
CTD_ANON_32._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_32._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_33._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'codeType'), BindType, scope=CTD_ANON_33, documentation=u'Allowed Values: source, exe default: source'))

CTD_ANON_33._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'codeLanguage'), BindType, scope=CTD_ANON_33, documentation=u'Allowed Values: C, C++, Java, Fortran, C Sharp, Basic, Visual Basic. Default: C'))
CTD_ANON_33._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_33._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'codeType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_33._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'codeLanguage')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_33._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_33._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_34._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'description'), BindType, scope=CTD_ANON_34))

CTD_ANON_34._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=CTD_ANON_34, documentation=u'uid of output'))

CTD_ANON_34._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_34))
CTD_ANON_34._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_34._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_34._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_34._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'description')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_34._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_34._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_36._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), BindType, scope=CTD_ANON_36, documentation=u'same as uidRef in attributes'))

CTD_ANON_36._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'time'), CTD_ANON_3, scope=CTD_ANON_36, documentation=u'time domain independent axis.'))

CTD_ANON_36._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'freqTime'), BindType, scope=CTD_ANON_36, documentation=u'Allowed values: freq, time.  default is time.  indicates if frequency of time domain descriptions.  '))

CTD_ANON_36._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'frequency'), ValueType, scope=CTD_ANON_36, documentation=u'frequency domain independent axis.'))

CTD_ANON_36._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'amplitude'), CTD_ANON_7, scope=CTD_ANON_36, documentation=u'amplitude dependent axis.'))
CTD_ANON_36._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_36._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_36._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'freqTime')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_36._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'amplitude')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_36._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'time')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_36._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'frequency')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_36._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_36._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objUidRef'), BindType, scope=CTD_ANON_37, documentation=u'UID of the object (subject or transducer, or probable subject).  local id of the subject if multiple ids are used to associate with each cell of  the logical structure.  '))

CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling'), CTD_ANON_10, scope=CTD_ANON_37, documentation=u'the CFSubSampling can be used for chipping part of a large dataArry out and for reducing the number of points within an array for which to associate modeling parameters.  there is one sub sampling element set of points for each component structure (col, row, plane).    index numbers of col, row or plane position within the CFs are listed for which corresponding modeling points will be associated.  sample points are separated by commas, ranges are indicated by ... between numbers which indicates a continuous interval for a single sample. interpolation between samples uses logical structure.  '))

CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_37, documentation=u'name of the object'))

CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objLocalID'), BindType, scope=CTD_ANON_37, documentation=u'if localId assigned to objUidRef for building CF of obj to data (i.e.CF) relationships. Sequence of values is the same as the sequence in the data (logical data structure or subsampled data structure, if present)'))

CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objType'), BindType, scope=CTD_ANON_37, documentation=u'identify object as a transducer or a subject. Allowed Values: subject, transducer. Default: subject'))

CTD_ANON_37._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'confidence'), BindType, scope=CTD_ANON_37, documentation=u'Value range -1 to 1.  -1 is 100% no confidence.  confidence values match same sequence as logical data structure or subsampled data structure, if present (if multiple objects in data structure)'))
CTD_ANON_37._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'objType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'objUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'objLocalID')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_37._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'confidence')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_37._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_37._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_38._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'property'), pyxb.binding.datatypes.anyType, scope=CTD_ANON_38))
CTD_ANON_38._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_38._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'property')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_38._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_38._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_40._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'serialNumber'), BindType, scope=CTD_ANON_40))

CTD_ANON_40._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ownedBy'), CTD_ANON_41, scope=CTD_ANON_40))

CTD_ANON_40._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'manufacture'), BindType, scope=CTD_ANON_40))

CTD_ANON_40._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'modelNumber'), BindType, scope=CTD_ANON_40))
CTD_ANON_40._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_40._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_40._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_40._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_40._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'complexity')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_40._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'characterization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_40._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'calibration')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_40._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_40._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'manufacture')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_40._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'modelNumber')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_40._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'serialNumber')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_40._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ownedBy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_40._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_40._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_40._GroupModel_2, min_occurs=1, max_occurs=1)
    )
CTD_ANON_40._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_40._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_41._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'email'), BindType, scope=CTD_ANON_41))

CTD_ANON_41._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'phone'), BindType, scope=CTD_ANON_41))

CTD_ANON_41._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_41))

CTD_ANON_41._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'date'), BindType, scope=CTD_ANON_41, documentation=u'ISO8601 dateTime stamp'))

CTD_ANON_41._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'organization'), BindType, scope=CTD_ANON_41))
CTD_ANON_41._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_41._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_41._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'organization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_41._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'email')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_41._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'phone')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_41._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'date')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_41._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_41._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_42._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'cfDataArray'), DataArrayType, scope=CTD_ANON_42, documentation=u'logical data structure of the characteristic frame.  Lowest frequency array first.'))

CTD_ANON_42._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ldsDimensionality'), BindType, scope=CTD_ANON_42, documentation=u'Allowed values: 0, 1, 2, 3.  Default is 0.  dimensionality of the logical data structure (lds).  number of structure components used for giving hints for data representation.  0 dim is a single value, 1 dim is a series of columns, rows or planes, 2 dim is any order of  two structure components (col-row, col-plane, or row-plane), and a 3 dim is any order of three structure components col-row-plane'))

CTD_ANON_42._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_42, documentation=u'name of lds'))

CTD_ANON_42._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=CTD_ANON_42, documentation=u'uid of lds'))

CTD_ANON_42._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numOfDataSetsInCf'), BindType, scope=CTD_ANON_42, documentation=u'Number of dataSets or dataArrays in the Characteristic Frame.  Allowed Value: positive integer.  Default:1'))
CTD_ANON_42._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_42._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_42._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_42._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ldsDimensionality')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_42._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numOfDataSetsInCf')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_42._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'cfDataArray')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_42._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_42._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_43._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'serialNumber'), BindType, scope=CTD_ANON_43))

CTD_ANON_43._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ownedBy'), CTD_ANON_46, scope=CTD_ANON_43))

CTD_ANON_43._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'processVersion'), BindType, scope=CTD_ANON_43))

CTD_ANON_43._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'manufacture'), BindType, scope=CTD_ANON_43))

CTD_ANON_43._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'modelNumber'), BindType, scope=CTD_ANON_43))
CTD_ANON_43._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_43._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_43._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_43._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'description')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_43._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'complexity')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_43._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'characterization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_43._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'calibration')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_43._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_43._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'manufacture')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_43._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'modelNumber')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_43._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'serialNumber')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_43._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'processVersion')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_43._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ownedBy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_43._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_43._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_43._GroupModel_2, min_occurs=1, max_occurs=1)
    )
CTD_ANON_43._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_43._GroupModel, min_occurs=0L, max_occurs=1)



CTD_ANON_44._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'frequencyResponse'), CTD_ANON_4, scope=CTD_ANON_44, documentation=u'one for each dataUnit and for each type of freqResp (carrier, modulation, and powerSpectrialDensity) and each type of plot amp vs freq and phase vs freq (can combine plots onto one as well)'))

CTD_ANON_44._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'impulseResponse'), CTD_ANON_36, scope=CTD_ANON_44, documentation=u'time domain or frequency domain impulse characteristics for linear time invariant transforms. May have a separate response for each dataUnit and for each type (freq and time).  Or dataUnits within a data Set may share the same response.'))

CTD_ANON_44._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'steadyStateResponse'), CTD_ANON_53, scope=CTD_ANON_44, documentation=u'input to output  mapping.  one or more mappings for each dataUnit.  Can have property-property, property-data, or data-property mappings.  property-property-property and property-property-data mappings are also allowed as long as independent property values can be found somewhere.  Separate mappings can be used for different hystersis directions or for non-continuous or broken functions.'))

CTD_ANON_44._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling'), CTD_ANON_10, scope=CTD_ANON_44, documentation=u'the CFSubSampling can be used for chipping part of a large dataArry out and for reducing the number of points within an array for which to associate modeling parameters.  there is one sub sampling element set of points for each component structure (col, row, plane).    index numbers of col, row or plane position within the CFs are listed for which corresponding modeling points will be associated.  sample points are separated by commas, ranges are indicated by ... between numbers which indicates a continuous interval for a single sample. interpolation between samples uses logical structure.  '))
CTD_ANON_44._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_44._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_44._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'steadyStateResponse')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_44._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'impulseResponse')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_44._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'frequencyResponse')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_44._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_44._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_45._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'latencyTime'), ValueType, scope=CTD_ANON_45, documentation=u'latency time in seconds (real number).  Time between the input and the output.  Transducer time tags should be corrected to reflect correct input time for receivers and output time for transmitters.  Latency for processes reflects the process delay.  Latency time does not vary over the CF.  Only one value. '))

CTD_ANON_45._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'ambiguityTime'), CTD_ANON_82, scope=CTD_ANON_45, documentation=u'data integration time for each sample in the CF. Each dataunit may have a different time.   This element contains the number of samples in a CF or the number indicated by the noOfSubSampledIndexPoints element in the CFsubSamplingSequence or just one time.  If just one time then the same time applies to all sample in the CF.'))

CTD_ANON_45._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'cfDuration'), ValueType, scope=CTD_ANON_45, documentation=u'time duration of the CF in seconds.  Can also be determined by the CF offset time values by subtracting the smallest offset time from the largest offset time.  Duration does not vary over the CF.  Only one value.'))

CTD_ANON_45._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'cfTrigger'), CTD_ANON_81, scope=CTD_ANON_45))

CTD_ANON_45._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'cfOffsetTime'), CTD_ANON_83, scope=CTD_ANON_45, documentation=u'cfOffSetTime contains time offsets for each dataUnit or dataSet in the CF relative to the clock attribute (clk or dateTime) in the data start tag.  contains the number of time values indicated by the numSubSampledIndexPoints in the cfSubSampling child element. or num'))
CTD_ANON_45._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_45._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'cfTrigger')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_45._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'cfDuration')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_45._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'latencyTime')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_45._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'ambiguityTime')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_45._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'cfOffsetTime')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_45._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_45._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_46._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'email'), BindType, scope=CTD_ANON_46))

CTD_ANON_46._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'date'), BindType, scope=CTD_ANON_46, documentation=u'ISO8601 dateTime stamp'))

CTD_ANON_46._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_46))

CTD_ANON_46._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'organization'), BindType, scope=CTD_ANON_46))

CTD_ANON_46._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'phone'), BindType, scope=CTD_ANON_46))
CTD_ANON_46._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_46._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_46._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'organization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_46._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'email')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_46._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'phone')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_46._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'date')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_46._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_46._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_47._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), pyxb.binding.datatypes.string, scope=CTD_ANON_47, documentation=u'name of the object'))

CTD_ANON_47._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dirIndirSubj'), BindType, scope=CTD_ANON_47, documentation=u'if objType is subject then identify if direct or indirect subject.  Allowed values: direct, indirect.  Default is direct.'))

CTD_ANON_47._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objType'), BindType, scope=CTD_ANON_47, documentation=u'identify object as a transducer or a subject. Allowed Values: subject, transducer. Default: subject'))

CTD_ANON_47._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objUidRef'), BindType, scope=CTD_ANON_47, documentation=u'UID of the subject (or probable subject).  local id of the subject if multiple ids are used to associate with each cell of  the logical structure.  Sequence of values is the same as the sequence in the data (logical data structure)'))
CTD_ANON_47._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_47._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_47._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'objType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_47._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dirIndirSubj')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_47._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'objUidRef')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_47._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_47._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_48._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'headerAttrib'), CTD_ANON_64, scope=CTD_ANON_48, documentation=u'ref, reference, dateTime, contents and ismClass attributes will be encoded and handled as "string" type'))
CTD_ANON_48._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_48._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'headerAttrib')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_48._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_48._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_49._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataValue'), BindType, scope=CTD_ANON_49, documentation=u'fixed or forced input value not.  single value or array defined by logical data structure '))

CTD_ANON_49._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'inputIdent'), CTD_ANON_, scope=CTD_ANON_49))

CTD_ANON_49._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'logicalDataStructure'), CTD_ANON_42, scope=CTD_ANON_49, documentation=u'the logical structure of data (i.e. of the characteristic frame).  This is not necessarily the structure or order that data is communicated in.  The transmission order is defined in the cluster description.  The transmission order is defined relative to the logical order.'))
CTD_ANON_49._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_49._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'inputIdent')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_49._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'logicalDataStructure')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_49._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataValue')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_49._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_49._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_50._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subject'), CTD_ANON_32, scope=CTD_ANON_50, documentation=u'This is the subject (object, thing) that relates to the phenomenon (property) that is affected or detected by the transducer. The relation between a subject and transducer data or subject and subject is described in the relationship element. An empty subject tag in a data stream indicates that this object is no longer a part of the system'))
CTD_ANON_50._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_50._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'subject')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_50._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_50._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_51._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'transducer'), TransducerType, scope=CTD_ANON_51, documentation=u'A transducer can be a stand alone object or part of a system.  An empty transducer tag in a data stream indicates that this transducer is no longer a part of the system'))
CTD_ANON_51._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_51._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'transducer')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_51._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_51._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_52._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_52))

CTD_ANON_52._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), CTD_ANON_28, scope=CTD_ANON_52, documentation=u'UID of the data (live or archived).  Archived data streams will have a UID indicative of the data source, time, and clk count of the start. '))

CTD_ANON_52._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'value'), BindType, scope=CTD_ANON_52))
CTD_ANON_52._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_52._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_52._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_52._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_52._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_52._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'value')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_52._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_52._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_53._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'code'), CTD_ANON_30, scope=CTD_ANON_53, documentation=u'computer code of the transfer process from input to output'))

CTD_ANON_53._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'propValues'), CTD_ANON_66, scope=CTD_ANON_53, documentation=u'values for the physical property (phenomenon) axis of the input output transfer function'))

CTD_ANON_53._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'responseParameters'), CTD_ANON_55, scope=CTD_ANON_53))

CTD_ANON_53._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataValues'), CTD_ANON_29, scope=CTD_ANON_53, documentation=u'values for the data axis of the input output transfer function'))
CTD_ANON_53._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_53._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'responseParameters')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_53._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'propValues')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_53._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataValues')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_53._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'code')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_53._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_53._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_54._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'tapPointUidRef'), BindType, scope=CTD_ANON_54, documentation=u'dataUidRef of the tap point in the system to which this cluster corresponds.  UID of the transducer, process input process output, or connection node from which or to which this cluster relates.  This is the UID used in the data header (i.e. reference attribute in data start tag).  Is some cases a data in a single cluster may come from multiple dataUid tap points.'))

CTD_ANON_54._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'localID'), BindType, scope=CTD_ANON_54, documentation=u'short ID used in the data header (i.e. ref attribute in data start tag)'))
CTD_ANON_54._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_54._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'tapPointUidRef')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_54._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'localID')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_54._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_54._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_55._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'intraCfInterpolate'), BindType, scope=CTD_ANON_55, documentation=u'Allowed values: continuous, discrete, lastValue, returnToZero.  how to interpolate between data values within a CF.  default continuous'))

CTD_ANON_55._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'proportional'), BindType, scope=CTD_ANON_55, documentation=u'For uncalibrated responses is the output proportional to the input? true of false. Mult factors can also reflect prop or inversely prop for calibrated responses. Default: true.'))

CTD_ANON_55._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'codePlot'), BindType, scope=CTD_ANON_55, documentation=u'Allowed values code, plot. Default: plot'))

CTD_ANON_55._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'linear'), BindType, scope=CTD_ANON_55, documentation=u'allowed values: true or false.  do not need explicit Phen plot values if linear is true. Phen and data mult and offset can be used if there are no limits.  default true'))

CTD_ANON_55._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'hysteresisDirection'), BindType, scope=CTD_ANON_55, documentation=u'allowed values: increasing, decreasing, both.  default both'))

CTD_ANON_55._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'invertability'), BindType, scope=CTD_ANON_55, documentation=u'a process input can be determined from its output. Allowed Values: true, false.  default true'))

CTD_ANON_55._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'interCfInterpolate'), BindType, scope=CTD_ANON_55, documentation=u"Allowed values: continuous, discrete, lastValue, returnToZero.  how to interpolate between corresponding data values between adjacent CF's.  default is continuous"))

CTD_ANON_55._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'calibrated'), BindType, scope=CTD_ANON_55, documentation=u'Is response calibrated, or is response a relative reading? true of false. Default: true'))

CTD_ANON_55._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'timeInvariant'), BindType, scope=CTD_ANON_55, documentation=u'a time shift in the input only results in a time shift in the output. Allowed Values: true, false.  default true'))
CTD_ANON_55._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_55._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'codePlot')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_55._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'hysteresisDirection')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_55._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'calibrated')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_55._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'proportional')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_55._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'invertability')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_55._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'timeInvariant')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_55._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'linear')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_55._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'interCfInterpolate')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_55._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'intraCfInterpolate')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_55._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_55._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_56._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'propToPropRelation'), CTD_ANON_62, scope=CTD_ANON_56, documentation=u'Property to property relation or phenomenon to phenomenon relation. transmitter to receiver, Ambient to receiver, Example: thermal to voltage transducer connected to a voltage to data transducer.  example optical filter on the front of an optical camera lens'))

CTD_ANON_56._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'positionRelation'), CTD_ANON_31, scope=CTD_ANON_56, documentation=u'For describing positional relations of subjects external to a system.  An empty posRelation tag in a data indicates that this uidRef relation is no longer exist'))

CTD_ANON_56._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objToObjRelation'), CTD_ANON_22, scope=CTD_ANON_56, documentation=u'This relation describes object to object relations. Attaching a transducer to an object (object is a subject or a transducer) (i.e. dangle, where the only thing the transducer interfaces to is that subject. (cant different individual data many measures with many individual subjects, see objToData). The transducer to transducers relation does not include phenomenon to phenomenon connections, see dataToData'))

CTD_ANON_56._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'timeRelation'), CTD_ANON_60, scope=CTD_ANON_56, documentation=u'Identifies the absolute time reference for each sysClk.  Default is any time reference in a cluster represents absolute time relating to the corresponding clock value.  An empty timeRelation tag in a data stream indicates that this uidRef relation is no longer a part of the system'))

CTD_ANON_56._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objToDataRelation'), CTD_ANON_23, scope=CTD_ANON_56, documentation=u'Connects transducer to bindUids.  Associate transducer data to a (remote) object.  This may occur after data acquisition. An object is either a transducer, subject or their properties.    Many subjects may be related to data in a dataArray. The objects can be related to data units, sets and arrays to subjects.  '))

CTD_ANON_56._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataToDataRelation'), CTD_ANON_70, scope=CTD_ANON_56, documentation=u'Connects bindUIDs to processes. connects outputs to inputs. transducer data to processes and processes to processes.  An empty connect tag in a data stream indicates that this UID relation is no longer a part of the system. Example of data to data relation.  attaching a process to monitor the state of the gain parameter on the steady state response through a bindUID point.  '))
CTD_ANON_56._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_56._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'positionRelation')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_56._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'timeRelation')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_56._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'objToObjRelation')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_56._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'objToDataRelation')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_56._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataToDataRelation')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_56._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'propToPropRelation')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_56._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_56._GroupModel, min_occurs=0L, max_occurs=None)



CTD_ANON_57._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_57))

CTD_ANON_57._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'phone'), BindType, scope=CTD_ANON_57))

CTD_ANON_57._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'date'), BindType, scope=CTD_ANON_57, documentation=u'ISO8601 dateTime stamp'))

CTD_ANON_57._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'email'), BindType, scope=CTD_ANON_57))

CTD_ANON_57._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'organization'), BindType, scope=CTD_ANON_57))
CTD_ANON_57._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_57._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_57._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'organization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_57._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'email')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_57._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'phone')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_57._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'date')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_57._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_57._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_58._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'clusterSize'), BindType, scope=CTD_ANON_58, documentation=u'Integer number of bytes in Cluster'))

CTD_ANON_58._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'direction'), BindType, scope=CTD_ANON_58, documentation=u'Allowed Values: fromSystem, toSystem.  default fromSystem'))

CTD_ANON_58._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'complexity'), BindType, scope=CTD_ANON_58, documentation=u'indication of the complexity of handling this data. Allowed Values: 1A - 1F, 2A -2F, 3A - 3F, 4A - 4F, 5A - 5F.  default 1A'))

CTD_ANON_58._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'clusterType'), BindType, scope=CTD_ANON_58, documentation=u'Allowed values: binary, packedXML.  verboseXML. default binary'))
CTD_ANON_58._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_58._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'direction')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_58._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'complexity')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_58._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'clusterType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_58._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'clusterSize')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_58._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_58._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_59._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), CTD_ANON_61, scope=CTD_ANON_59, documentation=u'UID of the data reference.  Archived data streams will have a UID indicative of the data source, time, and clk count of the start. '))

CTD_ANON_59._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_59))
CTD_ANON_59._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_59._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_59._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_59._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_59._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_60._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'timeCoordinate'), CTD_ANON_65, scope=CTD_ANON_60))

CTD_ANON_60._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'timeReference'), BindType, scope=CTD_ANON_60, documentation=u'time Datum.  Allowed Values: UTC, other,  Default UTC.'))

CTD_ANON_60._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'sysClkUidRef'), BindType, scope=CTD_ANON_60, documentation=u'UID of the sysClk.  Default: Uid of system clock which transducer is contained in.'))
CTD_ANON_60._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_60._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'sysClkUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_60._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'timeReference')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_60._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'timeCoordinate')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_60._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_60._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_62._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'propagationMedium'), BindType, scope=CTD_ANON_62, documentation=u'If the P-to-P interface has a distance between them, then this describes the medium in which the energy propagates.  Allowed values: vacuum, air, water.  default air'))

CTD_ANON_62._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=CTD_ANON_62, documentation=u'connection or node UID of the property relationship'))

CTD_ANON_62._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'relationDescription'), BindType, scope=CTD_ANON_62, documentation=u'longer description of  the property relation'))

CTD_ANON_62._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'propagationMechanism'), BindType, scope=CTD_ANON_62, documentation=u'If the P-to-P interface has a distance between them, then this describes the mechanism in which the energy propagates.  Allowed values: radiation, conduction, convection, osmosis.  default radiation'))

CTD_ANON_62._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'propUidRef'), BindType, scope=CTD_ANON_62, documentation=u'uidRef of the property or phenomenon'))
CTD_ANON_62._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_62._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'relationDescription')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_62._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_62._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'propUidRef')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_62._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'propagationMedium')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_62._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'propagationMechanism')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_62._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_62._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_63._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'otherRelations'), pyxb.binding.datatypes.anyType, scope=CTD_ANON_63))

CTD_ANON_63._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objToObjRelation'), CTD_ANON_22, scope=CTD_ANON_63, documentation=u'This relation describes object to object relations. Attaching a transducer to an object (object is a subject or a transducer) (i.e. dangle, where the only thing the transducer interfaces to is that subject. (cant different individual data many measures with many individual subjects, see objToData). The transducer to transducers relation does not include phenomenon to phenomenon connections, see dataToData'))

CTD_ANON_63._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'objToDataRelation'), CTD_ANON_23, scope=CTD_ANON_63, documentation=u'Connects transducer to bindUids.  Associate transducer data to a (remote) object.  This may occur after data acquisition. An object is either a transducer, subject or their properties.    Many subjects may be related to data in a dataArray. The objects can be related to data units, sets and arrays to subjects.  '))
CTD_ANON_63._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_63._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'objToObjRelation')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_63._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'objToDataRelation')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_63._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'otherRelations')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_63._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_63._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_64._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataType'), BindType, scope=CTD_ANON_64, documentation=u'Allowed values: text, number.  Default is number. '))

CTD_ANON_64._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'encode'), BindType, scope=CTD_ANON_64, documentation=u'Allowed values: ucs16, utf8, signInt, unsignInt, real,  bcd.  default unsignInt. '))

CTD_ANON_64._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUnitFieldSize'), CTD_ANON_67, scope=CTD_ANON_64))

CTD_ANON_64._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numBase'), BindType, scope=CTD_ANON_64, documentation=u'when numbers are encoded as text the number base must be understood.  Allowed values: 2, 8, 10, 16, 32, 64, 128.  default 10'))

CTD_ANON_64._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'headerAttribName'), BindType, scope=CTD_ANON_64, documentation=u'Allowed values: ref, clk, reference, dateTime, contents, seq, total, ismClass. Default ref'))

CTD_ANON_64._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'endian'), BindType, scope=CTD_ANON_64, documentation=u'Allowed values: big, little.  default little'))

CTD_ANON_64._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'handleAsType'), BindType, scope=CTD_ANON_64, documentation=u'how should the text or number be handled in the client application.  Allowed values: anuURI, boolean, byte, double, float, short, string, int, integer, long, nonNegativeInteger, nonPositiveInteger, positiveInteger,  unsignedByte, unsignedInt, unsignedShort, unsignedLong.'))
CTD_ANON_64._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_64._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'headerAttribName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_64._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_64._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUnitFieldSize')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_64._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'endian')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_64._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'encode')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_64._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numBase')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_64._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'handleAsType')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_64._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_64._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_65._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'absTimeUidRef'), BindType, scope=CTD_ANON_65, documentation=u'dataUid reference of the sensor measurements providing the absolute time reference.'))

CTD_ANON_65._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'timeCoordType'), BindType, scope=CTD_ANON_65, documentation=u'Allowed values: dateTime,  year, mo, day, hour, min, sec. Default: dateTime (ISO 8601)'))
CTD_ANON_65._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_65._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'timeCoordType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_65._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'absTimeUidRef')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_65._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_65._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_66._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'direction'), BindType, scope=CTD_ANON_66, documentation=u'if the physical property (phenomenon) had a direction associated with it such as torque or force. direction relative to the transducer reference system.  Allowed Values: horizontal, vertical, +xTranslation, -xTranslation, +yTranslation, -yTranslation, +zTranslation, -zTranslation, +alpha, -alpha, +beta, -beta, +rhoTranslation, -rhoTranslation, +latTranslation, -latTranslation, +longTranslation\n-longTranslation, +altTranslation, -altTranslation, +omegaRotation, -omegaRotation, +phiRotation, -phiRotation, +kappaRotation, -kappaRotation, none Default: none'))

CTD_ANON_66._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'propQualifier'), BindType, scope=CTD_ANON_66, documentation=u'Qualifier for the property.  From Qualifier Dictionary.  e.g. aveValue, rmsValue, rssValue, instValue, accumulatedValue, rateOfChange, range, min, max...'))

CTD_ANON_66._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'variableName'), BindType, scope=CTD_ANON_66, documentation=u'Name of mathematical term used in the transformation equations.  '))

CTD_ANON_66._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'propName'), CTD_ANON_68, scope=CTD_ANON_66, documentation=u'from Physical Property (Phenomenon) Dictionary'))

CTD_ANON_66._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'UOM'), CTD_ANON_26, scope=CTD_ANON_66, documentation=u'From Units Of Measure Dictionary (SI Units)'))

CTD_ANON_66._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'calibProp'), BindType, scope=CTD_ANON_66, documentation=u'If a calibrated source is available this elements identifies the calibration level or points (bindUID) to the calibrated sensor measuring the source.  This is used for post correcting relative readings Default: none'))

CTD_ANON_66._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'inputOutput'), BindType, scope=CTD_ANON_66, documentation=u'Is the physical property (phenomenon) the input or output for this dataUnit.  Allowed values: input, output.  Default: input'))
CTD_ANON_66._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numValues')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'arrayType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueDataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mult')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offset')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accuracy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_66._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'inputOutput')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'propName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'propQualifier')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'UOM')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'direction')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'variableName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'calibProp')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_66._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_66._GroupModel_, min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_66._GroupModel_2, min_occurs=1, max_occurs=1)
    )
CTD_ANON_66._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_66._GroupModel, min_occurs=0L, max_occurs=None)



CTD_ANON_67._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'beginTextDelimiter'), BindType, scope=CTD_ANON_67, documentation=u'delimiter used to separate variable size dataUnits in cluster when encode is text (utf or ucs). default delimiter is none. empty tag means none.'))

CTD_ANON_67._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numSigBits'), BindType, scope=CTD_ANON_67, documentation=u'number of significant bits. default 8'))

CTD_ANON_67._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'justification'), BindType, scope=CTD_ANON_67, documentation=u'if numSigBits is less than numBits this element indicates how sigbit are justified.  Allowed values: left, right. Default: right'))

CTD_ANON_67._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'endTextDelimiter'), BindType, scope=CTD_ANON_67, documentation=u'delimiter used to separate variable size dataUnits in cluster when encode is text (utf or ucs). default delimiter is none. Empty tag means none'))

CTD_ANON_67._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'numBits'), BindType, scope=CTD_ANON_67, documentation=u'number of bits. default 8 '))
CTD_ANON_67._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_67._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numBits')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_67._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numSigBits')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_67._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'justification')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_67._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_67._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'beginTextDelimiter')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_67._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'endTextDelimiter')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_67._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(CTD_ANON_67._GroupModel_, min_occurs=1, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_67._GroupModel_2, min_occurs=1, max_occurs=1)
    )
CTD_ANON_67._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_67._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_69._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'clusterDesc'), CTD_ANON_12, scope=CTD_ANON_69, documentation=u'An empty clusterdesc tag in a data stream indicates that this cluster is no longer contained in the data stream.'))
CTD_ANON_69._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_69._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'clusterDesc')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_69._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_69._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_70._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'relationDescription'), BindType, scope=CTD_ANON_70, documentation=u'longer description of the signal or the property relation'))

CTD_ANON_70._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataSource'), CTD_ANON_52, scope=CTD_ANON_70, documentation=u'data source'))

CTD_ANON_70._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=CTD_ANON_70, documentation=u'connection or node UID of the connection signal data relationship'))

CTD_ANON_70._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataSink'), CTD_ANON_59, scope=CTD_ANON_70, documentation=u'data sink'))
CTD_ANON_70._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_70._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'relationDescription')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_70._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_70._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataSource')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_70._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataSink')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_70._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_70._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_71._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'spaceLocCoords'), CTD_ANON_76, scope=CTD_ANON_71, documentation=u'one set of coordinates for each spatial axes.  Each shape is defined relative to an arbitrary data spatial reference system. '))

CTD_ANON_71._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'spaceCoordSystem'), BindType, scope=CTD_ANON_71, documentation=u'Allowed values: spherical,  rectangular, cylindrical, wgs84elliptical.  default is spherical.'))

CTD_ANON_71._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'pwrProfile'), CTD_ANON_17, scope=CTD_ANON_71, documentation=u'The equi-power surface power level compared to the point of transmission or reception.   default is -3db beam pattern, pwrProfile="-3".'))
CTD_ANON_71._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_71._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'pwrProfile')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_71._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spaceCoordSystem')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_71._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spaceLocCoords')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_71._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_71._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_72._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'property'), pyxb.binding.datatypes.anyType, scope=CTD_ANON_72))
CTD_ANON_72._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_72._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'property')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_72._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_72._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_73._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'date'), BindType, scope=CTD_ANON_73, documentation=u'ISO8601 dateTime stamp'))

CTD_ANON_73._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_73))

CTD_ANON_73._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'organization'), BindType, scope=CTD_ANON_73))

CTD_ANON_73._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'email'), BindType, scope=CTD_ANON_73))

CTD_ANON_73._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'phone'), BindType, scope=CTD_ANON_73))
CTD_ANON_73._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_73._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_73._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'organization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_73._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'email')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_73._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'phone')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_73._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'date')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_73._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_73._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_75._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'insituRemote'), BindType, scope=CTD_ANON_75, documentation=u'allowed values: insitu, remote.  Default is insitu.'))

CTD_ANON_75._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'spatialDependancy'), BindType, scope=CTD_ANON_75, documentation=u'Allowed values: attitudeIndependent (default), locationIndependent, positionalIndependent, positionalDependent'))

CTD_ANON_75._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'transmitterReceiver'), BindType, scope=CTD_ANON_75, documentation=u'allowed values: transmitter, receiver, transceiver.  default is receiver.'))
CTD_ANON_75._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_75._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'transmitterReceiver')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_75._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'insituRemote')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_75._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spatialDependancy')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_75._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_75._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_76._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'coordName'), BindType, scope=CTD_ANON_76, documentation=u'Allowed values: x, y, z, alpha, beta, rho.  '))

CTD_ANON_76._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'coords'), ValueType, scope=CTD_ANON_76, documentation=u'values contains a string of real numbers.  The mult and offset are single values, unless the shape varies over the Characteristic Frame then the mult and offset may contain a Characteristic Frame array of values. simple IFOV alpha=0, beta=0.  (ray where rho is infinite)'))
CTD_ANON_76._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_76._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'coordName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_76._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'coords')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_76._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_76._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_77._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_77, documentation=u'name of dataUnit'))

CTD_ANON_77._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'variableName'), BindType, scope=CTD_ANON_77, documentation=u'Name of mathematical term used in the transformation equations.  Index of component is the order in the sequence in the LDS structure.'))

CTD_ANON_77._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataType'), BindType, scope=CTD_ANON_77, documentation=u'Allowed values: number, complexNumber, text, or binaryBlob.  default is number'))

CTD_ANON_77._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=CTD_ANON_77, documentation=u'uid of dataUnit'))

CTD_ANON_77._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'bytesInBlob'), BindType, scope=CTD_ANON_77, documentation=u'If dataType is binaryBlob then number of bytes in the binary blob.  Not used for transducer structures, only for process structures.'))
CTD_ANON_77._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_77._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_77._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_77._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'variableName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_77._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_77._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'bytesInBlob')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_77._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_77._GroupModel, min_occurs=1, max_occurs=1)


CTD_ANON_78._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_78._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spaceCoordSystem')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_78._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spaceRefSystem')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_78._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'refObjUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_78._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'spaceCoords')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_78._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_78._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_80._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'coordName'), BindType, scope=CTD_ANON_80, documentation=u'Allowed Values: x, y, z, Alpha, beta, rho, latitude, longitude, altitude, omega, phi, kappa,'))

CTD_ANON_80._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'coords'), ValueType, scope=CTD_ANON_80))

CTD_ANON_80._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'posVelAccel'), BindType, scope=CTD_ANON_80, documentation=u'Allowed Values: pos, vel, accel,  Default is pos.'))
CTD_ANON_80._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_80._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'posVelAccel')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_80._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'coordName')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_80._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'coords')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_80._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_80._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_81._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'period'), ValueType, scope=CTD_ANON_81, documentation=u'if private trigger is periodic then,  trigger period in seconds'))

CTD_ANON_81._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'publicTrigger'), BindType, scope=CTD_ANON_81, documentation=u'if trigger is public then this identifies the uidRef of trigger source (command).  Whenever a data cluster is sent to this UID or to the uid of a process that is bound to this uid then this transducer or process cycle will trigger.  The bindUid enables late binding of the trigger source'))

CTD_ANON_81._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'trigType'), BindType, scope=CTD_ANON_81, documentation=u'Allowed Values: private, privateOnDataRecipt, privateOnInputTrig, pvtOnChgOutput.   publicOnTrigReciept.   public trigger: controllable by external commands. private trigger: uncontrollable by external commands.  Virtual trig sensor puts sysClk time in data tag.  If public a bindUid is made available.  default trigger is privatePeriodic.'))
CTD_ANON_81._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_81._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'trigType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_81._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'publicTrigger')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_81._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'period')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_81._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_81._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_82._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling'), CTD_ANON_10, scope=CTD_ANON_82, documentation=u'the CFSubSampling can be used for chipping part of a large dataArry out and for reducing the number of points within an array for which to associate modeling parameters.  there is one sub sampling element set of points for each component structure (col, row, plane).    index numbers of col, row or plane position within the CFs are listed for which corresponding modeling points will be associated.  sample points are separated by commas, ranges are indicated by ... between numbers which indicates a continuous interval for a single sample. interpolation between samples uses logical structure.  '))

CTD_ANON_82._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), BindType, scope=CTD_ANON_82, documentation=u'corresponding UID of dataUnit or dataSet. Duplicate of uid in identification element Default: Uid of dataSet'))
CTD_ANON_82._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_82._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numValues')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_82._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'arrayType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_82._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_82._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueDataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_82._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_82._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mult')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_82._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offset')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_82._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accuracy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_82._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_82._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_82._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_82._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_82._GroupModel_, min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_82._GroupModel_2, min_occurs=1, max_occurs=1)
    )
CTD_ANON_82._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_82._GroupModel, min_occurs=0L, max_occurs=None)



CTD_ANON_83._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef'), BindType, scope=CTD_ANON_83, documentation=u'corresponding UID of dataUnit or dataSet. Duplicate of uid in identification element Default: Uid of dataSet'))

CTD_ANON_83._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling'), CTD_ANON_10, scope=CTD_ANON_83, documentation=u'the CFSubSampling can be used for chipping part of a large dataArry out and for reducing the number of points within an array for which to associate modeling parameters.  there is one sub sampling element set of points for each component structure (col, row, plane).    index numbers of col, row or plane position within the CFs are listed for which corresponding modeling points will be associated.  sample points are separated by commas, ranges are indicated by ... between numbers which indicates a continuous interval for a single sample. interpolation between samples uses logical structure.  '))
CTD_ANON_83._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_83._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'numValues')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_83._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'arrayType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_83._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'fcnInterpol')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_83._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'valueDataType')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_83._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'values')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_83._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'mult')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_83._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'offset')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_83._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'accuracy')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_83._GroupModel_2 = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_83._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'dataUidRef')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_83._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'cfSubSampling')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_83._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_83._GroupModel_, min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_83._GroupModel_2, min_occurs=1, max_occurs=1)
    )
CTD_ANON_83._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_83._GroupModel, min_occurs=0L, max_occurs=None)



CTD_ANON_84._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'date'), BindType, scope=CTD_ANON_84, documentation=u'ISO8601 dateTime stamp'))

CTD_ANON_84._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'phone'), BindType, scope=CTD_ANON_84))

CTD_ANON_84._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_84))

CTD_ANON_84._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'email'), BindType, scope=CTD_ANON_84))

CTD_ANON_84._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'organization'), BindType, scope=CTD_ANON_84))
CTD_ANON_84._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_84._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_84._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'organization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_84._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'email')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_84._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'phone')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_84._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'date')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_84._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_84._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_85._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'organization'), BindType, scope=CTD_ANON_85))

CTD_ANON_85._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'phone'), BindType, scope=CTD_ANON_85))

CTD_ANON_85._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_85))

CTD_ANON_85._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'date'), BindType, scope=CTD_ANON_85, documentation=u'ISO8601 dateTime stamp'))

CTD_ANON_85._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'email'), BindType, scope=CTD_ANON_85))
CTD_ANON_85._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_85._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_85._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'organization')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_85._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'email')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_85._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'phone')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_85._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'date')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_85._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_85._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_86._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'sequence'), CTD_ANON_79, scope=CTD_ANON_86, documentation=u'Allowed values; The sequence shall contain a string of value separated by a comma.  Each value can be a positive integer or a range.  ranges shall be indicated by two integer numbers separated by three sequential decimal points (....) to indicate a run from the first number to the second'))

CTD_ANON_86._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'inThisDataStruct'), BindType, scope=CTD_ANON_86, documentation=u'Sequence of the data structure components identified in the previous element (seqOfThisDataStruct) in the data structure identified in this element (inThisDataStruct). seqOfBitsInUnit,  seqOfUnitsInSets, seqOfSetsInCf, seqOfCfInClust. Identify the dataStructComponent in this element by dataUidRef.  dataUid of the cluster is "cluster"'))

CTD_ANON_86._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'seqOfThisDataStruct'), BindType, scope=CTD_ANON_86, documentation=u'Sequence of (in this element - seqOfThisDataStruct) in the data structure identified in the next element (inThisDataStruct). seqOfBitsInUnit,  seqOfUnitsInSets, seqOfSetsInCf, seqOfCfInClust. Identify the dataStructComponent in this element by dataUidRef.  dataUid of the cluster is "cluster"'))
CTD_ANON_86._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_86._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'seqOfThisDataStruct')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_86._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'inThisDataStruct')), min_occurs=0L, max_occurs=None),
    pyxb.binding.content.ParticleModel(CTD_ANON_86._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'sequence')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_86._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_86._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_87._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'period'), ValueType, scope=CTD_ANON_87, documentation=u'Period in seconds'))

CTD_ANON_87._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'max'), BindType, scope=CTD_ANON_87, documentation=u'max counter count which roll over occurs'))

CTD_ANON_87._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'uid'), BindType, scope=CTD_ANON_87, documentation=u'sysClk UID same as the system UID.  There is only one clock per system.  Subsystems may have clocks'))

CTD_ANON_87._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'countNumBase'), BindType, scope=CTD_ANON_87, documentation=u'number base in which clock characters increment.  Allowed values are: 2, 8, 10, 16.  Default is 10'))

CTD_ANON_87._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'min'), BindType, scope=CTD_ANON_87, documentation=u'counter starting point after rollover.  default 0'))

CTD_ANON_87._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'name'), BindType, scope=CTD_ANON_87))
CTD_ANON_87._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_87._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'uid')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_87._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'name')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_87._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'period')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_87._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'countNumBase')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_87._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'min')), min_occurs=0L, max_occurs=1),
    pyxb.binding.content.ParticleModel(CTD_ANON_87._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'max')), min_occurs=0L, max_occurs=1)
    )
CTD_ANON_87._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_87._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_88._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'property'), pyxb.binding.datatypes.anyType, scope=CTD_ANON_88))
CTD_ANON_88._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_88._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'property')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_88._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_88._GroupModel, min_occurs=1, max_occurs=1)



CTD_ANON_89._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'system'), SystemType, scope=CTD_ANON_89, documentation=u'An empty system tag (with id) in a data stream indicates that the system is no longer available in the stream, or if system was not previously part of the parent system it will be added to the parent system.'))
CTD_ANON_89._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(CTD_ANON_89._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'system')), min_occurs=0L, max_occurs=None)
    )
CTD_ANON_89._ContentModel = pyxb.binding.content.ParticleModel(CTD_ANON_89._GroupModel, min_occurs=1, max_occurs=1)
