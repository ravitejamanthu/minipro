from flask import Flask, request, render_template, redirect,flash ,session
# Removed: from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess
import os 
import mysql.connector
from werkzeug.utils import secure_filename
from glob import glob
from flask import jsonify
app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'ramram')

# MySQL configurations
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')  # Enter your MySQL username
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'Manthu@2605')  # Enter your MySQL password
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'onroadservice')  # Enter your MySQL database name
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', '3306'))
# mechanics = {'admin': 'password'}

def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB'],
        port=app.config['MYSQL_PORT']
    )

@app.route('/')
def login():
    return render_template('welcome.html')

@app.route('/mechanic')
def mechanic_login():
    return render_template('mechanic_login.html')

@app.route('/user')
def user_login():
    return render_template('user_login.html')
@app.route('/profile')
def profile():
    username=session.get('username')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("select address,email,garage_name,owner_name,user_name,number from mechanic_data where user_name=%s",(username,))
    details=cur.fetchall()
    cur.close()
    conn.close()
    return render_template('mec_profile.html',details=details)


@app.route('/feedback')
def feedback():
    return render_template('feedback.html')
@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/mechanic_login', methods=['POST'])
def process_mechanic_login():
    username = request.form['username']
    password = request.form['password']
    session['username'] = username
    # print(username)
    # print(password)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password from mechanic_data where user_name=%s",(username,))
    details=cur.fetchone()
    
    # Check if username exists and password matches
    if details is not None and password==details[0]:
        # Successful login
        cur.close()
        conn.close()
        return render_template('mechanic_dashboard.html')
    else:
        # Invalid credentials, render login page with error message
        cur.close()
        conn.close()
        return render_template('mechanic_login.html', error="Incorrect login details")
@app.route('/mechanic_register', methods=['GET', 'POST'])
def mechanic_register():
    if request.method == 'POST':
        owner_name = request.form['owner_name']
        garage_name = request.form['garage_name']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        address = request.form['address']
        mobile_no = request.form['mobile_no']
        email = request.form['email']
        print(owner_name, garage_name, username, password, address, mobile_no)
        if password != confirm_password:
            return render_template('mec_reg.html', error="Passwords do not match")
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO mechanic_data (address, email, garage_name, owner_name, password, user_name) VALUES (%s, %s, %s, %s, %s, %s)",
                        (address, email, garage_name, owner_name, password, username))
            conn.commit()
            return redirect('/mechanic')
        except Exception as e:
            return render_template('mec_reg.html', error=str(e))
        finally:
            cur.close()
            conn.close()

    return render_template('mec_reg.html')

# App routes for USERS
@app.route('/user_login', methods=['POST'])
def process_user_login():
    username = request.form['username']
    session['username'] = username
    password = request.form['password']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT password from user_data where user_name=%s",(username,))
    details=cur.fetchone()
    if details is not None and password==details[0]:
        # Successful login
        cur.close()
        conn.close()
        return render_template('user_dashboard.html')
    else:
        # Invalid credentials, render login page with error message
        cur.close()
        conn.close()
        return render_template('user_login.html', error="Incorrect login details")

    

@app.route('/user_register', methods=['GET','POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['Name']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        address = request.form['address']
        mobile_no = request.form['Mobile No']
        email = request.form['Email']
        # Check if passwords match
        if password != confirm_password:
            return render_template('user_reg.html', error="Passwords do not match")

        # Hash the password for security

        # Insert data into the user_data table
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO user_data (name, user_name, password, address, mobile_number, email) VALUES (%s, %s, %s, %s, %s, %s)",
                        (name, username, password, address, mobile_no, email))
            conn.commit()
            cur.close()
            conn.close()
            return redirect('/user')  # Redirect to the user login page after successful registration
        except Exception as e:
            return render_template('user_reg.html', error=str(e))
    return render_template('user_reg.html')

    


@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

@app.route('/garages_near_you')
def garages_near_you():
    return render_template('garages_near_you.html')

@app.route('/process_dropdown', methods=['POST'])
def process_dropdown():
    username = session.get('username')
    selected_city = request.form['cityselect']
    print(selected_city)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT address, email, garage_name, owner_name,number FROM mechanic_data WHERE address=%s", (selected_city,))
    mechanics = cur.fetchall()
    for i in mechanics:
        print(i)
    cur.close()
    conn.close()
    return render_template('garages_near_you.html', mechanics=mechanics)

@app.route('/userprofile')  # Change '/profile' to '/userprofile'
def user_profile():
    return render_template('user_profile.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/our_service')
def our_service():
    return render_template('ourservice.html')
@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the login page or any other page you prefer
    return render_template('user_login.html')

if __name__ == '__main__':
    app.run(debug=True)