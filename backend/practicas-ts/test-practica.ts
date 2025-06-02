import axios from 'axios';
import * as fs from 'fs';
import * as FormData from 'form-data';

const api = 'http://localhost:3000';
const audioPath = './1mb.mp3'; //
const reportePath = './reporte-practica.txt';

const log: string[] = [];

function registrarLinea(linea: string) {
  console.log(linea);
  log.push(linea);
}

function guardarReporte() {
  fs.writeFileSync(reportePath, log.join('\n'), 'utf-8');
  console.log(`\n📄 Reporte guardado en: ${reportePath}`);
}

async function subirGrabacion() {
  registrarLinea('\n🎤 Subiendo grabación...');
  const form = new FormData();
  form.append('usuario_id', '4');
  form.append('presentacion_id', '3');
  form.append('archivo_audio', fs.createReadStream(audioPath));
  form.append('nombreArchivo', 'test-audio.mp3');

  const response = await axios.post(`${api}/grabacion/subir`, form, {
    headers: form.getHeaders(),
  });

  registrarLinea(`✅ Grabación subida: ID=${response.data.id}`);
  return response.data.id;
}

async function crearNavegaciones(grabacion_id: number) {
  registrarLinea('\n🧭 Registrando navegación por slides...');
  const eventos = [
    { slide_id: 1, timestamp: 0, tipo_navegacion: 'inicio' },
    { slide_id: 2, timestamp: 5000, tipo_navegacion: 'siguiente' },
    { slide_id: 3, timestamp: 10000, tipo_navegacion: 'siguiente' },
  ];

  for (const evento of eventos) {
    await axios.post(`${api}/navegacion-slide`, { grabacion_id, ...evento });
    registrarLinea(`✔️ Evento: slide ${evento.slide_id}, ts=${evento.timestamp}, tipo=${evento.tipo_navegacion}`);
  }
}

async function crearNota(grabacion_id: number) {
  registrarLinea('\n📝 Añadiendo nota al slide 3...');
  const nota = {
    grabacion_id,
    slide_id: 3,
    contenido: 'Nota generada automáticamente',
    timestamp: 12000,
  };

  const response = await axios.post(`${api}/nota-slide`, nota);
  registrarLinea(`✅ Nota creada: ID=${response.data.id}`);
}

async function crearFragmento(grabacion_id: number) {
  registrarLinea('\n🎧 Generando fragmento de audio...');
  const dto = {
    grabacion_id,
    slide_id: 3,
    inicio_segundo: 10000,
    fin_segundo: 12000,
  };

  const response = await axios.post(`${api}/fragmento-audio`, dto);
  registrarLinea(`✅ Fragmento creado: ${JSON.stringify(response.data)}`);
}

async function main() {
  try {
    registrarLinea('🚀 Iniciando flujo de prueba del módulo de prácticas...');

    const grabacionId = await subirGrabacion();
    await crearNavegaciones(grabacionId);
    await crearNota(grabacionId);
    await crearFragmento(grabacionId);

    registrarLinea('\n✅ Flujo completo ejecutado correctamente');
  } catch (err: any) {
    const errorMsg = err.response?.data ?? err.message;
    registrarLinea(`❌ ERROR: ${JSON.stringify(errorMsg)}`);
  } finally {
    guardarReporte();
  }
}

main();
