<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Tema extends Model
{
    protected $table = 'temas'; // Nombre de la tabla en la base de datos
    protected $fillable = ['nombre', 'descripcion'];     // Campos que se pueden asignar masivamente

    // Relación: un tema tiene muchas presentaciones
    public function presentaciones()
    {
        return $this->hasMany(Presentacion::class, 'id_tema', 'id');
    }
}
