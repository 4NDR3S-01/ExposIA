<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Calificacion extends Model
{
    protected $table = 'calificaciones';     // Nombre de la tabla en la base de datos
    protected $fillable = ['puntaje', 'comentario','id_usuario', 'id_presentacion'];     // Campos que se pueden asignar masivamente

    // Relación: Una calificación pertenece a una presentación
    public function presentacion()
    {
        return $this->belongsTo(Presentacion::class, 'id_presentacion', 'id');
    }

    // Relación: Una calificación pertenece a un usuario
    public function usuario()
    {
        return $this->belongsTo(Usuario::class, 'id_usuario', 'id');
    }
}
