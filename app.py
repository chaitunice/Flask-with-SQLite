from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity # our security.py file
from user import UserRegister, User, AllUsers
from Item import Item, Item_list

app = Flask(__name__)
app.secret_key = 'mypass'
api = Api(app)

    # To set apps secret key
jwt = JWT(app, authenticate, identity)  #returns a JWT Token


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Item_list, '/items')           # New resource as the end point changed here
api.add_resource(UserRegister, '/Register')     # New resource to register users
api.add_resource(AllUsers, '/Users')            # New resource to fetch all users

if __name__ == "__main__":          # This makes sure app.run doesn't run on importing app.py
    app.run(port=5000)
