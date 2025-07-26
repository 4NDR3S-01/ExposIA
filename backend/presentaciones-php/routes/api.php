<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\API\AuthController;
use App\Http\Controllers\API\UsuarioController;
use App\Http\Controllers\API\PresentacionController;
use App\Http\Controllers\API\SlideController;
use App\Http\Controllers\API\ComentarioController;
use App\Http\Controllers\API\ReaccionController;
use App\Http\Controllers\API\TemaController;
use App\Http\Controllers\API\CalificacionController;

// Ruta pública para probar que la API funciona sin autenticación
Route::get('/test', function () {
    return response()->json(['mensaje' => 'API funcionando sin auth']);
});

// Rutas públicas de autenticación
Route::prefix('auth')->group(function () {
    Route::post('register', [AuthController::class, 'register']);
    Route::post('login', [AuthController::class, 'login']);
});

// Registro público directo como usuario
Route::post('/usuarios', [UsuarioController::class, 'store']);

// === RUTAS TEMPORALMENTE SIN AUTH PARA TESTING ===
// TODO: Mover a auth centralizada desde API Gateway
Route::get('/usuarios', [UsuarioController::class, 'index']);
Route::get('/usuarios/{id}', [UsuarioController::class, 'show']);
Route::put('/usuarios/{id}', [UsuarioController::class, 'update']);
Route::delete('/usuarios/{id}', [UsuarioController::class, 'destroy']);

Route::apiResource('presentaciones', PresentacionController::class);
Route::apiResource('slides', SlideController::class);
Route::apiResource('comentarios', ComentarioController::class);
Route::apiResource('reacciones', ReaccionController::class);
Route::apiResource('temas', TemaController::class);
Route::apiResource('calificaciones', CalificacionController::class);

// Rutas protegidas por JWT (mantener solo las de auth)
Route::middleware(['jwt'])->group(function () {

    Route::get('/test-auth', function () {
        return response()->json([
            'success' => true,
            'mensaje' => '¡Token JWT válido!',
            'usuario' => auth()->user(),
            'timestamp' => now()
        ]);
    });

    Route::prefix('auth')->group(function () {
        Route::post('logout', [AuthController::class, 'logout']);
        Route::get('me', [AuthController::class, 'me']);
        Route::post('refresh', [AuthController::class, 'refresh']);
    });

});