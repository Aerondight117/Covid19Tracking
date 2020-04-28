import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup
import re
import pymysql
from sshtunnel import SSHTunnelForwarder
import json


url = "https://services8.arcgis.com/aCyQID5qQcyrJMm2/arcgis/rest/services/RHA_CurrentStats2_Public/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=name&outStatistics=%5B%7B%22statisticType%22%3A%22max%22%2C%22onStatisticField%22%3A%22total_number_of_cases%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&resultType=standard&cacheHint=true"

# get the website
response = requests.get(url, stream=True)

# Throw an error for bad status codes
response.raise_for_status()

#parse the response for html
soup = json.loads(BeautifulSoup(response.text, 'html.parser').text)
parsedData=[]

# narrow down the amount of code by parsing for the main content and searching for p
for row in soup['features']:
    parsedData.append(row['attributes'])



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
                        
                        dataIn = (row['value'],row['name'])       
                        print(dataIn)
                        sql = """UPDATE CovidCasesNFL SET `NumberOfCases` = %s WHERE (`RegionName` = %s);"""
                        cursor.execute(sql,  dataIn)
                        conn.commit()

                        
            finally:
                conn.close()
                print ("Done")


updateDatabase(SSHTunnelForwarder)