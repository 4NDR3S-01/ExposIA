<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        api: __DIR__.'/../routes/api.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        $middleware->alias([
            'jwt' => \App\Http\Middleware\JWTMiddleware::class,              // Alias 'jwt' para rutas protegidas
            'jwt.debug' => \App\Http\Middleware\DebugJWTMiddleware::class,   // Otro middleware, si lo usas
        ]);
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();