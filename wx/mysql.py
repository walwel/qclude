#-*- coding:UTF-8 -*-
import MySQLdb
#open mysql
db = MySQLdb.connect('localhost',"root",'662906..qqfsh')
#create database
cursor = db.cursor()
cursor.execute("create database dlzt character set utf8")
#use database
cursor.execute("use dlzt")
#create node table
create_table_node = "create table node(Laddr char(32),Saddr char(8),stat int,flag int,position int)"
cursor.execute(create_table_node)
#create command table
#create_table_comm = "create table command(query char())"
db.commit()
db.close()
