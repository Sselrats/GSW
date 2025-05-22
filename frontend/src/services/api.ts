import axios, { type AxiosResponse } from "axios";

// Load API URL from environment variables (defined in .env file)
// In React, environment variables are accessed via process.env and need to be prefixed with REACT_APP_
const API_BASE_URL = (import.meta.env?.REACT_APP_API_BASE_URL as string) || "http://localhost:8000/api/v1/gsw";

// Configure axios to send cookies with requests (important for session management)
axios.defaults.withCredentials = true;

// Define types for API requests and responses
export interface GSWInitParams {
  n: number;
  q: number;
}

export interface GSWEncryptParams {
  plaintext: number;
  reset?: boolean;
}

export interface GSWDecryptParams {
  ciphertext: number[][];
  key: number[];
  reset?: boolean;
}

export interface GSWOperateParams {
  operation: "Add" | "Mult";
  ciphertext: number[][];
  inputCiphertext: number[][];
  reset?: boolean;
}

export interface GSWCiphertextErrorParams {
  ciphertext: number[][];
  reset?: boolean;
}

export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
}

export interface GSWModelInfo {
  n: number;
  q: number;
  logq: number;
  l: number;
  s: number[];
}

export interface GSWCiphertextError {
  error: number;
  max_valid_error: number;
  is_valid: boolean;
}

// API service class
class ApiService {
  // Initialize GSW with parameters n and q
  async initializeGSW(
    params: GSWInitParams
  ): Promise<ApiResponse<GSWModelInfo>> {
    try {
      const response: AxiosResponse<ApiResponse<GSWModelInfo>> =
        await axios.post(`${API_BASE_URL}/init`, params);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        return error.response.data;
      }
      return {
        success: false,
        message: error.message || "Failed to initialize GSW",
      };
    }
  }

  // Encrypt plaintext using GSW
  async encrypt(
    params: GSWEncryptParams
  ): Promise<ApiResponse<{ ciphertext: number[][] }>> {
    try {
      const response: AxiosResponse<ApiResponse<{ ciphertext: number[][] }>> =
        await axios.post(`${API_BASE_URL}/encrypt`, params);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        return error.response.data;
      }
      return {
        success: false,
        message: error.message || "Failed to encrypt plaintext",
      };
    }
  }

  // Decrypt ciphertext using GSW
  async decrypt(
    params: GSWDecryptParams
  ): Promise<ApiResponse<{ plaintext: number[][] }>> {
    try {
      const response: AxiosResponse<ApiResponse<{ plaintext: number[][] }>> =
        await axios.post(`${API_BASE_URL}/decrypt`, params);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        return error.response.data;
      }
      return {
        success: false,
        message: error.message || "Failed to decrypt ciphertext",
      };
    }
  }

  async operate(
    params: GSWOperateParams
  ): Promise<ApiResponse<{ ciphertext: number[][] }>> {
    try {
      const response: AxiosResponse<ApiResponse<{ ciphertext: number[][] }>> =
        await axios.post(`${API_BASE_URL}/operate`, params);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        return error.response.data;
      }
      return {
        success: false,
        message: error.message || "Failed to operate on ciphertext",
      };
    }
  }

  // Get ciphertext error
  async getCiphertextError(
    params: GSWCiphertextErrorParams
  ): Promise<ApiResponse<GSWCiphertextError>> {
    try {
      const response: AxiosResponse<ApiResponse<GSWCiphertextError>> =
        await axios.post(`${API_BASE_URL}/ciphertext_error`, params);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        return error.response.data;
      }
      return {
        success: false,
        message: error.message || "Failed to get ciphertext error",
      };
    }
  }

  // Get model info
  async getModelInfo(): Promise<ApiResponse<GSWModelInfo>> {
    try {
      const response: AxiosResponse<ApiResponse<GSWModelInfo>> =
        await axios.get(`${API_BASE_URL}/model_info`);
      return response.data;
    } catch (error: any) {
      if (error.response) {
        return error.response.data;
      }
      return {
        success: false,
        message: error.message || "Failed to get model info",
      };
    }
  }
}

export default new ApiService();
