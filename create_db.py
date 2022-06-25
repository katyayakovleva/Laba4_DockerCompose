import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", port="3307", passwd="katya2905", auth_plugin='mysql_native_password')

my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE lab4")

