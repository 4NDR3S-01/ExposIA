<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Presentacion;
use App\Models\Slide;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class PresentacionController extends Controller
{
    public function index()
    {
        $presentaciones = Presentacion::with(['usuario', 'tema', 'slides', 'calificaciones'])->get();
        return response()->json(['success' => true, 'data' => $presentaciones]);
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'titulo' => 'required|string|max:255',
            'id_tema' => 'required|exists:temas,id',
            'archivo_pdf' => 'required|file|mimes:pdf|max:10240',
        ]);

        $data['id_usuario'] = Auth::id();
        $ruta = $request->file('archivo_pdf')->store('presentaciones', 'public');
        $data['archivo_pdf'] = 'storage/' . $ruta;

        $presentacion = Presentacion::create($data);

        // Ejemplo: crear slides vacíos (puedes quitar si no necesitas)
        for ($i = 1; $i <= 3; $i++) {
            Slide::create([
                'numero_slide' => $i,
                'id_presentacion' => $presentacion->id
            ]);
        }

        $presentacion->load(['usuario', 'tema', 'slides', 'calificaciones']);

        return response()->json(['success' => true, 'data' => $presentacion], 201);
    }

    public function show($id)
    {
        $presentacion = Presentacion::with(['usuario', 'tema', 'slides', 'calificaciones'])->findOrFail($id);
        return response()->json(['success' => true, 'data' => $presentacion]);
    }

    public function update(Request $request, $id)
    {
        $presentacion = Presentacion::findOrFail($id);

        $data = $request->validate([
            'titulo' => 'sometimes|string|max:255',
            'id_tema' => 'sometimes|exists:temas,id',
            'archivo_pdf' => 'nullable|file|mimes:pdf|max:10240',
        ]);

        if ($request->hasFile('archivo_pdf')) {
            // Borra el archivo viejo si existe
            if ($presentacion->archivo_pdf && file_exists(public_path($presentacion->archivo_pdf))) {
                @unlink(public_path($presentacion->archivo_pdf));
            }
            $ruta = $request->file('archivo_pdf')->store('presentaciones', 'public');
            $data['archivo_pdf'] = 'storage/' . $ruta;
        }

        $presentacion->update($data);

        return response()->json(['success' => true, 'data' => $presentacion->fresh(['usuario', 'tema', 'slides', 'calificaciones'])]);
    }

    public function destroy($id)
    {
        $presentacion = Presentacion::findOrFail($id);

        if ($presentacion->id_usuario !== Auth::id()) {
            return response()->json(['success' => false, 'message' => 'No autorizado'], 403);
        }

        if ($presentacion->archivo_pdf && file_exists(public_path($presentacion->archivo_pdf))) {
            @unlink(public_path($presentacion->archivo_pdf));
        }

        $presentacion->delete();

        return response()->json(['success' => true, 'message' => 'Presentación eliminada correctamente']);
    }
}