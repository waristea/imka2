 #project/controllers.py
from flask import flash, render_template, request, session, redirect, url_for, json, jsonify
from flask_login import current_user, login_user, logout_user
import smtplib

ADMIN_EMAIL = "waristea@gmail.com"
ADMIN_ACCESS_CODE = "uubcprkertzvurnv"

def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    else:
        return render_template('login.html')

def login():
    # if login is being done
    if request.method=='POST':
        # check login credentials
        from project.models import User
        from werkzeug import check_password_hash

        if request.form['email'] != None and request.form['password'] != None:
            user = User.query.filter_by(email=request.form['email']).first()
            password = request.form['password']

            if user and check_password_hash(user.password, password):
                if user.admin:
                    print("Logged in!")
                    login_user(user)
                else:
                    print("Credentials true, but not an admin")
            else:
                print("Log in credentials are false")
        else:
            print("Please fill in the email and password!")

    # if login page iss fetched
    elif request.method=='GET':
        # Login page is fetched
        print("Login page is fetched usign GET directly!")
        #return index()
    return redirect(url_for('index'))

def register():
    # if login is being done
    if request.method=='POST':
        if request.form['email'] != None:
            if request.form['name']!=None:
                from project.models import User
                from project import db

                email = request.form['email']
                password = request.form['password']
                name = request.form['name']

                user = User(email=email, password=password, name=name, admin=True)
                try:
                    db.session.add(user)
                    db.session.commit()
                    status = 'success'
                except Exception as e:
                    print("Error : " + str(e))
                    status = 'this user is already registered'
                print(status)
                db.session.close()
            else:
                return flash('please fill in all the creds')
        else:
            return flash('please fill in the email!')
    elif request.method=='GET':
        print("Signup page is fetched using GET directly!")
        return render_template('signup.html')
    return index()

def logout():
    logout_user()
    session.pop('logged_in', None)
    return redirect(url_for('index'))

# Untuk RekSTI
# Read
def request_detail(request_id):
    from project import app
    from project.models import Request
    import json

    open_requests_dict = []
    try:
        open_requests = Request.query.filter_by(id=request_id)
        open_requests_dict = []
        for r in open_requests:
            open_requests_dict.append(r.get_dict())

    except Exception as e:
        print(e)
    else:
        # TBD : route to view
        for r in open_requests_dict:
            print(r['id'])

def request_all():
    from project import app
    from project.models import Request
    import json

    open_requests_dict = []
    try:
        open_requests = Request.query.all()
        for r in open_requests:

            open_requests_dict.append(r.get_dict())

    except Exception as e:
        print(e)
    else:
        # TBD : route to view
        for r in open_requests_dict:
            print(r['id'])
            out = json.dumps(r, indent=4, sort_keys=True, default=str)
        print(out)
        return render_template("request_list.html", dict=open_requests_dict)
    return render_template("index.html")
    """
    response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response
    """

# Read all

# API
# Create
def api_request_create():
    from project import app, db
    from project.models import User, Request
    import datetime, json

    json_data = request.get_json()
    print(json_data)

    """
    today_pure = (datetime.datetime.now() + datetime.timedelta(hours=7))
    today = today_pure.isocalendar()
    """
    # today = datetime.datetime.now()

    open_request = Request(photo=json_data['photo'])
    data = {} # To report to IoT device
    try:
        db.session.add(open_request)
        db.session.commit()
        # Writing email
        user_list = User.query.all()

        names = []
        targets = []

        for user in user_list:
            names.append(user.name)
            targets.append(user.email)
        """
        subject = "Notification"
        body = "There are new door request, please check website for further info."

        send_email(ADMIN_EMAIL, targets, subject, body, ADMIN_ACCESS_CODE)
        """
        # Reporting to IoT Device
        data['creation_status'] = 'successful'
        data['message'] = 'Request creation successful. You can check request status by looking at http://imka.herokuapp.com/request/<request_id> or http://imka.herokuapp.com/api/request/<request_id>'
        data['request_id'] = open_request.get_id()
        data['request'] = json.dumps(open_request.get_dict(), indent=4, sort_keys=True, default=str)

        db.session.close()
    except Exception as e:
        data['status'] = 'failed'
        data['message'] = 'exception occured, please contact admin'
        print(e)
    else:
        response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )

    return response
# Read
def api_request_detail(request_id):
    from project import app
    from project.models import Request
    import json

    #json_data = request.get_json()
    #print(json_data)
    open_requests_dict = []
    data = {}
    try:
        open_requests = Request.query.filter_by(id=request_id)
        for r in open_requests:
            open_requests_dict.append(r.get_dict())
        data['status'] = 'successful'
        data['requests'] = json.dumps(open_requests_dict, indent=4, sort_keys=True, default=str)
    except Exception as e:
        data['status'] = 'failed'
        data['message'] = 'exception occured, please contact admin'
        print(e)

    response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Email
def send_email(from_addr, to_addr_list, subject, body, gmail_password, smtp_server = 'smtp.gmail.com', port = 587):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr_list[0]
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # SMTP_SSL Example
    server_ssl = smtplib.SMTP(smtp_server, port)
    server_ssl.ehlo() # optional, called by login()
    server_ssl.starttls()
    server_ssl.login(from_addr, gmail_password)
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
    server_ssl.sendmail(from_addr, to_addr_list, msg.as_string())
    #server_ssl.quit()
    server_ssl.quit()
    print('successfully sent the mail')
