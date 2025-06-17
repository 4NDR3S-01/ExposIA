<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Tema;
use Illuminate\Http\Request;

class TemaController extends Controller
{
    public function index()
    {
        return response()->json(['success' => true, 'data' => Tema::with('presentaciones')->get()]);
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'nombre' => 'required|string|max:255',
            'descripcion' => 'nullable|string',
        ]);

        $tema = Tema::create($data);

        return response()->json(['success' => true, 'data' => $tema->load('presentaciones')], 201);
    }

    public function show(Tema $tema)
    {
        return response()->json(['success' => true, 'data' => $tema->load('presentaciones')]);
    }

    public function update(Request $request, Tema $tema)
    {
        $data = $request->validate([
            'nombre' => 'sometimes|string|max:255',
            'descripcion' => 'nullable|string',
        ]);

        $tema->update($data);

        return response()->json(['success' => true, 'data' => $tema->load('presentaciones')]);
    }

    public function destroy(Tema $tema)
    {
        $tema->delete();
        return response()->json(['success' => true, 'message' => 'Tema eliminado']);
    }
}