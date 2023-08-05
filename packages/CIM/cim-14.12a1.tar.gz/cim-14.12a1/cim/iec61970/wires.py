# Copyright (C) 2010 Richard Lincoln
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" An extension to the Core and Topology package that models information on the electrical characteristics of Transmission and Distribution networks. This package is used by network applications such as State Estimation, Load Flow and Optimal Power Flow.
"""

from cim.iec61970.core import ConductingEquipment
from cim.iec61970.core import Equipment
from cim.iec61970.core import PowerSystemResource
from cim.iec61970.load_model import SeasonDayTypeSchedule
from cim.iec61970.core import EquipmentContainer
from cim.iec61970.core import Curve
from cim.iec61970.core import IdentifiedObject

# <<< imports
# @generated
# >>> imports

ns_prefix = "cim.wires"

ns_uri = "http://iec.ch/TC57/2009/CIM-schema-cim14#Wires"

class Switch(ConductingEquipment):
    """ A generic device designed to close, or open, or both, one or more electric circuits.
    """
    # <<< switch
    # @generated
    def __init__(self, switch_on_count=0, normal_open=False, retained=False, switch_on_date='', load_mgmt_functions=None, composite_switch=None, switch_schedules=None, connect_disconnect_functions=None, switching_operations=None, **kw_args):
        """ Initialises a new 'Switch' instance.
        """
        # The switch on count since the switch was last reset or initialized. 
        self.switch_on_count = switch_on_count

        # The attribute is used in cases when no Measurement for the status value is present. If the Switch has a status measurment the Discrete.normalValue is expected to match with the Switch.normalOpen. 
        self.normal_open = normal_open

        # Branch is retained in a bus branch model. 
        self.retained = retained

        # The date and time when the switch was last switched on. 
        self.switch_on_date = switch_on_date


        self._load_mgmt_functions = []
        if load_mgmt_functions is not None:
            self.load_mgmt_functions = load_mgmt_functions
        else:
            self.load_mgmt_functions = []

        self._composite_switch = None
        self.composite_switch = composite_switch

        self._switch_schedules = []
        if switch_schedules is not None:
            self.switch_schedules = switch_schedules
        else:
            self.switch_schedules = []

        self._connect_disconnect_functions = []
        if connect_disconnect_functions is not None:
            self.connect_disconnect_functions = connect_disconnect_functions
        else:
            self.connect_disconnect_functions = []

        self._switching_operations = []
        if switching_operations is not None:
            self.switching_operations = switching_operations
        else:
            self.switching_operations = []


        super(Switch, self).__init__(**kw_args)
    # >>> switch

    # <<< load_mgmt_functions
    # @generated
    def get_load_mgmt_functions(self):
        """ 
        """
        return self._load_mgmt_functions

    def set_load_mgmt_functions(self, value):
        for p in self._load_mgmt_functions:
            filtered = [q for q in p.switches if q != self]
            self._load_mgmt_functions._switches = filtered
        for r in value:
            if self not in r._switches:
                r._switches.append(self)
        self._load_mgmt_functions = value

    load_mgmt_functions = property(get_load_mgmt_functions, set_load_mgmt_functions)

    def add_load_mgmt_functions(self, *load_mgmt_functions):
        for obj in load_mgmt_functions:
            if self not in obj._switches:
                obj._switches.append(self)
            self._load_mgmt_functions.append(obj)

    def remove_load_mgmt_functions(self, *load_mgmt_functions):
        for obj in load_mgmt_functions:
            if self in obj._switches:
                obj._switches.remove(self)
            self._load_mgmt_functions.remove(obj)
    # >>> load_mgmt_functions

    # <<< composite_switch
    # @generated
    def get_composite_switch(self):
        """ Composite switch this Switch belongs to
        """
        return self._composite_switch

    def set_composite_switch(self, value):
        if self._composite_switch is not None:
            filtered = [x for x in self.composite_switch.switches if x != self]
            self._composite_switch._switches = filtered

        self._composite_switch = value
        if self._composite_switch is not None:
            self._composite_switch._switches.append(self)

    composite_switch = property(get_composite_switch, set_composite_switch)
    # >>> composite_switch

    # <<< switch_schedules
    # @generated
    def get_switch_schedules(self):
        """ A Switch can be associated with SwitchSchedules.
        """
        return self._switch_schedules

    def set_switch_schedules(self, value):
        for x in self._switch_schedules:
            x._switch = None
        for y in value:
            y._switch = self
        self._switch_schedules = value

    switch_schedules = property(get_switch_schedules, set_switch_schedules)

    def add_switch_schedules(self, *switch_schedules):
        for obj in switch_schedules:
            obj._switch = self
            self._switch_schedules.append(obj)

    def remove_switch_schedules(self, *switch_schedules):
        for obj in switch_schedules:
            obj._switch = None
            self._switch_schedules.remove(obj)
    # >>> switch_schedules

    # <<< connect_disconnect_functions
    # @generated
    def get_connect_disconnect_functions(self):
        """ 
        """
        return self._connect_disconnect_functions

    def set_connect_disconnect_functions(self, value):
        for p in self._connect_disconnect_functions:
            filtered = [q for q in p.switches if q != self]
            self._connect_disconnect_functions._switches = filtered
        for r in value:
            if self not in r._switches:
                r._switches.append(self)
        self._connect_disconnect_functions = value

    connect_disconnect_functions = property(get_connect_disconnect_functions, set_connect_disconnect_functions)

    def add_connect_disconnect_functions(self, *connect_disconnect_functions):
        for obj in connect_disconnect_functions:
            if self not in obj._switches:
                obj._switches.append(self)
            self._connect_disconnect_functions.append(obj)

    def remove_connect_disconnect_functions(self, *connect_disconnect_functions):
        for obj in connect_disconnect_functions:
            if self in obj._switches:
                obj._switches.remove(self)
            self._connect_disconnect_functions.remove(obj)
    # >>> connect_disconnect_functions

    # <<< switching_operations
    # @generated
    def get_switching_operations(self):
        """ A switch may be operated by many schedules.
        """
        return self._switching_operations

    def set_switching_operations(self, value):
        for p in self._switching_operations:
            filtered = [q for q in p.switches if q != self]
            self._switching_operations._switches = filtered
        for r in value:
            if self not in r._switches:
                r._switches.append(self)
        self._switching_operations = value

    switching_operations = property(get_switching_operations, set_switching_operations)

    def add_switching_operations(self, *switching_operations):
        for obj in switching_operations:
            if self not in obj._switches:
                obj._switches.append(self)
            self._switching_operations.append(obj)

    def remove_switching_operations(self, *switching_operations):
        for obj in switching_operations:
            if self in obj._switches:
                obj._switches.remove(self)
            self._switching_operations.remove(obj)
    # >>> switching_operations


    def __str__(self):
        """ Returns a string representation of the Switch.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< switch.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Switch.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Switch", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.load_mgmt_functions:
            s += '%s<%s:Switch.load_mgmt_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.composite_switch is not None:
            s += '%s<%s:Switch.composite_switch rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.composite_switch.uri)
        for obj in self.switch_schedules:
            s += '%s<%s:Switch.switch_schedules rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.connect_disconnect_functions:
            s += '%s<%s:Switch.connect_disconnect_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.switching_operations:
            s += '%s<%s:Switch.switching_operations rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Switch.switch_on_count>%s</%s:Switch.switch_on_count>' % \
            (indent, ns_prefix, self.switch_on_count, ns_prefix)
        s += '%s<%s:Switch.normal_open>%s</%s:Switch.normal_open>' % \
            (indent, ns_prefix, self.normal_open, ns_prefix)
        s += '%s<%s:Switch.retained>%s</%s:Switch.retained>' % \
            (indent, ns_prefix, self.retained, ns_prefix)
        s += '%s<%s:Switch.switch_on_date>%s</%s:Switch.switch_on_date>' % \
            (indent, ns_prefix, self.switch_on_date, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Switch")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> switch.serialize


class HeatExchanger(Equipment):
    """ Equipment for the cooling of electrical equipment and the extraction of heat
    """
    # <<< heat_exchanger
    # @generated
    def __init__(self, power_transformer=None, **kw_args):
        """ Initialises a new 'HeatExchanger' instance.
        """

        self._power_transformer = None
        self.power_transformer = power_transformer


        super(HeatExchanger, self).__init__(**kw_args)
    # >>> heat_exchanger

    # <<< power_transformer
    # @generated
    def get_power_transformer(self):
        """ A transformer may have a heat exchanger
        """
        return self._power_transformer

    def set_power_transformer(self, value):
        if self._power_transformer is not None:
            self._power_transformer._heat_exchanger = None

        self._power_transformer = value
        if self._power_transformer is not None:
            self._power_transformer._heat_exchanger = self

    power_transformer = property(get_power_transformer, set_power_transformer)
    # >>> power_transformer


    def __str__(self):
        """ Returns a string representation of the HeatExchanger.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< heat_exchanger.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the HeatExchanger.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "HeatExchanger", self.uri)
        if format:
            indent += ' ' * depth

        if self.power_transformer is not None:
            s += '%s<%s:HeatExchanger.power_transformer rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.power_transformer.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "HeatExchanger")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> heat_exchanger.serialize


class TapChanger(PowerSystemResource):
    """ Mechanism for changing transformer winding tap positions.
    """
    # <<< tap_changer
    # @generated
    def __init__(self, neutral_step=0, subsequent_delay=0.0, neutral_u=0.0, step_voltage_increment=0.0, low_step=0, normal_step=0, regulation_status=False, high_step=0, initial_delay=0.0, ltc_flag=False, regulating_control=None, impedance_variation_curve=None, sv_tap_step=None, tap_schedules=None, **kw_args):
        """ Initialises a new 'TapChanger' instance.
        """
        # The neutral tap step position for this winding. 
        self.neutral_step = neutral_step

        # For an LTC, the delay for subsequent tap changer operation (second and later step changes) 
        self.subsequent_delay = subsequent_delay

        # Voltage at which the winding operates at the neutral tap setting. 
        self.neutral_u = neutral_u

        # Tap step increment, in per cent of nominal voltage, per step position.  For a symmetrical PhaseTapChanger, the stepVoltageIncrement is used in the formula for calculation of the phase angle.  For a symmetrical PhaseTapChanger, the voltage magnitude does not change with tap step. 
        self.step_voltage_increment = step_voltage_increment

        # Lowest possible tap step position, retard from neutral 
        self.low_step = low_step

        # The tap step position used in 'normal' network operation for this winding. For a 'Fixed' tap changer indicates the current physical tap setting. 
        self.normal_step = normal_step

        # Specifies the default regulation status of the TapChanger.  True is regulating.  False is not regulating. 
        self.regulation_status = regulation_status

        # Highest possible tap step position, advance from neutral 
        self.high_step = high_step

        # For an LTC, the delay for initial tap changer operation (first step change) 
        self.initial_delay = initial_delay

        # Specifies whether or not a TapChanger has load tap changing capabilities. 
        self.ltc_flag = ltc_flag


        self._regulating_control = None
        self.regulating_control = regulating_control

        self._impedance_variation_curve = None
        self.impedance_variation_curve = impedance_variation_curve

        self._sv_tap_step = None
        self.sv_tap_step = sv_tap_step

        self._tap_schedules = []
        if tap_schedules is not None:
            self.tap_schedules = tap_schedules
        else:
            self.tap_schedules = []


        super(TapChanger, self).__init__(**kw_args)
    # >>> tap_changer

    # <<< regulating_control
    # @generated
    def get_regulating_control(self):
        """ 
        """
        return self._regulating_control

    def set_regulating_control(self, value):
        if self._regulating_control is not None:
            filtered = [x for x in self.regulating_control.tap_changer if x != self]
            self._regulating_control._tap_changer = filtered

        self._regulating_control = value
        if self._regulating_control is not None:
            self._regulating_control._tap_changer.append(self)

    regulating_control = property(get_regulating_control, set_regulating_control)
    # >>> regulating_control

    # <<< impedance_variation_curve
    # @generated
    def get_impedance_variation_curve(self):
        """ A TapChanger can have an associated ImpedanceVariationCurve to define impedance variations with tap step changes.
        """
        return self._impedance_variation_curve

    def set_impedance_variation_curve(self, value):
        if self._impedance_variation_curve is not None:
            self._impedance_variation_curve._tap_changer = None

        self._impedance_variation_curve = value
        if self._impedance_variation_curve is not None:
            self._impedance_variation_curve._tap_changer = self

    impedance_variation_curve = property(get_impedance_variation_curve, set_impedance_variation_curve)
    # >>> impedance_variation_curve

    # <<< sv_tap_step
    # @generated
    def get_sv_tap_step(self):
        """ The tap step state associated with the tap changer.
        """
        return self._sv_tap_step

    def set_sv_tap_step(self, value):
        if self._sv_tap_step is not None:
            self._sv_tap_step._tap_changer = None

        self._sv_tap_step = value
        if self._sv_tap_step is not None:
            self._sv_tap_step._tap_changer = self

    sv_tap_step = property(get_sv_tap_step, set_sv_tap_step)
    # >>> sv_tap_step

    # <<< tap_schedules
    # @generated
    def get_tap_schedules(self):
        """ A TapChanger can have TapSchedules.
        """
        return self._tap_schedules

    def set_tap_schedules(self, value):
        for x in self._tap_schedules:
            x._tap_changer = None
        for y in value:
            y._tap_changer = self
        self._tap_schedules = value

    tap_schedules = property(get_tap_schedules, set_tap_schedules)

    def add_tap_schedules(self, *tap_schedules):
        for obj in tap_schedules:
            obj._tap_changer = self
            self._tap_schedules.append(obj)

    def remove_tap_schedules(self, *tap_schedules):
        for obj in tap_schedules:
            obj._tap_changer = None
            self._tap_schedules.remove(obj)
    # >>> tap_schedules


    def __str__(self):
        """ Returns a string representation of the TapChanger.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< tap_changer.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the TapChanger.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "TapChanger", self.uri)
        if format:
            indent += ' ' * depth

        if self.regulating_control is not None:
            s += '%s<%s:TapChanger.regulating_control rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.regulating_control.uri)
        if self.impedance_variation_curve is not None:
            s += '%s<%s:TapChanger.impedance_variation_curve rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.impedance_variation_curve.uri)
        if self.sv_tap_step is not None:
            s += '%s<%s:TapChanger.sv_tap_step rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_tap_step.uri)
        for obj in self.tap_schedules:
            s += '%s<%s:TapChanger.tap_schedules rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TapChanger.neutral_step>%s</%s:TapChanger.neutral_step>' % \
            (indent, ns_prefix, self.neutral_step, ns_prefix)
        s += '%s<%s:TapChanger.subsequent_delay>%s</%s:TapChanger.subsequent_delay>' % \
            (indent, ns_prefix, self.subsequent_delay, ns_prefix)
        s += '%s<%s:TapChanger.neutral_u>%s</%s:TapChanger.neutral_u>' % \
            (indent, ns_prefix, self.neutral_u, ns_prefix)
        s += '%s<%s:TapChanger.step_voltage_increment>%s</%s:TapChanger.step_voltage_increment>' % \
            (indent, ns_prefix, self.step_voltage_increment, ns_prefix)
        s += '%s<%s:TapChanger.low_step>%s</%s:TapChanger.low_step>' % \
            (indent, ns_prefix, self.low_step, ns_prefix)
        s += '%s<%s:TapChanger.normal_step>%s</%s:TapChanger.normal_step>' % \
            (indent, ns_prefix, self.normal_step, ns_prefix)
        s += '%s<%s:TapChanger.regulation_status>%s</%s:TapChanger.regulation_status>' % \
            (indent, ns_prefix, self.regulation_status, ns_prefix)
        s += '%s<%s:TapChanger.high_step>%s</%s:TapChanger.high_step>' % \
            (indent, ns_prefix, self.high_step, ns_prefix)
        s += '%s<%s:TapChanger.initial_delay>%s</%s:TapChanger.initial_delay>' % \
            (indent, ns_prefix, self.initial_delay, ns_prefix)
        s += '%s<%s:TapChanger.ltc_flag>%s</%s:TapChanger.ltc_flag>' % \
            (indent, ns_prefix, self.ltc_flag, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "TapChanger")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> tap_changer.serialize


class RegulatingControl(PowerSystemResource):
    """ Specifies a set of equipment that works together to control a power system quantity such as voltage or flow.
    """
    # <<< regulating_control
    # @generated
    def __init__(self, mode='reactive_power', target_range=0.0, target_value=0.0, discrete=False, regulation_schedule=None, tap_changer=None, regulating_cond_eq=None, terminal=None, **kw_args):
        """ Initialises a new 'RegulatingControl' instance.
        """
        # The regulating control mode presently available.  This specifications allows for determining the kind of regualation without need for obtaining the units from a schedule. Values are: "reactive_power", "time_scheduled", "voltage", "current_flow", "admittance", "fixed", "power_factor", "temperature", "active_power"
        self.mode = 'reactive_power'

        # This is the case input target range.   This performs the same function as the value2 attribute on the regulation schedule in the case that schedules are not used.   The units of those appropriate for the mode. 
        self.target_range = target_range

        # The target value specified for case input.   This value can be used for the target value wihout the use of schedules. The value has the units appropriate to the mode attribute. 
        self.target_value = target_value

        # The regulation is performed in a discrete mode. 
        self.discrete = discrete


        self._regulation_schedule = []
        if regulation_schedule is not None:
            self.regulation_schedule = regulation_schedule
        else:
            self.regulation_schedule = []

        self._tap_changer = []
        if tap_changer is not None:
            self.tap_changer = tap_changer
        else:
            self.tap_changer = []

        self._regulating_cond_eq = []
        if regulating_cond_eq is not None:
            self.regulating_cond_eq = regulating_cond_eq
        else:
            self.regulating_cond_eq = []

        self._terminal = None
        self.terminal = terminal


        super(RegulatingControl, self).__init__(**kw_args)
    # >>> regulating_control

    # <<< regulation_schedule
    # @generated
    def get_regulation_schedule(self):
        """ Schedule for this Regulating regulating control.
        """
        return self._regulation_schedule

    def set_regulation_schedule(self, value):
        for x in self._regulation_schedule:
            x._regulating_control = None
        for y in value:
            y._regulating_control = self
        self._regulation_schedule = value

    regulation_schedule = property(get_regulation_schedule, set_regulation_schedule)

    def add_regulation_schedule(self, *regulation_schedule):
        for obj in regulation_schedule:
            obj._regulating_control = self
            self._regulation_schedule.append(obj)

    def remove_regulation_schedule(self, *regulation_schedule):
        for obj in regulation_schedule:
            obj._regulating_control = None
            self._regulation_schedule.remove(obj)
    # >>> regulation_schedule

    # <<< tap_changer
    # @generated
    def get_tap_changer(self):
        """ copy from reg conduting eq
        """
        return self._tap_changer

    def set_tap_changer(self, value):
        for x in self._tap_changer:
            x._regulating_control = None
        for y in value:
            y._regulating_control = self
        self._tap_changer = value

    tap_changer = property(get_tap_changer, set_tap_changer)

    def add_tap_changer(self, *tap_changer):
        for obj in tap_changer:
            obj._regulating_control = self
            self._tap_changer.append(obj)

    def remove_tap_changer(self, *tap_changer):
        for obj in tap_changer:
            obj._regulating_control = None
            self._tap_changer.remove(obj)
    # >>> tap_changer

    # <<< regulating_cond_eq
    # @generated
    def get_regulating_cond_eq(self):
        """ The equipment that participates in this regulating control scheme.
        """
        return self._regulating_cond_eq

    def set_regulating_cond_eq(self, value):
        for x in self._regulating_cond_eq:
            x._regulating_control = None
        for y in value:
            y._regulating_control = self
        self._regulating_cond_eq = value

    regulating_cond_eq = property(get_regulating_cond_eq, set_regulating_cond_eq)

    def add_regulating_cond_eq(self, *regulating_cond_eq):
        for obj in regulating_cond_eq:
            obj._regulating_control = self
            self._regulating_cond_eq.append(obj)

    def remove_regulating_cond_eq(self, *regulating_cond_eq):
        for obj in regulating_cond_eq:
            obj._regulating_control = None
            self._regulating_cond_eq.remove(obj)
    # >>> regulating_cond_eq

    # <<< terminal
    # @generated
    def get_terminal(self):
        """ The terminal associated with this regulating control.
        """
        return self._terminal

    def set_terminal(self, value):
        if self._terminal is not None:
            filtered = [x for x in self.terminal.regulating_control if x != self]
            self._terminal._regulating_control = filtered

        self._terminal = value
        if self._terminal is not None:
            self._terminal._regulating_control.append(self)

    terminal = property(get_terminal, set_terminal)
    # >>> terminal


    def __str__(self):
        """ Returns a string representation of the RegulatingControl.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< regulating_control.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the RegulatingControl.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "RegulatingControl", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.regulation_schedule:
            s += '%s<%s:RegulatingControl.regulation_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.tap_changer:
            s += '%s<%s:RegulatingControl.tap_changer rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.regulating_cond_eq:
            s += '%s<%s:RegulatingControl.regulating_cond_eq rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.terminal is not None:
            s += '%s<%s:RegulatingControl.terminal rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.terminal.uri)
        s += '%s<%s:RegulatingControl.mode>%s</%s:RegulatingControl.mode>' % \
            (indent, ns_prefix, self.mode, ns_prefix)
        s += '%s<%s:RegulatingControl.target_range>%s</%s:RegulatingControl.target_range>' % \
            (indent, ns_prefix, self.target_range, ns_prefix)
        s += '%s<%s:RegulatingControl.target_value>%s</%s:RegulatingControl.target_value>' % \
            (indent, ns_prefix, self.target_value, ns_prefix)
        s += '%s<%s:RegulatingControl.discrete>%s</%s:RegulatingControl.discrete>' % \
            (indent, ns_prefix, self.discrete, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "RegulatingControl")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> regulating_control.serialize


class TapSchedule(SeasonDayTypeSchedule):
    """ A pre-established pattern over time for a tap step.
    """
    # <<< tap_schedule
    # @generated
    def __init__(self, line_drop_x=0.0, line_drop_compensation=False, line_drop_r=0.0, tap_changer=None, **kw_args):
        """ Initialises a new 'TapSchedule' instance.
        """
        # Line drop reactance. 
        self.line_drop_x = line_drop_x

        # Flag to indicate that line drop compensation is to be applied 
        self.line_drop_compensation = line_drop_compensation

        # Line drop resistance. 
        self.line_drop_r = line_drop_r


        self._tap_changer = None
        self.tap_changer = tap_changer


        super(TapSchedule, self).__init__(**kw_args)
    # >>> tap_schedule

    # <<< tap_changer
    # @generated
    def get_tap_changer(self):
        """ A TapSchedule is associated with a TapChanger.
        """
        return self._tap_changer

    def set_tap_changer(self, value):
        if self._tap_changer is not None:
            filtered = [x for x in self.tap_changer.tap_schedules if x != self]
            self._tap_changer._tap_schedules = filtered

        self._tap_changer = value
        if self._tap_changer is not None:
            self._tap_changer._tap_schedules.append(self)

    tap_changer = property(get_tap_changer, set_tap_changer)
    # >>> tap_changer


    def __str__(self):
        """ Returns a string representation of the TapSchedule.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< tap_schedule.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the TapSchedule.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "TapSchedule", self.uri)
        if format:
            indent += ' ' * depth

        if self.tap_changer is not None:
            s += '%s<%s:TapSchedule.tap_changer rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.tap_changer.uri)
        s += '%s<%s:TapSchedule.line_drop_x>%s</%s:TapSchedule.line_drop_x>' % \
            (indent, ns_prefix, self.line_drop_x, ns_prefix)
        s += '%s<%s:TapSchedule.line_drop_compensation>%s</%s:TapSchedule.line_drop_compensation>' % \
            (indent, ns_prefix, self.line_drop_compensation, ns_prefix)
        s += '%s<%s:TapSchedule.line_drop_r>%s</%s:TapSchedule.line_drop_r>' % \
            (indent, ns_prefix, self.line_drop_r, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value2_multiplier>%s</%s:BasicIntervalSchedule.value2_multiplier>' % \
            (indent, ns_prefix, self.value2_multiplier, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value1_unit>%s</%s:BasicIntervalSchedule.value1_unit>' % \
            (indent, ns_prefix, self.value1_unit, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value2_unit>%s</%s:BasicIntervalSchedule.value2_unit>' % \
            (indent, ns_prefix, self.value2_unit, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value1_multiplier>%s</%s:BasicIntervalSchedule.value1_multiplier>' % \
            (indent, ns_prefix, self.value1_multiplier, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.start_time>%s</%s:BasicIntervalSchedule.start_time>' % \
            (indent, ns_prefix, self.start_time, ns_prefix)
        for obj in self.time_points:
            s += '%s<%s:RegularIntervalSchedule.time_points rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:RegularIntervalSchedule.time_step>%s</%s:RegularIntervalSchedule.time_step>' % \
            (indent, ns_prefix, self.time_step, ns_prefix)
        s += '%s<%s:RegularIntervalSchedule.end_time>%s</%s:RegularIntervalSchedule.end_time>' % \
            (indent, ns_prefix, self.end_time, ns_prefix)
        if self.day_type is not None:
            s += '%s<%s:SeasonDayTypeSchedule.day_type rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.day_type.uri)
        if self.season is not None:
            s += '%s<%s:SeasonDayTypeSchedule.season rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.season.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "TapSchedule")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> tap_schedule.serialize


class EnergyConsumer(ConductingEquipment):
    """ Generic user of energy - a  point of consumption on the power system model
    """
    # <<< energy_consumer
    # @generated
    def __init__(self, qfixed_pct=0.0, pfixed=0.0, customer_count=0, qfixed=0.0, pfixed_pct=0.0, power_cut_zone=None, service_delivery_points=None, load_response=None, **kw_args):
        """ Initialises a new 'EnergyConsumer' instance.
        """
        # Fixed reactive power as per cent of load group fixed reactive power. 
        self.qfixed_pct = qfixed_pct

        # Active power of the load that is a fixed quantity. 
        self.pfixed = pfixed

        # Number of individual customers represented by this Demand 
        self.customer_count = customer_count

        # Reactive power of the load that is a fixed quantity. 
        self.qfixed = qfixed

        # Fixed active power as per cent of load group fixed active power 
        self.pfixed_pct = pfixed_pct


        self._power_cut_zone = None
        self.power_cut_zone = power_cut_zone

        self._service_delivery_points = []
        if service_delivery_points is not None:
            self.service_delivery_points = service_delivery_points
        else:
            self.service_delivery_points = []

        self._load_response = None
        self.load_response = load_response


        super(EnergyConsumer, self).__init__(**kw_args)
    # >>> energy_consumer

    # <<< power_cut_zone
    # @generated
    def get_power_cut_zone(self):
        """ An energy consumer is assigned to a power cut zone
        """
        return self._power_cut_zone

    def set_power_cut_zone(self, value):
        if self._power_cut_zone is not None:
            filtered = [x for x in self.power_cut_zone.energy_consumers if x != self]
            self._power_cut_zone._energy_consumers = filtered

        self._power_cut_zone = value
        if self._power_cut_zone is not None:
            self._power_cut_zone._energy_consumers.append(self)

    power_cut_zone = property(get_power_cut_zone, set_power_cut_zone)
    # >>> power_cut_zone

    # <<< service_delivery_points
    # @generated
    def get_service_delivery_points(self):
        """ 
        """
        return self._service_delivery_points

    def set_service_delivery_points(self, value):
        for x in self._service_delivery_points:
            x._energy_consumer = None
        for y in value:
            y._energy_consumer = self
        self._service_delivery_points = value

    service_delivery_points = property(get_service_delivery_points, set_service_delivery_points)

    def add_service_delivery_points(self, *service_delivery_points):
        for obj in service_delivery_points:
            obj._energy_consumer = self
            self._service_delivery_points.append(obj)

    def remove_service_delivery_points(self, *service_delivery_points):
        for obj in service_delivery_points:
            obj._energy_consumer = None
            self._service_delivery_points.remove(obj)
    # >>> service_delivery_points

    # <<< load_response
    # @generated
    def get_load_response(self):
        """ The load response characteristic of this load.
        """
        return self._load_response

    def set_load_response(self, value):
        if self._load_response is not None:
            filtered = [x for x in self.load_response.energy_consumer if x != self]
            self._load_response._energy_consumer = filtered

        self._load_response = value
        if self._load_response is not None:
            self._load_response._energy_consumer.append(self)

    load_response = property(get_load_response, set_load_response)
    # >>> load_response


    def __str__(self):
        """ Returns a string representation of the EnergyConsumer.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< energy_consumer.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the EnergyConsumer.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "EnergyConsumer", self.uri)
        if format:
            indent += ' ' * depth

        if self.power_cut_zone is not None:
            s += '%s<%s:EnergyConsumer.power_cut_zone rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.power_cut_zone.uri)
        for obj in self.service_delivery_points:
            s += '%s<%s:EnergyConsumer.service_delivery_points rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.load_response is not None:
            s += '%s<%s:EnergyConsumer.load_response rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.load_response.uri)
        s += '%s<%s:EnergyConsumer.qfixed_pct>%s</%s:EnergyConsumer.qfixed_pct>' % \
            (indent, ns_prefix, self.qfixed_pct, ns_prefix)
        s += '%s<%s:EnergyConsumer.pfixed>%s</%s:EnergyConsumer.pfixed>' % \
            (indent, ns_prefix, self.pfixed, ns_prefix)
        s += '%s<%s:EnergyConsumer.customer_count>%s</%s:EnergyConsumer.customer_count>' % \
            (indent, ns_prefix, self.customer_count, ns_prefix)
        s += '%s<%s:EnergyConsumer.qfixed>%s</%s:EnergyConsumer.qfixed>' % \
            (indent, ns_prefix, self.qfixed, ns_prefix)
        s += '%s<%s:EnergyConsumer.pfixed_pct>%s</%s:EnergyConsumer.pfixed_pct>' % \
            (indent, ns_prefix, self.pfixed_pct, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "EnergyConsumer")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> energy_consumer.serialize


class EnergySource(ConductingEquipment):
    """ A generic equivalent for an energy supplier on a transmission or distribution voltage level.
    """
    # <<< energy_source
    # @generated
    def __init__(self, rn=0.0, r=0.0, r0=0.0, voltage_magnitude=0.0, x=0.0, voltage_angle=0.0, xn=0.0, x0=0.0, active_power=0.0, nominal_voltage=0.0, **kw_args):
        """ Initialises a new 'EnergySource' instance.
        """
        # Negative sequence Thevenin resistance. 
        self.rn = rn

        # Positive sequence Thevenin resistance. 
        self.r = r

        # Zero sequence Thevenin resistance. 
        self.r0 = r0

        # Phase-to-phase open circuit voltage magnitude. 
        self.voltage_magnitude = voltage_magnitude

        # Positive sequence Thevenin reactance. 
        self.x = x

        # Phase angle of a-phase open circuit. 
        self.voltage_angle = voltage_angle

        # Negative sequence Thevenin reactance. 
        self.xn = xn

        # Zero sequence Thevenin reactance. 
        self.x0 = x0

        # High voltage source load 
        self.active_power = active_power

        # Phase-to-phase nominal voltage. 
        self.nominal_voltage = nominal_voltage



        super(EnergySource, self).__init__(**kw_args)
    # >>> energy_source


    def __str__(self):
        """ Returns a string representation of the EnergySource.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< energy_source.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the EnergySource.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "EnergySource", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:EnergySource.rn>%s</%s:EnergySource.rn>' % \
            (indent, ns_prefix, self.rn, ns_prefix)
        s += '%s<%s:EnergySource.r>%s</%s:EnergySource.r>' % \
            (indent, ns_prefix, self.r, ns_prefix)
        s += '%s<%s:EnergySource.r0>%s</%s:EnergySource.r0>' % \
            (indent, ns_prefix, self.r0, ns_prefix)
        s += '%s<%s:EnergySource.voltage_magnitude>%s</%s:EnergySource.voltage_magnitude>' % \
            (indent, ns_prefix, self.voltage_magnitude, ns_prefix)
        s += '%s<%s:EnergySource.x>%s</%s:EnergySource.x>' % \
            (indent, ns_prefix, self.x, ns_prefix)
        s += '%s<%s:EnergySource.voltage_angle>%s</%s:EnergySource.voltage_angle>' % \
            (indent, ns_prefix, self.voltage_angle, ns_prefix)
        s += '%s<%s:EnergySource.xn>%s</%s:EnergySource.xn>' % \
            (indent, ns_prefix, self.xn, ns_prefix)
        s += '%s<%s:EnergySource.x0>%s</%s:EnergySource.x0>' % \
            (indent, ns_prefix, self.x0, ns_prefix)
        s += '%s<%s:EnergySource.active_power>%s</%s:EnergySource.active_power>' % \
            (indent, ns_prefix, self.active_power, ns_prefix)
        s += '%s<%s:EnergySource.nominal_voltage>%s</%s:EnergySource.nominal_voltage>' % \
            (indent, ns_prefix, self.nominal_voltage, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "EnergySource")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> energy_source.serialize


class SwitchSchedule(SeasonDayTypeSchedule):
    """ A schedule of switch positions.  If RegularTimePoint.value1 is 0, the switch is open.  If 1, the switch is closed.
    """
    # <<< switch_schedule
    # @generated
    def __init__(self, switch=None, **kw_args):
        """ Initialises a new 'SwitchSchedule' instance.
        """

        self._switch = None
        self.switch = switch


        super(SwitchSchedule, self).__init__(**kw_args)
    # >>> switch_schedule

    # <<< switch
    # @generated
    def get_switch(self):
        """ A SwitchSchedule is associated with a Switch.
        """
        return self._switch

    def set_switch(self, value):
        if self._switch is not None:
            filtered = [x for x in self.switch.switch_schedules if x != self]
            self._switch._switch_schedules = filtered

        self._switch = value
        if self._switch is not None:
            self._switch._switch_schedules.append(self)

    switch = property(get_switch, set_switch)
    # >>> switch


    def __str__(self):
        """ Returns a string representation of the SwitchSchedule.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< switch_schedule.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the SwitchSchedule.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "SwitchSchedule", self.uri)
        if format:
            indent += ' ' * depth

        if self.switch is not None:
            s += '%s<%s:SwitchSchedule.switch rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.switch.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value2_multiplier>%s</%s:BasicIntervalSchedule.value2_multiplier>' % \
            (indent, ns_prefix, self.value2_multiplier, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value1_unit>%s</%s:BasicIntervalSchedule.value1_unit>' % \
            (indent, ns_prefix, self.value1_unit, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value2_unit>%s</%s:BasicIntervalSchedule.value2_unit>' % \
            (indent, ns_prefix, self.value2_unit, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value1_multiplier>%s</%s:BasicIntervalSchedule.value1_multiplier>' % \
            (indent, ns_prefix, self.value1_multiplier, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.start_time>%s</%s:BasicIntervalSchedule.start_time>' % \
            (indent, ns_prefix, self.start_time, ns_prefix)
        for obj in self.time_points:
            s += '%s<%s:RegularIntervalSchedule.time_points rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:RegularIntervalSchedule.time_step>%s</%s:RegularIntervalSchedule.time_step>' % \
            (indent, ns_prefix, self.time_step, ns_prefix)
        s += '%s<%s:RegularIntervalSchedule.end_time>%s</%s:RegularIntervalSchedule.end_time>' % \
            (indent, ns_prefix, self.end_time, ns_prefix)
        if self.day_type is not None:
            s += '%s<%s:SeasonDayTypeSchedule.day_type rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.day_type.uri)
        if self.season is not None:
            s += '%s<%s:SeasonDayTypeSchedule.season rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.season.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "SwitchSchedule")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> switch_schedule.serialize


class Line(EquipmentContainer):
    """ A component part of a system extending between adjacent substations or from a substation to an adjacent interconnection point.
    """
    # <<< line
    # @generated
    def __init__(self, transmission_right_of_way=None, flowgates=None, region=None, **kw_args):
        """ Initialises a new 'Line' instance.
        """

        self._transmission_right_of_way = None
        self.transmission_right_of_way = transmission_right_of_way

        self._flowgates = []
        if flowgates is not None:
            self.flowgates = flowgates
        else:
            self.flowgates = []

        self._region = None
        self.region = region


        super(Line, self).__init__(**kw_args)
    # >>> line

    # <<< transmission_right_of_way
    # @generated
    def get_transmission_right_of_way(self):
        """ A transmission line can be part of a transmission corridor
        """
        return self._transmission_right_of_way

    def set_transmission_right_of_way(self, value):
        if self._transmission_right_of_way is not None:
            filtered = [x for x in self.transmission_right_of_way.lines if x != self]
            self._transmission_right_of_way._lines = filtered

        self._transmission_right_of_way = value
        if self._transmission_right_of_way is not None:
            self._transmission_right_of_way._lines.append(self)

    transmission_right_of_way = property(get_transmission_right_of_way, set_transmission_right_of_way)
    # >>> transmission_right_of_way

    # <<< flowgates
    # @generated
    def get_flowgates(self):
        """ 
        """
        return self._flowgates

    def set_flowgates(self, value):
        for p in self._flowgates:
            filtered = [q for q in p.lines if q != self]
            self._flowgates._lines = filtered
        for r in value:
            if self not in r._lines:
                r._lines.append(self)
        self._flowgates = value

    flowgates = property(get_flowgates, set_flowgates)

    def add_flowgates(self, *flowgates):
        for obj in flowgates:
            if self not in obj._lines:
                obj._lines.append(self)
            self._flowgates.append(obj)

    def remove_flowgates(self, *flowgates):
        for obj in flowgates:
            if self in obj._lines:
                obj._lines.remove(self)
            self._flowgates.remove(obj)
    # >>> flowgates

    # <<< region
    # @generated
    def get_region(self):
        """ A Line can be contained by a SubGeographical Region.
        """
        return self._region

    def set_region(self, value):
        if self._region is not None:
            filtered = [x for x in self.region.lines if x != self]
            self._region._lines = filtered

        self._region = value
        if self._region is not None:
            self._region._lines.append(self)

    region = property(get_region, set_region)
    # >>> region


    def __str__(self):
        """ Returns a string representation of the Line.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< line.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Line.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Line", self.uri)
        if format:
            indent += ' ' * depth

        if self.transmission_right_of_way is not None:
            s += '%s<%s:Line.transmission_right_of_way rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.transmission_right_of_way.uri)
        for obj in self.flowgates:
            s += '%s<%s:Line.flowgates rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.region is not None:
            s += '%s<%s:Line.region rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.region.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.topological_node:
            s += '%s<%s:ConnectivityNodeContainer.topological_node rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.connectivity_nodes:
            s += '%s<%s:ConnectivityNodeContainer.connectivity_nodes rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.equipments:
            s += '%s<%s:EquipmentContainer.equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Line")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> line.serialize


class RatioVariationCurve(Curve):
    """ A Ratio Variation Curve describes the change in tap ratio in relationship to tap step changes.  The tap step is represented using the xValue and the ratio using y1value.
    """
    # <<< ratio_variation_curve
    # @generated
    def __init__(self, ratio_tap_changer=None, **kw_args):
        """ Initialises a new 'RatioVariationCurve' instance.
        """

        self._ratio_tap_changer = None
        self.ratio_tap_changer = ratio_tap_changer


        super(RatioVariationCurve, self).__init__(**kw_args)
    # >>> ratio_variation_curve

    # <<< ratio_tap_changer
    # @generated
    def get_ratio_tap_changer(self):
        """ A RatioVariationCurve defines tap ratio changes for a RatioTapChanger.
        """
        return self._ratio_tap_changer

    def set_ratio_tap_changer(self, value):
        if self._ratio_tap_changer is not None:
            self._ratio_tap_changer._ratio_variation_curve = None

        self._ratio_tap_changer = value
        if self._ratio_tap_changer is not None:
            self._ratio_tap_changer._ratio_variation_curve = self

    ratio_tap_changer = property(get_ratio_tap_changer, set_ratio_tap_changer)
    # >>> ratio_tap_changer


    def __str__(self):
        """ Returns a string representation of the RatioVariationCurve.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< ratio_variation_curve.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the RatioVariationCurve.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "RatioVariationCurve", self.uri)
        if format:
            indent += ' ' * depth

        if self.ratio_tap_changer is not None:
            s += '%s<%s:RatioVariationCurve.ratio_tap_changer rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.ratio_tap_changer.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.curve_datas:
            s += '%s<%s:Curve.curve_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Curve.y3_multiplier>%s</%s:Curve.y3_multiplier>' % \
            (indent, ns_prefix, self.y3_multiplier, ns_prefix)
        s += '%s<%s:Curve.y2_multiplier>%s</%s:Curve.y2_multiplier>' % \
            (indent, ns_prefix, self.y2_multiplier, ns_prefix)
        s += '%s<%s:Curve.x_multiplier>%s</%s:Curve.x_multiplier>' % \
            (indent, ns_prefix, self.x_multiplier, ns_prefix)
        s += '%s<%s:Curve.y2_unit>%s</%s:Curve.y2_unit>' % \
            (indent, ns_prefix, self.y2_unit, ns_prefix)
        s += '%s<%s:Curve.curve_style>%s</%s:Curve.curve_style>' % \
            (indent, ns_prefix, self.curve_style, ns_prefix)
        s += '%s<%s:Curve.y1_unit>%s</%s:Curve.y1_unit>' % \
            (indent, ns_prefix, self.y1_unit, ns_prefix)
        s += '%s<%s:Curve.y1_multiplier>%s</%s:Curve.y1_multiplier>' % \
            (indent, ns_prefix, self.y1_multiplier, ns_prefix)
        s += '%s<%s:Curve.y3_unit>%s</%s:Curve.y3_unit>' % \
            (indent, ns_prefix, self.y3_unit, ns_prefix)
        s += '%s<%s:Curve.x_unit>%s</%s:Curve.x_unit>' % \
            (indent, ns_prefix, self.x_unit, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "RatioVariationCurve")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> ratio_variation_curve.serialize


class ReactiveCapabilityCurve(Curve):
    """ Reactive power rating envelope versus the synchronous machine's active power, in both the generating and motoring modes. For each active power value there is a corresponding high and low reactive power limit  value. Typically there will be a separate curve for each coolant condition, such as hydrogen pressure.  The Y1 axis values represent reactive minimum and the Y2 axis values represent reactive maximum.
    """
    # <<< reactive_capability_curve
    # @generated
    def __init__(self, coolant_temperature=0.0, hydrogen_pressure=0.0, synchronous_machines=None, initially_used_by_synchronous_machines=None, **kw_args):
        """ Initialises a new 'ReactiveCapabilityCurve' instance.
        """
        # The machine's coolant temperature (e.g., ambient air or stator circulating water). 
        self.coolant_temperature = coolant_temperature

        # The hydrogen coolant pressure 
        self.hydrogen_pressure = hydrogen_pressure


        self._synchronous_machines = []
        if synchronous_machines is not None:
            self.synchronous_machines = synchronous_machines
        else:
            self.synchronous_machines = []

        self._initially_used_by_synchronous_machines = []
        if initially_used_by_synchronous_machines is not None:
            self.initially_used_by_synchronous_machines = initially_used_by_synchronous_machines
        else:
            self.initially_used_by_synchronous_machines = []


        super(ReactiveCapabilityCurve, self).__init__(**kw_args)
    # >>> reactive_capability_curve

    # <<< synchronous_machines
    # @generated
    def get_synchronous_machines(self):
        """ Synchronous machines using this curve.
        """
        return self._synchronous_machines

    def set_synchronous_machines(self, value):
        for p in self._synchronous_machines:
            filtered = [q for q in p.reactive_capability_curves if q != self]
            self._synchronous_machines._reactive_capability_curves = filtered
        for r in value:
            if self not in r._reactive_capability_curves:
                r._reactive_capability_curves.append(self)
        self._synchronous_machines = value

    synchronous_machines = property(get_synchronous_machines, set_synchronous_machines)

    def add_synchronous_machines(self, *synchronous_machines):
        for obj in synchronous_machines:
            if self not in obj._reactive_capability_curves:
                obj._reactive_capability_curves.append(self)
            self._synchronous_machines.append(obj)

    def remove_synchronous_machines(self, *synchronous_machines):
        for obj in synchronous_machines:
            if self in obj._reactive_capability_curves:
                obj._reactive_capability_curves.remove(self)
            self._synchronous_machines.remove(obj)
    # >>> synchronous_machines

    # <<< initially_used_by_synchronous_machines
    # @generated
    def get_initially_used_by_synchronous_machines(self):
        """ Synchronous machines using this curve as default.
        """
        return self._initially_used_by_synchronous_machines

    def set_initially_used_by_synchronous_machines(self, value):
        for x in self._initially_used_by_synchronous_machines:
            x._initial_reactive_capability_curve = None
        for y in value:
            y._initial_reactive_capability_curve = self
        self._initially_used_by_synchronous_machines = value

    initially_used_by_synchronous_machines = property(get_initially_used_by_synchronous_machines, set_initially_used_by_synchronous_machines)

    def add_initially_used_by_synchronous_machines(self, *initially_used_by_synchronous_machines):
        for obj in initially_used_by_synchronous_machines:
            obj._initial_reactive_capability_curve = self
            self._initially_used_by_synchronous_machines.append(obj)

    def remove_initially_used_by_synchronous_machines(self, *initially_used_by_synchronous_machines):
        for obj in initially_used_by_synchronous_machines:
            obj._initial_reactive_capability_curve = None
            self._initially_used_by_synchronous_machines.remove(obj)
    # >>> initially_used_by_synchronous_machines


    def __str__(self):
        """ Returns a string representation of the ReactiveCapabilityCurve.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< reactive_capability_curve.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ReactiveCapabilityCurve.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ReactiveCapabilityCurve", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.synchronous_machines:
            s += '%s<%s:ReactiveCapabilityCurve.synchronous_machines rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.initially_used_by_synchronous_machines:
            s += '%s<%s:ReactiveCapabilityCurve.initially_used_by_synchronous_machines rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ReactiveCapabilityCurve.coolant_temperature>%s</%s:ReactiveCapabilityCurve.coolant_temperature>' % \
            (indent, ns_prefix, self.coolant_temperature, ns_prefix)
        s += '%s<%s:ReactiveCapabilityCurve.hydrogen_pressure>%s</%s:ReactiveCapabilityCurve.hydrogen_pressure>' % \
            (indent, ns_prefix, self.hydrogen_pressure, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.curve_datas:
            s += '%s<%s:Curve.curve_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Curve.y3_multiplier>%s</%s:Curve.y3_multiplier>' % \
            (indent, ns_prefix, self.y3_multiplier, ns_prefix)
        s += '%s<%s:Curve.y2_multiplier>%s</%s:Curve.y2_multiplier>' % \
            (indent, ns_prefix, self.y2_multiplier, ns_prefix)
        s += '%s<%s:Curve.x_multiplier>%s</%s:Curve.x_multiplier>' % \
            (indent, ns_prefix, self.x_multiplier, ns_prefix)
        s += '%s<%s:Curve.y2_unit>%s</%s:Curve.y2_unit>' % \
            (indent, ns_prefix, self.y2_unit, ns_prefix)
        s += '%s<%s:Curve.curve_style>%s</%s:Curve.curve_style>' % \
            (indent, ns_prefix, self.curve_style, ns_prefix)
        s += '%s<%s:Curve.y1_unit>%s</%s:Curve.y1_unit>' % \
            (indent, ns_prefix, self.y1_unit, ns_prefix)
        s += '%s<%s:Curve.y1_multiplier>%s</%s:Curve.y1_multiplier>' % \
            (indent, ns_prefix, self.y1_multiplier, ns_prefix)
        s += '%s<%s:Curve.y3_unit>%s</%s:Curve.y3_unit>' % \
            (indent, ns_prefix, self.y3_unit, ns_prefix)
        s += '%s<%s:Curve.x_unit>%s</%s:Curve.x_unit>' % \
            (indent, ns_prefix, self.x_unit, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ReactiveCapabilityCurve")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> reactive_capability_curve.serialize


class Connector(ConductingEquipment):
    """ A conductor, or group of conductors, with negligible impedance, that serve to connect other conducting equipment within a single substation and are modelled with a single logical terminal.
    """
    pass
    # <<< connector
    # @generated
    def __init__(self, **kw_args):
        """ Initialises a new 'Connector' instance.
        """


        super(Connector, self).__init__(**kw_args)
    # >>> connector


    def __str__(self):
        """ Returns a string representation of the Connector.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< connector.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Connector.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Connector", self.uri)
        if format:
            indent += ' ' * depth

        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Connector")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> connector.serialize


class Resistor(ConductingEquipment):
    """ Resistor, typically used in filter configurations or as earthing resistor for transformers.  Used for electrical model of distribution networks.
    """
    # <<< resistor
    # @generated
    def __init__(self, resistor_type_asset=None, resistor_asset=None, **kw_args):
        """ Initialises a new 'Resistor' instance.
        """

        self._resistor_type_asset = None
        self.resistor_type_asset = resistor_type_asset

        self._resistor_asset = None
        self.resistor_asset = resistor_asset


        super(Resistor, self).__init__(**kw_args)
    # >>> resistor

    # <<< resistor_type_asset
    # @generated
    def get_resistor_type_asset(self):
        """ 
        """
        return self._resistor_type_asset

    def set_resistor_type_asset(self, value):
        if self._resistor_type_asset is not None:
            filtered = [x for x in self.resistor_type_asset.resistors if x != self]
            self._resistor_type_asset._resistors = filtered

        self._resistor_type_asset = value
        if self._resistor_type_asset is not None:
            self._resistor_type_asset._resistors.append(self)

    resistor_type_asset = property(get_resistor_type_asset, set_resistor_type_asset)
    # >>> resistor_type_asset

    # <<< resistor_asset
    # @generated
    def get_resistor_asset(self):
        """ 
        """
        return self._resistor_asset

    def set_resistor_asset(self, value):
        if self._resistor_asset is not None:
            self._resistor_asset._resistor = None

        self._resistor_asset = value
        if self._resistor_asset is not None:
            self._resistor_asset._resistor = self

    resistor_asset = property(get_resistor_asset, set_resistor_asset)
    # >>> resistor_asset


    def __str__(self):
        """ Returns a string representation of the Resistor.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< resistor.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Resistor.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Resistor", self.uri)
        if format:
            indent += ' ' * depth

        if self.resistor_type_asset is not None:
            s += '%s<%s:Resistor.resistor_type_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.resistor_type_asset.uri)
        if self.resistor_asset is not None:
            s += '%s<%s:Resistor.resistor_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.resistor_asset.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Resistor")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> resistor.serialize


class SeriesCompensator(ConductingEquipment):
    """ A Series Compensator is a series capacitor or reactor or an AC transmission line without charging susceptance.  It is a two terminal device.
    """
    # <<< series_compensator
    # @generated
    def __init__(self, r=0.0, x=0.0, **kw_args):
        """ Initialises a new 'SeriesCompensator' instance.
        """
        # Positive sequence resistance. 
        self.r = r

        # Positive sequence reactance. 
        self.x = x



        super(SeriesCompensator, self).__init__(**kw_args)
    # >>> series_compensator


    def __str__(self):
        """ Returns a string representation of the SeriesCompensator.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< series_compensator.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the SeriesCompensator.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "SeriesCompensator", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:SeriesCompensator.r>%s</%s:SeriesCompensator.r>' % \
            (indent, ns_prefix, self.r, ns_prefix)
        s += '%s<%s:SeriesCompensator.x>%s</%s:SeriesCompensator.x>' % \
            (indent, ns_prefix, self.x, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "SeriesCompensator")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> series_compensator.serialize


class WindingTest(IdentifiedObject):
    """ Physical winding test data for the winding/tap pairs of a transformer (or phase shifter). This test data can be used to derive other attributes of specific transformer or phase shifter models.
    """
    # <<< winding_test
    # @generated
    def __init__(self, phase_shift=0.0, from_tap_step=0, no_load_loss=0.0, to_tap_step=0, exciting_current=0.0, load_loss=0.0, leakage_impedance=0.0, voltage=0.0, to_transformer_winding=None, from_transformer_winding=None, **kw_args):
        """ Initialises a new 'WindingTest' instance.
        """
        # The phase shift measured at the open-circuited 'to' winding, with the 'from' winding set to the 'from' winding's rated voltage and all other windings open-circuited. 
        self.phase_shift = phase_shift

        # The tap step number for the 'from' winding of the test pair. 
        self.from_tap_step = from_tap_step

        # The no load loss kW 'to' winding open-circuited) from the test report. 
        self.no_load_loss = no_load_loss

        # The tap step number for the 'to' winding of the test pair. 
        self.to_tap_step = to_tap_step

        # The exciting current on open-circuit test, expressed as a percentage of rated current, at nominal voltage 
        self.exciting_current = exciting_current

        # The load loss kW ('to' winding short-circuited) from the test report. 
        self.load_loss = load_loss

        # The leakage impedance measured at the 'from' winding  with the 'to' winding short-circuited and all other windings open-circuited.  Leakage impedance is expressed in units based on the apparent power and voltage ratings of the 'from' winding. 
        self.leakage_impedance = leakage_impedance

        # The voltage measured at the open-circuited 'to' winding, with the 'from' winding set to the 'from' winding's rated voltage and all other windings open-circuited. 
        self.voltage = voltage


        self._to_transformer_winding = None
        self.to_transformer_winding = to_transformer_winding

        self._from_transformer_winding = None
        self.from_transformer_winding = from_transformer_winding


        super(WindingTest, self).__init__(**kw_args)
    # >>> winding_test

    # <<< to_transformer_winding
    # @generated
    def get_to_transformer_winding(self):
        """ The winding to which the test was conducted.  Note that although the 'from' side of the test is required, the 'to' side of a test is not always required.
        """
        return self._to_transformer_winding

    def set_to_transformer_winding(self, value):
        if self._to_transformer_winding is not None:
            filtered = [x for x in self.to_transformer_winding.to_winding_test if x != self]
            self._to_transformer_winding._to_winding_test = filtered

        self._to_transformer_winding = value
        if self._to_transformer_winding is not None:
            self._to_transformer_winding._to_winding_test.append(self)

    to_transformer_winding = property(get_to_transformer_winding, set_to_transformer_winding)
    # >>> to_transformer_winding

    # <<< from_transformer_winding
    # @generated
    def get_from_transformer_winding(self):
        """ The winding from which the test was conducted
        """
        return self._from_transformer_winding

    def set_from_transformer_winding(self, value):
        if self._from_transformer_winding is not None:
            filtered = [x for x in self.from_transformer_winding.from_winding_test if x != self]
            self._from_transformer_winding._from_winding_test = filtered

        self._from_transformer_winding = value
        if self._from_transformer_winding is not None:
            self._from_transformer_winding._from_winding_test.append(self)

    from_transformer_winding = property(get_from_transformer_winding, set_from_transformer_winding)
    # >>> from_transformer_winding


    def __str__(self):
        """ Returns a string representation of the WindingTest.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< winding_test.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the WindingTest.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "WindingTest", self.uri)
        if format:
            indent += ' ' * depth

        if self.to_transformer_winding is not None:
            s += '%s<%s:WindingTest.to_transformer_winding rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.to_transformer_winding.uri)
        if self.from_transformer_winding is not None:
            s += '%s<%s:WindingTest.from_transformer_winding rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.from_transformer_winding.uri)
        s += '%s<%s:WindingTest.phase_shift>%s</%s:WindingTest.phase_shift>' % \
            (indent, ns_prefix, self.phase_shift, ns_prefix)
        s += '%s<%s:WindingTest.from_tap_step>%s</%s:WindingTest.from_tap_step>' % \
            (indent, ns_prefix, self.from_tap_step, ns_prefix)
        s += '%s<%s:WindingTest.no_load_loss>%s</%s:WindingTest.no_load_loss>' % \
            (indent, ns_prefix, self.no_load_loss, ns_prefix)
        s += '%s<%s:WindingTest.to_tap_step>%s</%s:WindingTest.to_tap_step>' % \
            (indent, ns_prefix, self.to_tap_step, ns_prefix)
        s += '%s<%s:WindingTest.exciting_current>%s</%s:WindingTest.exciting_current>' % \
            (indent, ns_prefix, self.exciting_current, ns_prefix)
        s += '%s<%s:WindingTest.load_loss>%s</%s:WindingTest.load_loss>' % \
            (indent, ns_prefix, self.load_loss, ns_prefix)
        s += '%s<%s:WindingTest.leakage_impedance>%s</%s:WindingTest.leakage_impedance>' % \
            (indent, ns_prefix, self.leakage_impedance, ns_prefix)
        s += '%s<%s:WindingTest.voltage>%s</%s:WindingTest.voltage>' % \
            (indent, ns_prefix, self.voltage, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "WindingTest")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> winding_test.serialize


class Conductor(ConductingEquipment):
    """ Combination of conducting material with consistent electrical characteristics, building a single electrical system, used to carry current between points in the power system.
    """
    # <<< conductor
    # @generated
    def __init__(self, length=0.0, **kw_args):
        """ Initialises a new 'Conductor' instance.
        """
        # Segment length for calculating line section capabilities 
        self.length = length



        super(Conductor, self).__init__(**kw_args)
    # >>> conductor


    def __str__(self):
        """ Returns a string representation of the Conductor.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< conductor.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Conductor.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Conductor", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:Conductor.length>%s</%s:Conductor.length>' % \
            (indent, ns_prefix, self.length, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Conductor")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> conductor.serialize


class PowerTransformer(Equipment):
    """ An electrical device consisting of  two or more coupled windings, with or without a magnetic core, for introducing mutual coupling between electric circuits. Transformers can be used to control voltage and phase shift (active power flow).
    """
    # <<< power_transformer
    # @generated
    def __init__(self, bmag_sat=0.0, mag_base_u=0.0, mag_sat_flux=0.0, transformer_windings=None, flowgates=None, heat_exchanger=None, **kw_args):
        """ Initialises a new 'PowerTransformer' instance.
        """
        # Core shunt magnetizing susceptance in the saturation region. 
        self.bmag_sat = bmag_sat

        # The reference voltage at which the magnetizing saturation measurements were made 
        self.mag_base_u = mag_base_u

        # Core magnetizing saturation curve knee flux level. 
        self.mag_sat_flux = mag_sat_flux


        self._transformer_windings = []
        if transformer_windings is not None:
            self.transformer_windings = transformer_windings
        else:
            self.transformer_windings = []

        self._flowgates = []
        if flowgates is not None:
            self.flowgates = flowgates
        else:
            self.flowgates = []

        self._heat_exchanger = None
        self.heat_exchanger = heat_exchanger


        super(PowerTransformer, self).__init__(**kw_args)
    # >>> power_transformer

    # <<< transformer_windings
    # @generated
    def get_transformer_windings(self):
        """ A transformer has windings
        """
        return self._transformer_windings

    def set_transformer_windings(self, value):
        for x in self._transformer_windings:
            x._power_transformer = None
        for y in value:
            y._power_transformer = self
        self._transformer_windings = value

    transformer_windings = property(get_transformer_windings, set_transformer_windings)

    def add_transformer_windings(self, *transformer_windings):
        for obj in transformer_windings:
            obj._power_transformer = self
            self._transformer_windings.append(obj)

    def remove_transformer_windings(self, *transformer_windings):
        for obj in transformer_windings:
            obj._power_transformer = None
            self._transformer_windings.remove(obj)
    # >>> transformer_windings

    # <<< flowgates
    # @generated
    def get_flowgates(self):
        """ 
        """
        return self._flowgates

    def set_flowgates(self, value):
        for p in self._flowgates:
            filtered = [q for q in p.power_transormers if q != self]
            self._flowgates._power_transormers = filtered
        for r in value:
            if self not in r._power_transormers:
                r._power_transormers.append(self)
        self._flowgates = value

    flowgates = property(get_flowgates, set_flowgates)

    def add_flowgates(self, *flowgates):
        for obj in flowgates:
            if self not in obj._power_transormers:
                obj._power_transormers.append(self)
            self._flowgates.append(obj)

    def remove_flowgates(self, *flowgates):
        for obj in flowgates:
            if self in obj._power_transormers:
                obj._power_transormers.remove(self)
            self._flowgates.remove(obj)
    # >>> flowgates

    # <<< heat_exchanger
    # @generated
    def get_heat_exchanger(self):
        """ A transformer may have a heat exchanger
        """
        return self._heat_exchanger

    def set_heat_exchanger(self, value):
        if self._heat_exchanger is not None:
            self._heat_exchanger._power_transformer = None

        self._heat_exchanger = value
        if self._heat_exchanger is not None:
            self._heat_exchanger._power_transformer = self

    heat_exchanger = property(get_heat_exchanger, set_heat_exchanger)
    # >>> heat_exchanger


    def __str__(self):
        """ Returns a string representation of the PowerTransformer.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< power_transformer.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the PowerTransformer.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "PowerTransformer", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.transformer_windings:
            s += '%s<%s:PowerTransformer.transformer_windings rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.flowgates:
            s += '%s<%s:PowerTransformer.flowgates rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.heat_exchanger is not None:
            s += '%s<%s:PowerTransformer.heat_exchanger rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.heat_exchanger.uri)
        s += '%s<%s:PowerTransformer.bmag_sat>%s</%s:PowerTransformer.bmag_sat>' % \
            (indent, ns_prefix, self.bmag_sat, ns_prefix)
        s += '%s<%s:PowerTransformer.mag_base_u>%s</%s:PowerTransformer.mag_base_u>' % \
            (indent, ns_prefix, self.mag_base_u, ns_prefix)
        s += '%s<%s:PowerTransformer.mag_sat_flux>%s</%s:PowerTransformer.mag_sat_flux>' % \
            (indent, ns_prefix, self.mag_sat_flux, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "PowerTransformer")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> power_transformer.serialize


class MutualCoupling(IdentifiedObject):
    """ This class represents the zero sequence line mutual coupling.
    """
    # <<< mutual_coupling
    # @generated
    def __init__(self, distance12=0.0, b0ch=0.0, r0=0.0, g0ch=0.0, distance22=0.0, distance21=0.0, distance11=0.0, x0=0.0, second_terminal=None, first_terminal=None, **kw_args):
        """ Initialises a new 'MutualCoupling' instance.
        """
        # Distance from the first line's from specified terminal to end of coupled region 
        self.distance12 = distance12

        # Zero sequence mutual coupling shunt (charging) susceptance, uniformly distributed, of the entire line section. 
        self.b0ch = b0ch

        # Zero sequence branch-to-branch mutual impedance coupling, resistance 
        self.r0 = r0

        # Zero sequence mutual coupling shunt (charging) conductance, uniformly distributed, of the entire line section. 
        self.g0ch = g0ch

        # Distance from the second line's specified terminal to end of coupled region 
        self.distance22 = distance22

        # Distance from the second line's specified terminal to start of coupled region 
        self.distance21 = distance21

        # Distance from the first line's specified terminal to start of coupled region 
        self.distance11 = distance11

        # Zero sequence branch-to-branch mutual impedance coupling, reactance 
        self.x0 = x0


        self._second_terminal = None
        self.second_terminal = second_terminal

        self._first_terminal = None
        self.first_terminal = first_terminal


        super(MutualCoupling, self).__init__(**kw_args)
    # >>> mutual_coupling

    # <<< second_terminal
    # @generated
    def get_second_terminal(self):
        """ The starting terminal for the calculation of distances along the second branch of the mutual coupling.
        """
        return self._second_terminal

    def set_second_terminal(self, value):
        if self._second_terminal is not None:
            filtered = [x for x in self.second_terminal.has_second_mutual_coupling if x != self]
            self._second_terminal._has_second_mutual_coupling = filtered

        self._second_terminal = value
        if self._second_terminal is not None:
            self._second_terminal._has_second_mutual_coupling.append(self)

    second_terminal = property(get_second_terminal, set_second_terminal)
    # >>> second_terminal

    # <<< first_terminal
    # @generated
    def get_first_terminal(self):
        """ The starting terminal for the calculation of distances along the first branch of the mutual coupling.  Normally MutualCoupling would only be used for terminals of AC line segments.  The first and second terminals of a mutual coupling should point to different AC line segments.
        """
        return self._first_terminal

    def set_first_terminal(self, value):
        if self._first_terminal is not None:
            filtered = [x for x in self.first_terminal.has_first_mutual_coupling if x != self]
            self._first_terminal._has_first_mutual_coupling = filtered

        self._first_terminal = value
        if self._first_terminal is not None:
            self._first_terminal._has_first_mutual_coupling.append(self)

    first_terminal = property(get_first_terminal, set_first_terminal)
    # >>> first_terminal


    def __str__(self):
        """ Returns a string representation of the MutualCoupling.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< mutual_coupling.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the MutualCoupling.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "MutualCoupling", self.uri)
        if format:
            indent += ' ' * depth

        if self.second_terminal is not None:
            s += '%s<%s:MutualCoupling.second_terminal rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.second_terminal.uri)
        if self.first_terminal is not None:
            s += '%s<%s:MutualCoupling.first_terminal rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.first_terminal.uri)
        s += '%s<%s:MutualCoupling.distance12>%s</%s:MutualCoupling.distance12>' % \
            (indent, ns_prefix, self.distance12, ns_prefix)
        s += '%s<%s:MutualCoupling.b0ch>%s</%s:MutualCoupling.b0ch>' % \
            (indent, ns_prefix, self.b0ch, ns_prefix)
        s += '%s<%s:MutualCoupling.r0>%s</%s:MutualCoupling.r0>' % \
            (indent, ns_prefix, self.r0, ns_prefix)
        s += '%s<%s:MutualCoupling.g0ch>%s</%s:MutualCoupling.g0ch>' % \
            (indent, ns_prefix, self.g0ch, ns_prefix)
        s += '%s<%s:MutualCoupling.distance22>%s</%s:MutualCoupling.distance22>' % \
            (indent, ns_prefix, self.distance22, ns_prefix)
        s += '%s<%s:MutualCoupling.distance21>%s</%s:MutualCoupling.distance21>' % \
            (indent, ns_prefix, self.distance21, ns_prefix)
        s += '%s<%s:MutualCoupling.distance11>%s</%s:MutualCoupling.distance11>' % \
            (indent, ns_prefix, self.distance11, ns_prefix)
        s += '%s<%s:MutualCoupling.x0>%s</%s:MutualCoupling.x0>' % \
            (indent, ns_prefix, self.x0, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "MutualCoupling")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> mutual_coupling.serialize


class Ground(ConductingEquipment):
    """ A common point for connecting grounded conducting equipment such as shunt capacitors. The power system model can have more than one ground.
    """
    # <<< ground
    # @generated
    def __init__(self, winding_insulations=None, **kw_args):
        """ Initialises a new 'Ground' instance.
        """

        self._winding_insulations = []
        if winding_insulations is not None:
            self.winding_insulations = winding_insulations
        else:
            self.winding_insulations = []


        super(Ground, self).__init__(**kw_args)
    # >>> ground

    # <<< winding_insulations
    # @generated
    def get_winding_insulations(self):
        """ 
        """
        return self._winding_insulations

    def set_winding_insulations(self, value):
        for x in self._winding_insulations:
            x._ground = None
        for y in value:
            y._ground = self
        self._winding_insulations = value

    winding_insulations = property(get_winding_insulations, set_winding_insulations)

    def add_winding_insulations(self, *winding_insulations):
        for obj in winding_insulations:
            obj._ground = self
            self._winding_insulations.append(obj)

    def remove_winding_insulations(self, *winding_insulations):
        for obj in winding_insulations:
            obj._ground = None
            self._winding_insulations.remove(obj)
    # >>> winding_insulations


    def __str__(self):
        """ Returns a string representation of the Ground.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< ground.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Ground.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Ground", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.winding_insulations:
            s += '%s<%s:Ground.winding_insulations rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Ground")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> ground.serialize


class ImpedanceVariationCurve(Curve):
    """ An Impedance Variation Curve describes the change in Transformer Winding impedance values in relationship to tap step changes.  The tap step is represented using the xValue, resistance using y1value, reactance using y2value, and magnetizing susceptance using y3value.  The resistance (r), reactance (x), and magnetizing susceptance (b) of the associated TransformerWinding define the impedance when the tap is at neutral step.  The curve values represent the change to the impedance from the neutral step values.  The impedance at a non-neutral step is calculated by adding the neutral step impedance (from the TransformerWinding) to the delta value from the curve.
    """
    # <<< impedance_variation_curve
    # @generated
    def __init__(self, tap_changer=None, **kw_args):
        """ Initialises a new 'ImpedanceVariationCurve' instance.
        """

        self._tap_changer = None
        self.tap_changer = tap_changer


        super(ImpedanceVariationCurve, self).__init__(**kw_args)
    # >>> impedance_variation_curve

    # <<< tap_changer
    # @generated
    def get_tap_changer(self):
        """ An ImpedanceVariationCurve is defines impedance changes for a TapChanger.
        """
        return self._tap_changer

    def set_tap_changer(self, value):
        if self._tap_changer is not None:
            self._tap_changer._impedance_variation_curve = None

        self._tap_changer = value
        if self._tap_changer is not None:
            self._tap_changer._impedance_variation_curve = self

    tap_changer = property(get_tap_changer, set_tap_changer)
    # >>> tap_changer


    def __str__(self):
        """ Returns a string representation of the ImpedanceVariationCurve.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< impedance_variation_curve.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ImpedanceVariationCurve.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ImpedanceVariationCurve", self.uri)
        if format:
            indent += ' ' * depth

        if self.tap_changer is not None:
            s += '%s<%s:ImpedanceVariationCurve.tap_changer rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.tap_changer.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.curve_datas:
            s += '%s<%s:Curve.curve_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Curve.y3_multiplier>%s</%s:Curve.y3_multiplier>' % \
            (indent, ns_prefix, self.y3_multiplier, ns_prefix)
        s += '%s<%s:Curve.y2_multiplier>%s</%s:Curve.y2_multiplier>' % \
            (indent, ns_prefix, self.y2_multiplier, ns_prefix)
        s += '%s<%s:Curve.x_multiplier>%s</%s:Curve.x_multiplier>' % \
            (indent, ns_prefix, self.x_multiplier, ns_prefix)
        s += '%s<%s:Curve.y2_unit>%s</%s:Curve.y2_unit>' % \
            (indent, ns_prefix, self.y2_unit, ns_prefix)
        s += '%s<%s:Curve.curve_style>%s</%s:Curve.curve_style>' % \
            (indent, ns_prefix, self.curve_style, ns_prefix)
        s += '%s<%s:Curve.y1_unit>%s</%s:Curve.y1_unit>' % \
            (indent, ns_prefix, self.y1_unit, ns_prefix)
        s += '%s<%s:Curve.y1_multiplier>%s</%s:Curve.y1_multiplier>' % \
            (indent, ns_prefix, self.y1_multiplier, ns_prefix)
        s += '%s<%s:Curve.y3_unit>%s</%s:Curve.y3_unit>' % \
            (indent, ns_prefix, self.y3_unit, ns_prefix)
        s += '%s<%s:Curve.x_unit>%s</%s:Curve.x_unit>' % \
            (indent, ns_prefix, self.x_unit, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ImpedanceVariationCurve")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> impedance_variation_curve.serialize


class Plant(EquipmentContainer):
    """ A Plant is a collection of equipment for purposes of generation.
    """
    pass
    # <<< plant
    # @generated
    def __init__(self, **kw_args):
        """ Initialises a new 'Plant' instance.
        """


        super(Plant, self).__init__(**kw_args)
    # >>> plant


    def __str__(self):
        """ Returns a string representation of the Plant.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< plant.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Plant.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Plant", self.uri)
        if format:
            indent += ' ' * depth

        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.topological_node:
            s += '%s<%s:ConnectivityNodeContainer.topological_node rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.connectivity_nodes:
            s += '%s<%s:ConnectivityNodeContainer.connectivity_nodes rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.equipments:
            s += '%s<%s:EquipmentContainer.equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Plant")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> plant.serialize


class RegulatingCondEq(ConductingEquipment):
    """ RegulatingCondEq is a type of ConductingEquipment that can regulate Measurements and have a RegulationSchedule.
    """
    # <<< regulating_cond_eq
    # @generated
    def __init__(self, regulating_control=None, controls=None, **kw_args):
        """ Initialises a new 'RegulatingCondEq' instance.
        """

        self._regulating_control = None
        self.regulating_control = regulating_control

        self._controls = []
        if controls is not None:
            self.controls = controls
        else:
            self.controls = []


        super(RegulatingCondEq, self).__init__(**kw_args)
    # >>> regulating_cond_eq

    # <<< regulating_control
    # @generated
    def get_regulating_control(self):
        """ The regulating control scheme in which this equipment participates.
        """
        return self._regulating_control

    def set_regulating_control(self, value):
        if self._regulating_control is not None:
            filtered = [x for x in self.regulating_control.regulating_cond_eq if x != self]
            self._regulating_control._regulating_cond_eq = filtered

        self._regulating_control = value
        if self._regulating_control is not None:
            self._regulating_control._regulating_cond_eq.append(self)

    regulating_control = property(get_regulating_control, set_regulating_control)
    # >>> regulating_control

    # <<< controls
    # @generated
    def get_controls(self):
        """ The controller outputs used to actually govern a regulating device, e.g. the magnetization of a synchronous machine or capacitor bank breaker actuator.
        """
        return self._controls

    def set_controls(self, value):
        for x in self._controls:
            x._regulating_cond_eq = None
        for y in value:
            y._regulating_cond_eq = self
        self._controls = value

    controls = property(get_controls, set_controls)

    def add_controls(self, *controls):
        for obj in controls:
            obj._regulating_cond_eq = self
            self._controls.append(obj)

    def remove_controls(self, *controls):
        for obj in controls:
            obj._regulating_cond_eq = None
            self._controls.remove(obj)
    # >>> controls


    def __str__(self):
        """ Returns a string representation of the RegulatingCondEq.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< regulating_cond_eq.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the RegulatingCondEq.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "RegulatingCondEq", self.uri)
        if format:
            indent += ' ' * depth

        if self.regulating_control is not None:
            s += '%s<%s:RegulatingCondEq.regulating_control rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.regulating_control.uri)
        for obj in self.controls:
            s += '%s<%s:RegulatingCondEq.controls rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "RegulatingCondEq")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> regulating_cond_eq.serialize


class PhaseVariationCurve(Curve):
    """ A Ratio Variation Curve describes the change in tap ratio in relationship to tap step changes.  The tap step is represented using the xValue and the ratio using y1value.
    """
    # <<< phase_variation_curve
    # @generated
    def __init__(self, phase_tap_changer=None, **kw_args):
        """ Initialises a new 'PhaseVariationCurve' instance.
        """

        self._phase_tap_changer = None
        self.phase_tap_changer = phase_tap_changer


        super(PhaseVariationCurve, self).__init__(**kw_args)
    # >>> phase_variation_curve

    # <<< phase_tap_changer
    # @generated
    def get_phase_tap_changer(self):
        """ A PhaseVariationCurve defines phase shift changes for a PhaseTapChanger.
        """
        return self._phase_tap_changer

    def set_phase_tap_changer(self, value):
        if self._phase_tap_changer is not None:
            self._phase_tap_changer._phase_variation_curve = None

        self._phase_tap_changer = value
        if self._phase_tap_changer is not None:
            self._phase_tap_changer._phase_variation_curve = self

    phase_tap_changer = property(get_phase_tap_changer, set_phase_tap_changer)
    # >>> phase_tap_changer


    def __str__(self):
        """ Returns a string representation of the PhaseVariationCurve.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< phase_variation_curve.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the PhaseVariationCurve.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "PhaseVariationCurve", self.uri)
        if format:
            indent += ' ' * depth

        if self.phase_tap_changer is not None:
            s += '%s<%s:PhaseVariationCurve.phase_tap_changer rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.phase_tap_changer.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.curve_datas:
            s += '%s<%s:Curve.curve_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Curve.y3_multiplier>%s</%s:Curve.y3_multiplier>' % \
            (indent, ns_prefix, self.y3_multiplier, ns_prefix)
        s += '%s<%s:Curve.y2_multiplier>%s</%s:Curve.y2_multiplier>' % \
            (indent, ns_prefix, self.y2_multiplier, ns_prefix)
        s += '%s<%s:Curve.x_multiplier>%s</%s:Curve.x_multiplier>' % \
            (indent, ns_prefix, self.x_multiplier, ns_prefix)
        s += '%s<%s:Curve.y2_unit>%s</%s:Curve.y2_unit>' % \
            (indent, ns_prefix, self.y2_unit, ns_prefix)
        s += '%s<%s:Curve.curve_style>%s</%s:Curve.curve_style>' % \
            (indent, ns_prefix, self.curve_style, ns_prefix)
        s += '%s<%s:Curve.y1_unit>%s</%s:Curve.y1_unit>' % \
            (indent, ns_prefix, self.y1_unit, ns_prefix)
        s += '%s<%s:Curve.y1_multiplier>%s</%s:Curve.y1_multiplier>' % \
            (indent, ns_prefix, self.y1_multiplier, ns_prefix)
        s += '%s<%s:Curve.y3_unit>%s</%s:Curve.y3_unit>' % \
            (indent, ns_prefix, self.y3_unit, ns_prefix)
        s += '%s<%s:Curve.x_unit>%s</%s:Curve.x_unit>' % \
            (indent, ns_prefix, self.x_unit, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "PhaseVariationCurve")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> phase_variation_curve.serialize


class TransformerWinding(ConductingEquipment):
    """ A winding is associated with each defined terminal of a transformer (or phase shifter).
    """
    # <<< transformer_winding
    # @generated
    def __init__(self, winding_type='tertiary', connection_type='y', short_term_s=0.0, rated_u=0.0, grounded=False, r0=0.0, rated_s=0.0, emergency_s=0.0, b0=0.0, xground=0.0, g0=0.0, b=0.0, r=0.0, rground=0.0, x=0.0, insulation_u=0.0, g=0.0, x0=0.0, to_winding_test=None, power_transformer=None, from_winding_test=None, ratio_tap_changer=None, phase_tap_changer=None, **kw_args):
        """ Initialises a new 'TransformerWinding' instance.
        """
        # The type of winding. Values are: "tertiary", "secondary", "primary", "quaternary"
        self.winding_type = 'tertiary'

        # The type of connection of the winding. Values are: "y", "yn", "zn", "i", "a", "d", "z"
        self.connection_type = 'y'

        # Apparent power that the winding can carry for a short period of time. 
        self.short_term_s = short_term_s

        # The rated voltage (phase-to-phase) of the winding, usually the same as the neutral voltage. 
        self.rated_u = rated_u

        # Set if the winding is grounded. 
        self.grounded = grounded

        # Zero sequence series resistance of the winding. 
        self.r0 = r0

        # The normal apparent power rating for the winding 
        self.rated_s = rated_s

        # The apparent power that the winding can carry  under emergency conditions. 
        self.emergency_s = emergency_s

        # Zero sequence magnetizing branch susceptance. 
        self.b0 = b0

        # Ground reactance path through connected grounding transformer. 
        self.xground = xground

        # Zero sequence magnetizing branch conductance. 
        self.g0 = g0

        # Magnetizing branch susceptance (B mag).  The value can be positive or negative. 
        self.b = b

        # Positive sequence series resistance of the winding.  For a two winding transformer, the full resistance of the transformer should be entered on the primary (high voltage) winding. 
        self.r = r

        # Ground resistance path through connected grounding transformer. 
        self.rground = rground

        # Positive sequence series reactance of the winding.  For a two winding transformer, the full reactance of the transformer should be entered on the primary (high voltage) winding. 
        self.x = x

        # Basic insulation level voltage rating 
        self.insulation_u = insulation_u

        # Magnetizing branch conductance (G mag). 
        self.g = g

        # Zero sequence series reactance of the winding. 
        self.x0 = x0


        self._to_winding_test = []
        if to_winding_test is not None:
            self.to_winding_test = to_winding_test
        else:
            self.to_winding_test = []

        self._power_transformer = None
        self.power_transformer = power_transformer

        self._from_winding_test = []
        if from_winding_test is not None:
            self.from_winding_test = from_winding_test
        else:
            self.from_winding_test = []

        self._ratio_tap_changer = None
        self.ratio_tap_changer = ratio_tap_changer

        self._phase_tap_changer = None
        self.phase_tap_changer = phase_tap_changer


        super(TransformerWinding, self).__init__(**kw_args)
    # >>> transformer_winding

    # <<< to_winding_test
    # @generated
    def get_to_winding_test(self):
        """ The winding winding tests for which the transformer winding (terminal) participates as the 'to' end of the test.
        """
        return self._to_winding_test

    def set_to_winding_test(self, value):
        for x in self._to_winding_test:
            x._to_transformer_winding = None
        for y in value:
            y._to_transformer_winding = self
        self._to_winding_test = value

    to_winding_test = property(get_to_winding_test, set_to_winding_test)

    def add_to_winding_test(self, *to_winding_test):
        for obj in to_winding_test:
            obj._to_transformer_winding = self
            self._to_winding_test.append(obj)

    def remove_to_winding_test(self, *to_winding_test):
        for obj in to_winding_test:
            obj._to_transformer_winding = None
            self._to_winding_test.remove(obj)
    # >>> to_winding_test

    # <<< power_transformer
    # @generated
    def get_power_transformer(self):
        """ A transformer has windings
        """
        return self._power_transformer

    def set_power_transformer(self, value):
        if self._power_transformer is not None:
            filtered = [x for x in self.power_transformer.transformer_windings if x != self]
            self._power_transformer._transformer_windings = filtered

        self._power_transformer = value
        if self._power_transformer is not None:
            self._power_transformer._transformer_windings.append(self)

    power_transformer = property(get_power_transformer, set_power_transformer)
    # >>> power_transformer

    # <<< from_winding_test
    # @generated
    def get_from_winding_test(self):
        """ The transformer winding tests for which the transformer winding (terminal) participates as the 'from' part of the test.
        """
        return self._from_winding_test

    def set_from_winding_test(self, value):
        for x in self._from_winding_test:
            x._from_transformer_winding = None
        for y in value:
            y._from_transformer_winding = self
        self._from_winding_test = value

    from_winding_test = property(get_from_winding_test, set_from_winding_test)

    def add_from_winding_test(self, *from_winding_test):
        for obj in from_winding_test:
            obj._from_transformer_winding = self
            self._from_winding_test.append(obj)

    def remove_from_winding_test(self, *from_winding_test):
        for obj in from_winding_test:
            obj._from_transformer_winding = None
            self._from_winding_test.remove(obj)
    # >>> from_winding_test

    # <<< ratio_tap_changer
    # @generated
    def get_ratio_tap_changer(self):
        """ The ratio tap changer associated with the transformer winding.
        """
        return self._ratio_tap_changer

    def set_ratio_tap_changer(self, value):
        if self._ratio_tap_changer is not None:
            self._ratio_tap_changer._transformer_winding = None

        self._ratio_tap_changer = value
        if self._ratio_tap_changer is not None:
            self._ratio_tap_changer._transformer_winding = self

    ratio_tap_changer = property(get_ratio_tap_changer, set_ratio_tap_changer)
    # >>> ratio_tap_changer

    # <<< phase_tap_changer
    # @generated
    def get_phase_tap_changer(self):
        """ The phase tap changer associated with the transformer winding.
        """
        return self._phase_tap_changer

    def set_phase_tap_changer(self, value):
        if self._phase_tap_changer is not None:
            self._phase_tap_changer._transformer_winding = None

        self._phase_tap_changer = value
        if self._phase_tap_changer is not None:
            self._phase_tap_changer._transformer_winding = self

    phase_tap_changer = property(get_phase_tap_changer, set_phase_tap_changer)
    # >>> phase_tap_changer


    def __str__(self):
        """ Returns a string representation of the TransformerWinding.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< transformer_winding.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the TransformerWinding.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "TransformerWinding", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.to_winding_test:
            s += '%s<%s:TransformerWinding.to_winding_test rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.power_transformer is not None:
            s += '%s<%s:TransformerWinding.power_transformer rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.power_transformer.uri)
        for obj in self.from_winding_test:
            s += '%s<%s:TransformerWinding.from_winding_test rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.ratio_tap_changer is not None:
            s += '%s<%s:TransformerWinding.ratio_tap_changer rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.ratio_tap_changer.uri)
        if self.phase_tap_changer is not None:
            s += '%s<%s:TransformerWinding.phase_tap_changer rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.phase_tap_changer.uri)
        s += '%s<%s:TransformerWinding.winding_type>%s</%s:TransformerWinding.winding_type>' % \
            (indent, ns_prefix, self.winding_type, ns_prefix)
        s += '%s<%s:TransformerWinding.connection_type>%s</%s:TransformerWinding.connection_type>' % \
            (indent, ns_prefix, self.connection_type, ns_prefix)
        s += '%s<%s:TransformerWinding.short_term_s>%s</%s:TransformerWinding.short_term_s>' % \
            (indent, ns_prefix, self.short_term_s, ns_prefix)
        s += '%s<%s:TransformerWinding.rated_u>%s</%s:TransformerWinding.rated_u>' % \
            (indent, ns_prefix, self.rated_u, ns_prefix)
        s += '%s<%s:TransformerWinding.grounded>%s</%s:TransformerWinding.grounded>' % \
            (indent, ns_prefix, self.grounded, ns_prefix)
        s += '%s<%s:TransformerWinding.r0>%s</%s:TransformerWinding.r0>' % \
            (indent, ns_prefix, self.r0, ns_prefix)
        s += '%s<%s:TransformerWinding.rated_s>%s</%s:TransformerWinding.rated_s>' % \
            (indent, ns_prefix, self.rated_s, ns_prefix)
        s += '%s<%s:TransformerWinding.emergency_s>%s</%s:TransformerWinding.emergency_s>' % \
            (indent, ns_prefix, self.emergency_s, ns_prefix)
        s += '%s<%s:TransformerWinding.b0>%s</%s:TransformerWinding.b0>' % \
            (indent, ns_prefix, self.b0, ns_prefix)
        s += '%s<%s:TransformerWinding.xground>%s</%s:TransformerWinding.xground>' % \
            (indent, ns_prefix, self.xground, ns_prefix)
        s += '%s<%s:TransformerWinding.g0>%s</%s:TransformerWinding.g0>' % \
            (indent, ns_prefix, self.g0, ns_prefix)
        s += '%s<%s:TransformerWinding.b>%s</%s:TransformerWinding.b>' % \
            (indent, ns_prefix, self.b, ns_prefix)
        s += '%s<%s:TransformerWinding.r>%s</%s:TransformerWinding.r>' % \
            (indent, ns_prefix, self.r, ns_prefix)
        s += '%s<%s:TransformerWinding.rground>%s</%s:TransformerWinding.rground>' % \
            (indent, ns_prefix, self.rground, ns_prefix)
        s += '%s<%s:TransformerWinding.x>%s</%s:TransformerWinding.x>' % \
            (indent, ns_prefix, self.x, ns_prefix)
        s += '%s<%s:TransformerWinding.insulation_u>%s</%s:TransformerWinding.insulation_u>' % \
            (indent, ns_prefix, self.insulation_u, ns_prefix)
        s += '%s<%s:TransformerWinding.g>%s</%s:TransformerWinding.g>' % \
            (indent, ns_prefix, self.g, ns_prefix)
        s += '%s<%s:TransformerWinding.x0>%s</%s:TransformerWinding.x0>' % \
            (indent, ns_prefix, self.x0, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "TransformerWinding")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> transformer_winding.serialize


class CompositeSwitch(Equipment):
    """ A model of a set of individual Switches normally enclosed within the same cabinet and possibly with interlocks that restrict the combination of switch positions. These are typically found in medium voltage distribution networks.  A CompositeSwitch could represent a Ring-Main-Unit (RMU), or pad-mounted switchgear, with primitive internal devices such as an internal bus-bar plus 3 or 4 internal switches each of which may individually be open or closed. A CompositeSwitch and a set of contained Switches can also be used to represent a multi-position switch e.g. a switch that can connect a circuit to Ground, Open or Busbar.
    """
    # <<< composite_switch
    # @generated
    def __init__(self, composite_switch_type='', switches=None, **kw_args):
        """ Initialises a new 'CompositeSwitch' instance.
        """
        # An alphanumeric code that can be used as a reference to extar information such as the description of the interlocking scheme if any 
        self.composite_switch_type = composite_switch_type


        self._switches = []
        if switches is not None:
            self.switches = switches
        else:
            self.switches = []


        super(CompositeSwitch, self).__init__(**kw_args)
    # >>> composite_switch

    # <<< switches
    # @generated
    def get_switches(self):
        """ Switches contained in this Composite switch.
        """
        return self._switches

    def set_switches(self, value):
        for x in self._switches:
            x._composite_switch = None
        for y in value:
            y._composite_switch = self
        self._switches = value

    switches = property(get_switches, set_switches)

    def add_switches(self, *switches):
        for obj in switches:
            obj._composite_switch = self
            self._switches.append(obj)

    def remove_switches(self, *switches):
        for obj in switches:
            obj._composite_switch = None
            self._switches.remove(obj)
    # >>> switches


    def __str__(self):
        """ Returns a string representation of the CompositeSwitch.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< composite_switch.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the CompositeSwitch.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "CompositeSwitch", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.switches:
            s += '%s<%s:CompositeSwitch.switches rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:CompositeSwitch.composite_switch_type>%s</%s:CompositeSwitch.composite_switch_type>' % \
            (indent, ns_prefix, self.composite_switch_type, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "CompositeSwitch")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> composite_switch.serialize


class VoltageControlZone(PowerSystemResource):
    """ An area of the power system network which is defined for secondary voltage control purposes. A voltage control zone consists of a collection of substations with a designated bus bar section whose voltage will be controlled.
    """
    # <<< voltage_control_zone
    # @generated
    def __init__(self, regulation_schedule=None, busbar_section=None, **kw_args):
        """ Initialises a new 'VoltageControlZone' instance.
        """

        self._regulation_schedule = None
        self.regulation_schedule = regulation_schedule

        self._busbar_section = None
        self.busbar_section = busbar_section


        super(VoltageControlZone, self).__init__(**kw_args)
    # >>> voltage_control_zone

    # <<< regulation_schedule
    # @generated
    def get_regulation_schedule(self):
        """ A VoltageControlZone may have a  voltage regulation schedule.
        """
        return self._regulation_schedule

    def set_regulation_schedule(self, value):
        if self._regulation_schedule is not None:
            filtered = [x for x in self.regulation_schedule.voltage_control_zones if x != self]
            self._regulation_schedule._voltage_control_zones = filtered

        self._regulation_schedule = value
        if self._regulation_schedule is not None:
            self._regulation_schedule._voltage_control_zones.append(self)

    regulation_schedule = property(get_regulation_schedule, set_regulation_schedule)
    # >>> regulation_schedule

    # <<< busbar_section
    # @generated
    def get_busbar_section(self):
        """ A VoltageControlZone is controlled by a designated BusbarSection.
        """
        return self._busbar_section

    def set_busbar_section(self, value):
        if self._busbar_section is not None:
            self._busbar_section._voltage_control_zone = None

        self._busbar_section = value
        if self._busbar_section is not None:
            self._busbar_section._voltage_control_zone = self

    busbar_section = property(get_busbar_section, set_busbar_section)
    # >>> busbar_section


    def __str__(self):
        """ Returns a string representation of the VoltageControlZone.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< voltage_control_zone.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the VoltageControlZone.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "VoltageControlZone", self.uri)
        if format:
            indent += ' ' * depth

        if self.regulation_schedule is not None:
            s += '%s<%s:VoltageControlZone.regulation_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.regulation_schedule.uri)
        if self.busbar_section is not None:
            s += '%s<%s:VoltageControlZone.busbar_section rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.busbar_section.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "VoltageControlZone")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> voltage_control_zone.serialize


class RectifierInverter(ConductingEquipment):
    """ Bi-directional AC-DC conversion equipment that can be used to control DC current, DC voltage, DC power flow, or firing angle.
    """
    # <<< rectifier_inverter
    # @generated
    def __init__(self, rated_u=0.0, max_p=0.0, min_p=0.0, commutating_resistance=0.0, bridges=0, compound_resistance=0.0, min_compound_voltage=0.0, commutating_reactance=0.0, min_u=0.0, operating_mode='', max_u=0.0, frequency=0.0, **kw_args):
        """ Initialises a new 'RectifierInverter' instance.
        """
        # Rectifier/inverter primary base voltage 
        self.rated_u = rated_u

        # The maximum active power on the DC side at which the fconverter should operate. 
        self.max_p = max_p

        # The minimum active power on the DC side at which the converter should operate. 
        self.min_p = min_p

        # Commutating resistance. 
        self.commutating_resistance = commutating_resistance

        # Number of bridges 
        self.bridges = bridges

        # Compounding resistance. 
        self.compound_resistance = compound_resistance

        # Minimum compounded DC voltage 
        self.min_compound_voltage = min_compound_voltage

        # Commutating reactance at AC bus frequency. 
        self.commutating_reactance = commutating_reactance

        # The minimum voltage on the DC side at which the converter should operate. 
        self.min_u = min_u

        # Operating mode for the converter. 
        self.operating_mode = operating_mode

        # The maximum voltage on the DC side at which the converter should operate. 
        self.max_u = max_u

        # Frequency on the AC side. 
        self.frequency = frequency



        super(RectifierInverter, self).__init__(**kw_args)
    # >>> rectifier_inverter


    def __str__(self):
        """ Returns a string representation of the RectifierInverter.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< rectifier_inverter.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the RectifierInverter.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "RectifierInverter", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:RectifierInverter.rated_u>%s</%s:RectifierInverter.rated_u>' % \
            (indent, ns_prefix, self.rated_u, ns_prefix)
        s += '%s<%s:RectifierInverter.max_p>%s</%s:RectifierInverter.max_p>' % \
            (indent, ns_prefix, self.max_p, ns_prefix)
        s += '%s<%s:RectifierInverter.min_p>%s</%s:RectifierInverter.min_p>' % \
            (indent, ns_prefix, self.min_p, ns_prefix)
        s += '%s<%s:RectifierInverter.commutating_resistance>%s</%s:RectifierInverter.commutating_resistance>' % \
            (indent, ns_prefix, self.commutating_resistance, ns_prefix)
        s += '%s<%s:RectifierInverter.bridges>%s</%s:RectifierInverter.bridges>' % \
            (indent, ns_prefix, self.bridges, ns_prefix)
        s += '%s<%s:RectifierInverter.compound_resistance>%s</%s:RectifierInverter.compound_resistance>' % \
            (indent, ns_prefix, self.compound_resistance, ns_prefix)
        s += '%s<%s:RectifierInverter.min_compound_voltage>%s</%s:RectifierInverter.min_compound_voltage>' % \
            (indent, ns_prefix, self.min_compound_voltage, ns_prefix)
        s += '%s<%s:RectifierInverter.commutating_reactance>%s</%s:RectifierInverter.commutating_reactance>' % \
            (indent, ns_prefix, self.commutating_reactance, ns_prefix)
        s += '%s<%s:RectifierInverter.min_u>%s</%s:RectifierInverter.min_u>' % \
            (indent, ns_prefix, self.min_u, ns_prefix)
        s += '%s<%s:RectifierInverter.operating_mode>%s</%s:RectifierInverter.operating_mode>' % \
            (indent, ns_prefix, self.operating_mode, ns_prefix)
        s += '%s<%s:RectifierInverter.max_u>%s</%s:RectifierInverter.max_u>' % \
            (indent, ns_prefix, self.max_u, ns_prefix)
        s += '%s<%s:RectifierInverter.frequency>%s</%s:RectifierInverter.frequency>' % \
            (indent, ns_prefix, self.frequency, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "RectifierInverter")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> rectifier_inverter.serialize


class RegulationSchedule(SeasonDayTypeSchedule):
    """ A pre-established pattern over time for a controlled variable, e.g., busbar voltage.
    """
    # <<< regulation_schedule
    # @generated
    def __init__(self, line_drop_compensation=False, line_drop_x=0.0, line_drop_r=0.0, regulating_control=None, voltage_control_zones=None, **kw_args):
        """ Initialises a new 'RegulationSchedule' instance.
        """
        # Flag to indicate that line drop compensation is to be applied 
        self.line_drop_compensation = line_drop_compensation

        # Line drop reactance. 
        self.line_drop_x = line_drop_x

        # Line drop resistance. 
        self.line_drop_r = line_drop_r


        self._regulating_control = None
        self.regulating_control = regulating_control

        self._voltage_control_zones = []
        if voltage_control_zones is not None:
            self.voltage_control_zones = voltage_control_zones
        else:
            self.voltage_control_zones = []


        super(RegulationSchedule, self).__init__(**kw_args)
    # >>> regulation_schedule

    # <<< regulating_control
    # @generated
    def get_regulating_control(self):
        """ Regulating controls that have this Schedule.
        """
        return self._regulating_control

    def set_regulating_control(self, value):
        if self._regulating_control is not None:
            filtered = [x for x in self.regulating_control.regulation_schedule if x != self]
            self._regulating_control._regulation_schedule = filtered

        self._regulating_control = value
        if self._regulating_control is not None:
            self._regulating_control._regulation_schedule.append(self)

    regulating_control = property(get_regulating_control, set_regulating_control)
    # >>> regulating_control

    # <<< voltage_control_zones
    # @generated
    def get_voltage_control_zones(self):
        """ A VoltageControlZone may have a  voltage regulation schedule.
        """
        return self._voltage_control_zones

    def set_voltage_control_zones(self, value):
        for x in self._voltage_control_zones:
            x._regulation_schedule = None
        for y in value:
            y._regulation_schedule = self
        self._voltage_control_zones = value

    voltage_control_zones = property(get_voltage_control_zones, set_voltage_control_zones)

    def add_voltage_control_zones(self, *voltage_control_zones):
        for obj in voltage_control_zones:
            obj._regulation_schedule = self
            self._voltage_control_zones.append(obj)

    def remove_voltage_control_zones(self, *voltage_control_zones):
        for obj in voltage_control_zones:
            obj._regulation_schedule = None
            self._voltage_control_zones.remove(obj)
    # >>> voltage_control_zones


    def __str__(self):
        """ Returns a string representation of the RegulationSchedule.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< regulation_schedule.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the RegulationSchedule.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "RegulationSchedule", self.uri)
        if format:
            indent += ' ' * depth

        if self.regulating_control is not None:
            s += '%s<%s:RegulationSchedule.regulating_control rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.regulating_control.uri)
        for obj in self.voltage_control_zones:
            s += '%s<%s:RegulationSchedule.voltage_control_zones rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:RegulationSchedule.line_drop_compensation>%s</%s:RegulationSchedule.line_drop_compensation>' % \
            (indent, ns_prefix, self.line_drop_compensation, ns_prefix)
        s += '%s<%s:RegulationSchedule.line_drop_x>%s</%s:RegulationSchedule.line_drop_x>' % \
            (indent, ns_prefix, self.line_drop_x, ns_prefix)
        s += '%s<%s:RegulationSchedule.line_drop_r>%s</%s:RegulationSchedule.line_drop_r>' % \
            (indent, ns_prefix, self.line_drop_r, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value2_multiplier>%s</%s:BasicIntervalSchedule.value2_multiplier>' % \
            (indent, ns_prefix, self.value2_multiplier, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value1_unit>%s</%s:BasicIntervalSchedule.value1_unit>' % \
            (indent, ns_prefix, self.value1_unit, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value2_unit>%s</%s:BasicIntervalSchedule.value2_unit>' % \
            (indent, ns_prefix, self.value2_unit, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.value1_multiplier>%s</%s:BasicIntervalSchedule.value1_multiplier>' % \
            (indent, ns_prefix, self.value1_multiplier, ns_prefix)
        s += '%s<%s:BasicIntervalSchedule.start_time>%s</%s:BasicIntervalSchedule.start_time>' % \
            (indent, ns_prefix, self.start_time, ns_prefix)
        for obj in self.time_points:
            s += '%s<%s:RegularIntervalSchedule.time_points rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:RegularIntervalSchedule.time_step>%s</%s:RegularIntervalSchedule.time_step>' % \
            (indent, ns_prefix, self.time_step, ns_prefix)
        s += '%s<%s:RegularIntervalSchedule.end_time>%s</%s:RegularIntervalSchedule.end_time>' % \
            (indent, ns_prefix, self.end_time, ns_prefix)
        if self.day_type is not None:
            s += '%s<%s:SeasonDayTypeSchedule.day_type rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.day_type.uri)
        if self.season is not None:
            s += '%s<%s:SeasonDayTypeSchedule.season rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.season.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "RegulationSchedule")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> regulation_schedule.serialize


class Fuse(Switch):
    """ An overcurrent protective device with a circuit opening fusible part that is heated and severed by the passage of overcurrent through it. A fuse is considered a switching device because it breaks current.
    """
    # <<< fuse
    # @generated
    def __init__(self, rating_current=0.0, **kw_args):
        """ Initialises a new 'Fuse' instance.
        """
        # Fault interrupting current rating. 
        self.rating_current = rating_current



        super(Fuse, self).__init__(**kw_args)
    # >>> fuse


    def __str__(self):
        """ Returns a string representation of the Fuse.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< fuse.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Fuse.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Fuse", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:Fuse.rating_current>%s</%s:Fuse.rating_current>' % \
            (indent, ns_prefix, self.rating_current, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        for obj in self.load_mgmt_functions:
            s += '%s<%s:Switch.load_mgmt_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.composite_switch is not None:
            s += '%s<%s:Switch.composite_switch rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.composite_switch.uri)
        for obj in self.switch_schedules:
            s += '%s<%s:Switch.switch_schedules rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.connect_disconnect_functions:
            s += '%s<%s:Switch.connect_disconnect_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.switching_operations:
            s += '%s<%s:Switch.switching_operations rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Switch.switch_on_count>%s</%s:Switch.switch_on_count>' % \
            (indent, ns_prefix, self.switch_on_count, ns_prefix)
        s += '%s<%s:Switch.normal_open>%s</%s:Switch.normal_open>' % \
            (indent, ns_prefix, self.normal_open, ns_prefix)
        s += '%s<%s:Switch.retained>%s</%s:Switch.retained>' % \
            (indent, ns_prefix, self.retained, ns_prefix)
        s += '%s<%s:Switch.switch_on_date>%s</%s:Switch.switch_on_date>' % \
            (indent, ns_prefix, self.switch_on_date, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Fuse")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> fuse.serialize


class PhaseTapChanger(TapChanger):
    """ A specialization of a voltage tap changer that has detailed modeling for phase shifting capabilities.   A phase shifting tap changer is also in general a voltage magnitude transformer.    The symmetrical and asymmetrical transformer tap changer models are defined here.
    """
    # <<< phase_tap_changer
    # @generated
    def __init__(self, phase_tap_changer_type='symmetrical', winding_connection_angle=0.0, step_phase_shift_increment=0.0, x_step_max=0.0, x_step_min=0.0, voltage_step_increment_out_of_phase=0.0, nominal_voltage_out_of_phase=0.0, phase_variation_curve=None, winding=None, transformer_winding=None, **kw_args):
        """ Initialises a new 'PhaseTapChanger' instance.
        """
        # The type of phase shifter construction. Values are: "symmetrical", "unknown", "asymmetrical"
        self.phase_tap_changer_type = 'symmetrical'

        # The phase angle between the in-phase winding and the out-of -phase winding used for creating phase shift.   It is only possible to have a symmemtrical transformer if this angle is 90 degrees. 
        self.winding_connection_angle = winding_connection_angle

        # Phase shift per step position. A positive value indicates a positive phase shift from the winding where the tap is located to the other winding (for a two-winding transformer). The actual phase shift increment might be more accureatly computed from the symmetrical or asymmetrical models or a tap step table lookup if those are available. 
        self.step_phase_shift_increment = step_phase_shift_increment

        # The reactance at the maximum tap step. 
        self.x_step_max = x_step_max

        # The reactance at the minimum tap step. 
        self.x_step_min = x_step_min

        # The voltage step increment on the out of phase winding.    This voltage step on the out of phase winding of the phase shifter.  Similar to TapChanger.voltageStepIncrement, but it is applied only to the out of phase winding. 
        self.voltage_step_increment_out_of_phase = voltage_step_increment_out_of_phase

        # Similar to TapChanger.nominalVoltage, but this is the nominal voltage in the out of phase winding at the nominal tap step. A typical case may have zero voltage at the nominal step, indicating no phase shift at the nominal voltage. 
        self.nominal_voltage_out_of_phase = nominal_voltage_out_of_phase


        self._phase_variation_curve = None
        self.phase_variation_curve = phase_variation_curve

        self._winding = None
        self.winding = winding

        self._transformer_winding = None
        self.transformer_winding = transformer_winding


        super(PhaseTapChanger, self).__init__(**kw_args)
    # >>> phase_tap_changer

    # <<< phase_variation_curve
    # @generated
    def get_phase_variation_curve(self):
        """ A PhaseTapChanger can have an associated PhaseVariationCurve to define phase shift variations with tap step changes.
        """
        return self._phase_variation_curve

    def set_phase_variation_curve(self, value):
        if self._phase_variation_curve is not None:
            self._phase_variation_curve._phase_tap_changer = None

        self._phase_variation_curve = value
        if self._phase_variation_curve is not None:
            self._phase_variation_curve._phase_tap_changer = self

    phase_variation_curve = property(get_phase_variation_curve, set_phase_variation_curve)
    # >>> phase_variation_curve

    # <<< winding
    # @generated
    def get_winding(self):
        """ Transformer winding to which this phase tap changer belongs.
        """
        return self._winding

    def set_winding(self, value):
        if self._winding is not None:
            self._winding._phase_tap_changer = None

        self._winding = value
        if self._winding is not None:
            self._winding._phase_tap_changer = self

    winding = property(get_winding, set_winding)
    # >>> winding

    # <<< transformer_winding
    # @generated
    def get_transformer_winding(self):
        """ The transformer winding to which the phase tap changer belongs.
        """
        return self._transformer_winding

    def set_transformer_winding(self, value):
        if self._transformer_winding is not None:
            self._transformer_winding._phase_tap_changer = None

        self._transformer_winding = value
        if self._transformer_winding is not None:
            self._transformer_winding._phase_tap_changer = self

    transformer_winding = property(get_transformer_winding, set_transformer_winding)
    # >>> transformer_winding


    def __str__(self):
        """ Returns a string representation of the PhaseTapChanger.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< phase_tap_changer.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the PhaseTapChanger.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "PhaseTapChanger", self.uri)
        if format:
            indent += ' ' * depth

        if self.phase_variation_curve is not None:
            s += '%s<%s:PhaseTapChanger.phase_variation_curve rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.phase_variation_curve.uri)
        if self.winding is not None:
            s += '%s<%s:PhaseTapChanger.winding rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.winding.uri)
        if self.transformer_winding is not None:
            s += '%s<%s:PhaseTapChanger.transformer_winding rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.transformer_winding.uri)
        s += '%s<%s:PhaseTapChanger.phase_tap_changer_type>%s</%s:PhaseTapChanger.phase_tap_changer_type>' % \
            (indent, ns_prefix, self.phase_tap_changer_type, ns_prefix)
        s += '%s<%s:PhaseTapChanger.winding_connection_angle>%s</%s:PhaseTapChanger.winding_connection_angle>' % \
            (indent, ns_prefix, self.winding_connection_angle, ns_prefix)
        s += '%s<%s:PhaseTapChanger.step_phase_shift_increment>%s</%s:PhaseTapChanger.step_phase_shift_increment>' % \
            (indent, ns_prefix, self.step_phase_shift_increment, ns_prefix)
        s += '%s<%s:PhaseTapChanger.x_step_max>%s</%s:PhaseTapChanger.x_step_max>' % \
            (indent, ns_prefix, self.x_step_max, ns_prefix)
        s += '%s<%s:PhaseTapChanger.x_step_min>%s</%s:PhaseTapChanger.x_step_min>' % \
            (indent, ns_prefix, self.x_step_min, ns_prefix)
        s += '%s<%s:PhaseTapChanger.voltage_step_increment_out_of_phase>%s</%s:PhaseTapChanger.voltage_step_increment_out_of_phase>' % \
            (indent, ns_prefix, self.voltage_step_increment_out_of_phase, ns_prefix)
        s += '%s<%s:PhaseTapChanger.nominal_voltage_out_of_phase>%s</%s:PhaseTapChanger.nominal_voltage_out_of_phase>' % \
            (indent, ns_prefix, self.nominal_voltage_out_of_phase, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.regulating_control is not None:
            s += '%s<%s:TapChanger.regulating_control rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.regulating_control.uri)
        if self.impedance_variation_curve is not None:
            s += '%s<%s:TapChanger.impedance_variation_curve rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.impedance_variation_curve.uri)
        if self.sv_tap_step is not None:
            s += '%s<%s:TapChanger.sv_tap_step rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_tap_step.uri)
        for obj in self.tap_schedules:
            s += '%s<%s:TapChanger.tap_schedules rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TapChanger.neutral_step>%s</%s:TapChanger.neutral_step>' % \
            (indent, ns_prefix, self.neutral_step, ns_prefix)
        s += '%s<%s:TapChanger.subsequent_delay>%s</%s:TapChanger.subsequent_delay>' % \
            (indent, ns_prefix, self.subsequent_delay, ns_prefix)
        s += '%s<%s:TapChanger.neutral_u>%s</%s:TapChanger.neutral_u>' % \
            (indent, ns_prefix, self.neutral_u, ns_prefix)
        s += '%s<%s:TapChanger.step_voltage_increment>%s</%s:TapChanger.step_voltage_increment>' % \
            (indent, ns_prefix, self.step_voltage_increment, ns_prefix)
        s += '%s<%s:TapChanger.low_step>%s</%s:TapChanger.low_step>' % \
            (indent, ns_prefix, self.low_step, ns_prefix)
        s += '%s<%s:TapChanger.normal_step>%s</%s:TapChanger.normal_step>' % \
            (indent, ns_prefix, self.normal_step, ns_prefix)
        s += '%s<%s:TapChanger.regulation_status>%s</%s:TapChanger.regulation_status>' % \
            (indent, ns_prefix, self.regulation_status, ns_prefix)
        s += '%s<%s:TapChanger.high_step>%s</%s:TapChanger.high_step>' % \
            (indent, ns_prefix, self.high_step, ns_prefix)
        s += '%s<%s:TapChanger.initial_delay>%s</%s:TapChanger.initial_delay>' % \
            (indent, ns_prefix, self.initial_delay, ns_prefix)
        s += '%s<%s:TapChanger.ltc_flag>%s</%s:TapChanger.ltc_flag>' % \
            (indent, ns_prefix, self.ltc_flag, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "PhaseTapChanger")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> phase_tap_changer.serialize


class ProtectedSwitch(Switch):
    """ A ProtectedSwitch is a switching device that can be operated by ProtectionEquipment.
    """
    # <<< protected_switch
    # @generated
    def __init__(self, reclose_sequences=None, **kw_args):
        """ Initialises a new 'ProtectedSwitch' instance.
        """

        self._reclose_sequences = []
        if reclose_sequences is not None:
            self.reclose_sequences = reclose_sequences
        else:
            self.reclose_sequences = []


        super(ProtectedSwitch, self).__init__(**kw_args)
    # >>> protected_switch

    # <<< reclose_sequences
    # @generated
    def get_reclose_sequences(self):
        """ A breaker may have zero or more automatic reclosures after a trip occurs.
        """
        return self._reclose_sequences

    def set_reclose_sequences(self, value):
        for x in self._reclose_sequences:
            x._protected_switch = None
        for y in value:
            y._protected_switch = self
        self._reclose_sequences = value

    reclose_sequences = property(get_reclose_sequences, set_reclose_sequences)

    def add_reclose_sequences(self, *reclose_sequences):
        for obj in reclose_sequences:
            obj._protected_switch = self
            self._reclose_sequences.append(obj)

    def remove_reclose_sequences(self, *reclose_sequences):
        for obj in reclose_sequences:
            obj._protected_switch = None
            self._reclose_sequences.remove(obj)
    # >>> reclose_sequences


    def __str__(self):
        """ Returns a string representation of the ProtectedSwitch.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< protected_switch.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ProtectedSwitch.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ProtectedSwitch", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.reclose_sequences:
            s += '%s<%s:ProtectedSwitch.reclose_sequences rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        for obj in self.load_mgmt_functions:
            s += '%s<%s:Switch.load_mgmt_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.composite_switch is not None:
            s += '%s<%s:Switch.composite_switch rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.composite_switch.uri)
        for obj in self.switch_schedules:
            s += '%s<%s:Switch.switch_schedules rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.connect_disconnect_functions:
            s += '%s<%s:Switch.connect_disconnect_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.switching_operations:
            s += '%s<%s:Switch.switching_operations rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Switch.switch_on_count>%s</%s:Switch.switch_on_count>' % \
            (indent, ns_prefix, self.switch_on_count, ns_prefix)
        s += '%s<%s:Switch.normal_open>%s</%s:Switch.normal_open>' % \
            (indent, ns_prefix, self.normal_open, ns_prefix)
        s += '%s<%s:Switch.retained>%s</%s:Switch.retained>' % \
            (indent, ns_prefix, self.retained, ns_prefix)
        s += '%s<%s:Switch.switch_on_date>%s</%s:Switch.switch_on_date>' % \
            (indent, ns_prefix, self.switch_on_date, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ProtectedSwitch")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> protected_switch.serialize


class Disconnector(Switch):
    """ A manually operated or motor operated mechanical switching device used for changing the connections in a circuit, or for isolating a circuit or equipment from a source of power. It is required to open or close circuits when negligible current is broken or made.
    """
    pass
    # <<< disconnector
    # @generated
    def __init__(self, **kw_args):
        """ Initialises a new 'Disconnector' instance.
        """


        super(Disconnector, self).__init__(**kw_args)
    # >>> disconnector


    def __str__(self):
        """ Returns a string representation of the Disconnector.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< disconnector.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Disconnector.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Disconnector", self.uri)
        if format:
            indent += ' ' * depth

        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        for obj in self.load_mgmt_functions:
            s += '%s<%s:Switch.load_mgmt_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.composite_switch is not None:
            s += '%s<%s:Switch.composite_switch rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.composite_switch.uri)
        for obj in self.switch_schedules:
            s += '%s<%s:Switch.switch_schedules rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.connect_disconnect_functions:
            s += '%s<%s:Switch.connect_disconnect_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.switching_operations:
            s += '%s<%s:Switch.switching_operations rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Switch.switch_on_count>%s</%s:Switch.switch_on_count>' % \
            (indent, ns_prefix, self.switch_on_count, ns_prefix)
        s += '%s<%s:Switch.normal_open>%s</%s:Switch.normal_open>' % \
            (indent, ns_prefix, self.normal_open, ns_prefix)
        s += '%s<%s:Switch.retained>%s</%s:Switch.retained>' % \
            (indent, ns_prefix, self.retained, ns_prefix)
        s += '%s<%s:Switch.switch_on_date>%s</%s:Switch.switch_on_date>' % \
            (indent, ns_prefix, self.switch_on_date, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Disconnector")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> disconnector.serialize


class Breaker(ProtectedSwitch):
    """ A mechanical switching device capable of making, carrying, and breaking currents under normal circuit conditions and also making, carrying for a specified time, and breaking currents under specified abnormal circuit conditions e.g.  those of short circuit.
    """
    # <<< breaker
    # @generated
    def __init__(self, in_transit_time=0.0, rated_current=0.0, **kw_args):
        """ Initialises a new 'Breaker' instance.
        """
        # The transition time from open to close. 
        self.in_transit_time = in_transit_time

        # Fault interrupting current rating. 
        self.rated_current = rated_current



        super(Breaker, self).__init__(**kw_args)
    # >>> breaker


    def __str__(self):
        """ Returns a string representation of the Breaker.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< breaker.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Breaker.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Breaker", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:Breaker.in_transit_time>%s</%s:Breaker.in_transit_time>' % \
            (indent, ns_prefix, self.in_transit_time, ns_prefix)
        s += '%s<%s:Breaker.rated_current>%s</%s:Breaker.rated_current>' % \
            (indent, ns_prefix, self.rated_current, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        for obj in self.load_mgmt_functions:
            s += '%s<%s:Switch.load_mgmt_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.composite_switch is not None:
            s += '%s<%s:Switch.composite_switch rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.composite_switch.uri)
        for obj in self.switch_schedules:
            s += '%s<%s:Switch.switch_schedules rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.connect_disconnect_functions:
            s += '%s<%s:Switch.connect_disconnect_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.switching_operations:
            s += '%s<%s:Switch.switching_operations rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Switch.switch_on_count>%s</%s:Switch.switch_on_count>' % \
            (indent, ns_prefix, self.switch_on_count, ns_prefix)
        s += '%s<%s:Switch.normal_open>%s</%s:Switch.normal_open>' % \
            (indent, ns_prefix, self.normal_open, ns_prefix)
        s += '%s<%s:Switch.retained>%s</%s:Switch.retained>' % \
            (indent, ns_prefix, self.retained, ns_prefix)
        s += '%s<%s:Switch.switch_on_date>%s</%s:Switch.switch_on_date>' % \
            (indent, ns_prefix, self.switch_on_date, ns_prefix)
        for obj in self.reclose_sequences:
            s += '%s<%s:ProtectedSwitch.reclose_sequences rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Breaker")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> breaker.serialize


class Jumper(Switch):
    """ A short section of conductor with negligible impedance which can be manually removed and replaced if the circuit is de-energized. Note that zero-impedance branches can be modelled by an ACLineSegment with a zero impedance ConductorType
    """
    pass
    # <<< jumper
    # @generated
    def __init__(self, **kw_args):
        """ Initialises a new 'Jumper' instance.
        """


        super(Jumper, self).__init__(**kw_args)
    # >>> jumper


    def __str__(self):
        """ Returns a string representation of the Jumper.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< jumper.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Jumper.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Jumper", self.uri)
        if format:
            indent += ' ' * depth

        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        for obj in self.load_mgmt_functions:
            s += '%s<%s:Switch.load_mgmt_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.composite_switch is not None:
            s += '%s<%s:Switch.composite_switch rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.composite_switch.uri)
        for obj in self.switch_schedules:
            s += '%s<%s:Switch.switch_schedules rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.connect_disconnect_functions:
            s += '%s<%s:Switch.connect_disconnect_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.switching_operations:
            s += '%s<%s:Switch.switching_operations rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Switch.switch_on_count>%s</%s:Switch.switch_on_count>' % \
            (indent, ns_prefix, self.switch_on_count, ns_prefix)
        s += '%s<%s:Switch.normal_open>%s</%s:Switch.normal_open>' % \
            (indent, ns_prefix, self.normal_open, ns_prefix)
        s += '%s<%s:Switch.retained>%s</%s:Switch.retained>' % \
            (indent, ns_prefix, self.retained, ns_prefix)
        s += '%s<%s:Switch.switch_on_date>%s</%s:Switch.switch_on_date>' % \
            (indent, ns_prefix, self.switch_on_date, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Jumper")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> jumper.serialize


class ACLineSegment(Conductor):
    """ A wire or combination of wires, with consistent electrical characteristics, building a single electrical system, used to carry alternating current between points in the power system.
    """
    # <<< acline_segment
    # @generated
    def __init__(self, bch=0.0, r=0.0, gch=0.0, r0=0.0, b0ch=0.0, x0=0.0, x=0.0, g0ch=0.0, **kw_args):
        """ Initialises a new 'ACLineSegment' instance.
        """
        # Positive sequence shunt (charging) susceptance, uniformly distributed, of the entire line section.  This value represents the full charging over the full length of the line. 
        self.bch = bch

        # Positive sequence series resistance of the entire line section. 
        self.r = r

        # Positive sequence shunt (charging) conductance, uniformly distributed, of the entire line section. 
        self.gch = gch

        # Zero sequence series resistance of the entire line section. 
        self.r0 = r0

        # Zero sequence shunt (charging) susceptance, uniformly distributed, of the entire line section. 
        self.b0ch = b0ch

        # Zero sequence series reactance of the entire line section. 
        self.x0 = x0

        # Positive sequence series reactance of the entire line section. 
        self.x = x

        # Zero sequence shunt (charging) conductance, uniformly distributed, of the entire line section. 
        self.g0ch = g0ch



        super(ACLineSegment, self).__init__(**kw_args)
    # >>> acline_segment


    def __str__(self):
        """ Returns a string representation of the ACLineSegment.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< acline_segment.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ACLineSegment.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ACLineSegment", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:ACLineSegment.bch>%s</%s:ACLineSegment.bch>' % \
            (indent, ns_prefix, self.bch, ns_prefix)
        s += '%s<%s:ACLineSegment.r>%s</%s:ACLineSegment.r>' % \
            (indent, ns_prefix, self.r, ns_prefix)
        s += '%s<%s:ACLineSegment.gch>%s</%s:ACLineSegment.gch>' % \
            (indent, ns_prefix, self.gch, ns_prefix)
        s += '%s<%s:ACLineSegment.r0>%s</%s:ACLineSegment.r0>' % \
            (indent, ns_prefix, self.r0, ns_prefix)
        s += '%s<%s:ACLineSegment.b0ch>%s</%s:ACLineSegment.b0ch>' % \
            (indent, ns_prefix, self.b0ch, ns_prefix)
        s += '%s<%s:ACLineSegment.x0>%s</%s:ACLineSegment.x0>' % \
            (indent, ns_prefix, self.x0, ns_prefix)
        s += '%s<%s:ACLineSegment.x>%s</%s:ACLineSegment.x>' % \
            (indent, ns_prefix, self.x, ns_prefix)
        s += '%s<%s:ACLineSegment.g0ch>%s</%s:ACLineSegment.g0ch>' % \
            (indent, ns_prefix, self.g0ch, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        s += '%s<%s:Conductor.length>%s</%s:Conductor.length>' % \
            (indent, ns_prefix, self.length, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ACLineSegment")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> acline_segment.serialize


class BusbarSection(Connector):
    """ A conductor, or group of conductors, with negligible impedance, that serve to connect other conducting equipment within a single substation.  Voltage measurements are typically obtained from VoltageTransformers that are connected to busbar sections. A bus bar section may have many physical terminals but for analysis is modelled with exactly one logical terminal.
    """
    # <<< busbar_section
    # @generated
    def __init__(self, voltage_control_zone=None, **kw_args):
        """ Initialises a new 'BusbarSection' instance.
        """

        self._voltage_control_zone = None
        self.voltage_control_zone = voltage_control_zone


        super(BusbarSection, self).__init__(**kw_args)
    # >>> busbar_section

    # <<< voltage_control_zone
    # @generated
    def get_voltage_control_zone(self):
        """ A VoltageControlZone is controlled by a designated BusbarSection.
        """
        return self._voltage_control_zone

    def set_voltage_control_zone(self, value):
        if self._voltage_control_zone is not None:
            self._voltage_control_zone._busbar_section = None

        self._voltage_control_zone = value
        if self._voltage_control_zone is not None:
            self._voltage_control_zone._busbar_section = self

    voltage_control_zone = property(get_voltage_control_zone, set_voltage_control_zone)
    # >>> voltage_control_zone


    def __str__(self):
        """ Returns a string representation of the BusbarSection.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< busbar_section.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the BusbarSection.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "BusbarSection", self.uri)
        if format:
            indent += ' ' * depth

        if self.voltage_control_zone is not None:
            s += '%s<%s:BusbarSection.voltage_control_zone rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.voltage_control_zone.uri)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "BusbarSection")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> busbar_section.serialize


class ShuntCompensator(RegulatingCondEq):
    """ A shunt capacitor or reactor or switchable bank of shunt capacitors or reactors. A section of a shunt compensator is an individual capacitor or reactor.  A negative value for reactivePerSection indicates that the compensator is a reactor. ShuntCompensator is a single terminal device.  Ground is implied.
    """
    # <<< shunt_compensator
    # @generated
    def __init__(self, b0_per_section=0.0, maximum_sections=0, normal_sections=0, nom_q=0.0, switch_on_count=0, max_u=0.0, reactive_per_section=0.0, a_vrdelay=0.0, b_per_section=0.0, voltage_sensitivity=0.0, nom_u=0.0, g_per_section=0.0, min_u=0.0, switch_on_date='', g0_per_section=0.0, sv_shunt_compensator_sections=None, **kw_args):
        """ Initialises a new 'ShuntCompensator' instance.
        """
        # Zero sequence shunt (charging) susceptance per section 
        self.b0_per_section = b0_per_section

        # For a capacitor bank, the maximum number of sections that may be switched in. 
        self.maximum_sections = maximum_sections

        # For a capacitor bank, the normal number of sections switched in. This number should correspond to the nominal reactive power (nomQ). 
        self.normal_sections = normal_sections

        # Nominal reactive power output of the capacitor bank at the nominal voltage. This number should be positive. 
        self.nom_q = nom_q

        # The switch on count since the capacitor count was last reset or initialized. 
        self.switch_on_count = switch_on_count

        # The maximum voltage at which the capacitor bank should operate. 
        self.max_u = max_u

        # For a capacitor bank, the size in reactive power of each switchable section at the nominal voltage. 
        self.reactive_per_section = reactive_per_section

        # Time delay required for the device to be connected or disconnected by automatic voltage regulation (AVR). 
        self.a_vrdelay = a_vrdelay

        # Positive sequence shunt (charging) susceptance per section 
        self.b_per_section = b_per_section

        # Voltage sensitivity required for the device to regulate the bus voltage, in voltage/reactive power. 
        self.voltage_sensitivity = voltage_sensitivity

        # The nominal voltage at which the nominal reactive power was measured. This should normally be within 10% of the voltage at which the capacitor is connected to the network. 
        self.nom_u = nom_u

        # Positive sequence shunt (charging) conductance per section 
        self.g_per_section = g_per_section

        # The minimum voltage at which the capacitor bank should operate. 
        self.min_u = min_u

        # The date and time when the capacitor bank was last switched on. 
        self.switch_on_date = switch_on_date

        # Zero sequence shunt (charging) conductance per section 
        self.g0_per_section = g0_per_section


        self._sv_shunt_compensator_sections = None
        self.sv_shunt_compensator_sections = sv_shunt_compensator_sections


        super(ShuntCompensator, self).__init__(**kw_args)
    # >>> shunt_compensator

    # <<< sv_shunt_compensator_sections
    # @generated
    def get_sv_shunt_compensator_sections(self):
        """ The state for the number of shunt compensator sections in service.
        """
        return self._sv_shunt_compensator_sections

    def set_sv_shunt_compensator_sections(self, value):
        if self._sv_shunt_compensator_sections is not None:
            self._sv_shunt_compensator_sections._shunt_compensator = None

        self._sv_shunt_compensator_sections = value
        if self._sv_shunt_compensator_sections is not None:
            self._sv_shunt_compensator_sections._shunt_compensator = self

    sv_shunt_compensator_sections = property(get_sv_shunt_compensator_sections, set_sv_shunt_compensator_sections)
    # >>> sv_shunt_compensator_sections


    def __str__(self):
        """ Returns a string representation of the ShuntCompensator.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< shunt_compensator.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ShuntCompensator.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ShuntCompensator", self.uri)
        if format:
            indent += ' ' * depth

        if self.sv_shunt_compensator_sections is not None:
            s += '%s<%s:ShuntCompensator.sv_shunt_compensator_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_shunt_compensator_sections.uri)
        s += '%s<%s:ShuntCompensator.b0_per_section>%s</%s:ShuntCompensator.b0_per_section>' % \
            (indent, ns_prefix, self.b0_per_section, ns_prefix)
        s += '%s<%s:ShuntCompensator.maximum_sections>%s</%s:ShuntCompensator.maximum_sections>' % \
            (indent, ns_prefix, self.maximum_sections, ns_prefix)
        s += '%s<%s:ShuntCompensator.normal_sections>%s</%s:ShuntCompensator.normal_sections>' % \
            (indent, ns_prefix, self.normal_sections, ns_prefix)
        s += '%s<%s:ShuntCompensator.nom_q>%s</%s:ShuntCompensator.nom_q>' % \
            (indent, ns_prefix, self.nom_q, ns_prefix)
        s += '%s<%s:ShuntCompensator.switch_on_count>%s</%s:ShuntCompensator.switch_on_count>' % \
            (indent, ns_prefix, self.switch_on_count, ns_prefix)
        s += '%s<%s:ShuntCompensator.max_u>%s</%s:ShuntCompensator.max_u>' % \
            (indent, ns_prefix, self.max_u, ns_prefix)
        s += '%s<%s:ShuntCompensator.reactive_per_section>%s</%s:ShuntCompensator.reactive_per_section>' % \
            (indent, ns_prefix, self.reactive_per_section, ns_prefix)
        s += '%s<%s:ShuntCompensator.a_vrdelay>%s</%s:ShuntCompensator.a_vrdelay>' % \
            (indent, ns_prefix, self.a_vrdelay, ns_prefix)
        s += '%s<%s:ShuntCompensator.b_per_section>%s</%s:ShuntCompensator.b_per_section>' % \
            (indent, ns_prefix, self.b_per_section, ns_prefix)
        s += '%s<%s:ShuntCompensator.voltage_sensitivity>%s</%s:ShuntCompensator.voltage_sensitivity>' % \
            (indent, ns_prefix, self.voltage_sensitivity, ns_prefix)
        s += '%s<%s:ShuntCompensator.nom_u>%s</%s:ShuntCompensator.nom_u>' % \
            (indent, ns_prefix, self.nom_u, ns_prefix)
        s += '%s<%s:ShuntCompensator.g_per_section>%s</%s:ShuntCompensator.g_per_section>' % \
            (indent, ns_prefix, self.g_per_section, ns_prefix)
        s += '%s<%s:ShuntCompensator.min_u>%s</%s:ShuntCompensator.min_u>' % \
            (indent, ns_prefix, self.min_u, ns_prefix)
        s += '%s<%s:ShuntCompensator.switch_on_date>%s</%s:ShuntCompensator.switch_on_date>' % \
            (indent, ns_prefix, self.switch_on_date, ns_prefix)
        s += '%s<%s:ShuntCompensator.g0_per_section>%s</%s:ShuntCompensator.g0_per_section>' % \
            (indent, ns_prefix, self.g0_per_section, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        if self.regulating_control is not None:
            s += '%s<%s:RegulatingCondEq.regulating_control rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.regulating_control.uri)
        for obj in self.controls:
            s += '%s<%s:RegulatingCondEq.controls rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ShuntCompensator")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> shunt_compensator.serialize


class SynchronousMachine(RegulatingCondEq):
    """ An electromechanical device that operates synchronously with the network. It is a single machine operating either as a generator or synchronous condenser or pump.
    """
    # <<< synchronous_machine
    # @generated
    def __init__(self, type='generator', coolant_type='air', operating_mode='condenser', x2=0.0, x0=0.0, q_percent=0.0, damping=0.0, manual_to_avr=0.0, x=0.0, min_q=0.0, x_quad_sync=0.0, x_quad_subtrans=0.0, r2=0.0, inertia=0.0, r=0.0, x_direct_sync=0.0, x_quad_trans=0.0, x_direct_trans=0.0, reference_priority=0, r0=0.0, min_u=0.0, max_q=0.0, condenser_p=0.0, base_q=0.0, x_direct_subtrans=0.0, rated_s=0.0, max_u=0.0, a_vrto_manual_lead=0.0, a_vrto_manual_lag=0.0, coolant_condition=0.0, reactive_capability_curves=None, hydro_pump=None, prime_movers=None, generating_unit=None, initial_reactive_capability_curve=None, **kw_args):
        """ Initialises a new 'SynchronousMachine' instance.
        """
        # Modes that this synchronous machine can operate in. Values are: "generator", "generator_or_condenser", "condenser"
        self.type = 'generator'

        # Method of cooling the machine. Values are: "air", "hydrogen_gas", "water"
        self.coolant_type = 'air'

        # Current mode of operation. Values are: "condenser", "generator"
        self.operating_mode = 'condenser'

        # Negative sequence reactance. 
        self.x2 = x2

        # Zero sequence reactance of the synchronous machine. 
        self.x0 = x0

        # Percent of the coordinated reactive control that comes from this machine. 
        self.q_percent = q_percent

        # Damping torque coefficient, a proportionality constant that, when multiplied by the angular velocity of the rotor poles with respect to the magnetic field (frequency), results in the damping torque. 
        self.damping = damping

        # Time delay required when switching from Manual to Automatic Voltage Regulation. This value is used in the accelerating power reference frame for powerflow solutions 
        self.manual_to_avr = manual_to_avr

        # Positive sequence reactance of the synchronous machine. 
        self.x = x

        # Minimum reactive power limit for the unit. 
        self.min_q = min_q

        # Quadrature-axis synchronous reactance (Xq) , the ratio of the component of reactive armature voltage, due to the quadrature-axis component of armature current, to this component of current, under steady state conditions and at rated frequency. 
        self.x_quad_sync = x_quad_sync

        # Quadrature-axis subtransient reactance, also known as X'q. 
        self.x_quad_subtrans = x_quad_subtrans

        # Negative sequence resistance. 
        self.r2 = r2

        # The energy stored in the rotor when operating at rated speed. This value is used in the accelerating power reference frame for  operator training simulator solutions. 
        self.inertia = inertia

        # Positive sequence resistance of the synchronous machine. 
        self.r = r

        # Direct-axis synchronous reactance. The quotient of a sustained value of that AC component of armature voltage that is produced by the total direct-axis flux due to direct-axis armature current and the value of the AC component of this current, the machine running at rated speed. (Xd) 
        self.x_direct_sync = x_direct_sync

        # Quadrature-axis transient reactance, also known as X'q. 
        self.x_quad_trans = x_quad_trans

        # Direct-axis transient reactance, also known as X'd. 
        self.x_direct_trans = x_direct_trans

        # Priority of unit for reference bus selection. 0 = don t care (default) 1 = highest priority. 2 is less than 1 and so on. 
        self.reference_priority = reference_priority

        # Zero sequence resistance of the synchronous machine. 
        self.r0 = r0

        # Minimum voltage  limit for the unit. 
        self.min_u = min_u

        # Maximum reactive power limit. This is the maximum (nameplate) limit for the unit. 
        self.max_q = max_q

        # Active power consumed when in condenser mode operation. 
        self.condenser_p = condenser_p

        # Default base reactive power value. This value represents the initial reactive power that can be used by any application function. 
        self.base_q = base_q

        # Direct-axis subtransient reactance, also known as X'd. 
        self.x_direct_subtrans = x_direct_subtrans

        # Nameplate apparent power rating for the unit 
        self.rated_s = rated_s

        # Maximum voltage limit for the unit. 
        self.max_u = max_u

        # Time delay required when switching from Automatic Voltage Regulation (AVR) to Manual for a leading MVAr violation. 
        self.a_vrto_manual_lead = a_vrto_manual_lead

        # Time delay required when switching from Automatic Voltage Regulation (AVR) to Manual for a lagging MVAr violation. 
        self.a_vrto_manual_lag = a_vrto_manual_lag

        # Temperature or pressure of coolant medium 
        self.coolant_condition = coolant_condition


        self._reactive_capability_curves = []
        if reactive_capability_curves is not None:
            self.reactive_capability_curves = reactive_capability_curves
        else:
            self.reactive_capability_curves = []

        self._hydro_pump = None
        self.hydro_pump = hydro_pump

        self._prime_movers = []
        if prime_movers is not None:
            self.prime_movers = prime_movers
        else:
            self.prime_movers = []

        self._generating_unit = None
        self.generating_unit = generating_unit

        self._initial_reactive_capability_curve = None
        self.initial_reactive_capability_curve = initial_reactive_capability_curve


        super(SynchronousMachine, self).__init__(**kw_args)
    # >>> synchronous_machine

    # <<< reactive_capability_curves
    # @generated
    def get_reactive_capability_curves(self):
        """ All available Reactive capability curves for this SynchronousMachine.
        """
        return self._reactive_capability_curves

    def set_reactive_capability_curves(self, value):
        for p in self._reactive_capability_curves:
            filtered = [q for q in p.synchronous_machines if q != self]
            self._reactive_capability_curves._synchronous_machines = filtered
        for r in value:
            if self not in r._synchronous_machines:
                r._synchronous_machines.append(self)
        self._reactive_capability_curves = value

    reactive_capability_curves = property(get_reactive_capability_curves, set_reactive_capability_curves)

    def add_reactive_capability_curves(self, *reactive_capability_curves):
        for obj in reactive_capability_curves:
            if self not in obj._synchronous_machines:
                obj._synchronous_machines.append(self)
            self._reactive_capability_curves.append(obj)

    def remove_reactive_capability_curves(self, *reactive_capability_curves):
        for obj in reactive_capability_curves:
            if self in obj._synchronous_machines:
                obj._synchronous_machines.remove(self)
            self._reactive_capability_curves.remove(obj)
    # >>> reactive_capability_curves

    # <<< hydro_pump
    # @generated
    def get_hydro_pump(self):
        """ The synchronous machine drives the turbine which moves the water from a low elevation to a higher elevation. The direction of machine rotation for pumping may or may not be the same as for generating.
        """
        return self._hydro_pump

    def set_hydro_pump(self, value):
        if self._hydro_pump is not None:
            self._hydro_pump._synchronous_machine = None

        self._hydro_pump = value
        if self._hydro_pump is not None:
            self._hydro_pump._synchronous_machine = self

    hydro_pump = property(get_hydro_pump, set_hydro_pump)
    # >>> hydro_pump

    # <<< prime_movers
    # @generated
    def get_prime_movers(self):
        """ Prime movers that drive this SynchronousMachine.
        """
        return self._prime_movers

    def set_prime_movers(self, value):
        for p in self._prime_movers:
            filtered = [q for q in p.synchronous_machines if q != self]
            self._prime_movers._synchronous_machines = filtered
        for r in value:
            if self not in r._synchronous_machines:
                r._synchronous_machines.append(self)
        self._prime_movers = value

    prime_movers = property(get_prime_movers, set_prime_movers)

    def add_prime_movers(self, *prime_movers):
        for obj in prime_movers:
            if self not in obj._synchronous_machines:
                obj._synchronous_machines.append(self)
            self._prime_movers.append(obj)

    def remove_prime_movers(self, *prime_movers):
        for obj in prime_movers:
            if self in obj._synchronous_machines:
                obj._synchronous_machines.remove(self)
            self._prime_movers.remove(obj)
    # >>> prime_movers

    # <<< generating_unit
    # @generated
    def get_generating_unit(self):
        """ A synchronous machine may operate as a generator and as such becomes a member of a generating unit
        """
        return self._generating_unit

    def set_generating_unit(self, value):
        if self._generating_unit is not None:
            filtered = [x for x in self.generating_unit.synchronous_machines if x != self]
            self._generating_unit._synchronous_machines = filtered

        self._generating_unit = value
        if self._generating_unit is not None:
            self._generating_unit._synchronous_machines.append(self)

    generating_unit = property(get_generating_unit, set_generating_unit)
    # >>> generating_unit

    # <<< initial_reactive_capability_curve
    # @generated
    def get_initial_reactive_capability_curve(self):
        """ The default ReactiveCapabilityCurve for use by a SynchronousMachine
        """
        return self._initial_reactive_capability_curve

    def set_initial_reactive_capability_curve(self, value):
        if self._initial_reactive_capability_curve is not None:
            filtered = [x for x in self.initial_reactive_capability_curve.initially_used_by_synchronous_machines if x != self]
            self._initial_reactive_capability_curve._initially_used_by_synchronous_machines = filtered

        self._initial_reactive_capability_curve = value
        if self._initial_reactive_capability_curve is not None:
            self._initial_reactive_capability_curve._initially_used_by_synchronous_machines.append(self)

    initial_reactive_capability_curve = property(get_initial_reactive_capability_curve, set_initial_reactive_capability_curve)
    # >>> initial_reactive_capability_curve


    def __str__(self):
        """ Returns a string representation of the SynchronousMachine.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< synchronous_machine.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the SynchronousMachine.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "SynchronousMachine", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.reactive_capability_curves:
            s += '%s<%s:SynchronousMachine.reactive_capability_curves rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.hydro_pump is not None:
            s += '%s<%s:SynchronousMachine.hydro_pump rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.hydro_pump.uri)
        for obj in self.prime_movers:
            s += '%s<%s:SynchronousMachine.prime_movers rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.generating_unit is not None:
            s += '%s<%s:SynchronousMachine.generating_unit rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.generating_unit.uri)
        if self.initial_reactive_capability_curve is not None:
            s += '%s<%s:SynchronousMachine.initial_reactive_capability_curve rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.initial_reactive_capability_curve.uri)
        s += '%s<%s:SynchronousMachine.type>%s</%s:SynchronousMachine.type>' % \
            (indent, ns_prefix, self.type, ns_prefix)
        s += '%s<%s:SynchronousMachine.coolant_type>%s</%s:SynchronousMachine.coolant_type>' % \
            (indent, ns_prefix, self.coolant_type, ns_prefix)
        s += '%s<%s:SynchronousMachine.operating_mode>%s</%s:SynchronousMachine.operating_mode>' % \
            (indent, ns_prefix, self.operating_mode, ns_prefix)
        s += '%s<%s:SynchronousMachine.x2>%s</%s:SynchronousMachine.x2>' % \
            (indent, ns_prefix, self.x2, ns_prefix)
        s += '%s<%s:SynchronousMachine.x0>%s</%s:SynchronousMachine.x0>' % \
            (indent, ns_prefix, self.x0, ns_prefix)
        s += '%s<%s:SynchronousMachine.q_percent>%s</%s:SynchronousMachine.q_percent>' % \
            (indent, ns_prefix, self.q_percent, ns_prefix)
        s += '%s<%s:SynchronousMachine.damping>%s</%s:SynchronousMachine.damping>' % \
            (indent, ns_prefix, self.damping, ns_prefix)
        s += '%s<%s:SynchronousMachine.manual_to_avr>%s</%s:SynchronousMachine.manual_to_avr>' % \
            (indent, ns_prefix, self.manual_to_avr, ns_prefix)
        s += '%s<%s:SynchronousMachine.x>%s</%s:SynchronousMachine.x>' % \
            (indent, ns_prefix, self.x, ns_prefix)
        s += '%s<%s:SynchronousMachine.min_q>%s</%s:SynchronousMachine.min_q>' % \
            (indent, ns_prefix, self.min_q, ns_prefix)
        s += '%s<%s:SynchronousMachine.x_quad_sync>%s</%s:SynchronousMachine.x_quad_sync>' % \
            (indent, ns_prefix, self.x_quad_sync, ns_prefix)
        s += '%s<%s:SynchronousMachine.x_quad_subtrans>%s</%s:SynchronousMachine.x_quad_subtrans>' % \
            (indent, ns_prefix, self.x_quad_subtrans, ns_prefix)
        s += '%s<%s:SynchronousMachine.r2>%s</%s:SynchronousMachine.r2>' % \
            (indent, ns_prefix, self.r2, ns_prefix)
        s += '%s<%s:SynchronousMachine.inertia>%s</%s:SynchronousMachine.inertia>' % \
            (indent, ns_prefix, self.inertia, ns_prefix)
        s += '%s<%s:SynchronousMachine.r>%s</%s:SynchronousMachine.r>' % \
            (indent, ns_prefix, self.r, ns_prefix)
        s += '%s<%s:SynchronousMachine.x_direct_sync>%s</%s:SynchronousMachine.x_direct_sync>' % \
            (indent, ns_prefix, self.x_direct_sync, ns_prefix)
        s += '%s<%s:SynchronousMachine.x_quad_trans>%s</%s:SynchronousMachine.x_quad_trans>' % \
            (indent, ns_prefix, self.x_quad_trans, ns_prefix)
        s += '%s<%s:SynchronousMachine.x_direct_trans>%s</%s:SynchronousMachine.x_direct_trans>' % \
            (indent, ns_prefix, self.x_direct_trans, ns_prefix)
        s += '%s<%s:SynchronousMachine.reference_priority>%s</%s:SynchronousMachine.reference_priority>' % \
            (indent, ns_prefix, self.reference_priority, ns_prefix)
        s += '%s<%s:SynchronousMachine.r0>%s</%s:SynchronousMachine.r0>' % \
            (indent, ns_prefix, self.r0, ns_prefix)
        s += '%s<%s:SynchronousMachine.min_u>%s</%s:SynchronousMachine.min_u>' % \
            (indent, ns_prefix, self.min_u, ns_prefix)
        s += '%s<%s:SynchronousMachine.max_q>%s</%s:SynchronousMachine.max_q>' % \
            (indent, ns_prefix, self.max_q, ns_prefix)
        s += '%s<%s:SynchronousMachine.condenser_p>%s</%s:SynchronousMachine.condenser_p>' % \
            (indent, ns_prefix, self.condenser_p, ns_prefix)
        s += '%s<%s:SynchronousMachine.base_q>%s</%s:SynchronousMachine.base_q>' % \
            (indent, ns_prefix, self.base_q, ns_prefix)
        s += '%s<%s:SynchronousMachine.x_direct_subtrans>%s</%s:SynchronousMachine.x_direct_subtrans>' % \
            (indent, ns_prefix, self.x_direct_subtrans, ns_prefix)
        s += '%s<%s:SynchronousMachine.rated_s>%s</%s:SynchronousMachine.rated_s>' % \
            (indent, ns_prefix, self.rated_s, ns_prefix)
        s += '%s<%s:SynchronousMachine.max_u>%s</%s:SynchronousMachine.max_u>' % \
            (indent, ns_prefix, self.max_u, ns_prefix)
        s += '%s<%s:SynchronousMachine.a_vrto_manual_lead>%s</%s:SynchronousMachine.a_vrto_manual_lead>' % \
            (indent, ns_prefix, self.a_vrto_manual_lead, ns_prefix)
        s += '%s<%s:SynchronousMachine.a_vrto_manual_lag>%s</%s:SynchronousMachine.a_vrto_manual_lag>' % \
            (indent, ns_prefix, self.a_vrto_manual_lag, ns_prefix)
        s += '%s<%s:SynchronousMachine.coolant_condition>%s</%s:SynchronousMachine.coolant_condition>' % \
            (indent, ns_prefix, self.coolant_condition, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        if self.regulating_control is not None:
            s += '%s<%s:RegulatingCondEq.regulating_control rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.regulating_control.uri)
        for obj in self.controls:
            s += '%s<%s:RegulatingCondEq.controls rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "SynchronousMachine")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> synchronous_machine.serialize


class FrequencyConverter(RegulatingCondEq):
    """ A device to convert from one frequency to another (e.g., frequency F1 to F2) comprises a pair of FrequencyConverter instances. One converts from F1 to DC, the other converts the DC to F2.
    """
    # <<< frequency_converter
    # @generated
    def __init__(self, max_u=0.0, min_u=0.0, min_p=0.0, frequency=0.0, max_p=0.0, operating_mode='', **kw_args):
        """ Initialises a new 'FrequencyConverter' instance.
        """
        # The maximum voltage on the DC side at which the frequency converter should operate. 
        self.max_u = max_u

        # The minimum voltage on the DC side at which the frequency converter should operate. 
        self.min_u = min_u

        # The minimum active power on the DC side at which the frequence converter should operate. 
        self.min_p = min_p

        # Frequency on the AC side. 
        self.frequency = frequency

        # The maximum active power on the DC side at which the frequence converter should operate. 
        self.max_p = max_p

        # Operating mode for the frequency converter 
        self.operating_mode = operating_mode



        super(FrequencyConverter, self).__init__(**kw_args)
    # >>> frequency_converter


    def __str__(self):
        """ Returns a string representation of the FrequencyConverter.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< frequency_converter.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the FrequencyConverter.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "FrequencyConverter", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:FrequencyConverter.max_u>%s</%s:FrequencyConverter.max_u>' % \
            (indent, ns_prefix, self.max_u, ns_prefix)
        s += '%s<%s:FrequencyConverter.min_u>%s</%s:FrequencyConverter.min_u>' % \
            (indent, ns_prefix, self.min_u, ns_prefix)
        s += '%s<%s:FrequencyConverter.min_p>%s</%s:FrequencyConverter.min_p>' % \
            (indent, ns_prefix, self.min_p, ns_prefix)
        s += '%s<%s:FrequencyConverter.frequency>%s</%s:FrequencyConverter.frequency>' % \
            (indent, ns_prefix, self.frequency, ns_prefix)
        s += '%s<%s:FrequencyConverter.max_p>%s</%s:FrequencyConverter.max_p>' % \
            (indent, ns_prefix, self.max_p, ns_prefix)
        s += '%s<%s:FrequencyConverter.operating_mode>%s</%s:FrequencyConverter.operating_mode>' % \
            (indent, ns_prefix, self.operating_mode, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        if self.regulating_control is not None:
            s += '%s<%s:RegulatingCondEq.regulating_control rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.regulating_control.uri)
        for obj in self.controls:
            s += '%s<%s:RegulatingCondEq.controls rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "FrequencyConverter")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> frequency_converter.serialize


class Junction(Connector):
    """ A point where one or more conducting equipments are connected with zero resistance.
    """
    pass
    # <<< junction
    # @generated
    def __init__(self, **kw_args):
        """ Initialises a new 'Junction' instance.
        """


        super(Junction, self).__init__(**kw_args)
    # >>> junction


    def __str__(self):
        """ Returns a string representation of the Junction.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< junction.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Junction.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Junction", self.uri)
        if format:
            indent += ' ' * depth

        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Junction")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> junction.serialize


class DCLineSegment(Conductor):
    """ A wire or combination of wires not insulated from one another, with consistent electrical characteristics, used to carry direct current between points in the DC region of the power system.
    """
    # <<< dcline_segment
    # @generated
    def __init__(self, dc_segment_inductance=0.0, dc_segment_resistance=0.0, **kw_args):
        """ Initialises a new 'DCLineSegment' instance.
        """
        # Inductance of the DC line segment. 
        self.dc_segment_inductance = dc_segment_inductance

        # Resistance of the DC line segment. 
        self.dc_segment_resistance = dc_segment_resistance



        super(DCLineSegment, self).__init__(**kw_args)
    # >>> dcline_segment


    def __str__(self):
        """ Returns a string representation of the DCLineSegment.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< dcline_segment.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the DCLineSegment.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "DCLineSegment", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:DCLineSegment.dc_segment_inductance>%s</%s:DCLineSegment.dc_segment_inductance>' % \
            (indent, ns_prefix, self.dc_segment_inductance, ns_prefix)
        s += '%s<%s:DCLineSegment.dc_segment_resistance>%s</%s:DCLineSegment.dc_segment_resistance>' % \
            (indent, ns_prefix, self.dc_segment_resistance, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        s += '%s<%s:Conductor.length>%s</%s:Conductor.length>' % \
            (indent, ns_prefix, self.length, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "DCLineSegment")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> dcline_segment.serialize


class RatioTapChanger(TapChanger):
    """ A tap changer that changes the voltage ratio impacting the voltage magnitude but not direclty the phase angle across the transformer..
    """
    # <<< ratio_tap_changer
    # @generated
    def __init__(self, tcul_control_mode='volt', winding=None, ratio_variation_curve=None, transformer_winding=None, **kw_args):
        """ Initialises a new 'RatioTapChanger' instance.
        """
        # Specifies the regulation control mode (voltage or reactive) of the RatioTapChanger. Values are: "volt", "reactive"
        self.tcul_control_mode = 'volt'


        self._winding = None
        self.winding = winding

        self._ratio_variation_curve = None
        self.ratio_variation_curve = ratio_variation_curve

        self._transformer_winding = None
        self.transformer_winding = transformer_winding


        super(RatioTapChanger, self).__init__(**kw_args)
    # >>> ratio_tap_changer

    # <<< winding
    # @generated
    def get_winding(self):
        """ Winding to which this ratio tap changer belongs.
        """
        return self._winding

    def set_winding(self, value):
        if self._winding is not None:
            self._winding._ratio_tap_changer = None

        self._winding = value
        if self._winding is not None:
            self._winding._ratio_tap_changer = self

    winding = property(get_winding, set_winding)
    # >>> winding

    # <<< ratio_variation_curve
    # @generated
    def get_ratio_variation_curve(self):
        """ A RatioTapChanger can have an associated RatioVariationCurve to define tap ratio variations with tap step changes.
        """
        return self._ratio_variation_curve

    def set_ratio_variation_curve(self, value):
        if self._ratio_variation_curve is not None:
            self._ratio_variation_curve._ratio_tap_changer = None

        self._ratio_variation_curve = value
        if self._ratio_variation_curve is not None:
            self._ratio_variation_curve._ratio_tap_changer = self

    ratio_variation_curve = property(get_ratio_variation_curve, set_ratio_variation_curve)
    # >>> ratio_variation_curve

    # <<< transformer_winding
    # @generated
    def get_transformer_winding(self):
        """ The transformer winding to which the ratio tap changer belongs.
        """
        return self._transformer_winding

    def set_transformer_winding(self, value):
        if self._transformer_winding is not None:
            self._transformer_winding._ratio_tap_changer = None

        self._transformer_winding = value
        if self._transformer_winding is not None:
            self._transformer_winding._ratio_tap_changer = self

    transformer_winding = property(get_transformer_winding, set_transformer_winding)
    # >>> transformer_winding


    def __str__(self):
        """ Returns a string representation of the RatioTapChanger.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< ratio_tap_changer.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the RatioTapChanger.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "RatioTapChanger", self.uri)
        if format:
            indent += ' ' * depth

        if self.winding is not None:
            s += '%s<%s:RatioTapChanger.winding rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.winding.uri)
        if self.ratio_variation_curve is not None:
            s += '%s<%s:RatioTapChanger.ratio_variation_curve rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.ratio_variation_curve.uri)
        if self.transformer_winding is not None:
            s += '%s<%s:RatioTapChanger.transformer_winding rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.transformer_winding.uri)
        s += '%s<%s:RatioTapChanger.tcul_control_mode>%s</%s:RatioTapChanger.tcul_control_mode>' % \
            (indent, ns_prefix, self.tcul_control_mode, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.regulating_control is not None:
            s += '%s<%s:TapChanger.regulating_control rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.regulating_control.uri)
        if self.impedance_variation_curve is not None:
            s += '%s<%s:TapChanger.impedance_variation_curve rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.impedance_variation_curve.uri)
        if self.sv_tap_step is not None:
            s += '%s<%s:TapChanger.sv_tap_step rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_tap_step.uri)
        for obj in self.tap_schedules:
            s += '%s<%s:TapChanger.tap_schedules rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TapChanger.neutral_step>%s</%s:TapChanger.neutral_step>' % \
            (indent, ns_prefix, self.neutral_step, ns_prefix)
        s += '%s<%s:TapChanger.subsequent_delay>%s</%s:TapChanger.subsequent_delay>' % \
            (indent, ns_prefix, self.subsequent_delay, ns_prefix)
        s += '%s<%s:TapChanger.neutral_u>%s</%s:TapChanger.neutral_u>' % \
            (indent, ns_prefix, self.neutral_u, ns_prefix)
        s += '%s<%s:TapChanger.step_voltage_increment>%s</%s:TapChanger.step_voltage_increment>' % \
            (indent, ns_prefix, self.step_voltage_increment, ns_prefix)
        s += '%s<%s:TapChanger.low_step>%s</%s:TapChanger.low_step>' % \
            (indent, ns_prefix, self.low_step, ns_prefix)
        s += '%s<%s:TapChanger.normal_step>%s</%s:TapChanger.normal_step>' % \
            (indent, ns_prefix, self.normal_step, ns_prefix)
        s += '%s<%s:TapChanger.regulation_status>%s</%s:TapChanger.regulation_status>' % \
            (indent, ns_prefix, self.regulation_status, ns_prefix)
        s += '%s<%s:TapChanger.high_step>%s</%s:TapChanger.high_step>' % \
            (indent, ns_prefix, self.high_step, ns_prefix)
        s += '%s<%s:TapChanger.initial_delay>%s</%s:TapChanger.initial_delay>' % \
            (indent, ns_prefix, self.initial_delay, ns_prefix)
        s += '%s<%s:TapChanger.ltc_flag>%s</%s:TapChanger.ltc_flag>' % \
            (indent, ns_prefix, self.ltc_flag, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "RatioTapChanger")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> ratio_tap_changer.serialize


class StaticVarCompensator(RegulatingCondEq):
    """ A facility for providing variable and controllable shunt reactive power. The SVC typically consists of a stepdown transformer, filter, thyristor-controlled reactor, and thyristor-switched capacitor arms.  The SVC may operate in fixed MVar output mode or in voltage control mode.  When in voltage control mode, the output of the SVC will be proportional to the deviation of voltage at the controlled bus from the voltage setpoint.  The SVC characteristic slope defines the proportion.  If the voltage at the controlled bus is equal to the voltage setpoint, the SVC MVar output is zero.
    """
    # <<< static_var_compensator
    # @generated
    def __init__(self, s_vccontrol_mode='off', capacitive_rating=0.0, slope=0.0, voltage_set_point=0.0, inductive_rating=0.0, **kw_args):
        """ Initialises a new 'StaticVarCompensator' instance.
        """
        # SVC control mode. Values are: "off", "reactive_power", "voltage"
        self.s_vccontrol_mode = 'off'

        # Maximum available capacitive reactive power 
        self.capacitive_rating = capacitive_rating

        # The characteristics slope of an SVC defines how the reactive power output changes in proportion to the difference between the regulated bus voltage and the voltage setpoint. 
        self.slope = slope

        # The reactive power output of the SVC is proportional to the difference between the voltage at the regulated bus and the voltage setpoint.  When the regulated bus voltage is equal to the voltage setpoint, the reactive power output is zero. 
        self.voltage_set_point = voltage_set_point

        # Maximum available inductive reactive power 
        self.inductive_rating = inductive_rating



        super(StaticVarCompensator, self).__init__(**kw_args)
    # >>> static_var_compensator


    def __str__(self):
        """ Returns a string representation of the StaticVarCompensator.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< static_var_compensator.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the StaticVarCompensator.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "StaticVarCompensator", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:StaticVarCompensator.s_vccontrol_mode>%s</%s:StaticVarCompensator.s_vccontrol_mode>' % \
            (indent, ns_prefix, self.s_vccontrol_mode, ns_prefix)
        s += '%s<%s:StaticVarCompensator.capacitive_rating>%s</%s:StaticVarCompensator.capacitive_rating>' % \
            (indent, ns_prefix, self.capacitive_rating, ns_prefix)
        s += '%s<%s:StaticVarCompensator.slope>%s</%s:StaticVarCompensator.slope>' % \
            (indent, ns_prefix, self.slope, ns_prefix)
        s += '%s<%s:StaticVarCompensator.voltage_set_point>%s</%s:StaticVarCompensator.voltage_set_point>' % \
            (indent, ns_prefix, self.voltage_set_point, ns_prefix)
        s += '%s<%s:StaticVarCompensator.inductive_rating>%s</%s:StaticVarCompensator.inductive_rating>' % \
            (indent, ns_prefix, self.inductive_rating, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        if self.regulating_control is not None:
            s += '%s<%s:RegulatingCondEq.regulating_control rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.regulating_control.uri)
        for obj in self.controls:
            s += '%s<%s:RegulatingCondEq.controls rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "StaticVarCompensator")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> static_var_compensator.serialize


class LoadBreakSwitch(ProtectedSwitch):
    """ A mechanical switching device capable of making, carrying, and breaking currents under normal operating conditions.
    """
    # <<< load_break_switch
    # @generated
    def __init__(self, rated_current=0.0, **kw_args):
        """ Initialises a new 'LoadBreakSwitch' instance.
        """
        # Current carrying capacity of a wire or cable under stated thermal conditions. 
        self.rated_current = rated_current



        super(LoadBreakSwitch, self).__init__(**kw_args)
    # >>> load_break_switch


    def __str__(self):
        """ Returns a string representation of the LoadBreakSwitch.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< load_break_switch.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the LoadBreakSwitch.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "LoadBreakSwitch", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:LoadBreakSwitch.rated_current>%s</%s:LoadBreakSwitch.rated_current>' % \
            (indent, ns_prefix, self.rated_current, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        for obj in self.load_mgmt_functions:
            s += '%s<%s:Switch.load_mgmt_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.composite_switch is not None:
            s += '%s<%s:Switch.composite_switch rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.composite_switch.uri)
        for obj in self.switch_schedules:
            s += '%s<%s:Switch.switch_schedules rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.connect_disconnect_functions:
            s += '%s<%s:Switch.connect_disconnect_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.switching_operations:
            s += '%s<%s:Switch.switching_operations rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Switch.switch_on_count>%s</%s:Switch.switch_on_count>' % \
            (indent, ns_prefix, self.switch_on_count, ns_prefix)
        s += '%s<%s:Switch.normal_open>%s</%s:Switch.normal_open>' % \
            (indent, ns_prefix, self.normal_open, ns_prefix)
        s += '%s<%s:Switch.retained>%s</%s:Switch.retained>' % \
            (indent, ns_prefix, self.retained, ns_prefix)
        s += '%s<%s:Switch.switch_on_date>%s</%s:Switch.switch_on_date>' % \
            (indent, ns_prefix, self.switch_on_date, ns_prefix)
        for obj in self.reclose_sequences:
            s += '%s<%s:ProtectedSwitch.reclose_sequences rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "LoadBreakSwitch")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> load_break_switch.serialize


class GroundDisconnector(Switch):
    """ A manually operated or motor operated mechanical switching device used for isolating a circuit or equipment from Ground.
    """
    pass
    # <<< ground_disconnector
    # @generated
    def __init__(self, **kw_args):
        """ Initialises a new 'GroundDisconnector' instance.
        """


        super(GroundDisconnector, self).__init__(**kw_args)
    # >>> ground_disconnector


    def __str__(self):
        """ Returns a string representation of the GroundDisconnector.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< ground_disconnector.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the GroundDisconnector.
        """
        s = ''
        indent = ' ' * depth if depth else ''
        if format:
            indent = '\n' + indent
        if header:
            s += '<?xml version="1.0" encoding="UTF-8"?>\n'
            s += '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:%s="%s">' % \
                (ns_prefix, ns_uri)
            if format:
                indent += ' ' * depth

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "GroundDisconnector", self.uri)
        if format:
            indent += ' ' * depth

        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)
        if self.modeling_authority_set is not None:
            s += '%s<%s:IdentifiedObject.modeling_authority_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.modeling_authority_set.uri)
        s += '%s<%s:IdentifiedObject.description>%s</%s:IdentifiedObject.description>' % \
            (indent, ns_prefix, self.description, ns_prefix)
        s += '%s<%s:IdentifiedObject.m_rid>%s</%s:IdentifiedObject.m_rid>' % \
            (indent, ns_prefix, self.m_rid, ns_prefix)
        s += '%s<%s:IdentifiedObject.name>%s</%s:IdentifiedObject.name>' % \
            (indent, ns_prefix, self.name, ns_prefix)
        s += '%s<%s:IdentifiedObject.path_name>%s</%s:IdentifiedObject.path_name>' % \
            (indent, ns_prefix, self.path_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.local_name>%s</%s:IdentifiedObject.local_name>' % \
            (indent, ns_prefix, self.local_name, ns_prefix)
        s += '%s<%s:IdentifiedObject.alias_name>%s</%s:IdentifiedObject.alias_name>' % \
            (indent, ns_prefix, self.alias_name, ns_prefix)
        for obj in self.change_items:
            s += '%s<%s:PowerSystemResource.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.asset_roles:
            s += '%s<%s:PowerSystemResource.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.geo_location is not None:
            s += '%s<%s:PowerSystemResource.geo_location rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.geo_location.uri)
        for obj in self.safety_documents:
            s += '%s<%s:PowerSystemResource.safety_documents rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.outage_schedule is not None:
            s += '%s<%s:PowerSystemResource.outage_schedule rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.outage_schedule.uri)
        for obj in self.measurements:
            s += '%s<%s:PowerSystemResource.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:PowerSystemResource.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.psrtype is not None:
            s += '%s<%s:PowerSystemResource.psrtype rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.psrtype.uri)
        for obj in self.psr_lists:
            s += '%s<%s:PowerSystemResource.psr_lists rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.psrevent:
            s += '%s<%s:PowerSystemResource.psrevent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operating_share:
            s += '%s<%s:PowerSystemResource.operating_share rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.schedule_steps:
            s += '%s<%s:PowerSystemResource.schedule_steps rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.document_roles:
            s += '%s<%s:PowerSystemResource.document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.reporting_group:
            s += '%s<%s:PowerSystemResource.reporting_group rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.circuit_sections:
            s += '%s<%s:PowerSystemResource.circuit_sections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:PowerSystemResource.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.contingency_equipment:
            s += '%s<%s:Equipment.contingency_equipment rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:Equipment.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.operational_limit_set:
            s += '%s<%s:Equipment.operational_limit_set rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.equipment_container is not None:
            s += '%s<%s:Equipment.equipment_container rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.equipment_container.uri)
        s += '%s<%s:Equipment.norma_ily_in_service>%s</%s:Equipment.norma_ily_in_service>' % \
            (indent, ns_prefix, self.norma_ily_in_service, ns_prefix)
        for obj in self.terminals:
            s += '%s<%s:ConductingEquipment.terminals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.clearance_tags:
            s += '%s<%s:ConductingEquipment.clearance_tags rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.outage_step_roles:
            s += '%s<%s:ConductingEquipment.outage_step_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.base_voltage is not None:
            s += '%s<%s:ConductingEquipment.base_voltage rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.base_voltage.uri)
        for obj in self.electrical_assets:
            s += '%s<%s:ConductingEquipment.electrical_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.sv_status is not None:
            s += '%s<%s:ConductingEquipment.sv_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.sv_status.uri)
        for obj in self.protection_equipments:
            s += '%s<%s:ConductingEquipment.protection_equipments rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConductingEquipment.phases>%s</%s:ConductingEquipment.phases>' % \
            (indent, ns_prefix, self.phases, ns_prefix)
        for obj in self.load_mgmt_functions:
            s += '%s<%s:Switch.load_mgmt_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.composite_switch is not None:
            s += '%s<%s:Switch.composite_switch rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.composite_switch.uri)
        for obj in self.switch_schedules:
            s += '%s<%s:Switch.switch_schedules rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.connect_disconnect_functions:
            s += '%s<%s:Switch.connect_disconnect_functions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.switching_operations:
            s += '%s<%s:Switch.switching_operations rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Switch.switch_on_count>%s</%s:Switch.switch_on_count>' % \
            (indent, ns_prefix, self.switch_on_count, ns_prefix)
        s += '%s<%s:Switch.normal_open>%s</%s:Switch.normal_open>' % \
            (indent, ns_prefix, self.normal_open, ns_prefix)
        s += '%s<%s:Switch.retained>%s</%s:Switch.retained>' % \
            (indent, ns_prefix, self.retained, ns_prefix)
        s += '%s<%s:Switch.switch_on_date>%s</%s:Switch.switch_on_date>' % \
            (indent, ns_prefix, self.switch_on_date, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "GroundDisconnector")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> ground_disconnector.serialize


# <<< wires
# @generated
# >>> wires
