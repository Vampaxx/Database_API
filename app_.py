import os 
from dotenv import load_dotenv
from flask_mysqldb import MySQL
from src.Database_API import logger
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from Database_API.config.configuration import ConfigurationManager




app = Flask(__name__)

load_dotenv()
# MySQL Configuration
app.config['MYSQL_HOST']        = os.getenv('db_host')
app.config['MYSQL_USER']        = os.getenv('db_user')
app.config['MYSQL_PASSWORD']    = os.getenv("db_password")
app.config['MYSQL_DB']          = os.getenv("db_name")
app.config['JWT_SECRET_KEY']    = os.getenv("secret_key")


mysql   = MySQL(app)
jwt     = JWTManager(app)



@app.route('/signup', methods=['POST'])
def register():
    email       = request.json.get('email')
    password    = request.json.get('password')
    
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO sign_up (email, passwords) VALUES (%s, %s)", (email, password))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"msg": "User registered successfully!"}), 201


@app.route('/login', methods=['POST'])
def login():
    email       = request.json.get('email')
    password    = request.json.get('password')
    
    cursor  = mysql.connection.cursor()
    cursor.execute("SELECT * FROM sign_up WHERE email = %s AND passwords = %s", (email, password))
    user    = cursor.fetchone()
    cursor.close()
    
    if user:
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200          # OK
    return jsonify({"msg": "Bad username or password"}), 401    # Unauthorized 



@app.route('/sign_up', methods=['GET'])
@jwt_required()
def get_items():
    cursor  = mysql.connection.cursor()
    cursor.execute("SELECT * FROM sign_up")
    items   = cursor.fetchall()
    cursor.close()
    
    return jsonify(items), 200          # OK 


# GET a specific account
@app.route('/sign_up/<string:email>', methods=['GET'])
@jwt_required()
def get_email(email):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM sign_up WHERE email = %s", (email,))
    email   = cursor.fetchone()
    cursor.close()

    if email is None:
        return jsonify({'message': 'account not found'}), 404   # Not Found 
    return jsonify(email), 200                                  # OK


# POST a new account 
@app.route('/sign_up', methods=['POST'])
@jwt_required()
def create_item():
    account_id  = request.json
    cursor      = mysql.connection.cursor()
    cursor.execute("INSERT INTO sign_up (email, passwords) VALUES (%s, %s)", (account_id['email'], account_id['password']))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"msg": "Account created"}), 201         # created 


# PUT to update an account
@app.route('/sign_up/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_item(account_id):
    updated_data    = request.json
    cursor          = mysql.connection.cursor()
    cursor.execute("UPDATE sign_up SET email = %s, passwords = %s WHERE account_id = %s", 
                   (updated_data['email'], updated_data['password'], account_id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"msg": "Account updated"}), 200         # Ok 



# DELETE an account
@app.route('/sign_up/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_item(account_id):
    cursor  = mysql.connection.cursor()
    cursor.execute("DELETE FROM sign_up WHERE account_id = %s", (account_id,))
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({"msg": "Account deleted"}), 204         # NO Content 




if __name__ == "__main__":
    app.run(debug=True)




