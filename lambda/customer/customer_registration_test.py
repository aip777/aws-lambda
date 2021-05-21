import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db

from botocore.exceptions import ClientError
from botocore.vendored import requests


def send_email():
    # This address must be verified with Amazon SES.
    SENDER = "arifulislamaip777@gmail.com"

    # If your account is still in the sandbox, this address must be verified.
    RECIPIENT = "sohan.bdtask@gmail.com"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # The AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-central-1"

    # The subject line for the email.
    SUBJECT = "Mapplate Email Service"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = "..."

    # The HTML body of the email.
    BODY_HTML = """<html> <head></head> <body> <h1>Amazon SES Test (SDK for Python)</h1> <p>This email was sent with <a href='https://aws.amazon.com/ses/'> Amazon SES </a> using <a href='https://aws.amazon.com/sdk-for-python/'> AWS SDK for Python (Boto)</a>.</p> </body> </html>"""

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name=AWS_REGION)

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        return (e.response['Error']['Message'])
    else:
        return ("Email sent! Message ID:" + response['MessageId'])


def send_email():
    SENDER = "arifulislamaip777@gmail.com"
    RECIPIENT = "arifulislamaip777@gmail.com"
    AWS_REGION = "eu-central-1"
    SUBJECT = "Mapplate Email Service"
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                 )
    BODY_HTML = """<!DOCTYPE html><html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head><meta charset="utf-8"> <!-- utf-8 works for most cases --><meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary --><meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine --><meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely --><title></title> <!-- The title tag shows in email notifications, like Android 4.4. --><link href="https://fonts.googleapis.com/css?family=Playfair+Display:400,400i,700,700i" rel="stylesheet"><!-- CSS Reset : BEGIN --><style>html,body {margin: 0 auto !important;padding: 0 !important;height: 100% !important;width: 100% !important;background: #f1f1f1;}/* What it does: Stops email clients resizing small text. */* {-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;}/* What it does: Centers email on Android 4.4 */div[style*="margin: 16px 0"] {margin: 0 !important;}/* What it does: Stops Outlook from adding extra spacing to tables. */table,td {mso-table-lspace: 0pt !important;mso-table-rspace: 0pt !important;}/* What it does: Fixes webkit padding issue. */table {border-spacing: 0 !important;border-collapse: collapse !important;table-layout: fixed !important;margin: 0 auto !important;}/* What it does: Uses a better rendering method when resizing images in IE. */img {-ms-interpolation-mode:bicubic;}/* What it does: Prevents Windows 10 Mail from underlining links despite inline CSS. Styles for underlined links should be inline. */a {text-decoration: none;}/* What it does: A work-around for email clients meddling in triggered links. */*[x-apple-data-detectors],  /* iOS */.unstyle-auto-detected-links *,.aBn {border-bottom: 0 !important;cursor: default !important;color: inherit !important;text-decoration: none !important;font-size: inherit !important;font-family: inherit !important;font-weight: inherit !important;line-height: inherit !important;}/* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */.a6S {display: none !important;opacity: 0.01 !important;}/* What it does: Prevents Gmail from changing the text color in conversation threads. */.im {color: inherit !important;}/* If the above doesn't work, add a .g-img class to any image in question. */img.g-img + div {display: none !important;}/* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  *//* Create one of these media queries for each additional viewport size you'd like to fix *//* iPhone 4, 4S, 5, 5S, 5C, and 5SE */@media only screen and (min-device-width: 320px) and (max-device-width: 374px) {u ~ div .email-container {min-width: 320px !important;}}/* iPhone 6, 6S, 7, 8, and X */@media only screen and (min-device-width: 375px) and (max-device-width: 413px) {u ~ div .email-container {min-width: 375px !important;}}/* iPhone 6+, 7+, and 8+ */@media only screen and (min-device-width: 414px) {u ~ div .email-container {min-width: 414px !important;}}</style><!-- CSS Reset : END --><!-- Progressive Enhancements : BEGIN --><style>.primary{background: #f3a333;}.bg_white{background: #ffffff;}.bg_light{background: #fafafa;}.bg_black{background: #000000;}.bg_dark{background: rgba(0,0,0,.8);}.email-section{padding:2.5em;}/*BUTTON*/.btn{padding: 10px 15px;}.btn.btn-primary{border-radius: 30px;background: #f3a333;color: #ffffff;}h1,h2,h3,h4,h5,h6{font-family: 'Playfair Display', serif;color: #000000;margin-top: 0;}body{font-family: 'Montserrat', sans-serif;font-weight: 400;font-size: 15px;line-height: 1.8;color: rgba(0,0,0,.4);}a{color: #f3a333;}table{}/*LOGO*/.logo h1{margin: 0;}.logo h1 a{color: #000;font-size: 20px;font-weight: 700;text-transform: uppercase;font-family: 'Montserrat', sans-serif;}/*HERO*/.hero{position: relative;}.hero img{}.hero .text{color: rgba(255,255,255,.8);}.hero .text h2{color: #ffffff;font-size: 30px;margin-bottom: 0;}/*HEADING SECTION*/.heading-section{}.heading-section h2{color: #000000;font-size: 28px;margin-top: 0;line-height: 1.4;}.heading-section .subheading{margin-bottom: 20px !important;display: inline-block;font-size: 13px;text-transform: uppercase;letter-spacing: 2px;color: rgba(0,0,0,.4);position: relative;}.heading-section .subheading::after{position: absolute;left: 0;right: 0;bottom: -10px;content: '';width: 100%;height: 2px;background: #f3a333;margin: 0 auto;}.heading-section-white{color: rgba(255,255,255,.8);}.heading-section-white h2{font-size: 28px;font-family:line-height: 1;padding-bottom: 0;}.heading-section-white h2{color: #ffffff;}.heading-section-white .subheading{margin-bottom: 0;display: inline-block;font-size: 13px;text-transform: uppercase;letter-spacing: 2px;color: rgba(255,255,255,.4);}.icon{text-align: center;}.icon img{}/*SERVICES*/.text-services{padding: 10px 10px 0;text-align: center;}.text-services h3{font-size: 20px;}/*BLOG*/.text-services .meta{text-transform: uppercase;font-size: 14px;}/*TESTIMONY*/.text-testimony .name{margin: 0;}.text-testimony .position{color: rgba(0,0,0,.3);}/*VIDEO*/.img{width: 100%;height: auto;position: relative;}.img .icon{position: absolute;top: 50%;left: 0;right: 0;bottom: 0;margin-top: -25px;}.img .icon a{display: block;width: 60px;position: absolute;top: 0;left: 50%;margin-left: -25px;}/*COUNTER*/.counter-text{text-align: center;}.counter-text .num{display: block;color: #ffffff;font-size: 34px;font-weight: 700;}.counter-text .name{display: block;color: rgba(255,255,255,.9);font-size: 13px;}/*FOOTER*/.footer{color: rgba(255,255,255,.5);}.footer .heading{color: #ffffff;font-size: 20px;}.footer ul{margin: 0;padding: 0;}.footer ul li{list-style: none;margin-bottom: 10px;}.footer ul li a{color: rgba(255,255,255,1);}@media screen and (max-width: 500px) {.icon{text-align: left;}.text-services{padding-left: 0;padding-right: 20px;text-align: left;}}</style></head><body width="100%" style="margin: 0; padding: 0 !important; mso-line-height-rule: exactly; background-color: #222222;"><center style="width: 100%; background-color: #f1f1f1;"><div style="display: none; font-size: 1px;max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;</div><div style="max-width: 600px; margin: 0 auto;" class="email-container"><!-- BEGIN BODY --><table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;"><tr><td class="bg_white logo" style="padding: 1em 2.5em; text-align: center"><h1><a href="#">Mapplate</a></h1></td></tr><!-- end tr --><tr></tr><!-- end tr --><tr><td class="bg_white"><table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"><tr><td class="bg_dark email-section" style="text-align:center;"><div class="heading-section heading-section-white"><span class="subheading">Welcome</span><h2>Welcome To RestoBar</h2><p>A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.</p></div></td></tr><!-- end: tr --><tr><td class="bg_light email-section" style="text-align:center;"><table><tr><td style="padding-top: 20px;"><h2>Watch Our Video</h2><p>A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth.</p></td></tr></table></td></tr><!-- end: tr --></table></td></tr><!-- end:tr --><!-- 1 Column Text + Button : END --></table><table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;"><tr><td valign="middle" class="bg_black footer email-section"><table><tr><td valign="top" width="33.333%" style="padding-top: 20px;"><table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"><tr><td style="text-align: left; padding-right: 10px;"><h3 class="heading">RestoBar</h3><p>A small river named Duden flows by their place and supplies it with the necessary regelialia.</p></td></tr></table></td><td valign="top" width="33.333%" style="padding-top: 20px;"><table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"><tr><td style="text-align: left; padding-left: 5px; padding-right: 5px;"><h3 class="heading">Contact Info</h3><ul><li><span class="text">203 Fake St. Mountain View, San Francisco, California, USA</span></li><li><span class="text">+2 392 3929 210</span></a></li></ul></td></tr></table></td><td valign="top" width="33.333%" style="padding-top: 20px;"><table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"><tr><td style="text-align: left; padding-left: 10px;"><h3 class="heading">Useful Links</h3><ul><li><a href="#">Breakfast</a></li><li><a href="#">Lunch</a></li><li><a href="#">Dinner</a></li><li><a href="#">Dessert</a></li></ul></td></tr></table></td></tr></table></td></tr><!-- end: tr --><tr><td valign="middle" class="bg_black footer email-section"><table><tr><td valign="top" width="33.333%"><table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"><tr><td style="text-align: left; padding-right: 10px;"><p>&copy; 2018 Restobar. All Rights Reserved</p></td></tr></table></td><td valign="top" width="33.333%"><table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%"><tr><td style="text-align: right; padding-left: 5px; padding-right: 5px;"><p><a href="#" style="color: rgba(255,255,255,.4);">Unsubcribe</a></p></td></tr></table></td></tr></table></td></tr></table></div></center></body></html>"""
    CHARSET = "UTF-8"
    client = boto3.client('ses', region_name=AWS_REGION)
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        return (e.response['Error']['Message'])
    else:
        return ("Email sent! Message ID:" + response['MessageId'])


def update_profile_info(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    sql = """ UPDATE waiter_waiter
                SET first_name = %s, last_name = %s, date_of_birth = %s, address_line_1 = %s, address_line_2 = %s, mobile = %s, city = %s, state = %s, country = %s, email = %s, zip_code = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(sql,
                    (data['first_name'],
                     data['last_name'],
                     data['to_char'],
                     data['address_line_1'],
                     data['address_line_2'],
                     data['mobile'],
                     data['city'],
                     data['state'],
                     data['country'],
                     data['email'],
                     data['zip_code'],
                     data['id']))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def profile_picture(event):
    s3 = boto3.client("s3")
    data = json.loads(event['body']) if event.get('body', 0) else event
    conn = get_db()
    conn.autocommit = True
    sql = """ UPDATE waiter_waiter 
                SET  profile_picture = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        name = data['profile_picture']
        customer_id = data['id']
        image_id = str(id(customer_id))
        image_name = str(image_id + '_waiter_id_{}.png'.format(customer_id))
        decode_content = base64.b64decode(name)
        s3.put_object(Bucket='mapplate-public', Key='media/waiter_profile_picture/' + image_name,
                      ContentType="image/png", Body=decode_content)
        s3_bucket_url = 'waiter_profile_picture/' + image_name
        conn = get_db()
        cur = conn.cursor()
        cur.execute(sql,
                    (s3_bucket_url,
                     data['id']))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return updated_rows


class WaiterLogin:
    def __init__(self):
        self.login_user = False
        self.email = ''
        self.password = ''
        self.user_info = ''

    def get_login_info(self, event):
        data = json.loads(event['body']) if event.get('body', 0) else event
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "SELECT id, first_name, last_name, to_char(date_of_birth, 'YYY-MM-DD'), 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| profile_picture AS profile_picture,  address_line_1, address_line_2, mobile, city, state, country, zip_code, is_active, email, password, restaurant_id, coffee_house_id, user_id, table_id from waiter_waiter where email= '{}' ".format(
                    data['email']))
            info = cur.fetchone()
            self.email = info['email']
            self.password = info['password']
            info.pop('password')
            self.user_info = info
            return self.user_info
        except Exception as e:
            return e

    def login(self, email, password):
        if self.email == email and self.password == password:
            self.login_user = True
            user_information = self.user_info
            return user_information
        else:
            return "Your email or password is incorrect"

    def user_login_activate(self):
        if self.login_user == True:
            return "Login success"
        else:
            return "Logout"

    def logout(self):
        self.login_user = False
        return self.login_user

    def forget_password(self, event):
        if self.email == event["email"]:
            print("")
    # using mailer for send email


def lambda_handler(event, context):
    # var = send_email()

    return event
