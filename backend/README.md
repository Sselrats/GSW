# GSW Encryption Service Backend

This is the FastAPI backend for the GSW Encryption Service. It provides a RESTful API for performing GSW encryption operations.

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables (optional):
   Create a `.env` file in the `backend` directory with the following variables:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   ```

## Running the Server

To start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- OpenAPI Schema: http://localhost:8000/api/openapi.json

## API Endpoints

### Initialize GSW

```
POST /api/v1/gsw/init
```

Initialize the GSW cryptosystem with parameters n and q.

**Request Body:**
```json
{
  "n": 4,
  "q": 256
}
```

### Encrypt

```
POST /api/v1/gsw/encrypt
```

Encrypt a plaintext matrix.

**Request Body:**
```json
{
  "plaintext": [[0, 1], [1, 0]],
  "reset": false
}
```

### Decrypt

```
POST /api/v1/gsw/decrypt
```

Decrypt a ciphertext using the provided key.

**Request Body:**
```json
{
  "ciphertext": [[...], [...]],
  "key": [0, 1, 1, 0],
  "reset": false
}
```

### Get Ciphertext Error

```
POST /api/v1/gsw/ciphertext_error
```

Get the error of a ciphertext.

**Request Body:**
```json
{
  "ciphertext": [[...], [...]],
  "reset": false
}
```

### Get Model Info

```
GET /api/v1/gsw/model_info
```

Get information about the current GSW model.

## Testing

To run the tests:

```bash
pytest
```

## License

This project is licensed under the MIT License.
