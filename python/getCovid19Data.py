

import requests 
from contextlib import closing
import csv
import sqlite3
import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder
import geocoder


#csv file download link
url = "https://github.com/ishaberry/Covid19Canada/raw/master/cases.csv"

# get the csv
##response.raise_for_status()

#save the file
#with open('covid19Canada.csv', 'wb') as handle:
#   for block in response.iter_content(1024):
#        handle.write(block)

rows = []
with open('covid19Canada.csv', newline='',encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    parsedData = []

    #connect to sqlite DB
    connection = sqlite3.connect('CanadaCovidResults.db')
    c = connection.cursor()

    c.execute("DROP TABLE IF EXISTS `CovidCasesIshaBerry`")


    c.execute("""CREATE TABLE IF NOT EXISTS `CovidCasesIshaBerry` (
    `case_id` int(11) DEFAULT NULL,
    `provincial_case_id` int(11) DEFAULT NULL,
    `age` text DEFAULT NULL,
    `sex` text DEFAULT NULL,
    `health_region` text DEFAULT NULL,
    `province` text DEFAULT NULL,
    `country` text DEFAULT NULL,
    `date_report` text DEFAULT NULL,
    `report_week` text DEFAULT NULL
    )""")

    c.execute("DELETE FROM `CovidCasesIshaBerry`")
    for row in reader:
        dataIn = (int(row['case_id']),int(row['provincial_case_id']),row['age'],row['sex'],str(row['health_region']),row['province'],row['country'],row['date_report'],row['report_week'])
        c.execute("""INSERT INTO CovidCasesIshaBerry ( case_id, provincial_case_id, age, sex, health_region, province, country, date_report, report_week) VALUES (?,?,?,?,?,?,?,?,?);""", dataIn)
        

        
    connection.commit()

    rows = c.execute("SELECT  count(case_id), health_region,province FROM CovidCasesIshaBerry GROUP BY health_region,province").fetchall()

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
                    cursor.execute("DELETE FROM CaseRegions")
                    
            finally:
                conn.commit()

            try:


                with conn.cursor() as cursor:
        
                    

                    for row in rows:  
                        g = geocoder.google(row[1] + "," + row[2])
                        latlong = g.latlong
                        if latlong is not None:
                            row[3] = latlong
                            sql = "INSERT INTO CaseRegions (NumberOfCases,HealthRegion,Province,LatLong) VALUES (%s,%s,%s,%s);"
                        else:
                            sql = "INSERT INTO CaseRegions (NumberOfCases,HealthRegion,Province) VALUES (%s,%s,%s);"
                        cursor.execute(sql, row )
                        print(row)
                        conn.commit()
            finally:
                conn.close()








