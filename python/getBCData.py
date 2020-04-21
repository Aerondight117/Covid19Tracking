import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup
import re
import pymysql
from sshtunnel import SSHTunnelForwarder


url = "http://www.bccdc.ca/Health-Info-Site/Documents/BCCDC_COVID19_Dashboard_Case_Details.csv"

# get the csv
response = requests.get(url, stream=True)

# Throw an error for bad status codes
response.raise_for_status()

#save the file
with open('covidCasesBC.csv', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)

#connect to sqlite DB
connection = sqlite3.connect('CanadaCovidResults.db')
c = connection.cursor()

#remove any old records 
c.execute("DELETE FROM `CovidCasesBC`")

c.execute("DROP VIEW IF EXISTS `CovidCasesBCView`")


c.execute("CREATE VIEW IF NOT EXISTS `CovidCasesBCView` AS SELECT COUNT(ReportedDate) as `NumberOfCases`,RegionName FROM `CovidCasesBC` GROUP BY `RegionName` ORDER BY NumberOfCases DESC ")
#create a table and store the data

c.execute("""CREATE TABLE IF NOT EXISTS `CovidCasesBC` (
  `ReportedDate` varchar(10) DEFAULT NULL,
  `RegionName` varchar(50) DEFAULT NULL
)""")

reader = csv.reader(open('covidCasesBC.csv', "r"))
next(reader)
for row in reader:
    to_db=((row[0],row[1]))
    
    c.execute("""INSERT INTO CovidCasesBC (ReportedDate,`RegionName`) VALUES (?, ?);""", to_db)
    

    
connection.commit()

rows = c.execute("SELECT * FROM CovidCasesBCView").fetchall()



def updateDatabase(SSHTunnelForwarder, pymysql, parsedData):
    
    sql_hostname = '127.0.0.1'
    sql_username = 'covicivy'
    sql_password = 'e#3(f$vL1MRq'
    sql_main_database = 'covicivy_covidCasesInCanada'
    sql_port = 3306
    ssh_host = 'server178.web-hosting.com'
    ssh_user = 'covicivy'
    ssh_port = 21098
    sql_ip = '127.0.0.1'

    with SSHTunnelForwarder(
        (ssh_host, ssh_port),
        ssh_username=ssh_user,
        ssh_password= sql_password,
        remote_bind_address=(sql_hostname, sql_port)) as tunnel:
            conn = pymysql.connect(host='127.0.0.1', user=sql_username,
            passwd=sql_password, db=sql_main_database,
            port=tunnel.local_bind_port)

            try:


                with conn.cursor() as cursor:
        
                    

                    for row in rows:        

                       
                        
                        print (row)
                        sql = """UPDATE CovidCasesBC SET `NumberOfCases` = %s WHERE (`RegionName` = CONCAT(%s, ' Health'));"""
                        cursor.execute(sql,  row)
                        conn.commit()

                        
            finally:
                conn.close()
                print ("Done")


updateDatabase(SSHTunnelForwarder, pymysql,rows)
