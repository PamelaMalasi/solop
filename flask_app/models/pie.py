from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
mydb = 'pypie_derby'

class Pie:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name'] 
        self.filling = data['filling']
        self.crust = data['crust']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.baker_id = data['baker_id']
        self.consumer_id = data['consumer_id']
        self.votes = data['votes']
    
    @classmethod
    def save(cls,data):
        query = '''
        INSERT INTO pies(name,filling,crust,baker_id)
        VALUES (%(name)s,%(filling)s,%(crust)s,%(baker_id)s);
        '''
        return connectToMySQL(mydb).query_db(query,data)
    
    @classmethod
    def like(cls,data):
        query = '''
        UPDATE pies
        SET votes = votes + 1,consumer_id = %(consumer_id)s
        WHERE id = %(id)s;
        '''
        connectToMySQL(mydb).query_db(query,data)

    @classmethod
    def dislike(cls,data):
        query = '''
        UPDATE pies
        SET votes = votes - 1,consumer_id = NULL
        WHERE id = %(id)s;
        '''
        connectToMySQL(mydb).query_db(query,data)
    
    @classmethod
    def edit(cls,data):
        query = '''
        UPDATE pies
        SET name = %(name)s, filling = %(filling)s, crust = %(crust)s
        WHERE id = %(id)s;
        '''
        connectToMySQL(mydb).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = '''
        DELETE FROM pies
        WHERE id = %(id)s;'''
        connectToMySQL(mydb).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query = '''
        SELECT *
        FROM pies
        WHERE baker_id = %(id)s;
        '''
        result = connectToMySQL(mydb).query_db(query,data)
        output = []
        print(result)
        for row in result:
            output.append(cls(row))
        return output
    
    @classmethod
    def get_all(cls):
        query = '''
        SELECT *
        FROM pies
        JOIN users
        ON pies.baker_id = users.id
        ORDER BY votes DESC;
        '''
        results = connectToMySQL(mydb).query_db(query)
        return results
    
    @classmethod
    def get_one(cls,data):
        query = '''
        SELECT *
        FROM pies
        JOIN users
        ON pies.baker_id = users.id
        WHERE pies.id = %(id)s;'''
        results = connectToMySQL(mydb).query_db(query,data)[0]
        print(results)
        return results

    @staticmethod
    def validate_pie(pie):
        is_valid = True
        if len(pie['name']) < 1:
            flash('Pie must have name.', 'add_pie')
            is_valid = False
        if len(pie['filling']) < 1:
            flash('Pie must have a filling.', 'add_pie')
            is_valid = False
        if len(pie['crust']) < 1:
            is_valid = False
            flash('Pie must have a crust', 'add_pie')
        return is_valid


