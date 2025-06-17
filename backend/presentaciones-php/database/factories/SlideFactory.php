<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class SlideFactory extends Factory
{
    protected $model = \App\Models\Slide::class;

    public function definition(): array
    {
        return [
            'numero_slide'    => $this->faker->numberBetween(1, 20),
            'imagen_slide'    => $this->faker->optional()->imageUrl(640, 480, 'business'),
            'texto_slide'     => $this->faker->paragraph(),
            'id_presentacion' => \App\Models\Presentacion::factory(),
        ];
    }
}