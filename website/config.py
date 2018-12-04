import os

class Config:
    SECRET_KEY = '38792F423F4528482B4B625065536856' #Secret Key, wird für die Passwortverschlüsselung verwendet. Dieser muss gesetzt werden damit der Webserver funktioniert.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cfrags.db' #Datenbank Uri, dieser pfad gibt an wo genau sich das Datenbankfile befindet.
    MAIL_SERVER = 'smtp.googlemail.com'             #Mailserver, dies ist der mailserver link - NICHT IN PRODUKTION
    MAIL_PORT = 587                                 #Mailport, Port des Mailservers - NICHT IN PRODUKTION
    MAIL_USE_TLS = True                             #TLS wird verwendet - NICHT IN PRODUKTION
    MAIL_USERNAME = os.environ.get('EMAIL_USER')    #Mail User - Username - NICHT IN PRODUKTION
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')    #Mail User - Passwort - NICHT IN PRODUKTION
