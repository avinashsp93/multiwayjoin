import mysql.connector 
from mysql.connector import errorcode

def connect_tpch(operation, isReturn):
    try:
        cnx = mysql.connector.connect(user='root', password='root', database='tpch')
        mycursor = cnx.cursor()
        mycursor.execute(operation)
        if(isReturn):
            results = mycursor.fetchall()
            return results


    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return 0