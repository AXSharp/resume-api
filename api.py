from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '---'
app.config['MYSQL_DB'] = 'resume_website'

mysql = MySQL(app)

@app.route("/get-comment/<email>")
def get_comment(email):
    cursor = mysql.connection.cursor()
    cursor.execute( '''SELECT email, comments FROM resume_website.comments WHERE email = %s ;''', [email])
    user_data = cursor.fetchall()
    user_data = user_data[0] 
    mysql.connection.commit()
    cursor.close()
    response = {
        "code" : 200,
        "message": {
            "email": user_data[0],
            "comment": user_data[1]
        } 
    }
    return jsonify (response), 200

@app.route("/create-comment", methods = ["POST"])

def create_comment():
    response = {
        "code": 201,
        "message": "Comment has been added to database!"
    }
    data = request.get_json()
    email= data['email']
    comment = data['comment']
    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO resume_website.comments (email, comments) VALUES(%s,%s);''', (email, comment))
    mysql.connection.commit()
    cursor.close()
    return jsonify(response), 201

if __name__ == "__main__":
    app.run(debug=True)