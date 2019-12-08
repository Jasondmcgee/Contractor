from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb+srv://peaches:peaches17@cluster0-btqwj.mongodb.net/test?retryWrites=true&w=majority")
database = client.Marketplace
goods = database.Goods
users = database.Users

@app.route('/marketplace')
def contractor_marketplace():
    items = goods.find()
    return render_template('market.html', items=items)

@app.route('/marketplace', methods=['POST'])
def contractor_new_item():
    username = request.form.get('username')
    print(username)
    item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'username': username
    }
    if (item['title'] != None):
        goods.insert_one(item)
    items = goods.find()
    login = users.find_one({'username': username})
    return render_template('market.html', login=login, items=items)

@app.route('/home', methods=['POST'])
def contractor_home():
    username = request.form.get('username')
    password = request.form.get('password')
    user = {
        'username': username,
        'password': password
    }
    login = users.find_one({'username':username, 'password':password})
    if(login is None):
        users.insert_one(user)
    login = users.find_one({'username':username, 'password':password})
    items = goods.find({'username':login['username']})
    return render_template('home.html', login=login, items=items)

@app.route('/home/removed', methods=['POST'])
def contractor_delete_item():    
    deleted_item_id = request.form.get('objid')
    username = request.form.get('username')
    if(deleted_item_id != None):
        goods.delete_one({'_id':ObjectId(deleted_item_id)})
    items = goods.find({'username': username})
    login = users.find_one({'username': username})
    return render_template('home.html', login=login, items=items)

@app.route('/')
def contractor_login():
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)