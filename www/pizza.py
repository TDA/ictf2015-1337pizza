#!/usr/bin/env python
import sqlite3
from flask import Flask
from datetime import datetime, date
import random
from flask import Flask, request, send_from_directory
import string
import sys

#sys.stdout = open('/dev/null', 'w')
#sys.stderr = open('/dev/null', 'w')

app = Flask(__name__, static_url_path='')

def get_conn_cur():
    conn = sqlite3.connect('../rw/pizza.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()
    return conn, cur

def get_pizza_status(timestamp):
    tdelta = datetime.utcnow() - timestamp

    if tdelta.seconds / 60 < 5:
        return "To be Processed!"
    elif tdelta.seconds / 60 < 10:
        return "In the Oven!"
    elif tdelta.seconds / 60 < 20:
        return "Out for Delivery!"
    else:
        return "Delivered. Enjoy!"

def get_sql_injection_msg():
    greetings = ["Hello! Is this 1990?", 
    "Is this NEO the hacker?",
    "Your attack was detected. As punishment, we will add Broccoli to your next order.",
    "Password: Swordfish?"]

    return greetings[random.randint(0, len(greetings) -1)]


def injection_check(xstring):
    if xstring.find('--') > 0:
        return True
        

@app.route('/dist/<path:path>')
def send_dist(path):
    return send_from_directory('dist', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route("/jumbotron.css")
def jumbotron():
    return open("jumbotron.css").read()

@app.route("/")
def homepage():
    return open("index.html.txt").read()

@app.route("/main.html")
def main():
    return open("main.html").read()


@app.route("/register.html", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # perform registration

        if not 'username' in request.form.keys():
            return "Fail"

        if not 'password' in request.form.keys():
            return "Fail"

        username = request.form['username']
        password = request.form['password']
        if len(username) > 50:
            return "input too long"

        if len(password) > 50:
            return "input too long"

        if len(username) < 2:
            return "input too short"

        if len(password) < 4:
            return "input too short"

        if injection_check(username):
            return get_sql_injection_msg()

        try:
            conn, cur = get_conn_cur()
            cur.execute("INSERT INTO customers (name, password) VALUES (?, ? )", [username, password ])
            customerid = cur.lastrowid
            conn.commit()
            conn.close()
            return 'Success, customerid: {0}'.format(customerid)
        except Exception as e:
            print "Fail: {0}".format(e)
            return "Fail"

    else:
        return open("register.html").read()

@app.route("/tracking_status.png", methods=['GET'])
def track_pic():

    try:
        orderid = int(request.args.get('orderid'))
        token = request.args.get('token').strip()
        if len(token) < 10:
            return "Input too short"

        conn, cur = get_conn_cur()
        cur.execute("select timestamp from orders where id = {0} and token = '{1}'".format(orderid, token))
        timestamp = cur.fetchone()[0]

        # Based on timestamp...
        tdelta  = (datetime.utcnow() - timestamp)

        if tdelta.seconds / 60 < 5:
            return open('img/icons/processing.png').read()
        elif tdelta.seconds / 60 < 10:
            return open('img/icons/baking.png').read()
        elif tdelta.seconds / 60 < 20:
            return open('img/icons/delivery.png').read()
        else:
            return open('img/icons/delivered.png').read()
    except Exception as e:
        print "Fail: {0}".format(e)
        print e.message, e.args
        # Fail
        return open('img/icons/questionmark.png').read()
    

@app.route("/tracking.html", methods=['POST', 'GET'])
def track_order():
    if request.method == 'POST':
        if not 'orderid' in request.form.keys():
            return "Fail due to order"
        
        if not 'token' in request.form.keys() and len(token) < 20:
            return "Fail due to token len"

        if not 'password' in request.form.keys():
            return "Fail due to password"


        try:
            orderid = int(request.form['orderid'])
            token = request.form['token'].strip()
            password = request.form['password'].strip()

            if injection_check(token) or injection_check(password):
                return get_sql_injection_msg()

            conn, cur = get_conn_cur()
            cur.execute("select address_line_1, address_line_2, timestamp, paymentinfo from orders, customers where customers.id = orders.customer_id and orders.id = ? and token = ? and customers.password = ?", [orderid, token, password])
            orderstatus = cur.fetchone()
            timestamp = orderstatus[2]
            payment = orderstatus[3]

            status = get_pizza_status(timestamp)
            if orderstatus == None:
                return "no order found"
            else:
                img_tag = "<img src='tracking_status.png?orderid={0}&token={1}'/>".format(orderid, token)
                return "Status of delivery to {0} {1} is: {2} {3}. Payment processed via {4}".format(orderstatus[0], orderstatus [1], status, img_tag, payment)
        except Exception as e:
            print "Fail: {0}".format(e)
            return "Fail"
    else:
        return open("tracking.html").read()

@app.route("/order.html", methods=['POST', 'GET'])
def order():
    if request.method == 'POST':

        if not 'customerid' in request.form.keys():
            return "Fail"

        if not 'password' in request.form.keys():
            return "Fail"

        if not 'address_line_1' in request.form.keys():
            return "Fail"

        if not 'payment_information' in request.form.keys():
            return "Fail"
        
        if not 'items' in request.form.keys():
            return "Fail"


        try:

            customer_id = int(request.form['customerid'])
            delivery_address_1 = request.form['address_line_1']
            payment_information = request.form['payment_information']
            password = request.form['password']
            items = request.form['items']

            if len(delivery_address_1) < 5 or len(items) < 5 or len(payment_information) < 5:
                return "Input too short"

            if 'delivery_address_2' in request.form.keys():
                delivery_address_2 = request.form['address_line_2']
            else:
                delivery_address_2 = ""


            if len(delivery_address_1) > 50 or len(items) > 50 or len(payment_information) > 50:
                return "input too long"

            if injection_check(items) or injection_check(delivery_address_1) or injection_check(delivery_address_2) or injection_check(payment_information) or injection_check(password):
                return get_sql_injection_msg()

            conn, cur = get_conn_cur()


            cur.execute("select id from customers where id = ? and password = ? ", [customer_id, password])
            if cur.fetchone() == None:
                return "Fail"

            order_token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64))
            cur.execute("INSERT INTO orders (customer_id, paymentinfo, address_line_1, address_line_2, items, token) VALUES (?, ?, ?, ?, ?, ? )", [customer_id, payment_information, delivery_address_1, delivery_address_2, items, order_token])

            orderid = cur.lastrowid
            conn.commit()
            conn.close()
            return 'OrderNr: {0}, Token: {1}'.format(orderid, order_token)
        except Exception as e:
            print "Fail: {0}".format(e)
            return "Fail"
    else:
        return open("order.html").read()

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port = 5000)

