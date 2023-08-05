wsdl2interface
==============

.. contents::

This package provides a simple script to generate the code for
`zope.interface`_ style interfaces based on a WSDL file. It relies on `suds`_
to perform the conversion.

Installation
------------

To install the package, use easy_install, buildout or some other mechanism to
install Python eggs, e.g.::

    $ easy_install -U wsdl2interface

You can also install it as a dependency of another package, e.g. by listing it
in that package's ``setup.py`` ``install_requires`` line.

Usage
-----

By default, ``wsdl2interface``` installs a console script of the same name,
which you can use to print the generated code to the screen. Pass the URL
of a WSDL file (which could be a ``file://`` URL for a local file) as the
only argument::

    $ wsdl2interface http://www.xignite.com/xIndexComponents.asmx?WSDL

The output will look something like this::

    """SOAP web services generated from:
    http://www.xignite.com/xIndexComponents.asmx?WSDL.
    """

    from zope.interface import Interface, Attribute
    from zope import schema


    class IArrayOfComponent(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}ArrayOfComponent``
        """

        Component = Attribute('Type: IComponent[]. Required: False')


    class IArrayOfPricedComponent(Interface):
        """SOAP complex type
        ``{http://www.xignite.com/services/}ArrayOfPricedComponent``
        """

        PricedComponent = Attribute('Type: IPricedComponent[]. Required: False')


    class ICommon(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}Common``
        """

        Outcome = Attribute('Type: IOutcomeTypes. Required: True')
        Message = schema.TextLine(description=u"WSDL type: string", required=False)
        Identity = schema.TextLine(description=u"WSDL type: string", required=False)
        Delay = schema.Float(description=u"WSDL type: double", required=True)


    class IComponent(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}Component``
        """

        Security = Attribute('Type: ISecurity. Required: False')
        Weight = schema.Float(description=u"WSDL type: double", required=True)
        AdjustmentFactor = schema.Float(description=u"WSDL type: double", required=True)
        IndexComponentWeightType = Attribute('Type: IIndexComponentWeightTypes. Required: True')


    class IComponents(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}Components``
        """

        Outcome = Attribute('Type: IOutcomeTypes. Required: True')
        Message = schema.TextLine(description=u"WSDL type: string", required=False)
        Identity = schema.TextLine(description=u"WSDL type: string", required=False)
        Delay = schema.Float(description=u"WSDL type: double", required=True)
        Security = Attribute('Type: ISecurity. Required: False')
        Count = schema.Int(description=u"WSDL type: int", required=True)
        Components = Attribute('Type: IArrayOfComponent. Required: False')


    class IHeader(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}Header``
        """

        Username = schema.TextLine(description=u"WSDL type: string", required=False)
        Password = schema.TextLine(description=u"WSDL type: string", required=False)
        Tracer = schema.TextLine(description=u"WSDL type: string", required=False)


    class IIdentifierTypes(Interface):
        """SOAP enumeration ``{http://www.xignite.com/services/}IdentifierTypes``
        """

        Symbol = Attribute('Enumeration value')
        CIK = Attribute('Enumeration value')
        CUSIP = Attribute('Enumeration value')
        ISIN = Attribute('Enumeration value')
        Valoren = Attribute('Enumeration value')
        SEDOL = Attribute('Enumeration value')


    class IIndexComponentWeightTypes(Interface):
        """SOAP enumeration
        ``{http://www.xignite.com/services/}IndexComponentWeightTypes``
        """

        Unknown = Attribute('Enumeration value')
        MarketCapitalizationWeighted = Attribute('Enumeration value')
        EqualWeighted = Attribute('Enumeration value')
        PriceWeighted = Attribute('Enumeration value')
        MarketCapitalizationWeightedWithLimits = Attribute('Enumeration value')
        OtherWeighting = Attribute('Enumeration value')


    class IOutcomeTypes(Interface):
        """SOAP enumeration ``{http://www.xignite.com/services/}OutcomeTypes``
        """

        Success = Attribute('Enumeration value')
        SystemError = Attribute('Enumeration value')
        RequestError = Attribute('Enumeration value')
        RegistrationError = Attribute('Enumeration value')


    class IPricedComponent(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}PricedComponent``
        """

        Outcome = Attribute('Type: IOutcomeTypes. Required: True')
        Message = schema.TextLine(description=u"WSDL type: string", required=False)
        Identity = schema.TextLine(description=u"WSDL type: string", required=False)
        Delay = schema.Float(description=u"WSDL type: double", required=True)
        Symbol = schema.TextLine(description=u"WSDL type: string", required=False)
        Name = schema.TextLine(description=u"WSDL type: string", required=False)
        Exchange = schema.TextLine(description=u"WSDL type: string", required=False)
        CIK = schema.TextLine(description=u"WSDL type: string", required=False)
        Cusip = schema.TextLine(description=u"WSDL type: string", required=False)
        ISIN = schema.TextLine(description=u"WSDL type: string", required=False)
        SEDOL = schema.TextLine(description=u"WSDL type: string", required=False)
        Valoren = schema.TextLine(description=u"WSDL type: string", required=False)
        Sector = schema.TextLine(description=u"WSDL type: string", required=False)
        Class = schema.TextLine(description=u"WSDL type: string", required=False)
        IndustryGroup = schema.TextLine(description=u"WSDL type: string", required=False)
        Industry = schema.TextLine(description=u"WSDL type: string", required=False)
        Country = schema.TextLine(description=u"WSDL type: string", required=False)
        Currency = schema.TextLine(description=u"WSDL type: string", required=False)
        Style = schema.TextLine(description=u"WSDL type: string", required=False)
        Price = schema.Float(description=u"WSDL type: double", required=True)
        Weight = schema.Float(description=u"WSDL type: double", required=True)
        Value = schema.Float(description=u"WSDL type: double", required=True)
        MarketCapitalization = schema.Float(description=u"WSDL type: double", required=True)
        AdjustmentFactor = schema.Float(description=u"WSDL type: double", required=True)
        IndexComponentWeightType = Attribute('Type: IIndexComponentWeightTypes. Required: True')


    class IPricedComponents(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}PricedComponents``
        """

        Outcome = Attribute('Type: IOutcomeTypes. Required: True')
        Message = schema.TextLine(description=u"WSDL type: string", required=False)
        Identity = schema.TextLine(description=u"WSDL type: string", required=False)
        Delay = schema.Float(description=u"WSDL type: double", required=True)
        Security = Attribute('Type: ISecurity. Required: False')
        Count = schema.Int(description=u"WSDL type: int", required=True)
        AsOfDate = schema.TextLine(description=u"WSDL type: string", required=False)
        Price = schema.Float(description=u"WSDL type: double", required=True)
        Divisor = schema.Float(description=u"WSDL type: double", required=True)
        DivisorDate = schema.TextLine(description=u"WSDL type: string", required=False)
        PricedComponents = Attribute('Type: IArrayOfPricedComponent. Required: False')


    class ISecurity(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}Security``
        """

        Outcome = Attribute('Type: IOutcomeTypes. Required: True')
        Message = schema.TextLine(description=u"WSDL type: string", required=False)
        Identity = schema.TextLine(description=u"WSDL type: string", required=False)
        Delay = schema.Float(description=u"WSDL type: double", required=True)
        CIK = schema.TextLine(description=u"WSDL type: string", required=False)
        Cusip = schema.TextLine(description=u"WSDL type: string", required=False)
        Symbol = schema.TextLine(description=u"WSDL type: string", required=False)
        ISIN = schema.TextLine(description=u"WSDL type: string", required=False)
        Valoren = schema.TextLine(description=u"WSDL type: string", required=False)
        Name = schema.TextLine(description=u"WSDL type: string", required=False)
        Market = schema.TextLine(description=u"WSDL type: string", required=False)
        CategoryOrIndustry = schema.TextLine(description=u"WSDL type: string", required=False)


    class IXigniteIndexComponents(Interface):
        """SOAP service ``XigniteIndexComponents`` with target namespace
        http://www.xignite.com/services/.
        """

        def GetIndexComponents(Identifier, IdentifierType):
            """Parameters:
        
            ``Identifier`` -- string (optional)
            ``IdentifierType`` -- IIdentifierTypes
        
            Returns: GetIndexComponentsResponse
            """


        def GetPricedIndexComponents(Identifier, IdentifierType, AsOfDate):
            """Parameters:
        
            ``Identifier`` -- string (optional)
            ``IdentifierType`` -- IIdentifierTypes
            ``AsOfDate`` -- string (optional)
        
            Returns: GetPricedIndexComponentsResponse
            """


        def GetPricedIndexComponentsSubset(Identifier, IdentifierType, AsOfDate, StartIndex, EndIndex):
            """Parameters:
        
            ``Identifier`` -- string (optional)
            ``IdentifierType`` -- IIdentifierTypes
            ``AsOfDate`` -- string (optional)
            ``StartIndex`` -- int
            ``EndIndex`` -- int
        
            Returns: GetPricedIndexComponentsSubsetResponse
            """



    WSDL_TYPES = {
        'ArrayOfComponent': IArrayOfComponent,
        'ArrayOfPricedComponent': IArrayOfPricedComponent,
        'Common': ICommon,
        'Component': IComponent,
        'Components': IComponents,
        'Header': IHeader,
        'IdentifierTypes': IIdentifierTypes,
        'IndexComponentWeightTypes': IIndexComponentWeightTypes,
        'OutcomeTypes': IOutcomeTypes,
        'PricedComponent': IPricedComponent,
        'PricedComponents': IPricedComponents,
        'Security': ISecurity
    }



If you want to use the generator from Python, you can do::

    >>> from suds.client import Client
    >>> client = Client(wsdlURL)
    
    >>> from wsdl2interface import generate
    >>> generated = generate(client, wsdlURL)

Caveats
-------

This package is not guaranteed to produce 100% correct code. In most cases,
you will need to perform some manual cleanup afterwards. It is also not
terribly well tested. Patches welcome!

Please note:

* WSDL allows identifiers that are not valid in Python. Thus, you could end
  up with attributes or method which are not valid Python. The script will
  convert spaces to underscores, but will not handle things like names
  starting with a digit.
* WSDL files with multiple service definitions and/or ports will be flattened.
* Complex types and enumerations specifies in the WSDL file will be output
  first, as individual interfaces.
* The namespace and original type name are both output in the docstring of
  the generated interface for a complex type or enumeration. However, it is
  possible that the same name will be output.
* Types in the following namespaces are not output as complex type interfaces,
  and are referenced as primitives when used in attributes or method
  arguments:
  
  * http://schemas.xmlsoap.org/soap/encoding/
  * http://schemas.xmlsoap.org/wsdl/
  * http://www.w3.org/2001/XMLSchema

.. _zope.interface: http://pypi.python.org/pypi/zope.interface
.. _suds: http://pypi.python.org/pypi/suds

Changelog
=========

1.0b1 - 2010-05-07
------------------

* Indicate whether a given field in a complex type is required (must be set)
  or not.

1.0a5 - 2010-03-22
------------------

* Don't include input/output message types in the list of complex types.

* Unwrap the return type to display the actual object that will be returned
  by Suds, if possible.

1.0a4 - 2010-03-22
------------------

* Display a return type for each method based on the SOAP output message.
  Note that this isn't perfect - it assumes the response type is in the main
  target namespace and unambiguous.

1.0a3 - 2010-03-18
------------------

* Use zope.schema fields for common attribute types in complex types.

* Mangle identifiers to ensure they are valid Python

1.0a2 - 2010-03-17
------------------

* Fix broken release

1.0a1 - 2010-02-12
------------------

* Initial release
