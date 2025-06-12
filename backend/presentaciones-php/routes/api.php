<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\API\AuthController;
use App\Http\Controllers\UsuarioController;
use App\Http\Controllers\PresentacionController;
use App\Http\Controllers\SlideController;
use App\Http\Controllers\ComentarioController;
use App\Http\Controllers\ReaccionController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Aquí se registran las rutas de tu API, protegidas o públicas.
|
*/

// Ruta de prueba pública
Route::get('/test', function () {
    return response()->json(['mensaje' => 'API funcionando sin auth']);
});

// Rutas públicas de autenticación
Route::prefix('auth')->group(function () {
    Route::post('register', [AuthController::class, 'register']);
    Route::post('login', [AuthController::class, 'login']);
});

// Rutas protegidas con JWT
Route::middleware(['auth:api'])->group(function () {

    // Ruta de prueba autenticada
    Route::get('/test-auth', function () {
        return response()->json([
            'success' => true,
            'mensaje' => '¡Token JWT válido!',
            'usuario' => auth('api')->user(),
            'timestamp' => now()
        ]);
    });

    // Acciones del usuario autenticado
    Route::prefix('auth')->group(function () {
        Route::get('me', [AuthController::class, 'me']);
        Route::post('logout', [AuthController::class, 'logout']);
        Route::post('refresh', [AuthController::class, 'refresh']);
    });

    // Recursos REST protegidos
    Route::apiResource('usuarios', UsuarioController::class);
    Route::apiResource('presentaciones', PresentacionController::class);
    Route::apiResource('slides', SlideController::class);
    Route::apiResource('comentarios', ComentarioController::class);
    Route::apiResource('reacciones', ReaccionController::class);
});
