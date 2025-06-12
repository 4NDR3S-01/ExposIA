<?php

namespace App\Http\Controllers;

use App\Models\Presentacion;
use App\Models\Slide;
use App\Models\Tema;
use Illuminate\Http\Request;

class PresentacionController extends Controller
{
    /**
     * Mostrar todas las presentaciones con relaciones.
     */
    public function index()
    {
        $presentaciones = Presentacion::with(['usuario', 'tema', 'slides', 'calificaciones'])->get();
        return view('presentaciones.index', compact('presentaciones'));
    }

    /**
     * Mostrar formulario para crear una nueva presentación.
     */
    public function create()
    {
        $temas = Tema::all();
        return view('presentaciones.create', compact('temas'));
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
            'archivo_pdf' => 'required|file|mimes:pdf|max:10240',
        ]);

        // Guardar el archivo en carpeta pública directamente accesible
        if ($request->hasFile('archivo_pdf')) {
            $file = $request->file('archivo_pdf');
            
            // Directorio donde guardar - aseguramos que exista
            $uploadDir = 'uploads/pdfs';
            if (!file_exists(public_path($uploadDir))) {
                mkdir(public_path($uploadDir), 0755, true);
            }
            
            // Nombre único para el archivo
            $fileName = time() . '_' . preg_replace('/\s+/', '_', $file->getClientOriginalName());
            
            // Mover el archivo a la carpeta pública
            $file->move(public_path($uploadDir), $fileName);
            
            // Guardar la ruta relativa en la base de datos
            $data['archivo_pdf'] = $uploadDir . '/' . $fileName;
        }

        // Crear la presentación
        $presentacion = Presentacion::create($data);

        // Crear algunos slides básicos
        for ($i = 1; $i <= 3; $i++) {
            Slide::create([
                'numero_slide' => $i,
                'texto_slide' => 'Contenido para slide ' . $i,
                'id_presentacion' => $presentacion->id
            ]);
        }

        return redirect()->route('presentaciones.show', $presentacion)
            ->with('success', 'Presentación creada correctamente. El PDF está disponible en: ' . url($data['archivo_pdf']));
    }

    /**
     * Mostrar una presentación específica con relaciones.
     */
    public function show(Presentacion $presentacion)
    {
        $presentacion->load(['usuario', 'tema', 'slides', 'calificaciones']);
        return view('presentaciones.show', compact('presentacion'));
    }

    /**
     * Mostrar formulario para editar una presentación.
     */
    public function edit(Presentacion $presentacion)
    {
        $temas = Tema::all();
        return view('presentaciones.edit', compact('presentacion', 'temas'));
    }

    /**
     * Actualizar una presentación.
     */
    public function update(Request $request, Presentacion $presentacion)
    {
        $data = $request->validate([
            'titulo' => 'sometimes|string|max:255',
            'id_tema' => 'sometimes|exists:temas,id',
            'archivo_pdf' => 'nullable|file|mimes:pdf|max:10240',
        ]);

        // Si se proporciona un nuevo archivo PDF
        if ($request->hasFile('archivo_pdf')) {
            // Eliminar el archivo antiguo si existe
            if ($presentacion->archivo_pdf && file_exists(public_path($presentacion->archivo_pdf))) {
                unlink(public_path($presentacion->archivo_pdf));
            }

            $file = $request->file('archivo_pdf');
            
            // Directorio donde guardar
            $uploadDir = 'uploads/pdfs';
            if (!file_exists(public_path($uploadDir))) {
                mkdir(public_path($uploadDir), 0755, true);
            }
            
            // Nombre único para el archivo
            $fileName = time() . '_' . preg_replace('/\s+/', '_', $file->getClientOriginalName());
            
            // Mover el archivo a la carpeta pública
            $file->move(public_path($uploadDir), $fileName);
            
            // Guardar la ruta relativa en la base de datos
            $data['archivo_pdf'] = $uploadDir . '/' . $fileName;
        }

        $presentacion->update($data);

        return redirect()->route('presentaciones.show', $presentacion)
            ->with('success', 'Presentación actualizada correctamente.');
    }

    /**
     * Eliminar una presentación.
     */
    public function destroy(Presentacion $presentacion)
    {
        // Eliminar el archivo si existe
        if ($presentacion->archivo_pdf && file_exists(public_path($presentacion->archivo_pdf))) {
            unlink(public_path($presentacion->archivo_pdf));
        }

        // Eliminar la presentación (los slides se eliminarán por la relación cascada)
        $presentacion->delete();

        if (request()->expectsJson()) {
            return response()->json(['message' => 'Presentación eliminada correctamente']);
        }

        return redirect()->route('presentaciones.index')
            ->with('success', 'Presentación eliminada correctamente.');
    }
}
