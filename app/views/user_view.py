from app import app, db
from app.models import User
from flask import jsonify, request
from sqlalchemy import exc

@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(
        [user.to_dict() for user in User.query.all()]
    ), 200


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    required_params = ["email", "first_name", "last_name"]
    try:
        assert all(param in data for param in required_params)
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
    except AssertionError:
        return jsonify(
            {
                "msg": "{0} are required params".format(",".join(required_params))
            }
        ), 400
    except exc.IntegrityError:
        return jsonify(
            {
                "msg": "User email is taken"
            }
        ), 400


@app.route("/users/<email>", methods=["GET"])
def get_user(email):
    user = User.query.get(email)
    if user is None:
        return jsonify(
            {
                "msg": "User not found"
            }
        ), 404
    return jsonify(user.to_dict()), 200