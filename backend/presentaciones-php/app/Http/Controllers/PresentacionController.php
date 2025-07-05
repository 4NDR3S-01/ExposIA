<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use App\Models\Presentacion;
use App\Models\Slide;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Services\Notifier;            // ← 1) importa la clase  🔔

class PresentacionController extends Controller
{
    /* ----------------------- GET /presentaciones ----------------------- */
    public function index()
    {
        $presentaciones = Presentacion::with(['usuario', 'tema', 'slides', 'calificaciones'])->get();
        return response()->json(['success' => true, 'data' => $presentaciones]);
    }

    /* ----------------------- POST /presentaciones ---------------------- */
    public function store(Request $request, Notifier $notifier)   // ← 2) Laravel inyecta Notifier  🔔
    {
        $data = $request->validate([
            'titulo'    => 'required|string|max:255',
            'id_tema'   => 'required|exists:temas,id',
            'archivo_pdf' => 'required|file|mimes:pdf|max:10240',
        ]);

        $data['id_usuario'] = Auth::id();
        $ruta = $request->file('archivo_pdf')->store('presentaciones', 'public');
        $data['archivo_pdf'] = 'storage/' . $ruta;

        $presentacion = Presentacion::create($data);

        /* Crea 3 slides “de ejemplo” */
        for ($i = 1; $i <= 3; $i++) {
            Slide::create([
                'numero_slide'   => $i,
                'texto_slide'    => "Contenido slide $i",
                'id_presentacion'=> $presentacion->id
            ]);
        }

        /* 🔔 3) Dispara evento presentación creada */
        $notifier->send('presentation.created', [
            'id'      => $presentacion->id,
            'titulo'  => $presentacion->titulo,
            'ownerId' => $presentacion->id_usuario,
        ]);

        return response()->json(['success' => true, 'data' => $presentacion], 201);
    }

    /* ------------------------ GET /presentaciones/{id} ----------------- */
    public function show($id)
    {
        $presentacion = Presentacion::with(['usuario', 'tema', 'slides', 'calificaciones'])->findOrFail($id);
        return response()->json(['success' => true, 'data' => $presentacion]);
    }

    /* ------------------------ DELETE /presentaciones/{id} -------------- */
    public function destroy($id, Notifier $notifier)              // (opcional) lanza evento borrado
    {
        $presentacion = Presentacion::findOrFail($id);

        if ($presentacion->id_usuario !== Auth::id()) {
            return response()->json(['success' => false, 'message' => 'No autorizado'], 403);
        }

        if ($presentacion->archivo_pdf && file_exists(public_path($presentacion->archivo_pdf))) {
            unlink(public_path($presentacion->archivo_pdf));
        }

        $presentacion->delete();

        /* 🔔 Evento opcional: presentación eliminada */
        $notifier->send('presentation.deleted', [
            'id'     => $id,
            'ownerId'=> Auth::id(),
        ]);

        return response()->json(['success' => true, 'message' => 'Presentación eliminada correctamente']);
    }
}
