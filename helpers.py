import hashlib
import time
import subprocess
import xml.etree.ElementTree as ET
import json

from db import get_account_id, is_payment_id_allready_exist
from settings import ourfa_args


def parse_post_params(_wsgi_input, _len):
    _post_params = {}
    body = _wsgi_input.read(_len).decode()
    for attr in body.split('&'):
        name, value = attr.split('=')
        _post_params[name] = value
    return _post_params


def is_correct_query_params(_params_dict, req_params):
    q_params = [_params_dict.get(param) is not None for param in req_params]
    return sum(q_params) == len(req_params)


def md5(_str):
    return hashlib.md5(_str.encode()).hexdigest()


def uppercase(_str):
    return _str.upper()


def our_signature(post_attrs, _password, req_params):
    _signature = post_attrs['Signature']
    _str = ''.join([
        post_attrs['Order_ID'],
        post_attrs['Status'],
        post_attrs['Customer_IDP'],
        post_attrs['BillNumber'],
        post_attrs['Total'],
        _password
    ])
    return _signature == uppercase(md5(_str))


def pay(_q_attrs_dict):
    account_id = get_account_id(_q_attrs_dict['Customer_IDP'])

    if account_id and not is_payment_id_allready_exist(_q_attrs_dict['BillNumber']):
        payment_date = str(int(time.time()))

        program_name = './ourfa_client'

        payment_args = [
            '-account_id', account_id,
            '-payment', _q_attrs_dict['Total'],
            '-payment_ext_number' ,_q_attrs_dict['BillNumber'],
            'payment_date', payment_date
        ]

        command = [program_name]
        command.extend(ourfa_args)
        command.extend(payment_args)

        output = subprocess.Popen(
            command,
            stdout=subprocess.PIPE).communicate()[0]

        root = ET.fromstring(output)
        for i in root.iter('integer'):
            _q_attrs_dict['transaction_id'] = i.attrib['value']

        if _q_attrs_dict.get('transaction_id'):
            report = json.dumps({'transaction_id': _q_attrs_dict['transaction_id']})
            return report.encode(), 200, {}

    return b'error', 500, {}
