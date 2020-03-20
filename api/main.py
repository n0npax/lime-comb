import googleclouddebugger
import googlecloudprofiler
import graphene
from flask import Flask
from flask_graphql import GraphQLView
from lime_comb_api.auth import jwt_validate
from lime_comb_api.schema import Mutation, Query

"""googleclouddebugger.enable()
googlecloudprofiler.start(
    service="lime-comb-api",
    service_version="0.0.0",
    # verbose is the logging level. 0-error, 1-warning, 2-info,
    # 3-debug. It defaults to 0 (error) if not set.
    verbose=3,
    # project_id must be set if not running on GCP.
    # project_id='lime-comb',
)
"""

schema = graphene.Schema(query=Query)


view_func = GraphQLView.as_view(
    "graphql",
    schema=graphene.Schema(query=Query, mutation=Mutation),
    graphiql=True,
    # get_context=lambda: {"session": db_session},
)

app = Flask(__name__)
app.add_url_rule("/", view_func=jwt_validate(view_func))


if __name__ == "__main__":
    app.run()
