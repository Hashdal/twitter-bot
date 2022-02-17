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
        self.__dbOne = mysql.connector.connect(
            host = self.__host,
            user = self.__user,
            password = self.__password,
        )
        cursor = self.__dbOne.cursor()
        checkDB = False
        cursor.execute('SHOW DATABASES')
        for dbName in cursor:
            if self.__database in dbName:
                checkDB = True
        if not checkDB:
            createDB = self. mysql.connector.connect(
                host = self.__host,
                user = self.__user,
                password = self.__password,
                database = self.__database,
                ).cursor()
            createDB.execute('CREATE DATABASE {}'.format(self.__database))
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
        for tableName in cursor:
            if self.__table in tableName:
                checkTable = True
        if not checkTable:
            self.__dbTwo = mysql.connector.connect(
                host = self.__host,
                user = self.__user,
                password = self.__password,
                database = self.__database,
                )
            createTable = self.__dbTwo.cursor()
            createTable.execute('CREATE TABLE {} (id INT AUTO_INCREMENT PRIMARY KEY, tweet VARCHAR(280))'.format(self.__table))
            file = open('Tweets.txt ', 'r')
            fileLines = file.readlines()
            insertTable = self.__dbTwo.cursor()
            sql = 'INSERT INTO {} (tweet) VALUES (%s)'.format(self.__table)
            for i in fileLines:
                val = (i,)
                insertTable.execute(sql, val)
                self.__dbTwo.commit()
            print('TABLE CREATED')
    def get_host(self) -> str:
        return self.__host

    def get_user(self) -> str:
        return self.__user

    def get_password(self) -> str:
        return self.__password

    def get_database(self) -> str:
        return self.__database

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
        sql_command = 'SELECT tweet FROM {} WHERE id = %s'.format(self.__table)
        id = (str(rand(0, number_of_tables),),)
        cursor.execute(sql_command, id)
        return cursor.fetchone()[0]
