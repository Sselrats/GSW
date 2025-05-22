import React from "react";
import { Box, TextField, Button, Typography, Tooltip } from "@mui/material";
import KeyIcon from "@mui/icons-material/Key";

interface HeaderProps {
  n: number;
  setN: (value: number) => void;
  logq: number;
  setLogq: (value: number) => void;
  onGenerate: () => void;
  secretKey: number[];
  showKey: boolean;
  setShowKey: (show: boolean) => void;
}

const Header: React.FC<HeaderProps> = ({
  n,
  setN,
  logq,
  setLogq,
  onGenerate,
  secretKey,
  showKey,
  setShowKey,
}) => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: { xs: "column", sm: "row" },
        gap: 2,
        alignItems: "center",
        mb: 4,
        p: 2,
        bgcolor: "background.paper",
        borderRadius: 1,
        boxShadow: 1,
      }}
    >
      <Tooltip title="Dimension of the lattice">
        <TextField
          label="n"
          type="number"
          value={n}
          onChange={(e) => setN(Number(e.target.value))}
          size="small"
          sx={{ width: "100px" }}
          inputProps={{ min: 1, max: 10 }}
        />
      </Tooltip>

      <Tooltip title="Logarithm of the modulus q">
        <TextField
          label="logq"
          type="number"
          value={logq}
          onChange={(e) => setLogq(Number(e.target.value))}
          size="small"
          sx={{ width: "100px" }}
          inputProps={{ min: 1, max: 32 }}
        />
      </Tooltip>

      <Button
        variant="contained"
        onClick={onGenerate}
        sx={{ minWidth: "160px" }}
      >
        Generate Model
      </Button>

      <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
        <Button
          variant="outlined"
          startIcon={<KeyIcon />}
          onClick={() => setShowKey(!showKey)}
          sx={{ minWidth: "160px" }}
        >
          {showKey ? "Hide Secret Key" : "Show Secret Key"}
        </Button>
        {showKey && (
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <Typography variant="body2" sx={{ fontFamily: "monospace" }}>
              {secretKey.length > 0
                ? `[${secretKey.join(", ")}]`
                : "No key generated"}
            </Typography>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default Header;
