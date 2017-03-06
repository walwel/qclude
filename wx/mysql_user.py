#-*- coding:UTF-8 -*-
import MySQLdb
#open mysql
db = MySQLdb.connect('localhost',"root",'662906..qqfsh')
#create database
cursor = db.cursor()
#use database
cursor.execute("use dlzt")
#create node table
create_table_node = "create table users(user_name char(32),count int,ctimes int,position int)"
cursor.execute(create_table_node)
#create command table
#create_table_comm = "create table command(query char())"
db.commit()
db.close()
