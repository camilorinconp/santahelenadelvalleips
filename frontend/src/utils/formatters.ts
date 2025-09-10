// frontend/src/utils/formatters.ts

/**
 * Convierte recursivamente todos los valores null o undefined en un objeto a cadenas vacías.
 * Útil para sanear datos de API antes de pasarlos a componentes controlados de React.
 * @param obj El objeto a sanear.
 * @returns Un nuevo objeto con los valores null/undefined reemplazados por cadenas vacías.
 */
export const convertNullsToEmptyStrings = (obj: any): any => {
  if (obj === null || typeof obj === 'undefined') {
    return '';
  }
  if (typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(convertNullsToEmptyStrings);
  }

  const newObj: { [key: string]: any } = {};
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      newObj[key] = convertNullsToEmptyStrings(obj[key]);
    }
  }
  return newObj;
};