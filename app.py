from flask import Flask, request, redirect, url_for, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb+srv://gowthamsiddharthan88:76SVBfLTQhaHZM20@cluster0.dcrypio.mongodb.net/")
db = client["userdb"]
users_collection = db["users"]

@app.route('/')
def index():
    users = list(users_collection.find())
    return render_template("index.html", users=users)

@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    age = request.form['age']
    users_collection.insert_one({'name': name, 'age': age})
    return redirect(url_for('index'))

@app.route('/edit/<user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if request.method == 'POST':
        users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {
            'name': request.form['name'],
            'age': request.form['age']
        }})
        return redirect(url_for('index'))
    return render_template("edit.html", user=user)

@app.route('/delete/<user_id>')
def delete(user_id):
    users_collection.delete_one({'_id': ObjectId(user_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 
