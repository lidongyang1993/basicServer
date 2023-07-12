#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/25 17:31
# @Author  : lidongyang
# @Site    : 
# @File    : PG_DB.py
# @Software: PyCharm
import psycopg2


class PG:

    def __init__(self, database, user, password, host, port=5432):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.con: psycopg2 = None
        self.result = None

    def connect(self):
        try:
            self.con = psycopg2.connect(database=self.database, user=self.user,
                                        password=self.password, host=self.host, port=self.port)

        except Exception as e:
            print('connection failed', str(e))

    def close_db_connection(self):
        self.con.commit()
        self.con.close()

    def done(self, SQL):
        if not self.con:
            return
        cur = self.con.cursor()
        try:
            cur.execute(SQL)
            if 'select' in SQL.lower():
                result = cur.fetchall()
            else:
                result = None
        except Exception as e:
            result = e
        self.close_db_connection()
        self.result = result

    def result_extract(self, row: int, col: int):
        if not self.result:
            return None
        return self.result[row][col]




if __name__ == '__main__':
    pg = PG("inv_xx", "user1", "123456", "192.168.2.65")
    pg.connect()
    pg.done("select* from xx_invoice_json_log where invoice_id = '1672892219301367810'")
    res = pg.result_extract(0, 10)
    print(res)
