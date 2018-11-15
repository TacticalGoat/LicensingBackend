from app import app
from app import License
from datetime import datetime
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
    return json.dumps(data), 200

