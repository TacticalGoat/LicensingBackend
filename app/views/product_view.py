from app import app, db
from app.models import Product
from flask import jsonify, request
from sqlalchemy import exc


@app.route("/products", methods=["GET"])
def list_products():
    products = [p.to_json() for p in Product.query.all()]
    return jsonify(products), 200


@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    required_params = ["name", "platform", "version"]
    try:
        assert all(param in data for param in required_params)
        new_product = Product(name=data["name"],
                              platform=data["platform"],
                              version=data["version"])
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201
    except AssertionError:
        data = {
            "msg": "{0} are required parameters"
                    .format(",".join(required_params))
        }
        return jsonify(data), 400
    except exc.IntegrityError:
        db.session.rollback()
        data = {
            "msg": "This product already exists"
        }
        return jsonify(data), 400


@app.route("/products/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    if product is None:
        return jsonify({
            "msg": "Product does not exist"
        }), 404
    return jsonify(product.to_dict()), 200