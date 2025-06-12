<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Usuario;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use Tymon\JWTAuth\Facades\JWTAuth;
use Tymon\JWTAuth\Exceptions\JWTException;

class AuthController extends Controller
{
    /**
     * Registro de nuevo usuario
     */
    public function register(Request $request)
    {
        try {
            $validator = Validator::make($request->all(), [
                'nombre' => 'required|string|max:255',
                'email' => 'required|string|email|max:255|unique:usuarios',
                'password' => 'required|string|min:6',
            ]);

            if ($validator->fails()) {
                return response()->json([
                    'success' => false,
                    'errors' => $validator->errors()
                ], 422);
            }

            $usuario = Usuario::create([
                'nombre' => $request->nombre,
                'email' => $request->email,
                'password' => Hash::make($request->password),
            ]);

            // Configurar el guard para JWT
            $token = auth('api')->login($usuario);

            return response()->json([
                'success' => true,
                'message' => 'Usuario registrado exitosamente',
                'data' => [
                    'usuario' => $usuario,
                    'token' => $token,
                    'token_type' => 'Bearer',
                    'expires_in' => auth('api')->factory()->getTTL() * 60
                ]
            ], 201);

        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error al registrar usuario',
                'error' => $e->getMessage()
            ], 500);
        }
    }

    /**
     * Login de usuario
     */
    public function login(Request $request)
    {
        try {
            $validator = Validator::make($request->all(), [
                'email' => 'required|email',
                'password' => 'required|string|min:6',
            ]);

            if ($validator->fails()) {
                return response()->json([
                    'success' => false,
                    'errors' => $validator->errors()
                ], 422);
            }

            $credentials = $request->only('email', 'password');

            if (!$token = auth('api')->attempt($credentials)) {
                return response()->json([
                    'success' => false,
                    'message' => 'Credenciales inválidas'
                ], 401);
            }

            $usuario = auth('api')->user();

            return response()->json([
                'success' => true,
                'message' => 'Login exitoso',
                'data' => [
                    'usuario' => $usuario,
                    'token' => $token,
                    'token_type' => 'Bearer',
                    'expires_in' => auth('api')->factory()->getTTL() * 60
                ]
            ]);

        } catch (JWTException $e) {
            return response()->json([
                'success' => false,
                'message' => 'No se pudo crear el token',
                'error' => $e->getMessage()
            ], 500);
        }
    }

    /**
     * Obtener usuario autenticado
     */
    public function me()
    {
        try {
            if (!$usuario = auth('api')->user()) {
                return response()->json([
                    'success' => false,
                    'message' => 'Usuario no encontrado'
                ], 404);
            }

            return response()->json([
                'success' => true,
                'data' => [
                    'usuario' => $usuario->load(['presentaciones', 'calificaciones'])
                ]
            ]);

        } catch (JWTException $e) {
            return response()->json([
                'success' => false,
                'message' => 'Token inválido',
                'error' => $e->getMessage()
            ], 500);
        }
    }

    /**
     * Logout
     */
    public function logout()
    {
        try {
            auth('api')->logout();
            return response()->json([
                'success' => true,
                'message' => 'Logout exitoso'
            ]);
        } catch (JWTException $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error al cerrar sesión',
                'error' => $e->getMessage()
            ], 500);
        }
    }

    /**
     * Refrescar token
     */
    public function refresh()
    {
        try {
            $token = auth('api')->refresh();
            return response()->json([
                'success' => true,
                'data' => [
                    'token' => $token,
                    'token_type' => 'Bearer',
                    'expires_in' => auth('api')->factory()->getTTL() * 60
                ]
            ]);
        } catch (JWTException $e) {
            return response()->json([
                'success' => false,
                'message' => 'No se pudo refrescar el token',
                'error' => $e->getMessage()
            ], 500);
        }
    }
}