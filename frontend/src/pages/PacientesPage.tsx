import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { DataGrid, GridColDef, GridRenderCellParams } from '@mui/x-data-grid';
import { Box, Button, CircularProgress, Typography, IconButton } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { Edit, Delete } from '@mui/icons-material';
import { getPacientes, deletePaciente } from '../api/pacientesApi';

export default function PacientesPage() {
  const queryClient = useQueryClient();

  // Query para obtener los datos de los pacientes
  const { data: pacientes, isLoading, isError, error } = useQuery({
    queryKey: ['pacientes'],
    queryFn: getPacientes,
  });

  // Mutación para eliminar un paciente
  const deleteMutation = useMutation({
    mutationFn: deletePaciente,
    onSuccess: () => {
      // Invalida y vuelve a obtener la query de pacientes para refrescar la lista
      queryClient.invalidateQueries({ queryKey: ['pacientes'] });
    },
  });

  const handleDelete = (id: string) => {
    if (window.confirm('¿Estás seguro de que deseas eliminar este paciente?')) {
      deleteMutation.mutate(id);
    }
  };

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
    {
      field: 'actions',
      headerName: 'Acciones',
      sortable: false,
      filterable: false,
      width: 100,
      renderCell: (params: GridRenderCellParams) => (
        <Box>
          <IconButton 
            aria-label="edit"
            component={RouterLink}
            to={`/pacientes/editar/${params.row.id}`}
          >
            <Edit />
          </IconButton>
          <IconButton 
            aria-label="delete"
            onClick={() => handleDelete(params.row.id as string)}
            disabled={deleteMutation.isPending}
          >
            <Delete />
          </IconButton>
        </Box>
      ),
    },
  ];

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
      {deleteMutation.isError && (
        <Typography color="error" sx={{ mb: 2 }}>
          Error al eliminar el paciente: {deleteMutation.error.message}
        </Typography>
      )}
      <DataGrid
        rows={pacientes || []}
        columns={columns}
        loading={deleteMutation.isPending}
        initialState={{
          pagination: {
            paginationModel: { page: 0, pageSize: 10 },
          },
        }}
        pageSizeOptions={[5, 10, 20]}
      />
    </Box>
  );
}