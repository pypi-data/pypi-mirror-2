#------------------------------------------------------------------------------
# Copyright (C) 2009 Richard Lincoln
#------------------------------------------------------------------------------

""" Test case for the Common Information Model.
"""

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

import sys
import unittest
import logging

from os.path import join, dirname

from CIM import CommonInformationModel

from CIM.LoadModel import \
    ConformLoadGroup, LoadArea, ConformLoadSchedule, Load

from CIM.Meas import \
    AnalogLimit, AnalogValue, Analog

from CIM.Protection import \
    CurrentRelay

from CIM.Topology import \
    ConnectivityNode, TopologicalNode

from CIM.Wires import \
    Breaker, SynchronousMachine, BusbarSection, ACLineSegment, \
    PowerTransformer, TransformerWinding

from CIM.Generation import Production

print dir(Production)

from CIM.Generation.Production import \
    ThermalGeneratingUnit, GenUnitOpCostCurve, GenUnitOpSchedule

from CIM.CIMReader import \
    read_cim

#-------------------------------------------------------------------------------
#  Constants:
#-------------------------------------------------------------------------------

RDFXML_FILE = join(dirname(__file__), "Data", "10Bus.xml")

#-------------------------------------------------------------------------------
#  "CIMTestCase" class:
#-------------------------------------------------------------------------------

class CIMTestCase(unittest.TestCase):
    """ Defines a test case for the Common Information Model.
    """

    def setUp(self):
        """ The test runner will execute this method prior to each test.
        """
        pass


    def test_create_elements(self):
        """ Test creation of Common Information Model elements.
        """
        production = [ThermalGeneratingUnit(), GenUnitOpCostCurve(),
            GenUnitOpSchedule()]

        load_model = [ConformLoadGroup(), LoadArea(), ConformLoadSchedule(),
            Load()]

        meas = [AnalogLimit(), AnalogValue(), Analog()]

        topology = [ConnectivityNode(), TopologicalNode()]

        wires = [Breaker(), SynchronousMachine(), BusbarSection(),
            ACLineSegment(), PowerTransformer(), TransformerWinding()]

        elements = production + load_model + meas + topology + wires
        for element in elements:
            self.assertNotEqual(element, None)


    def test_references(self):
        """ Test associations between model elements.
        """
        load_group = ConformLoadGroup(name="CLG1")
        load_group2 = ConformLoadGroup(name="CLG2")
        load = Load(name="Load 1", LoadGroup=load_group)
        model = CommonInformationModel(Contains=[load_group, load_group2, load])
#        load.configure_traits()


    def test_load_cim(self):
        """ Test loading a Common Information Model from a RDF/XML file.
        """
        elements = read_cim(RDFXML_FILE)
        model = CommonInformationModel( Elements=elements.values() )
        print "ELEMENTS:", len(model.Elements)
        model.Elements[6].configure_traits()

if __name__ == "__main__":
    unittest.main()

# EOF -------------------------------------------------------------------------
