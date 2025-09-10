
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box, Typography } from '@mui/material';

import Layout from './components/Layout';
import PacientesPage from './pages/PacientesPage';
import AtencionesPage from './pages/AtencionesPage';

// Placeholder para la página de inicio, ahora vivirá dentro del Layout
function HomePage() {
  return (
    <Box>
      <Typography variant="h4">Bienvenido al Sistema de Gestión RIAS</Typography>
      <Typography>Seleccione una opción del menú lateral para comenzar.</Typography>
    </Box>
  );
}

function App() {
  return (
    <Routes>
      {/* Todas las rutas principales se anidan dentro de la ruta del Layout */}
      {/* Esto asegura que la barra de navegación y la barra superior sean persistentes */}
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="pacientes" element={<PacientesPage />} />
        <Route path="atenciones" element={<AtencionesPage />} />
      </Route>
      
      {/* Aquí se podrían añadir rutas que no usen el Layout, como una página de Login */}
      {/* <Route path="/login" element={<LoginPage />} /> */}
    </Routes>
  );
}

export default App;
