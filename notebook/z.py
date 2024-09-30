import os 
import secrets
import jwt
from functools import wraps
from dotenv import load_dotenv
from src.Database_API import logger
from datetime import datetime,timedelta


from sqlalchemy import create_engine,text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask import Flask,render_template,redirect,url_for,request,jsonify,flash
from Database_API.config.configuration import ConfigurationManager


load_dotenv()

app          = Flask(__name__)
manager      = ConfigurationManager()
database     = manager.get_database_config()
#secret_key                                      = secrets.token_hex(16) 
app.config['SECRET_KEY']                        = os.getenv('secret_key')
app.config["SQLALCHEMY_DATABASE_URI"]           = f'mysql+pymysql://{database.db_user}:{database.db_password}@{database.db_host}/{database.db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']    = False
#app.secret_key                                  = os.environ.get(secret_key, 'default_secret_key')
db                                              = SQLAlchemy(app)



def token_required(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        token   = request.args.get("token")
        if not token:
            return jsonify({"Alert!":"Token is missing!"})
        try:
            payload = jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({"Alert!":"Invalid Token!"})
    return decorated



@app.route("/")
def home():
    return render_template("home_page.html")
    
##-----------------------Log_In_page-------------------------------------------##
@app.route("/login")
def login():
    return render_template("log_in.html")

#authenticated 
@app.route("/auth")
@token_required
def auth():
    return "JWT is verified, Welocome to yout Dashboard"


@app.route('/authentication', methods=['POST'])
def user_authentication():       
    email       = request.form.get('email')
    password    = request.form.get('password')
    try:
        user = db.session.execute(text("SELECT * FROM sign_up WHERE email=:email"), {'email': email}).fetchone()

        if user:
            stored_password = user[2]   
            print(stored_password,password)
            if password == stored_password:
                flash("Login successful!", "success")
                return render_template("sucess.html")
            else:
                flash("Incorrect password. Please try again.", "error")
                return redirect(url_for('login'))  #
        else:
            flash("Email not found. Please sign up.", "error")
            return redirect(url_for('signup'))  

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('login'))  # Redirect to login on error

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
   
@app.route("/reset_password", methods=["GET", "PUT"])
def reset_password():
    if request.method == "GET":
        return render_template("forgot_password.html")
    if request.method == "PUT":
        data            = request.get_json()
        email           = data.get('email')
        new_password    = data.get('new_password')

        
        print(email, new_password)  

        return jsonify({"message": "Password updated successfully."}), 200



    
if __name__ == "__main__":
    app.run(debug=True)