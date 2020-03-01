import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from users where username=?"
        result = cursor.execute(query, (username,))   # parameters for SQL always have to be in tuple eventhough if its single value

        row = result.fetchone()
        if row:              #If row is Not none
            user = cls(*row)    # Expands to User(row[0], row[1], row[2])
        else:
            user = None
        
        connection.close()
        return user     # Returning User object or None

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from users where id=?"
        result = cursor.execute(query,(_id,))   # parameters for SQL always have to be in tuple eventhough if its single value

        row = result.fetchone()
        if row:              #If row is none
            user = cls(*row)    # Expands to User(row[0], row[1], row[2])
        else:
            user = None
        
        connection.close()
        return user     # Returning User object or None

    @classmethod
    def get_all_users(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from users"
        result = cursor.execute(query)   # parameters for SQL always have to be in tuple eventhough if its single value

        row = result.fetchall()
        return row

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required = True,
        help = 'Please provide all the mandatory field data'
    )
    parser.add_argument('password',
        type = str,
        required = True,
        help = 'Please provide all the mandatory field data'
    )


    def post(self):

        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'Message': 'User {} does not exists'.format(data['username'])}, 400

        conn = sqlite3.connect('data.db')
        cur = conn.cursor()

        query = "Insert into users values(null, ?, ?)"
        cur.execute(query, (data['username'], data['password']))    # provide user, pass in tuple even if only one arg is needed

        conn.commit()
        conn.close()
        return {'Message': 'User created successfully!'}, 201

class AllUsers(Resource):
    def get(self):
        return {'Users' : User.get_all_users()}
        
