import React from 'react';
import { Button, CircularProgress } from '@mui/material';
import LockOpenIcon from '@mui/icons-material/LockOpen';

interface DecryptButtonProps {
  onClick: () => void;
  loading?: boolean;
}

const DecryptButton: React.FC<DecryptButtonProps> = ({ 
  onClick, 
  loading = false 
}) => {
  return (
    <Button
      variant="contained"
      color="secondary"
      size="large"
      startIcon={!loading && <LockOpenIcon />}
      onClick={onClick}
      disabled={loading}
      sx={{
        minWidth: '200px',
        py: 1.5,
        px: 4,
        fontSize: '1.1rem',
        fontWeight: 500,
        textTransform: 'none',
        boxShadow: 2,
        '&:hover': {
          boxShadow: 4,
        },
      }}
    >
      {loading ? <CircularProgress size={24} color="inherit" /> : 'Decrypt'}
    </Button>
  );
};

export default DecryptButton;
