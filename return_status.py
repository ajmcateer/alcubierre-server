from flask import jsonify


def to_error_json(error):
    return jsonify(dict={"Error": error})

def to_success_json(str):
    return jsonify(dict={"Error": str})