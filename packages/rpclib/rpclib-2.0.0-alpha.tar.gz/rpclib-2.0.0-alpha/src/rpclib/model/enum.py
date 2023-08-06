
from lxml import etree

from rpclib.model import SimpleType
from rpclib.model import nillable_element
from rpclib.model import nillable_value

import rpclib.const.xml_ns

_ns_xsd = rpclib.const.xml_ns.xsd

# adapted from: http://code.activestate.com/recipes/413486/

class EnumBase(SimpleType):
    __namespace__ = None

    @staticmethod
    def resolve_namespace(cls, default_ns):
        if cls.__namespace__ is None:
            cls.__namespace__ = default_ns

    @classmethod
    @nillable_value
    def to_parent_element(cls, value, tns, parent_elt, name='retval'):
        if name is None:
            name = cls.get_type_name()

        SimpleType.to_parent_element(str(value), tns, parent_elt, name)

    @classmethod
    @nillable_element
    def from_xml(cls, element):
        return getattr(cls, element.text)

def Enum(*values, **kwargs):
    type_name = kwargs.get('type_name', None)
    docstr = kwargs.get('__doc__', '')
    if type_name is None:
        raise ValueError("Please specify 'type_name' as a keyword argument")

    assert len(values) > 0, "Empty enums are meaningless"

    maximum = len(values) # to make __invert__ work

    class EnumValue(object):
        __slots__ = ('__value')

        def __init__(self, value):
            self.__value = value

        def __hash__(self):
            return hash(self.__value)

        def __cmp__(self, other):
            assert type(self) is type(other), \
                             "Only values from the same enum are comparable"

            return cmp(self.__value, other.__value)

        def __invert__(self):
            return values[maximum - self.__value]

        def __nonzero__(self):
            return bool(self.__value)

        def __repr__(self):
            return str(values[self.__value])

    class EnumType(EnumBase):
        __doc__ = docstr
        __type_name__ = type_name

        def __iter__(self):
            return iter(values)

        def __len__(self):
            return len(values)

        def __getitem__(self, i):
            return values[i]

        def __repr__(self):
            return 'Enum' + str(enumerate(values))

        def __str__(self):
            return 'enum ' + str(values)

        @classmethod
        def add_to_schema(cls, interface):
            if not interface.has_class(cls):
                simple_type = etree.Element('{%s}simpleType' % _ns_xsd)
                simple_type.set('name', cls.get_type_name())

                restriction = etree.SubElement(simple_type,
                                                    '{%s}restriction' % _ns_xsd)
                restriction.set('base', '%s:string' %
                                        interface.get_namespace_prefix(_ns_xsd))

                for v in values:
                    enumeration = etree.SubElement(restriction,
                                                    '{%s}enumeration' % _ns_xsd)
                    enumeration.set('value', v)

                interface.add_simple_type(cls, simple_type)

    for i,v in enumerate(values):
        setattr(EnumType, v, EnumValue(i))

    return EnumType
