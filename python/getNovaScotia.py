import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup
import re
import pymysql
from sshtunnel import SSHTunnelForwarder


url = "https://novascotia.ca/coronavirus/data/COVID-19-data.csv"

# get the csv
response = requests.get(url, stream=True, verify=False)

# Throw an error for bad status codes
response.raise_for_status()

#save the file
with open('covid19.csv', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)

rows = []
reader = csv.reader(open('covid19.csv', "r"))


for row in reader:
    rows.append(row)



print(rows[len(rows)-1])
row = rows[len(rows)-1]

parsedData = []
parsedData.append((int(row[7]),'Western'))
parsedData.append((int(row[8]),'Northern'))
parsedData.append((int(row[9]),'Eastern'))
parsedData.append((int(row[10]),'Central'))

for row in parsedData:
    print(row)

def updateDatabase(SSHTunnelForwarder):
    
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
            i=3
            try:


                with conn.cursor() as cursor:
        
                    

                    for row in parsedData:        

                        print (row)
                        sql = """UPDATE CovidCasesNovaScotia SET `NumberOfCases` = %s WHERE (`RegionName` = %s);"""
                        cursor.execute(sql,  row)
                        conn.commit()

                        
            finally:
                conn.close()
                print ("Done")


updateDatabase(SSHTunnelForwarder)
