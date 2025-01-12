import * as React from 'react';
import { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  Backdrop,
  Dialog,
  Button,
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

export default function ChartsList() {
  // declaring variables 
  const [chartData, setChartData] = useState({});
  const [sortedCharts, setSortedCharts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedSong, setSelectedSong] = useState(null);

  // using the useVideoFetch hook from utils folder
  const {
    videoLoading,
    uploadComplete,
    videoUrl,
    fetchVideoForSong,
    handleDownload,
    handleCloseModal
  } = useVideoFetch();

  //hook for fetching chart data
  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const response = await fetch('https://2a0a-188-141-96-109.ngrok-free.app/chart', {
          headers: {
            'ngrok-skip-browser-warning': 'true'
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const text = await response.text();
        let data;
        try {
          data = JSON.parse(text);
        } catch (parseError) {
          console.error('Parsing error:', text);
          throw new Error('Failed to parse JSON: ' + text);
        }

        // sort and limit chart data to top 50 songs
        const sorted = Object.entries(data)
          .sort(([, a], [, b]) => b - a)
          .slice(0, 50)
          .map(([song, downloads]) => ({ song, downloads }));

        setChartData(data);
        setSortedCharts(sorted);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching chart data:', error);
        setError(error.message);
        setIsLoading(false);
      }
    };

    fetchChartData();
  }, []);

  // handler for generating video for selected song
  const generateVideo = async (song) => {
    const [songName, artistName] = song.split(' - ');
    setSelectedSong(song);
    await fetchVideoForSong(songName, artistName);
  };

  // handler for downloading the generated video
  const onDownload = () => {
    const [songName, artistName] = selectedSong.split(' - ');
    handleDownload(songName, artistName);
  };

  return (
    <>
      {/* grid container for the charts list */}
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
            {/* charts list container */}
            <Box
              sx={{
                position: 'relative',
                zIndex: 1,
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: '100%'
              }}
            >
              {/* charts list paper component */}
              <Item
                elevation={6}
                sx={{
                  width: '80%',
                  height: '85%',
                  backgroundColor: 'rgba(255, 255, 255, 0.9)',
                  overflowY: 'auto',
                  padding: '1.5rem',
                }}
              >
                <Typography variant="h4" color="secondary" sx={{ textAlign: 'center', mb: 3 }}>
                  Most Downloaded Songs
                </Typography>
                {/* conditional rendering */}
                {isLoading ? (
                  <Typography variant="body2" sx={{ textAlign: 'center' }}>
                    Loading charts...
                  </Typography>
                ) : error ? (
                  <Typography variant="body2" color="error" sx={{ textAlign: 'center' }}>
                    Error loading charts: {error}
                  </Typography>
                ) : (
                  <List>
                    {/* charts list where clicking generates a video*/}
                    {sortedCharts.map((item, index) => (
                      <ListItem
                        key={item.song}
                        divider
                        button
                        onClick={() => generateVideo(item.song)}
                        sx={{
                          cursor: 'pointer',
                          '&:hover': {
                            backgroundColor: 'rgba(0,0,0,0.1)'
                          }
                        }}
                      >
                        {/*song info text*/}
                        <ListItemText
                          primary={`${index + 1}. ${item.song}`}
                          secondary={`Downloads: ${item.downloads}`}
                        />
                      </ListItem>
                    ))}
                  </List>
                )}
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
        onClose={() => {
          handleCloseModal();
          setSelectedSong(null);
        }}
        aria-labelledby="upload-complete-title"
      >
        <Box sx={{ textAlign: 'center', padding: 3 }}>
          {/* close button */}
          <IconButton
            aria-label="close"
            onClick={() => {
              handleCloseModal();
              setSelectedSong(null);
            }}
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