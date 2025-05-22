import React from 'react';
import { Paper, ToggleButton, ToggleButtonGroup, Typography, Tooltip } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import CloseIcon from '@mui/icons-material/Close';

interface OperationPanelProps {
  operation: 'add' | 'multiply';
  setOperation: (op: 'add' | 'multiply') => void;
}

const OperationPanel: React.FC<OperationPanelProps> = ({ operation, setOperation }) => {
  const handleOperationChange = (
    _event: React.MouseEvent<HTMLElement>,
    newOperation: 'add' | 'multiply' | null,
  ) => {
    if (newOperation !== null) {
      setOperation(newOperation);
    }
  };

  return (
    <Paper 
      elevation={2} 
      sx={{ 
        p: 4, 
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minWidth: '120px',
      }}
    >
      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
        Operation
      </Typography>
      <ToggleButtonGroup
        value={operation}
        exclusive
        onChange={handleOperationChange}
        aria-label="operation"
        orientation="vertical"
        sx={{ width: '100%' }}
      >
        <Tooltip title="Add">
          <ToggleButton value="add" aria-label="add" sx={{ p: 2 }}>
            <AddIcon />
          </ToggleButton>
        </Tooltip>
        <Tooltip title="Multiply">
          <ToggleButton value="multiply" aria-label="multiply" sx={{ p: 2 }}>
            <CloseIcon />
          </ToggleButton>
        </Tooltip>
      </ToggleButtonGroup>
    </Paper>
  );
};

export default OperationPanel;
