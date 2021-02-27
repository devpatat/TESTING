from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    return "Hello World,Dev!"

class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')  # read local CSV
        data = data.to_dict()  # convert dataframe to dict
        return {'data': data}, 200  # return data and 200 OK

api.add_resource(Users, '/users')  # add endpoints
api.add_resource(Locations, '/locations')

if __name__ == '__main__':
    app.run()  # run our print hellolask app