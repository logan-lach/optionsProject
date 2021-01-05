
import mysql.connector
from mysql.connector import errorcode
import os

class Database:


    def __init__(self):
        self.connection = self.databaseConfig()
        self.cursor = self.connection.cursor()

    def databaseConfig(self):
        try:
            cnx = mysql.connector.connect(user=str(os.environ.get('USER')),
                                      password=str(os.environ.get('PASSWORD')),  # Some boilerplate I have, dont touch it
                                      host=str(os.environ.get('HOST')),
                                      database=str(os.environ.get('DATABASE'))
                                      )
            return cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
                return cnx
    def testAccess(self):
        command = 'SELECT * FROM $AMD'
        self.cursor.execute(command)
        for x in self.cursor:
            print(x)

    def testReading(self):
        file = open('S&P500.txt', 'r')
        count = 0
        value = file.readline()
        for i in range(0,50):
            print(value)
            value = file.readline()

    def analyzeDB(self, stockname, values):
        command = 'SELECT * FROM ' + '$' + stockname
        results = []
        for x in self.cursor:
            results.append(x)


        #command = 'INSERT INTO ' + '$'+stockname + ' VALUES (%s,%s,%s,%s)'
        self.cursor.execute(command,(values[0], values[1],values[2],values[3]))
        #self.connection.commit()
    def createTables(self):
        file = open('S&P500.txt', 'r')
        currentStock = file.readline().replace('\n','').replace('.','')
        count = 0
        while(currentStock != ''):
            try:
                command = 'CREATE TABLE ' + '$' + currentStock + '(' \
                  'tradeID VARCHAR(35),' \
                  'weeklyVolume VARCHAR(10),' \
                  'yesterdayVolume VARCHAR(10),' \
                  'todayVolume VARCHAR(10), PRIMARY KEY (tradeID));'
                self.cursor.execute(command)

            except mysql.connector.ProgrammingError:
              print(currentStock + ' Already exists, moving on')
            currentStock = file.readline().replace('\n','').replace('.','')
            count += 1

        self.cursor.close()
        self.connection.close()
    def close(self):
        self.cursor.close()
        self.connection.close()
db = Database()
db.testAccess()




