
import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { TextField, Button, Box, Typography, MenuItem, CircularProgress } from '@mui/material';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { createPaciente, PacienteData } from '../api/pacientesApi';

// 1. Definir el esquema de validación con Zod
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

  // 2. Configurar la mutación para crear el paciente
  const mutation = useMutation({
    mutationFn: createPaciente,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pacientes'] });
      navigate('/pacientes');
    },
  });

  // 3. Configurar react-hook-form
  const {
    control,
    handleSubmit,
    formState: { errors },
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

  // 4. Manejador de envío que llama a la mutación
  const onSubmit = (data: PacienteData) => {
    mutation.mutate(data);
  };

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 1 }}>
      <Typography variant="h4" sx={{ mb: 2 }}>Crear Nuevo Paciente</Typography>
      {mutation.isError && (
        <Typography color="error" sx={{ mb: 2 }}>Error al crear el paciente: {mutation.error.message}</Typography>
      )}
      
      {/* Fila 1 */}
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

      {/* Fila 2 */}
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

      {/* Fila 3 */}
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

      {/* Fila 4 */}
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
        <Button type="submit" variant="contained" color="primary" disabled={mutation.isPending}>
          Guardar Paciente
        </Button>
        {mutation.isPending && (
          <CircularProgress size={24} sx={{ position: 'absolute', top: '50%', left: '50%', marginTop: '-12px', marginLeft: '-12px' }} />
        )}
      </Box>
    </Box>
  );
}
