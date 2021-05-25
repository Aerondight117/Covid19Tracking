

import requests 
from contextlib import closing
import csv
import sqlite3
import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder


#csv file download link
url = "https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"

# get the csv
response = requests.get(url, stream=True)

# Throw an error for bad status codes
response.raise_for_status()

#save the file
with open('covid19.csv', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)

rows = []
reader = csv.reader(open('covid19.csv', "r"))

parsedData = []

for row in reader:
    rows.append(row)

def updateDatabase(SSHTunnelForwarder, pymysql):
    
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
        
                    i = len(rows) - 15

                    while i < len(rows):
                        row = rows[i]
                        dataIn = (row[1], row[4], row[6],row[8],row[12],row[1])
                        print(row)
                        sql = """Update CovidCasesCanada SET RegionName = %s,NumberOfCases = %s,Deaths= %s,NumberTested= %s, NewCases = %s WHERE RegionName = %s;"""
                        cursor.execute(sql,  dataIn )
                        conn.commit()
                        i+=1
            finally:
                conn.close()
    
updateDatabase(SSHTunnelForwarder, pymysql)