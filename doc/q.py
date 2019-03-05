# -*- coding: utf-8 -*-
import pymysql


def generate_mysql_connect_dict():
    return {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "111111",
        "db": 'aces',
        "charset": "utf8",
        "cursorclass": pymysql.cursors.DictCursor,
    }

connection = pymysql.connect(**generate_mysql_connect_dict())

def get_children(parent_id):
    with connection.cursor() as cursor:
        sql = '''
        select * from departments_department where  parent_dept={}
        '''.format(parent_id)
        cursor.execute(sql)
        return cursor.fetchall()



def generate_tree(parent_id, root):
    children = get_children(parent_id)
    if children:
        for child in children:
            generate_tree(child.get('id'), root.setdefault(child.get('name'), {}))
    else:
        return

init_id = 0
data = {}
generate_tree(init_id, data)
print(data)





