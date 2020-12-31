
import mysql.connector
from mysql.connector import errorcode

class Database:


    def __init__(self):
        self.connection = self.databaseConfig()
        self.cursor = self.connection.cursor()

    def databaseConfig(self):
        try:
            cnx = mysql.connector.connect(user='root',
                                      password='SmokingWalnut58',  # Some boilerplate I have, dont touch it
                                      host='127.0.0.1',
                                      database='optionsTracker',
                                      auth_plugin='mysql_native_password')
            return cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
                return cnx

    def testReading(self):
        file = open('S&P500.txt', 'r')
        count = 0
        value = file.readline()
        for i in range(0,50):
            print(value)
            value = file.readline()

    def createTables(self):
        file = open('S&P500.txt', 'r')
        currentStock = file.readline()
        count = 0
        while(currentStock != ''):
            try:
                command = 'CREATE TABLE ' + currentStock + '(' \
                  'tradeID VARCHAR(30),' \
                  'weeklyVolume INT,' \
                  'yesterdayVolume INT,' \
                  'todayVolume INT);'
                self.cursor.execute(command,[])

            except mysql.connector.ProgrammingError:
                print(currentStock + ' Already exists, moving on')
            currentStock = file.readline()
            count += 1

        self.cursor.close()
        self.connection.close()


db = Database()
db.createTables()