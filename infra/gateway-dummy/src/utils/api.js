const axios = require('axios');

// URLs de los microservicios con variables de entorno
const getServiceUrls = () => ({
  PHP: process.env.PHP_API_URL || 'http://localhost:8001/api',
  TS: process.env.NEST_API_URL || 'http://localhost:3000',
  PYTHON: process.env.PYTHON_API_URL || 'http://localhost:8000/api/v1',
  JAVA: process.env.JAVA_API_URL || 'http://localhost:8080/api'
});

// Función para determinar el servicio basado en la URL
const getServiceName = (url) => {
  if (url.includes('8001')) return 'PHP';
  if (url.includes('3000')) return 'TypeScript';
  if (url.includes('8000')) return 'Python';
  if (url.includes('8080')) return 'Java';
  return 'Unknown';
};

// Función para manejar errores de API con más detalle
const handleApiError = (error, service) => {
  console.error(`❌ Error en servicio ${service}:`);
  console.error(`   Mensaje: ${error.message}`);
  
  if (error.response) {
    console.error(`   Status: ${error.response.status}`);
    console.error(`   Data:`, error.response.data);
    
    // Personalizar mensajes de error según el status
    switch (error.response.status) {
      case 404:
        throw new Error(`Recurso no encontrado en ${service}`);
      case 500:
        throw new Error(`Error interno del servidor ${service}`);
      case 503:
        throw new Error(`Servicio ${service} no disponible`);
      default:
        throw new Error(`Error ${error.response.status} en ${service}: ${error.message}`);
    }
  } else if (error.request) {
    console.error(`   No se recibió respuesta del servicio ${service}`);
    throw new Error(`${service} no responde - verifique que el servicio esté ejecutándose`);
  } else {
    throw new Error(`Error configurando petición a ${service}: ${error.message}`);
  }
};

// Función principal para hacer peticiones con retry y manejo de errores mejorado
const apiCall = async (url, options = {}, retries = 3) => {
  const service = getServiceName(url);
  
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      console.log(`📡 ${service} - Intento ${attempt}/${retries}: ${options.method || 'GET'} ${url}`);
      
      const response = await axios({
        url,
        timeout: 15000, // 15 segundos de timeout
        ...options,
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...options.headers
        }
      });
      
      console.log(`✅ ${service} - Respuesta exitosa (${response.status})`);
      return response.data;
      
    } catch (error) {
      console.log(`⚠️ ${service} - Intento ${attempt}/${retries} falló`);
      
      if (attempt === retries) {
        handleApiError(error, service);
      }
      
      // Esperar antes del siguiente intento (exponential backoff)
      if (attempt < retries) {
        const delay = Math.pow(2, attempt) * 1000; // 2s, 4s, 8s...
        console.log(`⏳ Esperando ${delay}ms antes del siguiente intento...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }
};

// Función específica para consultas con filtros
const buildQueryUrl = (baseUrl, filters = {}) => {
  const url = new URL(baseUrl);
  Object.entries(filters).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      url.searchParams.append(key, value);
    }
  });
  return url.toString();
};

// Función para validar datos de entrada
const validateInput = (input, requiredFields) => {
  const missing = requiredFields.filter(field => !input[field]);
  if (missing.length > 0) {
    throw new Error(`Campos requeridos faltantes: ${missing.join(', ')}`);
  }
};

module.exports = {
  getServiceUrls,
  apiCall,
  buildQueryUrl,
  validateInput,
  handleApiError
};
