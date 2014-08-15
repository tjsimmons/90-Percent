class GenericResult(object):
    """
    Must set _bindings in subclass. It's how the set_attributes method knows to get the values from the SOAP object.
    Do note that the items must be entered into the tuple IN ORDER, so we can properly generate the field{num} values.
    It's a tuple because tuples are immutable.
    """

    _bindings = ()

    def __init__(self, **kwargs):
        self._set_attributes(**kwargs)

    def _set_attributes(self, **kwargs):
        soap_name = 'field{num}'
        num = 1

        for field in self._bindings:
            #print 'Setting', field, 'to', kwargs[soap_name.format(num=num)]
            setattr(self, field, kwargs[soap_name.format(num=num)])

            num += 1

    def __repr__(self):
        fields = filter(lambda x: x[:1] != '_', dir(self))

        # ugly, but it returns a string representing the object and it's values
        return '\n'.join(f for f in map(lambda x: '%s = %s' % (x[0], x[1]), ((field, getattr(self, field)) for field in fields)))

class PaymentInfo(GenericResult):
    _bindings = ('debtornum', 'payment_date', 'ref_code', 'payment_amount', 'payment_status', 'payment_detail', 'location')

class BillInfo(GenericResult):
    _bindings = ('debtornum', 'stmtnum', 'bill_date', 'due_date', 'bill_amount', 'total_amt_due', 'amount_paid', 'amount_unpaid', 'status')

class AccountInfo(GenericResult):
    _bindings = ('debtornum', 'premnum', 'current_plan', 'prev_balance', 'prev_payments', 'current_charges', 'meter_cycle_day', 'energy_type')

class OfferInfo(GenericResult):
    _bindings = ('premises', 'offer', 'start_date', 'end_date', 'price')
