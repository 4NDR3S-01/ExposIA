<?php

namespace App\Http\Controllers;

use App\Models\Slide;
use Illuminate\Http\Request;

class SlideController extends Controller
{
    /**
     * Muestra todos los slides con su presentación relacionada.
     */
    public function index()
    {
        return Slide::with('presentacion')->get();
    }

    /**
     * Almacena un nuevo slide.
     */
    public function store(Request $request)
    {
        $data = $request->validate([
            'numero_slide' => 'required|integer|min:1',
            'imagen_slide' => 'nullable|string', 
            'texto_slide' => 'nullable|string',
            'id_presentacion' => 'required|exists:presentaciones,id',
        ]);

        $slide = Slide::create($data);

        return response()->json($slide->load('presentacion'), 201);
    }

    /**
     * Muestra un slide específico con su presentación relacionada.
     */
    public function show(Slide $slide)
    {
        return $slide->load('presentacion');
    }

    /**
     * Actualiza un slide existente.
     */
    public function update(Request $request, Slide $slide)
    {
        $data = $request->validate([
            'numero_slide' => 'sometimes|integer|min:1',
            'imagen_slide' => 'nullable|string',
            'texto_slide' => 'nullable|string',
            'id_presentacion' => 'sometimes|exists:presentaciones,id',
        ]);

        $slide->update($data);

        return response()->json($slide->load('presentacion'));
    }

    /**
     * Elimina un slide.
     */
    public function destroy(Slide $slide)
    {
        $slide->delete();
        return response()->json(['message' => 'Slide eliminado']);
    }
}
