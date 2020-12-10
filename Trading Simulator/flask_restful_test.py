from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

people = {
    1: {
        'name': 'First Person',
        'course': 'Artificial Intelligence & Machine Learning',
        'location': 'Toronto'
    },
    2: {
        'name': 'Second Person',
        'course': 'Business Management',
        'location': 'Vancouver'
    }
}

parser = reqparse.RequestParser()


class People(Resource):
    def get(self):
        parser.add_argument('id', type=int)
        args = parser.parse_args()
        if args['id'] in people:
            return jsonify(people[args['id']])

    def post(self):
        parser.add_argument('name', type=str)
        parser.add_argument('id', type=int)
        parser.add_argument('course', type=str)
        parser.add_argument('location', type=str)
        args = parser.parse_args()
        people[args['id']] = {
            'name': args['name'],
            'course': args['course'],
            'location': args['location']
        }
        print("Updated People Dictionary - ", people)
        return f"added {args['name']} with {args['id']}"


api.add_resource(People, '/')

if __name__ == '__main__':
    app.run(debug=True)
