from flask import Flask, request, jsonify
import os
import hashlib
import uuid
import logging
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1024MB

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Setup basic logging
logging.basicConfig(level=logging.INFO)

def hash_data(data):
    """Hash function using SHA-256."""
    return hashlib.sha256(data).hexdigest()

def create_merkle_tree(chunks):
    """Create a Merkle tree from the given chunks."""
    leaf_nodes = [hash_data(chunk) for chunk in chunks]
    tree = leaf_nodes.copy()

    while len(leaf_nodes) > 1:
        temp_nodes = []
        for i in range(0, len(leaf_nodes), 2):
            left = leaf_nodes[i]
            right = leaf_nodes[i + 1] if i + 1 < len(leaf_nodes) else left
            parent = hash_data((left + right).encode())
            temp_nodes.append(parent)
        leaf_nodes = temp_nodes
        tree.extend(leaf_nodes)

    return tree

@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint to upload a file, save it, and process it into a Merkle tree."""
    file = request.files.get('file')

    if not file:
        return jsonify({"error": "No file part"}), 400
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Secure the filename and generate a unique name to prevent overwrites and directory traversal
    filename = secure_filename(file.filename)
    unique_filename = str(uuid.uuid4()) + "_" + filename
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Save the file to the upload directory after checking its size
    file.seek(0, os.SEEK_END)  # Move pointer to end of file to get size
    file_size = file.tell()
    if file_size > MAX_FILE_SIZE:
        return jsonify({"error": "File size exceeds limit"}), 413  # Payload Too Large
    file.seek(0)  # Reset pointer to start of file

    file.save(filepath)
    logging.info(f"File saved as {unique_filename}")

    # Process the file in chunks to build the Merkle tree
    with open(filepath, 'rb') as saved_file:
        chunks = []
        chunk_size = 1024 * 1024  # 1MB chunk size
        while chunk := saved_file.read(chunk_size):
            chunks.append(chunk)

    merkle_tree = create_merkle_tree(chunks)
    root_hash = merkle_tree[-1]

    # Cleanup: Remove the saved file
    os.remove(filepath)
    logging.info(f"File {unique_filename} processed and removed")

    return jsonify({"message": "File processed in chunks", "merkle_root": root_hash}), 200

if __name__ == '__main__':
    app.run(debug=True)
