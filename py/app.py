import psr_data_generater
import time
import mysql.connector
import psycopg2

def test(cnx):
    cursor = cnx.cursor()
    try:
        cursor.execute("select 1")
        for r in cursor:
            print("connected")
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
    
def get_connection():
    mysql_cnx = mysql.connector.connection.MySQLConnection(
        user='someone', password='passme',
        host='mysql', database='psr')
    pg_cnx = psycopg2.connect(host="postgres", dbname="postgres", user="postgres", password="postgres")
    while(not test(mysql_cnx) and not test(pg_cnx)):
        print("testing db connection")
    return mysql_cnx, pg_cnx

if __name__ == "__main__":
    mysql_cnx, pg_cnx = get_connection()
    psr_data_generater.start(mysql_cnx, pg_cnx)

