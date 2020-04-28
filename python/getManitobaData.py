import requests 
from contextlib import closing
import csv
import sqlite3
from bs4 import BeautifulSoup
import re
import pymysql
import json
from sshtunnel import SSHTunnelForwarder
from datetime import date , timedelta


def parsedDataIntoRows(response):
        #parse the response for html
    soup = BeautifulSoup(response.text, 'html.parser')

    # narrow down the amount of code by parsing
    rows = json.loads(soup.find('script', type='application/json').text)

    global parsedData

    x =  rows['x']['data']

    cases = x[0]['x']
    regions = x[0]['y']

    
    i = 0

    while i < len(cases):
        parsedData.append((cases[i], regions[i]))
        i+=1

    updateDatabase(SSHTunnelForwarder)
    


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
                        print(row)       
                        sql = """UPDATE CovidCasesManitoba SET `NumberOfCases` = %s WHERE (`RegionName` = %s);"""
                        cursor.execute(sql,  row)
                        conn.commit()

                        
            finally:
                conn.close()
                print ("Done")


today = str(date.today()).replace("-",'')
yesterday = str(date.today() - timedelta(days=1)).replace("-",'')


url = "https://manitoba.ca/health/publichealth/public_app/By_RHA_"+today+".html"
urly = "https://manitoba.ca/health/publichealth/public_app/By_RHA_"+yesterday+".html"

parsedData = []

try:
    # get the website
    response = requests.get(url, stream=True)
    #throw error if invalid
    response.raise_for_status()
    print(today)
    parsedDataIntoRows(response)
except:
    #print the error and default back to the previous days data
    response = requests.get(urly, stream=True)
    response.raise_for_status()
    print(yesterday)
    parsedDataIntoRows(response)