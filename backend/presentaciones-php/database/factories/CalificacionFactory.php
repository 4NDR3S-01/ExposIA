<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class CalificacionFactory extends Factory
{
    protected $model = \App\Models\Calificacion::class;

    public function definition(): array
    {
        return [
            'puntaje' => $this->faker->numberBetween(1, 5),
            'comentario' => $this->faker->optional()->sentence(),
            'id_usuario' => \App\Models\Usuario::factory(),
            'id_presentacion' => \App\Models\Presentacion::factory(),
        ];
    }
}