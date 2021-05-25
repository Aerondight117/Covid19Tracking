import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup
import re
import pymysql
from sshtunnel import SSHTunnelForwarder


def getNumber(string):
    return string[:string.find(" ")]

url = "https://www.princeedwardisland.ca/en/information/health-and-wellness/pei-covid-19-testing-data"

# get the website
response = requests.get(url, stream=True)

# Throw an error for bad status codes
response.raise_for_status()

#parse the response for html
soup = BeautifulSoup(response.text, 'html.parser')

# narrow down the amount of code by parsing for the main content and searching for p
rows = soup.find(class_='field-items').find_all("td")


lenthOfRows =len(rows)
parsedData = []


kingsRow = rows[lenthOfRows-5].text.strip()
queensRow = rows[lenthOfRows-3].text.strip()
princeRow = rows[lenthOfRows-1].text.strip()

parsedData.append((kingsRow,'Kings'))
parsedData.append((queensRow,'Queens'))
parsedData.append((princeRow,'Prince'))

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
                        sql = """UPDATE CovidCasesPEI SET `NumberOfCases` = %s WHERE (`RegionName` = %s);"""
                        cursor.execute(sql,  row)
                        conn.commit()

                        
            finally:
                conn.close()
                print ("Done")


updateDatabase(SSHTunnelForwarder)