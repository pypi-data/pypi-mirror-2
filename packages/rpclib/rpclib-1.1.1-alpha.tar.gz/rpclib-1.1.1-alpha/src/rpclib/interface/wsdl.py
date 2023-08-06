
#
# rpclib - Copyright (C) Rpclib contributors.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#

import logging
logger = logging.getLogger(__name__)

import shutil
import tempfile

from lxml import etree

import rpclib
from rpclib.model.exception import Fault
from rpclib.interface.base import Base

class ValidationError(Fault):
    pass

def add_port_type(service, interface, root, service_name, types, url, port_type):
    ns_wsdl = rpclib.ns_wsdl

    # FIXME: I don't think this call is working.
    cb_port_type = _add_callbacks(service, root, types, service_name, url)

    for method in service.public_methods:
        if method.is_callback:
            operation = etree.SubElement(cb_port_type, '{%s}operation'
                                                        % ns_wsdl)
        else:
            operation = etree.SubElement(port_type,'{%s}operation'% ns_wsdl)

        operation.set('name', method.name)

        if method.doc is not None:
            documentation = etree.SubElement(operation, '{%s}documentation'
                                                            % ns_wsdl)
            documentation.text = method.doc

        operation.set('parameterOrder', method.in_message.get_type_name())

        op_input = etree.SubElement(operation, '{%s}input' % ns_wsdl)
        op_input.set('name', method.in_message.get_type_name())
        op_input.set('message', method.in_message.get_type_name_ns(interface))

        if (not method.is_callback) and (not method.is_async):
            op_output = etree.SubElement(operation, '{%s}output' %  ns_wsdl)
            op_output.set('name', method.out_message.get_type_name())
            op_output.set('message', method.out_message.get_type_name_ns(interface))

# FIXME: I don't think this is working.
def _add_callbacks(service, root, types, service_name, url):
    ns_xsd = rpclib.ns_xsd
    ns_wsa = rpclib.ns_wsa
    pref_wsa = rpclib.const_prefmap[rpclib.ns_wsa]

    ns_wsdl = rpclib.ns_wsdl
    ns_soap = rpclib.ns_soap

    ns_tns = service.get_tns()
    pref_tns = 'tns'

    cb_port_type = None

    # add necessary async headers
    # WS-Addressing -> RelatesTo ReplyTo MessageID
    # callback porttype
    if service._has_callbacks():
        wsa_schema = etree.SubElement(types, "{%s}schema" % ns_xsd)
        wsa_schema.set("targetNamespace", '%sCallback'  % ns_tns)
        wsa_schema.set("elementFormDefault", "qualified")

        import_ = etree.SubElement(wsa_schema, "{%s}import" % ns_xsd)
        import_.set("namespace", ns_wsa)
        import_.set("schemaLocation", ns_wsa)

        relt_message = etree.SubElement(root, '{%s}message' % ns_wsdl)
        relt_message.set('name', 'RelatesToHeader')
        relt_part = etree.SubElement(relt_message, '{%s}part' % ns_wsdl)
        relt_part.set('name', 'RelatesTo')
        relt_part.set('element', '%s:RelatesTo' % pref_wsa)

        reply_message = etree.SubElement(root, '{%s}message' % ns_wsdl)
        reply_message.set('name', 'ReplyToHeader')
        reply_part = etree.SubElement(reply_message, '{%s}part' % ns_wsdl)
        reply_part.set('name', 'ReplyTo')
        reply_part.set('element', '%s:ReplyTo' % pref_wsa)

        id_header = etree.SubElement(root, '{%s}message' % ns_wsdl)
        id_header.set('name', 'MessageIDHeader')
        id_part = etree.SubElement(id_header, '{%s}part' % ns_wsdl)
        id_part.set('name', 'MessageID')
        id_part.set('element', '%s:MessageID' % pref_wsa)

        # make portTypes
        cb_port_type = etree.SubElement(root, '{%s}portType' % ns_wsdl)
        cb_port_type.set('name', '%sCallback' % service_name)

        cb_service_name = '%sCallback' % service_name

        cb_service = etree.SubElement(root, '{%s}service' % ns_wsdl)
        cb_service.set('name', cb_service_name)

        cb_wsdl_port = etree.SubElement(cb_service, '{%s}port' % ns_wsdl)
        cb_wsdl_port.set('name', cb_service_name)
        cb_wsdl_port.set('binding', '%s:%s' % (pref_tns, cb_service_name))

        cb_address = etree.SubElement(cb_wsdl_port, '{%s}address'
                                                          % ns_soap)
        cb_address.set('location', url)

    return cb_port_type

def _add_message_for_object(self, app, root, messages, obj):
    if obj != None and not (obj.get_type_name() in messages):
        messages.add(obj.get_type_name())

        message = etree.SubElement(root, '{%s}message' % rpclib.ns_wsdl)
        message.set('name', obj.get_type_name())

        part = etree.SubElement(message, '{%s}part' % rpclib.ns_wsdl)
        part.set('name', obj.get_type_name())
        part.set('element', obj.get_type_name_ns(app))

def add_messages_for_methods(service, app, root, messages):
    for method in service.public_methods:
        _add_message_for_object(service, app, root, messages,method.in_message)
        _add_message_for_object(service, app, root, messages,method.out_message)
        _add_message_for_object(service, app, root, messages,method.in_header)
        _add_message_for_object(service, app, root, messages,method.out_header)

def add_bindings_for_methods(service, app, root, service_name,
                                    binding, transport, cb_binding=None):
    '''Adds bindings to the wsdl

    @param the root element of the wsdl
    @param the name of this service
    '''

    ns_wsdl = rpclib.ns_wsdl
    ns_soap = rpclib.ns_soap
    pref_tns = app.get_namespace_prefix(service.get_tns())

    if service._has_callbacks():
        if cb_binding is None:
            cb_binding = etree.SubElement(root, '{%s}binding' % ns_wsdl)
            cb_binding.set('name', '%sCallback' % service_name)
            cb_binding.set('type', 'typens:%sCallback' % service_name)

        soap_binding = etree.SubElement(cb_binding, '{%s}binding' % ns_soap)
        soap_binding.set('transport', transport)

    for method in service.public_methods:
        operation = etree.Element('{%s}operation' % ns_wsdl)
        operation.set('name', method.name)

        soap_operation = etree.SubElement(operation, '{%s}operation' %
                                                                   ns_soap)
        soap_operation.set('soapAction', method.public_name)
        soap_operation.set('style', 'document')

        # get input
        input = etree.SubElement(operation, '{%s}input' % ns_wsdl)
        input.set('name', method.in_message.get_type_name())

        soap_body = etree.SubElement(input, '{%s}body' % ns_soap)
        soap_body.set('use', 'literal')

        # get input soap header
        in_header = method.in_header
        if in_header is None:
            in_header = service.__in_header__

        if not (in_header is None):
            soap_header = etree.SubElement(input, '{%s}header' % ns_soap)
            soap_header.set('use', 'literal')
            soap_header.set('message', in_header.get_type_name_ns(app))
            soap_header.set('part', in_header.get_type_name())

        if not (method.is_async or method.is_callback):
            output = etree.SubElement(operation, '{%s}output' % ns_wsdl)
            output.set('name', method.out_message.get_type_name())

            soap_body = etree.SubElement(output, '{%s}body' % ns_soap)
            soap_body.set('use', 'literal')

            # get input soap header
            out_header = method.in_header
            if out_header is None:
                out_header = service.__in_header__

            if not (out_header is None):
                soap_header = etree.SubElement(output, '{%s}header' %
                                                                    ns_soap)
                soap_header.set('use', 'literal')
                soap_header.set('message', out_header.get_type_name_ns(app))
                soap_header.set('part', out_header.get_type_name())


        if method.is_callback:
            relates_to = etree.SubElement(input, '{%s}header' % ns_soap)

            relates_to.set('message', '%s:RelatesToHeader' % pref_tns)
            relates_to.set('part', 'RelatesTo')
            relates_to.set('use', 'literal')

            cb_binding.append(operation)

        else:
            if method.is_async:
                rt_header = etree.SubElement(input,'{%s}header' % ns_soap)
                rt_header.set('message', '%s:ReplyToHeader' % pref_tns)
                rt_header.set('part', 'ReplyTo')
                rt_header.set('use', 'literal')

                mid_header = etree.SubElement(input, '{%s}header'% ns_soap)
                mid_header.set('message', '%s:MessageIDHeader' % pref_tns)
                mid_header.set('part', 'MessageID')
                mid_header.set('use', 'literal')

            binding.append(operation)

    return cb_binding

class Wsdl11(Base):
    def __init__(self, parent, services, tns, name=None, _with_partnerlink=False):
        '''Constructor.

        @param An iterable of ServiceBase subclasses that define the exposed
               services.
        @param The targetNamespace attribute of the exposed service.
        @param The name attribute of the exposed service.
        @param Flag to indicate whether to generate partnerlink node in wsdl.
        '''

        Base.__init__(self, parent, services, tns, name)
        
        self._with_plink = _with_partnerlink
        self.__wsdl = None

    def build_schema_nodes(self, types=None):
        retval = {}
        
        for pref in self.namespaces:
            schema = self.get_schema_node(pref, types, retval)

            # append import tags
            for namespace in self.imports[pref]:
                import_ = etree.SubElement(schema, "{%s}import" % rpclib.ns_xsd)
                import_.set("namespace", namespace)
                if types is None:
                    import_.set('schemaLocation', "%s.xsd" %
                                           self.get_namespace_prefix(namespace))

            # append element tags
            for node in self.namespaces[pref].elements.values():
                schema.append(node)

            # append simpleType and complexType tags
            for node in self.namespaces[pref].types.values():
                schema.append(node)

        return retval

    def get_schema_document(self):
        """Simple accessor method that caches application's xml schema, once
        generated.

        Not meant to be overridden.
        """
        if self.schema is None:
            return self.populate_interface()
        else:
            return self.schema

    def get_interface_document(self, url):
        """Simple accessor method that caches the wsdl of the application, once
        generated.

        Not meant to be overridden.
        """
        if self.__wsdl is None:
            return self.__build_wsdl(url)
        else:
            return self.__wsdl

    def get_schema_node(self, pref, types, schema_nodes):
        """Return schema node for the given namespace prefix.

        types == None means the call is for creating a standalone xml schema
                      file for one single namespace.
        types != None means the call is for creating the wsdl file.
        """

        # create schema node
        if not (pref in schema_nodes):
            if types is None:
                schema = etree.Element("{%s}schema" % rpclib.ns_xsd,
                                                        nsmap=self.nsmap)
            else:
                schema = etree.SubElement(types, "{%s}schema" % rpclib.ns_xsd)

            schema.set("targetNamespace", self.nsmap[pref])
            schema.set("elementFormDefault", "qualified")

            schema_nodes[pref] = schema

        else:
            schema = schema_nodes[pref]

        return schema

    def __build_wsdl(self, url):
        """Build the wsdl for the application.
        """
        ns_wsdl = rpclib.ns_wsdl
        ns_soap = rpclib.ns_soap
        ns_plink = rpclib.ns_plink
        pref_tns = self.get_namespace_prefix(self.tns)

        # FIXME: doesn't look so robust
        url = url.replace('.wsdl', '')

        service_name = self.get_name()

        # create wsdl root node
        root = etree.Element("{%s}definitions" % ns_wsdl, nsmap=self.nsmap)
        root.set('targetNamespace', self.tns)
        root.set('name', service_name)

        # create types node
        types = etree.SubElement(root, "{%s}types" % ns_wsdl)
        self.build_schema_nodes(types)

        messages = set()
        for s in self.services:
            s=self.parent.get_service(s,None)

            add_messages_for_methods(s, self, root, messages)

        if self._with_plink:
            # create plink node
            plink = etree.SubElement(root, '{%s}partnerLinkType' % ns_plink)
            plink.set('name', service_name)
            self.__add_partner_link(service_name, plink)

        # create service node
        service = etree.SubElement(root, '{%s}service' % ns_wsdl)
        service.set('name', service_name)
        self.__add_service(service_name, url, service)

        # create portType node
        port_type = etree.SubElement(root, '{%s}portType' % ns_wsdl)
        port_type.set('name', service_name)

        # create binding nodes
        binding = etree.SubElement(root, '{%s}binding' % ns_wsdl)
        binding.set('name', service_name)
        binding.set('type', '%s:%s'% (pref_tns, service_name))

        soap_binding = etree.SubElement(binding, '{%s}binding' % ns_soap)
        soap_binding.set('style', 'document')

        if self.parent.transport is None:
            raise Exception("You must set the 'transport' property")
        soap_binding.set('transport', self.parent.transport)

        cb_binding = None

        for s in self.services:
            s=self.parent.get_service(s)
            add_port_type(s, self, root, service_name, types, url, port_type)
            cb_binding = add_bindings_for_methods(s, self, root, service_name,
                                                  binding, cb_binding)

        self.__wsdl = etree.tostring(root, xml_declaration=True,
                                                               encoding="UTF-8")

        return self.__wsdl

    def __add_partner_link(self, service_name, plink):
        """Add the partnerLinkType node to the wsdl.
        """
        ns_plink = rpclib.ns_plink
        ns_tns = self.get_tns()
        pref_tns = self.get_namespace_prefix(ns_tns)

        role = etree.SubElement(plink, '{%s}role' % ns_plink)
        role.set('name', service_name)

        plink_port_type = etree.SubElement(role, '{%s}portType' % ns_plink)
        plink_port_type.set('name', '%s:%s' % (pref_tns, service_name))

        if self._has_callbacks():
            role = etree.SubElement(plink, '{%s}role' % ns_plink)
            role.set('name', '%sCallback' % service_name)

            plink_port_type = etree.SubElement(role, '{%s}portType' % ns_plink)
            plink_port_type.set('name', '%s:%sCallback' %
                                                       (pref_tns, service_name))
    def __add_service(self, service_name, url, service):
        """Add service node to the wsdl.
        """
        pref_tns = self.get_namespace_prefix(self.get_tns())

        wsdl_port = etree.SubElement(service, '{%s}port' % rpclib.ns_wsdl)
        wsdl_port.set('name', service_name)
        wsdl_port.set('binding', '%s:%s' % (pref_tns, service_name))

        addr = etree.SubElement(wsdl_port, '{%s}address' % rpclib.ns_soap)
        addr.set('location', url)

    def _has_callbacks(self):
        retval = False

        for s in self.services:
            if self.get_service(s)._has_callbacks():
                return True

        return retval

    def validate(self, payload):
        """Method to be overriden to perform any sort of custom input
        validation.
        """

    def on_exception_object(self, exc):
        '''Called when the app throws an exception. (might be inside or outside
        the service call.

        @param the wsgi environment
        @param the fault object
        '''

    def on_exception_doc(self, fault_doc):
        '''Called when the app throws an exception. (might be inside or outside
        the service call.

        @param the wsgi environment
        @param the xml element containing the xml serialization of the fault
        '''

class Wsdl11Strict(Wsdl11):
    def __init__(self, parent, services, tns, name=None, _with_partnerlink=False):
        Wsdl11.__init__(self, parent, services, tns, name, _with_partnerlink)

        self.schema = self.build_schema()

    def build_schema(self):
        """Build application schema specifically for xml validation purposes."""
        schema_nodes = self.build_schema_nodes()

        pref_tns = self.get_namespace_prefix(self.get_tns())
        logger.debug("generating schema for targetNamespace=%r, prefix: %r"
                                               % (self.get_tns(), pref_tns))

        tmp_dir_name = tempfile.mkdtemp()

        # serialize nodes to files
        for k,v in schema_nodes.items():
            file_name = '%s/%s.xsd' % (tmp_dir_name, k)
            f = open(file_name, 'w')
            etree.ElementTree(v).write(f, pretty_print=True)
            f.close()
            logger.debug("writing %r for ns %s" % (file_name,
                                                        self.nsmap[k]))

        f = open('%s/%s.xsd' % (tmp_dir_name, pref_tns), 'r')

        logger.debug("building schema...")
        schema = etree.XMLSchema(etree.parse(f))
        logger.debug("schema %r built, cleaning up..." % schema)
        f.close()
        shutil.rmtree(tmp_dir_name)
        logger.debug("removed %r" % tmp_dir_name)

        return schema

    def validate(self, payload):
        schema = self.schema
        ret = schema.validate(payload)

        logger.debug("validation result: %s" % str(ret))
        if ret == False:
            err = schema.error_log.last_error

            fault_code = 'Client.SchemaValidation'

            raise ValidationError(fault_code, faultstring=str(err))
