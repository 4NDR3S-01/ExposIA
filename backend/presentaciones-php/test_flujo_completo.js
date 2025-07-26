import axios from 'axios';
import FormData from 'form-data';
import fs from 'fs';

// --- CONFIGURACIÓN ---
const API_BASE_URL = 'http://localhost:8000/api';

const RESET = '\x1b[0m';
const GREEN = '\x1b[32m';
const RED = '\x1b[31m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';

const logInfo = (message) => console.log(`\n${CYAN}--- ${message} ---${RESET}`);
const logSuccess = (message) => console.log(`${GREEN}✔ SUCCESS:${RESET} ${message}`);
const logFailure = (message, error) => {
  console.error(`${RED}✖ FAILURE:${RESET} ${message}`);
  if (error?.response?.data) {
    console.error(RED, JSON.stringify(error.response.data, null, 2), RESET);
  } else if (error?.message) {
    console.error(RED, error.message, RESET);
  }
};

const apiClient = axios.create({ baseURL: API_BASE_URL });

async function runFullFlowTest() {
  logInfo(`INICIANDO PRUEBA DE FLUJO COMPLETO PARA ${API_BASE_URL}`);

  let token;
  let userId, temaId, presentacionId, slideId, calificacionId;

  const testIdentifier = Date.now();
  const newUser = {
    nombre: `Usuario de Prueba ${testIdentifier}`,
    email: `testuser_${testIdentifier}@example.com`,
    password: 'password_segura_123'
  };

  try {
    // 1. REGISTRO DE NUEVO USUARIO
    logInfo('PASO 1: REGISTRO DE NUEVO USUARIO');
    const registerResponse = await apiClient.post('/usuarios', newUser);
    userId = registerResponse?.data?.data?.id;
    if (!userId) throw new Error('No se pudo obtener el ID del usuario registrado.');
    logSuccess(`Usuario registrado: ${newUser.email} con ID: ${userId}`);

    // 2. AUTENTICACIÓN
    logInfo('PASO 2: AUTENTICACIÓN');
    const loginResponse = await apiClient.post('/auth/login', { email: newUser.email, password: newUser.password });
    token = loginResponse?.data?.data?.token;
    if (!token) throw new Error('No se pudo obtener el token del login.');
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    logSuccess(`Login exitoso para ${newUser.email}.`);

    // 3. CREACIÓN (CREATE)
    logInfo('PASO 3: CREANDO RECURSOS');
    const temaResponse = await apiClient.post('/temas', { nombre: 'Tema de Prueba Automatizada', descripcion: 'Creado por script' });
    temaId = temaResponse?.data?.data?.id;
    if (!temaId) throw new Error('No se pudo obtener el ID del tema creado.');
    logSuccess(`Tema creado con ID: ${temaId}`);

    // ENVÍO DE PDF REAL (FormData)
    const form = new FormData();
    form.append('titulo', 'Presentación de Prueba');
    form.append('id_usuario', userId);
    form.append('id_tema', temaId);
    form.append('archivo_pdf', fs.createReadStream('./test.pdf'));

    const presentacionResponse = await apiClient.post(
      '/presentaciones',
      form,
      { headers: { ...form.getHeaders(), Authorization: `Bearer ${token}` } }
    );
    presentacionId = presentacionResponse?.data?.data?.id;
    if (!presentacionId) throw new Error('No se pudo obtener el ID de la presentación creada.');
    logSuccess(`Presentación creada con ID: ${presentacionId}`);

    const slideResponse = await apiClient.post('/slides', { numero_slide: 1, texto_slide: 'Slide de prueba', id_presentacion: presentacionId });
    slideId = slideResponse?.data?.data?.id;
    if (!slideId) throw new Error('No se pudo obtener el ID del slide creado.');
    logSuccess(`Slide creado con ID: ${slideId}`);

    const calificacionResponse = await apiClient.post('/calificaciones', { puntaje: 5, comentario: 'Calificación de prueba', id_usuario: userId, id_presentacion: presentacionId });
    calificacionId = calificacionResponse?.data?.data?.id;
    if (!calificacionId) throw new Error('No se pudo obtener el ID de la calificación creada.');
    logSuccess(`Calificación creada con ID: ${calificacionId}`);

    // 4. LECTURA (READ)
    logInfo('PASO 4: LEYENDO RECURSOS CREADOS');
    await apiClient.get(`/temas/${temaId}`);
    logSuccess(`Lectura del Tema ID: ${temaId}`);
    await apiClient.get(`/presentaciones/${presentacionId}`);
    logSuccess(`Lectura de la Presentación ID: ${presentacionId}`);

    // 5. ACTUALIZACIÓN (UPDATE)
    logInfo('PASO 5: ACTUALIZANDO RECURSOS');
    await apiClient.put(`/temas/${temaId}`, { nombre: 'Tema de Prueba (Actualizado)' });
    logSuccess(`Actualización del Tema ID: ${temaId}`);

  } catch (error) {
    logFailure('Una operación crítica falló. Se procederá a la limpieza.', error);
  } finally {
    // 6. LIMPIEZA (DELETE)
    logInfo('PASO 6: LIMPIEZA DE RECURSOS DE PRUEBA');
    if (!token) {
      console.log(YELLOW, 'No hay token, no se puede realizar la limpieza completa.', RESET);
      return;
    }

    if (calificacionId) { try { await apiClient.delete(`/calificaciones/${calificacionId}`); logSuccess(`Calificación eliminada ID: ${calificacionId}`); } catch (e) { logFailure(`No se pudo eliminar la calificación ID: ${calificacionId}`, e); } }
    if (slideId) { try { await apiClient.delete(`/slides/${slideId}`); logSuccess(`Slide eliminado ID: ${slideId}`); } catch (e) { logFailure(`No se pudo eliminar el slide ID: ${slideId}`, e); } }
    if (presentacionId) { try { await apiClient.delete(`/presentaciones/${presentacionId}`); logSuccess(`Presentación eliminada ID: ${presentacionId}`); } catch (e) { logFailure(`No se pudo eliminar la presentación ID: ${presentacionId}`, e); } }
    if (temaId) { try { await apiClient.delete(`/temas/${temaId}`); logSuccess(`Tema eliminado ID: ${temaId}`); } catch (e) { logFailure(`No se pudo eliminar el tema ID: ${temaId}`, e); } }

    try { await apiClient.post('/auth/logout'); logSuccess('Logout exitoso.'); } catch(e) { logFailure('Falló el logout.', e); }

    if (userId) {
      try {
        await apiClient.delete(`/usuarios/${userId}`);
        logSuccess(`Usuario de prueba eliminado ID: ${userId}`);
      } catch (e) {
        logFailure(`No se pudo eliminar el usuario de prueba ID: ${userId}. Puede que necesites hacerlo manualmente.`, e);
      }
    }

    logInfo('PRUEBA DE FLUJO COMPLETO FINALIZADA');
  }
}

runFullFlowTest();
