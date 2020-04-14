import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup
import re
import pymysql
from sshtunnel import SSHTunnelForwarder


url = "http://www.bccdc.ca/health-info/diseases-conditions/covid-19/case-counts-press-statements"

# get the csv
response = requests.get(url, stream=True)
# Throw an error for bad status codes

response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.find(class_="content-body").find_all('li')





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
            i=3
            try:


                with conn.cursor() as cursor:
        
                    

                    while i < 8 and i < len(rows):
                        row = rows[i].get_text()

                        datain = (row[:row.find('i')].strip() , row[row.find('n') +1:].strip())
                        
                        print (datain)
                        sql = """UPDATE CovidCasesBC SET `NumberOfCases` = %s WHERE (`RegionName` = %s);"""
                        cursor.execute(sql,  datain)
                        conn.commit()
                        i += 1
            finally:
                conn.close()


updateDatabase(SSHTunnelForwarder, pymysql,rows)
