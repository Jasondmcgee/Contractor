from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb+srv://peaches:peaches17@cluster0-btqwj.mongodb.net/test?retryWrites=true&w=majority")
database = client.Marketplace
goods = database.Goods
users = database.Users

def get_login_get():
    username = request.args.get('username')
    login = users.find_one({'username':username})
    return login

def get_login_post():
    username = request.form.get('username')
    login = users.find_one({'username': username})
    return login
    
@app.route('/item/<id>')
def contractor_view_item(id):
    item = goods.find_one({'_id':ObjectId(id)})
    login = get_login_get()
    print(item['_id'])
    return render_template('item.html', item=item, login=login)

@app.route('/marketplace', methods=['GET'])
def contractor_marketplace():
    items = goods.find()
    login = get_login_get()
    return render_template('market.html', items=items, login=login)

@app.route('/marketplace', methods=['POST'])
def contractor_new_item():
    username = request.form.get('username')
    item = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'messages': [],
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

@app.route('/home/message_sent', methods=['POST'])
def contractor_after_message():
    username = request.form.get('username')
    message = request.form.get('message')
    item_id = request.form.get('item_id')
    goods.update({'_id': ObjectId(item_id)}, { '$push': {'messages': [message , username]}})
    items = goods.find({'username':username})
    login = users.find_one({'username': username})
    return render_template('home.html', login=login, items=items)

@app.route('/send_message', methods=['POST'])
def contractor_message_owner():
    item_id = request.form.get('item_id')
    login = get_login_post()
    item = goods.find_one({'_id':ObjectId(item_id)})
    return render_template('send_message.html', login=login, item=item)

@app.route('/messages', methods=['POST'])
def contractor_view_messages():
    login = get_login_post()
    items = goods.find()
    messages = []
    show_message = False
    for item in items:
        if (len(item['messages']) > 0):
            for message in item['messages']:
                if (message[1] == login['username'] or item['username'] == login['username']):
                    show_message = True
                    if (show_message):
                        break
            if (show_message):
                messages.append(item)
                print(item['messages'] ,item['username'])
            show_message = False
    return render_template('messages.html', login=login, items=items, messages=messages)

@app.route('/')
def contractor_login():
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)