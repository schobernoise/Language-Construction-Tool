import time
import sqlite3
from sqlite3 import Error
import datetime
from lct import log
from lct.utils import utils

# BASIC DB HANDLING
def userTempWerte_db_anlegen():
    # Temperatur-Werte für erste Inbetriebnahme    
    minTempSensor = -50.00 # Messbereich Sensor Untergerenze
    maxTempSensor = 125.00 # Messbereich Sensor Obergrenze
    minTempUser = 20.00 # Benutzerdefinierte Untergrenze der Temperatur
    maxTempUser = 21.00 # Benutzerdefinierte Obergrenze der Temperatur
    connection = sqlite3.connect("/var/www/tempdata.db")
    cursor = connection.cursor()
    # Tabelle erzeugen
    sql = "CREATE TABLE tempWerte("\
        "minTempSensor FLOAT, maxTempSensor FLOAT, minTempUser FLOAT, \
         maxTempUser FLOAT) " 
    cursor.execute(sql)
    # Werte für erste Inbetriebnahme
    sql = "INSERT INTO tempWerte VALUES(" + str(minTempSensor) + ", " \
           + str(maxTempSensor) + ", " \
           + str(minTempUser) + ", " + str(maxTempUser) + ")"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    print "Datenbank tempdata.db mit ", sql ," Inhalt angelegt"