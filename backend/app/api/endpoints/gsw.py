from fastapi import APIRouter, HTTPException, status, Depends
from typing import Any, Dict, List, Optional
import numpy as np

from app.schemas.gsw import (
    GSWInitRequest, GSWEncryptRequest, GSWDecryptRequest, 
    GSWCiphertextErrorRequest, GSWResponse, GSWModelInfo, GSWCiphertextErrorResponse
)
from app.services.gsw_service import GSWService

router = APIRouter()
gsw_service = GSWService()

@router.post("/init", response_model=GSWResponse, status_code=status.HTTP_201_CREATED)
async def initialize_gsw(params: GSWInitRequest) -> Dict[str, Any]:
    """
    Initialize the GSW cryptosystem with parameters n and q.
    
    - **n**: Dimension of the lattice (1-10)
    - **q**: Modulus (must be > 1)
    """
    try:
        result = gsw_service.initialize(n=params.n, q=params.q)
        return {
            "success": True,
            "message": result["message"],
            "data": {
                "n": result["n"],
                "q": result["q"],
                "logq": result["logq"],
                "l": result["l"]
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "message": f"An error occurred: {str(e)}"}
        )

@router.post("/encrypt", response_model=GSWResponse)
async def encrypt_plaintext(request: GSWEncryptRequest) -> Dict[str, Any]:
    """
    Encrypt a plaintext matrix using the GSW cryptosystem.
    
    - **plaintext**: 2D array of integers to encrypt
    - **reset**: If True, resets the GSW instance before encryption
    """
    try:
        result = gsw_service.encrypt(
            plaintext=request.plaintext,
            reset=request.reset
        )
        return {
            "success": True,
            "message": result["message"],
            "data": {
                "ciphertext": result["ciphertext"]
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "message": f"An error occurred: {str(e)}"}
        )

@router.post("/decrypt", response_model=GSWResponse)
async def decrypt_ciphertext(request: GSWDecryptRequest) -> Dict[str, Any]:
    """
    Decrypt a ciphertext using the provided key.
    
    - **ciphertext**: 2D array of integers to decrypt
    - **key**: Secret key for decryption
    - **reset**: If True, resets the GSW instance before decryption
    """
    try:
        result = gsw_service.decrypt(
            ciphertext=request.ciphertext,
            key=request.key,
            reset=request.reset
        )
        return {
            "success": True,
            "message": result["message"],
            "data": {
                "plaintext": result["plaintext"]
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "message": f"An error occurred: {str(e)}"}
        )

@router.post("/ciphertext_error", response_model=GSWResponse)
async def get_ciphertext_error(request: GSWCiphertextErrorRequest) -> Dict[str, Any]:
    """
    Get the error of a ciphertext.
    
    - **ciphertext**: 2D array of integers to check error for
    - **reset**: If True, resets the GSW instance before checking
    """
    try:
        result = gsw_service.get_ciphertext_error(
            ciphertext=request.ciphertext,
            reset=request.reset
        )
        return {
            "success": True,
            "message": result["message"],
            "data": {
                "error": result["error"],
                "max_valid_error": result["max_valid_error"],
                "is_valid": result["is_valid"]
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"success": False, "message": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"success": False, "message": f"An error occurred: {str(e)}"}
        )

@router.get("/model_info", response_model=GSWResponse)
async def get_model_info() -> Dict[str, Any]:
    """Get information about the current GSW model."""
    model_info = gsw_service.get_model_info()
    if model_info is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "GSW cryptosystem not initialized. Call /init first."}
        )
    
    return {
        "success": True,
        "message": "Model information retrieved successfully",
        "data": model_info
    }
