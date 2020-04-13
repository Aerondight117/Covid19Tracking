import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup
import re
import pymysql
from sshtunnel import SSHTunnelForwarder


def first2(s):
    return s[:2]


def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

def parseData(rows):
    
    regionData = []
    i = 3

    if rows[0].getText() == "Regions":
        
        while i < len(rows):
            regionData.append({ 'id':first2( rows[i].getText() ) ,  'regionName': rows[i].getText() , 'numberCases': (re.sub(r"\s+", "", rows[i + 1].getText(), flags=re.UNICODE))})
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
                        if intTryParse(row.get('id')):
                            varin = (int(row.get('numberCases')), int(row.get('id')))
                            print(varin)
                            sql = """UPDATE CovidCasesQuebec SET `number_of_cases` = ' %s' WHERE (`id` = ' %s');"""
                            cursor.execute(sql,  varin )
                            conn.commit()
            finally:
                conn.close()



url = "https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/"

# get the csv
response = requests.get(url, stream=True)
# Throw an error for bad status codes

response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.find(class_="contenttable").find_all("p")

updateDatabase(SSHTunnelForwarder, pymysql, parseData(rows))








