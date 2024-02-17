# Flask File Merkle Tree Generator

This Flask application provides an API endpoint to upload files, process them in chunks, and generate a Merkle tree based on the content of the file. The root hash of the Merkle tree is returned as a response.

## Features

- File upload via a RESTful API endpoint.
- Processing of files in chunks to build a Merkle tree.
- Generation of a unique hash for the uploaded file using SHA-256.
- Ensures file security by using secure filenames and unique identifiers.
- Limits file size to prevent abuse (current limit set to 1024MB).

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your machine.
- Pip for installing Python packages.

### Installation

1. Clone the repository to your local machine:
```
git clone [<repository-url>](https://github.com/Arkay92/MerkleStreamUploader)
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```

### Running the Application
To run the application, execute the following command in the terminal:
```
flask run
or
python -m flask run
```

This will start the Flask development server, and the application will be accessible at `http://127.0.0.1:5000/`.

### Usage
To upload a file and generate its Merkle root hash, use the `/upload` endpoint. This can be done using a tool like `curl` or Postman.

Example using `curl`:
```
curl -X POST -F "file=@<path-to-your-file>" http://127.0.0.1:5000/upload
```

Replace `<path-to-your-file>` with the actual file path you want to upload.

## Contributing

Contributions to this project are welcome. Please adhere to this project's `Code of Conduct`.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or comments about the project, please feel free to get in touch.
