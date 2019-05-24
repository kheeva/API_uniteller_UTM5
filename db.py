import MySQLdb

from settings import db_cfg


class Database:
    def __init__(self, db_cfg):
        try:
            self._conn = MySQLdb.connect(**db_cfg)
        except Exception:
            self._conn = None
        else:
            self._cur = self._conn.cursor()

    def execute(self, query, params):
        self._cur.execute(query, params)
        return self._cur

    def __del__(self):
        if self._conn:
            self._conn.close()


def get_account_id(login):
    db = Database(db_cfg)
    query = 'SELECT id FROM users WHERE login=%s AND is_deleted=0'

    if not db._conn:
        return ()

    account_id = db.execute(query, (login,)).fetchone()
    return str(account_id[0]) if account_id else None


def is_payment_id_allready_exist(_post_payment_id):
    db = Database(db_cfg)
    query = 'SELECT id FROM payment_transactions WHERE method=108 AND payment_ext_number=%s'

    if not db._conn:
        return ()

    db_payment_id = db.execute(query, (_post_payment_id,)).fetchone()

    return False if not db_payment_id else True
