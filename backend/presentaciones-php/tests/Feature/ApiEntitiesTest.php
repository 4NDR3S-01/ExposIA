<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;
use App\Models\Usuario;
use App\Models\Presentacion;
use App\Models\Slide;
use App\Models\Tema;
use App\Models\Calificacion;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use PHPUnit\Framework\Attributes\Test;

class ApiEntitiesTest extends TestCase
{
    use RefreshDatabase;

    protected $token;
    protected $usuario;

    protected function setUp(): void
    {
        parent::setUp();

        Storage::fake('public'); // Para fake de archivos PDF

        $this->usuario = Usuario::factory()->create(['password' => bcrypt('password123')]);

        $login = $this->postJson('/api/auth/login', [
            'email' => $this->usuario->email,
            'password' => 'password123'
        ]);

        $this->token = $login->json('data.token');
    }

    protected function authHeaders()
    {
        return [
            'Authorization' => 'Bearer ' . $this->token,
        ];
    }

    #[Test]
    public function puede_listar_usuarios()
    {
        Usuario::factory()->count(3)->create();
        $response = $this->getJson('/api/usuarios', $this->authHeaders());
        $response->assertStatus(200)
                 ->assertJsonStructure([
                     'data' => [
                         '*' => ['id', 'nombre', 'email']
                     ]
                 ]);
    }

    #[Test]
    public function puede_crear_presentacion()
    {
        $tema = Tema::factory()->create();

        $data = [
            'titulo' => 'Presentación de prueba',
            'id_tema' => $tema->id,
            'id_usuario' => $this->usuario->id,
            'archivo_pdf' => UploadedFile::fake()->create('archivo.pdf', 100, 'application/pdf'),
        ];
        $response = $this->postJson('/api/presentaciones', $data, $this->authHeaders());
        $response->assertStatus(201)
                 ->assertJsonFragment(['titulo' => 'Presentación de prueba']);
    }

    #[Test]
    public function puede_listar_presentaciones()
    {
        $tema = Tema::factory()->create();
        Presentacion::factory()->count(2)->create([
            'id_tema' => $tema->id,
            'id_usuario' => $this->usuario->id,
            'archivo_pdf' => 'archivo.pdf' // Si tu factory crea archivos, usa UploadedFile::fake() allí también
        ]);
        $response = $this->getJson('/api/presentaciones', $this->authHeaders());
        $response->assertStatus(200)
                 ->assertJsonStructure([
                     'data' => [
                         '*' => ['id', 'titulo', 'id_tema', 'id_usuario', 'archivo_pdf']
                     ]
                 ]);
    }

    #[Test]
    public function puede_crear_slide()
    {
        $tema = Tema::factory()->create();
        $presentacion = Presentacion::factory()->create([
            'id_tema' => $tema->id,
            'id_usuario' => $this->usuario->id,
            'archivo_pdf' => 'archivo.pdf'
        ]);
        $data = [
            'id_presentacion' => $presentacion->id,
            'numero_slide' => 1,
            'imagen_slide' => null,
            'texto_slide' => 'Contenido 1',
        ];
        $response = $this->postJson('/api/slides', $data, $this->authHeaders());
        $response->assertStatus(201)
                 ->assertJsonFragment(['texto_slide' => 'Contenido 1']);
    }

    #[Test]
    public function puede_crear_tema()
    {
        $data = [
            'nombre' => 'Tema de prueba',
            'descripcion' => 'Descripción de prueba',
        ];
        $response = $this->postJson('/api/temas', $data, $this->authHeaders());
        $response->assertStatus(201)
                 ->assertJsonFragment(['nombre' => 'Tema de prueba']);
    }

    #[Test]
    public function puede_crear_calificacion()
    {
        $tema = Tema::factory()->create();
        $presentacion = Presentacion::factory()->create([
            'id_tema' => $tema->id,
            'id_usuario' => $this->usuario->id,
            'archivo_pdf' => 'archivo.pdf'
        ]);
        $data = [
            'id_presentacion' => $presentacion->id,
            'id_usuario' => $this->usuario->id,
            'puntaje' => 5,
            'comentario' => 'Muy buena presentación',
        ];
        $response = $this->postJson('/api/calificaciones', $data, $this->authHeaders());
        $response->assertStatus(201)
                 ->assertJsonFragment(['puntaje' => 5]);
    }
}