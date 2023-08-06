# ./pyxb/bundles/opengis/raw/_dc.py
# PyXB bindings for NM:fde543a00b9681daae05bbc5a17f3dce9cfacb0c
# Generated 2011-09-09 14:19:15.800259 by PyXB version 1.1.3
# Namespace http://purl.org/dc/elements/1.1/ [xmlns:dc]

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
import pyxb.binding.datatypes

Namespace = pyxb.namespace.NamespaceForURI(u'http://purl.org/dc/elements/1.1/', create_if_missing=True)
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


# Complex type SimpleLiteral with content type MIXED
class SimpleLiteral (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_MIXED
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'SimpleLiteral')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute scheme uses Python identifier scheme
    __scheme = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, u'scheme'), 'scheme', '__httppurl_orgdcelements1_1_SimpleLiteral_scheme', pyxb.binding.datatypes.anyURI)
    
    scheme = property(__scheme.value, __scheme.set, None, None)

    _HasWildcardElement = True

    _ElementMap = {
        
    }
    _AttributeMap = {
        __scheme.name() : __scheme
    }
Namespace.addCategoryObject('typeBinding', u'SimpleLiteral', SimpleLiteral)


# Complex type elementContainer with content type ELEMENT_ONLY
class elementContainer (pyxb.binding.basis.complexTypeDefinition):
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, u'elementContainer')
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://purl.org/dc/elements/1.1/}DC-element uses Python identifier DC_element
    __DC_element = pyxb.binding.content.ElementUse(pyxb.namespace.ExpandedName(Namespace, u'DC-element'), 'DC_element', '__httppurl_orgdcelements1_1_elementContainer_httppurl_orgdcelements1_1DC_element', True)

    
    DC_element = property(__DC_element.value, __DC_element.set, None, None)


    _ElementMap = {
        __DC_element.name() : __DC_element
    }
    _AttributeMap = {
        
    }
Namespace.addCategoryObject('typeBinding', u'elementContainer', elementContainer)


DC_element = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DC-element'), SimpleLiteral, abstract=pyxb.binding.datatypes.boolean(1))
Namespace.addCategoryObject('elementBinding', DC_element.name().localName(), DC_element)

creator = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'creator'), SimpleLiteral, documentation=u'An entity primarily responsible for making the content of the resource.\n      Examples of Creator include a person, an organization, or a service. \n      Typically, the name of a Creator should be used to indicate the entity.')
Namespace.addCategoryObject('elementBinding', creator.name().localName(), creator)

description = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'description'), SimpleLiteral, documentation=u'An account of the content of the resource. Examples of Description \n      include, but are not limited to, an abstract, table of contents, \n      reference to a graphical representation of content, or free-text \n      account of the content.')
Namespace.addCategoryObject('elementBinding', description.name().localName(), description)

subject = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'subject'), SimpleLiteral, documentation=u'A topic of the content of the resource. Typically, Subject will be \n      expressed as keywords, key phrases, or classification codes that \n      describe a topic of the resource. Recommended best practice is to \n      select a value from a controlled vocabulary or formal classification \n      scheme.')
Namespace.addCategoryObject('elementBinding', subject.name().localName(), subject)

contributor = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'contributor'), SimpleLiteral, documentation=u'An entity responsible for making contributions to the content of \n      the resource. Examples of Contributor include a person, an organization, \n      or a service. Typically, the name of a Contributor should be used to \n      indicate the entity.')
Namespace.addCategoryObject('elementBinding', contributor.name().localName(), contributor)

title = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'title'), SimpleLiteral, documentation=u'A name given to the resource. Typically, Title will be a name by \n      which the resource is formally known.')
Namespace.addCategoryObject('elementBinding', title.name().localName(), title)

type = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'type'), SimpleLiteral, documentation=u'The nature or genre of the content of the resource. Type includes \n      terms describing general categories, functions, genres, or aggregation \n      levels for content. Recommended best practice is to select a value \n      from a controlled vocabulary (for example, the DCMI Type Vocabulary). \n      To describe the physical or digital manifestation of the resource, \n      use the Format element.')
Namespace.addCategoryObject('elementBinding', type.name().localName(), type)

coverage = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'coverage'), SimpleLiteral, documentation=u'The extent or scope of the content of the resource. Typically, \n      Coverage will include spatial location (a place name or geographic \n      coordinates), temporal period (a period label, date, or date range), \n      or jurisdiction (such as a named administrative entity). Recommended \n      best practice is to select a value from a controlled vocabulary \n      (for example, the Thesaurus of Geographic Names [TGN]) and to use, \n      where appropriate, named places or time periods in preference to \n      numeric identifiers such as sets of coordinates or date ranges.')
Namespace.addCategoryObject('elementBinding', coverage.name().localName(), coverage)

identifier = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'identifier'), SimpleLiteral, documentation=u'An unambiguous reference to the resource within a given context. \n      Recommended best practice is to identify the resource by means of a \n      string or number conforming to a formal identification system. Formal \n      identification systems include but are not limited to the Uniform \n      Resource Identifier (URI) (including the Uniform Resource Locator \n      (URL)), the Digital Object Identifier (DOI), and the International \n      Standard Book Number (ISBN).')
Namespace.addCategoryObject('elementBinding', identifier.name().localName(), identifier)

date = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'date'), SimpleLiteral, documentation=u'A date of an event in the lifecycle of the resource. Typically, Date \n      will be associated with the creation or availability of the resource. \n      Recommended best practice for encoding the date value is defined in a \n      profile of ISO 8601 and includes (among others) dates of the \n      form YYYY-MM-DD.')
Namespace.addCategoryObject('elementBinding', date.name().localName(), date)

source = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'source'), SimpleLiteral, documentation=u'A Reference to a resource from which the present resource is derived.\n      The present resource may be derived from the Source resource in whole \n      or in part. Recommended best practice is to identify the referenced \n      resource by means of a string or number conforming to a formal \n      identification system.')
Namespace.addCategoryObject('elementBinding', source.name().localName(), source)

language = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'language'), SimpleLiteral, documentation=u'A language of the intellectual content of the resource. Recommended \n      best practice is to use RFC 3066, which, in conjunction with ISO 639, \n      defines two- and three-letter primary language tags with optional \n      subtags. Examples include "en" or "eng" for English, "akk" for\n      Akkadian, and "en-GB" for English used in the United Kingdom.')
Namespace.addCategoryObject('elementBinding', language.name().localName(), language)

rights = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'rights'), SimpleLiteral, documentation=u'Information about rights held in and over the resource. Typically, \n      Rights will contain a rights management statement for the resource, \n      or reference a service providing such information. Rights information \n      often encompasses Intellectual Property Rights (IPR), Copyright, and \n      various Property Rights. If the Rights element is absent, no \n      assumptions may be made about any rights held in or over the resource.')
Namespace.addCategoryObject('elementBinding', rights.name().localName(), rights)

relation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'relation'), SimpleLiteral, documentation=u'A reference to a related resource. Recommended best practice is to \n      identify the referenced resource by means of a string or number \n      conforming to a formal identification system.')
Namespace.addCategoryObject('elementBinding', relation.name().localName(), relation)

publisher = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'publisher'), SimpleLiteral, documentation=u'An entity responsible for making the resource available. Examples of \n      Publisher include a person, an organization, or a service. Typically, \n      the name of a Publisher should be used to indicate the entity.')
Namespace.addCategoryObject('elementBinding', publisher.name().localName(), publisher)

format = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'format'), SimpleLiteral, documentation=u'The physical or digital manifestation of the resource. Typically, \n      Format will include the media-type or dimensions of the resource. \n      Format may be used to identify the software, hardware, or other \n      equipment needed to display or operate the resource. Examples of \n      dimensions include size and duration. Recommended best practice is to \n      select a value from a controlled vocabulary (for example, the list \n      of Internet Media Types defining computer media formats).')
Namespace.addCategoryObject('elementBinding', format.name().localName(), format)


SimpleLiteral._GroupModel = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), min_occurs=0L, max_occurs=0L)
    )
SimpleLiteral._ContentModel = pyxb.binding.content.ParticleModel(SimpleLiteral._GroupModel, min_occurs=1, max_occurs=1)



elementContainer._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, u'DC-element'), SimpleLiteral, abstract=pyxb.binding.datatypes.boolean(1), scope=elementContainer))
elementContainer._GroupModel_2 = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(elementContainer._UseForTag(pyxb.namespace.ExpandedName(Namespace, u'DC-element')), min_occurs=1, max_occurs=1)
    )
elementContainer._GroupModel_ = pyxb.binding.content.GroupSequence(
    pyxb.binding.content.ParticleModel(elementContainer._GroupModel_2, min_occurs=0L, max_occurs=None)
    )
elementContainer._GroupModel = pyxb.binding.content.GroupChoice(
    pyxb.binding.content.ParticleModel(elementContainer._GroupModel_, min_occurs=1, max_occurs=1)
    )
elementContainer._ContentModel = pyxb.binding.content.ParticleModel(elementContainer._GroupModel, min_occurs=1, max_occurs=1)

creator._setSubstitutionGroup(DC_element)

description._setSubstitutionGroup(DC_element)

subject._setSubstitutionGroup(DC_element)

contributor._setSubstitutionGroup(DC_element)

title._setSubstitutionGroup(DC_element)

type._setSubstitutionGroup(DC_element)

coverage._setSubstitutionGroup(DC_element)

identifier._setSubstitutionGroup(DC_element)

date._setSubstitutionGroup(DC_element)

source._setSubstitutionGroup(DC_element)

language._setSubstitutionGroup(DC_element)

rights._setSubstitutionGroup(DC_element)

relation._setSubstitutionGroup(DC_element)

publisher._setSubstitutionGroup(DC_element)

format._setSubstitutionGroup(DC_element)
