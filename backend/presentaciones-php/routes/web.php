<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PresentacionController;
use App\Http\Controllers\UsuarioController;

// Ruta principal - página de bienvenida
Route::get('/', function () {
    return view('welcome');
});

// Rutas para mostrar formularios de registro y login (vistas Blade)
Route::get('/registro', function() {
    return view('auth.register');
})->name('registro');

Route::get('/login', function() {
    return view('auth.login');
})->name('login');

// Rutas para manejar presentaciones (CRUD web, no API)
Route::resource('presentaciones', PresentacionController::class, [
    'parameters' => ['presentaciones' => 'presentacion']
]);

// Ruta para registrar usuarios mediante formulario web (POST)
Route::post('/usuarios', [UsuarioController::class, 'store'])->name('usuarios.store');
