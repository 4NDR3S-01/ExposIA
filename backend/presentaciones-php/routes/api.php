<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

use App\Http\Controllers\UsuarioController;
use App\Http\Controllers\TemaController;
use App\Http\Controllers\PresentacionController;
use App\Http\Controllers\SlideController;
use App\Http\Controllers\CalificacionController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and assigned the "api"
| middleware group. Enjoy building your API!
|
*/

// Ruta protegida para obtener el usuario autenticado (si usas Laravel Sanctum)
Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

// Ruta de prueba sin autenticación (para comprobar que la API responde)
Route::get('/prueba', function () {
    return response()->json(['mensaje' => '¡La API funciona correctamente!']);
});

// Rutas RESTful para tus controladores
Route::apiResource('usuarios', UsuarioController::class);
Route::apiResource('temas', TemaController::class);
Route::apiResource('presentaciones', PresentacionController::class);
Route::apiResource('slides', SlideController::class);
Route::apiResource('calificaciones', CalificacionController::class);