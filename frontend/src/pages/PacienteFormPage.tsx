
import React, { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { TextField, Button, Box, Typography, MenuItem, CircularProgress } from '@mui/material';
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query';
import { useNavigate, useParams } from 'react-router-dom';
import { createPaciente, getPacienteById, updatePaciente, PacienteData } from '../api/pacientesApi';

// El esquema de validación no cambia
const pacienteSchema = z.object({
  tipo_documento: z.string().min(1, 'El tipo de documento es requerido'),
  numero_documento: z.string().min(1, 'El número de documento es requerido'),
  primer_nombre: z.string().min(1, 'El primer nombre es requerido'),
  segundo_nombre: z.string().optional(),
  primer_apellido: z.string().min(1, 'El primer apellido es requerido'),
  segundo_apellido: z.string().optional(),
  fecha_nacimiento: z.string().refine((val) => !isNaN(Date.parse(val)), {
    message: 'Fecha de nacimiento inválida',
  }),
  genero: z.string().min(1, 'El género es requerido'),
});

export default function PacienteFormPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { id } = useParams<{ id: string }>(); // Obtener el ID de la URL
  const isEditMode = !!id;

  // 1. Si estamos en modo edición, obtener los datos del paciente
  const { data: pacienteData, isLoading: isLoadingPaciente } = useQuery({
    queryKey: ['pacientes', id],
    queryFn: () => getPacienteById(id!),
    enabled: isEditMode, // Solo ejecutar esta query si estamos en modo edición
  });

  const {
    control,
    handleSubmit,
    formState: { errors },
    reset, // Función para resetear el formulario con nuevos valores
  } = useForm<PacienteData>({
    resolver: zodResolver(pacienteSchema),
    defaultValues: {
      tipo_documento: '',
      numero_documento: '',
      primer_nombre: '',
      segundo_nombre: '',
      primer_apellido: '',
      segundo_apellido: '',
      fecha_nacimiento: '',
      genero: '',
    },
  });

  // 2. Usar un useEffect para poblar el formulario cuando los datos se cargan
  useEffect(() => {
    if (pacienteData) {
      console.log('Datos del paciente antes de formatear:', pacienteData);
      // Formatear la fecha para el input type="date"
      const formattedData = {
        ...pacienteData,
        fecha_nacimiento: pacienteData.fecha_nacimiento.split('T')[0],
        // Saneamiento del campo genero
        genero: (pacienteData.genero === 'M' || pacienteData.genero === 'F') ? pacienteData.genero : 'M',
      };
      console.log('Datos del paciente después de formatear:', formattedData);
      reset(formattedData);
    }
  }, [pacienteData, reset]);

  // 3. Mutaciones para crear y actualizar
  const createMutation = useMutation({
    mutationFn: createPaciente,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pacientes'] });
      navigate('/pacientes');
    },
  });

  const updateMutation = useMutation({
    mutationFn: updatePaciente,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pacientes'] });
      navigate('/pacientes');
    },
  });

  // 4. El manejador de envío ahora decide qué mutación llamar
  const onSubmit = (data: PacienteData) => {
    console.log('Submitting form. isEditMode:', isEditMode, 'ID:', id, 'Data:', data);
    if (isEditMode) {
      updateMutation.mutate({ id: id!, ...data });
    } else {
      createMutation.mutate(data);
    }
  };

  const mutation = isEditMode ? updateMutation : createMutation;

  if (isLoadingPaciente) {
    return <CircularProgress />;
  }

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 1 }}>
      <Typography variant="h4" sx={{ mb: 2 }}>
        {isEditMode ? 'Editar Paciente' : 'Crear Nuevo Paciente'}
      </Typography>
      {mutation.isError && (
        <Typography color="error" sx={{ mb: 2 }}>Error: {mutation.error.message}</Typography>
      )}
      
      {/* El resto del formulario es idéntico */}
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Box sx={{ flex: 1 }}>
          <Controller
            name="tipo_documento"
            control={control}
            render={({ field }) => (
              <TextField {...field} select label="Tipo de Documento" variant="outlined" fullWidth error={!!errors.tipo_documento} helperText={errors.tipo_documento?.message}>
                <MenuItem value="CC">Cédula de Ciudadanía</MenuItem>
                <MenuItem value="TI">Tarjeta de Identidad</MenuItem>
                <MenuItem value="RC">Registro Civil</MenuItem>
                <MenuItem value="CE">Cédula de Extranjería</MenuItem>
              </TextField>
            )}
          />
        </Box>
        <Box sx={{ flex: 1 }}>
          <Controller
            name="numero_documento"
            control={control}
            render={({ field }) => <TextField {...field} label="Número de Documento" variant="outlined" fullWidth error={!!errors.numero_documento} helperText={errors.numero_documento?.message} />}
          />
        </Box>
      </Box>

      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Box sx={{ flex: 1 }}>
          <Controller
            name="primer_nombre"
            control={control}
            render={({ field }) => <TextField {...field} label="Primer Nombre" variant="outlined" fullWidth error={!!errors.primer_nombre} helperText={errors.primer_nombre?.message} />}
          />
        </Box>
        <Box sx={{ flex: 1 }}>
          <Controller
            name="segundo_nombre"
            control={control}
            render={({ field }) => <TextField {...field} label="Segundo Nombre (Opcional)" variant="outlined" fullWidth />}
          />
        </Box>
      </Box>

      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Box sx={{ flex: 1 }}>
          <Controller
            name="primer_apellido"
            control={control}
            render={({ field }) => <TextField {...field} label="Primer Apellido" variant="outlined" fullWidth error={!!errors.primer_apellido} helperText={errors.primer_apellido?.message} />}
          />
        </Box>
        <Box sx={{ flex: 1 }}>
          <Controller
            name="segundo_apellido"
            control={control}
            render={({ field }) => <TextField {...field} label="Segundo Apellido (Opcional)" variant="outlined" fullWidth />}
          />
        </Box>
      </Box>

      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <Box sx={{ flex: 1 }}>
          <Controller
            name="fecha_nacimiento"
            control={control}
            render={({ field }) => <TextField {...field} label="Fecha de Nacimiento" type="date" InputLabelProps={{ shrink: true }} variant="outlined" fullWidth error={!!errors.fecha_nacimiento} helperText={errors.fecha_nacimiento?.message} />}
          />
        </Box>
        <Box sx={{ flex: 1 }}>
          <Controller
            name="genero"
            control={control}
            render={({ field }) => (
              <TextField {...field} select label="Género" variant="outlined" fullWidth error={!!errors.genero} helperText={errors.genero?.message}>
                <MenuItem value="M">Masculino</MenuItem>
                <MenuItem value="F">Femenino</MenuItem>
              </TextField>
            )}
          />
        </Box>
      </Box>

      <Box sx={{ mt: 3, position: 'relative' }}>
        <Button 
          type="submit" 
          variant="contained" 
          color="primary"
          disabled={mutation.isPending}
        >
          {isEditMode ? 'Actualizar Paciente' : 'Guardar Paciente'}
        </Button>
        {mutation.isPending && (
          <CircularProgress
            size={24}
            sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              marginTop: '-12px',
              marginLeft: '-12px',
            }}
          />
        )}
      </Box>
    </Box>
  );
}
