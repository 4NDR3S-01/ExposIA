<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class TemaFactory extends Factory
{
    protected $model = \App\Models\Tema::class;

    public function definition(): array
    {
        return [
            'nombre' => $this->faker->word(),
            'descripcion' => $this->faker->sentence(),
        ];
    }
}