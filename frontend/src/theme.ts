
import { createTheme } from '@mui/material/styles';
import { red } from '@mui/material/colors';

// Un tema personalizado para nuestra aplicación de salud
const theme = createTheme({
  palette: {
    primary: {
      main: '#005A9C', // Un azul profesional y sereno
    },
    secondary: {
      main: '#4CAF50', // Un verde para acciones de éxito o confirmación
    },
    error: {
      main: red.A400,
    },
    background: {
      default: '#f4f6f8', // Un gris muy claro para el fondo de la aplicación
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
});

export default theme;
