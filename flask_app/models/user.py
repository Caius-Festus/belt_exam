from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from flask_app.models import magazine

DATABASE = "belt_exam"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.[a-z])(?=.[A-Z])(?=.[0-9])[A-Za-z\d@$!#%*?&]{6,20}$')

class User:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.subscribed_to = []

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users"
        return connectToMySQL(DATABASE).query_db(query)

    @classmethod
    def add_user(cls, data):
        query="INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def update_user(cls, data):
        query="UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(user_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT id, first_name, last_name, email, password FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            flash("Email not in use!")
            return False
        return results[0]

    
    @classmethod
    def recipes_created_by_user(cls, data):
        query = "SELECT * FROM recipes WHERE user_id = %(user_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_login(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Invalid Email Address!")
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters in length")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_registration(data):
        is_valid = True
        for piece in data:
            # print(piece)
            if not data[piece]:
                flash("All fields are required")
                is_valid = False
                break
        if len(data['first_name']) < 3:
            flash("Fist name must be at least 3 character long")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 character long")
            is_valid = False
        # check for valid email
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email Address!")
            is_valid = False
        query="SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            flash("Email already in use")
            is_valid = False
        # check for valid password
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters in length")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match!")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_update(data):
        is_valid = True
        for piece in data:
            # print(piece)
            if not data[piece]:
                flash("All fields are required")
                is_valid = False
                break
        if len(data['first_name']) < 3:
            flash("Fist name must be at least 3 character long")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 character long")
            is_valid = False
        # check for valid email
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email Address!")
            is_valid = False
        query="SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            flash("Email already in use")
            is_valid = False
        return is_valid


    # @classmethod
    # def get_user(cls, data:dict):
    #     query="SELECT * FROM users LEFT JOIN user_has_magazine ON user_has_magazine.user_id = users.id LEFT JOIN magazines ON user_has_magazine.magazine_id = magazines.id WHERE users.id = %(user_id)s;"
    #     results = connectToMySQL(DATABASE).query_db(query, data)
    #     subscriptions = cls( results[0] )
    #     for row_from_db in results:
    #         magazine_data = {
    #             'id' : row_from_db['id'],
    #             'title' : row_from_db['title'],
    #             'description' : row_from_db['description'],
    #             'created_at' : row_from_db['created_at'],
    #             'updated_at' : row_from_db['updated_at'],
    #             'creator_id' : row_from_db['creator_id'],
    #             'creator_name' : row_from_db['creator_name']
    #         }
    #         subscriptions.subscribed_to.append(magazine.Magazine(magazine_data))
    #         return subscriptions

