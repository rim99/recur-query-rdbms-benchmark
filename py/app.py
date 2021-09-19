import psr_data_generater
import time
import datetime
import mysql.connector.pooling
import psycopg2
import os
import mariadb

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
            mariadb_cnx_pool = mariadb.ConnectionPool(
                pool_name = "mariadb-test",
                pool_size = 20,
                user="someone",
                password="passme",
                host="mariadb",
                port=3306,
                database="psr"
            )    
            pg_cnx = psycopg2.connect(
                host="postgres", 
                dbname="postgres", 
                user="postgres", 
                password="postgres")
            my_cnx = mysql_cnx_pool.get_connection()
            ma_cnx = mariadb_cnx_pool.get_connection()
            connected = test(my_cnx) and test(pg_cnx) and test(ma_cnx)
            my_cnx.close()
            ma_cnx.close()
        except Exception as e:
            print(e)
            print("Try connecting ...")
        finally:
            time.sleep(3)
    return mysql_cnx_pool, pg_cnx, mariadb_cnx_pool

if __name__ == "__main__":
    mysql_cnx_pool, pg_cnx, mariadb_cnx_pool = get_connection()
    print("Generating testing data ... at " + str(datetime.datetime.now()))
    psr_data_generater.start(mysql_cnx_pool, pg_cnx, mariadb_cnx_pool)
    print("Finish at " + str(datetime.datetime.now()))

