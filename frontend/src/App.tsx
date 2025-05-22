import { useState } from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme, Box, Typography } from '@mui/material';
import { blue, teal } from '@mui/material/colors';
import Header from './components/Header';
import CiphertextPanel from './components/CiphertextPanel';
import OperationPanel from './components/OperationPanel';
import PlaintextInput from './components/PlaintextInput';
import DecryptButton from './components/DecryptButton';
import './App.css';

const theme = createTheme({
  palette: {
    primary: {
      main: blue[700],
    },
    secondary: {
      main: teal[500],
    },
    background: {
      default: '#f8f9fa',
    },
  },
  typography: {
    h4: {
      fontWeight: 600,
      marginBottom: '1rem',
    },
  },
});

function App() {
  const [n, setN] = useState<number>(4);
  const [logq, setLogq] = useState<number>(8);
  const [operation, setOperation] = useState<'add' | 'multiply'>('add');
  const [ciphertext, setCiphertext] = useState<number[][]>([]);
  const [plaintext, setPlaintext] = useState<string>('');
  const [secretKey, setSecretKey] = useState<number[]>([]);
  const [showKey, setShowKey] = useState<boolean>(false);

  const handleGenerateModel = () => {
    // TODO: Implement model generation logic
    console.log('Generating model with n:', n, 'logq:', logq);
  };

  const handleDecrypt = () => {
    // TODO: Implement decryption logic
    console.log('Decrypting ciphertext:', ciphertext);
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
        
        <Box sx={{ 
          display: 'flex', 
          flexDirection: { xs: 'column', md: 'row' }, 
          gap: 4, 
          my: 4,
          alignItems: 'stretch'
        }}>
          <CiphertextPanel ciphertext={ciphertext} />
          <OperationPanel operation={operation} setOperation={setOperation} />
          <PlaintextInput value={plaintext} onChange={setPlaintext} />
        </Box>
        
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
          <DecryptButton onClick={handleDecrypt} />
        </Box>
      </Container>
    </ThemeProvider>
  )
}

export default App
