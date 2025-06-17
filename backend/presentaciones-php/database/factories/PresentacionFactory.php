<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class PresentacionFactory extends Factory
{
    protected $model = \App\Models\Presentacion::class;

    public function definition(): array
    {
        return [
            'titulo' => $this->faker->sentence(),
            'id_usuario' => \App\Models\Usuario::factory(),
            'id_tema' => \App\Models\Tema::factory(),
            'archivo_pdf' => 'archivo.pdf', // O usa UploadedFile::fake() si realmente subes archivos
        ];
    }
}