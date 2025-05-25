<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Usuario extends Model
{
    protected $table = 'usuarios'; // Nombre real de la tabla en tu BD
    protected $fillable = ['nombre', 'email', 'password'];     // Campos que se pueden asignar masivamente

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
