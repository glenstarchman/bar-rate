from ..models.invoice import Invoice



def create_invoice(organization, user, items, subtotal, tax, final_cost):
    # temporary... change this when we create actual invoices via Dynamics
    invoice = Invoice(
        dynamics_id="FAKEINV-1234",
        subtotal=subtotal,
        tax=tax,
        final_cost=final_cost,
        organization=organization,
        user=user
    )

    invoice.save()
    return invoice
