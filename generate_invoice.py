#!/usr/bin/env python3

from datetime import date, timedelta
import re
from subprocess import run, PIPE
import os
import html
from config.config import (
    TEMPLATE_VARS, 
    BILLING_PRICE, 
    DIR_GENERETE, 
    TERMS, 
    TERMS_TAXES_CONTRACTOR,
    INVOICE_DATE_FORMAT,
    TEMPLATE_NAME
)
try:
    from config.config import HTML_MODE
except ImportError:
    HTML_MODE = False

_today = date.today().replace(day=1)

try:
    billing_hours = float(input('Hours worked: '))
except:
    print('Hours must be provided as int argument')
    exit()

if _input_today := input(f'TODAY ({_today.isoformat()}): '):
    date_of_invoice = date.fromisoformat(_input_today)
else:
    date_of_invoice = _today.replace(day=1)


_billing_start = (date_of_invoice.replace(day=1) - timedelta(days=1)).replace(day=1)
_billing_end = (_billing_start + timedelta(31)).replace(day=1) - timedelta(days=1)
_default_billing_period = f'{_billing_start.strftime("%d %B")} - {_billing_end.strftime("%d %B")}'

billing_period = (
    input(f'BILLING_PERIOD ({_default_billing_period}): ') or
    _default_billing_period
)

terms = TERMS if bool(input('Transfer taxes by client? [1/0](0): ')) else TERMS_TAXES_CONTRACTOR

invoice_number = date_of_invoice.strftime('%Y%m%d')


def prepare_html_for_formatting(html: str) -> str:
    # escape non-placeholders curly with second curly
    html = re.sub(r'({)([^#])', r'{{\2', html)
    html = re.sub(r'([^#])(})', r'\1}}', html)
    return re.sub(r'{#([^}]+)#}', r'{\1}', html)

template_name = os.path.abspath(f'templates/{TEMPLATE_NAME}')

with open(template_name, 'r', encoding='utf-8') as f:
    safe_curly = prepare_html_for_formatting(''.join(f.readlines()))
    data = dict(
        **TEMPLATE_VARS,
        INVOICE_NUMBER=invoice_number,
        INVOICE_DATE=date_of_invoice.strftime(INVOICE_DATE_FORMAT),
        BILLING_PERIOD=billing_period,
        BILLING_HOURS='{:.1f}'.format(billing_hours),
        BILLING_PRICE='{:.2f}'.format(BILLING_PRICE),
        BILLING_TOTAL='{:.2f}'.format(BILLING_PRICE * billing_hours),
    )
    html = safe_curly.format(**data, TERMS=terms)

output_file = os.path.abspath(
    f"{DIR_GENERETE}/invoice_{invoice_number}.{'html' if (HTML_MODE) else 'pdf'}"
)

if (HTML_MODE is True):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
else:
    process = run(
        [
            'wkhtmltopdf', 
            '--margin-top', '20mm',
            '--margin-bottom', '20mm',
            '--margin-left', '15mm',
            '--margin-right', '15mm',
            '-',
            output_file,
        ],
        stdout=PIPE,
        input=html,
        encoding='utf-8',
    )

    print(' '.join(process.args))
    print(process.stdout)
    if (process.returncode):
        exit(process.returncode)


print(f'Generated as {output_file}')

exit(0)
