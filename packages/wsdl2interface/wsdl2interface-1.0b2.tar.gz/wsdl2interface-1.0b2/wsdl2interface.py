from StringIO import StringIO

import os.path
import sys
import textwrap
import keyword
import re

import suds.client

VALID_IDENTIFIER_RE                   = re.compile(r"[_A-Za-z][_A-Za-z1-9]*")
VALID_IDENTIFIER_FIRST_LETTER_RE      = re.compile(r"[_A-Za-z]")
VALID_IDENTIFIER_SUBSEQUENT_LETTER_RE = re.compile(r"[_A-Za-z1-9]")

HEADER = '''\
"""SOAP web services generated from:
%(wsdl)s.
"""

from zope.interface import Interface, Attribute
from zope import schema
'''

INTERFACE = '''\
class %(name)s(%(bases)s):
    """%(docstring)s"""
'''

SERVICE_INTERFACE_DOCSTRING = '''\
SOAP service ``%(serviceName)s`` with target namespace %(tns)s.
'''

TYPE_INTERFACE_DOCSTRING = '''\
SOAP %(type)s ``{%(namespace)s}%(name)s``
'''

TYPE_MAP = '''\
WSDL_TYPES = {
%(items)s
}
'''

METHOD = '''    def %(name)s(%(args)s):'''

METHOD_DOCSTRING = '''\
        """Parameters:
        
        %(args)s
        
        Returns: %(response)s
        """
'''

STANDARD_TYPE_NAMESPACES = [
    'http://schemas.xmlsoap.org/soap/encoding/',
    'http://schemas.xmlsoap.org/wsdl/',
    'http://www.w3.org/2001/XMLSchema'
]

SCHEMA_TYPE_MAPPING = {
    None:                   "Attribute('Type: %(typeName)s. Required: %(required)s')",
    
    'boolean':              'schema.Bool(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'string':               'schema.TextLine(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    
    'long':                 'schema.Int(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'int':                  'schema.Int(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'short':                'schema.Int(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'byte':                 'schema.Int(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    
    'unsignedLong':         'schema.Int(min=0, description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'unsignedInt':          'schema.Int(min=0, description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'unsignedShort':        'schema.Int(min=0, description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'unsignedByte':         'schema.Int(min=0, description=u"WSDL type: %(typeName)s", required=%(required)s)',
    
    'positiveInteger':      'schema.Int(min=1, description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'nonPositiveInteger':   'schema.Int(max=0, description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'negativeInteger':      'schema.Int(max=-1, description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'nonNegativeInteger':   'schema.Int(min=0, description=u"WSDL type: %(typeName)s", required=%(required)s)',
    
    'float':                'schema.Float(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'double':               'schema.Float(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    
    'decimal':              'schema.Decimal(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    
    'duration':             'schema.Timedelta(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'dateTime':             'schema.Datetime(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'date':                 'schema.Date(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    
    'anyURI':               'schema.URI(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'token':                'schema.ASCIILine(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'normalizedString':     'schema.TextLine(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    
    'base64Binary':         'schema.Bytes(description=u"WSDL type: %(typeName)s", required=%(required)s)',
    'hexBinary':            'schema.Bytes(description=u"WSDL type: %(typeName)s", required=%(required)s)',
}


def formatDocstring(text, indent=4, colwidth=78):
    width = colwidth - indent
    joiner = '\n' + ' ' * indent
    return joiner.join(textwrap.wrap(text, width) + [''])

def interfaceName(name):
    name = name[0].upper() + name[1:]
    return 'I' + name

def typeName(type, sd, interface=True):
    resolved = type.resolve()
    name = resolved.name
    
    if not name:
        name = ''
    
    if type.unbounded():
        name += '[]'
    
    ns = resolved.namespace()
    if ns[1] in STANDARD_TYPE_NAMESPACES or not interface:
        return name
    
    return interfaceName(name)

def normalizeIdentifier(identifier):
    if not VALID_IDENTIFIER_RE.match(identifier):
        newIdentifierLetters = []
        firstLetter = True
        for letter in identifier:
            if firstLetter:
                if VALID_IDENTIFIER_FIRST_LETTER_RE.match(letter):
                    newIdentifierLetters.append(letter)
                else:
                    newIdentifierLetters.append('_')
                firstLetter = False
            else:
                if VALID_IDENTIFIER_SUBSEQUENT_LETTER_RE.match(letter):
                    newIdentifierLetters.append(letter)
                else:
                    newIdentifierLetters.append('_')
        identifier = ''.join(newIdentifierLetters)
    
    if keyword.iskeyword(identifier):
        identifier = identifier + '_'
    
    return identifier

def generate(client, url=None, standardTypeNamespaces=STANDARD_TYPE_NAMESPACES, removeInputOutputMesssages=True):
    """Given a WSDL URL, return a file that could become your interfaces.py
    """
    
    printed = [] # sequence of type name -> string
    
    for sd in client.sd:
        
        serviceOut = StringIO()
        
        print >>serviceOut, HEADER % dict(
                wsdl=url,
            )
        
        printed.append(('', serviceOut.getvalue(),))
        
        # Types
        
        typeMap = {}
        typeSeq = []
        typeAttributes = {}
        
        for type_ in sd.types:
            
            typeOut = StringIO()
            
            resolved = type_[0].resolve()
            namespaceURL = resolved.namespace()[1]
            if namespaceURL not in standardTypeNamespaces:
                
                if resolved.enum():
                    typeDescription = "enumeration"
                else:
                    typeDescription = "complex type"
                
                # Look for basess
                interfaceBases = []
                if resolved.extension():
                    def find(t):
                        for c in t.rawchildren:
                            if c.extension():
                                find(c)
                            if c.ref is not None:
                                interfaceBases.append(interfaceName(c.ref[0]))
                    find(resolved)
                    
                if not interfaceBases:
                    interfaceBases = ['Interface']
                
                rawTypeName = typeName(type_[0], sd, interface=False)
                typeInterfaceName = interfaceName(typeName(type_[0], sd, interface=False)).replace(':', '_')
                
                typeMap[rawTypeName] = typeInterfaceName
                typeSeq.append((rawTypeName, typeInterfaceName,))
                typeAttributes[rawTypeName] = {}
                
                print >>typeOut, INTERFACE % dict(
                        name=normalizeIdentifier(typeInterfaceName),
                        bases=', '.join(interfaceBases),
                        docstring=formatDocstring(TYPE_INTERFACE_DOCSTRING % dict(
                                type=typeDescription,
                                name=rawTypeName,
                                namespace=namespaceURL,
                            )
                        )
                    )
                
                if resolved.enum():
                    for attr in type_[0].children():
                        name = attr[0].name.replace(' ', '_')
                        print >>typeOut, "    %s = Attribute('Enumeration value')" % name
                else:
                    for attr in type_[0].children():
                        name = attr[0].name.replace(' ', '_')
                        attrTypeName = typeName(attr[0], sd)
                        typeAttributes[rawTypeName][name] = attrTypeName
                        required = attr[0].required()
                        
                        schemaType = SCHEMA_TYPE_MAPPING.get(attrTypeName)
                        if schemaType is None:
                            schemaType = SCHEMA_TYPE_MAPPING[None]
                        
                        schemaType = schemaType % dict(typeName=attrTypeName, required=required)
                        
                        print >>typeOut, "    %s = %s" % (normalizeIdentifier(name), schemaType,)
                
                print >>typeOut
                
                printed.append((rawTypeName, typeOut.getvalue(),))
        
        serviceInterfaceOut = StringIO()
        
        # Main service interface
        print >>serviceInterfaceOut, INTERFACE % dict(
                name=normalizeIdentifier(interfaceName(sd.service.name)),
                bases=u"Interface",
                docstring=formatDocstring(SERVICE_INTERFACE_DOCSTRING % dict(
                        serviceName=sd.service.name,
                        tns=sd.wsdl.tns[1],
                    )
                )
            )
        
        methods = {} # name -> (response type, list of parameters,)
        
        for p in sd.ports:
            for m in p[1]:
                methodName = m[0]
                methodArgs = m[1]
                if methodName not in methods:
                    methodDef = p[0].method(methodName)
                    
                    # XXX: This is discards the namespace part
                    if methodDef.soap.output.body.wrapped:
                        
                        inputMessage  = methodDef.soap.input.body.parts[0].element[0]
                        outputMessage = methodDef.soap.output.body.parts[0].element[0]
                        
                        if outputMessage in typeAttributes:
                            if len(typeAttributes[outputMessage]) > 0:
                                response = typeAttributes[outputMessage].values()[0]
                            else:
                                response = "None"
                        else:
                            response = outputMessage
                        
                        # Remove types used as input/output messages
                        if removeInputOutputMesssages:
                            remove = False
                            for idx, (t, x) in enumerate(printed):
                                if t == inputMessage:
                                    remove = True
                                    break
                            if remove:
                                del printed[idx]
                                if inputMessage in typeMap:
                                    del typeMap[inputMessage]
                            
                            remove = False
                            for idx, (t, x) in enumerate(printed):
                                if t == outputMessage:
                                    remove = True
                                    break
                            if remove:
                                del printed[idx]
                                if outputMessage in typeMap:
                                    del typeMap[outputMessage]
                        
                    else:
                        response = methodDef.soap.output.body.parts[0].element[0]
                    
                    methods[methodName] = (response, methodArgs,)
        
        for methodName in sorted(methods):
            
            methodArgNames = [m[0] for m in methods[methodName][1]]
            methodReturnType = methods[methodName][0]
            
            methodArgDetails = []
            for m in methods[methodName][1]:
                argDetail = m[1]
                
                methodModifierParts = []
                
                if not argDetail.required():
                    methodModifierParts.append('optional')
                if argDetail.nillable:
                    methodModifierParts.append('may be None')
                
                methodModifiers = ""
                if methodModifierParts:
                    methodModifiers = ' (%s)' % ', '.join(methodModifierParts)
                
                argTypeName = typeName(argDetail, sd)
                
                methodSpec = "``%s`` -- %s%s" % (
                        argDetail.name,
                        argTypeName,
                        methodModifiers
                    )
                
                methodArgDetails.append(methodSpec)
            
            print >>serviceInterfaceOut, METHOD % dict(
                    name=normalizeIdentifier(methodName),
                    args=', '.join(methodArgNames),
                )
            
            if methodReturnType in typeMap:
                methodReturnType = interfaceName(methodReturnType)
            
            print >>serviceInterfaceOut, METHOD_DOCSTRING % dict(
                    args='\n        '.join(methodArgDetails),
                    response=methodReturnType,
                )
            
            print >>serviceInterfaceOut
    
        printed.append((sd.service.name, serviceInterfaceOut.getvalue(),))
        
        typeMapOut = StringIO()
        print >>typeMapOut, TYPE_MAP % dict(
                items=',\n'.join(["    '%s': %s" % k for k in typeSeq if k[0] in typeMap])
            )
        print >>typeMapOut
        printed.append(('', typeMapOut.getvalue(),))
    
    return '\n'.join([v[1] for v in printed])

def main():
    if len(sys.argv) < 2:
        print "Usage: %s <url>" % sys.argv[0]
        print "The output will be printed to the console"
        return
    
    if not '://' in sys.argv[1]:
        sys.argv[1] = 'file://' + os.path.abspath(sys.argv[1])
    
    client = suds.client.Client(sys.argv[1])
    print generate(client, sys.argv[1])

if __name__ == '__main__':
    main()
