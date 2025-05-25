<?php

namespace App\Http\Controllers;

use App\Models\Tema;
use Illuminate\Http\Request;

class TemaController extends Controller
{
    /**
     * Muestra todos los temas.
     */
    public function index()
    {
        return Tema::with('presentaciones')->get();
    }

    /**
     * Almacena un nuevo tema.
     */
    public function store(Request $request)
    {
        $data = $request->validate([
            'nombre' => 'required|string|max:255',
            'descripcion' => 'nullable|string',
        ]);

        $tema = Tema::create($data);

        return response()->json($tema, 201);
    }

    /**
     * Muestra un tema específico con sus presentaciones.
     */
    public function show(Tema $tema)
    {
        return $tema->load('presentaciones');
    }

    /**
     * Actualiza un tema existente.
     */
    public function update(Request $request, Tema $tema)
    {
        $data = $request->validate([
            'nombre' => 'sometimes|string|max:255',
            'descripcion' => 'nullable|string',
        ]);

        $tema->update($data);
        return response()->json($tema);
    }

    /**
     * Elimina un tema.
     */
    public function destroy(Tema $tema)
    {
        $tema->delete();
        return response()->json(['message' => 'Tema eliminado']);
    }
}
