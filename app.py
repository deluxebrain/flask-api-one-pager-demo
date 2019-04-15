import datetime as dt

from flask import Flask, Blueprint, jsonify
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import fields, validates_schema, ValidationError
from flask_marshmallow import Marshmallow

spec = APISpec(
   title='Flask Api One-Pager Demo',
   version='1.0.0',
   openapi_version='3.0.2',
   plugins=[
      FlaskPlugin(),
      MarshmallowPlugin(),
   ]
)
app = Flask(__name__)
api = Blueprint('api', __name__, url_prefix="/api")
ma = Marshmallow(app)
ma.init_app(app)

class User(object):
    def __init__(self, name, email):
        self.id = 1
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)

class UserParameter(ma.Schema):
    user_id = fields.Int(required=True)

class UserSchema(ma.Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.Date(required=True)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.user_detail', user_id='<id>'),
        'collection': ma.URLFor('api.user_listing')
    })

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@api.route('/users')
def user_listing():
    """User listing view.
    ---
    get:
        description: Get user listing
        responses:
            200:
                description: User listing
                schema: UserSchema
    """
    users = [ User(name="Bob", email="bob@example.com") ]
    return users_schema.jsonify(users)

@api.route('/users/<user_id>')
def user_detail(user_id):
    """User detail view.
    ---
    get:
        description: Get user by id
        parameters:
            - in: user_id
              schema: UserParameter
        responses:
            200:
                description: The specified user
                schema: UserSchema
    """
    the_user = User(name="Bob", email="bob@example.com")
    return user_schema.jsonify(the_user)

@api.route('/swagger')
def get_swagger():
    return jsonify(spec.to_dict())

app.register_blueprint(api)

with app.test_request_context():
    spec.path(view=user_detail)
