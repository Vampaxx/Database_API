import os 
import secrets

from functools import wraps
from dotenv import load_dotenv
from src.Database_API import logger
from datetime import datetime,timedelta
from jwt import JWT,supported_key_types

from sqlalchemy import create_engine,text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import Flask,render_template,redirect,url_for,request,jsonify,flash,session
from Database_API.config.configuration import ConfigurationManager


load_dotenv()
def secrets_key():
    str_secrets_key = os.getenv('secret_key')
    b_SECRET_KEY    = (str_secrets_key.encode("UTF-8"))
    supported_key   = supported_key_types()['oct'](b_SECRET_KEY)
    return supported_key


app             = Flask(__name__)
manager         = ConfigurationManager()
database        = manager.get_database_config()
supported_key   = secrets_key() 

app.config['SECRET_KEY']                        = os.getenv("secret_key")
app.config["SQLALCHEMY_DATABASE_URI"]           = f'mysql+pymysql://{database.db_user}:{database.db_password}@{database.db_host}/{database.db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']    = False
db                                              = SQLAlchemy(app)
jwt_instance                                    = JWT()




def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token   = request.args.get("token")
        #token   = request.get("token")
        if not token:
            return jsonify({"Alert!":"Token is missing!"})
        try:
            #payload = jwt_instance.decode(token,app.config['SECRET_KEY'])
            payload     = jwt_instance.decode(token,secrets_key())
            expiration  = payload.get("expiration")
            if datetime.utcnow() > datetime.strptime(expiration, '%Y-%m-%d %H:%M:%S.%f'):
                flash("Session expired. Please log in again.", "error")
                session.pop('logged_in', None)
                return redirect(url_for('home'))
        except:
            return jsonify({"Alert!":"Invalid Token!"})
        return func(*args, **kwargs)
    return decorated



@app.route("/")
def home():
    return render_template("home_page.html")
    
##-----------------------Log_In_page-------------------------------------------##
@app.route("/login")
def login():
    return render_template("log_in.html")

#authenticated 
@app.route("/sucess")
@token_required
def sucess():
    return render_template("sucess.html")


@app.route('/authentication', methods=['POST'])
def user_authentication():       
    email       = request.form.get('email')
    password    = request.form.get('password')

    print(email,password)
    try:
        user = db.session.execute(text("SELECT * FROM sign_up WHERE email=:email"), {'email': email}).fetchone()
        if user:
            stored_password = user[2]   
            if password == stored_password:
                session['logged_in'] = True

                token = jwt_instance.encode({
                    "email"     : email,
                    "expiration": str(datetime.utcnow() + timedelta(seconds=5))
                },
                supported_key  
                )
                #return render_template("sucess.html")
                #return jsonify({'token': token})
                return redirect(url_for('sucess', token=token))


            else:
                flash("Incorrect password. Please try again.", "error")
                return redirect(url_for('login'))  #
        else:
            flash("Email not found. Please sign up.", "error")
            return redirect(url_for('signup'))  

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('home'))  # Redirect to login on error


##-----------------------------------Sign_up_page---------------------------------------------------------------------------
@app.route("/signup")
def signup():
    return render_template("sign_up.html")
    

@app.route('/create_account', methods=['POST',"GET"])
def create_new_account():       
    if request.method == "POST":
        email       = request.form.get('email')
        password    = request.form.get('password')
        try:
            existing_user = db.session.execute(text("SELECT * FROM sign_up WHERE email=:email"), {'email': email}).fetchone()
            
            if existing_user:
                flash("The account already exists, please try another email address.", "error")
                return redirect(url_for('signup'))
                
            db.session.execute(
                text("INSERT INTO sign_up (email, passwords) VALUES (:email, :password)"), 
                {'email': email, 'password': password}  # Hash the password here for security
            )
            db.session.commit()

            flash("Account created successfully!", "success")
            return render_template('log_in.html')  # Redirect to login after successful signup

        except IntegrityError:
            db.session.rollback()  # Rollback if there is a database error
            flash("An error occurred while creating the account. Please try again.", "error")
            return redirect(url_for('signup'))

        except Exception as e:
            db.session.rollback()  # Rollback for any other exceptions
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('home'))
    else:
        return render_template("sign_up.html")


 ##------------------------------------Reset_password---------------------------------------------------------   
@app.route("/forgot_password")
def forgot_password():
    return render_template("forgot_password.html")


@app.route("/reset_password", methods=["GET","PUT"])
def reset_password():
    if request.method == "GET":
        return render_template("reset_password.html")
    if request.method == "PUT":
        #data            = request.get_json()
        #email           = data.get('email')
        #new_password    = data.get('new_password')
        email           = request.form.get('email')
        new_password    = request.form.get('password')
        print(email,new_password)

        
        print(email, new_password)  

        return jsonify({"message": "Password updated successfully."}), 200


@app.route('/delete_item/<int:email_id>', methods=['DELETE'])
def delete_item(email_id):
    item = db.session.execute(text("SELECT * FROM sign_up WHERE email=:email"), {'email': email}).fetchone()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': f'Item {item_id} deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Item not found.'}), 404



    
if __name__ == "__main__":
    app.run(debug=True)