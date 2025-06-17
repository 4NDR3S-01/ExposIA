<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Calificacion;
use Illuminate\Http\Request;

class CalificacionController extends Controller
{
    public function index()
    {
        return response()->json(['success' => true, 'data' => Calificacion::with(['presentacion', 'usuario'])->get()]);
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'puntaje' => 'required|integer|min:1|max:10',
            'comentario' => 'nullable|string',
            'id_usuario' => 'required|exists:usuarios,id',
            'id_presentacion' => 'required|exists:presentaciones,id',
        ]);

        $calificacion = Calificacion::create($data);

        return response()->json(['success' => true, 'data' => $calificacion->load(['presentacion', 'usuario'])], 201);
    }

    public function show(Calificacion $calificacion)
    {
        return response()->json(['success' => true, 'data' => $calificacion->load(['presentacion', 'usuario'])]);
    }

    public function update(Request $request, Calificacion $calificacion)
    {
        $data = $request->validate([
            'puntaje' => 'sometimes|integer|min:1|max:10',
            'comentario' => 'nullable|string',
            'id_usuario' => 'sometimes|exists:usuarios,id',
            'id_presentacion' => 'sometimes|exists:presentaciones,id',
        ]);

        $calificacion->update($data);

        return response()->json(['success' => true, 'data' => $calificacion->load(['presentacion', 'usuario'])]);
    }

    public function destroy(Calificacion $calificacion)
    {
        $calificacion->delete();

        return response()->json(['success' => true, 'message' => 'Calificación eliminada']);
    }
}