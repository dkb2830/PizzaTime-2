# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.order import Order


methods_JSON=[{'method': 'Carry Out','price':0}, {'method': 'Delivery','price':10}]
size_JSON=[{'size': 'Small','price':10}, {'size': 'Medium','price':15}, {'size': 'Large','price':20}, {'size': 'X-Large','price':25}]
crust_JSON=[{'crust': 'Thin Crust','price':0}, {'crust': 'Hand Tossed','price':5}, {'crust': 'Stuffed crust','price':10}]
quantity_JSON=[{'qty': 1}, {'qty': 2}, {'qty': 3}, {'qty': 4}, {'qty': 5}]
toppings_JSON = [{'topping':'Pepperoni','price':1},{'topping':'Olives','price':1},{'topping':'Bacon','price':1},{'topping':'Peppers','price':1},{'topping':'Pineapple','price':1},{'topping':'Spinach','price':1},]

class User:
    db = 'pizza_petes'
    def __init__( self , data ):
        self.id = data['id']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.email = data['email']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.password = data['password']
        self.favorite_order = data['favorite_order']
        self.created_at = ''
        self.updated_at = ''
    # Now we use class methods to query our database
        self.orders = []
        
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db( query, data)
        
        print(results[0])
        return cls(results[0])

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET firstname=%(firstname)s, lastname=%(lastname)s, email=%(email)s, address%(address)s, city=%(city)s, state=%(state)s WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
        
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( firstname , lastname , email, password, address, city, state) VALUES ( %(fname)s , %(lname)s , %(email)s, %(password)s, %(address)s, %(city)s, %(state)s);"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db( query, data )
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db( query, data)
        
        if len(results) < 1:
            return False
        
        return cls(results[0])
    
    @classmethod
    def get_orders_by_user(cls, data):
        query = "SELECT orders.* FROM orders WHERE orders.user_id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def update_user_favorite(cls, data):
        query = "UPDATE users SET favorite = %(favorite)s WHERE id = %(id)s;"
        
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_favorite_order(cls, data):
        query = "SELECT orders.* FROM orders WHERE orders.id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        
        if len(results) < 1:
            return False
        
        return Order(results[0])

    @staticmethod
    def calcOrderTotal(info):
        num_sum = 0
        
        for m in methods_JSON:
            print(m['method'], m['price'])
            if info['method'] == m['method']:
                num_sum += m['price']
                
        for s in size_JSON:
            print(s['size'], s['price'])
            if info['size'] == s['size']:
                num_sum += s['price']
                
        for c in crust_JSON:
            print(c['crust'], c['price'])
            if info['crust'] == c['crust']:
                num_sum += c['price']

        num_sum += info['number_of_toppings'] * 1
        
        num_sum = (num_sum * int(info['quantity']))
        return num_sum