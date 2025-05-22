import React from "react";
import {
  Box,
  TextField,
  Typography,
  Paper,
  Button,
  CircularProgress,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";

interface PlaintextPanelProps {
  inputPlaintext: string;
  onChange: (value: string) => void;
  onEncrypt: () => void;
  inputCiphertext: number[][];
  loading: boolean;
}

const PlaintextPanel: React.FC<PlaintextPanelProps> = ({
  inputPlaintext,
  onChange,
  onEncrypt,
  inputCiphertext,
  loading,
}) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onEncrypt();
  };

  return (
    <Paper
      elevation={2}
      sx={{
        p: 2,
        flex: 1,
        minHeight: "300px",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Typography variant="h6" gutterBottom>
        Plaintext Input
      </Typography>
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{
          display: "flex",
          flexDirection: "column",
          flex: 1,
          gap: 2,
        }}
      >
        <TextField
          multiline
          rows={1}
          fullWidth
          variant="outlined"
          placeholder="Enter plaintext (0 or 1)"
          value={inputPlaintext}
          onChange={(e) => onChange(e.target.value)}
          sx={{ flex: 1 }}
        />
        <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
          <Button
            type="submit"
            variant="contained"
            endIcon={
              loading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                <SendIcon />
              )
            }
            disabled={!inputPlaintext.trim() || loading}
          >
            {loading ? "Encrypting..." : "Encrypt"}
          </Button>
        </Box>
        <Box
          sx={{
            flex: 1,
            border: "1px solid",
            borderColor: "divider",
            borderRadius: 1,
            p: 2,
            overflow: "auto",
            bgcolor: "background.paper",
            fontFamily: "monospace",
            whiteSpace: "pre",
          }}
        >
          {inputCiphertext.length > 0 ? (
            inputCiphertext.map((row, i) => (
              <div key={i}>
                {`[${row.map((num) => String(num).padStart(4)).join(", ")}]`}
              </div>
            ))
          ) : (
            <Typography color="text.secondary" fontStyle="italic">
              No ciphertext generated
            </Typography>
          )}
        </Box>
      </Box>
    </Paper>
  );
};

export default PlaintextPanel;
