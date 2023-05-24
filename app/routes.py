from flask import Flask,redirect,render_template,request,flash,session,send_file
import database
import mysql.connector
import os
from werkzeug.utils import secure_filename

from app import app

login_status = False
Email = None
ID = None
info = None
admin_status = False
user_status = False
user_id = None
user_flag = False
file_path = ""

path_cwd = os.getcwd()
pa_th = path_cwd+"/"+"pdf_files"

@app.route("/", methods = ["POST","GET"])
@app.route("/home", methods = ["POST","GET"])
def home():
    msg = ""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        pwd = request.form.get("password")
        confirm_pwd = request.form.get("confirm_pswd")

        if database.exist_mail(email) == True:
            msg = "Email Already exist."
            return render_template("home.html",msg=msg,name=name,email=email,pwd=pwd,confirm_pwd=confirm_pwd)
        else:
            if pwd == confirm_pwd:
                database.insert_data(name,email,pwd)
                msg = ""
            else:
                msg = "Password miss match!"
                return render_template("home.html",msg=msg,name=name,email=email,pwd=pwd,confirm_pwd=confirm_pwd)

    return render_template("home.html",msg=msg)


@app.route("/forget",methods = ["POST","GET"])
def forget():
    return render_template("forgotpwd.html")

@app.route("/reset",methods = ["POST","GET"])
def reset():
    if request.method == "POST":
        secretkey = request.form.get("secretkey")
        email = request.form.get("email")
        newpwd = request.form.get("password")

        f = database.check_secret_key(email,secretkey)

        if f == True:
            database.update_pwd(newpwd,email)

    return redirect("/")


@app.route("/Login",methods = ["POST","GET"])
def login():
    global Email,admin_status,login_status,user_status,ID
    if request.method == "POST":
        email = request.form.get("email")
        pwd = request.form.get("password")

        admin_mail,admin_p = database.admin_data()

        if email == admin_mail and pwd == admin_p:
            Email = email
            admin_status = True
            login_status = True
            return redirect("/Admin")
        else:
            f = database.check_mail_pwd(email,pwd)
            if f == True:
                msg = ""
                Email = email
                user_status = True
                login_status = True
                ID = database.get_info(Email)[0]
                # flash("Login Successfully")
                return redirect("/User")

            else:
                msg = "Invalid Credentials."
                return render_template("home.html",msg_login=msg)

@app.route("/Update",methods = ["POST","GET"])
def update():
    if login_status == True:
        global info,ID,user_id,user_flag
        user_id = request.args.get("UID")
        if user_id == None:
            info = list(database.get_info(Email))
            ID = info[0]
            n = info[1]
            e = info[2]
            num = info[3]
            p = info[4]
            ast = admin_status
            ust = user_status
        else:
            user_id = int(user_id)
            info = list(database.get_info_using_id(user_id))
            ID = info[0]
            n = info[1]
            e = info[2]
            num = info[3]
            p = info[4]
            ast = admin_status
            ust = user_status
            user_flag = True
            user_id = None
        return render_template("update_info.html",n=n,e=e,num=num,p=p,ast=ast,ust=ust)
    else:
        return redirect("/")


@app.route("/User",methods = ["POST","GET"])
def user():
    if login_status == True:
        all_report_data = database.get_specific_report(ID)
        all_data = all_report_data
        n = len(all_data)
        return render_template("user.html",all_data = all_data,n=n)
    else:
        return redirect("/")

@app.route("/Admin",methods = ["POST","GET"])
def admin():
    if (login_status == True) and (admin_status==True):
        all_data = database.get_all()
        return render_template("admin.html",all_data = all_data)
    else:
        return redirect("/")


@app.route("/Save",methods = ["POST","GET"])
def save():
    if login_status == True:
        global user_flag
        n1 = request.form.get("n1")
        e1 = request.form.get("e1")
        num1 = request.form.get("num1")
        p1 = request.form.get("p1")
        database.update_info(int(ID),[n1,e1,num1,p1])
        if user_flag == True:
            user_flag = False
            return redirect("/Admin")
        else:   
            return redirect("/Update")
    else:
        return redirect("/")

@app.route("/Upload",methods = ["POST","GET"])
def upload():
    global file_path
    if login_status == True:
        if request.method == "POST":
            filel = request.files["file_name"]
            file_name = filel.filename
            p = path_cwd + os.path.join('/pdf_files',secure_filename(filel.filename))

            filel.save(p)
            with open(p, 'rb') as file:
                binaryData = file.read()

            file_data = binaryData

            insert_blob_tuple = [int(ID), file_name, "report", file_data]
            database.upload_pdf_file(insert_blob_tuple)

            if os.path.isfile(p):
                os.remove(p)

            return render_template("upload.html")

        return render_template("upload.html")

    else:
        return redirect("/")


@app.route("/delete",methods = ["POST","GET"])
def delete():
    if (login_status == True) and (admin_status==True):
        global user_id
        user_id = request.args.get("UID")
        user_id = int(user_id)
        sameids = database.get_same_id(user_id)
        database.delete_user(user_id)
        if len(sameids) != 0:
            for i in sameids:
                database.delete_row_report(int(i[0]))
        return redirect("/Admin")

    else:
        return redirect("/")


@app.route("/Report",methods = ["POST","GET"])
def Report():
    if (login_status == True) and (admin_status==True):
        all_report_data = database.get_all_reports()
        nl = len(all_report_data)

        return render_template("report.html",all_data = all_report_data,nl = nl)
    else:
        redirect("/")


@app.route("/deletereport",methods = ["POST","GET"])
def deletereport():
    if login_status == True:
        global user_id
        report_id = request.args.get("report_id")
        report_id = int(report_id)
        database.delete_row_report(report_id)
        report_id = None
        if (admin_status == True) and (user_status==False):
            return redirect("/Report")
        else:
            return redirect("/User")
    else:
        return redirect("/")


@app.route("/downloadreport",methods = ["POST","GET"])
def downloadreport():
    global user_id
    if login_status == True:

        dir_name = os.listdir(pa_th)
        if len(dir_name) != 0:
            for i in dir_name:
                delflpath  = pa_th+"/"+i
                os.remove(delflpath)

        report_id = request.args.get("report_id")
        report_id = int(report_id)
        fdata = database.fetch_pdf_file_data(report_id)
        fname = database.get_file_name(report_id)

        fname  = pa_th +"/"+fname
        filed = open(fname, 'wb')
        for i in fdata:
            filed.write(i)
        filed.close()
        report_id = None

        return send_file(fname,as_attachment=True)
    else:
        return redirect("/")

@app.route("/logout",methods = ["POST","GET"])
def logout():
    global login_status,Email,ID,info,admin_status,user_status,user_id,user_flag,file_path
    file_path = ""
    login_status = False
    Email = None
    ID = None
    info = None
    admin_status = False
    user_status = False
    user_id = None
    user_flag = False
    return redirect("/")