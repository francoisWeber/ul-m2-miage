#!/usr/bin/env python3
from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

def text_to_vector(text):
    """Generate a reproducible 64-dimensional vector from text."""
    if not text:
        text = ""
    
    # Create hash from text (SHA256 produces 32 bytes)
    text_bytes = text.encode('utf-8')
    hash_obj = hashlib.sha256(text_bytes)
    hash_digest = hash_obj.digest()
    
    # Split each byte into two 4-bit chunks (64 chunks total from 32 bytes)
    vector = []
    for byte in hash_digest:
        # Upper 4 bits
        vector.append((byte >> 4) / 15.0)
        # Lower 4 bits
        vector.append((byte & 0x0F) / 15.0)
    
    return vector

@app.route('/vectorize', methods=['GET'])
def vectorize():
    # Accept JSON payload from request body or query string
    if request.is_json:
        data = request.get_json()
    else:
        # Try to parse from query string if no JSON body
        text = request.args.get('text')
        data = {'text': text} if text else {}
    
    # Get text from payload
    text = data.get('text', '')
    
    # Generate reproducible 64-dimensional vector from text
    vector = text_to_vector(text)
    
    return jsonify(vector)

if __name__ == '__main__':
    # Enable threading to handle concurrent requests from multiple students
    # threaded=True allows handling multiple requests simultaneously
    app.run(host='0.0.0.0', port=5000, threaded=True)

