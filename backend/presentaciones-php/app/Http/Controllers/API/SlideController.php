<?php

namespace App\Http\Controllers\API;

use App\Http\Controllers\Controller;
use App\Models\Slide;
use Illuminate\Http\Request;

class SlideController extends Controller
{
    public function index()
    {
        return response()->json(['success' => true, 'data' => Slide::with('presentacion')->get()]);
    }

    public function store(Request $request)
    {
        $data = $request->validate([
            'numero_slide' => 'required|integer|min:1',
            'imagen_slide' => 'nullable|string',
            'texto_slide' => 'nullable|string',
            'id_presentacion' => 'required|exists:presentaciones,id',
        ]);

        $slide = Slide::create($data);

        return response()->json(['success' => true, 'data' => $slide->load('presentacion')], 201);
    }

    public function show(Slide $slide)
    {
        return response()->json(['success' => true, 'data' => $slide->load('presentacion')]);
    }

    public function update(Request $request, Slide $slide)
    {
        $data = $request->validate([
            'numero_slide' => 'sometimes|integer|min:1',
            'imagen_slide' => 'nullable|string',
            'texto_slide' => 'nullable|string',
            'id_presentacion' => 'sometimes|exists:presentaciones,id',
        ]);

        $slide->update($data);

        return response()->json(['success' => true, 'data' => $slide->load('presentacion')]);
    }

    public function destroy(Slide $slide)
    {
        $slide->delete();
        return response()->json(['success' => true, 'message' => 'Slide eliminado']);
    }
}