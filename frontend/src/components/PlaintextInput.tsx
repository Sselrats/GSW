import React from 'react';
import { Box, TextField, Typography, Paper, Button } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

interface PlaintextInputProps {
  value: string;
  onChange: (value: string) => void;
}

const PlaintextInput: React.FC<PlaintextInputProps> = ({ value, onChange }) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle plaintext submission here
    console.log('Plaintext submitted:', value);
  };

  return (
    <Paper 
      elevation={2} 
      sx={{ 
        p: 2, 
        flex: 1,
        minHeight: '300px',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      <Typography variant="h6" gutterBottom>
        Plaintext Input
      </Typography>
      <Box 
        component="form"
        onSubmit={handleSubmit}
        sx={{ 
          display: 'flex', 
          flexDirection: 'column',
          flex: 1,
          gap: 2
        }}
      >
        <TextField
          multiline
          rows={8}
          fullWidth
          variant="outlined"
          placeholder="Enter plaintext or matrix (e.g., [[1, 0], [0, 1]])"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          sx={{ flex: 1 }}
        />
        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            type="submit"
            variant="contained"
            endIcon={<SendIcon />}
            disabled={!value.trim()}
          >
            Encrypt
          </Button>
        </Box>
      </Box>
    </Paper>
  );
};

export default PlaintextInput;
