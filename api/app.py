from flask import Flask
import graphene
from flask_graphql import GraphQLView

from schema import Query
import data

schema = graphene.Schema(query=Query)


view_func = GraphQLView.as_view(
    "graphql", schema=graphene.Schema(query=Query), graphiql=True
)

app = Flask(__name__)
app.add_url_rule("/", view_func=view_func)

if __name__ == "__main__":
    data.setup()
    app.run()
