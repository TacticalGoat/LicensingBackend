from app import app, db
from app.models import License, User, Product
from datetime import datetime
from flask import jsonify, request
from sqlalchemy import exc
import json


@app.route("/licenses/status")
def check_status():
    data = {
        "user_email": request.args.get("email", None),
        "product_id": request.args.get("product", None),
        "account_number": request.args.get("account_number", None)
    }
    required_params = ["user_email", "product_id", "account_number"]
    try:
        assert all(data[key] is not None for key in data)
        license = License.query.filter_by(user_email=data["user_email"],
                                          product_id=data["product_id"],
                                          account_number=data["account_number"]
                  ).first()
        if license is None:
            return jsonify({
                "msg": "User or license don't exist"
            }), 400
        output = license.to_dict()
        if datetime.utcnow() >= license.end_time:
            output["status"] = False
        else:
            output["status"] = True
        return jsonify(output), 200
    except AssertionError:
        return jsonify(
            {
                "msg": "{0} are required parameters"
                       .format(",".join(required_params))
            }
        ), 400


@app.route("/licenses", methods=["GET"])
def list_licenses():
    data = [license.to_dict() for license in License.query.all()]
    return jsonify(data), 200


@app.route("/licenses/<id>", methods=["GET"])
def get_license():
    license = License.query.get(id)
    if license is None:
        return jsonify(
            {
                "msg": "License not found."
            }, 404
        )
    return jsonify(license.to_dict()), 200


@app.route("/licenses", methods=["POST"])
def create_license():
    data = request.get_json()
    required_params = ["user_email", "product_id", "start_time", "end_time", "account_number"]
    try:
        assert all(param in data for param in required_params)
        user = User.query.get(data["user_email"])
        product = Product.query.get(data["product_id"])
        if user is None:
            return jsonify({
                "msg": "User does not exist"
            }), 400
        
        if product is None:
            return jsonify({
                "msg": "Product does not exists"
            }), 400
        new_license = License(
            account_number=data["account_number"],
            user=user,
            product=product,
            start_time=datetime.fromtimestamp(int(data["start_time"])),
            end_time=datetime.fromtimestamp(int(data["end_time"]))
        )
        db.session.add(new_license)
        db.session.commit()
        return jsonify(new_license.to_dict()), 201
    except AssertionError:
        return jsonify({
            "msg": "{0} are required params".format(required_params)
        }), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({
            "msg": "A License for the product already exists"
        }), 400
        

