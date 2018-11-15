from app import app
import json

@app.errorhandler(404)
def not_found(e):
    return json.dumps({"msg": "resource not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    return json.dumps({"msg": "internal server error"}), 500