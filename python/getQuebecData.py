import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup
import re
import pymysql
from sshtunnel import SSHTunnelForwarder


url = "https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/"

# get the website
response = requests.get(url, stream=True)

# Throw an error for bad status codes
response.raise_for_status()

#parse the response for html
soup = BeautifulSoup(response.text, 'html.parser')

# narrow down the amount of code by parsing for the main content and searching for p
rows = soup.find(class_="contenttable").find_all("p")






def first2(s):
    return s[:2]


def intTryParse(value):
    try:
        print (int(value))
        return int(value), True
    except ValueError:
        return value, False

def parseData(rows):
    
    regionData = []
    i = 3

    if rows[0].getText() == "Regions":
            

        while i < 38 and i < len(rows):
            row = rows[i].get_text()
            print (str(i) +" " + row)
            regionData.append({ 'id':first2( row ) ,  'regionName': row , 'numberCases': (re.sub(r"\s+", "", rows[i + 1].getText(), flags=re.UNICODE))})
            i+=2
        return regionData

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
        
                    

                    for row in parsedData:
                        
                        varin = (int(row.get('numberCases')), int(row.get('id')))
                        print(varin)
                        sql = """UPDATE CovidCasesQuebec SET `NumberOfCases` = ' %s' WHERE (`ID` = ' %s');"""
                        cursor.execute(sql,  varin )
                        conn.commit()
            finally:
                conn.close()


updateDatabase(SSHTunnelForwarder, pymysql, parseData(rows))








