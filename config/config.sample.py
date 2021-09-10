from datetime import date
from typing import Mapping

CONTRACT_DATE = date(2021, 1, 1)
BILLING_PRICE = 999
DIR_GENERETE = 'generated_invoices'
TEMPLATE_NAME = 'invoice_template.html'
INVOICE_DATE_FORMAT = '%b&nbsp;%d,&nbsp;%Y'
# HTML_MODE = True


TEMPLATE_VARS: Mapping[str, str] = dict(
    CONTRACT_NUMBER=f"Contract from {CONTRACT_DATE.strftime('%d.%m.%Y')}",
    CONTRACT_DATE=CONTRACT_DATE.strftime(INVOICE_DATE_FORMAT),

    TO_NAME='JOHN DOE',
    TO_TAX_NUMBER='TAX NUMBER: 123',
    TO_ADDRESS='Your Address',
    TO_BANK='Your bank info',
    TO_BANK_SWIFT='Your bank swift',
    TO_BANK_ACCOUNT='Your bank account',

    FROM_ORGANIZATION='Client organization',
    FROM_ADDRESS='Client organization address',
    FROM_BANK='Client bank info',
    FROM_SWIFT='Client bank swift',
    FROM_BANK_ACCOUNT='Client bank account'
)

TERMS = '''Some terms'''

TERMS_TAXES_CONTRACTOR = TERMS + '''
    <br />All charges of correspondent banks shall be paid by the Contractor.
'''