import * as React from 'react';
import { useState } from 'react';
import {
  Grid,
  Paper,
  Box,
  Button,
  Typography,
  TextField,
  Backdrop,
  Dialog,
  IconButton,
  CircularProgress
} from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import CloseIcon from '@mui/icons-material/Close';
import DownloadIcon from '@mui/icons-material/Download';
import { styled } from '@mui/material/styles';
import waveform from '../utils/waveform.gif';
import { useVideoFetch } from '../utils/useVideoFetch';

// styled component for paper styling
const Item = styled(Paper)(({ theme }) => ({
  ...theme.typography.body2,
  color: theme.palette.text.secondary,
  lineHeight: '60px',
}));

export default function FileUpload() {
  // variables for the input form
  const [songName, setSongName] = useState('');
  const [artistName, setArtistName] = useState('');

  // using the useVideoFetch hook in the utils folder
  const {
    videoLoading,
    uploadComplete,
    videoUrl,
    fetchVideoForSong,
    handleDownload,
    handleCloseModal
  } = useVideoFetch();

  // handler for form submission
  const submitRequest = async () => {
    await fetchVideoForSong(songName, artistName);
  };

  const onDownload = () => {
    handleDownload(songName, artistName);
  };

  return (
    <>
      {/*grid container for the upload form */}
      <Grid
        container
        spacing={2}
        sx={{
          height: '85vh',
          padding: '2rem',
        }}
      >
        <Grid item xs={12} sx={{ height: '100%' }}>
          {/* container for background effects */}
          <Box
            sx={{
              p: 2,
              borderRadius: 2,
              position: 'relative',
              height: '95%',
              overflow: 'hidden',
            }}
          >
            {/* animated gradient background */}
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
                    backgroundPosition: '0% 50%',
                  },
                  '50%': {
                    backgroundPosition: '100% 50%',
                  },
                  '100%': {
                    backgroundPosition: '0% 50%',
                  },
                },
              }}
            />
            {/* waveform gif */}
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
            {/* form container */}
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
              {/* input form */}
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
                <Typography variant="h6" component="div" color="secondary">
                  Enter Song Details
                </Typography>
                {/* song title textfield */}
                <TextField
                  fullWidth
                  label="Song Title"
                  variant="outlined"
                  size="small"
                  value={songName}
                  onChange={(e) => setSongName(e.target.value)}
                />
                {/* artist textfield */}
                <TextField
                  fullWidth
                  label="Artist"
                  variant="outlined"
                  size="small"
                  value={artistName}
                  onChange={(e) => setArtistName(e.target.value)}
                />
                <Box sx={{ flexGrow: 1 }} />
                {/* submit button */}
                <Button
                  sx={{
                    bgcolor: 'orange',
                    '&:hover': {
                      bgcolor: '#e69500',
                    },
                  }}
                  variant="contained"
                  onClick={submitRequest}
                >
                  Submit
                </Button>
              </Item>
            </Box>
          </Box>
        </Grid>
      </Grid>

      {/* loading state */}
      <Backdrop
        sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={videoLoading}
      >
        <CircularProgress color="inherit" />
      </Backdrop>

      {/* success dialog */}
      <Dialog
        open={uploadComplete}
        onClose={handleCloseModal}
        aria-labelledby="upload-complete-title"
      >
        <Box sx={{ textAlign: 'center', padding: 3 }}>
          {/* close button */}
          <IconButton
            aria-label="close"
            onClick={handleCloseModal}
            sx={{ position: 'absolute', top: 8, right: 8 }}
          >
            <CloseIcon />
          </IconButton>
          <CheckCircleOutlineIcon color="success" sx={{ fontSize: 50 }} />
          <Typography variant="h6">Karaoke Track Ready</Typography>
          <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
            Your track is ready for download.
          </Typography>
          {/* download button */}
          <Button
            onClick={onDownload}
            variant="contained"
            startIcon={<DownloadIcon />}
          >
            Download
          </Button>
          {/* video preview */}
          {videoUrl && (
            <Box
              sx={{
                mt: 2,
                width: '100%',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center'
              }}
            >
              <video
                controls
                style={{
                  maxWidth: '300px',
                  maxHeight: '250px',
                  objectFit: 'contain'
                }}
              >
                <source src={videoUrl} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </Box>
          )}
        </Box>
      </Dialog>
    </>
  );
}