import numpy as np
from typing import Tuple, Optional, List, Dict, Any
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the GSW implementation directly from the gsw.py file
# This assumes that gsw.py defines GSW and GSW_Ciphertext classes
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from gsw import GSW, GSW_Ciphertext

class GSWService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GSWService, cls).__new__(cls)
            cls._gsw = None
            cls._initialized = False
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._gsw = None
            self._initialized = True
    
    def initialize(self, n: int, q: int) -> Dict[str, Any]:
        """Initialize the GSW cryptosystem with parameters n and q."""
        try:
            self._gsw = GSW(n=n, q=q)
            return {
                'n': n,
                'q': q,
                'logq': self._gsw.logq,
                'l': self._gsw.l,
                'message': 'GSW cryptosystem initialized successfully'
            }
        except Exception as e:
            raise ValueError(f"Failed to initialize GSW: {str(e)}")
    
    def encrypt(self, plaintext: List[List[int]], reset: bool = False) -> Dict[str, Any]:
        """Encrypt a plaintext matrix."""
        if self._gsw is None:
            raise ValueError("GSW cryptosystem not initialized. Call /init first.")
        
        if reset:
            self.reset()
        
        try:
            # Convert plaintext to numpy array
            ptxt = np.array(plaintext, dtype=np.int32)
            
            # Encrypt the plaintext
            ciphertext = self._gsw.Enc(ptxt)
            
            # Convert ciphertext to list for JSON serialization
            ciphertext_list = ciphertext.C.tolist()
            
            return {
                'ciphertext': ciphertext_list,
                'message': 'Encryption successful'
            }
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")
    
    def decrypt(self, ciphertext: List[List[int]], key: List[int], reset: bool = False) -> Dict[str, Any]:
        """Decrypt a ciphertext using the provided key."""
        if self._gsw is None:
            raise ValueError("GSW cryptosystem not initialized. Call /init first.")
        
        if reset:
            self.reset()
        
        try:
            # Convert ciphertext to numpy array
            ctxt = np.array(ciphertext, dtype=np.int32)
            
            # Create a GSW_Ciphertext object
            gsw_ctxt = GSW_Ciphertext(self._gsw, ctxt)
            
            # Convert key to numpy array
            s = np.array(key, dtype=np.int32).reshape(-1, 1)
            
            # Decrypt the ciphertext
            decrypted = gsw_ctxt.Dec_with_key(s)
            
            return {
                'plaintext': decrypted.tolist(),
                'message': 'Decryption successful'
            }
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def get_ciphertext_error(self, ciphertext: List[List[int]], reset: bool = False) -> Dict[str, Any]:
        """Get the error of a ciphertext."""
        if self._gsw is None:
            raise ValueError("GSW cryptosystem not initialized. Call /init first.")
        
        if reset:
            self.reset()
        
        try:
            # Convert ciphertext to numpy array
            ctxt = np.array(ciphertext, dtype=np.int32)
            
            # Create a GSW_Ciphertext object
            gsw_ctxt = GSW_Ciphertext(self._gsw, ctxt)
            
            # Get the error
            error = gsw_ctxt.get_error(0)  # Using 0 as a placeholder plaintext
            max_error = gsw_ctxt.max_valid_error()
            is_valid = gsw_ctxt.is_error_valid(0)  # Using 0 as a placeholder plaintext
            
            return {
                'error': float(error),
                'max_valid_error': float(max_error),
                'is_valid': bool(is_valid),
                'message': 'Error calculation successful'
            }
        except Exception as e:
            raise ValueError(f"Error calculation failed: {str(e)}")
    
    def get_model_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the current GSW model."""
        if self._gsw is None:
            return None
            
        return {
            'n': self._gsw.n,
            'q': self._gsw.q,
            'logq': self._gsw.logq,
            'l': self._gsw.l
        }
    
    def reset(self) -> None:
        """Reset the GSW cryptosystem."""
        if self._gsw is not None:
            n = self._gsw.n
            q = self._gsw.q
            self._gsw = GSW(n=n, q=q)
    
    def is_initialized(self) -> bool:
        """Check if the GSW cryptosystem is initialized."""
        return self._gsw is not None
