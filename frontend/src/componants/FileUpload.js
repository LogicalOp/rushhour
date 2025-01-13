import * as React from 'react';
import { Grid, Paper, Box, Button, Typography, TextField } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { createTheme, ThemeProvider, styled } from '@mui/material/styles';
import waveform from '../utils/waveform.gif';

const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  color: theme.palette.text.secondary,
  lineHeight: '60px',
}));

const VisuallyHiddenInput = styled('input')({
  display: 'none',
});

const lightTheme = createTheme({ palette: { mode: 'light' } });

export default function FileUpload() {
  return (
    <Grid
      container
      spacing={2}
      sx={{
        height: '85vh',
        padding: '2rem',
      }}
    >
      {[lightTheme].map((theme, index) => (
        <Grid item xs={12} key={index} sx={{ height: '100%' }}>
          <ThemeProvider theme={theme}>
            <Box
              sx={{
                p: 2,
                borderRadius: 2,
                position: 'relative',
                height: '95%',
                overflow: 'hidden',
              }}
            >
              {/* Background Gradient Layer with Animation */}
              <Box
                sx={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  backgroundImage: `linear-gradient(-225deg, #231557 0%, #44107A 29%, #FF1361 67%, #FFF800 100%)`,
                  backgroundSize: '200% 100%',
                  animation: 'gradient 15s ease infinite',
                  '@keyframes gradient': {
                    '0%': {
                      backgroundPosition: '0% 50%'
                    },
                    '50%': {
                      backgroundPosition: '100% 50%'
                    },
                    '100%': {
                      backgroundPosition: '0% 50%'
                    }
                  }
                }}
              />
              {/* Waveform GIF Layer */}
              <Box
                sx={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  backgroundImage: `url(${waveform})`,
                  backgroundSize: '80% 80%',
                  backgroundPosition: 'center',
                  backgroundRepeat: 'no-repeat',
                  opacity: 0.4,
                }}
              />
              {/* Content Layer */}
              <Box
                sx={{
                  position: 'relative',
                  zIndex: 1,
                  height: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'flex-start',
                  paddingLeft: '4rem',
                }}
              >
                <Item
                  elevation={6}
                  sx={{
                    textAlign: 'center',
                    width: '25%',
                    height: '75%',
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    display: 'flex',
                    flexDirection: 'column',
                    padding: '2rem',
                    gap: '1.5rem',
                  }}
                >
                  <Typography variant="h6" component="div">
                    Enter Song Details
                  </Typography>
                  <TextField
                    fullWidth
                    label="Song Title"
                    variant="outlined"
                    size="small"
                  />

                  <TextField
                    fullWidth
                    label="Artist"
                    variant="outlined"
                    size="small"
                  />

                  <Box sx={{ flexGrow: 1 }} />

                  <Button
                    sx={{
                      bgcolor: 'orange',
                      '&:hover': {
                        bgcolor: '#e69500',
                      },
                    }}
                    component="label"
                    variant="contained"
                    startIcon={<CloudUploadIcon />}
                  >
                    Upload files
                    <VisuallyHiddenInput
                      type="file"
                      onChange={(event) => console.log(event.target.files)}
                      multiple
                    />
                  </Button>
                </Item>
              </Box>
            </Box>
          </ThemeProvider>
        </Grid>
      ))}
    </Grid>
  );
}