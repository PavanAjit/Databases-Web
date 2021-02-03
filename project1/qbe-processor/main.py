from flask import Flask
from flask_graphql import GraphQLView
from qbe import schema
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

if __name__ == '__main__':
    app.run()

app.run(debug=True)
