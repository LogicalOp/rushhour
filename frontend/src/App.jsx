import { createTheme, ThemeProvider } from '@mui/material/styles';
import NavBar from './components/NavBar';
const style = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#863fb5',
      light: '#faf2ff',
      dark: '#4a335a',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      paper: '#b32dac',
    },
    text: {
      primary: 'rgba(243,239,239,0.87)',
      secondary: 'rgba(249,244,244,0.6)',
      hint: '#ffffff',
    },
  },
});


function App() {
  return (
    <ThemeProvider theme={style}>
          <NavBar />  
    </ThemeProvider>
   
  );
}

export default App;
