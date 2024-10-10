import { useState } from 'react'
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline'
import Header from './components/Header';
import Home from './pages/Home';
import './App.css'

const dark = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ed4b82',
    },
    secondary: {
      main: '#18181c',
    },
  },
});

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <ThemeProvider theme={dark}>
        <CssBaseline />
        <Header />
        <Router>
          <Routes>
              <Route path='/' element={<Home />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </>
  )
}

export default App
