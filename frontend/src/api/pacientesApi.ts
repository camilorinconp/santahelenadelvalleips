
import axios from 'axios';

// Interfaz de TypeScript que coincide con el modelo Pydantic de Paciente
export interface Paciente {
  id: string; // UUID se maneja como string en JSON
  tipo_documento: string;
  numero_documento: string;
  primer_nombre: string;
  segundo_nombre?: string;
  primer_apellido: string;
  segundo_apellido?: string;
  fecha_nacimiento: string; // Las fechas se manejan como strings en JSON
  genero: string;
}

// Tipo para los datos del formulario, excluyendo el id que es generado por el servidor
export type PacienteData = Omit<Paciente, 'id'>;

// Configuración de la instancia de Axios
// La URL base apunta al backend de FastAPI. 
// Asumimos que el backend corre en el puerto 8000.
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Función para obtener todos los pacientes
export const getPacientes = async (): Promise<Paciente[]> => {
  try {
    const response = await apiClient.get<{ data: Paciente[] }>('/pacientes/');
    return response.data.data; // Se accede a la propiedad anidada "data"
  } catch (error) {
    console.error('Error fetching pacientes:', error);
    throw error;
  }
};

// Función para obtener un paciente por su ID
export const getPacienteById = async (id: string): Promise<Paciente> => {
  try {
    const response = await apiClient.get<{ data: Paciente }>(`/pacientes/${id}`);
    return response.data.data;
  } catch (error) {
    console.error(`Error fetching paciente with id ${id}:`, error);
    throw error;
  }
};

// Función para crear un nuevo paciente
export const createPaciente = async (pacienteData: PacienteData): Promise<Paciente> => {
  try {
    const response = await apiClient.post<{ data: Paciente[] }>('/pacientes/', pacienteData);
    return response.data.data[0]; // El backend devuelve un array con el nuevo objeto
  } catch (error) {
    console.error('Error creating paciente:', error);
    throw error;
  }
};

// Función para actualizar un paciente
export const updatePaciente = async ({ id, ...pacienteData }: { id: string } & PacienteData): Promise<Paciente> => {
  try {
    const response = await apiClient.put<{ data: Paciente[] }>(`/pacientes/${id}`, pacienteData);
    return response.data.data[0];
  } catch (error) {
    console.error(`Error updating paciente with id ${id}:`, error);
    throw error;
  }
};

// Función para eliminar un paciente
export const deletePaciente = async (id: string): Promise<void> => {
  try {
    await apiClient.delete(`/pacientes/${id}`);
  } catch (error) {
    console.error('Error deleting paciente:', error);
    throw error;
  }
};
