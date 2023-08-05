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

    class IArrayOfComponent(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}ArrayOfComponent``
        """

        Component = Attribute('Type: IComponent[]')

    class IArrayOfPricedComponent(Interface):
        """SOAP complex type
        ``{http://www.xignite.com/services/}ArrayOfPricedComponent``
        """

        PricedComponent = Attribute('Type: IPricedComponent[]')

    class ICommon(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}Common``
        """

        Outcome = Attribute('Type: IOutcomeTypes')
        Message = Attribute('Type: string')
        Identity = Attribute('Type: string')
        Delay = Attribute('Type: double')

    class IComponent(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}Component``
        """

        Security = Attribute('Type: ISecurity')
        Weight = Attribute('Type: double')
        AdjustmentFactor = Attribute('Type: double')
        IndexComponentWeightType = Attribute('Type: IIndexComponentWeightTypes')

    class IComponents(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}Components``
        """

        Outcome = Attribute('Type: IOutcomeTypes')
        Message = Attribute('Type: string')
        Identity = Attribute('Type: string')
        Delay = Attribute('Type: double')
        Security = Attribute('Type: ISecurity')
        Count = Attribute('Type: int')
        Components = Attribute('Type: IArrayOfComponent')

    class IHeader(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}Header``
        """

        Username = Attribute('Type: string')
        Password = Attribute('Type: string')
        Tracer = Attribute('Type: string')

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

        Outcome = Attribute('Type: IOutcomeTypes')
        Message = Attribute('Type: string')
        Identity = Attribute('Type: string')
        Delay = Attribute('Type: double')
        Symbol = Attribute('Type: string')
        Name = Attribute('Type: string')
        Exchange = Attribute('Type: string')
        CIK = Attribute('Type: string')
        Cusip = Attribute('Type: string')
        ISIN = Attribute('Type: string')
        SEDOL = Attribute('Type: string')
        Valoren = Attribute('Type: string')
        Sector = Attribute('Type: string')
        Class = Attribute('Type: string')
        IndustryGroup = Attribute('Type: string')
        Industry = Attribute('Type: string')
        Country = Attribute('Type: string')
        Currency = Attribute('Type: string')
        Style = Attribute('Type: string')
        Price = Attribute('Type: double')
        Weight = Attribute('Type: double')
        Value = Attribute('Type: double')
        MarketCapitalization = Attribute('Type: double')
        AdjustmentFactor = Attribute('Type: double')
        IndexComponentWeightType = Attribute('Type: IIndexComponentWeightTypes')

    class IPricedComponents(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}PricedComponents``
        """

        Outcome = Attribute('Type: IOutcomeTypes')
        Message = Attribute('Type: string')
        Identity = Attribute('Type: string')
        Delay = Attribute('Type: double')
        Security = Attribute('Type: ISecurity')
        Count = Attribute('Type: int')
        AsOfDate = Attribute('Type: string')
        Price = Attribute('Type: double')
        Divisor = Attribute('Type: double')
        DivisorDate = Attribute('Type: string')
        PricedComponents = Attribute('Type: IArrayOfPricedComponent')

    class ISecurity(Interface):
        """SOAP complex type ``{http://www.xignite.com/services/}Security``
        """

        Outcome = Attribute('Type: IOutcomeTypes')
        Message = Attribute('Type: string')
        Identity = Attribute('Type: string')
        Delay = Attribute('Type: double')
        CIK = Attribute('Type: string')
        Cusip = Attribute('Type: string')
        Symbol = Attribute('Type: string')
        ISIN = Attribute('Type: string')
        Valoren = Attribute('Type: string')
        Name = Attribute('Type: string')
        Market = Attribute('Type: string')
        CategoryOrIndustry = Attribute('Type: string')

    class IXigniteIndexComponents(Interface):
        """SOAP service ``XigniteIndexComponents`` with target namespace
        http://www.xignite.com/services/.
        """

        def GetIndexComponents(Identifier, IdentifierType):
            """Parameters:
        
            ``Identifier`` -- string (optional)
            ``IdentifierType`` -- IIdentifierTypes
            """

        def GetPricedIndexComponents(Identifier, IdentifierType, AsOfDate):
            """Parameters:
        
            ``Identifier`` -- string (optional)
            ``IdentifierType`` -- IIdentifierTypes
            ``AsOfDate`` -- string (optional)
            """

        def GetPricedIndexComponentsSubset(Identifier, IdentifierType, AsOfDate, StartIndex, EndIndex):
            """Parameters:
        
            ``Identifier`` -- string (optional)
            ``IdentifierType`` -- IIdentifierTypes
            ``AsOfDate`` -- string (optional)
            ``StartIndex`` -- int
            ``EndIndex`` -- int
            """

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
  
  * http://schemas.xmlsoap.org/soap/encoding/'
  * http://schemas.xmlsoap.org/wsdl/
  * http://www.w3.org/2001/XMLSchema

.. _zope.interface: http://pypi.python.org/pypi/zope.interface
.. _suds: http://pypi.python.org/pypi/suds

Changelog
=========

1.0a2 - 2010-03-17
------------------

* Fix broken release

1.0a1 - 2010-02-12
------------------

* Initial release
