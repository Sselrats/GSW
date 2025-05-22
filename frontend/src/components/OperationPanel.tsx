import React from "react";
import {
  Paper,
  ToggleButton,
  ToggleButtonGroup,
  Typography,
  Tooltip,
  Button,
} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CloseIcon from "@mui/icons-material/Close";
import SendIcon from "@mui/icons-material/Send";

interface OperationPanelProps {
  operation: "Add" | "Mult";
  setOperation: (op: "Add" | "Mult") => void;
  onOperate: () => void;
}

const OperationPanel: React.FC<OperationPanelProps> = ({
  operation,
  setOperation,
  onOperate,
}) => {
  const handleOperationChange = (
    _event: React.MouseEvent<HTMLElement>,
    newOperation: "Add" | "Mult"
  ) => {
    setOperation(newOperation);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onOperate();
  };

  return (
    <Paper
      elevation={2}
      sx={{
        p: 4,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minWidth: "120px",
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
        sx={{ width: "100%" }}
      >
        <Tooltip title="Add">
          <ToggleButton value="Add" aria-label="Add" sx={{ p: 2 }}>
            <AddIcon />
          </ToggleButton>
        </Tooltip>
        <Tooltip title="Multiply">
          <ToggleButton value="Mult" aria-label="Mult" sx={{ p: 2 }}>
            <CloseIcon />
          </ToggleButton>
        </Tooltip>
      </ToggleButtonGroup>
      <Button
        variant="contained"
        color="primary"
        size="large"
        startIcon={<SendIcon />}
        onClick={handleSubmit}
        sx={{
          minWidth: "200px",
          py: 1.5,
          px: 4,
          fontSize: "1.1rem",
          fontWeight: 500,
          textTransform: "none",
          boxShadow: 2,
          "&:hover": {
            boxShadow: 4,
          },
        }}
      >
        Operate
      </Button>
    </Paper>
  );
};

export default OperationPanel;
