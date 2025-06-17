<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Usuario;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class UsuarioController extends Controller
{
    // Listar todos los usuarios
    public function index()
    {
        return response()->json([
            'success' => true,
            'data' => Usuario::with(['presentaciones', 'calificaciones'])->get()
        ]);
    }

    // Crear un nuevo usuario
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

    // Mostrar un usuario específico
    public function show($id)
    {
        $usuario = Usuario::with(['presentaciones', 'calificaciones'])->findOrFail($id);
        return response()->json(['success' => true, 'data' => $usuario]);
    }

    // Actualizar usuario
    public function update(Request $request, $id)
    {
        $usuario = Usuario::findOrFail($id);

        $data = $request->validate([
            'nombre' => 'sometimes|string|max:255',
            'email' => 'sometimes|email|unique:usuarios,email,' . $id,
            'password' => 'nullable|string|min:6',
        ]);

        if (isset($data['password'])) {
            $data['password'] = Hash::make($data['password']);
        } else {
            unset($data['password']);
        }

        $usuario->update($data);

        return response()->json(['success' => true, 'data' => $usuario]);
    }

    // Eliminar usuario
    public function destroy($id)
    {
        $usuario = Usuario::findOrFail($id);
        $usuario->delete();
        return response()->json(['success' => true, 'message' => 'Usuario eliminado']);
    }
}