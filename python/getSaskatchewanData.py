import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup
import re
import pymysql
from sshtunnel import SSHTunnelForwarder


def parseRegion(string):

    if string.find('(') > 0:
        return string[:(string.find(" ("))]
    else:
        return string

url = "https://dashboard.saskatchewan.ca/export/cases/1174.csv"

response = requests.get(url, stream=True)

# Throw an error for bad status codes
response.raise_for_status()

#save the file
with open('saskatchewan.csv', 'wb') as handle:
    for block in response.iter_content(1024):
        handle.write(block)

rows = []
reader = csv.reader(open('saskatchewan.csv', "r"))

parsedData = []

for row in reader:
    rows.append(row)




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
            try:


                with conn.cursor() as cursor:
        
                    i = len(rows) - 7

                    while i < len(rows) -1:
                        row = rows[i]
                        print(parseRegion(row[1]),row[4])
                        sql = """UPDATE CovidCasesSaskatchewan SET `NumberOfCases` = %s WHERE (`RegionName` = %s);"""
                        cursor.execute(sql, (row[4],parseRegion(row[1])))
                        conn.commit()
                        i+=1
                                       
            finally:
                conn.close()
                print ("Done")


updateDatabase(SSHTunnelForwarder)