import { useState } from "react";
import {
  Container,
  CssBaseline,
  ThemeProvider,
  createTheme,
  Box,
  Typography,
  Snackbar,
  Alert,
} from "@mui/material";
import { blue, teal } from "@mui/material/colors";
import Header from "./components/Header";
import CiphertextPanel from "./components/CiphertextPanel";
import OperationPanel from "./components/OperationPanel";
import PlaintextPanel from "./components/PlaintextPanel";
import DecryptButton from "./components/DecryptButton";
import "./App.css";
import apiService from "./services/api";

const theme = createTheme({
  palette: {
    primary: {
      main: blue[700],
    },
    secondary: {
      main: teal[500],
    },
    background: {
      default: "#f8f9fa",
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
      marginBottom: "1rem",
    },
  },
});

function App() {
  const [n, setN] = useState<number>(4);
  const [logq, setLogq] = useState<number>(8);
  const [operation, setOperation] = useState<"Add" | "Mult">("Add");
  const [plaintext, setPlaintext] = useState<number>(0);
  const [ciphertext, setCiphertext] = useState<number[][]>([]);
  const [inputPlaintext, setInputPlaintext] = useState<string>("");
  const [inputCiphertext, setInputCiphertext] = useState<number[][]>([]);
  const [secretKey, setSecretKey] = useState<number[]>([]);
  const [showKey, setShowKey] = useState<boolean>(false);
  const [decryptResult, setDecryptResult] = useState<string>("");
  const [isModelInitialized, setIsModelInitialized] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [alert, setAlert] = useState<{
    show: boolean;
    message: string;
    severity: "success" | "error" | "info" | "warning";
  }>({ show: false, message: "", severity: "info" });

  const clear = () => {
    setPlaintext(0);
    setCiphertext([]);
    setInputPlaintext("");
    setInputCiphertext([]);
    setSecretKey([]);
    setDecryptResult("");
    setIsModelInitialized(false);
    setLoading(false);
  };

  const handleGenerateModel = async () => {
    try {
      clear();
      setLoading(true);
      const q = Math.pow(2, logq);
      const response = await apiService.initializeGSW({ n, q });

      if (response.success) {
        setIsModelInitialized(true);
        setSecretKey(response.data?.s || []);
        setAlert({
          show: true,
          message: "GSW model initialized successfully!",
          severity: "success",
        });
      } else {
        setAlert({
          show: true,
          message: response.message || "Failed to initialize GSW model",
          severity: "error",
        });
      }
    } catch (error) {
      console.error("Error initializing GSW model:", error);
      setAlert({
        show: true,
        message: "Error initializing GSW model",
        severity: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleInputEncrypt = async () => {
    if (!isModelInitialized) {
      setAlert({
        show: true,
        message: "Please initialize the model first",
        severity: "warning",
      });
      return;
    }

    try {
      setLoading(true);
      const ptxt = parseInt(inputPlaintext);

      if (ptxt !== 0 && ptxt !== 1) {
        setAlert({
          show: true,
          message: "Plaintext must be 0 or 1",
          severity: "error",
        });
        return;
      }

      const response = await apiService.encrypt({
        plaintext: ptxt,
        reset: false,
      });

      if (response.success && response.data) {
        if (ciphertext.length === 0) {
          setCiphertext(response.data.ciphertext);
          setPlaintext(ptxt);
        } else {
          setInputCiphertext(response.data.ciphertext);
        }
        setAlert({
          show: true,
          message: "Encryption successful!",
          severity: "success",
        });
      } else {
        setAlert({
          show: true,
          message: response.message || "Encryption failed",
          severity: "error",
        });
      }
    } catch (error) {
      console.error("Error encrypting plaintext:", error);
      setAlert({
        show: true,
        message: "Error encrypting plaintext",
        severity: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleOperate = async () => {
    if (!isModelInitialized) {
      setAlert({
        show: true,
        message: "Please initialize the model first",
        severity: "warning",
      });
      return;
    }

    try {
      setLoading(true);

      const response = await apiService.operate({
        operation,
        ciphertext,
        inputCiphertext,
        reset: false,
      });

      if (response.success && response.data) {
        if (operation == "Add") {
          setPlaintext((plaintext + parseInt(inputPlaintext)) % 2);
        } else {
          setPlaintext((plaintext * parseInt(inputPlaintext)) % 2);
        }
        setCiphertext(response.data.ciphertext);
        setInputCiphertext([]);
        setAlert({
          show: true,
          message: "Operation successful!",
          severity: "success",
        });
      } else {
        setAlert({
          show: true,
          message: response.message || "Encryption failed",
          severity: "error",
        });
      }
    } catch (error) {
      console.error("Error encrypting plaintext:", error);
      setAlert({
        show: true,
        message: "Error encrypting plaintext",
        severity: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDecrypt = async () => {
    if (!isModelInitialized || ciphertext.length === 0) {
      setAlert({
        show: true,
        message: "Please initialize the model and encrypt data first",
        severity: "warning",
      });
      return;
    }

    try {
      setLoading(true);
      const response = await apiService.decrypt({
        ciphertext: ciphertext,
        key: secretKey,
        reset: false,
      });

      if (response.success && response.data) {
        const decryptedText = JSON.stringify(response.data.plaintext);
        setDecryptResult(decryptedText);
        setAlert({
          show: true,
          message: "Decryption successful!",
          severity: "success",
        });
      } else {
        setAlert({
          show: true,
          message: response.message || "Decryption failed",
          severity: "error",
        });
      }
    } catch (error) {
      console.error("Error decrypting ciphertext:", error);
      setAlert({
        show: true,
        message: "Error decrypting ciphertext",
        severity: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          GSW Encryption Service
        </Typography>

        <Header
          n={n}
          setN={setN}
          logq={logq}
          setLogq={setLogq}
          onGenerate={handleGenerateModel}
          secretKey={secretKey}
          showKey={showKey}
          setShowKey={setShowKey}
        />

        <Box
          sx={{
            display: "flex",
            flexDirection: { xs: "column", md: "row" },
            gap: 4,
            my: 4,
            alignItems: "stretch",
          }}
        >
          <CiphertextPanel plaintext={plaintext} ciphertext={ciphertext} />
          <OperationPanel
            operation={operation}
            setOperation={setOperation}
            onOperate={handleOperate}
          />
          <PlaintextPanel
            inputPlaintext={inputPlaintext}
            onChange={setInputPlaintext}
            onEncrypt={handleInputEncrypt}
            inputCiphertext={inputCiphertext}
            loading={loading}
          />
        </Box>

        <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
          <DecryptButton onClick={handleDecrypt} loading={loading} />
          Decryption Result: {decryptResult}
        </Box>
        <Snackbar
          open={alert.show}
          autoHideDuration={6000}
          onClose={() => setAlert({ ...alert, show: false })}
          anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
        >
          <Alert
            onClose={() => setAlert({ ...alert, show: false })}
            severity={alert.severity}
            sx={{ width: "100%" }}
          >
            {alert.message}
          </Alert>
        </Snackbar>
      </Container>
    </ThemeProvider>
  );
}

export default App;
