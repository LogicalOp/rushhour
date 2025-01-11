import * as React from 'react';
import { Link, BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import MicIcon from '@mui/icons-material/Mic';
import Home from '../pages/Home';
import Charts from '../pages/Charts';

// declaring the pages, with their labels and paths
const pages = [
  { label: 'Home', path: '/' },
  { label: 'Charts', path: '/charts' }
];

// common styles for reuse
const commonStyles = {
  link: {
    textDecoration: 'none',
    color: 'inherit'
  },
  typography: {
    fontFamily: 'monospace',
    fontWeight: 700,
    letterSpacing: '.3rem',
    color: 'inherit',
    textDecoration: 'none',
  },
  gradient: {
    background: 'linear-gradient(-225deg, #231557 0%, #44107A 29%, #FF1361 67%, #FFF800 100%)', // the background which changes colour
    backgroundSize: '200% 100%',
    animation: 'gradient 15s ease infinite', // animation to make the background change colour
    '@keyframes gradient': {
      '0%': { backgroundPosition: '0% 50%' },
      '50%': { backgroundPosition: '100% 50%' },
      '100%': { backgroundPosition: '0% 50%' }
    }
  }
};

// the navbar function
function NavBar() {
  // state for mobile menu
  const [anchorElNav, setAnchorElNav] = React.useState(null);

  // handling open and closing of the nav menu
  const handleOpenNavMenu = (event) => setAnchorElNav(event.currentTarget);
  const handleCloseNavMenu = () => setAnchorElNav(null);

  return (
    // wrapping the component in router to enable routing
    <Router>
      {/* appbar component to create the top navigation bar */}
      <AppBar position="static" sx={commonStyles.gradient}>
        <Container maxWidth="xl">
          <Toolbar disableGutters>
            {/* the mic logo seen in the navbar*/}
            <MicIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1 }} />
            
            {/* 'karaoke bar' text that links to the homepage */}
            <Typography
              variant="h6"
              noWrap
              component={Link}
              to="/"
              sx={{ ...commonStyles.typography, mr: 2, display: { xs: 'none', md: 'flex' } }}
            >
              Karaoke Bar
            </Typography>

            {/* mobile menu section */}
            <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
              <IconButton
                size="large"
                aria-label="mobile menu"
                onClick={handleOpenNavMenu}
                color="inherit"
              >
                <MenuIcon />
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorElNav}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
                transformOrigin={{ vertical: 'top', horizontal: 'left' }}
                open={Boolean(anchorElNav)}
                onClose={handleCloseNavMenu}
                sx={{ display: { xs: 'block', md: 'none' } }}
              >
                {/* mobile menu items */}
                {pages.map((page) => (
                  <MenuItem key={page.label} onClick={handleCloseNavMenu}>
                    <Typography textAlign="center">
                      <Link to={page.path} style={commonStyles.link}>
                        {page.label}
                      </Link>
                    </Typography>
                  </MenuItem>
                ))}
              </Menu>
            </Box>

            {/* mobile mic logo */}
            <MicIcon sx={{ display: { xs: 'flex', md: 'none' }, mr: 1 }} />
            {/* mobile 'karaoke bar' text */}
            <Typography
              variant="h5"
              noWrap
              component={Link}
              to="/"
              sx={{ ...commonStyles.typography, mr: 2, display: { xs: 'flex', md: 'none' }, flexGrow: 1 }}
            >
              Karaoke Bar
            </Typography>

            {/* desktop menu section */}
            <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
              {pages.map((page) => (
                <Button
                  key={page.label}
                  onClick={handleCloseNavMenu}
                  sx={{ my: 2, color: 'white', display: 'block' }}
                >
                  <Link to={page.path} style={commonStyles.link}>
                    {page.label}
                  </Link>
                </Button>
              ))}
            </Box>
          </Toolbar>
        </Container>
      </AppBar>

      {/* route definitions for page navigation */}      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/charts" element={<Charts />} />
      </Routes>
    </Router>
  );
}

export default NavBar;