import os

class Config:
    SECRET_KEY = '38792F423F4528482B4B625065536856' #Secret Key, wird für die Passwortverschlüsselung verwendet. Dieser muss gesetzt werden damit der Webserver funktioniert.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cfrags.db' #Datenbank Uri, dieser pfad gibt an wo genau sich das Datenbankfile befindet.
