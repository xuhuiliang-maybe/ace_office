# -*- coding: utf-8 -*-
import pymysql


def generate_mysql_connect_dict(host):
    assert host, 'must pass `host` and `db_name`'
    return {
        "host": host,
        "user": "root",
        "password": "Mike123456-",
        "db": 'dept',
        "charset": "utf8",
        "cursorclass": pymysql.cursors.DictCursor,
    }

connection = pymysql.connect(**generate_mysql_connect_dict('192.168.199.165'))

def get_children(parent_id):
    with connection.cursor() as cursor:
        sql = '''
        select * from departments_department where  parent_dept={}
        '''.format(parent_id)
        cursor.execute(sql)
        return cursor.fetchall()

def get_root_dict(id):
    with connection.cursor() as cursor:
        sql = '''
        select * from departments_department where  id={}
        '''.format(id)
        cursor.execute(sql)
        return cursor.fetchone()


def level_dict(id, id_dict, is_root=False):
    if is_root:
        return_value = {}
        children = get_children(id)
        for child in children:
            id = child.pop('id')
            return_value.update({str(id): level_dict(id, child)})
        return return_value
    children = get_children(id)
    if children:
        add_params = id_dict.setdefault('additionalParameters', {})
        add_params['children'] = {}
        for child in children:
            id = child.pop('id')
            add_params['children'][str(id)] = level_dict(id, child)
    return id_dict


init_id = 0
data = level_dict(init_id, None, True)
import json
print(json.dumps(data))





