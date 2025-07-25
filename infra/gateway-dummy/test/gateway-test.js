const axios = require('axios');

const GATEWAY_URL = 'http://localhost:4000';

// Función para ejecutar consultas GraphQL
const executeQuery = async (query, variables = {}) => {
  try {
    const response = await axios.post(GATEWAY_URL, {
      query,
      variables
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 10000
    });
    
    if (response.data.errors) {
      console.error('❌ GraphQL Errors:', response.data.errors);
      return null;
    }
    
    return response.data.data;
  } catch (error) {
    console.error('❌ Network Error:', error.message);
    return null;
  }
};

// Tests básicos
const tests = [
  {
    name: 'Test Conectividad Gateway',
    query: `
      query TestBasico {
        usuarios {
          id
          nombre
        }
      }
    `
  },
  {
    name: 'Test Módulo PHP - Usuarios',
    query: `
      query TestPHP {
        usuarios {
          id
          nombre
          email
          created_at
        }
      }
    `
  },
  {
    name: 'Test Módulo Python - Tipos de Métrica',
    query: `
      query TestPython {
        tiposMetrica {
          id
          nombre
          descripcion
        }
      }
    `
  },
  {
    name: 'Test Módulo Java - Criterios',
    query: `
      query TestJava {
        criteriosEvaluacion {
          id
          nombre
          descripcion
        }
      }
    `
  },
  {
    name: 'Test Usuario Específico',
    query: `
      query TestUsuario($id: ID!) {
        usuario(id: $id) {
          id
          nombre
          email
          presentaciones {
            id
            titulo
          }
        }
      }
    `,
    variables: { id: "1" }
  },
  {
    name: 'Test Flujo Completo',
    query: `
      query TestFlujoCompleto($userId: ID!, $presentacionId: ID!) {
        flujoCompleto(id_presentacion: $presentacionId, id_usuario: $userId) {
          usuario {
            nombre
          }
          presentacion {
            titulo
          }
          estado
          timestamp
        }
      }
    `,
    variables: { userId: "1", presentacionId: "1" }
  }
];

// Ejecutar todos los tests
const runTests = async () => {
  console.log('🚀 Iniciando tests del API Gateway...\n');
  
  let passed = 0;
  let failed = 0;
  
  for (const test of tests) {
    console.log(`📋 Ejecutando: ${test.name}`);
    
    const result = await executeQuery(test.query, test.variables);
    
    if (result) {
      console.log('✅ PASSED');
      console.log(`   Datos recibidos:`, JSON.stringify(result, null, 2));
      passed++;
    } else {
      console.log('❌ FAILED');
      failed++;
    }
    
    console.log(''); // línea en blanco
  }
  
  console.log('📊 RESUMEN DE TESTS:');
  console.log(`✅ Pasaron: ${passed}`);
  console.log(`❌ Fallaron: ${failed}`);
  console.log(`📋 Total: ${tests.length}`);
  
  if (failed === 0) {
    console.log('\n🎉 ¡Todos los tests pasaron! El gateway está funcionando correctamente.');
  } else {
    console.log('\n⚠️ Algunos tests fallaron. Revisa la configuración de los microservicios.');
  }
};

// Test de mutation (comentado por defecto para no crear datos de prueba)
const testMutation = async () => {
  console.log('🧪 Test de Mutation - Flujo Completo...');
  
  const mutation = `
    mutation TestFlujoCompleto {
      ejecutarFlujoCompleto(
        id_usuario: "1"
        id_presentacion: "1"
        archivo_audio: "test_audio.mp3"
        navegaciones: [
          {
            numero_slide: 1
            tiempo_inicio: 0.0
            tiempo_fin: 30.0
          }
        ]
        notas: [
          {
            numero_slide: 1
            nota: "Test de nota"
          }
        ]
        usar_ia_calificacion: false
      ) {
        estado
        timestamp
        usuario {
          nombre
        }
        presentacion {
          titulo
        }
      }
    }
  `;
  
  const result = await executeQuery(mutation);
  
  if (result) {
    console.log('✅ Mutation ejecutada exitosamente');
    console.log('   Resultado:', JSON.stringify(result, null, 2));
  } else {
    console.log('❌ Mutation falló');
  }
};

// Función principal
const main = async () => {
  console.log('='.repeat(60));
  console.log('🎯 SUITE DE TESTS - EXPOSIA API GATEWAY');
  console.log('='.repeat(60));
  
  // Verificar que el gateway esté ejecutándose
  try {
    await axios.get('http://localhost:4000/.well-known/apollo/server-health');
    console.log('✅ Gateway está ejecutándose en puerto 4000\n');
  } catch (error) {
    console.log('❌ Gateway no está ejecutándose. Inicia el servidor primero.');
    console.log('   Comando: npm start o npm run dev\n');
    return;
  }
  
  await runTests();
  
  // Descomenta la siguiente línea para probar mutations
  // await testMutation();
};

// Ejecutar si se llama directamente
if (require.main === module) {
  main();
}

module.exports = {
  executeQuery,
  runTests,
  testMutation
};
