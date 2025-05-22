from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class GSWInitRequest(BaseModel):
    n: int = Field(..., gt=1, le=512, description="Dimension of the lattice")
    q: int = Field(..., gt=1, le=2**15, description="Modulus")

class GSWEncryptRequest(BaseModel):
    plaintext: int = Field(..., description="Plaintext matrix to encrypt")
    reset: bool = Field(False, description="Reset the GSW instance before operation")

class GSWDecryptRequest(BaseModel):
    ciphertext: List[List[int]] = Field(..., description="Ciphertext to decrypt")
    key: List[List[int]] = Field(..., description="Secret key for decryption")
    reset: bool = Field(False, description="Reset the GSW instance before operation")

class GSWOperateRequest(BaseModel):
    operation: str = Field(..., description="Operation to perform")
    ciphertext: List[List[int]] = Field(..., description="Ciphertext to operate on")
    inputCiphertext: List[List[int]] = Field(..., description="Input ciphertext to operate on")
    reset: bool = Field(False, description="Reset the GSW instance before operation")

class GSWCiphertextErrorRequest(BaseModel):
    ciphertext: List[List[int]] = Field(..., description="Ciphertext to check error for")
    reset: bool = Field(False, description="Reset the GSW instance before operation")

class GSWResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class GSWModelInfo(BaseModel):
    n: int
    q: int
    logq: int
    l: int
    s: List[int]

class GSWCiphertextErrorResponse(BaseModel):
    error: float
    max_valid_error: float
    is_valid: bool
    message: Optional[str] = None
