 #project/controllers.py
from flask import flash, render_template, request, session, redirect, url_for, json, jsonify
from flask_login import current_user, login_user, logout_user
import smtplib

# Reminder:
# - Buat jadwal
# - Query user based on name
# - Implement absen ke api
# - Buat form input (banyak..)

def index():
    if current_user.is_authenticated:
        print(current_user.get_id())
        return redirect(url_for('schedule'))
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
    return index()

def register():
    # if login is being done
    if request.method=='POST':
        if request.form['email'] != None:
            if request.form['name']!=None:
                from project.models import User
                from project import db

                email = request.form['email']
                password = "123456"
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

def schedule():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        from project.models import User, Schedule
        from project import db
        o_user_list = User.query.all()
        user_name_list = []
        for o in o_user_list:
            user_name_list.append(o.get_name())
        if request.method=='POST':
            if request.form['name']!=None and request.form['date']!=None:
                from project.models import User
                from project import db
                import dateutil.parser as dt

                name = request.form['name']
                date = dt.parse(request.form['date'])
                activity = request.form['activity']

                print(name)
                print(date)
                print(activity)

                if activity==None: activity=""

                print(activity)


                user = User.query.filter_by(name=name).first()
                user_id = user.get_id()

                schedule = Schedule(user_id, activity, date)
                try:
                    db.session.add(schedule)
                    db.session.commit()
                    status = 'success'
                except Exception as e:
                    print("Error : " + str(e))
                    status = 'failed'
                print(status)
                db.session.close()


                return render_template('scheduleform.html', user_name_list=user_name_list, message="Add is successful!")
            else:
                return render_template('scheduleform.html', user_name_list=user_name_list, message="Please fill in all the textboxes!")
        else:# request.method=='GET':
            return render_template('scheduleform.html', user_name_list=user_name_list)

def analytics():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        from project.models import User, Presence
        from project import db
        import datetime

        o_presence_list = Presence.query.all()

        filtered_presence_dict_list = []

        kali_hadir_dict = {}

        today = datetime.datetime.now()

        for o in o_presence_list:
            p_dict = o.get_dict()
            kali_hadir_dict[p_dict['owner']] = 0

        for o in o_presence_list:
            p_dict = o.get_dict()
            time = p_dict["time"]
            if(time.month==today.month):
                kali_hadir_dict[p_dict['owner']] += 1

        nama = ["None"] * len(kali_hadir_dict)
        kali_hadir = [0] * len(kali_hadir_dict)
        persentase = [0.00] * len(kali_hadir_dict)

        tanggal = today.date

        print(kali_hadir_dict)
        i = 0
        for k, v in kali_hadir_dict.items():
            nama[i] = k
            kali_hadir[i] = v
            persentase[i] = (v/today.day)*100
            i += 1
        print(nama)
        print(kali_hadir)
        print(persentase)

        return render_template('kehadiranpegawai.html', nama=nama, kali_hadir=kali_hadir, persentase=persentase)


# Untuk RekSTI
# API
# Create
def api_presence_add():
    from project import app, db
    from project.models import User, Presence, Schedule
    import datetime

    json_data = request.get_json()
    print(json_data)
    user_name = json_data['owner']
    user = User.query.filter_by(name=user_name).first()

    data = {}
    if user==None:
        data['status'] = 'failed'
        data['message'] = 'person is not registered'

        response = app.response_class(
            response = json.dumps(data),
            status=400,
            mimetype='application/json'
        )
    else:
        presence = Presence.query.filter_by(owner=user.get_id()).order_by(Presence.time.desc()).first()
        today_pure = (datetime.datetime.now() + datetime.timedelta(hours=7))
        today = today_pure.isocalendar()

        if (presence==None or presence.time.date()!=today_pure.date()):

            user_id = user.get_id()
            presence = Presence(user_id, today_pure)

            try:

                db.session.add(presence)
                db.session.commit()

                gmail_user = "waristea@gmail.com"
                gmail_password = "uubcprkertzvurnv"

                to = [user.email]
                subject = "Notification"
                body = "You are marked as present."

                user_id = user.get_id()
                schedule_list = Schedule.query.filter_by(owner=user_id).all()

                print(len(schedule_list))
                print(today)

                for s in schedule_list:
                    s_dict = s.get_dict()
                    time = s_dict["time"]
                    print(time.isocalendar())
                    print(today)
                    print(s_dict["text"])

                    if(time.isocalendar()==today):
                        print("IN!!!!!!!!!!")
                        body = "You are marked as present.\n Here are your schedules:\n " + s_dict["text"]

                send_email(gmail_user, to, subject, body, gmail_password)

                data['status'] = 'successful'
                data['message'] = 'user is marked as present'
                data['user'] = user.serialize()

            except Exception as e:
                data['status'] = 'failed'
                data['message'] = 'expection occured, please contact admin'
                print(e)
            db.session.close()
        else:

            data['status'] = 'successful'
            data['message'] = 'user has already been marked as present'
            data['user'] = user.serialize()

        response = app.response_class(
            response = json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    print("Yes")

    return response
# Read
def api_presence_today():
    from project import app, db
    from project.models import Presence
    from sqlalchemy import Date, cast
    import datetime
    #json_data = request.get_json()
    #print(json_data)# Seharusnya gk ada
    o_presence_list = db.session.query(Presence).filter(cast(Presence.time,Date) == datetime.date.today()).all()

    presence_list = []

    for p in o_presence_list:
        presence_list.append(p.get_dict())

    print(presence_list)

    response = app.response_class(
        response = json.dumps(presence_list),
        status=200,
        mimetype='application/json'
    )
    return response

def api_presence_detail_by_user(user_id):
    from project import app
    from datetime import date

    #json_data = request.get_json()
    #print(json_data)



    data = {'status' : 'successful'}

    response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

def api_presence_detail_by_id(presence_id):
    from project import app

    #json_data = request.get_json()
    #print(json_data)

    data = {'status' : 'successful'}

    response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response
# Update
def api_presence_update(presence_id):
    from project import app

    json_data = request.get_json()
    print(json_data)

    data = {'status' : 'successful'}

    response = app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype='application/json'
    )
    return response

# Delete
def api_presence_delete(presence_id):
    from project import app

    json_data = request.get_json()
    print(json_data)

    data = {'status' : 'successful'}

    response = app.response_class(
        response = json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

# Gunakan password dan username yagn disediakan google
def send_email(from_addr, to_addr_list, subject, body, gmail_password, smtp_server = 'smtp.gmail.com', port = 465):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr_list[0]
    msg['Subject'] = "SUBJECT"
    msg.attach(MIMEText(body, 'plain'))

    # SMTP_SSL Example
    server_ssl = smtplib.SMTP("smtp.gmail.com", 587)
    server_ssl.ehlo() # optional, called by login()
    server_ssl.starttls()
    server_ssl.login(from_addr, gmail_password)
    # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
    server_ssl.sendmail(from_addr, to_addr_list, msg.as_string())
    #server_ssl.quit()
    server_ssl.quit()
    print('successfully sent the mail')
