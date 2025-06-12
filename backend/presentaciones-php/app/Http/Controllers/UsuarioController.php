<?php

namespace App\Http\Controllers;

use App\Models\Usuario;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class UsuarioController extends Controller
{
    /**
     * Listar todos los usuarios
     */
    public function index()
    {
        try {
            $usuarios = Usuario::all();
            return response()->json([
                'success' => true,
                'data' => $usuarios
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'error' => 'Error al obtener usuarios: ' . $e->getMessage()
            ], 500);
        }
    }

    /**
     * Crear nuevo usuario
     */
    public function store(Request $request)
    {
        $data = $request->validate([
            'nombre' => 'required|string|max:255',
            'email' => 'required|email|unique:usuarios,email',
            'password' => 'required|string|min:6',
        ]);

        $data['password'] = Hash::make($data['password']);
        $usuario = Usuario::create($data);
        
        return response()->json([
            'success' => true,
            'data' => $usuario
        ], 201);
    }

    /**
     * Muestra un usuario específico con sus relaciones.
     */
    public function show($id)
    {
        $usuario = Usuario::findOrFail($id);
        return response()->json(['success' => true, 'data' => $usuario]);
    }

    /**
     * Actualiza un usuario existente.
     */
    public function update(Request $request, $id)
    {
        $usuario = Usuario::findOrFail($id);
        $usuario->update($request->all());
        return response()->json(['success' => true, 'data' => $usuario]);
    }

    /**
     * Elimina un usuario.
     */
    public function destroy($id)
    {
        Usuario::destroy($id);
        return response()->json(['success' => true, 'message' => 'Usuario eliminado']);
    }
}
