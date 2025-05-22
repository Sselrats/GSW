import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

interface CiphertextPanelProps {
  ciphertext: number[][];
}

const CiphertextPanel: React.FC<CiphertextPanelProps> = ({ ciphertext }) => {
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
        Ciphertext
      </Typography>
      <Box 
        sx={{ 
          flex: 1, 
          border: '1px solid',
          borderColor: 'divider',
          borderRadius: 1,
          p: 2,
          overflow: 'auto',
          bgcolor: 'background.paper',
          fontFamily: 'monospace',
          whiteSpace: 'pre',
        }}
      >
        {ciphertext.length > 0 ? (
          ciphertext.map((row, i) => (
            <div key={i}>
              {`[${row.map(num => String(num).padStart(4)).join(', ')}]`}
            </div>
          ))
        ) : (
          <Typography color="text.secondary" fontStyle="italic">
            No ciphertext generated
          </Typography>
        )}
      </Box>
    </Paper>
  );
};

export default CiphertextPanel;
