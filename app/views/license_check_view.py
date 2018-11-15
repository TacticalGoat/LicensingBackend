from app import app, License, db
from datetime import datetime
from flask import jsonify, request
from sqlalchemy import exc
import json


@app.route("/license/machine/<id>", methods=["GET"])
def check_license(id):
    license = License.query.filter_by(machine_id=id).first_or_404()
    now = datetime.utcnow()
    data = {
        "machine_id": license.machine_id,
        "start_time": str(license.start_time),
        "end_time": str(license.end_time)
    }
    if license.end_time <= now:
        data["status"] = False
    else:
        data["status"] = True
    return jsonify(data)


@app.route("/license/machine", methods=["POST"])
def create_license():
    data = request.get_json()
    required_params = ["machine_id", "start_time", "end_time"]
    try:
        assert all(param in data for param in required_params)
        data["start_time"] = datetime.fromtimestamp(int(data["start_time"]))
        data["end_time"] = datetime.fromtimestamp(int(data["end_time"]))
        new_license = License(**data)
        db.session.add(new_license)
        db.session.commit()
        data = {
            "machine_id": new_license.machine_id,
            "start_time": str(new_license.start_time),
            "end_time": str(new_license.end_time)
        }
        return jsonify(data)
    except AssertionError:
        return jsonify(
            {
                "msg": "{0} are required parameters for this operation"
                .format(", ".join(required_params))
            }
        ), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(
            {
                "msg": "Already Exists"
                .format(", ".join(required_params))
            }
        ), 400
