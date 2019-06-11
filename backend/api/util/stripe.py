from pinax.stripe.models import Customer
from pinax.stripe.actions.charges import create
from decimal import Decimal


def charge(customer, amount):
    amount = Decimal(amount)
    return create(amount=amount, customer=customer,
                  send_receipt=False)
