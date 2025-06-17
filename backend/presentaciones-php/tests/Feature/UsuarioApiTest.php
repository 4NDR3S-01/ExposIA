<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\Usuario;

class UsuarioApiTest extends TestCase
{
    use RefreshDatabase;

    /** @test */
    public function puede_registrar_un_usuario()
    {
        $response = $this->postJson('/api/auth/register', [
            'nombre' => 'Test User',
            'email' => 'testuser@example.com',
            'password' => 'password123'
        ]);

        $response->assertStatus(201)
                 ->assertJsonStructure([
                     'success',
                     'message',
                     'data' => [
                         'usuario' => [
                             'id',
                             'nombre',
                             'email',
                         ],
                         'token',
                         'token_type',
                         'expires_in'
                     ]
                 ]);

        $this->assertDatabaseHas('usuarios', [
            'email' => 'testuser@example.com'
        ]);
    }
}