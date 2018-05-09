import json
import urllib.request
import base64

local = "http://127.0.0.1:5000"
remote = "http://imka.herokuapp.com"

def test_api_request_create():
    path = ["/api/request"]

    data = {}
    data['photo'] = "Testing"

    headers = {'content-type': 'application/json'}

    json_data = json.dumps(data).encode('utf8')
    url = local+path[0]
    print(url)
    method = 'POST'

    req = urllib.request.Request(url, data=json_data, headers=headers, method=method)
    response = urllib.request.urlopen(req)

    print(response.read())

def test_api_request_detail(id):
    import json, urllib
    path = ["/api/request/"]

    url = remote+path[0]+str(id)
    print(url)

    response = urllib.request.urlopen(url).read()
    jsonResponse = json.loads(response.decode('utf-8'))
    request = jsonResponse['requests']
    print(request['id'])

def test_api_request_detail_change(id):
    path = ["/api/request/"]

    with open("ruby.jpg", "rb") as image_file:
        photo_string = base64.b64encode(image_file.read())

    data = {}
    data['photo'] = photo_string

    headers = {'content-type': 'application/json'}

    json_data = json.dumps(data, indent=4, sort_keys=True, default=str).encode('utf8')
    url = local+path[0]+str(id)
    print(url)
    method = 'POST'

    req = urllib.request.Request(url, data=json_data, headers=headers, method=method)
    response = urllib.request.urlopen(req)

    print(response.read())

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

def test_email():
    gmail_user = "waristea@gmail.com"
    gmail_password = "uubcprkertzvurnv"

    to = ["waristea@gmail.com"]
    subject = "Wibu"
    body = "Testing"
    send_email(gmail_user, to, subject, body, gmail_password)

if __name__=="__main__":
    test_api_request_detail(25)
