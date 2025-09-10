import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Box, Button, CircularProgress, Typography } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { getPacientes } from '../api/pacientesApi';

// Definición de las columnas para la tabla de pacientes
const columns: GridColDef[] = [
  {
    field: 'numero_documento',
    headerName: 'Número Documento',
    width: 150,
  },
  {
    field: 'primer_nombre',
    headerName: 'Primer Nombre',
    width: 150,
  },
  {
    field: 'primer_apellido',
    headerName: 'Primer Apellido',
    width: 150,
  },
  {
    field: 'fecha_nacimiento',
    headerName: 'Fecha de Nacimiento',
    width: 150,
  },
  {
    field: 'genero',
    headerName: 'Género',
    width: 120,
  },
];

export default function PacientesPage() {
  // Usamos useQuery para obtener los datos de los pacientes
  const { data: pacientes, isLoading, isError, error } = useQuery({
    queryKey: ['pacientes'],
    queryFn: getPacientes,
  });

  if (isLoading) {
    return <CircularProgress />;
  }

  if (isError) {
    return <Typography color="error">Error al cargar los datos: {error.message}</Typography>;
  }

  return (
    <Box sx={{ height: 600, width: '100%' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4">Gestión de Pacientes</Typography>
        <Button
          variant="contained"
          component={RouterLink}
          to="/pacientes/nuevo"
        >
          Nuevo Paciente
        </Button>
      </Box>
      <DataGrid
        rows={pacientes || []}
        columns={columns}
        initialState={{
          pagination: {
            paginationModel: { page: 0, pageSize: 10 },
          },
        }}
        pageSizeOptions={[5, 10, 20]}
        // El DataGrid necesita un campo 'id' en cada fila para funcionar correctamente.
        // Nuestro modelo de datos ya lo proporciona.
      />
    </Box>
  );
}