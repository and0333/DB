from DBconn import DBContextManager


def select_dict(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql)
            products = cursor.fetchall()
            if products:
                products_dict = []
                schema = [item[0] for item in cursor.description]
                for product in products:
                    products_dict.append(dict(zip(schema, product)))
                return products_dict
            else:
                return None


def call_proc(dbconfig: dict, proc_name: str, *args):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_list = []
        for arg in args:
            param_list.append(arg)
        res = cursor.callproc(proc_name, param_list)
        return res


def insert_into_db(db_config, _sql):
    with DBContextManager(db_config) as cursor:
        if cursor:
            return cursor.execute(_sql)
        else:
            raise ValueError('Курсор не создан')