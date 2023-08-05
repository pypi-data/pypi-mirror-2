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

""" This package is an extension of the Metering package and contains the information classes that support specialized applications such as prepayment metering. These classes are generally associated with the collection and control of revenue from the customer for a delivered service.
"""

from cim.iec61968.common import Document
from cim import Element
from cim.iec61970.core import IdentifiedObject
from cim.iec61968.common import Agreement
from cim.iec61968.common import Organisation

# <<< imports
# @generated
# >>> imports

ns_prefix = "cim.paymentmetering"

ns_uri = "http://iec.ch/TC57/2009/CIM-schema-cim14#PaymentMetering"

class MerchantAccount(Document):
    """ The operating account controlled by MerchantAgreement, against which Vendor may vend tokens or receipt payments. Transactions via VendorShift debit the account and bank deposits via BankStatement credit the account.
    """
    # <<< merchant_account
    # @generated
    def __init__(self, provisional_balance=0.0, current_balance=0.0, vendors=None, transactors=None, bank_statements=None, merchant_agreement=None, vendor_shifts=None, **kw_args):
        """ Initialises a new 'MerchantAccount' instance.
        """
        # The balance of this account after taking into account any pending debits from VendorShift.merchantDebitAmount and pending credits from BankStatement.merchantCreditAmount or credits (see also BankStatement attributes and VendorShift attributes). 
        self.provisional_balance = provisional_balance

        # The current operating balance of this account. 
        self.current_balance = current_balance


        self._vendors = []
        if vendors is not None:
            self.vendors = vendors
        else:
            self.vendors = []

        self._transactors = []
        if transactors is not None:
            self.transactors = transactors
        else:
            self.transactors = []

        self._bank_statements = []
        if bank_statements is not None:
            self.bank_statements = bank_statements
        else:
            self.bank_statements = []

        self._merchant_agreement = None
        self.merchant_agreement = merchant_agreement

        self._vendor_shifts = []
        if vendor_shifts is not None:
            self.vendor_shifts = vendor_shifts
        else:
            self.vendor_shifts = []


        super(MerchantAccount, self).__init__(**kw_args)
    # >>> merchant_account

    # <<< vendors
    # @generated
    def get_vendors(self):
        """ All vendors selling tokens or receipt payments against this merchant account.
        """
        return self._vendors

    def set_vendors(self, value):
        for x in self._vendors:
            x._merchant_account = None
        for y in value:
            y._merchant_account = self
        self._vendors = value

    vendors = property(get_vendors, set_vendors)

    def add_vendors(self, *vendors):
        for obj in vendors:
            obj._merchant_account = self
            self._vendors.append(obj)

    def remove_vendors(self, *vendors):
        for obj in vendors:
            obj._merchant_account = None
            self._vendors.remove(obj)
    # >>> vendors

    # <<< transactors
    # @generated
    def get_transactors(self):
        """ All transactors this merchant account is registered with.
        """
        return self._transactors

    def set_transactors(self, value):
        for p in self._transactors:
            filtered = [q for q in p.merchant_accounts if q != self]
            self._transactors._merchant_accounts = filtered
        for r in value:
            if self not in r._merchant_accounts:
                r._merchant_accounts.append(self)
        self._transactors = value

    transactors = property(get_transactors, set_transactors)

    def add_transactors(self, *transactors):
        for obj in transactors:
            if self not in obj._merchant_accounts:
                obj._merchant_accounts.append(self)
            self._transactors.append(obj)

    def remove_transactors(self, *transactors):
        for obj in transactors:
            if self in obj._merchant_accounts:
                obj._merchant_accounts.remove(self)
            self._transactors.remove(obj)
    # >>> transactors

    # <<< bank_statements
    # @generated
    def get_bank_statements(self):
        """ 
        """
        return self._bank_statements

    def set_bank_statements(self, value):
        for x in self._bank_statements:
            x._merchant_account = None
        for y in value:
            y._merchant_account = self
        self._bank_statements = value

    bank_statements = property(get_bank_statements, set_bank_statements)

    def add_bank_statements(self, *bank_statements):
        for obj in bank_statements:
            obj._merchant_account = self
            self._bank_statements.append(obj)

    def remove_bank_statements(self, *bank_statements):
        for obj in bank_statements:
            obj._merchant_account = None
            self._bank_statements.remove(obj)
    # >>> bank_statements

    # <<< merchant_agreement
    # @generated
    def get_merchant_agreement(self):
        """ Merchant agreement that instantiated this merchant account.
        """
        return self._merchant_agreement

    def set_merchant_agreement(self, value):
        if self._merchant_agreement is not None:
            filtered = [x for x in self.merchant_agreement.merchant_accounts if x != self]
            self._merchant_agreement._merchant_accounts = filtered

        self._merchant_agreement = value
        if self._merchant_agreement is not None:
            self._merchant_agreement._merchant_accounts.append(self)

    merchant_agreement = property(get_merchant_agreement, set_merchant_agreement)
    # >>> merchant_agreement

    # <<< vendor_shifts
    # @generated
    def get_vendor_shifts(self):
        """ All vendor shifts that operate on this merchant account.
        """
        return self._vendor_shifts

    def set_vendor_shifts(self, value):
        for x in self._vendor_shifts:
            x._merchant_account = None
        for y in value:
            y._merchant_account = self
        self._vendor_shifts = value

    vendor_shifts = property(get_vendor_shifts, set_vendor_shifts)

    def add_vendor_shifts(self, *vendor_shifts):
        for obj in vendor_shifts:
            obj._merchant_account = self
            self._vendor_shifts.append(obj)

    def remove_vendor_shifts(self, *vendor_shifts):
        for obj in vendor_shifts:
            obj._merchant_account = None
            self._vendor_shifts.remove(obj)
    # >>> vendor_shifts


    def __str__(self):
        """ Returns a string representation of the MerchantAccount.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< merchant_account.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the MerchantAccount.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "MerchantAccount", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.vendors:
            s += '%s<%s:MerchantAccount.vendors rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.transactors:
            s += '%s<%s:MerchantAccount.transactors rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.bank_statements:
            s += '%s<%s:MerchantAccount.bank_statements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.merchant_agreement is not None:
            s += '%s<%s:MerchantAccount.merchant_agreement rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.merchant_agreement.uri)
        for obj in self.vendor_shifts:
            s += '%s<%s:MerchantAccount.vendor_shifts rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:MerchantAccount.provisional_balance>%s</%s:MerchantAccount.provisional_balance>' % \
            (indent, ns_prefix, self.provisional_balance, ns_prefix)
        s += '%s<%s:MerchantAccount.current_balance>%s</%s:MerchantAccount.current_balance>' % \
            (indent, ns_prefix, self.current_balance, ns_prefix)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "MerchantAccount")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> merchant_account.serialize


class AuxiliaryAccount(Document):
    """ Variable and dynamic part of AuxiliaryAgreement, generally representing the current state of the account related to the outstanding balance defined in AuxiliaryAgreement.
    """
    # <<< auxiliary_account
    # @generated
    def __init__(self, balance=0.0, principle_amount=0.0, last_debit=None, charges=None, last_credit=None, auxiliary_agreement=None, payment_transactions=None, due=None, **kw_args):
        """ Initialises a new 'AuxiliaryAccount' instance.
        """
        # The total amount currently remaining on this account that is required to be paid in order to settle the account to zero. This excludes any due amounts not yet paid. 
        self.balance = balance

        # The initial principle amount, with which this account was instantiated. 
        self.principle_amount = principle_amount


        self.last_debit = last_debit

        self._charges = []
        if charges is not None:
            self.charges = charges
        else:
            self.charges = []

        self.last_credit = last_credit

        self._auxiliary_agreement = None
        self.auxiliary_agreement = auxiliary_agreement

        self._payment_transactions = []
        if payment_transactions is not None:
            self.payment_transactions = payment_transactions
        else:
            self.payment_transactions = []

        self.due = due


        super(AuxiliaryAccount, self).__init__(**kw_args)
    # >>> auxiliary_account

    # <<< last_debit
    # @generated
    # Details of the last debit transaction performed on this account.
    last_debit = None
    # >>> last_debit

    # <<< charges
    # @generated
    def get_charges(self):
        """ All charges levied on this account.
        """
        return self._charges

    def set_charges(self, value):
        for p in self._charges:
            filtered = [q for q in p.auxiliary_accounts if q != self]
            self._charges._auxiliary_accounts = filtered
        for r in value:
            if self not in r._auxiliary_accounts:
                r._auxiliary_accounts.append(self)
        self._charges = value

    charges = property(get_charges, set_charges)

    def add_charges(self, *charges):
        for obj in charges:
            if self not in obj._auxiliary_accounts:
                obj._auxiliary_accounts.append(self)
            self._charges.append(obj)

    def remove_charges(self, *charges):
        for obj in charges:
            if self in obj._auxiliary_accounts:
                obj._auxiliary_accounts.remove(self)
            self._charges.remove(obj)
    # >>> charges

    # <<< last_credit
    # @generated
    # Details of the last credit transaction performed on this account.
    last_credit = None
    # >>> last_credit

    # <<< auxiliary_agreement
    # @generated
    def get_auxiliary_agreement(self):
        """ Auxiliary agreement regulating this account.
        """
        return self._auxiliary_agreement

    def set_auxiliary_agreement(self, value):
        if self._auxiliary_agreement is not None:
            filtered = [x for x in self.auxiliary_agreement.auxiliary_accounts if x != self]
            self._auxiliary_agreement._auxiliary_accounts = filtered

        self._auxiliary_agreement = value
        if self._auxiliary_agreement is not None:
            self._auxiliary_agreement._auxiliary_accounts.append(self)

    auxiliary_agreement = property(get_auxiliary_agreement, set_auxiliary_agreement)
    # >>> auxiliary_agreement

    # <<< payment_transactions
    # @generated
    def get_payment_transactions(self):
        """ All payments against this account.
        """
        return self._payment_transactions

    def set_payment_transactions(self, value):
        for x in self._payment_transactions:
            x._auxiliary_account = None
        for y in value:
            y._auxiliary_account = self
        self._payment_transactions = value

    payment_transactions = property(get_payment_transactions, set_payment_transactions)

    def add_payment_transactions(self, *payment_transactions):
        for obj in payment_transactions:
            obj._auxiliary_account = self
            self._payment_transactions.append(obj)

    def remove_payment_transactions(self, *payment_transactions):
        for obj in payment_transactions:
            obj._auxiliary_account = None
            self._payment_transactions.remove(obj)
    # >>> payment_transactions

    # <<< due
    # @generated
    # Current amounts now due for payment on this account.
    due = None
    # >>> due


    def __str__(self):
        """ Returns a string representation of the AuxiliaryAccount.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< auxiliary_account.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the AuxiliaryAccount.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "AuxiliaryAccount", self.uri)
        if format:
            indent += ' ' * depth

        if self.last_debit is not None:
            s += '%s<%s:AuxiliaryAccount.last_debit rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.last_debit.uri)
        for obj in self.charges:
            s += '%s<%s:AuxiliaryAccount.charges rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.last_credit is not None:
            s += '%s<%s:AuxiliaryAccount.last_credit rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.last_credit.uri)
        if self.auxiliary_agreement is not None:
            s += '%s<%s:AuxiliaryAccount.auxiliary_agreement rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.auxiliary_agreement.uri)
        for obj in self.payment_transactions:
            s += '%s<%s:AuxiliaryAccount.payment_transactions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.due is not None:
            s += '%s<%s:AuxiliaryAccount.due rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.due.uri)
        s += '%s<%s:AuxiliaryAccount.balance>%s</%s:AuxiliaryAccount.balance>' % \
            (indent, ns_prefix, self.balance, ns_prefix)
        s += '%s<%s:AuxiliaryAccount.principle_amount>%s</%s:AuxiliaryAccount.principle_amount>' % \
            (indent, ns_prefix, self.principle_amount, ns_prefix)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "AuxiliaryAccount")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> auxiliary_account.serialize


class BankAccountDetail(Element):
    """ Details of a bank account.
    """
    # <<< bank_account_detail
    # @generated
    def __init__(self, branch_code='', holder_id='', holder_name='', account_number='', bank_name='', **kw_args):
        """ Initialises a new 'BankAccountDetail' instance.
        """
        # Branch of bank where account is held. 
        self.branch_code = branch_code

        # National identity number (or equivalent) of account holder. 
        self.holder_id = holder_id

        # Name of account holder. 
        self.holder_name = holder_name

        # Operational account reference number. 
        self.account_number = account_number

        # Name of bank where account is held. 
        self.bank_name = bank_name



        super(BankAccountDetail, self).__init__(**kw_args)
    # >>> bank_account_detail


    def __str__(self):
        """ Returns a string representation of the BankAccountDetail.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< bank_account_detail.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the BankAccountDetail.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "BankAccountDetail", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:BankAccountDetail.branch_code>%s</%s:BankAccountDetail.branch_code>' % \
            (indent, ns_prefix, self.branch_code, ns_prefix)
        s += '%s<%s:BankAccountDetail.holder_id>%s</%s:BankAccountDetail.holder_id>' % \
            (indent, ns_prefix, self.holder_id, ns_prefix)
        s += '%s<%s:BankAccountDetail.holder_name>%s</%s:BankAccountDetail.holder_name>' % \
            (indent, ns_prefix, self.holder_name, ns_prefix)
        s += '%s<%s:BankAccountDetail.account_number>%s</%s:BankAccountDetail.account_number>' % \
            (indent, ns_prefix, self.account_number, ns_prefix)
        s += '%s<%s:BankAccountDetail.bank_name>%s</%s:BankAccountDetail.bank_name>' % \
            (indent, ns_prefix, self.bank_name, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "BankAccountDetail")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> bank_account_detail.serialize


class AccountMovement(Element):
    """ Credit/debit movements for an account.
    """
    # <<< account_movement
    # @generated
    def __init__(self, amount=0.0, date_time='', reason='', **kw_args):
        """ Initialises a new 'AccountMovement' instance.
        """
        # Amount that was credited to/debited from an account. For example: payment received/interest charge on arrears. 
        self.amount = amount

        # Date and time when the credit/debit transaction was performed. 
        self.date_time = date_time

        # Reason for credit/debit transaction on an account. Example: payment received/arrears interest levied. 
        self.reason = reason



        super(AccountMovement, self).__init__(**kw_args)
    # >>> account_movement


    def __str__(self):
        """ Returns a string representation of the AccountMovement.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< account_movement.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the AccountMovement.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "AccountMovement", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:AccountMovement.amount>%s</%s:AccountMovement.amount>' % \
            (indent, ns_prefix, self.amount, ns_prefix)
        s += '%s<%s:AccountMovement.date_time>%s</%s:AccountMovement.date_time>' % \
            (indent, ns_prefix, self.date_time, ns_prefix)
        s += '%s<%s:AccountMovement.reason>%s</%s:AccountMovement.reason>' % \
            (indent, ns_prefix, self.reason, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "AccountMovement")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> account_movement.serialize


class TimeTariffInterval(Element):
    """ One of a sequence of time intervals defined in terms of real time. It is typically used in association with TariffProfile to define the intervals in a time of use tariff structure, where startDateTime simultaneously determines the starting point of this interval and the ending point of the previous interval.
    """
    # <<< time_tariff_interval
    # @generated
    def __init__(self, start_date_time='', sequence_number=0, tariff_profiles=None, charges=None, **kw_args):
        """ Initialises a new 'TimeTariffInterval' instance.
        """
        # A real time marker that defines the starting time (typically it is the time of day) for this interval. The interval extends to the start of the next interval or until it is reset to the start of the first interval by TariffProfile.tariffCycle. 
        self.start_date_time = start_date_time

        # A sequential reference that defines the identity of this interval and its relative position with respect to other intervals in a sequence of intervals. 
        self.sequence_number = sequence_number


        self._tariff_profiles = []
        if tariff_profiles is not None:
            self.tariff_profiles = tariff_profiles
        else:
            self.tariff_profiles = []

        self._charges = []
        if charges is not None:
            self.charges = charges
        else:
            self.charges = []


        super(TimeTariffInterval, self).__init__(**kw_args)
    # >>> time_tariff_interval

    # <<< tariff_profiles
    # @generated
    def get_tariff_profiles(self):
        """ All tariff profiles defined by this time tariff interval.
        """
        return self._tariff_profiles

    def set_tariff_profiles(self, value):
        for p in self._tariff_profiles:
            filtered = [q for q in p.time_tariff_intervals if q != self]
            self._tariff_profiles._time_tariff_intervals = filtered
        for r in value:
            if self not in r._time_tariff_intervals:
                r._time_tariff_intervals.append(self)
        self._tariff_profiles = value

    tariff_profiles = property(get_tariff_profiles, set_tariff_profiles)

    def add_tariff_profiles(self, *tariff_profiles):
        for obj in tariff_profiles:
            if self not in obj._time_tariff_intervals:
                obj._time_tariff_intervals.append(self)
            self._tariff_profiles.append(obj)

    def remove_tariff_profiles(self, *tariff_profiles):
        for obj in tariff_profiles:
            if self in obj._time_tariff_intervals:
                obj._time_tariff_intervals.remove(self)
            self._tariff_profiles.remove(obj)
    # >>> tariff_profiles

    # <<< charges
    # @generated
    def get_charges(self):
        """ All charges used to define this time tariff interval.
        """
        return self._charges

    def set_charges(self, value):
        for p in self._charges:
            filtered = [q for q in p.time_tariff_intervals if q != self]
            self._charges._time_tariff_intervals = filtered
        for r in value:
            if self not in r._time_tariff_intervals:
                r._time_tariff_intervals.append(self)
        self._charges = value

    charges = property(get_charges, set_charges)

    def add_charges(self, *charges):
        for obj in charges:
            if self not in obj._time_tariff_intervals:
                obj._time_tariff_intervals.append(self)
            self._charges.append(obj)

    def remove_charges(self, *charges):
        for obj in charges:
            if self in obj._time_tariff_intervals:
                obj._time_tariff_intervals.remove(self)
            self._charges.remove(obj)
    # >>> charges


    def __str__(self):
        """ Returns a string representation of the TimeTariffInterval.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< time_tariff_interval.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the TimeTariffInterval.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "TimeTariffInterval", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.tariff_profiles:
            s += '%s<%s:TimeTariffInterval.tariff_profiles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.charges:
            s += '%s<%s:TimeTariffInterval.charges rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TimeTariffInterval.start_date_time>%s</%s:TimeTariffInterval.start_date_time>' % \
            (indent, ns_prefix, self.start_date_time, ns_prefix)
        s += '%s<%s:TimeTariffInterval.sequence_number>%s</%s:TimeTariffInterval.sequence_number>' % \
            (indent, ns_prefix, self.sequence_number, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "TimeTariffInterval")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> time_tariff_interval.serialize


class Due(Element):
    """ Details on amounts due for an account.
    """
    # <<< due
    # @generated
    def __init__(self, principle=0.0, current=0.0, charges=0.0, arrears=0.0, interest=0.0, **kw_args):
        """ Initialises a new 'Due' instance.
        """
        # Part of 'current' that constitutes the portion of the principle amount currently due. 
        self.principle = principle

        # Current total amount now due: current = principle + arrears + interest + charges. Typically the rule for settlement priority is: interest dues, then arrears dues, then current dues, then charge dues. 
        self.current = current

        # Part of 'current' that constitutes the charge portion: 'charges' = 'Charge.fixedPortion' + 'Charge.variablePortion'. 
        self.charges = charges

        # Part of 'current' that constitutes the arrears portion. 
        self.arrears = arrears

        # Part of 'current' that constitutes the interest portion. 
        self.interest = interest



        super(Due, self).__init__(**kw_args)
    # >>> due


    def __str__(self):
        """ Returns a string representation of the Due.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< due.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Due.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Due", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:Due.principle>%s</%s:Due.principle>' % \
            (indent, ns_prefix, self.principle, ns_prefix)
        s += '%s<%s:Due.current>%s</%s:Due.current>' % \
            (indent, ns_prefix, self.current, ns_prefix)
        s += '%s<%s:Due.charges>%s</%s:Due.charges>' % \
            (indent, ns_prefix, self.charges, ns_prefix)
        s += '%s<%s:Due.arrears>%s</%s:Due.arrears>' % \
            (indent, ns_prefix, self.arrears, ns_prefix)
        s += '%s<%s:Due.interest>%s</%s:Due.interest>' % \
            (indent, ns_prefix, self.interest, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Due")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> due.serialize


class ConsumptionTariffInterval(Element):
    """ One of a sequence of intervals defined in terms of consumption quantity of a service such as electricity, water, gas, etc. It is typically used in association with TariffProfile to define the steps or blocks in a step tariff structure, where startValue simultaneously defines the entry value of this step and the closing value of the previous step. Where consumption is &gt;= startValue it falls within this interval and where consumption is &lt; startValue it falls within the previous interval.
    """
    # <<< consumption_tariff_interval
    # @generated
    def __init__(self, sequence_number=0, start_value=0.0, charges=None, tariff_profiles=None, **kw_args):
        """ Initialises a new 'ConsumptionTariffInterval' instance.
        """
        # A sequential reference that defines the identity of this interval and its relative position with respect to other intervals in a sequence of intervals. 
        self.sequence_number = sequence_number

        # The lowest level of consumption that defines the starting point of this interval. The interval extends to the start of the next interval or until it is reset to the start of the first interval by TariffProfile.tariffCycle. 
        self.start_value = start_value


        self._charges = []
        if charges is not None:
            self.charges = charges
        else:
            self.charges = []

        self._tariff_profiles = []
        if tariff_profiles is not None:
            self.tariff_profiles = tariff_profiles
        else:
            self.tariff_profiles = []


        super(ConsumptionTariffInterval, self).__init__(**kw_args)
    # >>> consumption_tariff_interval

    # <<< charges
    # @generated
    def get_charges(self):
        """ All charges used to define this consumption tariff interval.
        """
        return self._charges

    def set_charges(self, value):
        for p in self._charges:
            filtered = [q for q in p.consumption_tariff_intervals if q != self]
            self._charges._consumption_tariff_intervals = filtered
        for r in value:
            if self not in r._consumption_tariff_intervals:
                r._consumption_tariff_intervals.append(self)
        self._charges = value

    charges = property(get_charges, set_charges)

    def add_charges(self, *charges):
        for obj in charges:
            if self not in obj._consumption_tariff_intervals:
                obj._consumption_tariff_intervals.append(self)
            self._charges.append(obj)

    def remove_charges(self, *charges):
        for obj in charges:
            if self in obj._consumption_tariff_intervals:
                obj._consumption_tariff_intervals.remove(self)
            self._charges.remove(obj)
    # >>> charges

    # <<< tariff_profiles
    # @generated
    def get_tariff_profiles(self):
        """ All tariff profiles defined by this consumption tariff interval.
        """
        return self._tariff_profiles

    def set_tariff_profiles(self, value):
        for p in self._tariff_profiles:
            filtered = [q for q in p.consumption_tariff_intervals if q != self]
            self._tariff_profiles._consumption_tariff_intervals = filtered
        for r in value:
            if self not in r._consumption_tariff_intervals:
                r._consumption_tariff_intervals.append(self)
        self._tariff_profiles = value

    tariff_profiles = property(get_tariff_profiles, set_tariff_profiles)

    def add_tariff_profiles(self, *tariff_profiles):
        for obj in tariff_profiles:
            if self not in obj._consumption_tariff_intervals:
                obj._consumption_tariff_intervals.append(self)
            self._tariff_profiles.append(obj)

    def remove_tariff_profiles(self, *tariff_profiles):
        for obj in tariff_profiles:
            if self in obj._consumption_tariff_intervals:
                obj._consumption_tariff_intervals.remove(self)
            self._tariff_profiles.remove(obj)
    # >>> tariff_profiles


    def __str__(self):
        """ Returns a string representation of the ConsumptionTariffInterval.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< consumption_tariff_interval.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ConsumptionTariffInterval.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ConsumptionTariffInterval", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.charges:
            s += '%s<%s:ConsumptionTariffInterval.charges rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.tariff_profiles:
            s += '%s<%s:ConsumptionTariffInterval.tariff_profiles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ConsumptionTariffInterval.sequence_number>%s</%s:ConsumptionTariffInterval.sequence_number>' % \
            (indent, ns_prefix, self.sequence_number, ns_prefix)
        s += '%s<%s:ConsumptionTariffInterval.start_value>%s</%s:ConsumptionTariffInterval.start_value>' % \
            (indent, ns_prefix, self.start_value, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ConsumptionTariffInterval")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> consumption_tariff_interval.serialize


class Cashier(IdentifiedObject):
    """ The operator of the point of sale for the duration of CashierShift. Cashier is under the exclusive management control of Vendor.
    """
    # <<< cashier
    # @generated
    def __init__(self, electronic_addresses=None, cashier_shifts=None, vendor=None, **kw_args):
        """ Initialises a new 'Cashier' instance.
        """

        self._electronic_addresses = []
        if electronic_addresses is not None:
            self.electronic_addresses = electronic_addresses
        else:
            self.electronic_addresses = []

        self._cashier_shifts = []
        if cashier_shifts is not None:
            self.cashier_shifts = cashier_shifts
        else:
            self.cashier_shifts = []

        self._vendor = None
        self.vendor = vendor


        super(Cashier, self).__init__(**kw_args)
    # >>> cashier

    # <<< electronic_addresses
    # @generated
    def get_electronic_addresses(self):
        """ 
        """
        return self._electronic_addresses

    def set_electronic_addresses(self, value):
        for x in self._electronic_addresses:
            x._cashier = None
        for y in value:
            y._cashier = self
        self._electronic_addresses = value

    electronic_addresses = property(get_electronic_addresses, set_electronic_addresses)

    def add_electronic_addresses(self, *electronic_addresses):
        for obj in electronic_addresses:
            obj._cashier = self
            self._electronic_addresses.append(obj)

    def remove_electronic_addresses(self, *electronic_addresses):
        for obj in electronic_addresses:
            obj._cashier = None
            self._electronic_addresses.remove(obj)
    # >>> electronic_addresses

    # <<< cashier_shifts
    # @generated
    def get_cashier_shifts(self):
        """ All shifts operated by this cashier.
        """
        return self._cashier_shifts

    def set_cashier_shifts(self, value):
        for x in self._cashier_shifts:
            x._cashier = None
        for y in value:
            y._cashier = self
        self._cashier_shifts = value

    cashier_shifts = property(get_cashier_shifts, set_cashier_shifts)

    def add_cashier_shifts(self, *cashier_shifts):
        for obj in cashier_shifts:
            obj._cashier = self
            self._cashier_shifts.append(obj)

    def remove_cashier_shifts(self, *cashier_shifts):
        for obj in cashier_shifts:
            obj._cashier = None
            self._cashier_shifts.remove(obj)
    # >>> cashier_shifts

    # <<< vendor
    # @generated
    def get_vendor(self):
        """ Vendor that manages this Cachier.
        """
        return self._vendor

    def set_vendor(self, value):
        if self._vendor is not None:
            filtered = [x for x in self.vendor.cashiers if x != self]
            self._vendor._cashiers = filtered

        self._vendor = value
        if self._vendor is not None:
            self._vendor._cashiers.append(self)

    vendor = property(get_vendor, set_vendor)
    # >>> vendor


    def __str__(self):
        """ Returns a string representation of the Cashier.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< cashier.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Cashier.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Cashier", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.electronic_addresses:
            s += '%s<%s:Cashier.electronic_addresses rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.cashier_shifts:
            s += '%s<%s:Cashier.cashier_shifts rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.vendor is not None:
            s += '%s<%s:Cashier.vendor rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.vendor.uri)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "Cashier")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> cashier.serialize


class Shift(IdentifiedObject):
    """ Generally referring to a period of operation or work performed. Whether shift is open/closed can be derived from attributes 'activiryInterval.start' and 'activityInterval.end'. The grand total for receipts (i.e., cumulative total of all actual receipted amounts during this shift; bankable + non-bankable; excludes rounding error totals) can be derived from Receipt attributes: =sum(Receipt.receiptAmount) ; includes bankable and non-bankable receipts. Must also reconcile against: =sum(receiptsGrandTotalBankable + receiptsGrandTotalNonBankable). Must also reconcile against ReceiptSummary: =sum(ReceiptSummary.receiptsTotal). The attributes with 'GrandTotal' defined in this class may need to be used when the source data is periodically flushed from the system and then these cannot be derived.
    """
    # <<< shift
    # @generated
    def __init__(self, transactions_grand_total_rounding=0.0, transactions_grand_total=0.0, receipts_grand_total_bankable=0.0, receipts_grand_total_rounding=0.0, receipts_grand_total_non_bankable=0.0, receipt_summaries=None, activity_interval=None, transaction_summaries=None, **kw_args):
        """ Initialises a new 'Shift' instance.
        """
        # Cumulative amount in error due to process rounding not reflected in transactionsGandTotal. Values are obtained from Transaction attributes: =sum(Transaction.transactionRounding). 
        self.transactions_grand_total_rounding = transactions_grand_total_rounding

        # Cumulative total of transacted amounts during this shift. Values are obtained from Transaction attributes: =sum(Transaction.transactionAmount). It must also reconcile against TransactionSummary: =sum(TransactionSummary.transactionsTotal). 
        self.transactions_grand_total = transactions_grand_total

        # Total of amounts receipted during this shift that can be manually banked (cash and cheques for example). Values are obtained from Receipt attributes: =sum(Receipt.receiptAmount) for all Receipt.bankable = true. 
        self.receipts_grand_total_bankable = receipts_grand_total_bankable

        # Cumulative amount in error due to process rounding not reflected in receiptsGrandTotal. Values are obtained from Receipt attributes: =sum(Receipt.receiptRounding). 
        self.receipts_grand_total_rounding = receipts_grand_total_rounding

        # Total of amounts receipted during this shift that cannot be manually banked (card payments for example). Values are obtained from Receipt attributes: =sum(Receipt.receiptAmount) for all Receipt.bankable = false. 
        self.receipts_grand_total_non_bankable = receipts_grand_total_non_bankable


        self._receipt_summaries = []
        if receipt_summaries is not None:
            self.receipt_summaries = receipt_summaries
        else:
            self.receipt_summaries = []

        self.activity_interval = activity_interval

        self._transaction_summaries = []
        if transaction_summaries is not None:
            self.transaction_summaries = transaction_summaries
        else:
            self.transaction_summaries = []


        super(Shift, self).__init__(**kw_args)
    # >>> shift

    # <<< receipt_summaries
    # @generated
    def get_receipt_summaries(self):
        """ All receipt summaries for this shift.
        """
        return self._receipt_summaries

    def set_receipt_summaries(self, value):
        for x in self._receipt_summaries:
            x._shift = None
        for y in value:
            y._shift = self
        self._receipt_summaries = value

    receipt_summaries = property(get_receipt_summaries, set_receipt_summaries)

    def add_receipt_summaries(self, *receipt_summaries):
        for obj in receipt_summaries:
            obj._shift = self
            self._receipt_summaries.append(obj)

    def remove_receipt_summaries(self, *receipt_summaries):
        for obj in receipt_summaries:
            obj._shift = None
            self._receipt_summaries.remove(obj)
    # >>> receipt_summaries

    # <<< activity_interval
    # @generated
    # Interval for activity of this shift.
    activity_interval = None
    # >>> activity_interval

    # <<< transaction_summaries
    # @generated
    def get_transaction_summaries(self):
        """ All transaction summaries recorded for this shift.
        """
        return self._transaction_summaries

    def set_transaction_summaries(self, value):
        for x in self._transaction_summaries:
            x._shift = None
        for y in value:
            y._shift = self
        self._transaction_summaries = value

    transaction_summaries = property(get_transaction_summaries, set_transaction_summaries)

    def add_transaction_summaries(self, *transaction_summaries):
        for obj in transaction_summaries:
            obj._shift = self
            self._transaction_summaries.append(obj)

    def remove_transaction_summaries(self, *transaction_summaries):
        for obj in transaction_summaries:
            obj._shift = None
            self._transaction_summaries.remove(obj)
    # >>> transaction_summaries


    def __str__(self):
        """ Returns a string representation of the Shift.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< shift.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Shift.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Shift", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.receipt_summaries:
            s += '%s<%s:Shift.receipt_summaries rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.activity_interval is not None:
            s += '%s<%s:Shift.activity_interval rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.activity_interval.uri)
        for obj in self.transaction_summaries:
            s += '%s<%s:Shift.transaction_summaries rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Shift.transactions_grand_total_rounding>%s</%s:Shift.transactions_grand_total_rounding>' % \
            (indent, ns_prefix, self.transactions_grand_total_rounding, ns_prefix)
        s += '%s<%s:Shift.transactions_grand_total>%s</%s:Shift.transactions_grand_total>' % \
            (indent, ns_prefix, self.transactions_grand_total, ns_prefix)
        s += '%s<%s:Shift.receipts_grand_total_bankable>%s</%s:Shift.receipts_grand_total_bankable>' % \
            (indent, ns_prefix, self.receipts_grand_total_bankable, ns_prefix)
        s += '%s<%s:Shift.receipts_grand_total_rounding>%s</%s:Shift.receipts_grand_total_rounding>' % \
            (indent, ns_prefix, self.receipts_grand_total_rounding, ns_prefix)
        s += '%s<%s:Shift.receipts_grand_total_non_bankable>%s</%s:Shift.receipts_grand_total_non_bankable>' % \
            (indent, ns_prefix, self.receipts_grand_total_non_bankable, ns_prefix)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "Shift")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> shift.serialize


class MerchantAgreement(Agreement):
    """ A formal controlling contractual agreement between Supplier and Merchant, in terms of which Merchant is authorised to vend tokens and receipt payments on behalf of Supplier. Merchant is accountable to Supplier for revenue collected at PointOfSale.
    """
    # <<< merchant_agreement
    # @generated
    def __init__(self, merchant_accounts=None, **kw_args):
        """ Initialises a new 'MerchantAgreement' instance.
        """

        self._merchant_accounts = []
        if merchant_accounts is not None:
            self.merchant_accounts = merchant_accounts
        else:
            self.merchant_accounts = []


        super(MerchantAgreement, self).__init__(**kw_args)
    # >>> merchant_agreement

    # <<< merchant_accounts
    # @generated
    def get_merchant_accounts(self):
        """ All merchant accounts instantiated as a result of this merchant agreement.
        """
        return self._merchant_accounts

    def set_merchant_accounts(self, value):
        for x in self._merchant_accounts:
            x._merchant_agreement = None
        for y in value:
            y._merchant_agreement = self
        self._merchant_accounts = value

    merchant_accounts = property(get_merchant_accounts, set_merchant_accounts)

    def add_merchant_accounts(self, *merchant_accounts):
        for obj in merchant_accounts:
            obj._merchant_agreement = self
            self._merchant_accounts.append(obj)

    def remove_merchant_accounts(self, *merchant_accounts):
        for obj in merchant_accounts:
            obj._merchant_agreement = None
            self._merchant_accounts.remove(obj)
    # >>> merchant_accounts


    def __str__(self):
        """ Returns a string representation of the MerchantAgreement.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< merchant_agreement.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the MerchantAgreement.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "MerchantAgreement", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.merchant_accounts:
            s += '%s<%s:MerchantAgreement.merchant_accounts rdf:resource="#%s"/>' % \
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
        if self.validity_interval is not None:
            s += '%s<%s:Agreement.validity_interval rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.validity_interval.uri)
        s += '%s<%s:Agreement.sign_date>%s</%s:Agreement.sign_date>' % \
            (indent, ns_prefix, self.sign_date, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "MerchantAgreement")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> merchant_agreement.serialize


class Charge(IdentifiedObject):
    """ A charge element associated with other entities such as tariff structures, auxiliary agreements or other charge elements. The total charge amount applicable to this instance of Charge is the sum of fixedPortion plus percentagePortion.
    """
    # <<< charge
    # @generated
    def __init__(self, kind='other', variable_portion=0.0, consumption_tariff_intervals=None, auxiliary_accounts=None, time_tariff_intervals=None, parent_charge=None, child_charges=None, fixed_portion=None, **kw_args):
        """ Initialises a new 'Charge' instance.
        """
        # The kind of charge to be applied. Values are: "other", "auxiliary_charge", "demand_charge", "tax_charge", "consumption_charge"
        self.kind = 'other'

        # The variable portion of this charge element, calculated as a percentage of the total amount of a parent charge. 
        self.variable_portion = variable_portion


        self._consumption_tariff_intervals = []
        if consumption_tariff_intervals is not None:
            self.consumption_tariff_intervals = consumption_tariff_intervals
        else:
            self.consumption_tariff_intervals = []

        self._auxiliary_accounts = []
        if auxiliary_accounts is not None:
            self.auxiliary_accounts = auxiliary_accounts
        else:
            self.auxiliary_accounts = []

        self._time_tariff_intervals = []
        if time_tariff_intervals is not None:
            self.time_tariff_intervals = time_tariff_intervals
        else:
            self.time_tariff_intervals = []

        self._parent_charge = None
        self.parent_charge = parent_charge

        self._child_charges = []
        if child_charges is not None:
            self.child_charges = child_charges
        else:
            self.child_charges = []

        self.fixed_portion = fixed_portion


        super(Charge, self).__init__(**kw_args)
    # >>> charge

    # <<< consumption_tariff_intervals
    # @generated
    def get_consumption_tariff_intervals(self):
        """ Tariff intervals to which this consumption-based charge must be levied.
        """
        return self._consumption_tariff_intervals

    def set_consumption_tariff_intervals(self, value):
        for p in self._consumption_tariff_intervals:
            filtered = [q for q in p.charges if q != self]
            self._consumption_tariff_intervals._charges = filtered
        for r in value:
            if self not in r._charges:
                r._charges.append(self)
        self._consumption_tariff_intervals = value

    consumption_tariff_intervals = property(get_consumption_tariff_intervals, set_consumption_tariff_intervals)

    def add_consumption_tariff_intervals(self, *consumption_tariff_intervals):
        for obj in consumption_tariff_intervals:
            if self not in obj._charges:
                obj._charges.append(self)
            self._consumption_tariff_intervals.append(obj)

    def remove_consumption_tariff_intervals(self, *consumption_tariff_intervals):
        for obj in consumption_tariff_intervals:
            if self in obj._charges:
                obj._charges.remove(self)
            self._consumption_tariff_intervals.remove(obj)
    # >>> consumption_tariff_intervals

    # <<< auxiliary_accounts
    # @generated
    def get_auxiliary_accounts(self):
        """ All auxiliary accounts to which this charge must be levied.
        """
        return self._auxiliary_accounts

    def set_auxiliary_accounts(self, value):
        for p in self._auxiliary_accounts:
            filtered = [q for q in p.charges if q != self]
            self._auxiliary_accounts._charges = filtered
        for r in value:
            if self not in r._charges:
                r._charges.append(self)
        self._auxiliary_accounts = value

    auxiliary_accounts = property(get_auxiliary_accounts, set_auxiliary_accounts)

    def add_auxiliary_accounts(self, *auxiliary_accounts):
        for obj in auxiliary_accounts:
            if self not in obj._charges:
                obj._charges.append(self)
            self._auxiliary_accounts.append(obj)

    def remove_auxiliary_accounts(self, *auxiliary_accounts):
        for obj in auxiliary_accounts:
            if self in obj._charges:
                obj._charges.remove(self)
            self._auxiliary_accounts.remove(obj)
    # >>> auxiliary_accounts

    # <<< time_tariff_intervals
    # @generated
    def get_time_tariff_intervals(self):
        """ Tariff intervals to which this time-based charge must be levied.
        """
        return self._time_tariff_intervals

    def set_time_tariff_intervals(self, value):
        for p in self._time_tariff_intervals:
            filtered = [q for q in p.charges if q != self]
            self._time_tariff_intervals._charges = filtered
        for r in value:
            if self not in r._charges:
                r._charges.append(self)
        self._time_tariff_intervals = value

    time_tariff_intervals = property(get_time_tariff_intervals, set_time_tariff_intervals)

    def add_time_tariff_intervals(self, *time_tariff_intervals):
        for obj in time_tariff_intervals:
            if self not in obj._charges:
                obj._charges.append(self)
            self._time_tariff_intervals.append(obj)

    def remove_time_tariff_intervals(self, *time_tariff_intervals):
        for obj in time_tariff_intervals:
            if self in obj._charges:
                obj._charges.remove(self)
            self._time_tariff_intervals.remove(obj)
    # >>> time_tariff_intervals

    # <<< parent_charge
    # @generated
    def get_parent_charge(self):
        """ 
        """
        return self._parent_charge

    def set_parent_charge(self, value):
        if self._parent_charge is not None:
            filtered = [x for x in self.parent_charge.child_charges if x != self]
            self._parent_charge._child_charges = filtered

        self._parent_charge = value
        if self._parent_charge is not None:
            self._parent_charge._child_charges.append(self)

    parent_charge = property(get_parent_charge, set_parent_charge)
    # >>> parent_charge

    # <<< child_charges
    # @generated
    def get_child_charges(self):
        """ All sub-components of this complex charge.
        """
        return self._child_charges

    def set_child_charges(self, value):
        for x in self._child_charges:
            x._parent_charge = None
        for y in value:
            y._parent_charge = self
        self._child_charges = value

    child_charges = property(get_child_charges, set_child_charges)

    def add_child_charges(self, *child_charges):
        for obj in child_charges:
            obj._parent_charge = self
            self._child_charges.append(obj)

    def remove_child_charges(self, *child_charges):
        for obj in child_charges:
            obj._parent_charge = None
            self._child_charges.remove(obj)
    # >>> child_charges

    # <<< fixed_portion
    # @generated
    # The fixed portion of this charge element.
    fixed_portion = None
    # >>> fixed_portion


    def __str__(self):
        """ Returns a string representation of the Charge.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< charge.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Charge.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Charge", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.consumption_tariff_intervals:
            s += '%s<%s:Charge.consumption_tariff_intervals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.auxiliary_accounts:
            s += '%s<%s:Charge.auxiliary_accounts rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.time_tariff_intervals:
            s += '%s<%s:Charge.time_tariff_intervals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.parent_charge is not None:
            s += '%s<%s:Charge.parent_charge rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent_charge.uri)
        for obj in self.child_charges:
            s += '%s<%s:Charge.child_charges rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.fixed_portion is not None:
            s += '%s<%s:Charge.fixed_portion rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.fixed_portion.uri)
        s += '%s<%s:Charge.kind>%s</%s:Charge.kind>' % \
            (indent, ns_prefix, self.kind, ns_prefix)
        s += '%s<%s:Charge.variable_portion>%s</%s:Charge.variable_portion>' % \
            (indent, ns_prefix, self.variable_portion, ns_prefix)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "Charge")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> charge.serialize


class ServiceSupplier(Organisation):
    """ Organisation that provides services to Customers.
    """
    # <<< service_supplier
    # @generated
    def __init__(self, kind='other', issuer_identification_number='', service_delivery_points=None, customer_agreements=None, bank_accounts=None, **kw_args):
        """ Initialises a new 'ServiceSupplier' instance.
        """
        # Kind of supplier. Values are: "other", "retailer", "utility"
        self.kind = 'other'

        # Unique transaction reference prefix number issued to an entity by the International Standards Organisation for the purpose of tagging onto electronic financial transactions, as defined in ISO/IEC 7812-1 and ISO/IEC 7812-2. 
        self.issuer_identification_number = issuer_identification_number


        self._service_delivery_points = []
        if service_delivery_points is not None:
            self.service_delivery_points = service_delivery_points
        else:
            self.service_delivery_points = []

        self._customer_agreements = []
        if customer_agreements is not None:
            self.customer_agreements = customer_agreements
        else:
            self.customer_agreements = []

        self._bank_accounts = []
        if bank_accounts is not None:
            self.bank_accounts = bank_accounts
        else:
            self.bank_accounts = []


        super(ServiceSupplier, self).__init__(**kw_args)
    # >>> service_supplier

    # <<< service_delivery_points
    # @generated
    def get_service_delivery_points(self):
        """ All service delivery points this service supplier utilises to deliver a service.
        """
        return self._service_delivery_points

    def set_service_delivery_points(self, value):
        for x in self._service_delivery_points:
            x._service_supplier = None
        for y in value:
            y._service_supplier = self
        self._service_delivery_points = value

    service_delivery_points = property(get_service_delivery_points, set_service_delivery_points)

    def add_service_delivery_points(self, *service_delivery_points):
        for obj in service_delivery_points:
            obj._service_supplier = self
            self._service_delivery_points.append(obj)

    def remove_service_delivery_points(self, *service_delivery_points):
        for obj in service_delivery_points:
            obj._service_supplier = None
            self._service_delivery_points.remove(obj)
    # >>> service_delivery_points

    # <<< customer_agreements
    # @generated
    def get_customer_agreements(self):
        """ All customer agreements of this service supplier.
        """
        return self._customer_agreements

    def set_customer_agreements(self, value):
        for x in self._customer_agreements:
            x._service_supplier = None
        for y in value:
            y._service_supplier = self
        self._customer_agreements = value

    customer_agreements = property(get_customer_agreements, set_customer_agreements)

    def add_customer_agreements(self, *customer_agreements):
        for obj in customer_agreements:
            obj._service_supplier = self
            self._customer_agreements.append(obj)

    def remove_customer_agreements(self, *customer_agreements):
        for obj in customer_agreements:
            obj._service_supplier = None
            self._customer_agreements.remove(obj)
    # >>> customer_agreements

    # <<< bank_accounts
    # @generated
    def get_bank_accounts(self):
        """ All BackAccounts this ServiceSupplier owns.
        """
        return self._bank_accounts

    def set_bank_accounts(self, value):
        for x in self._bank_accounts:
            x._service_supplier = None
        for y in value:
            y._service_supplier = self
        self._bank_accounts = value

    bank_accounts = property(get_bank_accounts, set_bank_accounts)

    def add_bank_accounts(self, *bank_accounts):
        for obj in bank_accounts:
            obj._service_supplier = self
            self._bank_accounts.append(obj)

    def remove_bank_accounts(self, *bank_accounts):
        for obj in bank_accounts:
            obj._service_supplier = None
            self._bank_accounts.remove(obj)
    # >>> bank_accounts


    def __str__(self):
        """ Returns a string representation of the ServiceSupplier.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< service_supplier.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the ServiceSupplier.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "ServiceSupplier", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.service_delivery_points:
            s += '%s<%s:ServiceSupplier.service_delivery_points rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.customer_agreements:
            s += '%s<%s:ServiceSupplier.customer_agreements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.bank_accounts:
            s += '%s<%s:ServiceSupplier.bank_accounts rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:ServiceSupplier.kind>%s</%s:ServiceSupplier.kind>' % \
            (indent, ns_prefix, self.kind, ns_prefix)
        s += '%s<%s:ServiceSupplier.issuer_identification_number>%s</%s:ServiceSupplier.issuer_identification_number>' % \
            (indent, ns_prefix, self.issuer_identification_number, ns_prefix)
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
        for obj in self.business_roles:
            s += '%s<%s:Organisation.business_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.telephone_numbers:
            s += '%s<%s:Organisation.telephone_numbers rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.street_address is not None:
            s += '%s<%s:Organisation.street_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.street_address.uri)
        for obj in self.market_roles:
            s += '%s<%s:Organisation.market_roles rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.postal_address is not None:
            s += '%s<%s:Organisation.postal_address rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.postal_address.uri)
        for obj in self.electronic_addresses:
            s += '%s<%s:Organisation.electronic_addresses rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "ServiceSupplier")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> service_supplier.serialize


class Receipt(IdentifiedObject):
    """ Record of total receipted payment from customer.
    """
    # <<< receipt
    # @generated
    def __init__(self, is_bankable=False, transactions=None, cashier_shift=None, vendor_shift=None, tenders=None, line=None, **kw_args):
        """ Initialises a new 'Receipt' instance.
        """
        # True if this receipted payment is manually bankable, otherwise it is an electronic funds transfer. 
        self.is_bankable = is_bankable


        self._transactions = []
        if transactions is not None:
            self.transactions = transactions
        else:
            self.transactions = []

        self._cashier_shift = None
        self.cashier_shift = cashier_shift

        self._vendor_shift = None
        self.vendor_shift = vendor_shift

        self._tenders = []
        if tenders is not None:
            self.tenders = tenders
        else:
            self.tenders = []

        self.line = line


        super(Receipt, self).__init__(**kw_args)
    # >>> receipt

    # <<< transactions
    # @generated
    def get_transactions(self):
        """ All transactions recorded for this receipted payment.
        """
        return self._transactions

    def set_transactions(self, value):
        for x in self._transactions:
            x._receipt = None
        for y in value:
            y._receipt = self
        self._transactions = value

    transactions = property(get_transactions, set_transactions)

    def add_transactions(self, *transactions):
        for obj in transactions:
            obj._receipt = self
            self._transactions.append(obj)

    def remove_transactions(self, *transactions):
        for obj in transactions:
            obj._receipt = None
            self._transactions.remove(obj)
    # >>> transactions

    # <<< cashier_shift
    # @generated
    def get_cashier_shift(self):
        """ Cashier shift during which this receipt was recorded.
        """
        return self._cashier_shift

    def set_cashier_shift(self, value):
        if self._cashier_shift is not None:
            filtered = [x for x in self.cashier_shift.receipts if x != self]
            self._cashier_shift._receipts = filtered

        self._cashier_shift = value
        if self._cashier_shift is not None:
            self._cashier_shift._receipts.append(self)

    cashier_shift = property(get_cashier_shift, set_cashier_shift)
    # >>> cashier_shift

    # <<< vendor_shift
    # @generated
    def get_vendor_shift(self):
        """ Vendor shift during which this receipt was recorded.
        """
        return self._vendor_shift

    def set_vendor_shift(self, value):
        if self._vendor_shift is not None:
            filtered = [x for x in self.vendor_shift.receipts if x != self]
            self._vendor_shift._receipts = filtered

        self._vendor_shift = value
        if self._vendor_shift is not None:
            self._vendor_shift._receipts.append(self)

    vendor_shift = property(get_vendor_shift, set_vendor_shift)
    # >>> vendor_shift

    # <<< tenders
    # @generated
    def get_tenders(self):
        """ All payments received in the form of tenders recorded by this receipt.
        """
        return self._tenders

    def set_tenders(self, value):
        for x in self._tenders:
            x._receipt = None
        for y in value:
            y._receipt = self
        self._tenders = value

    tenders = property(get_tenders, set_tenders)

    def add_tenders(self, *tenders):
        for obj in tenders:
            obj._receipt = self
            self._tenders.append(obj)

    def remove_tenders(self, *tenders):
        for obj in tenders:
            obj._receipt = None
            self._tenders.remove(obj)
    # >>> tenders

    # <<< line
    # @generated
    # Receipted amount with rounding, date and note.
    line = None
    # >>> line


    def __str__(self):
        """ Returns a string representation of the Receipt.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< receipt.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Receipt.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Receipt", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.transactions:
            s += '%s<%s:Receipt.transactions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.cashier_shift is not None:
            s += '%s<%s:Receipt.cashier_shift rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cashier_shift.uri)
        if self.vendor_shift is not None:
            s += '%s<%s:Receipt.vendor_shift rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.vendor_shift.uri)
        for obj in self.tenders:
            s += '%s<%s:Receipt.tenders rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.line is not None:
            s += '%s<%s:Receipt.line rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.line.uri)
        s += '%s<%s:Receipt.is_bankable>%s</%s:Receipt.is_bankable>' % \
            (indent, ns_prefix, self.is_bankable, ns_prefix)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "Receipt")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> receipt.serialize


class Tender(IdentifiedObject):
    """ Tender is what is 'offered' by the customer towards making a payment and is often more than the required payment (hence the need for 'change'). The payment is thus that part of the Tender that goes towards settlement of a particular transaction. Tender is modelled as an aggregation of Cheque and Card. Both these tender types can exist in a single tender bid thus 'accountHolderName' must exist separately in each of Cheque and Card as each could have a different account holder name.
    """
    # <<< tender
    # @generated
    def __init__(self, kind='cheque', amount=0.0, change=0.0, cheque=None, card=None, receipt=None, **kw_args):
        """ Initialises a new 'Tender' instance.
        """
        # Kind of tender from customer. Values are: "cheque", "card", "other", "unspecified", "cash"
        self.kind = 'cheque'

        # Amount tendered by customer. 
        self.amount = amount

        # Difference between amount tendered by customer and the amount charged by point of sale. 
        self.change = change


        self._cheque = None
        self.cheque = cheque

        self._card = None
        self.card = card

        self._receipt = None
        self.receipt = receipt


        super(Tender, self).__init__(**kw_args)
    # >>> tender

    # <<< cheque
    # @generated
    def get_cheque(self):
        """ Cheque used to tender payment.
        """
        return self._cheque

    def set_cheque(self, value):
        if self._cheque is not None:
            self._cheque._tender = None

        self._cheque = value
        if self._cheque is not None:
            self._cheque._tender = self

    cheque = property(get_cheque, set_cheque)
    # >>> cheque

    # <<< card
    # @generated
    def get_card(self):
        """ Card used to tender payment.
        """
        return self._card

    def set_card(self, value):
        if self._card is not None:
            self._card._tender = None

        self._card = value
        if self._card is not None:
            self._card._tender = self

    card = property(get_card, set_card)
    # >>> card

    # <<< receipt
    # @generated
    def get_receipt(self):
        """ Receipt that recorded this receiving of a payment in the form of tenders.
        """
        return self._receipt

    def set_receipt(self, value):
        if self._receipt is not None:
            filtered = [x for x in self.receipt.tenders if x != self]
            self._receipt._tenders = filtered

        self._receipt = value
        if self._receipt is not None:
            self._receipt._tenders.append(self)

    receipt = property(get_receipt, set_receipt)
    # >>> receipt


    def __str__(self):
        """ Returns a string representation of the Tender.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< tender.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Tender.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Tender", self.uri)
        if format:
            indent += ' ' * depth

        if self.cheque is not None:
            s += '%s<%s:Tender.cheque rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cheque.uri)
        if self.card is not None:
            s += '%s<%s:Tender.card rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.card.uri)
        if self.receipt is not None:
            s += '%s<%s:Tender.receipt rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.receipt.uri)
        s += '%s<%s:Tender.kind>%s</%s:Tender.kind>' % \
            (indent, ns_prefix, self.kind, ns_prefix)
        s += '%s<%s:Tender.amount>%s</%s:Tender.amount>' % \
            (indent, ns_prefix, self.amount, ns_prefix)
        s += '%s<%s:Tender.change>%s</%s:Tender.change>' % \
            (indent, ns_prefix, self.change, ns_prefix)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "Tender")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> tender.serialize


class PointOfSale(IdentifiedObject):
    """ Logical point where transactions take place with operational interaction between Cashier and the payment system; in certain cases PointOfSale interacts directly with the end customer, in which case Cashier might not be a real person: for example a self-service kiosk or over the internet.
    """
    # <<< point_of_sale
    # @generated
    def __init__(self, location='', vendor=None, tokens=None, cashier_shifts=None, **kw_args):
        """ Initialises a new 'PointOfSale' instance.
        """
        # Local description for where this point of sale is physically located. 
        self.location = location


        self._vendor = None
        self.vendor = vendor

        self._tokens = []
        if tokens is not None:
            self.tokens = tokens
        else:
            self.tokens = []

        self._cashier_shifts = []
        if cashier_shifts is not None:
            self.cashier_shifts = cashier_shifts
        else:
            self.cashier_shifts = []


        super(PointOfSale, self).__init__(**kw_args)
    # >>> point_of_sale

    # <<< vendor
    # @generated
    def get_vendor(self):
        """ Vendor that controls this PointOfSale.
        """
        return self._vendor

    def set_vendor(self, value):
        if self._vendor is not None:
            filtered = [x for x in self.vendor.point_of_sales if x != self]
            self._vendor._point_of_sales = filtered

        self._vendor = value
        if self._vendor is not None:
            self._vendor._point_of_sales.append(self)

    vendor = property(get_vendor, set_vendor)
    # >>> vendor

    # <<< tokens
    # @generated
    def get_tokens(self):
        """ All Tokens sold or dispensed at this PointOfSale.
        """
        return self._tokens

    def set_tokens(self, value):
        for x in self._tokens:
            x._point_of_sale = None
        for y in value:
            y._point_of_sale = self
        self._tokens = value

    tokens = property(get_tokens, set_tokens)

    def add_tokens(self, *tokens):
        for obj in tokens:
            obj._point_of_sale = self
            self._tokens.append(obj)

    def remove_tokens(self, *tokens):
        for obj in tokens:
            obj._point_of_sale = None
            self._tokens.remove(obj)
    # >>> tokens

    # <<< cashier_shifts
    # @generated
    def get_cashier_shifts(self):
        """ All shifts this point of sale operated in.
        """
        return self._cashier_shifts

    def set_cashier_shifts(self, value):
        for x in self._cashier_shifts:
            x._point_of_sale = None
        for y in value:
            y._point_of_sale = self
        self._cashier_shifts = value

    cashier_shifts = property(get_cashier_shifts, set_cashier_shifts)

    def add_cashier_shifts(self, *cashier_shifts):
        for obj in cashier_shifts:
            obj._point_of_sale = self
            self._cashier_shifts.append(obj)

    def remove_cashier_shifts(self, *cashier_shifts):
        for obj in cashier_shifts:
            obj._point_of_sale = None
            self._cashier_shifts.remove(obj)
    # >>> cashier_shifts


    def __str__(self):
        """ Returns a string representation of the PointOfSale.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< point_of_sale.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the PointOfSale.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "PointOfSale", self.uri)
        if format:
            indent += ' ' * depth

        if self.vendor is not None:
            s += '%s<%s:PointOfSale.vendor rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.vendor.uri)
        for obj in self.tokens:
            s += '%s<%s:PointOfSale.tokens rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.cashier_shifts:
            s += '%s<%s:PointOfSale.cashier_shifts rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:PointOfSale.location>%s</%s:PointOfSale.location>' % \
            (indent, ns_prefix, self.location, ns_prefix)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "PointOfSale")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> point_of_sale.serialize


class Transaction(IdentifiedObject):
    """ The record of details of payment for service or token sale.
    """
    # <<< transaction
    # @generated
    def __init__(self, kind='auxiliary_charge_payment', service_units_energy=0.0, service_units_error=0.0, reversed_id='', receiver_reference='', diverse_reference='', donor_reference='', vendor_shift=None, receipt=None, customer_account=None, meter_asset=None, user_attributes=None, auxiliary_account=None, pricing_structure=None, cashier_shift=None, line=None, **kw_args):
        """ Initialises a new 'Transaction' instance.
        """
        # Kind of transaction. Values are: "auxiliary_charge_payment", "token_exchange", "token_cancellation", "transaction_reversal", "diverse_payment", "token_free_issue", "other", "meter_configuration_token", "token_sale_payment", "account_payment", "tax_charge_payment", "service_charge_payment", "token_grant"
        self.kind = 'auxiliary_charge_payment'

        # Actual amount of service units that is being paid for. 
        self.service_units_energy = service_units_energy

        # Number of service units not reflected in 'serviceUnitsEnergy' due to process rounding or truncating errors. 
        self.service_units_error = service_units_error

        # (if 'kind' is transactionReversal) Reference to the original transaction that is being reversed by this transaction. 
        self.reversed_id = reversed_id

        # Reference to the entity that is the recipient of 'amount' (for example, supplier for service charge payment; or tax receiver for VAT). 
        self.receiver_reference = receiver_reference

        # Formal reference for use with diverse payment (traffic fine for example). 
        self.diverse_reference = diverse_reference

        # Reference to the entity that is the source of 'amount' (for example: customer for token purchase; or supplier for free issue token). 
        self.donor_reference = donor_reference


        self._vendor_shift = None
        self.vendor_shift = vendor_shift

        self._receipt = None
        self.receipt = receipt

        self._customer_account = None
        self.customer_account = customer_account

        self._meter_asset = None
        self.meter_asset = meter_asset

        self._user_attributes = []
        if user_attributes is not None:
            self.user_attributes = user_attributes
        else:
            self.user_attributes = []

        self._auxiliary_account = None
        self.auxiliary_account = auxiliary_account

        self._pricing_structure = None
        self.pricing_structure = pricing_structure

        self._cashier_shift = None
        self.cashier_shift = cashier_shift

        self.line = line


        super(Transaction, self).__init__(**kw_args)
    # >>> transaction

    # <<< vendor_shift
    # @generated
    def get_vendor_shift(self):
        """ Vendor shift during which this transaction was recorded.
        """
        return self._vendor_shift

    def set_vendor_shift(self, value):
        if self._vendor_shift is not None:
            filtered = [x for x in self.vendor_shift.transactions if x != self]
            self._vendor_shift._transactions = filtered

        self._vendor_shift = value
        if self._vendor_shift is not None:
            self._vendor_shift._transactions.append(self)

    vendor_shift = property(get_vendor_shift, set_vendor_shift)
    # >>> vendor_shift

    # <<< receipt
    # @generated
    def get_receipt(self):
        """ The receipted payment for which this transaction has been recorded.
        """
        return self._receipt

    def set_receipt(self, value):
        if self._receipt is not None:
            filtered = [x for x in self.receipt.transactions if x != self]
            self._receipt._transactions = filtered

        self._receipt = value
        if self._receipt is not None:
            self._receipt._transactions.append(self)

    receipt = property(get_receipt, set_receipt)
    # >>> receipt

    # <<< customer_account
    # @generated
    def get_customer_account(self):
        """ Customer account for this payment transaction.
        """
        return self._customer_account

    def set_customer_account(self, value):
        if self._customer_account is not None:
            filtered = [x for x in self.customer_account.payment_transactions if x != self]
            self._customer_account._payment_transactions = filtered

        self._customer_account = value
        if self._customer_account is not None:
            self._customer_account._payment_transactions.append(self)

    customer_account = property(get_customer_account, set_customer_account)
    # >>> customer_account

    # <<< meter_asset
    # @generated
    def get_meter_asset(self):
        """ Meter asset for this vending transaction.
        """
        return self._meter_asset

    def set_meter_asset(self, value):
        if self._meter_asset is not None:
            filtered = [x for x in self.meter_asset.vending_transactions if x != self]
            self._meter_asset._vending_transactions = filtered

        self._meter_asset = value
        if self._meter_asset is not None:
            self._meter_asset._vending_transactions.append(self)

    meter_asset = property(get_meter_asset, set_meter_asset)
    # >>> meter_asset

    # <<< user_attributes
    # @generated
    def get_user_attributes(self):
        """ All snapshots of meter parameters recorded at the time of this transaction. Use 'name' and 'value.value' attributes to specify name and value of a parameter from meter.
        """
        return self._user_attributes

    def set_user_attributes(self, value):
        for x in self._user_attributes:
            x._transaction = None
        for y in value:
            y._transaction = self
        self._user_attributes = value

    user_attributes = property(get_user_attributes, set_user_attributes)

    def add_user_attributes(self, *user_attributes):
        for obj in user_attributes:
            obj._transaction = self
            self._user_attributes.append(obj)

    def remove_user_attributes(self, *user_attributes):
        for obj in user_attributes:
            obj._transaction = None
            self._user_attributes.remove(obj)
    # >>> user_attributes

    # <<< auxiliary_account
    # @generated
    def get_auxiliary_account(self):
        """ Auxiliary account for this payment transaction.
        """
        return self._auxiliary_account

    def set_auxiliary_account(self, value):
        if self._auxiliary_account is not None:
            filtered = [x for x in self.auxiliary_account.payment_transactions if x != self]
            self._auxiliary_account._payment_transactions = filtered

        self._auxiliary_account = value
        if self._auxiliary_account is not None:
            self._auxiliary_account._payment_transactions.append(self)

    auxiliary_account = property(get_auxiliary_account, set_auxiliary_account)
    # >>> auxiliary_account

    # <<< pricing_structure
    # @generated
    def get_pricing_structure(self):
        """ Pricing structure applicable for this transaction.
        """
        return self._pricing_structure

    def set_pricing_structure(self, value):
        if self._pricing_structure is not None:
            filtered = [x for x in self.pricing_structure.transactions if x != self]
            self._pricing_structure._transactions = filtered

        self._pricing_structure = value
        if self._pricing_structure is not None:
            self._pricing_structure._transactions.append(self)

    pricing_structure = property(get_pricing_structure, set_pricing_structure)
    # >>> pricing_structure

    # <<< cashier_shift
    # @generated
    def get_cashier_shift(self):
        """ Cashier shift during which this transaction was recorded.
        """
        return self._cashier_shift

    def set_cashier_shift(self, value):
        if self._cashier_shift is not None:
            filtered = [x for x in self.cashier_shift.transactions if x != self]
            self._cashier_shift._transactions = filtered

        self._cashier_shift = value
        if self._cashier_shift is not None:
            self._cashier_shift._transactions.append(self)

    cashier_shift = property(get_cashier_shift, set_cashier_shift)
    # >>> cashier_shift

    # <<< line
    # @generated
    # Transaction amount, rounding, date and note for this transaction line.
    line = None
    # >>> line


    def __str__(self):
        """ Returns a string representation of the Transaction.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< transaction.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Transaction.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Transaction", self.uri)
        if format:
            indent += ' ' * depth

        if self.vendor_shift is not None:
            s += '%s<%s:Transaction.vendor_shift rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.vendor_shift.uri)
        if self.receipt is not None:
            s += '%s<%s:Transaction.receipt rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.receipt.uri)
        if self.customer_account is not None:
            s += '%s<%s:Transaction.customer_account rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.customer_account.uri)
        if self.meter_asset is not None:
            s += '%s<%s:Transaction.meter_asset rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.meter_asset.uri)
        for obj in self.user_attributes:
            s += '%s<%s:Transaction.user_attributes rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.auxiliary_account is not None:
            s += '%s<%s:Transaction.auxiliary_account rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.auxiliary_account.uri)
        if self.pricing_structure is not None:
            s += '%s<%s:Transaction.pricing_structure rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.pricing_structure.uri)
        if self.cashier_shift is not None:
            s += '%s<%s:Transaction.cashier_shift rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cashier_shift.uri)
        if self.line is not None:
            s += '%s<%s:Transaction.line rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.line.uri)
        s += '%s<%s:Transaction.kind>%s</%s:Transaction.kind>' % \
            (indent, ns_prefix, self.kind, ns_prefix)
        s += '%s<%s:Transaction.service_units_energy>%s</%s:Transaction.service_units_energy>' % \
            (indent, ns_prefix, self.service_units_energy, ns_prefix)
        s += '%s<%s:Transaction.service_units_error>%s</%s:Transaction.service_units_error>' % \
            (indent, ns_prefix, self.service_units_error, ns_prefix)
        s += '%s<%s:Transaction.reversed_id>%s</%s:Transaction.reversed_id>' % \
            (indent, ns_prefix, self.reversed_id, ns_prefix)
        s += '%s<%s:Transaction.receiver_reference>%s</%s:Transaction.receiver_reference>' % \
            (indent, ns_prefix, self.receiver_reference, ns_prefix)
        s += '%s<%s:Transaction.diverse_reference>%s</%s:Transaction.diverse_reference>' % \
            (indent, ns_prefix, self.diverse_reference, ns_prefix)
        s += '%s<%s:Transaction.donor_reference>%s</%s:Transaction.donor_reference>' % \
            (indent, ns_prefix, self.donor_reference, ns_prefix)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "Transaction")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> transaction.serialize


class Transactor(IdentifiedObject):
    """ The entity that ultimately executes the transaction and who is in control of the process; typically this is embodied in secure software running on a server that may employ secure hardware encryption devices for secure transaction processing.
    """
    # <<< transactor
    # @generated
    def __init__(self, merchant_accounts=None, **kw_args):
        """ Initialises a new 'Transactor' instance.
        """

        self._merchant_accounts = []
        if merchant_accounts is not None:
            self.merchant_accounts = merchant_accounts
        else:
            self.merchant_accounts = []


        super(Transactor, self).__init__(**kw_args)
    # >>> transactor

    # <<< merchant_accounts
    # @generated
    def get_merchant_accounts(self):
        """ All merchant accounts registered with this transactor.
        """
        return self._merchant_accounts

    def set_merchant_accounts(self, value):
        for p in self._merchant_accounts:
            filtered = [q for q in p.transactors if q != self]
            self._merchant_accounts._transactors = filtered
        for r in value:
            if self not in r._transactors:
                r._transactors.append(self)
        self._merchant_accounts = value

    merchant_accounts = property(get_merchant_accounts, set_merchant_accounts)

    def add_merchant_accounts(self, *merchant_accounts):
        for obj in merchant_accounts:
            if self not in obj._transactors:
                obj._transactors.append(self)
            self._merchant_accounts.append(obj)

    def remove_merchant_accounts(self, *merchant_accounts):
        for obj in merchant_accounts:
            if self in obj._transactors:
                obj._transactors.remove(self)
            self._merchant_accounts.remove(obj)
    # >>> merchant_accounts


    def __str__(self):
        """ Returns a string representation of the Transactor.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< transactor.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Transactor.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Transactor", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.merchant_accounts:
            s += '%s<%s:Transactor.merchant_accounts rdf:resource="#%s"/>' % \
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "Transactor")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> transactor.serialize


class AccountingUnit(Element):
    """ Unit for accounting; use either 'energyUnit' or 'currencyUnit' to specify the unit for 'value'.
    """
    # <<< accounting_unit
    # @generated
    def __init__(self, monetary_unit='eur', multiplier='m', energy_unit=0.0, value=0.0, **kw_args):
        """ Initialises a new 'AccountingUnit' instance.
        """
        # Unit of currency. Values are: "eur", "other", "jpy", "dkk", "nok", "cny", "usd", "inr", "sek", "aud", "chf", "cad", "rur", "gbp"
        self.monetary_unit = 'eur'

        # Multiplier for the 'energyUnit' or 'monetaryUnit'. Values are: "m", "t", "p", "k", "m", "micro", "n", "d", "g", "c", "none"
        self.multiplier = 'm'

        # Unit of service. 
        self.energy_unit = energy_unit

        # Value expressed in applicable units. 
        self.value = value



        super(AccountingUnit, self).__init__(**kw_args)
    # >>> accounting_unit


    def __str__(self):
        """ Returns a string representation of the AccountingUnit.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< accounting_unit.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the AccountingUnit.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "AccountingUnit", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:AccountingUnit.monetary_unit>%s</%s:AccountingUnit.monetary_unit>' % \
            (indent, ns_prefix, self.monetary_unit, ns_prefix)
        s += '%s<%s:AccountingUnit.multiplier>%s</%s:AccountingUnit.multiplier>' % \
            (indent, ns_prefix, self.multiplier, ns_prefix)
        s += '%s<%s:AccountingUnit.energy_unit>%s</%s:AccountingUnit.energy_unit>' % \
            (indent, ns_prefix, self.energy_unit, ns_prefix)
        s += '%s<%s:AccountingUnit.value>%s</%s:AccountingUnit.value>' % \
            (indent, ns_prefix, self.value, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "AccountingUnit")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> accounting_unit.serialize


class TariffProfile(Document):
    """ A schedule of charges; structure associated with Tariff that allows the definition of complex tarif structures such as step and time of use when used in conjunction with TimeTariffInterval and Charge. Inherited 'status.value' is defined in the context of the utility's business rules, for example: active, inactive, etc.
    """
    # <<< tariff_profile
    # @generated
    def __init__(self, tariff_cycle='', consumption_tariff_intervals=None, tariffs=None, time_tariff_intervals=None, **kw_args):
        """ Initialises a new 'TariffProfile' instance.
        """
        # The frequency at which the tariff charge schedule is repeated Examples are: once off on a specified date and time; hourly; daily; weekly; monthly; 3-monthly; 6-monthly; 12-monthly; etc. At the end of each cycle, the business rules are reset to start from the beginning again. 
        self.tariff_cycle = tariff_cycle


        self._consumption_tariff_intervals = []
        if consumption_tariff_intervals is not None:
            self.consumption_tariff_intervals = consumption_tariff_intervals
        else:
            self.consumption_tariff_intervals = []

        self._tariffs = []
        if tariffs is not None:
            self.tariffs = tariffs
        else:
            self.tariffs = []

        self._time_tariff_intervals = []
        if time_tariff_intervals is not None:
            self.time_tariff_intervals = time_tariff_intervals
        else:
            self.time_tariff_intervals = []


        super(TariffProfile, self).__init__(**kw_args)
    # >>> tariff_profile

    # <<< consumption_tariff_intervals
    # @generated
    def get_consumption_tariff_intervals(self):
        """ All consumption tariff intervals used to define this tariff profile.
        """
        return self._consumption_tariff_intervals

    def set_consumption_tariff_intervals(self, value):
        for p in self._consumption_tariff_intervals:
            filtered = [q for q in p.tariff_profiles if q != self]
            self._consumption_tariff_intervals._tariff_profiles = filtered
        for r in value:
            if self not in r._tariff_profiles:
                r._tariff_profiles.append(self)
        self._consumption_tariff_intervals = value

    consumption_tariff_intervals = property(get_consumption_tariff_intervals, set_consumption_tariff_intervals)

    def add_consumption_tariff_intervals(self, *consumption_tariff_intervals):
        for obj in consumption_tariff_intervals:
            if self not in obj._tariff_profiles:
                obj._tariff_profiles.append(self)
            self._consumption_tariff_intervals.append(obj)

    def remove_consumption_tariff_intervals(self, *consumption_tariff_intervals):
        for obj in consumption_tariff_intervals:
            if self in obj._tariff_profiles:
                obj._tariff_profiles.remove(self)
            self._consumption_tariff_intervals.remove(obj)
    # >>> consumption_tariff_intervals

    # <<< tariffs
    # @generated
    def get_tariffs(self):
        """ All tariffs defined by this tariff profile.
        """
        return self._tariffs

    def set_tariffs(self, value):
        for p in self._tariffs:
            filtered = [q for q in p.tariff_profiles if q != self]
            self._tariffs._tariff_profiles = filtered
        for r in value:
            if self not in r._tariff_profiles:
                r._tariff_profiles.append(self)
        self._tariffs = value

    tariffs = property(get_tariffs, set_tariffs)

    def add_tariffs(self, *tariffs):
        for obj in tariffs:
            if self not in obj._tariff_profiles:
                obj._tariff_profiles.append(self)
            self._tariffs.append(obj)

    def remove_tariffs(self, *tariffs):
        for obj in tariffs:
            if self in obj._tariff_profiles:
                obj._tariff_profiles.remove(self)
            self._tariffs.remove(obj)
    # >>> tariffs

    # <<< time_tariff_intervals
    # @generated
    def get_time_tariff_intervals(self):
        """ All time tariff intervals used to define this tariff profile.
        """
        return self._time_tariff_intervals

    def set_time_tariff_intervals(self, value):
        for p in self._time_tariff_intervals:
            filtered = [q for q in p.tariff_profiles if q != self]
            self._time_tariff_intervals._tariff_profiles = filtered
        for r in value:
            if self not in r._tariff_profiles:
                r._tariff_profiles.append(self)
        self._time_tariff_intervals = value

    time_tariff_intervals = property(get_time_tariff_intervals, set_time_tariff_intervals)

    def add_time_tariff_intervals(self, *time_tariff_intervals):
        for obj in time_tariff_intervals:
            if self not in obj._tariff_profiles:
                obj._tariff_profiles.append(self)
            self._time_tariff_intervals.append(obj)

    def remove_time_tariff_intervals(self, *time_tariff_intervals):
        for obj in time_tariff_intervals:
            if self in obj._tariff_profiles:
                obj._tariff_profiles.remove(self)
            self._time_tariff_intervals.remove(obj)
    # >>> time_tariff_intervals


    def __str__(self):
        """ Returns a string representation of the TariffProfile.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< tariff_profile.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the TariffProfile.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "TariffProfile", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.consumption_tariff_intervals:
            s += '%s<%s:TariffProfile.consumption_tariff_intervals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.tariffs:
            s += '%s<%s:TariffProfile.tariffs rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.time_tariff_intervals:
            s += '%s<%s:TariffProfile.time_tariff_intervals rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:TariffProfile.tariff_cycle>%s</%s:TariffProfile.tariff_cycle>' % \
            (indent, ns_prefix, self.tariff_cycle, ns_prefix)
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "TariffProfile")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> tariff_profile.serialize


class LineDetail(Element):
    """ Details on an amount line, with rounding, date and note.
    """
    # <<< line_detail
    # @generated
    def __init__(self, amount=0.0, rounding=0.0, note='', date_time='', **kw_args):
        """ Initialises a new 'LineDetail' instance.
        """
        # Amount for this line item. 
        self.amount = amount

        # Totalised monetary value of all errors due to process rounding or truncating that is not reflected in 'amount'. 
        self.rounding = rounding

        # Free format note relevant to this line. 
        self.note = note

        # Date and time when this line was created in the application process. 
        self.date_time = date_time



        super(LineDetail, self).__init__(**kw_args)
    # >>> line_detail


    def __str__(self):
        """ Returns a string representation of the LineDetail.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< line_detail.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the LineDetail.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "LineDetail", self.uri)
        if format:
            indent += ' ' * depth

        s += '%s<%s:LineDetail.amount>%s</%s:LineDetail.amount>' % \
            (indent, ns_prefix, self.amount, ns_prefix)
        s += '%s<%s:LineDetail.rounding>%s</%s:LineDetail.rounding>' % \
            (indent, ns_prefix, self.rounding, ns_prefix)
        s += '%s<%s:LineDetail.note>%s</%s:LineDetail.note>' % \
            (indent, ns_prefix, self.note, ns_prefix)
        s += '%s<%s:LineDetail.date_time>%s</%s:LineDetail.date_time>' % \
            (indent, ns_prefix, self.date_time, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "LineDetail")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> line_detail.serialize


class AuxiliaryAgreement(Agreement):
    """ An ad-hoc auxiliary account agreement associated with a customer agreement, not part of the customer's account, but typically subject to formal agreement between customer and supplier (utility). Typically this is used to collect revenue owing by the customer for other services or arrears accrued with the utility for other services. It is typically linked to a prepaid token purchase transaction, thus forcing the customer to make a payment towards settlement of the auxiliary account balance whenever he needs to purchase a prepaid token for electricity. The present status of AuxiliaryAgreement can be defined in the context of the utility's business rules, for example: enabled, disabled, pending, over recovered, under recovered, written off, etc.
    """
    # <<< auxiliary_agreement
    # @generated
    def __init__(self, aux_priority_code='', fixed_amount=0.0, pay_cycle='', vend_portion=0.0, vend_portion_arrear=0.0, min_amount=0.0, aux_cycle='', aux_ref='', sub_category='', arrears_interest=0.0, customer_agreement=None, auxiliary_accounts=None, **kw_args):
        """ Initialises a new 'AuxiliaryAgreement' instance.
        """
        # The coded priority indicating the priority that this AuxiliaryAgreement has above other AuxiliaryAgreements (associated with the same customer agreement) when it comes to competing for settlement from a payment transaction or token purchase. 
        self.aux_priority_code = aux_priority_code

        # The fixed amount that must be collected from each vending transaction towards settlement of this AuxiliaryAgreement. Note that there may be multiple tokens vended per vending transaction, but this is not relevant. 
        self.fixed_amount = fixed_amount

        # The contractually expected payment frequency (by the customer). Examples are: ad-hoc; on specified date; hourly, daily, weekly, monthly. etc. 
        self.pay_cycle = pay_cycle

        # The percentage of the transaction amount that must be collected from each vending transaction towards settlement of this AuxiliaryAgreement when payments are not in arrears. Note that there may be multiple tokens vended per vending transaction, but this is not relevant. 
        self.vend_portion = vend_portion

        # The percentage of the transaction amount that must be collected from each vending transaction towards settlement of this AuxiliaryAgreement when payments are in arrears. Note that there may be multiple tokens vended per vending transaction, but this is not relevant. 
        self.vend_portion_arrear = vend_portion_arrear

        # The minimum amount that must be paid at any transaction towards settling this AuxiliryAgreement or reducing the balance. 
        self.min_amount = min_amount

        # The frequency for automatically recurring auxiliary charges, where AuxiliaryAccount.initialCharge is recursively added to AuxiliaryAccount.dueCurrent at the start of each auxCycle. For example: on a specified date and time; hourly; daily; weekly; monthly; 3-monthly; 6-monthly; 12-monthly; etc. 
        self.aux_cycle = aux_cycle

        # A local reference to this AuxiliaryAgreement defined in the context of the implementation and not related to IdentifiedObject.mRID. 
        self.aux_ref = aux_ref

        # Sub-category of this AuxiliaryAgreement as sub-classification of the inherited 'category'. 
        self.sub_category = sub_category

        # The interest per annum to be charged prorata on AuxiliaryAccount.dueArrears at the end of each payCycle. 
        self.arrears_interest = arrears_interest


        self._customer_agreement = None
        self.customer_agreement = customer_agreement

        self._auxiliary_accounts = []
        if auxiliary_accounts is not None:
            self.auxiliary_accounts = auxiliary_accounts
        else:
            self.auxiliary_accounts = []


        super(AuxiliaryAgreement, self).__init__(**kw_args)
    # >>> auxiliary_agreement

    # <<< customer_agreement
    # @generated
    def get_customer_agreement(self):
        """ Customer agreement this (non-service related) auxiliary agreement refers to.
        """
        return self._customer_agreement

    def set_customer_agreement(self, value):
        if self._customer_agreement is not None:
            filtered = [x for x in self.customer_agreement.auxiliary_agreements if x != self]
            self._customer_agreement._auxiliary_agreements = filtered

        self._customer_agreement = value
        if self._customer_agreement is not None:
            self._customer_agreement._auxiliary_agreements.append(self)

    customer_agreement = property(get_customer_agreement, set_customer_agreement)
    # >>> customer_agreement

    # <<< auxiliary_accounts
    # @generated
    def get_auxiliary_accounts(self):
        """ All auxiliary accounts regulated by this agreement.
        """
        return self._auxiliary_accounts

    def set_auxiliary_accounts(self, value):
        for x in self._auxiliary_accounts:
            x._auxiliary_agreement = None
        for y in value:
            y._auxiliary_agreement = self
        self._auxiliary_accounts = value

    auxiliary_accounts = property(get_auxiliary_accounts, set_auxiliary_accounts)

    def add_auxiliary_accounts(self, *auxiliary_accounts):
        for obj in auxiliary_accounts:
            obj._auxiliary_agreement = self
            self._auxiliary_accounts.append(obj)

    def remove_auxiliary_accounts(self, *auxiliary_accounts):
        for obj in auxiliary_accounts:
            obj._auxiliary_agreement = None
            self._auxiliary_accounts.remove(obj)
    # >>> auxiliary_accounts


    def __str__(self):
        """ Returns a string representation of the AuxiliaryAgreement.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< auxiliary_agreement.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the AuxiliaryAgreement.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "AuxiliaryAgreement", self.uri)
        if format:
            indent += ' ' * depth

        if self.customer_agreement is not None:
            s += '%s<%s:AuxiliaryAgreement.customer_agreement rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.customer_agreement.uri)
        for obj in self.auxiliary_accounts:
            s += '%s<%s:AuxiliaryAgreement.auxiliary_accounts rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:AuxiliaryAgreement.aux_priority_code>%s</%s:AuxiliaryAgreement.aux_priority_code>' % \
            (indent, ns_prefix, self.aux_priority_code, ns_prefix)
        s += '%s<%s:AuxiliaryAgreement.fixed_amount>%s</%s:AuxiliaryAgreement.fixed_amount>' % \
            (indent, ns_prefix, self.fixed_amount, ns_prefix)
        s += '%s<%s:AuxiliaryAgreement.pay_cycle>%s</%s:AuxiliaryAgreement.pay_cycle>' % \
            (indent, ns_prefix, self.pay_cycle, ns_prefix)
        s += '%s<%s:AuxiliaryAgreement.vend_portion>%s</%s:AuxiliaryAgreement.vend_portion>' % \
            (indent, ns_prefix, self.vend_portion, ns_prefix)
        s += '%s<%s:AuxiliaryAgreement.vend_portion_arrear>%s</%s:AuxiliaryAgreement.vend_portion_arrear>' % \
            (indent, ns_prefix, self.vend_portion_arrear, ns_prefix)
        s += '%s<%s:AuxiliaryAgreement.min_amount>%s</%s:AuxiliaryAgreement.min_amount>' % \
            (indent, ns_prefix, self.min_amount, ns_prefix)
        s += '%s<%s:AuxiliaryAgreement.aux_cycle>%s</%s:AuxiliaryAgreement.aux_cycle>' % \
            (indent, ns_prefix, self.aux_cycle, ns_prefix)
        s += '%s<%s:AuxiliaryAgreement.aux_ref>%s</%s:AuxiliaryAgreement.aux_ref>' % \
            (indent, ns_prefix, self.aux_ref, ns_prefix)
        s += '%s<%s:AuxiliaryAgreement.sub_category>%s</%s:AuxiliaryAgreement.sub_category>' % \
            (indent, ns_prefix, self.sub_category, ns_prefix)
        s += '%s<%s:AuxiliaryAgreement.arrears_interest>%s</%s:AuxiliaryAgreement.arrears_interest>' % \
            (indent, ns_prefix, self.arrears_interest, ns_prefix)
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
        if self.validity_interval is not None:
            s += '%s<%s:Agreement.validity_interval rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.validity_interval.uri)
        s += '%s<%s:Agreement.sign_date>%s</%s:Agreement.sign_date>' % \
            (indent, ns_prefix, self.sign_date, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "AuxiliaryAgreement")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> auxiliary_agreement.serialize


class Card(Element):
    """ Documentation of the tender when it is a type of card (credit, debit, etc).
    """
    # <<< card
    # @generated
    def __init__(self, pan='', expiry_date='', account_holder_name='', cv_number='', tender=None, **kw_args):
        """ Initialises a new 'Card' instance.
        """
        # The primary account number. 
        self.pan = pan

        # The date when this card expires. 
        self.expiry_date = expiry_date

        # Name of account holder. 
        self.account_holder_name = account_holder_name

        # The card verification number. 
        self.cv_number = cv_number


        self._tender = None
        self.tender = tender


        super(Card, self).__init__(**kw_args)
    # >>> card

    # <<< tender
    # @generated
    def get_tender(self):
        """ Payment tender this card is being used for.
        """
        return self._tender

    def set_tender(self, value):
        if self._tender is not None:
            self._tender._card = None

        self._tender = value
        if self._tender is not None:
            self._tender._card = self

    tender = property(get_tender, set_tender)
    # >>> tender


    def __str__(self):
        """ Returns a string representation of the Card.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< card.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Card.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Card", self.uri)
        if format:
            indent += ' ' * depth

        if self.tender is not None:
            s += '%s<%s:Card.tender rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.tender.uri)
        s += '%s<%s:Card.pan>%s</%s:Card.pan>' % \
            (indent, ns_prefix, self.pan, ns_prefix)
        s += '%s<%s:Card.expiry_date>%s</%s:Card.expiry_date>' % \
            (indent, ns_prefix, self.expiry_date, ns_prefix)
        s += '%s<%s:Card.account_holder_name>%s</%s:Card.account_holder_name>' % \
            (indent, ns_prefix, self.account_holder_name, ns_prefix)
        s += '%s<%s:Card.cv_number>%s</%s:Card.cv_number>' % \
            (indent, ns_prefix, self.cv_number, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Card")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> card.serialize


class Vendor(IdentifiedObject):
    """ The entity that owns PointOfSale and contracts with Cashier to receipt payments and vend tokens using the payment system. Vendor has a private contract with and is managed by Merchant who is a type of Organisation. Vendor is accountable to Merchant for revenue collected, who is in turn accountable to Supplier.
    """
    # <<< vendor
    # @generated
    def __init__(self, point_of_sales=None, bank_statements=None, cashiers=None, merchant_account=None, vendor_shifts=None, **kw_args):
        """ Initialises a new 'Vendor' instance.
        """

        self._point_of_sales = []
        if point_of_sales is not None:
            self.point_of_sales = point_of_sales
        else:
            self.point_of_sales = []

        self._bank_statements = []
        if bank_statements is not None:
            self.bank_statements = bank_statements
        else:
            self.bank_statements = []

        self._cashiers = []
        if cashiers is not None:
            self.cashiers = cashiers
        else:
            self.cashiers = []

        self._merchant_account = None
        self.merchant_account = merchant_account

        self._vendor_shifts = []
        if vendor_shifts is not None:
            self.vendor_shifts = vendor_shifts
        else:
            self.vendor_shifts = []


        super(Vendor, self).__init__(**kw_args)
    # >>> vendor

    # <<< point_of_sales
    # @generated
    def get_point_of_sales(self):
        """ All points of sale this Vendor controls.
        """
        return self._point_of_sales

    def set_point_of_sales(self, value):
        for x in self._point_of_sales:
            x._vendor = None
        for y in value:
            y._vendor = self
        self._point_of_sales = value

    point_of_sales = property(get_point_of_sales, set_point_of_sales)

    def add_point_of_sales(self, *point_of_sales):
        for obj in point_of_sales:
            obj._vendor = self
            self._point_of_sales.append(obj)

    def remove_point_of_sales(self, *point_of_sales):
        for obj in point_of_sales:
            obj._vendor = None
            self._point_of_sales.remove(obj)
    # >>> point_of_sales

    # <<< bank_statements
    # @generated
    def get_bank_statements(self):
        """ All BankStatements reflecting deposits made by this Vendor.
        """
        return self._bank_statements

    def set_bank_statements(self, value):
        for x in self._bank_statements:
            x._vendor = None
        for y in value:
            y._vendor = self
        self._bank_statements = value

    bank_statements = property(get_bank_statements, set_bank_statements)

    def add_bank_statements(self, *bank_statements):
        for obj in bank_statements:
            obj._vendor = self
            self._bank_statements.append(obj)

    def remove_bank_statements(self, *bank_statements):
        for obj in bank_statements:
            obj._vendor = None
            self._bank_statements.remove(obj)
    # >>> bank_statements

    # <<< cashiers
    # @generated
    def get_cashiers(self):
        """ All Cachiers managed by this Vendor.
        """
        return self._cashiers

    def set_cashiers(self, value):
        for x in self._cashiers:
            x._vendor = None
        for y in value:
            y._vendor = self
        self._cashiers = value

    cashiers = property(get_cashiers, set_cashiers)

    def add_cashiers(self, *cashiers):
        for obj in cashiers:
            obj._vendor = self
            self._cashiers.append(obj)

    def remove_cashiers(self, *cashiers):
        for obj in cashiers:
            obj._vendor = None
            self._cashiers.remove(obj)
    # >>> cashiers

    # <<< merchant_account
    # @generated
    def get_merchant_account(self):
        """ Merchant account against which this vendor sells tokens or recept payments.
        """
        return self._merchant_account

    def set_merchant_account(self, value):
        if self._merchant_account is not None:
            filtered = [x for x in self.merchant_account.vendors if x != self]
            self._merchant_account._vendors = filtered

        self._merchant_account = value
        if self._merchant_account is not None:
            self._merchant_account._vendors.append(self)

    merchant_account = property(get_merchant_account, set_merchant_account)
    # >>> merchant_account

    # <<< vendor_shifts
    # @generated
    def get_vendor_shifts(self):
        """ All vendor shifts opened and owned by this vendor.
        """
        return self._vendor_shifts

    def set_vendor_shifts(self, value):
        for x in self._vendor_shifts:
            x._vendor = None
        for y in value:
            y._vendor = self
        self._vendor_shifts = value

    vendor_shifts = property(get_vendor_shifts, set_vendor_shifts)

    def add_vendor_shifts(self, *vendor_shifts):
        for obj in vendor_shifts:
            obj._vendor = self
            self._vendor_shifts.append(obj)

    def remove_vendor_shifts(self, *vendor_shifts):
        for obj in vendor_shifts:
            obj._vendor = None
            self._vendor_shifts.remove(obj)
    # >>> vendor_shifts


    def __str__(self):
        """ Returns a string representation of the Vendor.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< vendor.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Vendor.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Vendor", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.point_of_sales:
            s += '%s<%s:Vendor.point_of_sales rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.bank_statements:
            s += '%s<%s:Vendor.bank_statements rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.cashiers:
            s += '%s<%s:Vendor.cashiers rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.merchant_account is not None:
            s += '%s<%s:Vendor.merchant_account rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.merchant_account.uri)
        for obj in self.vendor_shifts:
            s += '%s<%s:Vendor.vendor_shifts rdf:resource="#%s"/>' % \
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
        s += '%s</%s:%s>' % (indent, ns_prefix, "Vendor")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> vendor.serialize


class Cheque(Element):
    """ The actual tender when it is a type of cheque.
    """
    # <<< cheque
    # @generated
    def __init__(self, kind='bank_order', micr_number='', cheque_number='', date='', tender=None, bank_account_detail=None, **kw_args):
        """ Initialises a new 'Cheque' instance.
        """
        # Kind of cheque. Values are: "bank_order", "postal_order", "other"
        self.kind = 'bank_order'

        # The magnetic ink character recognition number printed on the cheque. 
        self.micr_number = micr_number

        # Cheque reference number as printed on the cheque. 
        self.cheque_number = cheque_number

        # Date when cheque becomes valid. 
        self.date = date


        self._tender = None
        self.tender = tender

        self.bank_account_detail = bank_account_detail


        super(Cheque, self).__init__(**kw_args)
    # >>> cheque

    # <<< tender
    # @generated
    def get_tender(self):
        """ Payment tender the cheque is being used for.
        """
        return self._tender

    def set_tender(self, value):
        if self._tender is not None:
            self._tender._cheque = None

        self._tender = value
        if self._tender is not None:
            self._tender._cheque = self

    tender = property(get_tender, set_tender)
    # >>> tender

    # <<< bank_account_detail
    # @generated
    # Details of the account holder and bank.
    bank_account_detail = None
    # >>> bank_account_detail


    def __str__(self):
        """ Returns a string representation of the Cheque.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< cheque.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the Cheque.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "Cheque", self.uri)
        if format:
            indent += ' ' * depth

        if self.tender is not None:
            s += '%s<%s:Cheque.tender rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.tender.uri)
        if self.bank_account_detail is not None:
            s += '%s<%s:Cheque.bank_account_detail rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.bank_account_detail.uri)
        s += '%s<%s:Cheque.kind>%s</%s:Cheque.kind>' % \
            (indent, ns_prefix, self.kind, ns_prefix)
        s += '%s<%s:Cheque.micr_number>%s</%s:Cheque.micr_number>' % \
            (indent, ns_prefix, self.micr_number, ns_prefix)
        s += '%s<%s:Cheque.cheque_number>%s</%s:Cheque.cheque_number>' % \
            (indent, ns_prefix, self.cheque_number, ns_prefix)
        s += '%s<%s:Cheque.date>%s</%s:Cheque.date>' % \
            (indent, ns_prefix, self.date, ns_prefix)
        if self.parent is not None:
            s += '%s<%s:Element.parent rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.parent.uri)
        s += '%s<%s:Element.uuid>%s</%s:Element.uuid>' % \
            (indent, ns_prefix, self.uuid, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "Cheque")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> cheque.serialize


class VendorShift(Shift):
    """ The operating shift for a vendor during which he may transact against the merchant's account. It aggregates transactions and receipts during the shift and periodically debits a merchant account. The totals in VendorShift should always = sum of totals aggregated in all cashier shifts that were open under the particular vendor shift.
    """
    # <<< vendor_shift
    # @generated
    def __init__(self, posted=False, merchant_debit_amount=0.0, transactions=None, receipts=None, merchant_account=None, vendor=None, **kw_args):
        """ Initialises a new 'VendorShift' instance.
        """
        # = true if merchantDebitAmount has been debited from MerchantAccount; typically happens at the end of VendorShift when it closes. 
        self.posted = posted

        # The amount that is to be debited from the merchant account for this vendor shift. This amount reflects the sum(PaymentTransaction.transactionAmount). 
        self.merchant_debit_amount = merchant_debit_amount


        self._transactions = []
        if transactions is not None:
            self.transactions = transactions
        else:
            self.transactions = []

        self._receipts = []
        if receipts is not None:
            self.receipts = receipts
        else:
            self.receipts = []

        self._merchant_account = None
        self.merchant_account = merchant_account

        self._vendor = None
        self.vendor = vendor


        super(VendorShift, self).__init__(**kw_args)
    # >>> vendor_shift

    # <<< transactions
    # @generated
    def get_transactions(self):
        """ 
        """
        return self._transactions

    def set_transactions(self, value):
        for x in self._transactions:
            x._vendor_shift = None
        for y in value:
            y._vendor_shift = self
        self._transactions = value

    transactions = property(get_transactions, set_transactions)

    def add_transactions(self, *transactions):
        for obj in transactions:
            obj._vendor_shift = self
            self._transactions.append(obj)

    def remove_transactions(self, *transactions):
        for obj in transactions:
            obj._vendor_shift = None
            self._transactions.remove(obj)
    # >>> transactions

    # <<< receipts
    # @generated
    def get_receipts(self):
        """ 
        """
        return self._receipts

    def set_receipts(self, value):
        for x in self._receipts:
            x._vendor_shift = None
        for y in value:
            y._vendor_shift = self
        self._receipts = value

    receipts = property(get_receipts, set_receipts)

    def add_receipts(self, *receipts):
        for obj in receipts:
            obj._vendor_shift = self
            self._receipts.append(obj)

    def remove_receipts(self, *receipts):
        for obj in receipts:
            obj._vendor_shift = None
            self._receipts.remove(obj)
    # >>> receipts

    # <<< merchant_account
    # @generated
    def get_merchant_account(self):
        """ Merchant account this vendor shift periodically debits (based on aggregated transactions).
        """
        return self._merchant_account

    def set_merchant_account(self, value):
        if self._merchant_account is not None:
            filtered = [x for x in self.merchant_account.vendor_shifts if x != self]
            self._merchant_account._vendor_shifts = filtered

        self._merchant_account = value
        if self._merchant_account is not None:
            self._merchant_account._vendor_shifts.append(self)

    merchant_account = property(get_merchant_account, set_merchant_account)
    # >>> merchant_account

    # <<< vendor
    # @generated
    def get_vendor(self):
        """ Vendor that opens and owns this vendor shift.
        """
        return self._vendor

    def set_vendor(self, value):
        if self._vendor is not None:
            filtered = [x for x in self.vendor.vendor_shifts if x != self]
            self._vendor._vendor_shifts = filtered

        self._vendor = value
        if self._vendor is not None:
            self._vendor._vendor_shifts.append(self)

    vendor = property(get_vendor, set_vendor)
    # >>> vendor


    def __str__(self):
        """ Returns a string representation of the VendorShift.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< vendor_shift.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the VendorShift.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "VendorShift", self.uri)
        if format:
            indent += ' ' * depth

        for obj in self.transactions:
            s += '%s<%s:VendorShift.transactions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        for obj in self.receipts:
            s += '%s<%s:VendorShift.receipts rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.merchant_account is not None:
            s += '%s<%s:VendorShift.merchant_account rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.merchant_account.uri)
        if self.vendor is not None:
            s += '%s<%s:VendorShift.vendor rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.vendor.uri)
        s += '%s<%s:VendorShift.posted>%s</%s:VendorShift.posted>' % \
            (indent, ns_prefix, self.posted, ns_prefix)
        s += '%s<%s:VendorShift.merchant_debit_amount>%s</%s:VendorShift.merchant_debit_amount>' % \
            (indent, ns_prefix, self.merchant_debit_amount, ns_prefix)
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
        for obj in self.receipt_summaries:
            s += '%s<%s:Shift.receipt_summaries rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.activity_interval is not None:
            s += '%s<%s:Shift.activity_interval rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.activity_interval.uri)
        for obj in self.transaction_summaries:
            s += '%s<%s:Shift.transaction_summaries rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Shift.transactions_grand_total_rounding>%s</%s:Shift.transactions_grand_total_rounding>' % \
            (indent, ns_prefix, self.transactions_grand_total_rounding, ns_prefix)
        s += '%s<%s:Shift.transactions_grand_total>%s</%s:Shift.transactions_grand_total>' % \
            (indent, ns_prefix, self.transactions_grand_total, ns_prefix)
        s += '%s<%s:Shift.receipts_grand_total_bankable>%s</%s:Shift.receipts_grand_total_bankable>' % \
            (indent, ns_prefix, self.receipts_grand_total_bankable, ns_prefix)
        s += '%s<%s:Shift.receipts_grand_total_rounding>%s</%s:Shift.receipts_grand_total_rounding>' % \
            (indent, ns_prefix, self.receipts_grand_total_rounding, ns_prefix)
        s += '%s<%s:Shift.receipts_grand_total_non_bankable>%s</%s:Shift.receipts_grand_total_non_bankable>' % \
            (indent, ns_prefix, self.receipts_grand_total_non_bankable, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "VendorShift")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> vendor_shift.serialize


class CashierShift(Shift):
    """ The operating shift for a cashier, during which he may transact against the CashierShift, subject to VendorShift being open.
    """
    # <<< cashier_shift
    # @generated
    def __init__(self, cash_float=0.0, cashier=None, receipts=None, point_of_sale=None, transactions=None, **kw_args):
        """ Initialises a new 'CashierShift' instance.
        """
        # The amount of cash that the cashier brings with him to start his shift and that he will take away at the end of his shift; i.e. the cash float does not get banked. 
        self.cash_float = cash_float


        self._cashier = None
        self.cashier = cashier

        self._receipts = []
        if receipts is not None:
            self.receipts = receipts
        else:
            self.receipts = []

        self._point_of_sale = None
        self.point_of_sale = point_of_sale

        self._transactions = []
        if transactions is not None:
            self.transactions = transactions
        else:
            self.transactions = []


        super(CashierShift, self).__init__(**kw_args)
    # >>> cashier_shift

    # <<< cashier
    # @generated
    def get_cashier(self):
        """ Cashier operating this shift.
        """
        return self._cashier

    def set_cashier(self, value):
        if self._cashier is not None:
            filtered = [x for x in self.cashier.cashier_shifts if x != self]
            self._cashier._cashier_shifts = filtered

        self._cashier = value
        if self._cashier is not None:
            self._cashier._cashier_shifts.append(self)

    cashier = property(get_cashier, set_cashier)
    # >>> cashier

    # <<< receipts
    # @generated
    def get_receipts(self):
        """ All Receipts recorded for this Shift.
        """
        return self._receipts

    def set_receipts(self, value):
        for x in self._receipts:
            x._cashier_shift = None
        for y in value:
            y._cashier_shift = self
        self._receipts = value

    receipts = property(get_receipts, set_receipts)

    def add_receipts(self, *receipts):
        for obj in receipts:
            obj._cashier_shift = self
            self._receipts.append(obj)

    def remove_receipts(self, *receipts):
        for obj in receipts:
            obj._cashier_shift = None
            self._receipts.remove(obj)
    # >>> receipts

    # <<< point_of_sale
    # @generated
    def get_point_of_sale(self):
        """ Point of sale that is in operation during this shift.
        """
        return self._point_of_sale

    def set_point_of_sale(self, value):
        if self._point_of_sale is not None:
            filtered = [x for x in self.point_of_sale.cashier_shifts if x != self]
            self._point_of_sale._cashier_shifts = filtered

        self._point_of_sale = value
        if self._point_of_sale is not None:
            self._point_of_sale._cashier_shifts.append(self)

    point_of_sale = property(get_point_of_sale, set_point_of_sale)
    # >>> point_of_sale

    # <<< transactions
    # @generated
    def get_transactions(self):
        """ 
        """
        return self._transactions

    def set_transactions(self, value):
        for x in self._transactions:
            x._cashier_shift = None
        for y in value:
            y._cashier_shift = self
        self._transactions = value

    transactions = property(get_transactions, set_transactions)

    def add_transactions(self, *transactions):
        for obj in transactions:
            obj._cashier_shift = self
            self._transactions.append(obj)

    def remove_transactions(self, *transactions):
        for obj in transactions:
            obj._cashier_shift = None
            self._transactions.remove(obj)
    # >>> transactions


    def __str__(self):
        """ Returns a string representation of the CashierShift.
        """
        return self.serialize(header=True, depth=2, format=True)


    # <<< cashier_shift.serialize
    # @generated
    def serialize(self, header=False, depth=0, format=False):
        """ Returns an RDF/XML representation of the CashierShift.
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

        s += '%s<%s:%s rdf:ID="%s">' % (indent, ns_prefix, "CashierShift", self.uri)
        if format:
            indent += ' ' * depth

        if self.cashier is not None:
            s += '%s<%s:CashierShift.cashier rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.cashier.uri)
        for obj in self.receipts:
            s += '%s<%s:CashierShift.receipts rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.point_of_sale is not None:
            s += '%s<%s:CashierShift.point_of_sale rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.point_of_sale.uri)
        for obj in self.transactions:
            s += '%s<%s:CashierShift.transactions rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:CashierShift.cash_float>%s</%s:CashierShift.cash_float>' % \
            (indent, ns_prefix, self.cash_float, ns_prefix)
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
        for obj in self.receipt_summaries:
            s += '%s<%s:Shift.receipt_summaries rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        if self.activity_interval is not None:
            s += '%s<%s:Shift.activity_interval rdf:resource="#%s"/>' % \
                (indent, ns_prefix, self.activity_interval.uri)
        for obj in self.transaction_summaries:
            s += '%s<%s:Shift.transaction_summaries rdf:resource="#%s"/>' % \
                (indent, ns_prefix, obj.uri)
        s += '%s<%s:Shift.transactions_grand_total_rounding>%s</%s:Shift.transactions_grand_total_rounding>' % \
            (indent, ns_prefix, self.transactions_grand_total_rounding, ns_prefix)
        s += '%s<%s:Shift.transactions_grand_total>%s</%s:Shift.transactions_grand_total>' % \
            (indent, ns_prefix, self.transactions_grand_total, ns_prefix)
        s += '%s<%s:Shift.receipts_grand_total_bankable>%s</%s:Shift.receipts_grand_total_bankable>' % \
            (indent, ns_prefix, self.receipts_grand_total_bankable, ns_prefix)
        s += '%s<%s:Shift.receipts_grand_total_rounding>%s</%s:Shift.receipts_grand_total_rounding>' % \
            (indent, ns_prefix, self.receipts_grand_total_rounding, ns_prefix)
        s += '%s<%s:Shift.receipts_grand_total_non_bankable>%s</%s:Shift.receipts_grand_total_non_bankable>' % \
            (indent, ns_prefix, self.receipts_grand_total_non_bankable, ns_prefix)

        if format:
            indent = indent[:-depth]
        s += '%s</%s:%s>' % (indent, ns_prefix, "CashierShift")

        if header:
            s += '%s</rdf:RDF>' % indent[:-depth]

        return s
    # >>> cashier_shift.serialize


# <<< payment_metering
# @generated
# >>> payment_metering
