import psr_data_generater
import time
import datetime
import mysql.connector.pooling
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
    connected = False
    while not connected:
        try:
            mysql_cnx_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name = "mypool", pool_size = 20,
                user='someone', password='passme',
                host='mysql', database='psr')
            pg_cnx = psycopg2.connect(
                host="postgres", 
                dbname="postgres", 
                user="postgres", 
                password="postgres")
            my_cnx = mysql_cnx_pool.get_connection()
            connected = test(my_cnx) and test(pg_cnx)
            my_cnx.close()
        except Exception as e:
            print(e)
            print("Try connecting ...")
        finally:
            time.sleep(3)
    return mysql_cnx_pool, pg_cnx

if __name__ == "__main__":
    mysql_cnx_pool, pg_cnx = get_connection()
    print("Generating testing data ... at " + str(datetime.datetime.now()))
    psr_data_generater.start(mysql_cnx_pool, pg_cnx)
    print("Finish at " + str(datetime.datetime.now()))

