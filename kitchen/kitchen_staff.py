import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json
import psycopg2
from psycopg2.extras import RealDictConnection
from rds.postgresql_rds import get_db


def update_profile_info(event):
    data = json.loads(event['body']) if event.get('body', 0) else event
    sql = """ UPDATE kitchen_kitchenstaff
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


def device_token_update(device_token, email):
    sql = """ UPDATE kitchen_kitchenstaff 
                SET device_token = %s 
                WHERE email = %s"""
    conn = None
    updated_rows = 0
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(sql,
                    (device_token,
                     email
                     ))
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
    sql = """ UPDATE kitchen_kitchenstaff 
                SET  profile_picture = %s
                WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        name = data['profile_picture']
        customer_id = data['id']
        image_id = str(id(customer_id))
        image_name = str(image_id + '_kitchen_kitchenstaff_id_{}.png'.format(customer_id))
        decode_content = base64.b64decode(name)
        s3.put_object(Bucket='mapplate-public', Key='media/kitchen_staff_profile_picture/' + image_name,
                      ContentType="image/png", Body=decode_content)
        s3_bucket_url = 'kitchen_staff_profile_picture/' + image_name
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


class KitchenStaffLogin:
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
                "SELECT id, first_name, last_name, to_char(date_of_birth, 'YYYY-MM-DD') AS date_of_birth, 'https://mapplate-public.s3.eu-central-1.amazonaws.com/media/'|| profile_picture AS profile_picture,  address_line_1, address_line_2, mobile, city, state, country, zip_code, is_active, email, password, restaurant_id, coffee_house_id from kitchen_kitchenstaff where email= '{}' ".format(
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


def lambda_handler(event, context):
    data = json.loads(event['body']) if event.get('body', 0) else event

    if data.get('password') and data.get('email'):
        kitchen_staff = KitchenStaffLogin()
        password = hashlib.sha256(data['password'].encode()).hexdigest()
        print("password", password)
        email = data['email']
        print("email", email)

        kitchen_staff.get_login_info(event)
        login_status = kitchen_staff.login(email, password)

        event_length = len(data)
        if kitchen_staff.login_user == True:

            if event_length == 3:
                login_info = kitchen_staff.get_login_info(event)

                if data.get('device_token'):
                    device_token = data.get('device_token')
                    email = data.get('email')
                    device_token_update(device_token, email)

                return {
                    'body': login_info
                }

            elif event_length == 14:
                images = data.get("profile_picture")
                if images:
                    profile_picture(event)
                update_profile_info(event)
                login_info = kitchen_staff.get_login_info(event)

                return {
                    'body': login_info
                }

            return {
                'body': "Your email or password is incorrect"
            }

        return {
            'body': login_status
        }
