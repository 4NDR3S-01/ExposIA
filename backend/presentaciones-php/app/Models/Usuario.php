<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Tymon\JWTAuth\Contracts\JWTSubject;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Usuario extends Authenticatable implements JWTSubject
{
    use HasFactory;
    
    protected $table = 'usuarios'; // Nombre real de la tabla en tu BD
    protected $fillable = ['nombre', 'email', 'password'];     // Campos que se pueden asignar masivamente
    protected $hidden = ['password'];

    // Métodos requeridos por JWTSubject
    public function getJWTIdentifier()
    {
        return $this->getKey();
    }

    public function getJWTCustomClaims()
    {
        return [
            'nombre' => $this->nombre,
            'email' => $this->email,
        ];
    }

    // Relación 1:N con presentaciones
    public function presentaciones()
    {
        return $this->hasMany(Presentacion::class, 'id_usuario', 'id');
    }

    // Relación 1:N con calificaciones
    public function calificaciones()
    {
        return $this->hasMany(Calificacion::class, 'id_usuario', 'id');
    }
}
