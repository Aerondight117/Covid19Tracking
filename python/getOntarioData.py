import requests 
from contextlib import closing
import csv
import sqlite3
import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder


#csv file download link
url = "https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv"

# get the csv
response = requests.get(url, stream=True)

# Throw an error for bad status codes
response.raise_for_status()

#save the file
with open('conposcovidloc.csv', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)

#connect to sqlite DB
connection = sqlite3.connect('CanadaCovidResults.db')
c = connection.cursor()

#remove any old records 
c.execute("DELETE FROM `CovidCasesOntario`")

c.execute("DROP VIEW IF EXISTS `CovidCases`")


c.execute("CREATE VIEW IF NOT EXISTS `CovidCases` AS SELECT COUNT(`ROW_ID`) AS 'NumberOfCases', Reporting_PHU,Reporting_PHU_City,Reporting_PHU_Latitude,Reporting_PHU_Longitude FROM `CovidCasesOntario` GROUP BY `Reporting_PHU` ORDER BY COUNT(`ROW_ID`) DESC ")
#create a table and store the data

c.execute("""CREATE TABLE IF NOT EXISTS `CovidCasesOntario` (
  `ROW_ID` int(4) DEFAULT NULL,
  `ACCURATE_EPISODE_DATE` varchar(10) DEFAULT NULL,
  `Age_Group` varchar(7) DEFAULT NULL,
  `CLIENT_GENDER` varchar(11) DEFAULT NULL,
  `CASE_ACQUISITIONINFO` varchar(27) DEFAULT NULL,
  `OUTCOME1` varchar(12) DEFAULT NULL,
  `Reporting_PHU` varchar(56) DEFAULT NULL,
  `Reporting_PHU_Address` varchar(30) DEFAULT NULL,
  `Reporting_PHU_City` varchar(16) DEFAULT NULL,
  `Reporting_PHU_Postal_Code` varchar(7) DEFAULT NULL,
  `Reporting_PHU_Website` varchar(61) DEFAULT NULL,
  `Reporting_PHU_Latitude` decimal(10,8) DEFAULT NULL,
  `Reporting_PHU_Longitude` decimal(11,8) DEFAULT NULL
)""")

reader = csv.reader(open('conposcovidloc.csv', "r"))
next(reader)
for row in reader:
    to_db=[]
    for r in row:
        to_db += [r]
    c.execute("""INSERT INTO CovidCasesOntario (ROW_ID,ACCURATE_EPISODE_DATE,Age_Group,CLIENT_GENDER,CASE_ACQUISITIONINFO,OUTCOME1,Reporting_PHU,Reporting_PHU_Address,
                Reporting_PHU_City,Reporting_PHU_Postal_Code,Reporting_PHU_Website,Reporting_PHU_Latitude,Reporting_PHU_Longitude) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ?);""", to_db)
    

    
connection.commit()

rows = c.execute("SELECT * FROM CovidCases").fetchall()



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
                cursor.execute("DELETE FROM CovidCases")
                
        finally:
            conn.commit()

        try:


            with conn.cursor() as cursor:
    
                

                for row in rows:  
                    
                    sql = """INSERT INTO CovidCases(NumberOfCases,RegionName,ProvinceName,TownName,Latitude,Longitude) VALUES (%s,%s, 'Ontario', %s, %s,%s);"""
                    cursor.execute(sql, row )
                    print(row)
                    conn.commit()
        finally:
            conn.close()


