import mysql.connector
from random import randint as rand
import json

class Database:

    __host = None
    __user = None
    __password = None
    __database = None
    __db = None
    __table = None

    def __init__(self, configFile: str) -> None:
        DBInfo = json.loads(open(configFile, 'r').read())
        self.__host = DBInfo['host']
        self.__user = DBInfo['user']
        self.__password = DBInfo['password']
        self.__database = DBInfo['database']
        self.__table = DBInfo['table']

        checkDB = mysql.connector.connect(
            host = self.__host,
            user = self.__user,
            password = self.__password,
        )
        cursor = checkDB.cursor()
        DBExist = False
        cursor.execute('SHOW DATABASES')
        for dbName in cursor:
            if self.__database in dbName:
                DBExist = True
        if not DBExist:
            createDB = mysql.connector.connect(
                host = self.__host,
                user = self.__user,
                password = self.__password,
                )
            cursor = createDB.cursor()
            cursor.execute('CREATE DATABASE {}'.format(self.__database))
            print('DATABASE CREATED')

        self.__db = mysql.connector.connect(
            host = self.__host,
            user = self.__user,
            password = self.__password,
            database = self.__database,
        )

        checkTable = False
        cursor = self.__db.cursor()
        cursor.execute('SHOW TABLES')
        a = cursor.fetchall()
        for tableName in a:
            if self.__table == tableName[0]:
                checkTable = True
        if not checkTable:
            createTable = mysql.connector.connect(
                host = self.__host,
                user = self.__user,
                password = self.__password,
                database = self.__database,
                )
            cursor = createTable.cursor()
            cursor.execute('CREATE TABLE {} (id INT AUTO_INCREMENT PRIMARY KEY, tweet VARCHAR(280), sent VARCHAR(1))'.format(self.__table))
            file = open('Tweets.txt', 'r')
            fileLines = file.readlines()
            insertTable = createTable.cursor()
            sqlCommand = 'INSERT INTO {} (tweet, sent) VALUES (%s, "F")'.format(self.__table)
            for i in fileLines:
                val = (i,)
                insertTable.execute(sqlCommand, val)
                createTable.commit()
            print('TABLE CREATED')
        else:
            print('TABLE EXISTS, TRY ANOTHER TABLE NAME')
            return
        

    def get_host(self) -> str:
        return self.__host

    def get_user(self) -> str:
        return self.__user

    def get_password(self) -> str:
        return self.__password

    def get_database(self) -> str:
        return self.__database

    def get_table_rows(self) -> int:
        sql = mysql.connector.connect(
            host = self.__host,
            user = self.__user,
            password = self.__password,
            database = self.__database
        )
        cursor = sql.cursor()
        sql_command = 'SELECT COUNT(*) FROM {}'.format(self.__table)
        cursor.execute(sql_command)
        number_of_tables: int = cursor.fetchone()[0]
        return number_of_tables

    def update_table(self, id):
        sql = mysql.connector.connect(
            host = self.__host,
            user = self.__user,
            password = self.__password,
            database = self.__database
        )
        cursor = sql.cursor()
        sql_command = "UPDATE {} SET sent = 'T' WHERE id = %s".format(self.__table)
        cursor.execute(sql_command, id)
        sql.commit()

    def read_random_data_from_table(self) -> str:
        sql = mysql.connector.connect(
            host = self.__host,
            user = self.__user,
            password = self.__password,
            database = self.__database
        )
        cursor = sql.cursor()
        sql_command = 'SELECT COUNT(*) FROM {}'.format(self.__table)
        cursor.execute(sql_command)
        number_of_tables: int = cursor.fetchone()[0]
        sql_command = 'SELECT tweet FROM {} WHERE sent = "F" AND id = %s'.format(self.__table)
        id = (str(rand(0, number_of_tables),),)
        cursor.execute(sql_command, id)
        try:
            tweet = cursor.fetchone()[0]
        except:
            return self.read_random_data_from_table()
        if tweet != None:
            self.update_table(id=id)
        return tweet

    def pop_random_data_from_table(self, id = None) -> str:
        sql = mysql.connector.connect(
            host = self.__host,
            user = self.__user,
            password = self.__password,
            database = self.__database
        )
        cursor = sql.cursor()
        sql_command = 'SELECT tweet FROM {} WHERE id = {}'.format(self.__table, id)
        cursor.execute(sql_command)
        table_row_tweet = cursor.fetchone()[0]
        sql_command = 'DELETE FROM {} WHERE id = {}'.format(self.__table, id)
        sql2 = mysql.connector.connect(
            host = self.__host,
            user = self.__user,
            password = self.__password,
            database = self.__database
        )
        cursor2 = sql2.cursor()
        cursor2.execute(sql_command)
        sql2.commit()
        return table_row_tweet