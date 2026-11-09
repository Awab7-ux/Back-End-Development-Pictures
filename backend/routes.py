from flask import jsonify, request

from . import app, data


@app.get("/health")
def health():
    return jsonify({"status": "OK"}), 200


@app.get("/count")
def count():
    return jsonify({"length": len(data)}), 200


@app.get("/picture")
def get_pictures():
    return jsonify(data), 200


@app.get("/picture/<int:picture_id>")
def get_picture(picture_id):
    picture = next((item for item in data if item.get("id") == picture_id), None)
    if picture is None:
        return jsonify({"message": "picture not found"}), 404
    return jsonify(picture), 200


@app.post("/picture")
def create_picture():
    picture = request.get_json(silent=True)
    if not isinstance(picture, dict) or "id" not in picture:
        return jsonify({"message": "a picture with an id is required"}), 400

    if any(item.get("id") == picture["id"] for item in data):
        return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302

    data.append(picture)
    return jsonify(picture), 201


@app.put("/picture/<int:picture_id>")
def update_picture(picture_id):
    index = next((i for i, item in enumerate(data) if item.get("id") == picture_id), None)
    if index is None:
        return jsonify({"message": "picture not found"}), 404

    picture = request.get_json(silent=True)
    if not isinstance(picture, dict):
        return jsonify({"message": "a picture object is required"}), 400

    data[index] = picture
    return jsonify(picture), 200


@app.delete("/picture/<int:picture_id>")
def delete_picture(picture_id):
    index = next((i for i, item in enumerate(data) if item.get("id") == picture_id), None)
    if index is None:
        return jsonify({"message": "picture not found"}), 404

    data.pop(index)
    return "", 204