<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Tymon\JWTAuth\Facades\JWTAuth;
use Tymon\JWTAuth\Exceptions\JWTException;
use Tymon\JWTAuth\Exceptions\TokenExpiredException;
use Tymon\JWTAuth\Exceptions\TokenInvalidException;

class JWTMiddleware
{
    public function handle(Request $request, Closure $next)
    {
        try {
            // Obtener el token
            $token = $request->bearerToken();
            
            if (!$token) {
                return response()->json(['error' => 'Token no proporcionado'], 401);
            }

            // Establecer el token en JWT
            JWTAuth::setToken($token);
            
            // Intentar obtener el usuario
            $user = JWTAuth::authenticate();
            
            if (!$user) {
                return response()->json(['error' => 'Usuario no encontrado'], 401);
            }

        } catch (TokenExpiredException $e) {
            return response()->json(['error' => 'Token expirado'], 401);
        } catch (TokenInvalidException $e) {
            return response()->json(['error' => 'Token inválido'], 401);
        } catch (JWTException $e) {
            return response()->json(['error' => 'Error procesando token: ' . $e->getMessage()], 401);
        }

        return $next($request);
    }
}