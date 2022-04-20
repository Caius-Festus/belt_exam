from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash, re
from flask_app.models import user
from flask_app.models.user import DATABASE

class Magazine:
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']
        self.creator_name = data['creator_name']
        self.subscribed_by = []

    # @classmethod
    # def get_magazine(cls, data:dict):
    #     query="SELECT * FROM magazines LEFT JOIN user_has_magazine ON user_has_magazine.magazine_id = magazines.id LEFT JOIN users ON user_has_magazine.user_id = users.id WHERE magazines.id = %(id)s;"
    #     results = connectToMySQL(DATABASE).query_db(query, data)
    #     print(results)
    #     magazine = cls( results[0] )
    #     for row_from_db in results:
    #         user_data = {
    #             "id" : row_from_db["id"],
    #             "first_name" : row_from_db["first_name"],
    #             "last_name" : row_from_db["last_name"],
    #             "email" : row_from_db["email"],
    #             "password" : row_from_db["password"],
    #             "created_at" : row_from_db["created_at"],
    #             "updated_at" : row_from_db["updated_at"],
    #         }
    #         magazine.subscribed_by.append(user.User(user_data))
    #         return magazine

    @classmethod
    def get_magazine(cls, data:dict):
        query="SELECT magazines.id, magazines.title, magazines.description, magazines.creator_id, magazines.creator_name, users.id, users.first_name, users.last_name, users.email, users.password, users.created_at, users.updated_at, user_has_magazine.user_id AS user_magazine FROM magazines LEFT JOIN user_has_magazine ON user_has_magazine.magazine_id = magazines.id LEFT JOIN users ON user_has_magazine.user_id = users.id WHERE magazines.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        magazine = cls( results[0] )
        for row_from_db in results:
            magazine.subscribed_by.append(row_from_db["user_magazine"])
        print(magazine)
        return magazine

    # @classmethod
    # def get_magazine_users(cls, data:dict):
    #     query="SELECT magazines.title, magazines.description, magazines.creator_id, magazines.creator_name, users.id, users.first_name, users.last_name, users.email, users.password, users.created_at, users.updated_at, user_has_magazine.user_id AS user_magazine FROM magazines LEFT JOIN user_has_magazine ON user_has_magazine.magazine_id = magazines.id LEFT JOIN users ON user_has_magazine.user_id = users.id WHERE magazines.id = %(id)s;"
    #     results = connectToMySQL(DATABASE).query_db(query, data)
    #     print(results)
    #     magazine = cls( results[0] )
    #     for row_from_db in results:
    #         magazine.subscribed_by.append(row_from_db["user_magazine"])
    #     print(magazine)
    #     return magazine

    @classmethod
    def get_full_magazine(cls, data:dict):
        query="SELECT * FROM magazines LEFT JOIN user_has_magazine ON user_has_magazine.magazine_id = magazines.id LEFT JOIN users ON user_has_magazine.user_id = users.id WHERE magazines.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        magazine = cls( results[0] )
        for row_from_db in results:
            user_data = {
                'id' : row_from_db['id'],
                'first_name' : row_from_db['first_name'],
                'last_name' : row_from_db['last_name'],
                'email' : row_from_db['email'],
                'password' : row_from_db['password'],
                'created_at' : row_from_db['created_at'],
                'updated_at' : row_from_db['updated_at']
            }
            magazine.subscribed_by.append(user.User(user_data))
        return magazine

    @classmethod
    def get_all_magazines(cls):
        query="SELECT magazines.id FROM magazines"
        results = connectToMySQL(DATABASE).query_db(query)
        return results

    @classmethod
    def get_magazines_created_by(cls, data):
        query = "SELECT *, COUNT(user_has_magazine.user_id) AS sub_count FROM magazines LEFT JOIN user_has_magazine ON user_has_magazine.magazine_id = magazines.id WHERE creator_id = %(user_id)s GROUP BY magazines.id;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_subbed_mags_by(cls, data):
        query = "SELECT *, COUNT(user_has_magazine.user_id) AS sub_count FROM magazines LEFT JOIN user_has_magazine ON user_has_magazine.magazine_id = magazines.id WHERE user_has_magazine.user_id = %(user_id)s GROUP BY magazines.id;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def add_magazine(cls, data:dict):
        query = "INSERT INTO magazines (title, description, created_at, updated_at, creator_id, creator_name) VALUES (%(title)s, %(description)s, NOW(), NOW(), %(user_id)s, %(user_name)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_magazine(cls, data:dict):
        query1 = "DELETE FROM user_has_magazine WHERE user_has_magazine.magazine_id=%(id)s"
        connectToMySQL(DATABASE).query_db(query1, data)
        query = "DELETE FROM magazines WHERE magazines.id=%(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def subscribe(cls, data:dict):
        query = "INSERT INTO user_has_magazine (user_id, magazine_id) VALUES (%(user_id)s, %(magazine_id)s)"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def unsub(cls, data: dict):
        query = "DELETE FROM user_has_magazine WHERE user_id=%(user_id)s, magazine_id=%(magazine_id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate_magazine(data:dict):
        is_valid = True
        if not len(data['title']) > 1:
            flash("Title must be at least two characters long!")
            is_valid = False
        if not len(data['description']) > 9:
            flash("description must be at least 10 characters long!")
            is_valid = False
        return is_valid


    # @classmethod
    # def get_users_subbed_magazines(cls, data):
    #     query = "SELECT * FROM magazines LEFT JOIN user_has_magazine ON user_has_magazine.magazine_id = magazines.id WHERE user_has_magazine.user_id = 1"
    #     results = connectToMySQL(DATABASE).query_db(query, data)
    #     return connectToMySQL(DATABASE).query_db(query, data)

    # @classmethod
    # def get_all_thoughts(cls):
    #     query = "SELECT thoughts.id, thoughts.content, users.id AS creator_id, users.first_name AS creator_name, user_likes_thought.user_id AS user_id_likes, COUNT(user_likes_thought.thought_id) AS number_liked FROM thoughts LEFT JOIN user_likes_thought ON user_likes_thought.thought_id = thoughts.id LEFT JOIN users ON thoughts.created_by = users.id GROUP BY thoughts.id ORDER BY thoughts.created_at DESC;"
    #     return connectToMySQL(DATABASE).query_db(query)

    # @classmethod
    # def delete_thought(cls, data:dict):
    #     query = "DELETE FROM thoughts WHERE id=%(id)s"
    #     return connectToMySQL(DATABASE).query_db(query, data)

    # @classmethod
    # def add_user_likes_thought(cls, data:dict):
    #     query = "INSERT INTO user_likes_thought (user_id, thought_id) VALUES (%(user_id)s, %(thought_id)s)"
    #     return connectToMySQL(DATABASE).query_db(query, data)

    # @classmethod
    # def remove_user_likes_thought(cls, data:dict):
    #     query = "DELETE FROM user_likes_thought WHERE thought_id=%(thought_id)s AND user_id=%(user_id)s"
    #     return connectToMySQL(DATABASE).query_db(query, data)

    # @staticmethod
    # def validate_thought(data:dict):
    #     is_valid = True
    #     if not len(data['content']) > 3:
    #         flash("Thought must be more than 3 characters long!")
    #         is_valid = False
    #     return is_valid
        