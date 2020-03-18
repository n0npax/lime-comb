from flask import Flask
import graphene
from flask_graphql import GraphQLView

from schema import Query, Mutation

schema = graphene.Schema(query=Query)


view_func = GraphQLView.as_view(
    "graphql", schema=graphene.Schema(query=Query, mutation=Mutation), graphiql=True
)

app = Flask(__name__)
app.add_url_rule("/", view_func=view_func)

if __name__ == "__main__":
    app.run()
