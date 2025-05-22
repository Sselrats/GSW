import numpy as np
from typing import Tuple, Optional, List, Dict, Any
import sys
import os
import time
import uuid
from fastapi import Request

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import the GSW implementation directly from the gsw.py file
# This assumes that gsw.py defines GSW and GSW_Ciphertext classes
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from gsw import GSW, GSW_Ciphertext

class GSWService:
    def __init__(self):
        # Dictionary to store user sessions: {session_id: {'gsw': GSW instance, 'last_activity': timestamp}}
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        self.session_timeout = 3600  # 1 hour timeout for sessions
    
    def _get_or_create_session(self, request: Request) -> str:
        """Get or create a session ID for the user."""
        session = request.session
        session_id = session.get('session_id')
        
        if not session_id or session_id not in self.user_sessions:
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            self.user_sessions[session_id] = {
                'gsw': None,
                'last_activity': time.time()
            }
        elif session_id in self.user_sessions:
            # Update last activity for existing session
            self.user_sessions[session_id]['last_activity'] = time.time()
            
        return session_id

    def _get_user_session(self, request: Request) -> Dict[str, Any]:
        """Get the user's session data."""
        session_id = self._get_or_create_session(request)
        return self.user_sessions[session_id]

    def _cleanup_sessions(self):
        """Clean up expired sessions."""
        current_time = time.time()
        expired = [sid for sid, data in self.user_sessions.items() 
                  if (current_time - data['last_activity']) > self.session_timeout]
        for sid in expired:
            del self.user_sessions[sid]
    
    def initialize(self, n: int, q: int, request: Request) -> Dict[str, Any]:
        """Initialize the GSW cryptosystem with parameters n and q."""
        try:
            session = self._get_user_session(request)
            session['gsw'] = GSW(n, q)
            session['last_activity'] = time.time()
            return {
                'n': n,
                'q': q,
                'logq': session['gsw'].logq,
                'l': session['gsw'].l,
                's': session['gsw'].s.tolist(),  # Include the secret key in the response
                'message': 'GSW cryptosystem initialized successfully'
            }
        except Exception as e:
            raise ValueError(f"Initialization failed: {str(e)}")
    
    def encrypt(self, plaintext: int, request: Request, reset: bool = False) -> Dict[str, Any]:
        """Encrypt a plaintext matrix."""
        session = self._get_user_session(request)
        if session['gsw'] is None:
            raise ValueError("GSW cryptosystem not initialized. Call /init first.")
        
        if reset:
            session['gsw'] = GSW(session['gsw'].n, session['gsw'].q)
        
        try:
            # Encrypt the plaintext integer
            ciphertext = session['gsw'].Enc(plaintext)
            session['last_activity'] = time.time()
        
            return {
                'ciphertext': ciphertext.C.tolist(),
                'message': 'Encryption successful'
            }
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")
    
    def decrypt(self, ciphertext: List[List[int]], key: List[List[int]], request: Request, reset: bool = False) -> Dict[str, Any]:
        """Decrypt a ciphertext using the provided key."""
        session = self._get_user_session(request)
        if session['gsw'] is None:
            raise ValueError("GSW cryptosystem not initialized. Call /init first.")
        
        if reset:
            session['gsw'] = GSW(session['gsw'].n, session['gsw'].q)
        
        try:
            # Convert ciphertext to numpy array
            ctxt = np.array(ciphertext, dtype=np.int32)
            
            # Create a GSW_Ciphertext object
            gsw_ctxt = GSW_Ciphertext(session['gsw'], ctxt)
            
            # Convert key to numpy array
            s = np.array(key, dtype=np.int32)
            
            # Decrypt the ciphertext
            decrypted = gsw_ctxt.Dec_with_key(s)
            
            return {
                'plaintext': decrypted.tolist(),
                'message': 'Decryption successful'
            }
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def operate(self, operation: str, ciphertext: List[List[int]], inputCiphertext: List[List[int]], request: Request, reset: bool = False) -> Dict[str, Any]:
        """Operate on a ciphertext."""
        session = self._get_user_session(request)
        if session['gsw'] is None:
            raise ValueError("GSW cryptosystem not initialized. Call /init first.")
        
        if reset:
            session['gsw'] = GSW(session['gsw'].n, session['gsw'].q)
        
        try:
            # Convert ciphertext to numpy array
            ctxt = np.array(ciphertext, dtype=np.int32)
            
            # Create a GSW_Ciphertext object
            gsw_ctxt = GSW_Ciphertext(session['gsw'], ctxt)
            
            # Convert input ciphertext to numpy array
            input_ctxt = np.array(inputCiphertext, dtype=np.int32)
            gsw_input_ctxt = GSW_Ciphertext(session['gsw'], input_ctxt)

            # Operate on the ciphertext
            if operation == "Add":
                operated = gsw_ctxt.Add(gsw_input_ctxt)
            elif operation == "Mult":
                operated = gsw_ctxt.Mult(gsw_input_ctxt)
            
            session['last_activity'] = time.time()
            
            return {
                'ciphertext': operated.C.tolist(),
                'message': 'Operation successful'
            }
        except Exception as e:
            raise ValueError(f"Operation failed: {str(e)}")

    def get_ciphertext_error(self, ciphertext: List[List[int]], request: Request, reset: bool = False) -> Dict[str, Any]:
        """Get the error of a ciphertext."""
        session = self._get_user_session(request)
        if session['gsw'] is None:
            raise ValueError("GSW cryptosystem not initialized. Call /init first.")
        
        if reset:
            session['gsw'] = GSW(session['gsw'].n, session['gsw'].q)
        
        try:
            # Convert ciphertext to numpy array
            ctxt = np.array(ciphertext, dtype=np.int32)
            
            # Create a GSW_Ciphertext object
            gsw_ctxt = GSW_Ciphertext(session['gsw'], ctxt)
            
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
    
    def get_model_info(self, request: Request) -> Optional[Dict[str, Any]]:
        """Get information about the current GSW model."""
        session = self._get_user_session(request)
        if session['gsw'] is None:
            return None
            
        return {
            'n': session['gsw'].n,
            'q': session['gsw'].q,
            'logq': session['gsw'].logq,
            'l': session['gsw'].l
        }
    
    def reset(self, request: Request) -> None:
        """Reset the GSW instance for a specific user."""
        session = self._get_user_session(request)
        if session['gsw'] is not None:
            session['gsw'] = GSW(session['gsw'].n, session['gsw'].q)
            session['last_activity'] = time.time()
    
    def is_initialized(self, request: Request) -> bool:
        """Check if the GSW cryptosystem is initialized."""
        session = self._get_user_session(request)
        return session['gsw'] is not None

# Note: Create instances of GSWService in the respective modules that need it
# This avoids circular import issues
