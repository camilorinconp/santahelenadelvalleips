
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
    // En una aplicación real, manejaríamos este error de forma más elegante
    throw error;
  }
};
