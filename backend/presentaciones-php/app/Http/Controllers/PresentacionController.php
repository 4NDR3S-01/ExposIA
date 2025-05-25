<?php

namespace App\Http\Controllers;

use App\Models\Presentacion;
use Illuminate\Http\Request;

class PresentacionController extends Controller
{
    /**
     * Mostrar todas las presentaciones con relaciones.
     */
    public function index()
    {
        return Presentacion::with(['usuario', 'tema', 'slides', 'calificaciones'])->get();
    }

    /**
     * Crear una nueva presentación.
     */
    public function store(Request $request)
    {
        $data = $request->validate([
            'titulo' => 'required|string|max:255',
            'id_usuario' => 'required|exists:usuarios,id',
            'id_tema' => 'required|exists:temas,id',
            'archivo_pdf' => 'nullable|string', // Asegúrate que el campo exista si vas a usarlo
        ]);

        $presentacion = Presentacion::create($data);

        return response()->json($presentacion->load(['usuario', 'tema', 'slides', 'calificaciones']), 201);
    }

    /**
     * Mostrar una presentación específica con relaciones.
     */
    public function show(Presentacion $presentacion)
    {
        return $presentacion->load(['usuario', 'tema', 'slides', 'calificaciones']);
    }

    /**
     * Actualizar una presentación.
     */
    public function update(Request $request, Presentacion $presentacion)
    {
        $data = $request->validate([
            'titulo' => 'sometimes|string|max:255',
            'id_usuario' => 'sometimes|exists:usuarios,id',
            'id_tema' => 'sometimes|exists:temas,id',
            'archivo_pdf' => 'nullable|string',
        ]);

        $presentacion->update($data);

        return response()->json($presentacion->load(['usuario', 'tema', 'slides', 'calificaciones']));
    }

    /**
     * Eliminar una presentación.
     */
    public function destroy(Presentacion $presentacion)
    {
        $presentacion->delete();
        return response()->json(['message' => 'Presentación eliminada']);
    }
}
