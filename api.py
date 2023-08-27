from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from settings import *
import requests

app = Flask(__name__)

app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB

mysql = MySQL(app)

@app.route("/token/<token>")

def validate_token(token):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM resume_website.api_keys WHERE apiKey = %s''', [token])
    user_data = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    if not user_data:
        response = {
            "code": 200,
            "message": {
                "valid": False,
                "error": "Invalid api key!"
            }
        } 
        return jsonify(response), 200
    user_data = user_data[0]
    response = {
        "code": 200,
        "message": {
            "valid": True,
            "getPerm": user_data[2],
            "postPerm": user_data[3],
            "deletePerm": user_data[4]    
        } 
    }
    return jsonify(response), 200
@app.route("/get-comments")
def get_all_comments():
    apiKey = request.headers.get('apiKey', None)
    if apiKey is not None:    
        url = TOKEN_URL + apiKey
        token = requests.get(url)
        token = token.json()
        if token['message']['valid'] and token['message']['getPerm'] == 1: 
            cursor = mysql.connection.cursor()
            cursor.execute( GET_ALL_COMMENTS_QUERY)
            user_data = cursor.fetchall()
            transformed_data = [{'email': row[1], 'comment': row[2]} for row in user_data]
            
            response = {
                "code": 200,
                "message": transformed_data
            }
            return jsonify(response), 200
        
        
        
        response = {
            "code": 400,
            "message": "Invalid API key!"
        }
        return jsonify(response), 400
    
    response = {
            "code": 400,
            "message": "API key required!"
        }
    return jsonify(response), 400

@app.route("/get-comments/<email>")
def get_comment(email):
    apiKey = request.headers.get('apiKey', None)
    if apiKey is not None:    
        url = TOKEN_URL + apiKey
        token = requests.get(url)
        token = token.json()
        if token['message']['valid'] and token['message']['getPerm'] == 1: 
            cursor = mysql.connection.cursor()
            cursor.execute( GET_COMMENT_QUERY, [email])
            user_data = cursor.fetchall()
            user_data = user_data[0] 
            mysql.connection.commit()
            cursor.close()
            response = {
                "code" : 200,
                "message": {
                    "email": user_data[0],
                    "comment": user_data[1],
                    
                }
            }
            
            
            
            return jsonify (response), 200
        response = {
            "code": 400,
            "message": "Invalid API key!"
        }
        return jsonify(response), 400
    
    response = {
            "code": 400,
            "message": "API key required!"
        }
    return jsonify(response), 400

@app.route("/create-comment", methods = ["POST"])
def create_comment():
    
    apiKey = request.headers.get('apiKey', None)
    if apiKey is not None:
        url = TOKEN_URL + apiKey
        token = requests.get(url)
        token = token.json()
        if token['message']['valid'] and token['message']['postPerm'] == 1: 
            response = {
                "code": 201,
                "message": "Comment has been added to database!"
            }
            email= request.json.get("email", None)
            comment = request.json.get("comment", None)
            if email is None or comment is None:
                response = {
                    "code": 400,
                    "message": "Keys 'email' or 'comment' were not provided!"
                }
                return jsonify (response), 400
            else:
                cursor = mysql.connection.cursor()
                cursor.execute(POST_COMMENT_QUERY, (email, comment))
                mysql.connection.commit()
                cursor.close()
                return jsonify(response), 201
        
        response = {
            "code": 400,
            "message": "Invalid API key!"
        }
        return jsonify(response), 400
    response = {
            "code": 400,
            "message": "API key required!"
        }
    return jsonify(response), 400

@app.route("/delete-comment/<id>", methods = ["DELETE"])
def delete_comment(id):
    apiKey = request.headers.get('apiKey', None)
    if apiKey is not None:
        url = TOKEN_URL + apiKey
        token = requests.get(url)
        token = token.json()
        if token['message']['valid'] and token['message']['deletePerm'] == 1:
            cursor = mysql.connection.cursor()
            cursor.execute(DELETE_COMMENT_QUERY, [id])
            mysql.connection.commit()
            cursor.close()
            response = {
                "code": 200,
                "message": "Comment has been deleted!"
            }
            return jsonify(response), 200
        response = {
            "code": 400,
            "message": "Invalid API key!"
        }
        return jsonify(response), 400
    response = {
            "code": 400,
            "message": "API key required!"
        }
    return jsonify(response), 400


if __name__ == "__main__":
    app.run(debug=True)