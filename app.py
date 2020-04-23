from os import environ
from flask import Flask, request
from cryptography.fernet import Fernet
import base64
import hashlib


app = Flask(__name__)
expected_token = b'yes'
secret_key = 'abc123'
secret_key_hash = hashlib.sha256(secret_key.encode())
secret_key_fernet = base64.urlsafe_b64encode(secret_key_hash.digest())
cipher_suite = Fernet(secret_key_fernet)


@app.route('/auth', methods=['POST'])
def auth():
    body = request.get_json()
    token = body.get('token')

    try:
        decrypted_token = cipher_suite.decrypt(token.encode())
    except:
        return f"except: {token}"

    if decrypted_token == expected_token:
        return "success"
    else:
        return f"fail: {decrypted_token}"


if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
