from flask_app.config.mysqlconnection import connectToMySQL
#in the class apps you need this ^ written from folder to file 
from flask import flash
from flask_app.models import user

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.description = data['description']
        self.user_id = data['user_id']
        self.current_user = None

    @staticmethod
    def validate_comment(data):
        is_valid = True
        if len(data['description']) < 5:
            flash("Comment must be at least 5 characters long.")
            is_valid = False
        return is_valid

    @classmethod 
    def get_all_comments(cls):
        query = "SELECT * FROM weddingProject.comments JOIN users on comments.user_id = users.id;"
        results = connectToMySQL("weddingProject").query_db(query)

        comments=[]

        for row in results:
            comment = cls(row)
            user_information = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email_address': row['email_address'],
                'password': row['password'],
            }
            comment.current_user = user.User(user_information)
            comments.append(comment)

        return comments
# --------------------------


    @classmethod
    def get_id(cls, data):
        query = "SELECT * FROM weddingProject.comments JOIN users on comments.user_id = users.id WHERE comments.id = %(id)s;"

        result = connectToMySQL("weddingProject").query_db(query, data)
        if not result:
            return False
        
        result = result[0]
        comment = cls(result)

        user_information = {
                'id': result['users.id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email_address': result['email_address'],
                'password': result['password']
            }
        comment.current_user = user.User(user_information)
        return comment
    @classmethod
    def delete_comment(cls,data):
        query = "DELETE FROM `weddingProject`.`comments` WHERE id =%(id)s"
        return connectToMySQL('weddingProject').query_db(query, data)
# ------------------------------
    @classmethod
    def update_comment(cls,data):
        query = 'UPDATE weddingProject.comments SET description = %(description)s WHERE id = %(id)s;'
        return connectToMySQL('weddingProject').query_db(query,data)

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO weddingProject.comments (description,user_id) VALUES (%(description)s,%(user_id)s);'
        return connectToMySQL('weddingProject').query_db(query,data)

