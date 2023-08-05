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


from cim.iec61968.common import Document
from cim.iec61970.core import IdentifiedObject

# <<< imports
# @generated
# >>> imports

ns_prefix = "cim.inftypeasset"

ns_uri = "http://iec.ch/TC57/2009/CIM-schema-cim14#InfTypeAsset"

class TypeAsset(Document):
    """ Whereas an AssetModel is a particular model and version of a vendor's product, a TypeAsset is documentation for a generic asset or material item that may be used for design purposes. Any number of AssetModels may be used to perform this generic function. The primary role of the TypeAsset is typically defined by the PowereSystemResource it is associated with.
    """
    # <<< type_asset
    # @generated
    def __init__(self, quantity='', stock_item=False, estimated_unit_cost=0.0, cuwork_equipment_asset=None, cuasset=None, type_asset_catalogue=None, asset_models=None, erp_inventory_issues=None, erp_req_line_items=None, erp_bom_item_datas=None, **kw_args):
        """ Initialises a new 'TypeAsset' instance.
        """
        # The value, unit of measure, and multiplier for the quantity. 
        self.quantity = quantity

        # True if item is a stock item (default). 
        self.stock_item = stock_item

        # Estimated unit cost (or cost per unit length) of this type of asset. It does not include labor to install/construct or configure it. 
        self.estimated_unit_cost = estimated_unit_cost


        self._cuwork_equipment_asset = None
        self.cuwork_equipment_asset = cuwork_equipment_asset

        self._cuasset = None
        self.cuasset = cuasset

        self._type_asset_catalogue = None
        self.type_asset_catalogue = type_asset_catalogue

        self._asset_models = []
        if asset_models is not None:
            self.asset_models = asset_models
        else:
            self.asset_models = []

        self._erp_inventory_issues = []
        if erp_inventory_issues is not None:
            self.erp_inventory_issues = erp_inventory_issues
        else:
            self.erp_inventory_issues = []

        self._erp_req_line_items = []
        if erp_req_line_items is not None:
            self.erp_req_line_items = erp_req_line_items
        else:
            self.erp_req_line_items = []

        self._erp_bom_item_datas = []
        if erp_bom_item_datas is not None:
            self.erp_bom_item_datas = erp_bom_item_datas
        else:
            self.erp_bom_item_datas = []


        super(TypeAsset, self).__init__(**kw_args)
    # >>> type_asset

    # <<< cuwork_equipment_asset
    # @generated
    def get_cuwork_equipment_asset(self):
        """ 
        """
        return self._cuwork_equipment_asset

    def set_cuwork_equipment_asset(self, value):
        if self._cuwork_equipment_asset is not None:
            self._cuwork_equipment_asset._type_asset = None

        self._cuwork_equipment_asset = value
        if self._cuwork_equipment_asset is not None:
            self._cuwork_equipment_asset._type_asset = self

    cuwork_equipment_asset = property(get_cuwork_equipment_asset, set_cuwork_equipment_asset)
    # >>> cuwork_equipment_asset

    # <<< cuasset
    # @generated
    def get_cuasset(self):
        """ 
        """
        return self._cuasset

    def set_cuasset(self, value):
        if self._cuasset is not None:
            self._cuasset._type_asset = None

        self._cuasset = value
        if self._cuasset is not None:
            self._cuasset._type_asset = self

    cuasset = property(get_cuasset, set_cuasset)
    # >>> cuasset

    # <<< type_asset_catalogue
    # @generated
    def get_type_asset_catalogue(self):
        """ 
        """
        return self._type_asset_catalogue

    def set_type_asset_catalogue(self, value):
        if self._type_asset_catalogue is not None:
            filtered = [x for x in self.type_asset_catalogue.type_assets if x != self]
            self._type_asset_catalogue._type_assets = filtered

        self._type_asset_catalogue = value
        if self._type_asset_catalogue is not None:
            self._type_asset_catalogue._type_assets.append(self)

    type_asset_catalogue = property(get_type_asset_catalogue, set_type_asset_catalogue)
    # >>> type_asset_catalogue

    # <<< asset_models
    # @generated
    def get_asset_models(self):
        """ A type of asset may be satisified with many different types of asset models.
        """
        return self._asset_models

    def set_asset_models(self, value):
        for x in self._asset_models:
            x._type_asset = None
        for y in value:
            y._type_asset = self
        self._asset_models = value

    asset_models = property(get_asset_models, set_asset_models)

    def add_asset_models(self, *asset_models):
        for obj in asset_models:
            obj._type_asset = self
            self._asset_models.append(obj)

    def remove_asset_models(self, *asset_models):
        for obj in asset_models:
            obj._type_asset = None
            self._asset_models.remove(obj)
    # >>> asset_models

    # <<< erp_inventory_issues
    # @generated
    def get_erp_inventory_issues(self):
        """ 
        """
        return self._erp_inventory_issues

    def set_erp_inventory_issues(self, value):
        for x in self._erp_inventory_issues:
            x._type_asset = None
        for y in value:
            y._type_asset = self
        self._erp_inventory_issues = value

    erp_inventory_issues = property(get_erp_inventory_issues, set_erp_inventory_issues)

    def add_erp_inventory_issues(self, *erp_inventory_issues):
        for obj in erp_inventory_issues:
            obj._type_asset = self
            self._erp_inventory_issues.append(obj)

    def remove_erp_inventory_issues(self, *erp_inventory_issues):
        for obj in erp_inventory_issues:
            obj._type_asset = None
            self._erp_inventory_issues.remove(obj)
    # >>> erp_inventory_issues

    # <<< erp_req_line_items
    # @generated
    def get_erp_req_line_items(self):
        """ 
        """
        return self._erp_req_line_items

    def set_erp_req_line_items(self, value):
        for x in self._erp_req_line_items:
            x._type_asset = None
        for y in value:
            y._type_asset = self
        self._erp_req_line_items = value

    erp_req_line_items = property(get_erp_req_line_items, set_erp_req_line_items)

    def add_erp_req_line_items(self, *erp_req_line_items):
        for obj in erp_req_line_items:
            obj._type_asset = self
            self._erp_req_line_items.append(obj)

    def remove_erp_req_line_items(self, *erp_req_line_items):
        for obj in erp_req_line_items:
            obj._type_asset = None
            self._erp_req_line_items.remove(obj)
    # >>> erp_req_line_items

    # <<< erp_bom_item_datas
    # @generated
    def get_erp_bom_item_datas(self):
        """ 
        """
        return self._erp_bom_item_datas

    def set_erp_bom_item_datas(self, value):
        for x in self._erp_bom_item_datas:
            x._type_asset = None
        for y in value:
            y._type_asset = self
        self._erp_bom_item_datas = value

    erp_bom_item_datas = property(get_erp_bom_item_datas, set_erp_bom_item_datas)

    def add_erp_bom_item_datas(self, *erp_bom_item_datas):
        for obj in erp_bom_item_datas:
            obj._type_asset = self
            self._erp_bom_item_datas.append(obj)

    def remove_erp_bom_item_datas(self, *erp_bom_item_datas):
        for obj in erp_bom_item_datas:
            obj._type_asset = None
            self._erp_bom_item_datas.remove(obj)
    # >>> erp_bom_item_datas


    def __str__(self):
        """ Returns a string representation of the TypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the TypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "TypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "TypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> type_asset.serialize


class MountingPoint(IdentifiedObject):
    """ Point on a structure that a connection may have a conductor connected to. Defined with an x and y coordinate plus a phase. A connection may have multiple mounting points, one for each phase.
    """
    # <<< mounting_point
    # @generated
    def __init__(self, phase_code='abc', y_coord=0, x_coord=0, overhead_conductors=None, connections=None, **kw_args):
        """ Initialises a new 'MountingPoint' instance.
        """
 Values are: "abc", "ab", "b", "bc", "ac", "split_secondary1_n", "abn", "abcn", "cn", "an", "split_secondary12_n", "bcn", "split_secondary2_n", "acn", "a", "c", "n", "bn"
        self.phase_code = 'abc'

 
        self.y_coord = y_coord

 
        self.x_coord = x_coord


        self._overhead_conductors = []
        if overhead_conductors is not None:
            self.overhead_conductors = overhead_conductors
        else:
            self.overhead_conductors = []

        self._connections = []
        if connections is not None:
            self.connections = connections
        else:
            self.connections = []


        super(MountingPoint, self).__init__(**kw_args)
    # >>> mounting_point

    # <<< overhead_conductors
    # @generated
    def get_overhead_conductors(self):
        """ 
        """
        return self._overhead_conductors

    def set_overhead_conductors(self, value):
        for x in self._overhead_conductors:
            x._mounting_point = None
        for y in value:
            y._mounting_point = self
        self._overhead_conductors = value

    overhead_conductors = property(get_overhead_conductors, set_overhead_conductors)

    def add_overhead_conductors(self, *overhead_conductors):
        for obj in overhead_conductors:
            obj._mounting_point = self
            self._overhead_conductors.append(obj)

    def remove_overhead_conductors(self, *overhead_conductors):
        for obj in overhead_conductors:
            obj._mounting_point = None
            self._overhead_conductors.remove(obj)
    # >>> overhead_conductors

    # <<< connections
    # @generated
    def get_connections(self):
        """ 
        """
        return self._connections

    def set_connections(self, value):
        for p in self._connections:
            filtered = [q for q in p.mounting_points if q != self]
            self._connections._mounting_points = filtered
        for r in value:
            if self not in r._mounting_points:
                r._mounting_points.append(self)
        self._connections = value

    connections = property(get_connections, set_connections)

    def add_connections(self, *connections):
        for obj in connections:
            if self not in obj._mounting_points:
                obj._mounting_points.append(self)
            self._connections.append(obj)

    def remove_connections(self, *connections):
        for obj in connections:
            if self in obj._mounting_points:
                obj._mounting_points.remove(self)
            self._connections.remove(obj)
    # >>> connections


    def __str__(self):
        """ Returns a string representation of the MountingPoint.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< mounting_point.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the MountingPoint.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "MountingPoint", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.overhead_conductors:
            s += '%s<%s:MountingPoint.overhead_conductors rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.connections:
            s += '%s<%s:MountingPoint.connections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:MountingPoint.phase_code>%s</%s:MountingPoint.phase_code>' % \
            (indent, ns_prefix, self.phase_code, ns_prefix)
        s += '%s<%s:MountingPoint.y_coord>%s</%s:MountingPoint.y_coord>' % \
            (indent, ns_prefix, self.y_coord, ns_prefix)
        s += '%s<%s:MountingPoint.x_coord>%s</%s:MountingPoint.x_coord>' % \
            (indent, ns_prefix, self.x_coord, ns_prefix)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "MountingPoint")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> mounting_point.serialize


class TypeAssetCatalogue(IdentifiedObject):
    """ Catalogue of generic types of assets (TypeAsset) that may be used for design purposes. It is not associated with a particular manufacturer.
    """
    # <<< type_asset_catalogue
    # @generated
    def __init__(self, type_assets=None, status=None, **kw_args):
        """ Initialises a new 'TypeAssetCatalogue' instance.
        """

        self._type_assets = []
        if type_assets is not None:
            self.type_assets = type_assets
        else:
            self.type_assets = []

        self.status = status


        super(TypeAssetCatalogue, self).__init__(**kw_args)
    # >>> type_asset_catalogue

    # <<< type_assets
    # @generated
    def get_type_assets(self):
        """ 
        """
        return self._type_assets

    def set_type_assets(self, value):
        for x in self._type_assets:
            x._type_asset_catalogue = None
        for y in value:
            y._type_asset_catalogue = self
        self._type_assets = value

    type_assets = property(get_type_assets, set_type_assets)

    def add_type_assets(self, *type_assets):
        for obj in type_assets:
            obj._type_asset_catalogue = self
            self._type_assets.append(obj)

    def remove_type_assets(self, *type_assets):
        for obj in type_assets:
            obj._type_asset_catalogue = None
            self._type_assets.remove(obj)
    # >>> type_assets

    # <<< status
    # @generated
    status = None
    # >>> status


    def __str__(self):
        """ Returns a string representation of the TypeAssetCatalogue.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< type_asset_catalogue.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the TypeAssetCatalogue.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "TypeAssetCatalogue", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.type_assets:
            s += '%s<%s:TypeAssetCatalogue.type_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:TypeAssetCatalogue.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "TypeAssetCatalogue")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> type_asset_catalogue.serialize


class Connection(IdentifiedObject):
    """ A structure can have multiple connection points for electrical connections (e.g. line) each with multiple mounting points, one for each phase. e.g. a Tower may have three Connections, two with three mounting points, one for each phase and a third with a single mounting point for the neutral line. A pole, on the other hand, may have a single Connection with one, two or three mounting points depending on whether it is carrying 1,2 or 3 phases.
    """
    # <<< connection
    # @generated
    def __init__(self, structure_type_assets=None, mounting_points=None, **kw_args):
        """ Initialises a new 'Connection' instance.
        """

        self._structure_type_assets = []
        if structure_type_assets is not None:
            self.structure_type_assets = structure_type_assets
        else:
            self.structure_type_assets = []

        self._mounting_points = []
        if mounting_points is not None:
            self.mounting_points = mounting_points
        else:
            self.mounting_points = []


        super(Connection, self).__init__(**kw_args)
    # >>> connection

    # <<< structure_type_assets
    # @generated
    def get_structure_type_assets(self):
        """ 
        """
        return self._structure_type_assets

    def set_structure_type_assets(self, value):
        for p in self._structure_type_assets:
            filtered = [q for q in p.mount_connections if q != self]
            self._structure_type_assets._mount_connections = filtered
        for r in value:
            if self not in r._mount_connections:
                r._mount_connections.append(self)
        self._structure_type_assets = value

    structure_type_assets = property(get_structure_type_assets, set_structure_type_assets)

    def add_structure_type_assets(self, *structure_type_assets):
        for obj in structure_type_assets:
            if self not in obj._mount_connections:
                obj._mount_connections.append(self)
            self._structure_type_assets.append(obj)

    def remove_structure_type_assets(self, *structure_type_assets):
        for obj in structure_type_assets:
            if self in obj._mount_connections:
                obj._mount_connections.remove(self)
            self._structure_type_assets.remove(obj)
    # >>> structure_type_assets

    # <<< mounting_points
    # @generated
    def get_mounting_points(self):
        """ 
        """
        return self._mounting_points

    def set_mounting_points(self, value):
        for p in self._mounting_points:
            filtered = [q for q in p.connections if q != self]
            self._mounting_points._connections = filtered
        for r in value:
            if self not in r._connections:
                r._connections.append(self)
        self._mounting_points = value

    mounting_points = property(get_mounting_points, set_mounting_points)

    def add_mounting_points(self, *mounting_points):
        for obj in mounting_points:
            if self not in obj._connections:
                obj._connections.append(self)
            self._mounting_points.append(obj)

    def remove_mounting_points(self, *mounting_points):
        for obj in mounting_points:
            if self in obj._connections:
                obj._connections.remove(self)
            self._mounting_points.remove(obj)
    # >>> mounting_points


    def __str__(self):
        """ Returns a string representation of the Connection.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< connection.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Connection.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Connection", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.structure_type_assets:
            s += '%s<%s:Connection.structure_type_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.mounting_points:
            s += '%s<%s:Connection.mounting_points rdf:resource="#%s"/>' % \
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

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Connection")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> connection.serialize


class ElectricalTypeAsset(TypeAsset):
    """ Generic TypeAsset for all types of component in the network that have electrical characteristics.
    """
    # <<< electrical_type_asset
    # @generated
    def __init__(self, electrical_infos=None, **kw_args):
        """ Initialises a new 'ElectricalTypeAsset' instance.
        """

        self._electrical_infos = []
        if electrical_infos is not None:
            self.electrical_infos = electrical_infos
        else:
            self.electrical_infos = []


        super(ElectricalTypeAsset, self).__init__(**kw_args)
    # >>> electrical_type_asset

    # <<< electrical_infos
    # @generated
    def get_electrical_infos(self):
        """ 
        """
        return self._electrical_infos

    def set_electrical_infos(self, value):
        for p in self._electrical_infos:
            filtered = [q for q in p.electrical_type_assets if q != self]
            self._electrical_infos._electrical_type_assets = filtered
        for r in value:
            if self not in r._electrical_type_assets:
                r._electrical_type_assets.append(self)
        self._electrical_infos = value

    electrical_infos = property(get_electrical_infos, set_electrical_infos)

    def add_electrical_infos(self, *electrical_infos):
        for obj in electrical_infos:
            if self not in obj._electrical_type_assets:
                obj._electrical_type_assets.append(self)
            self._electrical_infos.append(obj)

    def remove_electrical_infos(self, *electrical_infos):
        for obj in electrical_infos:
            if self in obj._electrical_type_assets:
                obj._electrical_type_assets.remove(self)
            self._electrical_infos.remove(obj)
    # >>> electrical_infos


    def __str__(self):
        """ Returns a string representation of the ElectricalTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< electrical_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ElectricalTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ElectricalTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ElectricalTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> electrical_type_asset.serialize


class ShuntCompensatorTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic shunt compensator that may be used for design purposes.
    """
    # <<< shunt_compensator_type_asset
    # @generated
    def __init__(self, max_power_loss=0.0, shunt_impedance_info=None, shunt_compensator_asset_models=None, **kw_args):
        """ Initialises a new 'ShuntCompensatorTypeAsset' instance.
        """
        # Maximum allowed Apparent Power loss 
        self.max_power_loss = max_power_loss


        self._shunt_impedance_info = None
        self.shunt_impedance_info = shunt_impedance_info

        self._shunt_compensator_asset_models = []
        if shunt_compensator_asset_models is not None:
            self.shunt_compensator_asset_models = shunt_compensator_asset_models
        else:
            self.shunt_compensator_asset_models = []


        super(ShuntCompensatorTypeAsset, self).__init__(**kw_args)
    # >>> shunt_compensator_type_asset

    # <<< shunt_impedance_info
    # @generated
    def get_shunt_impedance_info(self):
        """ 
        """
        return self._shunt_impedance_info

    def set_shunt_impedance_info(self, value):
        if self._shunt_impedance_info is not None:
            self._shunt_impedance_info._shunt_compensator_type_asset = None

        self._shunt_impedance_info = value
        if self._shunt_impedance_info is not None:
            self._shunt_impedance_info._shunt_compensator_type_asset = self

    shunt_impedance_info = property(get_shunt_impedance_info, set_shunt_impedance_info)
    # >>> shunt_impedance_info

    # <<< shunt_compensator_asset_models
    # @generated
    def get_shunt_compensator_asset_models(self):
        """ 
        """
        return self._shunt_compensator_asset_models

    def set_shunt_compensator_asset_models(self, value):
        for x in self._shunt_compensator_asset_models:
            x._shunt_compensator_type_asset = None
        for y in value:
            y._shunt_compensator_type_asset = self
        self._shunt_compensator_asset_models = value

    shunt_compensator_asset_models = property(get_shunt_compensator_asset_models, set_shunt_compensator_asset_models)

    def add_shunt_compensator_asset_models(self, *shunt_compensator_asset_models):
        for obj in shunt_compensator_asset_models:
            obj._shunt_compensator_type_asset = self
            self._shunt_compensator_asset_models.append(obj)

    def remove_shunt_compensator_asset_models(self, *shunt_compensator_asset_models):
        for obj in shunt_compensator_asset_models:
            obj._shunt_compensator_type_asset = None
            self._shunt_compensator_asset_models.remove(obj)
    # >>> shunt_compensator_asset_models


    def __str__(self):
        """ Returns a string representation of the ShuntCompensatorTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< shunt_compensator_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ShuntCompensatorTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ShuntCompensatorTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        if self.shunt_impedance_info is not None:
            s += '%s<%s:ShuntCompensatorTypeAsset.shunt_impedance_info rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.shunt_impedance_info.uri)
        for obj in self.shunt_compensator_asset_models:
            s += '%s<%s:ShuntCompensatorTypeAsset.shunt_compensator_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ShuntCompensatorTypeAsset.max_power_loss>%s</%s:ShuntCompensatorTypeAsset.max_power_loss>' % \
            (indent, ns_prefix, self.max_power_loss, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ShuntCompensatorTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> shunt_compensator_type_asset.serialize


class EndDeviceTypeAsset(TypeAsset):
    """ Documentation for generic End Device that may be used for various purposes such as work planning.
    """
    # <<< end_device_type_asset
    # @generated
    def __init__(self, end_device_models=None, **kw_args):
        """ Initialises a new 'EndDeviceTypeAsset' instance.
        """

        self._end_device_models = []
        if end_device_models is not None:
            self.end_device_models = end_device_models
        else:
            self.end_device_models = []


        super(EndDeviceTypeAsset, self).__init__(**kw_args)
    # >>> end_device_type_asset

    # <<< end_device_models
    # @generated
    def get_end_device_models(self):
        """ 
        """
        return self._end_device_models

    def set_end_device_models(self, value):
        for x in self._end_device_models:
            x._end_device_type_asset = None
        for y in value:
            y._end_device_type_asset = self
        self._end_device_models = value

    end_device_models = property(get_end_device_models, set_end_device_models)

    def add_end_device_models(self, *end_device_models):
        for obj in end_device_models:
            obj._end_device_type_asset = self
            self._end_device_models.append(obj)

    def remove_end_device_models(self, *end_device_models):
        for obj in end_device_models:
            obj._end_device_type_asset = None
            self._end_device_models.remove(obj)
    # >>> end_device_models


    def __str__(self):
        """ Returns a string representation of the EndDeviceTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< end_device_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the EndDeviceTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "EndDeviceTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.end_device_models:
            s += '%s<%s:EndDeviceTypeAsset.end_device_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "EndDeviceTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> end_device_type_asset.serialize


class BusbarTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic busbar that may be used for design purposes. It is typically associated with PoserSystemResource BusbarSection.
    """
    # <<< busbar_type_asset
    # @generated
    def __init__(self, busbar_type_assets=None, **kw_args):
        """ Initialises a new 'BusbarTypeAsset' instance.
        """

        self._busbar_type_assets = []
        if busbar_type_assets is not None:
            self.busbar_type_assets = busbar_type_assets
        else:
            self.busbar_type_assets = []


        super(BusbarTypeAsset, self).__init__(**kw_args)
    # >>> busbar_type_asset

    # <<< busbar_type_assets
    # @generated
    def get_busbar_type_assets(self):
        """ 
        """
        return self._busbar_type_assets

    def set_busbar_type_assets(self, value):
        for x in self._busbar_type_assets:
            x._busbar_asset_model = None
        for y in value:
            y._busbar_asset_model = self
        self._busbar_type_assets = value

    busbar_type_assets = property(get_busbar_type_assets, set_busbar_type_assets)

    def add_busbar_type_assets(self, *busbar_type_assets):
        for obj in busbar_type_assets:
            obj._busbar_asset_model = self
            self._busbar_type_assets.append(obj)

    def remove_busbar_type_assets(self, *busbar_type_assets):
        for obj in busbar_type_assets:
            obj._busbar_asset_model = None
            self._busbar_type_assets.remove(obj)
    # >>> busbar_type_assets


    def __str__(self):
        """ Returns a string representation of the BusbarTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< busbar_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the BusbarTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "BusbarTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.busbar_type_assets:
            s += '%s<%s:BusbarTypeAsset.busbar_type_assets rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "BusbarTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> busbar_type_asset.serialize


class WorkEquipmentTypeAsset(TypeAsset):
    """ Documentation for generic equipment that may be used for various purposes such as work planning.
    """
    # <<< work_equipment_type_asset
    # @generated
    def __init__(self, work_equipment_asset_models=None, **kw_args):
        """ Initialises a new 'WorkEquipmentTypeAsset' instance.
        """

        self._work_equipment_asset_models = []
        if work_equipment_asset_models is not None:
            self.work_equipment_asset_models = work_equipment_asset_models
        else:
            self.work_equipment_asset_models = []


        super(WorkEquipmentTypeAsset, self).__init__(**kw_args)
    # >>> work_equipment_type_asset

    # <<< work_equipment_asset_models
    # @generated
    def get_work_equipment_asset_models(self):
        """ 
        """
        return self._work_equipment_asset_models

    def set_work_equipment_asset_models(self, value):
        for x in self._work_equipment_asset_models:
            x._work_equipment_type_asset = None
        for y in value:
            y._work_equipment_type_asset = self
        self._work_equipment_asset_models = value

    work_equipment_asset_models = property(get_work_equipment_asset_models, set_work_equipment_asset_models)

    def add_work_equipment_asset_models(self, *work_equipment_asset_models):
        for obj in work_equipment_asset_models:
            obj._work_equipment_type_asset = self
            self._work_equipment_asset_models.append(obj)

    def remove_work_equipment_asset_models(self, *work_equipment_asset_models):
        for obj in work_equipment_asset_models:
            obj._work_equipment_type_asset = None
            self._work_equipment_asset_models.remove(obj)
    # >>> work_equipment_asset_models


    def __str__(self):
        """ Returns a string representation of the WorkEquipmentTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< work_equipment_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the WorkEquipmentTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "WorkEquipmentTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.work_equipment_asset_models:
            s += '%s<%s:WorkEquipmentTypeAsset.work_equipment_asset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "WorkEquipmentTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> work_equipment_type_asset.serialize


class SwitchTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic switch asset that may be used for design purposes.
    """
    # <<< switch_type_asset
    # @generated
    def __init__(self, switch_asset_models=None, composite_switch_type_asset=None, switch_info=None, **kw_args):
        """ Initialises a new 'SwitchTypeAsset' instance.
        """

        self._switch_asset_models = []
        if switch_asset_models is not None:
            self.switch_asset_models = switch_asset_models
        else:
            self.switch_asset_models = []

        self._composite_switch_type_asset = None
        self.composite_switch_type_asset = composite_switch_type_asset

        self._switch_info = None
        self.switch_info = switch_info


        super(SwitchTypeAsset, self).__init__(**kw_args)
    # >>> switch_type_asset

    # <<< switch_asset_models
    # @generated
    def get_switch_asset_models(self):
        """ 
        """
        return self._switch_asset_models

    def set_switch_asset_models(self, value):
        for x in self._switch_asset_models:
            x._switch_type_asset = None
        for y in value:
            y._switch_type_asset = self
        self._switch_asset_models = value

    switch_asset_models = property(get_switch_asset_models, set_switch_asset_models)

    def add_switch_asset_models(self, *switch_asset_models):
        for obj in switch_asset_models:
            obj._switch_type_asset = self
            self._switch_asset_models.append(obj)

    def remove_switch_asset_models(self, *switch_asset_models):
        for obj in switch_asset_models:
            obj._switch_type_asset = None
            self._switch_asset_models.remove(obj)
    # >>> switch_asset_models

    # <<< composite_switch_type_asset
    # @generated
    def get_composite_switch_type_asset(self):
        """ 
        """
        return self._composite_switch_type_asset

    def set_composite_switch_type_asset(self, value):
        if self._composite_switch_type_asset is not None:
            filtered = [x for x in self.composite_switch_type_asset.switch_types_assets if x != self]
            self._composite_switch_type_asset._switch_types_assets = filtered

        self._composite_switch_type_asset = value
        if self._composite_switch_type_asset is not None:
            self._composite_switch_type_asset._switch_types_assets.append(self)

    composite_switch_type_asset = property(get_composite_switch_type_asset, set_composite_switch_type_asset)
    # >>> composite_switch_type_asset

    # <<< switch_info
    # @generated
    def get_switch_info(self):
        """ 
        """
        return self._switch_info

    def set_switch_info(self, value):
        if self._switch_info is not None:
            self._switch_info._switch_type_asset = None

        self._switch_info = value
        if self._switch_info is not None:
            self._switch_info._switch_type_asset = self

    switch_info = property(get_switch_info, set_switch_info)
    # >>> switch_info


    def __str__(self):
        """ Returns a string representation of the SwitchTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< switch_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the SwitchTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "SwitchTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.switch_asset_models:
            s += '%s<%s:SwitchTypeAsset.switch_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.composite_switch_type_asset is not None:
            s += '%s<%s:SwitchTypeAsset.composite_switch_type_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.composite_switch_type_asset.uri)
        if self.switch_info is not None:
            s += '%s<%s:SwitchTypeAsset.switch_info rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.switch_info.uri)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "SwitchTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> switch_type_asset.serialize


class StructureTypeAsset(TypeAsset):
    """ A Type of Structural Asset with properties common to a large number of asset models.
    """
    # <<< structure_type_asset
    # @generated
    def __init__(self, rated_voltage=0.0, mount_connections=None, **kw_args):
        """ Initialises a new 'StructureTypeAsset' instance.
        """
        # Maximum rated voltage of the equipment that can be mounted on/contained within the structure. 
        self.rated_voltage = rated_voltage


        self._mount_connections = []
        if mount_connections is not None:
            self.mount_connections = mount_connections
        else:
            self.mount_connections = []


        super(StructureTypeAsset, self).__init__(**kw_args)
    # >>> structure_type_asset

    # <<< mount_connections
    # @generated
    def get_mount_connections(self):
        """ 
        """
        return self._mount_connections

    def set_mount_connections(self, value):
        for p in self._mount_connections:
            filtered = [q for q in p.structure_type_assets if q != self]
            self._mount_connections._structure_type_assets = filtered
        for r in value:
            if self not in r._structure_type_assets:
                r._structure_type_assets.append(self)
        self._mount_connections = value

    mount_connections = property(get_mount_connections, set_mount_connections)

    def add_mount_connections(self, *mount_connections):
        for obj in mount_connections:
            if self not in obj._structure_type_assets:
                obj._structure_type_assets.append(self)
            self._mount_connections.append(obj)

    def remove_mount_connections(self, *mount_connections):
        for obj in mount_connections:
            if self in obj._structure_type_assets:
                obj._structure_type_assets.remove(self)
            self._mount_connections.remove(obj)
    # >>> mount_connections


    def __str__(self):
        """ Returns a string representation of the StructureTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< structure_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the StructureTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "StructureTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.mount_connections:
            s += '%s<%s:StructureTypeAsset.mount_connections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:StructureTypeAsset.rated_voltage>%s</%s:StructureTypeAsset.rated_voltage>' % \
            (indent, ns_prefix, self.rated_voltage, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "StructureTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> structure_type_asset.serialize


class TowerTypeAsset(StructureTypeAsset):
    """ Documentation for a generic tower that may be used for various purposes such as work planning. A transmission tower carrying two 3-phase circuits will have 2 instances of Connection, each of which will have 3 MountingPoint instances, one for each phase all with coordinates relative to a common origin on the tower. (It may also have a 3rd Connection with a single MountingPoint for the Neutral line).
    """
    # <<< tower_type_asset
    # @generated
    def __init__(self, tower_asset_models=None, **kw_args):
        """ Initialises a new 'TowerTypeAsset' instance.
        """

        self._tower_asset_models = []
        if tower_asset_models is not None:
            self.tower_asset_models = tower_asset_models
        else:
            self.tower_asset_models = []


        super(TowerTypeAsset, self).__init__(**kw_args)
    # >>> tower_type_asset

    # <<< tower_asset_models
    # @generated
    def get_tower_asset_models(self):
        """ 
        """
        return self._tower_asset_models

    def set_tower_asset_models(self, value):
        for x in self._tower_asset_models:
            x._tower_type_asset = None
        for y in value:
            y._tower_type_asset = self
        self._tower_asset_models = value

    tower_asset_models = property(get_tower_asset_models, set_tower_asset_models)

    def add_tower_asset_models(self, *tower_asset_models):
        for obj in tower_asset_models:
            obj._tower_type_asset = self
            self._tower_asset_models.append(obj)

    def remove_tower_asset_models(self, *tower_asset_models):
        for obj in tower_asset_models:
            obj._tower_type_asset = None
            self._tower_asset_models.remove(obj)
    # >>> tower_asset_models


    def __str__(self):
        """ Returns a string representation of the TowerTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< tower_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the TowerTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "TowerTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.tower_asset_models:
            s += '%s<%s:TowerTypeAsset.tower_asset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.mount_connections:
            s += '%s<%s:StructureTypeAsset.mount_connections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:StructureTypeAsset.rated_voltage>%s</%s:StructureTypeAsset.rated_voltage>' % \
            (indent, ns_prefix, self.rated_voltage, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "TowerTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> tower_type_asset.serialize


class StreetlightTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic streetlight that may be used for various purposes such as work planning. Use 'category' for utility specific categorisation, such as luminar, grid light, lantern, open bottom, flood, etc.
    """
    # <<< streetlight_type_asset
    # @generated
    def __init__(self, light_rating=0.0, streetlight_asset_models=None, **kw_args):
        """ Initialises a new 'StreetlightTypeAsset' instance.
        """
        # Nominal (as designed) power rating of light. 
        self.light_rating = light_rating


        self._streetlight_asset_models = []
        if streetlight_asset_models is not None:
            self.streetlight_asset_models = streetlight_asset_models
        else:
            self.streetlight_asset_models = []


        super(StreetlightTypeAsset, self).__init__(**kw_args)
    # >>> streetlight_type_asset

    # <<< streetlight_asset_models
    # @generated
    def get_streetlight_asset_models(self):
        """ 
        """
        return self._streetlight_asset_models

    def set_streetlight_asset_models(self, value):
        for p in self._streetlight_asset_models:
            filtered = [q for q in p.streetlight_type_assets if q != self]
            self._streetlight_asset_models._streetlight_type_assets = filtered
        for r in value:
            if self not in r._streetlight_type_assets:
                r._streetlight_type_assets.append(self)
        self._streetlight_asset_models = value

    streetlight_asset_models = property(get_streetlight_asset_models, set_streetlight_asset_models)

    def add_streetlight_asset_models(self, *streetlight_asset_models):
        for obj in streetlight_asset_models:
            if self not in obj._streetlight_type_assets:
                obj._streetlight_type_assets.append(self)
            self._streetlight_asset_models.append(obj)

    def remove_streetlight_asset_models(self, *streetlight_asset_models):
        for obj in streetlight_asset_models:
            if self in obj._streetlight_type_assets:
                obj._streetlight_type_assets.remove(self)
            self._streetlight_asset_models.remove(obj)
    # >>> streetlight_asset_models


    def __str__(self):
        """ Returns a string representation of the StreetlightTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< streetlight_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the StreetlightTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "StreetlightTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.streetlight_asset_models:
            s += '%s<%s:StreetlightTypeAsset.streetlight_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:StreetlightTypeAsset.light_rating>%s</%s:StreetlightTypeAsset.light_rating>' % \
            (indent, ns_prefix, self.light_rating, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "StreetlightTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> streetlight_type_asset.serialize


class ToolTypeAsset(TypeAsset):
    """ Documentation for a generic tool that may be used for various purposes such as work planning.
    """
    # <<< tool_type_asset
    # @generated
    def __init__(self, tool_asset_models=None, **kw_args):
        """ Initialises a new 'ToolTypeAsset' instance.
        """

        self._tool_asset_models = []
        if tool_asset_models is not None:
            self.tool_asset_models = tool_asset_models
        else:
            self.tool_asset_models = []


        super(ToolTypeAsset, self).__init__(**kw_args)
    # >>> tool_type_asset

    # <<< tool_asset_models
    # @generated
    def get_tool_asset_models(self):
        """ 
        """
        return self._tool_asset_models

    def set_tool_asset_models(self, value):
        for x in self._tool_asset_models:
            x._tool_type_asset = None
        for y in value:
            y._tool_type_asset = self
        self._tool_asset_models = value

    tool_asset_models = property(get_tool_asset_models, set_tool_asset_models)

    def add_tool_asset_models(self, *tool_asset_models):
        for obj in tool_asset_models:
            obj._tool_type_asset = self
            self._tool_asset_models.append(obj)

    def remove_tool_asset_models(self, *tool_asset_models):
        for obj in tool_asset_models:
            obj._tool_type_asset = None
            self._tool_asset_models.remove(obj)
    # >>> tool_asset_models


    def __str__(self):
        """ Returns a string representation of the ToolTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< tool_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ToolTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ToolTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.tool_asset_models:
            s += '%s<%s:ToolTypeAsset.tool_asset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ToolTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> tool_type_asset.serialize


class CompositeSwitchTypeAsset(TypeAsset):
    """ Documentation for a generic composite switch asset that may be used for design purposes. A composite wwitch is an amalgamation of multiple Switches.
    """
    # <<< composite_switch_type_asset
    # @generated
    def __init__(self, composite_switch_asset_models=None, switch_types_assets=None, composite_switch_info=None, **kw_args):
        """ Initialises a new 'CompositeSwitchTypeAsset' instance.
        """

        self._composite_switch_asset_models = []
        if composite_switch_asset_models is not None:
            self.composite_switch_asset_models = composite_switch_asset_models
        else:
            self.composite_switch_asset_models = []

        self._switch_types_assets = []
        if switch_types_assets is not None:
            self.switch_types_assets = switch_types_assets
        else:
            self.switch_types_assets = []

        self._composite_switch_info = None
        self.composite_switch_info = composite_switch_info


        super(CompositeSwitchTypeAsset, self).__init__(**kw_args)
    # >>> composite_switch_type_asset

    # <<< composite_switch_asset_models
    # @generated
    def get_composite_switch_asset_models(self):
        """ 
        """
        return self._composite_switch_asset_models

    def set_composite_switch_asset_models(self, value):
        for x in self._composite_switch_asset_models:
            x._composite_switch_type_asset = None
        for y in value:
            y._composite_switch_type_asset = self
        self._composite_switch_asset_models = value

    composite_switch_asset_models = property(get_composite_switch_asset_models, set_composite_switch_asset_models)

    def add_composite_switch_asset_models(self, *composite_switch_asset_models):
        for obj in composite_switch_asset_models:
            obj._composite_switch_type_asset = self
            self._composite_switch_asset_models.append(obj)

    def remove_composite_switch_asset_models(self, *composite_switch_asset_models):
        for obj in composite_switch_asset_models:
            obj._composite_switch_type_asset = None
            self._composite_switch_asset_models.remove(obj)
    # >>> composite_switch_asset_models

    # <<< switch_types_assets
    # @generated
    def get_switch_types_assets(self):
        """ 
        """
        return self._switch_types_assets

    def set_switch_types_assets(self, value):
        for x in self._switch_types_assets:
            x._composite_switch_type_asset = None
        for y in value:
            y._composite_switch_type_asset = self
        self._switch_types_assets = value

    switch_types_assets = property(get_switch_types_assets, set_switch_types_assets)

    def add_switch_types_assets(self, *switch_types_assets):
        for obj in switch_types_assets:
            obj._composite_switch_type_asset = self
            self._switch_types_assets.append(obj)

    def remove_switch_types_assets(self, *switch_types_assets):
        for obj in switch_types_assets:
            obj._composite_switch_type_asset = None
            self._switch_types_assets.remove(obj)
    # >>> switch_types_assets

    # <<< composite_switch_info
    # @generated
    def get_composite_switch_info(self):
        """ 
        """
        return self._composite_switch_info

    def set_composite_switch_info(self, value):
        if self._composite_switch_info is not None:
            self._composite_switch_info._composite_switch_type_asset = None

        self._composite_switch_info = value
        if self._composite_switch_info is not None:
            self._composite_switch_info._composite_switch_type_asset = self

    composite_switch_info = property(get_composite_switch_info, set_composite_switch_info)
    # >>> composite_switch_info


    def __str__(self):
        """ Returns a string representation of the CompositeSwitchTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< composite_switch_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the CompositeSwitchTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "CompositeSwitchTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.composite_switch_asset_models:
            s += '%s<%s:CompositeSwitchTypeAsset.composite_switch_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.switch_types_assets:
            s += '%s<%s:CompositeSwitchTypeAsset.switch_types_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.composite_switch_info is not None:
            s += '%s<%s:CompositeSwitchTypeAsset.composite_switch_info rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.composite_switch_info.uri)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "CompositeSwitchTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> composite_switch_type_asset.serialize


class ComEquipmentTypeAsset(TypeAsset):
    """ Documentation for a piece of Communication Equipment (e.g., gateway, router, network hub, etc.) that may be used for design purposes.
    """
    pass
    # <<< com_equipment_type_asset
    # @generated
    def __init__(self, **kw_args):
        """ Initialises a new 'ComEquipmentTypeAsset' instance.
        """


        super(ComEquipmentTypeAsset, self).__init__(**kw_args)
    # >>> com_equipment_type_asset


    def __str__(self):
        """ Returns a string representation of the ComEquipmentTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< com_equipment_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ComEquipmentTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ComEquipmentTypeAsset", self.uri)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ComEquipmentTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> com_equipment_type_asset.serialize


class FACTSDeviceTypeAsset(ElectricalTypeAsset):
    """ Documentation for generic Flexible alternating current transmission systems (FACTS) devices that may be used for various purposes such as work planning.
    """
    # <<< factsdevice_type_asset
    # @generated
    def __init__(self, factsdevice_asset_models=None, **kw_args):
        """ Initialises a new 'FACTSDeviceTypeAsset' instance.
        """

        self._factsdevice_asset_models = []
        if factsdevice_asset_models is not None:
            self.factsdevice_asset_models = factsdevice_asset_models
        else:
            self.factsdevice_asset_models = []


        super(FACTSDeviceTypeAsset, self).__init__(**kw_args)
    # >>> factsdevice_type_asset

    # <<< factsdevice_asset_models
    # @generated
    def get_factsdevice_asset_models(self):
        """ 
        """
        return self._factsdevice_asset_models

    def set_factsdevice_asset_models(self, value):
        for x in self._factsdevice_asset_models:
            x._factsdevice_type_asset = None
        for y in value:
            y._factsdevice_type_asset = self
        self._factsdevice_asset_models = value

    factsdevice_asset_models = property(get_factsdevice_asset_models, set_factsdevice_asset_models)

    def add_factsdevice_asset_models(self, *factsdevice_asset_models):
        for obj in factsdevice_asset_models:
            obj._factsdevice_type_asset = self
            self._factsdevice_asset_models.append(obj)

    def remove_factsdevice_asset_models(self, *factsdevice_asset_models):
        for obj in factsdevice_asset_models:
            obj._factsdevice_type_asset = None
            self._factsdevice_asset_models.remove(obj)
    # >>> factsdevice_asset_models


    def __str__(self):
        """ Returns a string representation of the FACTSDeviceTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< factsdevice_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the FACTSDeviceTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "FACTSDeviceTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.factsdevice_asset_models:
            s += '%s<%s:FACTSDeviceTypeAsset.factsdevice_asset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "FACTSDeviceTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> factsdevice_type_asset.serialize


class SVCTypeAsset(FACTSDeviceTypeAsset):
    """ Documentation for a generic Static Var Compensator (SVC) that may be used for various purposes such as work planning.
    """
    # <<< svctype_asset
    # @generated
    def __init__(self, svc_infos=None, svcasset_models=None, **kw_args):
        """ Initialises a new 'SVCTypeAsset' instance.
        """

        self._svc_infos = []
        if svc_infos is not None:
            self.svc_infos = svc_infos
        else:
            self.svc_infos = []

        self._svcasset_models = []
        if svcasset_models is not None:
            self.svcasset_models = svcasset_models
        else:
            self.svcasset_models = []


        super(SVCTypeAsset, self).__init__(**kw_args)
    # >>> svctype_asset

    # <<< svc_infos
    # @generated
    def get_svc_infos(self):
        """ 
        """
        return self._svc_infos

    def set_svc_infos(self, value):
        for p in self._svc_infos:
            filtered = [q for q in p.svctype_assets if q != self]
            self._svc_infos._svctype_assets = filtered
        for r in value:
            if self not in r._svctype_assets:
                r._svctype_assets.append(self)
        self._svc_infos = value

    svc_infos = property(get_svc_infos, set_svc_infos)

    def add_svc_infos(self, *svc_infos):
        for obj in svc_infos:
            if self not in obj._svctype_assets:
                obj._svctype_assets.append(self)
            self._svc_infos.append(obj)

    def remove_svc_infos(self, *svc_infos):
        for obj in svc_infos:
            if self in obj._svctype_assets:
                obj._svctype_assets.remove(self)
            self._svc_infos.remove(obj)
    # >>> svc_infos

    # <<< svcasset_models
    # @generated
    def get_svcasset_models(self):
        """ 
        """
        return self._svcasset_models

    def set_svcasset_models(self, value):
        for x in self._svcasset_models:
            x._svctype_asset = None
        for y in value:
            y._svctype_asset = self
        self._svcasset_models = value

    svcasset_models = property(get_svcasset_models, set_svcasset_models)

    def add_svcasset_models(self, *svcasset_models):
        for obj in svcasset_models:
            obj._svctype_asset = self
            self._svcasset_models.append(obj)

    def remove_svcasset_models(self, *svcasset_models):
        for obj in svcasset_models:
            obj._svctype_asset = None
            self._svcasset_models.remove(obj)
    # >>> svcasset_models


    def __str__(self):
        """ Returns a string representation of the SVCTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< svctype_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the SVCTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "SVCTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.svc_infos:
            s += '%s<%s:SVCTypeAsset.svc_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.svcasset_models:
            s += '%s<%s:SVCTypeAsset.svcasset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.factsdevice_asset_models:
            s += '%s<%s:FACTSDeviceTypeAsset.factsdevice_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "SVCTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> svctype_asset.serialize


class ResistorTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic resistor that may be used for design purposes.
    """
    # <<< resistor_type_asset
    # @generated
    def __init__(self, resistor_asset_models=None, resistors=None, **kw_args):
        """ Initialises a new 'ResistorTypeAsset' instance.
        """

        self._resistor_asset_models = []
        if resistor_asset_models is not None:
            self.resistor_asset_models = resistor_asset_models
        else:
            self.resistor_asset_models = []

        self._resistors = []
        if resistors is not None:
            self.resistors = resistors
        else:
            self.resistors = []


        super(ResistorTypeAsset, self).__init__(**kw_args)
    # >>> resistor_type_asset

    # <<< resistor_asset_models
    # @generated
    def get_resistor_asset_models(self):
        """ 
        """
        return self._resistor_asset_models

    def set_resistor_asset_models(self, value):
        for x in self._resistor_asset_models:
            x._resistor_type_asset = None
        for y in value:
            y._resistor_type_asset = self
        self._resistor_asset_models = value

    resistor_asset_models = property(get_resistor_asset_models, set_resistor_asset_models)

    def add_resistor_asset_models(self, *resistor_asset_models):
        for obj in resistor_asset_models:
            obj._resistor_type_asset = self
            self._resistor_asset_models.append(obj)

    def remove_resistor_asset_models(self, *resistor_asset_models):
        for obj in resistor_asset_models:
            obj._resistor_type_asset = None
            self._resistor_asset_models.remove(obj)
    # >>> resistor_asset_models

    # <<< resistors
    # @generated
    def get_resistors(self):
        """ 
        """
        return self._resistors

    def set_resistors(self, value):
        for x in self._resistors:
            x._resistor_type_asset = None
        for y in value:
            y._resistor_type_asset = self
        self._resistors = value

    resistors = property(get_resistors, set_resistors)

    def add_resistors(self, *resistors):
        for obj in resistors:
            obj._resistor_type_asset = self
            self._resistors.append(obj)

    def remove_resistors(self, *resistors):
        for obj in resistors:
            obj._resistor_type_asset = None
            self._resistors.remove(obj)
    # >>> resistors


    def __str__(self):
        """ Returns a string representation of the ResistorTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< resistor_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ResistorTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ResistorTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.resistor_asset_models:
            s += '%s<%s:ResistorTypeAsset.resistor_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.resistors:
            s += '%s<%s:ResistorTypeAsset.resistors rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ResistorTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> resistor_type_asset.serialize


class SeriesCompensatorTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic series compensator that may be used for design purposes.
    """
    # <<< series_compensator_type_asset
    # @generated
    def __init__(self, shunt_compensator_asset_models=None, **kw_args):
        """ Initialises a new 'SeriesCompensatorTypeAsset' instance.
        """

        self._shunt_compensator_asset_models = []
        if shunt_compensator_asset_models is not None:
            self.shunt_compensator_asset_models = shunt_compensator_asset_models
        else:
            self.shunt_compensator_asset_models = []


        super(SeriesCompensatorTypeAsset, self).__init__(**kw_args)
    # >>> series_compensator_type_asset

    # <<< shunt_compensator_asset_models
    # @generated
    def get_shunt_compensator_asset_models(self):
        """ 
        """
        return self._shunt_compensator_asset_models

    def set_shunt_compensator_asset_models(self, value):
        for x in self._shunt_compensator_asset_models:
            x._shunt_compensator_type_asset = None
        for y in value:
            y._shunt_compensator_type_asset = self
        self._shunt_compensator_asset_models = value

    shunt_compensator_asset_models = property(get_shunt_compensator_asset_models, set_shunt_compensator_asset_models)

    def add_shunt_compensator_asset_models(self, *shunt_compensator_asset_models):
        for obj in shunt_compensator_asset_models:
            obj._shunt_compensator_type_asset = self
            self._shunt_compensator_asset_models.append(obj)

    def remove_shunt_compensator_asset_models(self, *shunt_compensator_asset_models):
        for obj in shunt_compensator_asset_models:
            obj._shunt_compensator_type_asset = None
            self._shunt_compensator_asset_models.remove(obj)
    # >>> shunt_compensator_asset_models


    def __str__(self):
        """ Returns a string representation of the SeriesCompensatorTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< series_compensator_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the SeriesCompensatorTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "SeriesCompensatorTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.shunt_compensator_asset_models:
            s += '%s<%s:SeriesCompensatorTypeAsset.shunt_compensator_asset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "SeriesCompensatorTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> series_compensator_type_asset.serialize


class FaultIndicatorTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic fault indicator that may be used for design purposes.
    """
    # <<< fault_indicator_type_asset
    # @generated
    def __init__(self, reset_kind='other', fault_indicator_asset_models=None, fault_indicators=None, **kw_args):
        """ Initialises a new 'FaultIndicatorTypeAsset' instance.
        """
        # Kind of reset mechanisim of this fault indicator. Values are: "other", "remote", "manual", "automatic"
        self.reset_kind = 'other'


        self._fault_indicator_asset_models = []
        if fault_indicator_asset_models is not None:
            self.fault_indicator_asset_models = fault_indicator_asset_models
        else:
            self.fault_indicator_asset_models = []

        self._fault_indicators = []
        if fault_indicators is not None:
            self.fault_indicators = fault_indicators
        else:
            self.fault_indicators = []


        super(FaultIndicatorTypeAsset, self).__init__(**kw_args)
    # >>> fault_indicator_type_asset

    # <<< fault_indicator_asset_models
    # @generated
    def get_fault_indicator_asset_models(self):
        """ 
        """
        return self._fault_indicator_asset_models

    def set_fault_indicator_asset_models(self, value):
        for x in self._fault_indicator_asset_models:
            x._fault_indicator_type_asset = None
        for y in value:
            y._fault_indicator_type_asset = self
        self._fault_indicator_asset_models = value

    fault_indicator_asset_models = property(get_fault_indicator_asset_models, set_fault_indicator_asset_models)

    def add_fault_indicator_asset_models(self, *fault_indicator_asset_models):
        for obj in fault_indicator_asset_models:
            obj._fault_indicator_type_asset = self
            self._fault_indicator_asset_models.append(obj)

    def remove_fault_indicator_asset_models(self, *fault_indicator_asset_models):
        for obj in fault_indicator_asset_models:
            obj._fault_indicator_type_asset = None
            self._fault_indicator_asset_models.remove(obj)
    # >>> fault_indicator_asset_models

    # <<< fault_indicators
    # @generated
    def get_fault_indicators(self):
        """ 
        """
        return self._fault_indicators

    def set_fault_indicators(self, value):
        for x in self._fault_indicators:
            x._fault_indicator_type_asset = None
        for y in value:
            y._fault_indicator_type_asset = self
        self._fault_indicators = value

    fault_indicators = property(get_fault_indicators, set_fault_indicators)

    def add_fault_indicators(self, *fault_indicators):
        for obj in fault_indicators:
            obj._fault_indicator_type_asset = self
            self._fault_indicators.append(obj)

    def remove_fault_indicators(self, *fault_indicators):
        for obj in fault_indicators:
            obj._fault_indicator_type_asset = None
            self._fault_indicators.remove(obj)
    # >>> fault_indicators


    def __str__(self):
        """ Returns a string representation of the FaultIndicatorTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< fault_indicator_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the FaultIndicatorTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "FaultIndicatorTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.fault_indicator_asset_models:
            s += '%s<%s:FaultIndicatorTypeAsset.fault_indicator_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.fault_indicators:
            s += '%s<%s:FaultIndicatorTypeAsset.fault_indicators rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:FaultIndicatorTypeAsset.reset_kind>%s</%s:FaultIndicatorTypeAsset.reset_kind>' % \
            (indent, ns_prefix, self.reset_kind, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "FaultIndicatorTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> fault_indicator_type_asset.serialize


class VehicleTypeAsset(TypeAsset):
    """ Documentation for a generic vehicle that may be used for various purposes such as work planning.
    """
    # <<< vehicle_type_asset
    # @generated
    def __init__(self, vehicle_asset_models=None, **kw_args):
        """ Initialises a new 'VehicleTypeAsset' instance.
        """

        self._vehicle_asset_models = []
        if vehicle_asset_models is not None:
            self.vehicle_asset_models = vehicle_asset_models
        else:
            self.vehicle_asset_models = []


        super(VehicleTypeAsset, self).__init__(**kw_args)
    # >>> vehicle_type_asset

    # <<< vehicle_asset_models
    # @generated
    def get_vehicle_asset_models(self):
        """ 
        """
        return self._vehicle_asset_models

    def set_vehicle_asset_models(self, value):
        for x in self._vehicle_asset_models:
            x._vehicle_type_asset = None
        for y in value:
            y._vehicle_type_asset = self
        self._vehicle_asset_models = value

    vehicle_asset_models = property(get_vehicle_asset_models, set_vehicle_asset_models)

    def add_vehicle_asset_models(self, *vehicle_asset_models):
        for obj in vehicle_asset_models:
            obj._vehicle_type_asset = self
            self._vehicle_asset_models.append(obj)

    def remove_vehicle_asset_models(self, *vehicle_asset_models):
        for obj in vehicle_asset_models:
            obj._vehicle_type_asset = None
            self._vehicle_asset_models.remove(obj)
    # >>> vehicle_asset_models


    def __str__(self):
        """ Returns a string representation of the VehicleTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< vehicle_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the VehicleTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "VehicleTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.vehicle_asset_models:
            s += '%s<%s:VehicleTypeAsset.vehicle_asset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "VehicleTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> vehicle_type_asset.serialize


class BreakerTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic breaker asset that may be used for design purposes.
    """
    # <<< breaker_type_asset
    # @generated
    def __init__(self, breaker_info=None, breaker_asset_models=None, **kw_args):
        """ Initialises a new 'BreakerTypeAsset' instance.
        """

        self._breaker_info = None
        self.breaker_info = breaker_info

        self._breaker_asset_models = []
        if breaker_asset_models is not None:
            self.breaker_asset_models = breaker_asset_models
        else:
            self.breaker_asset_models = []


        super(BreakerTypeAsset, self).__init__(**kw_args)
    # >>> breaker_type_asset

    # <<< breaker_info
    # @generated
    def get_breaker_info(self):
        """ 
        """
        return self._breaker_info

    def set_breaker_info(self, value):
        if self._breaker_info is not None:
            self._breaker_info._breaker_type_asset = None

        self._breaker_info = value
        if self._breaker_info is not None:
            self._breaker_info._breaker_type_asset = self

    breaker_info = property(get_breaker_info, set_breaker_info)
    # >>> breaker_info

    # <<< breaker_asset_models
    # @generated
    def get_breaker_asset_models(self):
        """ 
        """
        return self._breaker_asset_models

    def set_breaker_asset_models(self, value):
        for x in self._breaker_asset_models:
            x._breaker_type_asset = None
        for y in value:
            y._breaker_type_asset = self
        self._breaker_asset_models = value

    breaker_asset_models = property(get_breaker_asset_models, set_breaker_asset_models)

    def add_breaker_asset_models(self, *breaker_asset_models):
        for obj in breaker_asset_models:
            obj._breaker_type_asset = self
            self._breaker_asset_models.append(obj)

    def remove_breaker_asset_models(self, *breaker_asset_models):
        for obj in breaker_asset_models:
            obj._breaker_type_asset = None
            self._breaker_asset_models.remove(obj)
    # >>> breaker_asset_models


    def __str__(self):
        """ Returns a string representation of the BreakerTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< breaker_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the BreakerTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "BreakerTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        if self.breaker_info is not None:
            s += '%s<%s:BreakerTypeAsset.breaker_info rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.breaker_info.uri)
        for obj in self.breaker_asset_models:
            s += '%s<%s:BreakerTypeAsset.breaker_asset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "BreakerTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> breaker_type_asset.serialize


class PoleTypeAsset(StructureTypeAsset):
    """ Documentation for a generic pole that may be used for various purposes such as work planning. A pole typically has a single Connection with 1,2 or 3 mounting points.
    """
    # <<< pole_type_asset
    # @generated
    def __init__(self, length=0.0, diameter=0.0, pole_models=None, **kw_args):
        """ Initialises a new 'PoleTypeAsset' instance.
        """
        # Length of the pole (inclusive of any section of the pole that may be underground post-installation). 
        self.length = length

        # Diameter of the pole. 
        self.diameter = diameter


        self._pole_models = []
        if pole_models is not None:
            self.pole_models = pole_models
        else:
            self.pole_models = []


        super(PoleTypeAsset, self).__init__(**kw_args)
    # >>> pole_type_asset

    # <<< pole_models
    # @generated
    def get_pole_models(self):
        """ 
        """
        return self._pole_models

    def set_pole_models(self, value):
        for x in self._pole_models:
            x._pole_type_asset = None
        for y in value:
            y._pole_type_asset = self
        self._pole_models = value

    pole_models = property(get_pole_models, set_pole_models)

    def add_pole_models(self, *pole_models):
        for obj in pole_models:
            obj._pole_type_asset = self
            self._pole_models.append(obj)

    def remove_pole_models(self, *pole_models):
        for obj in pole_models:
            obj._pole_type_asset = None
            self._pole_models.remove(obj)
    # >>> pole_models


    def __str__(self):
        """ Returns a string representation of the PoleTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< pole_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the PoleTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "PoleTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.pole_models:
            s += '%s<%s:PoleTypeAsset.pole_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:PoleTypeAsset.length>%s</%s:PoleTypeAsset.length>' % \
            (indent, ns_prefix, self.length, ns_prefix)
        s += '%s<%s:PoleTypeAsset.diameter>%s</%s:PoleTypeAsset.diameter>' % \
            (indent, ns_prefix, self.diameter, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.mount_connections:
            s += '%s<%s:StructureTypeAsset.mount_connections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:StructureTypeAsset.rated_voltage>%s</%s:StructureTypeAsset.rated_voltage>' % \
            (indent, ns_prefix, self.rated_voltage, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "PoleTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> pole_type_asset.serialize


class DuctTypeAsset(StructureTypeAsset):
    """ A Duct contains underground cables and is contained within a duct bank. The xCoord and yCoord attributes define its positioning within the DuctBank.
    """
    # <<< duct_type_asset
    # @generated
    def __init__(self, x_coord=0, y_coord=0, cable_assets=None, duct_bank_type_asset=None, **kw_args):
        """ Initialises a new 'DuctTypeAsset' instance.
        """
        # X position of the duct within the duct bank. 
        self.x_coord = x_coord

        # Y position of the duct within the duct bank. 
        self.y_coord = y_coord


        self._cable_assets = []
        if cable_assets is not None:
            self.cable_assets = cable_assets
        else:
            self.cable_assets = []

        self._duct_bank_type_asset = None
        self.duct_bank_type_asset = duct_bank_type_asset


        super(DuctTypeAsset, self).__init__(**kw_args)
    # >>> duct_type_asset

    # <<< cable_assets
    # @generated
    def get_cable_assets(self):
        """ 
        """
        return self._cable_assets

    def set_cable_assets(self, value):
        for x in self._cable_assets:
            x._duct_bank_type_asset = None
        for y in value:
            y._duct_bank_type_asset = self
        self._cable_assets = value

    cable_assets = property(get_cable_assets, set_cable_assets)

    def add_cable_assets(self, *cable_assets):
        for obj in cable_assets:
            obj._duct_bank_type_asset = self
            self._cable_assets.append(obj)

    def remove_cable_assets(self, *cable_assets):
        for obj in cable_assets:
            obj._duct_bank_type_asset = None
            self._cable_assets.remove(obj)
    # >>> cable_assets

    # <<< duct_bank_type_asset
    # @generated
    def get_duct_bank_type_asset(self):
        """ 
        """
        return self._duct_bank_type_asset

    def set_duct_bank_type_asset(self, value):
        if self._duct_bank_type_asset is not None:
            filtered = [x for x in self.duct_bank_type_asset.duct_type_assets if x != self]
            self._duct_bank_type_asset._duct_type_assets = filtered

        self._duct_bank_type_asset = value
        if self._duct_bank_type_asset is not None:
            self._duct_bank_type_asset._duct_type_assets.append(self)

    duct_bank_type_asset = property(get_duct_bank_type_asset, set_duct_bank_type_asset)
    # >>> duct_bank_type_asset


    def __str__(self):
        """ Returns a string representation of the DuctTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< duct_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the DuctTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "DuctTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.cable_assets:
            s += '%s<%s:DuctTypeAsset.cable_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.duct_bank_type_asset is not None:
            s += '%s<%s:DuctTypeAsset.duct_bank_type_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.duct_bank_type_asset.uri)
        s += '%s<%s:DuctTypeAsset.x_coord>%s</%s:DuctTypeAsset.x_coord>' % \
            (indent, ns_prefix, self.x_coord, ns_prefix)
        s += '%s<%s:DuctTypeAsset.y_coord>%s</%s:DuctTypeAsset.y_coord>' % \
            (indent, ns_prefix, self.y_coord, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.mount_connections:
            s += '%s<%s:StructureTypeAsset.mount_connections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:StructureTypeAsset.rated_voltage>%s</%s:StructureTypeAsset.rated_voltage>' % \
            (indent, ns_prefix, self.rated_voltage, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "DuctTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> duct_type_asset.serialize


class SurgeProtectorTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic surge arrestor that may be used for design purposes.
    """
    # <<< surge_protector_type_asset
    # @generated
    def __init__(self, maximum_energy_absorption=0.0, maximum_continous_operating_voltage=0.0, maximum_current_rating=0.0, nominal_design_voltage=0.0, surge_protectors=None, surge_protector_asset_models=None, **kw_args):
        """ Initialises a new 'SurgeProtectorTypeAsset' instance.
        """
 
        self.maximum_energy_absorption = maximum_energy_absorption

 
        self.maximum_continous_operating_voltage = maximum_continous_operating_voltage

 
        self.maximum_current_rating = maximum_current_rating

 
        self.nominal_design_voltage = nominal_design_voltage


        self._surge_protectors = []
        if surge_protectors is not None:
            self.surge_protectors = surge_protectors
        else:
            self.surge_protectors = []

        self._surge_protector_asset_models = []
        if surge_protector_asset_models is not None:
            self.surge_protector_asset_models = surge_protector_asset_models
        else:
            self.surge_protector_asset_models = []


        super(SurgeProtectorTypeAsset, self).__init__(**kw_args)
    # >>> surge_protector_type_asset

    # <<< surge_protectors
    # @generated
    def get_surge_protectors(self):
        """ 
        """
        return self._surge_protectors

    def set_surge_protectors(self, value):
        for x in self._surge_protectors:
            x._surge_protector_type_asset = None
        for y in value:
            y._surge_protector_type_asset = self
        self._surge_protectors = value

    surge_protectors = property(get_surge_protectors, set_surge_protectors)

    def add_surge_protectors(self, *surge_protectors):
        for obj in surge_protectors:
            obj._surge_protector_type_asset = self
            self._surge_protectors.append(obj)

    def remove_surge_protectors(self, *surge_protectors):
        for obj in surge_protectors:
            obj._surge_protector_type_asset = None
            self._surge_protectors.remove(obj)
    # >>> surge_protectors

    # <<< surge_protector_asset_models
    # @generated
    def get_surge_protector_asset_models(self):
        """ 
        """
        return self._surge_protector_asset_models

    def set_surge_protector_asset_models(self, value):
        for x in self._surge_protector_asset_models:
            x._surge_protector_type_asset = None
        for y in value:
            y._surge_protector_type_asset = self
        self._surge_protector_asset_models = value

    surge_protector_asset_models = property(get_surge_protector_asset_models, set_surge_protector_asset_models)

    def add_surge_protector_asset_models(self, *surge_protector_asset_models):
        for obj in surge_protector_asset_models:
            obj._surge_protector_type_asset = self
            self._surge_protector_asset_models.append(obj)

    def remove_surge_protector_asset_models(self, *surge_protector_asset_models):
        for obj in surge_protector_asset_models:
            obj._surge_protector_type_asset = None
            self._surge_protector_asset_models.remove(obj)
    # >>> surge_protector_asset_models


    def __str__(self):
        """ Returns a string representation of the SurgeProtectorTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< surge_protector_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the SurgeProtectorTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "SurgeProtectorTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.surge_protectors:
            s += '%s<%s:SurgeProtectorTypeAsset.surge_protectors rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.surge_protector_asset_models:
            s += '%s<%s:SurgeProtectorTypeAsset.surge_protector_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:SurgeProtectorTypeAsset.maximum_energy_absorption>%s</%s:SurgeProtectorTypeAsset.maximum_energy_absorption>' % \
            (indent, ns_prefix, self.maximum_energy_absorption, ns_prefix)
        s += '%s<%s:SurgeProtectorTypeAsset.maximum_continous_operating_voltage>%s</%s:SurgeProtectorTypeAsset.maximum_continous_operating_voltage>' % \
            (indent, ns_prefix, self.maximum_continous_operating_voltage, ns_prefix)
        s += '%s<%s:SurgeProtectorTypeAsset.maximum_current_rating>%s</%s:SurgeProtectorTypeAsset.maximum_current_rating>' % \
            (indent, ns_prefix, self.maximum_current_rating, ns_prefix)
        s += '%s<%s:SurgeProtectorTypeAsset.nominal_design_voltage>%s</%s:SurgeProtectorTypeAsset.nominal_design_voltage>' % \
            (indent, ns_prefix, self.nominal_design_voltage, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "SurgeProtectorTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> surge_protector_type_asset.serialize


class ComFunctionTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic communication function that may be used for various purposes such as work planning.
    """
    # <<< com_function_type_asset
    # @generated
    def __init__(self, com_function_asset_models=None, **kw_args):
        """ Initialises a new 'ComFunctionTypeAsset' instance.
        """

        self._com_function_asset_models = []
        if com_function_asset_models is not None:
            self.com_function_asset_models = com_function_asset_models
        else:
            self.com_function_asset_models = []


        super(ComFunctionTypeAsset, self).__init__(**kw_args)
    # >>> com_function_type_asset

    # <<< com_function_asset_models
    # @generated
    def get_com_function_asset_models(self):
        """ 
        """
        return self._com_function_asset_models

    def set_com_function_asset_models(self, value):
        for x in self._com_function_asset_models:
            x._com_function_type_asset = None
        for y in value:
            y._com_function_type_asset = self
        self._com_function_asset_models = value

    com_function_asset_models = property(get_com_function_asset_models, set_com_function_asset_models)

    def add_com_function_asset_models(self, *com_function_asset_models):
        for obj in com_function_asset_models:
            obj._com_function_type_asset = self
            self._com_function_asset_models.append(obj)

    def remove_com_function_asset_models(self, *com_function_asset_models):
        for obj in com_function_asset_models:
            obj._com_function_type_asset = None
            self._com_function_asset_models.remove(obj)
    # >>> com_function_asset_models


    def __str__(self):
        """ Returns a string representation of the ComFunctionTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< com_function_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ComFunctionTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ComFunctionTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.com_function_asset_models:
            s += '%s<%s:ComFunctionTypeAsset.com_function_asset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ComFunctionTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> com_function_type_asset.serialize


class ProtectionEquipmentTypeAsset(ElectricalTypeAsset):
    """ Documentation for generic protection equiment that may be used for design purposes.
    """
    # <<< protection_equipment_type_asset
    # @generated
    def __init__(self, default_phase_trip=0.0, default_ground_trip=0.0, protection_equipment_asset_models=None, **kw_args):
        """ Initialises a new 'ProtectionEquipmentTypeAsset' instance.
        """
        # Default phase trip setting for this type of relay, if applicable. 
        self.default_phase_trip = default_phase_trip

        # Default ground trip setting for this type of relay, if applicable. 
        self.default_ground_trip = default_ground_trip


        self._protection_equipment_asset_models = []
        if protection_equipment_asset_models is not None:
            self.protection_equipment_asset_models = protection_equipment_asset_models
        else:
            self.protection_equipment_asset_models = []


        super(ProtectionEquipmentTypeAsset, self).__init__(**kw_args)
    # >>> protection_equipment_type_asset

    # <<< protection_equipment_asset_models
    # @generated
    def get_protection_equipment_asset_models(self):
        """ 
        """
        return self._protection_equipment_asset_models

    def set_protection_equipment_asset_models(self, value):
        for x in self._protection_equipment_asset_models:
            x._protection_equipment_type_asset = None
        for y in value:
            y._protection_equipment_type_asset = self
        self._protection_equipment_asset_models = value

    protection_equipment_asset_models = property(get_protection_equipment_asset_models, set_protection_equipment_asset_models)

    def add_protection_equipment_asset_models(self, *protection_equipment_asset_models):
        for obj in protection_equipment_asset_models:
            obj._protection_equipment_type_asset = self
            self._protection_equipment_asset_models.append(obj)

    def remove_protection_equipment_asset_models(self, *protection_equipment_asset_models):
        for obj in protection_equipment_asset_models:
            obj._protection_equipment_type_asset = None
            self._protection_equipment_asset_models.remove(obj)
    # >>> protection_equipment_asset_models


    def __str__(self):
        """ Returns a string representation of the ProtectionEquipmentTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< protection_equipment_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ProtectionEquipmentTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ProtectionEquipmentTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.protection_equipment_asset_models:
            s += '%s<%s:ProtectionEquipmentTypeAsset.protection_equipment_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ProtectionEquipmentTypeAsset.default_phase_trip>%s</%s:ProtectionEquipmentTypeAsset.default_phase_trip>' % \
            (indent, ns_prefix, self.default_phase_trip, ns_prefix)
        s += '%s<%s:ProtectionEquipmentTypeAsset.default_ground_trip>%s</%s:ProtectionEquipmentTypeAsset.default_ground_trip>' % \
            (indent, ns_prefix, self.default_ground_trip, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ProtectionEquipmentTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> protection_equipment_type_asset.serialize


class CabinetTypeAsset(StructureTypeAsset):
    """ Documentation for a generic cabinet that may be used for various purposes such as work planning.
    """
    # <<< cabinet_type_asset
    # @generated
    def __init__(self, cabinet_models=None, **kw_args):
        """ Initialises a new 'CabinetTypeAsset' instance.
        """

        self._cabinet_models = []
        if cabinet_models is not None:
            self.cabinet_models = cabinet_models
        else:
            self.cabinet_models = []


        super(CabinetTypeAsset, self).__init__(**kw_args)
    # >>> cabinet_type_asset

    # <<< cabinet_models
    # @generated
    def get_cabinet_models(self):
        """ 
        """
        return self._cabinet_models

    def set_cabinet_models(self, value):
        for x in self._cabinet_models:
            x._cabinet_type_asset = None
        for y in value:
            y._cabinet_type_asset = self
        self._cabinet_models = value

    cabinet_models = property(get_cabinet_models, set_cabinet_models)

    def add_cabinet_models(self, *cabinet_models):
        for obj in cabinet_models:
            obj._cabinet_type_asset = self
            self._cabinet_models.append(obj)

    def remove_cabinet_models(self, *cabinet_models):
        for obj in cabinet_models:
            obj._cabinet_type_asset = None
            self._cabinet_models.remove(obj)
    # >>> cabinet_models


    def __str__(self):
        """ Returns a string representation of the CabinetTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< cabinet_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the CabinetTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "CabinetTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.cabinet_models:
            s += '%s<%s:CabinetTypeAsset.cabinet_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.mount_connections:
            s += '%s<%s:StructureTypeAsset.mount_connections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:StructureTypeAsset.rated_voltage>%s</%s:StructureTypeAsset.rated_voltage>' % \
            (indent, ns_prefix, self.rated_voltage, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "CabinetTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> cabinet_type_asset.serialize


class MeterTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic meter that may be used for design purposes. Rather than being associated with CustomerMeter, it is associated with EnergyConsumer as it may be used for many applications, such as tie line metering, in addition to customer metering.
    """
    # <<< meter_type_asset
    # @generated
    def __init__(self, meter_asset_models=None, **kw_args):
        """ Initialises a new 'MeterTypeAsset' instance.
        """

        self._meter_asset_models = []
        if meter_asset_models is not None:
            self.meter_asset_models = meter_asset_models
        else:
            self.meter_asset_models = []


        super(MeterTypeAsset, self).__init__(**kw_args)
    # >>> meter_type_asset

    # <<< meter_asset_models
    # @generated
    def get_meter_asset_models(self):
        """ 
        """
        return self._meter_asset_models

    def set_meter_asset_models(self, value):
        for x in self._meter_asset_models:
            x._meter_type_asset = None
        for y in value:
            y._meter_type_asset = self
        self._meter_asset_models = value

    meter_asset_models = property(get_meter_asset_models, set_meter_asset_models)

    def add_meter_asset_models(self, *meter_asset_models):
        for obj in meter_asset_models:
            obj._meter_type_asset = self
            self._meter_asset_models.append(obj)

    def remove_meter_asset_models(self, *meter_asset_models):
        for obj in meter_asset_models:
            obj._meter_type_asset = None
            self._meter_asset_models.remove(obj)
    # >>> meter_asset_models


    def __str__(self):
        """ Returns a string representation of the MeterTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< meter_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the MeterTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "MeterTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.meter_asset_models:
            s += '%s<%s:MeterTypeAsset.meter_asset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "MeterTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> meter_type_asset.serialize


class GeneratorTypeAsset(ElectricalTypeAsset):
    """ Documentation for generic generation equipment that may be used for various purposes such as work planning. It defines both the Real and Reactive power properties (modelled at the PSR level as a GeneratingUnit + SynchronousMachine)
    """
    # <<< generator_type_asset
    # @generated
    def __init__(self, r_direct_subtrans=0.0, x_direct_subtrans=0.0, r_quad_trans=0.0, x_quad_trans=0.0, x_quad_sync=0.0, x_direct_sync=0.0, r_quad_sync=0.0, max_q=0.0, r_direct_sync=0.0, r_direct_trans=0.0, r_quad_subtrans=0.0, min_q=0.0, min_p=0.0, max_p=0.0, x_direct_trans=0.0, x_quad_subtrans=0.0, generator_asset_models=None, **kw_args):
        """ Initialises a new 'GeneratorTypeAsset' instance.
        """
        # Direct-axis subtransient resistance 
        self.r_direct_subtrans = r_direct_subtrans

        # Direct-axis subtransient reactance 
        self.x_direct_subtrans = x_direct_subtrans

        # Quadrature-axis Transient resistance 
        self.r_quad_trans = r_quad_trans

        # Quadrature-axis transient reactance. 
        self.x_quad_trans = x_quad_trans

        # Quadrature-axis synchronous reactance 
        self.x_quad_sync = x_quad_sync

        # Direct-axis synchronous reactance 
        self.x_direct_sync = x_direct_sync

        # Quadrature-axis synchronous resistance 
        self.r_quad_sync = r_quad_sync

        # Maximum reactive power limit. 
        self.max_q = max_q

        # Direct-axis synchronous resistance 
        self.r_direct_sync = r_direct_sync

        # Direct-axis Transient resistance 
        self.r_direct_trans = r_direct_trans

        # Quadrature-axis subtransient resistance 
        self.r_quad_subtrans = r_quad_subtrans

        # Minimum reactive power generated. 
        self.min_q = min_q

        # Minimum real power generated. 
        self.min_p = min_p

        # Maximum real power limit. 
        self.max_p = max_p

        # Direct-axis Transient reactance 
        self.x_direct_trans = x_direct_trans

        # Quadrature-axis subtransient reactance 
        self.x_quad_subtrans = x_quad_subtrans


        self._generator_asset_models = []
        if generator_asset_models is not None:
            self.generator_asset_models = generator_asset_models
        else:
            self.generator_asset_models = []


        super(GeneratorTypeAsset, self).__init__(**kw_args)
    # >>> generator_type_asset

    # <<< generator_asset_models
    # @generated
    def get_generator_asset_models(self):
        """ 
        """
        return self._generator_asset_models

    def set_generator_asset_models(self, value):
        for x in self._generator_asset_models:
            x._generator_type_asset = None
        for y in value:
            y._generator_type_asset = self
        self._generator_asset_models = value

    generator_asset_models = property(get_generator_asset_models, set_generator_asset_models)

    def add_generator_asset_models(self, *generator_asset_models):
        for obj in generator_asset_models:
            obj._generator_type_asset = self
            self._generator_asset_models.append(obj)

    def remove_generator_asset_models(self, *generator_asset_models):
        for obj in generator_asset_models:
            obj._generator_type_asset = None
            self._generator_asset_models.remove(obj)
    # >>> generator_asset_models


    def __str__(self):
        """ Returns a string representation of the GeneratorTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< generator_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the GeneratorTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "GeneratorTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.generator_asset_models:
            s += '%s<%s:GeneratorTypeAsset.generator_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:GeneratorTypeAsset.r_direct_subtrans>%s</%s:GeneratorTypeAsset.r_direct_subtrans>' % \
            (indent, ns_prefix, self.r_direct_subtrans, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.x_direct_subtrans>%s</%s:GeneratorTypeAsset.x_direct_subtrans>' % \
            (indent, ns_prefix, self.x_direct_subtrans, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.r_quad_trans>%s</%s:GeneratorTypeAsset.r_quad_trans>' % \
            (indent, ns_prefix, self.r_quad_trans, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.x_quad_trans>%s</%s:GeneratorTypeAsset.x_quad_trans>' % \
            (indent, ns_prefix, self.x_quad_trans, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.x_quad_sync>%s</%s:GeneratorTypeAsset.x_quad_sync>' % \
            (indent, ns_prefix, self.x_quad_sync, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.x_direct_sync>%s</%s:GeneratorTypeAsset.x_direct_sync>' % \
            (indent, ns_prefix, self.x_direct_sync, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.r_quad_sync>%s</%s:GeneratorTypeAsset.r_quad_sync>' % \
            (indent, ns_prefix, self.r_quad_sync, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.max_q>%s</%s:GeneratorTypeAsset.max_q>' % \
            (indent, ns_prefix, self.max_q, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.r_direct_sync>%s</%s:GeneratorTypeAsset.r_direct_sync>' % \
            (indent, ns_prefix, self.r_direct_sync, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.r_direct_trans>%s</%s:GeneratorTypeAsset.r_direct_trans>' % \
            (indent, ns_prefix, self.r_direct_trans, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.r_quad_subtrans>%s</%s:GeneratorTypeAsset.r_quad_subtrans>' % \
            (indent, ns_prefix, self.r_quad_subtrans, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.min_q>%s</%s:GeneratorTypeAsset.min_q>' % \
            (indent, ns_prefix, self.min_q, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.min_p>%s</%s:GeneratorTypeAsset.min_p>' % \
            (indent, ns_prefix, self.min_p, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.max_p>%s</%s:GeneratorTypeAsset.max_p>' % \
            (indent, ns_prefix, self.max_p, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.x_direct_trans>%s</%s:GeneratorTypeAsset.x_direct_trans>' % \
            (indent, ns_prefix, self.x_direct_trans, ns_prefix)
        s += '%s<%s:GeneratorTypeAsset.x_quad_subtrans>%s</%s:GeneratorTypeAsset.x_quad_subtrans>' % \
            (indent, ns_prefix, self.x_quad_subtrans, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "GeneratorTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> generator_type_asset.serialize


class SubstationTypeAsset(TypeAsset):
    """ Documentation for a type of substation that may be used for design purposes.
    """
    pass
    # <<< substation_type_asset
    # @generated
    def __init__(self, **kw_args):
        """ Initialises a new 'SubstationTypeAsset' instance.
        """


        super(SubstationTypeAsset, self).__init__(**kw_args)
    # >>> substation_type_asset


    def __str__(self):
        """ Returns a string representation of the SubstationTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< substation_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the SubstationTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "SubstationTypeAsset", self.uri)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "SubstationTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> substation_type_asset.serialize


class AssetFunctionTypeAsset(TypeAsset):
    """ Documentation for a generic Asset Function that may be used for various purposes such as work planning.
    """
    # <<< asset_function_type_asset
    # @generated
    def __init__(self, asset_function_asset_models=None, **kw_args):
        """ Initialises a new 'AssetFunctionTypeAsset' instance.
        """

        self._asset_function_asset_models = []
        if asset_function_asset_models is not None:
            self.asset_function_asset_models = asset_function_asset_models
        else:
            self.asset_function_asset_models = []


        super(AssetFunctionTypeAsset, self).__init__(**kw_args)
    # >>> asset_function_type_asset

    # <<< asset_function_asset_models
    # @generated
    def get_asset_function_asset_models(self):
        """ 
        """
        return self._asset_function_asset_models

    def set_asset_function_asset_models(self, value):
        for x in self._asset_function_asset_models:
            x._asset_function_type_asset = None
        for y in value:
            y._asset_function_type_asset = self
        self._asset_function_asset_models = value

    asset_function_asset_models = property(get_asset_function_asset_models, set_asset_function_asset_models)

    def add_asset_function_asset_models(self, *asset_function_asset_models):
        for obj in asset_function_asset_models:
            obj._asset_function_type_asset = self
            self._asset_function_asset_models.append(obj)

    def remove_asset_function_asset_models(self, *asset_function_asset_models):
        for obj in asset_function_asset_models:
            obj._asset_function_type_asset = None
            self._asset_function_asset_models.remove(obj)
    # >>> asset_function_asset_models


    def __str__(self):
        """ Returns a string representation of the AssetFunctionTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< asset_function_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the AssetFunctionTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "AssetFunctionTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.asset_function_asset_models:
            s += '%s<%s:AssetFunctionTypeAsset.asset_function_asset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "AssetFunctionTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> asset_function_type_asset.serialize


class PotentialTransformerTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic Potential Transformer (PT) that may be used for various purposes such as work planning.
    """
    # <<< potential_transformer_type_asset
    # @generated
    def __init__(self, pt_class='', accuracy_class='', nominal_ratio=None, potential_transformers=None, potential_transformer_asset_models=None, potential_transformer_info=None, **kw_args):
        """ Initialises a new 'PotentialTransformerTypeAsset' instance.
        """
 
        self.pt_class = pt_class

 
        self.accuracy_class = accuracy_class


        self.nominal_ratio = nominal_ratio

        self._potential_transformers = []
        if potential_transformers is not None:
            self.potential_transformers = potential_transformers
        else:
            self.potential_transformers = []

        self._potential_transformer_asset_models = []
        if potential_transformer_asset_models is not None:
            self.potential_transformer_asset_models = potential_transformer_asset_models
        else:
            self.potential_transformer_asset_models = []

        self._potential_transformer_info = None
        self.potential_transformer_info = potential_transformer_info


        super(PotentialTransformerTypeAsset, self).__init__(**kw_args)
    # >>> potential_transformer_type_asset

    # <<< nominal_ratio
    # @generated
    nominal_ratio = None
    # >>> nominal_ratio

    # <<< potential_transformers
    # @generated
    def get_potential_transformers(self):
        """ 
        """
        return self._potential_transformers

    def set_potential_transformers(self, value):
        for x in self._potential_transformers:
            x._potential_transformer_type_asset = None
        for y in value:
            y._potential_transformer_type_asset = self
        self._potential_transformers = value

    potential_transformers = property(get_potential_transformers, set_potential_transformers)

    def add_potential_transformers(self, *potential_transformers):
        for obj in potential_transformers:
            obj._potential_transformer_type_asset = self
            self._potential_transformers.append(obj)

    def remove_potential_transformers(self, *potential_transformers):
        for obj in potential_transformers:
            obj._potential_transformer_type_asset = None
            self._potential_transformers.remove(obj)
    # >>> potential_transformers

    # <<< potential_transformer_asset_models
    # @generated
    def get_potential_transformer_asset_models(self):
        """ 
        """
        return self._potential_transformer_asset_models

    def set_potential_transformer_asset_models(self, value):
        for x in self._potential_transformer_asset_models:
            x._potential_transformer_type_asset = None
        for y in value:
            y._potential_transformer_type_asset = self
        self._potential_transformer_asset_models = value

    potential_transformer_asset_models = property(get_potential_transformer_asset_models, set_potential_transformer_asset_models)

    def add_potential_transformer_asset_models(self, *potential_transformer_asset_models):
        for obj in potential_transformer_asset_models:
            obj._potential_transformer_type_asset = self
            self._potential_transformer_asset_models.append(obj)

    def remove_potential_transformer_asset_models(self, *potential_transformer_asset_models):
        for obj in potential_transformer_asset_models:
            obj._potential_transformer_type_asset = None
            self._potential_transformer_asset_models.remove(obj)
    # >>> potential_transformer_asset_models

    # <<< potential_transformer_info
    # @generated
    def get_potential_transformer_info(self):
        """ 
        """
        return self._potential_transformer_info

    def set_potential_transformer_info(self, value):
        if self._potential_transformer_info is not None:
            self._potential_transformer_info._potential_transformer_type_asset = None

        self._potential_transformer_info = value
        if self._potential_transformer_info is not None:
            self._potential_transformer_info._potential_transformer_type_asset = self

    potential_transformer_info = property(get_potential_transformer_info, set_potential_transformer_info)
    # >>> potential_transformer_info


    def __str__(self):
        """ Returns a string representation of the PotentialTransformerTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< potential_transformer_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the PotentialTransformerTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "PotentialTransformerTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        if self.nominal_ratio is not None:
            s += '%s<%s:PotentialTransformerTypeAsset.nominal_ratio rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.nominal_ratio.uri)
        for obj in self.potential_transformers:
            s += '%s<%s:PotentialTransformerTypeAsset.potential_transformers rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.potential_transformer_asset_models:
            s += '%s<%s:PotentialTransformerTypeAsset.potential_transformer_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.potential_transformer_info is not None:
            s += '%s<%s:PotentialTransformerTypeAsset.potential_transformer_info rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.potential_transformer_info.uri)
        s += '%s<%s:PotentialTransformerTypeAsset.pt_class>%s</%s:PotentialTransformerTypeAsset.pt_class>' % \
            (indent, ns_prefix, self.pt_class, ns_prefix)
        s += '%s<%s:PotentialTransformerTypeAsset.accuracy_class>%s</%s:PotentialTransformerTypeAsset.accuracy_class>' % \
            (indent, ns_prefix, self.accuracy_class, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "PotentialTransformerTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> potential_transformer_type_asset.serialize


class RecloserTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic recloser asset that may be used for design purposes.
    """
    # <<< recloser_type_asset
    # @generated
    def __init__(self, recloser_info=None, recloser_asset_models=None, **kw_args):
        """ Initialises a new 'RecloserTypeAsset' instance.
        """

        self._recloser_info = None
        self.recloser_info = recloser_info

        self._recloser_asset_models = []
        if recloser_asset_models is not None:
            self.recloser_asset_models = recloser_asset_models
        else:
            self.recloser_asset_models = []


        super(RecloserTypeAsset, self).__init__(**kw_args)
    # >>> recloser_type_asset

    # <<< recloser_info
    # @generated
    def get_recloser_info(self):
        """ 
        """
        return self._recloser_info

    def set_recloser_info(self, value):
        if self._recloser_info is not None:
            self._recloser_info._recloser_type_asset = None

        self._recloser_info = value
        if self._recloser_info is not None:
            self._recloser_info._recloser_type_asset = self

    recloser_info = property(get_recloser_info, set_recloser_info)
    # >>> recloser_info

    # <<< recloser_asset_models
    # @generated
    def get_recloser_asset_models(self):
        """ 
        """
        return self._recloser_asset_models

    def set_recloser_asset_models(self, value):
        for x in self._recloser_asset_models:
            x._recloser_type_asset = None
        for y in value:
            y._recloser_type_asset = self
        self._recloser_asset_models = value

    recloser_asset_models = property(get_recloser_asset_models, set_recloser_asset_models)

    def add_recloser_asset_models(self, *recloser_asset_models):
        for obj in recloser_asset_models:
            obj._recloser_type_asset = self
            self._recloser_asset_models.append(obj)

    def remove_recloser_asset_models(self, *recloser_asset_models):
        for obj in recloser_asset_models:
            obj._recloser_type_asset = None
            self._recloser_asset_models.remove(obj)
    # >>> recloser_asset_models


    def __str__(self):
        """ Returns a string representation of the RecloserTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< recloser_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the RecloserTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "RecloserTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        if self.recloser_info is not None:
            s += '%s<%s:RecloserTypeAsset.recloser_info rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.recloser_info.uri)
        for obj in self.recloser_asset_models:
            s += '%s<%s:RecloserTypeAsset.recloser_asset_models rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "RecloserTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> recloser_type_asset.serialize


class CurrentTransformerTypeAsset(ElectricalTypeAsset):
    """ Documentation for a generic Current Transformer (CT) that may be used for various purposes such as work planning.
    """
    # <<< current_transformer_type_asset
    # @generated
    def __init__(self, usage='', accuracy_class='', accuracy_limit=0.0, knee_point_current=0.0, core_burden=0.0, ct_class='', core_count=0, knee_point_voltage=0.0, current_transformer_info=None, current_transformer_asset_models=None, current_transformers=None, nominal_ratio=None, max_ratio=None, **kw_args):
        """ Initialises a new 'CurrentTransformerTypeAsset' instance.
        """
        # eg. metering, protection, etc 
        self.usage = usage

        # CT accuracy classification 
        self.accuracy_class = accuracy_class

 
        self.accuracy_limit = accuracy_limit

        # Maximum primary current where the CT still displays linear characteristicts. 
        self.knee_point_current = knee_point_current

        # Power burden of the CT core 
        self.core_burden = core_burden

 
        self.ct_class = ct_class

        # Number of cores. 
        self.core_count = core_count

        # Maximum voltage across the secondary terminals where the CT still displays linear characteristicts. 
        self.knee_point_voltage = knee_point_voltage


        self._current_transformer_info = None
        self.current_transformer_info = current_transformer_info

        self._current_transformer_asset_models = []
        if current_transformer_asset_models is not None:
            self.current_transformer_asset_models = current_transformer_asset_models
        else:
            self.current_transformer_asset_models = []

        self._current_transformers = []
        if current_transformers is not None:
            self.current_transformers = current_transformers
        else:
            self.current_transformers = []

        self.nominal_ratio = nominal_ratio

        self.max_ratio = max_ratio


        super(CurrentTransformerTypeAsset, self).__init__(**kw_args)
    # >>> current_transformer_type_asset

    # <<< current_transformer_info
    # @generated
    def get_current_transformer_info(self):
        """ 
        """
        return self._current_transformer_info

    def set_current_transformer_info(self, value):
        if self._current_transformer_info is not None:
            self._current_transformer_info._current_transformer_type_asset = None

        self._current_transformer_info = value
        if self._current_transformer_info is not None:
            self._current_transformer_info._current_transformer_type_asset = self

    current_transformer_info = property(get_current_transformer_info, set_current_transformer_info)
    # >>> current_transformer_info

    # <<< current_transformer_asset_models
    # @generated
    def get_current_transformer_asset_models(self):
        """ 
        """
        return self._current_transformer_asset_models

    def set_current_transformer_asset_models(self, value):
        for x in self._current_transformer_asset_models:
            x._current_transformer_type_asset = None
        for y in value:
            y._current_transformer_type_asset = self
        self._current_transformer_asset_models = value

    current_transformer_asset_models = property(get_current_transformer_asset_models, set_current_transformer_asset_models)

    def add_current_transformer_asset_models(self, *current_transformer_asset_models):
        for obj in current_transformer_asset_models:
            obj._current_transformer_type_asset = self
            self._current_transformer_asset_models.append(obj)

    def remove_current_transformer_asset_models(self, *current_transformer_asset_models):
        for obj in current_transformer_asset_models:
            obj._current_transformer_type_asset = None
            self._current_transformer_asset_models.remove(obj)
    # >>> current_transformer_asset_models

    # <<< current_transformers
    # @generated
    def get_current_transformers(self):
        """ 
        """
        return self._current_transformers

    def set_current_transformers(self, value):
        for x in self._current_transformers:
            x._current_transformer_type_asset = None
        for y in value:
            y._current_transformer_type_asset = self
        self._current_transformers = value

    current_transformers = property(get_current_transformers, set_current_transformers)

    def add_current_transformers(self, *current_transformers):
        for obj in current_transformers:
            obj._current_transformer_type_asset = self
            self._current_transformers.append(obj)

    def remove_current_transformers(self, *current_transformers):
        for obj in current_transformers:
            obj._current_transformer_type_asset = None
            self._current_transformers.remove(obj)
    # >>> current_transformers

    # <<< nominal_ratio
    # @generated
    # Nominal ratio between the primary and secondary current; i.e. 100:5
    nominal_ratio = None
    # >>> nominal_ratio

    # <<< max_ratio
    # @generated
    # Maximum ratio between the primary and secondary current.
    max_ratio = None
    # >>> max_ratio


    def __str__(self):
        """ Returns a string representation of the CurrentTransformerTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< current_transformer_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the CurrentTransformerTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "CurrentTransformerTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        if self.current_transformer_info is not None:
            s += '%s<%s:CurrentTransformerTypeAsset.current_transformer_info rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.current_transformer_info.uri)
        for obj in self.current_transformer_asset_models:
            s += '%s<%s:CurrentTransformerTypeAsset.current_transformer_asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.current_transformers:
            s += '%s<%s:CurrentTransformerTypeAsset.current_transformers rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.nominal_ratio is not None:
            s += '%s<%s:CurrentTransformerTypeAsset.nominal_ratio rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.nominal_ratio.uri)
        if self.max_ratio is not None:
            s += '%s<%s:CurrentTransformerTypeAsset.max_ratio rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.max_ratio.uri)
        s += '%s<%s:CurrentTransformerTypeAsset.usage>%s</%s:CurrentTransformerTypeAsset.usage>' % \
            (indent, ns_prefix, self.usage, ns_prefix)
        s += '%s<%s:CurrentTransformerTypeAsset.accuracy_class>%s</%s:CurrentTransformerTypeAsset.accuracy_class>' % \
            (indent, ns_prefix, self.accuracy_class, ns_prefix)
        s += '%s<%s:CurrentTransformerTypeAsset.accuracy_limit>%s</%s:CurrentTransformerTypeAsset.accuracy_limit>' % \
            (indent, ns_prefix, self.accuracy_limit, ns_prefix)
        s += '%s<%s:CurrentTransformerTypeAsset.knee_point_current>%s</%s:CurrentTransformerTypeAsset.knee_point_current>' % \
            (indent, ns_prefix, self.knee_point_current, ns_prefix)
        s += '%s<%s:CurrentTransformerTypeAsset.core_burden>%s</%s:CurrentTransformerTypeAsset.core_burden>' % \
            (indent, ns_prefix, self.core_burden, ns_prefix)
        s += '%s<%s:CurrentTransformerTypeAsset.ct_class>%s</%s:CurrentTransformerTypeAsset.ct_class>' % \
            (indent, ns_prefix, self.ct_class, ns_prefix)
        s += '%s<%s:CurrentTransformerTypeAsset.core_count>%s</%s:CurrentTransformerTypeAsset.core_count>' % \
            (indent, ns_prefix, self.core_count, ns_prefix)
        s += '%s<%s:CurrentTransformerTypeAsset.knee_point_voltage>%s</%s:CurrentTransformerTypeAsset.knee_point_voltage>' % \
            (indent, ns_prefix, self.knee_point_voltage, ns_prefix)
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.electrical_infos:
            s += '%s<%s:ElectricalTypeAsset.electrical_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "CurrentTransformerTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> current_transformer_type_asset.serialize


class DuctBankTypeAsset(StructureTypeAsset):
    """ A DuctBank contains multiple Ducts. The DuctBank itself should have no connections, since these are defined by the individual ducts within it. However, it will have a ConstructionType and the material it is constructed from.
    """
    # <<< duct_bank_type_asset
    # @generated
    def __init__(self, duct_type_assets=None, duct_banks=None, **kw_args):
        """ Initialises a new 'DuctBankTypeAsset' instance.
        """

        self._duct_type_assets = []
        if duct_type_assets is not None:
            self.duct_type_assets = duct_type_assets
        else:
            self.duct_type_assets = []

        self._duct_banks = []
        if duct_banks is not None:
            self.duct_banks = duct_banks
        else:
            self.duct_banks = []


        super(DuctBankTypeAsset, self).__init__(**kw_args)
    # >>> duct_bank_type_asset

    # <<< duct_type_assets
    # @generated
    def get_duct_type_assets(self):
        """ 
        """
        return self._duct_type_assets

    def set_duct_type_assets(self, value):
        for x in self._duct_type_assets:
            x._duct_bank_type_asset = None
        for y in value:
            y._duct_bank_type_asset = self
        self._duct_type_assets = value

    duct_type_assets = property(get_duct_type_assets, set_duct_type_assets)

    def add_duct_type_assets(self, *duct_type_assets):
        for obj in duct_type_assets:
            obj._duct_bank_type_asset = self
            self._duct_type_assets.append(obj)

    def remove_duct_type_assets(self, *duct_type_assets):
        for obj in duct_type_assets:
            obj._duct_bank_type_asset = None
            self._duct_type_assets.remove(obj)
    # >>> duct_type_assets

    # <<< duct_banks
    # @generated
    def get_duct_banks(self):
        """ 
        """
        return self._duct_banks

    def set_duct_banks(self, value):
        for x in self._duct_banks:
            x._duct_bank_type_asset = None
        for y in value:
            y._duct_bank_type_asset = self
        self._duct_banks = value

    duct_banks = property(get_duct_banks, set_duct_banks)

    def add_duct_banks(self, *duct_banks):
        for obj in duct_banks:
            obj._duct_bank_type_asset = self
            self._duct_banks.append(obj)

    def remove_duct_banks(self, *duct_banks):
        for obj in duct_banks:
            obj._duct_bank_type_asset = None
            self._duct_banks.remove(obj)
    # >>> duct_banks


    def __str__(self):
        """ Returns a string representation of the DuctBankTypeAsset.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< duct_bank_type_asset.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the DuctBankTypeAsset.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "DuctBankTypeAsset", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.duct_type_assets:
            s += '%s<%s:DuctBankTypeAsset.duct_type_assets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.duct_banks:
            s += '%s<%s:DuctBankTypeAsset.duct_banks rdf:resource="#%s"/>' % \
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
        for obj in self.activity_records:
            s += '%s<%s:Document.activity_records rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_organisation_roles:
            s += '%s<%s:Document.erp_organisation_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.scheduled_events:
            s += '%s<%s:Document.scheduled_events rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.from_document_roles:
            s += '%s<%s:Document.from_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.location_roles:
            s += '%s<%s:Document.location_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.power_system_resource_roles:
            s += '%s<%s:Document.power_system_resource_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.network_data_sets:
            s += '%s<%s:Document.network_data_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_person_roles:
            s += '%s<%s:Document.erp_person_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_items:
            s += '%s<%s:Document.change_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.measurements:
            s += '%s<%s:Document.measurements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.doc_status is not None:
            s += '%s<%s:Document.doc_status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.doc_status.uri)
        for obj in self.schedule_parameter_infos:
            s += '%s<%s:Document.schedule_parameter_infos rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.electronic_address is not None:
            s += '%s<%s:Document.electronic_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.electronic_address.uri)
        for obj in self.to_document_roles:
            s += '%s<%s:Document.to_document_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.status is not None:
            s += '%s<%s:Document.status rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.status.uri)
        for obj in self.asset_roles:
            s += '%s<%s:Document.asset_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.change_sets:
            s += '%s<%s:Document.change_sets rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Document.subject>%s</%s:Document.subject>' % \
            (indent, ns_prefix, self.subject, ns_prefix)
        s += '%s<%s:Document.revision_number>%s</%s:Document.revision_number>' % \
            (indent, ns_prefix, self.revision_number, ns_prefix)
        s += '%s<%s:Document.category>%s</%s:Document.category>' % \
            (indent, ns_prefix, self.category, ns_prefix)
        s += '%s<%s:Document.last_modified_date_time>%s</%s:Document.last_modified_date_time>' % \
            (indent, ns_prefix, self.last_modified_date_time, ns_prefix)
        s += '%s<%s:Document.title>%s</%s:Document.title>' % \
            (indent, ns_prefix, self.title, ns_prefix)
        s += '%s<%s:Document.created_date_time>%s</%s:Document.created_date_time>' % \
            (indent, ns_prefix, self.created_date_time, ns_prefix)
        if self.cuwork_equipment_asset is not None:
            s += '%s<%s:TypeAsset.cuwork_equipment_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuwork_equipment_asset.uri)
        if self.cuasset is not None:
            s += '%s<%s:TypeAsset.cuasset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cuasset.uri)
        if self.type_asset_catalogue is not None:
            s += '%s<%s:TypeAsset.type_asset_catalogue rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.type_asset_catalogue.uri)
        for obj in self.asset_models:
            s += '%s<%s:TypeAsset.asset_models rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_inventory_issues:
            s += '%s<%s:TypeAsset.erp_inventory_issues rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_req_line_items:
            s += '%s<%s:TypeAsset.erp_req_line_items rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.erp_bom_item_datas:
            s += '%s<%s:TypeAsset.erp_bom_item_datas rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TypeAsset.quantity>%s</%s:TypeAsset.quantity>' % \
            (indent, ns_prefix, self.quantity, ns_prefix)
        s += '%s<%s:TypeAsset.stock_item>%s</%s:TypeAsset.stock_item>' % \
            (indent, ns_prefix, self.stock_item, ns_prefix)
        s += '%s<%s:TypeAsset.estimated_unit_cost>%s</%s:TypeAsset.estimated_unit_cost>' % \
            (indent, ns_prefix, self.estimated_unit_cost, ns_prefix)
        for obj in self.mount_connections:
            s += '%s<%s:StructureTypeAsset.mount_connections rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:StructureTypeAsset.rated_voltage>%s</%s:StructureTypeAsset.rated_voltage>' % \
            (indent, ns_prefix, self.rated_voltage, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "DuctBankTypeAsset")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> duct_bank_type_asset.serialize


# <<< inf_type_asset
# @generated
# >>> inf_type_asset
