import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=int,
    required=True,
    help='This cant be left blank and should be integer'
    )

    @classmethod
    def find_by_name(cls, name):        # Class method to make things easier without duplicating a code
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from items where name=?"

        result = cursor.execute(query, (name,)).fetchone()
        connection.close()

        if result:
            return {'Item' : { 'name' : result[0], 'price' : result[1]}}
        return None

    @jwt_required()     #You can put this on any of the below methods to make authentication nececssary for an user 
    def get(self,name):

        item = self.find_by_name(name)
        if item:
            return item
        return {'Message': 'Item {} not found'.format(name)}


    def post(self,name):
        if self.find_by_name(name):
            return {'Messageg' : 'Item {} already exists'.format(name)}

        # req_data = request.get_json()
        req_data = Item.parser.parse_args()

        new_item = {
            'name' : name,
            'price' : req_data['price']
            } 

        try:
            self.insesrt_item(new_item)
        except:
            return {'Message' : 'An error occured while insertion'}, 500    # Internal server error
        
        return new_item, 201

    @classmethod
    def insesrt_item(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "insert into items values(?,?)"

        cursor.execute(query, (item['name'],item['price']))
        connection.commit()
        connection.close()
    
    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "update items set value =? where name=?)"

        cursor.execute(query, (item['price'],item['name']))
        connection.commit()
        connection.close()

    def put(self, name):

        # req_data = request.get_json()
        req_data = Item.parser.parse_args()
        
        item = self.find_by_name(name)
        updated_item = {'name' : name, 'price': req_data['price']}

        if item is None:
            self.insesrt_item(updated_item)
            return {'Message': 'Item {} inserted'.format(updated_item)}
        else:
            self.update(updated_item)
            return {'Message': 'Item {} updated'.format(updated_item)}
        return item

    def delete(self,name):
        if not self.find_by_name(name):
            return {'Messageg' : 'Item {} does not exists'.format(name)}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "delete from items where name = ?"

        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'Message': 'Item {} deleted'.format(name)}



class Item_list(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select * from items"

        result = cursor.execute(query).fetchall()

        connection.close()

        if result:
            return {'Items' : result}
        return {'Message','No Items found'}, 404
        