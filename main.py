from flask import Flask, render_template , request
from markupsafe import escape
import sqlite3
import os
import json
import hashlib
import random
import in_house.email_sender as email
import datetime
from markupsafe import Markup

###CONFIGS
shortened_length = 5
random_charset = ['a', 'b','c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's','t', 'u', 'v', 'w', 'x', 'y', 'z' , 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' , '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
additional_letters = 1



app = Flask(__name__)



def gta5(variables):
    returnable = ()
    for variable in variables:
        if variable:
            returnable = returnable + (variable.strip(),)
        else:
            returnable = returnable + (variable,)
    else:
        return returnable

con = sqlite3.connect("main.db", check_same_thread=False)
cur = con.cursor()
#cur.execute("CREATE TABLE all_shortened (original_url VARCHAR(4096), shortened_hash VARCHAR(256), email_creator VARCHAR(512), expiry VARCHAR(16), authenticated INTEGER);")


checking_main = cur.execute("SELECT name FROM sqlite_master").fetchall()
if "all_shortened" not in checking_main:
    pass
else:
    print("NO TABLE")


@app.route("/" ,methods = ['GET'])
def main_shorten():
    return render_template('main.html')

@app.route("/make_short_url" ,methods = ['POST'])
def shortening_api():
    data = request.get_json()

    url_to_shorten = data["urlToShorten"]
    if url_to_shorten != None:
        
        email = data["email"]
        expiry_date = data["expiryDate"]
        allowed_emails = data["allowedEmails"]
        url_to_shorten , email , expiry_date , allowed_emails = gta5([url_to_shorten , email , expiry_date , allowed_emails])


        full_hash = hashlib.sha256(url_to_shorten.encode()).hexdigest()
        hash_trimming = False
        trimmed_hash = full_hash[:shortened_length:]

        while not hash_trimming:
            hash_use_check = cur.execute("SELECT count(*) FROM all_shortened WHERE shortened_hash=? ;" , (trimmed_hash ,)).fetchone()
            if hash_use_check[0] != 0:
                more_letters = ""
                for x in range(additional_letters):
                    more_letters = more_letters + random.choice(random_charset)
                trimmed_hash = trimmed_hash + more_letters
            else:
                if allowed_emails:
                    a_e = 1
                else:
                    a_e = 0
                cur.execute("INSERT INTO all_shortened VALUES(?, ?, ? , ? , ?) ;" , (url_to_shorten , trimmed_hash , email ,expiry_date, a_e,)).fetchone()
                con.commit()
                hash_trimming = True
        
        if allowed_emails:
            special_table_name = f"table{trimmed_hash}"
            allowed_emails_arr = list(set(allowed_emails.split(",")))
            data_to_insert = []
            cur.execute(f"CREATE TABLE {special_table_name}(emails_allowed VARCHAR(512));" ,)
            
            sql_email_arr = []
            for email in allowed_emails_arr:
                sql_email_arr.append((email,))
            cur.executemany(f"INSERT INTO {special_table_name} VALUES(?);", sql_email_arr)
            con.commit()            
    
    else:
        return {"status":"invalid input"} , 406


    return {"status":"success" , "shortened_url":f"/short/{trimmed_hash}"} , 200

@app.route("/short/<shortened>",methods = ['GET'])
def view_shortened_url(shortened):

    shortened_exists = cur.execute("SELECT count(*) FROM all_shortened WHERE shortened_hash=? ;" , (shortened ,)).fetchone()
    if shortened_exists[0] == 0:
        return render_template('doesnt_exist.html')
    else:
        shortened_url_info = cur.execute("SELECT * FROM all_shortened WHERE shortened_hash=? ;" , (shortened ,)).fetchone()

        og_url = shortened_url_info[0]
        notification_email = shortened_url_info[2]
        expiry_date = shortened_url_info[3]
        auth = int(shortened_url_info[4])

        if expiry_date:
            splitted = expiry_date.split(r"/")
            date , month , year = int(splitted[0]) , int(splitted[1]) , int(splitted[2])
            del splitted

            expiry_as_date = datetime.date(year, month, date)
            today_date = datetime.date.today()


            if expiry_as_date < today_date:
                if auth == 1:
                    cur.execute(f"DROP TABLE ?" , (shortened,))
                else:
                    pass
                cur.execute(f"DELETE FROM all_shortened WHERE shortened_hash=?;" , (shortened,))
                con.commit()
                return render_template('doesnt_exist.html')

        if auth == 1:
            return render_template('auth_short.html' , hash = Markup(shortened))

        if notification_email:
            email.notify(notification_email, og_url , shortened , "notify")

        return render_template('short.html' , og_url = Markup(og_url))

@app.route("/auth",methods = ['POST'])
def view_auth_url():
    data = request.get_json()
    short_url_hash = data["shortenedUrl"]
    email_address_given = data["email"]

    shortened_exists = cur.execute("SELECT count(*) FROM all_shortened WHERE shortened_hash=? ;" , (short_url_hash ,)).fetchone()
    if shortened_exists[0] == 0:
        return render_template('doesnt_exist.html')
    else:
        shortened_url_info = cur.execute("SELECT * FROM all_shortened WHERE shortened_hash=? ;" , (short_url_hash  ,)).fetchone()

        og_url = shortened_url_info[0]
        notification_email = shortened_url_info[2]
        expiry_date = shortened_url_info[3]
        auth = int(shortened_url_info[4])

        if expiry_date:
            splitted = expiry_date.split(r"/")
            date , month , year = int(splitted[0]) , int(splitted[1]) , int(splitted[2])
            del splitted

            expiry_as_date = datetime.date(year, month, date)
            today_date = datetime.date.today()


            if expiry_as_date < today_date:
                if auth == 1:
                    cur.execute(f"DROP TABLE ?" , (short_url_hash,))
                else:
                    pass
                cur.execute(f"DELETE FROM all_shortened WHERE shortened_hash=?;" , (short_url_hash,))
                con.commit()
                return render_template('doesnt_exist.html')

        if auth == 0:
            if notification_email:
                email.notify(notification_email, og_url , short_url_hash , "notify")
            return render_template('short.html' , og_url = Markup(og_url))

        allowed_emails = cur.execute(f"SELECT * FROM table{short_url_hash};").fetchall()
        print(allowed_emails)
        if (email_address_given.strip(),) in allowed_emails:
            email.notify(email_address_given, og_url , short_url_hash , "walled")
        
        return {"message":"If the email exists and has been allowed by the link creator, then the orignal URL has been sent."}

        