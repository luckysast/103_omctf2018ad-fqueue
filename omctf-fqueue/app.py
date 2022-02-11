from flask import Flask, jsonify, request
from models import *
from service import Service

app = Flask(__name__)
service = Service()


@app.route('/')
def index():
    return jsonify(name='FQueue REST API Service',
                   version='1.0'), 200


@app.route('/claims', methods=["POST"])
def add_new_claim():
    data = request.get_json()

    if data is None:
        return make_bad_request('it is not json')

    if ('flag' in data) & ('team' in data):
        claim = Claim(data['flag'], data['team'])
        try:
            cipher_claim = service.add_new_claim(claim)
            response = jsonify({'id': cipher_claim.id, 'cipher_text': cipher_claim.cipher_text, 'key': cipher_claim.key})
            response.status_code = 201
            return response
        except Exception:
            return make_bad_request('error in add claim')
    else:
        response = jsonify({'error': 'Incorrect json'})
        response.status_code = 400
        return response


@app.route("/claims/<claim_id>", methods=["GET"])
def get_claim(claim_id):
    try:
        cipher_claim = service.get_cipher_claim_by_id(claim_id)
        if cipher_claim is not None:
            response = jsonify(cipher_claim)
            response.status_code = 200
            return response
        else:
            message = {'error': 'Claim with id: %s was not found' % str(claim_id)}
            resp = jsonify(message)
            resp.status_code = 404
    except Exception:
        return make_bad_request('error in get claim')

@app.route("/claims/recent", methods=["GET"])
def get_recent():
    try:
        claims = service.get_recent()
        result = []
        for item in claims:
            result.append({'claim_id': item[0], 'cipher_text': item[1]})
        recent = jsonify(recent = result)
        response = recent
        response.status_code = 200
        return response
    except Exception:
        return make_bad_request('error in process claims')

@app.route("/claim/<claim_id>/decrypt", methods=["POST"])
def decrypt(claim_id):
    try:
        cipher_claim = service.get_cipher_claim_by_id(claim_id)
        if cipher_claim is None:
            message = {'error': 'Claim with id: %s was not found' % str(claim_id)}
            resp = jsonify(message)
            resp.status_code = 404
            return resp
    except Exception:
        return make_bad_request('error in get claim cipher_text')

    data = request.get_json()

    if data is None:
        return make_bad_request('it is not json')

    if 'key' in data:
        key = data['key']
        try:
            decrypted = service.decrypt_claim(cipher_claim['cipher_text'], key)
            response = jsonify({'plain_text': decrypted.decode('utf-8')})
            response.status_code = 200
            return response
        except Exception:
            return make_bad_request('error in decryption')
    else:
        response = jsonify({'error': 'Incorrect key'})
        response.status_code = 400
        return response


def make_bad_request(message):
    response = jsonify({'error': message})
    response.status_code = 400
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5535)
