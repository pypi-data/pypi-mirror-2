from StringIO import StringIO

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
class %(name)s(Interface):
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
        """
'''

STANDARD_TYPE_NAMESPACES = [
    'http://schemas.xmlsoap.org/soap/encoding/',
    'http://schemas.xmlsoap.org/wsdl/',
    'http://www.w3.org/2001/XMLSchema'
]

SCHEMA_TYPE_MAPPING = {
    'boolean':              'schema.Bool(description=u"WSDL type: %(typeName)s")',
    'string':               'schema.TextLine(description=u"WSDL type: %(typeName)s")',
    
    'long':                 'schema.Int(description=u"WSDL type: %(typeName)s")',
    'int':                  'schema.Int(description=u"WSDL type: %(typeName)s")',
    'short':                'schema.Int(description=u"WSDL type: %(typeName)s")',
    'byte':                 'schema.Int(description=u"WSDL type: %(typeName)s")',
    
    'unsignedLong':         'schema.Int(min=0, description=u"WSDL type: %(typeName)s")',
    'unsignedInt':          'schema.Int(min=0, description=u"WSDL type: %(typeName)s")',
    'unsignedShort':        'schema.Int(min=0, description=u"WSDL type: %(typeName)s")',
    'unsignedByte':         'schema.Int(min=0, description=u"WSDL type: %(typeName)s")',
    
    'positiveInteger':      'schema.Int(min=1, description=u"WSDL type: %(typeName)s")',
    'nonPositiveInteger':   'schema.Int(max=0, description=u"WSDL type: %(typeName)s")',
    'negativeInteger':      'schema.Int(max=-1, description=u"WSDL type: %(typeName)s")',
    'nonNegativeInteger':   'schema.Int(min=0, description=u"WSDL type: %(typeName)s")',
    
    'float':                'schema.Float(description=u"WSDL type: %(typeName)s")',
    'double':               'schema.Float(description=u"WSDL type: %(typeName)s")',
    
    'decimal':              'schema.Decimal(description=u"WSDL type: %(typeName)s")',
    
    'duration':             'schema.Timedelta(description=u"WSDL type: %(typeName)s")',
    'dateTime':             'schema.Datetime(description=u"WSDL type: %(typeName)s")',
    'date':                 'schema.Date(description=u"WSDL type: %(typeName)s")',
    
    'anyURI':               'schema.URI(description=u"WSDL type: %(typeName)s")',
    'token':                'schema.ASCIILine(description=u"WSDL type: %(typeName)s")',
    'normalizedString':     'schema.TextLine(description=u"WSDL type: %(typeName)s")',
    
    'base64Binary':         'schema.Bytes(description=u"WSDL type: %(typeName)s")',
    'hexBinary':            'schema.Bytes(description=u"WSDL type: %(typeName)s")',
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

def generate(client, url=None, standardTypeNamespaces=STANDARD_TYPE_NAMESPACES):
    """Given a WSDL URL, return a file that could become your interfaces.py
    """
    
    out = StringIO()
    
    for sd in client.sd:
        print >>out, HEADER % dict(
                wsdl=url,
            )
        
        # Types
        
        typeMapItems = []
        
        for type_ in sd.types:
            
            resolved = type_[0].resolve()
            namespaceURL = resolved.namespace()[1]
            if namespaceURL not in standardTypeNamespaces:
                
                if resolved.enum():
                    typeDescription = "enumeration"
                else:
                    typeDescription = "complex type"
                
                rawTypeName = typeName(type_[0], sd, interface=False)
                typeInterfaceName = interfaceName(typeName(type_[0], sd, interface=False)).replace(':', '_')
                
                typeMapItems.append((rawTypeName, typeInterfaceName,))
                
                print >>out, INTERFACE % dict(
                        name=normalizeIdentifier(typeInterfaceName),
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
                        print >>out, "    %s = Attribute('Enumeration value')" % name
                else:
                    for attr in type_[0].children():
                        name = attr[0].name.replace(' ', '_')
                        attrTypeName = typeName(attr[0], sd)
                        
                        schemaType = SCHEMA_TYPE_MAPPING.get(attrTypeName)
                        if schemaType is None:
                            schemaType = "Attribute('Type: %s')" % attrTypeName
                        else:
                            schemaType = schemaType % dict(typeName=attrTypeName)
                        
                        print >>out, "    %s = %s" % (normalizeIdentifier(name), schemaType,)
                
                print >>out
        
        print >>out, TYPE_MAP % dict(
                items=',\n'.join(["    '%s': %s" % k for k in typeMapItems])
            )
        
        print >>out
        
        # Main service interface
        
        print >>out, INTERFACE % dict(
                name=normalizeIdentifier(interfaceName(sd.service.name)),
                docstring=formatDocstring(SERVICE_INTERFACE_DOCSTRING % dict(
                        serviceName=sd.service.name,
                        tns=sd.wsdl.tns[1],
                    )
                )
            )
        
        methods = {} # name -> list of parameters
        for p in sd.ports:
            for m in p[1]:
                if m[0] not in methods:
                    methods[m[0]] = m[1]
        
        for methodName in sorted(methods):
            methodArgNames = [m[0] for m in methods[methodName]]
            
            methodArgDetails = []
            for m in methods[methodName]:
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
            
            print >>out, METHOD % dict(
                    name=normalizeIdentifier(methodName),
                    args=', '.join(methodArgNames),
                )
            
            print >>out, METHOD_DOCSTRING % dict(args='\n        '.join(methodArgDetails)),
            
            print >>out
            
    return out.getvalue()

def main():
    if len(sys.argv) < 2:
        print "Usage: %s <url>" % sys.argv[0]
        print "The output will be printed to the console"
        return
    
    client = suds.client.Client(sys.argv[1])
    print generate(client, sys.argv[1])

if __name__ == '__main__':
    main()
