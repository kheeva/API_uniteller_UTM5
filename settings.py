ip_white_list = [
    '127.0.0.1',
]

required_query_params = [
    'Signature',
    'Order_ID',
    'Status',
    'Customer_IDP',
    'BillNumber'
]

db_cfg = {
    'host': 'localhost',
    'port': 3306,
    'user': 'db_user',
    'password': 'db_password',
    'database': 'UTM5',
    'charset': 'utf8'
}

ourfa_args = ['-x', 'xml',
              '-H', 'localhost',
              '-l', 'bill_login',
              '-P', 'bill_password',
              '-S', 'rsa_cert',
              '-a', 'add_payment',
              '-payment_method', '10',
              '-turn_on_inet', '1'
]

password = 'agoodpassword'
