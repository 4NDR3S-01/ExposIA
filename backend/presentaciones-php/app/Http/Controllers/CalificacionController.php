<?php

namespace App\Http\Controllers;

use App\Models\Calificacion;
use Illuminate\Http\Request;

class CalificacionController extends Controller
{
    /**
     * Devuelve todas las calificaciones con su presentación y usuario relacionados.
     */
    public function index()
    {
        return Calificacion::with(['presentacion', 'usuario'])->get();
    }

    /**
     * Almacena una nueva calificación.
     */
    public function store(Request $request)
    {
        $data = $request->validate([
            'puntaje' => 'required|integer|min:1|max:10',
            'comentario' => 'nullable|string',
            'id_usuario' => 'required|exists:usuarios,id',
            'id_presentacion' => 'required|exists:presentaciones,id',
        ]);

        $calificacion = Calificacion::create($data);

        return response()->json($calificacion->load(['presentacion', 'usuario']), 201);
    }

    /**
     * Muestra una calificación específica.
     */
    public function show(Calificacion $calificacion)
    {
        return $calificacion->load(['presentacion', 'usuario']);
    }

    /**
     * Actualiza una calificación existente.
     */
    public function update(Request $request, Calificacion $calificacion)
    {
        $data = $request->validate([
            'puntaje' => 'sometimes|integer|min:1|max:10',
            'comentario' => 'nullable|string',
            'id_usuario' => 'sometimes|exists:usuarios,id',
            'id_presentacion' => 'sometimes|exists:presentaciones,id',
        ]);

        $calificacion->update($data);

        return response()->json($calificacion->load(['presentacion', 'usuario']));
    }

    /**
     * Elimina una calificación.
     */
    public function destroy(Calificacion $calificacion)
    {
        $calificacion->delete();

        return response()->json(['message' => 'Calificación eliminada']);
    }
}
