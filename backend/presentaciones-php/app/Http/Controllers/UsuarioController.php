<?php

namespace App\Http\Controllers;

use App\Models\Usuario;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class UsuarioController extends Controller
{
    /**
     * Muestra una lista de todos los usuarios con sus relaciones.
     */
    public function index()
    {
        return Usuario::with(['presentaciones', 'calificaciones'])->get();
    }

    /**
     * Almacena un nuevo usuario en la base de datos.
     */
    public function store(Request $request)
    {
        $data = $request->validate([
            'nombre' => 'required|string|max:255',
            'email' => 'required|email|unique:usuarios,email',
            'password' => 'required|string|min:6',
        ]);

        // Encriptar la contraseña
        $data['password'] = Hash::make($data['password']);

        $usuario = Usuario::create($data);
        return response()->json($usuario, 201);
    }

    /**
     * Muestra un usuario específico con sus relaciones.
     */
    public function show(Usuario $usuario)
    {
        return $usuario->load(['presentaciones', 'calificaciones']);
    }

    /**
     * Actualiza un usuario existente.
     */
    public function update(Request $request, Usuario $usuario)
    {
        $data = $request->validate([
            'nombre' => 'sometimes|string|max:255',
            'email' => 'sometimes|email|unique:usuarios,email,' . $usuario->id,
            'password' => 'nullable|string|min:6',
        ]);

        // Encriptar el password solo si se envió uno nuevo
        if (!empty($data['password'])) {
            $data['password'] = Hash::make($data['password']);
        } else {
            unset($data['password']);
        }

        $usuario->update($data);
        return response()->json($usuario);
    }

    /**
     * Elimina un usuario.
     */
    public function destroy(Usuario $usuario)
    {
        $usuario->delete();
        return response()->json(['message' => 'Usuario eliminado']);
    }
}
