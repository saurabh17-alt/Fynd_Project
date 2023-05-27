# update,delete, fetchone and fetchall
import mysql.connector
from login import *

db = mysql.connector.connect(
    host= host,
    user = user,
    password = password,
    database=database
)

cur = db.cursor()


def exist_mail(m):
    cur.execute("SELECT email from user_details;")
    fall = cur.fetchall()
    for i in fall:
        e = i[0]
        if m.lower() == e.lower():
            return True 
    return False

def insert_data(name,email,pwd):
    query = "INSERT INTO user_details(user_name, email,user_password) VALUES (%s,%s,%s);"
    val = [name,email,pwd]
    cur.execute(query,val)
    db.commit()

def check_mail_pwd(mail,pwd):
    if exist_mail(mail)==True:
        query = "SELECT user_password from user_details WHERE email = %s;"
        cur.execute(query,[mail])
        passwd = cur.fetchone()[0]
        if passwd==pwd:
            return True
        else:
            return False

    else:
        return False

def get_info(v):
    query = "SELECT * from user_details WHERE email = %s;"
    cur.execute(query,[v])
    all_data = cur.fetchone()
    return all_data


def update_info(id_number,updated_list):
    l1 = updated_list
    l1.append(id_number)
    query = "UPDATE user_details SET user_name='%s',email='%s', user_password='%s', secret_key='%s' WHERE user_id=%d;"%tuple(l1)
    cur.execute(query)
    db.commit()


def get_all():
    cur.execute("SELECT * from user_details;")
    fall = cur.fetchall()
    l = [list(i) for i in fall] 
    return l


def get_info_using_id(v):

    query = "SELECT * from user_details WHERE user_id = %d;"%v
    cur.execute(query)
    all_data = cur.fetchone()
    return all_data

def get_specific_report(v):
    query = "SELECT * from reports WHERE user_id = %d;"%v
    cur.execute(query)
    all_data = cur.fetchall()
    return list(all_data)

def get_all_reports():
    cur.execute("SELECT * from reports;")
    fall = cur.fetchall()
    l = [list(i) for i in fall] 
    return l

def delete_user(v):
    query = "DELETE FROM user_details WHERE user_id = %d;"%v
    cur.execute(query)
    db.commit()
    
def delete_row_report(v):
    query = "DELETE FROM reports WHERE report_id = %d;"%v
    cur.execute(query)
    db.commit()

def upload_pdf_file(insert_blob_tuple):
    sql_insert_blob_query = " INSERT INTO reports (user_id, File_name, note, file_data) VALUES (%s,%s,%s,%s);"
    cur.execute(sql_insert_blob_query, insert_blob_tuple)
    db.commit()


def fetch_pdf_file_data(report_id):
    sql_fetch_blob_query = "SELECT file_data from reports where report_id = %d"%report_id
    cur.execute(sql_fetch_blob_query)
    record = cur.fetchall()
    record = record[0]

    return record

def get_file_name(report_id):
    sql_fetch_blob_query = "SELECT File_name from reports where report_id = %d"%report_id
    cur.execute(sql_fetch_blob_query)
    fname = cur.fetchall()
    fname = fname[0][0]

    return fname


def get_same_id(v):
    query = "SELECT report_id from reports where user_id = %d"%v
    cur.execute(query)
    all_users_data = cur.fetchall()

    return all_users_data

def check_secret_key(mail,s):
    query = "SELECT secret_key from user_details WHERE email = %s;"
    cur.execute(query,[mail])
    sk = cur.fetchone()[0]
    if sk==s:
        return True
    else:
        return False


def update_pwd(newpassword,mail):
        query = "UPDATE user_details SET user_password = %s WHERE email = %s;"
        cur.execute(query,[newpassword,mail])
        db.commit()


def admin_data():
    query = "SELECT * from user_details WHERE user_id = 1000;"
    cur.execute(query)
    admin_data = cur.fetchone()
    m = admin_data[2]
    p = admin_data[3]

    return m,p


# print(admin_data())

# insert_data("saurabh","saurabh@gmail.com","1234")




