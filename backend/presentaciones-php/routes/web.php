<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PresentacionController;
use App\Http\Controllers\UsuarioController;

// Página principal
Route::get('/', function () {
    return view('welcome');
});

// Formularios de registro y login (Blade)
Route::get('/registro', function() {
    return view('auth.register');
})->name('registro');

Route::get('/login', function() {
    return view('auth.login');
})->name('login');

// CRUD de presentaciones usando vistas Blade/web
Route::resource('presentaciones', PresentacionController::class,
    ['parameters' => ['presentaciones' => 'presentacion']]
);

// Registro de usuarios por formulario web (POST)
Route::post('/usuarios', [UsuarioController::class, 'store'])->name('usuarios.store');