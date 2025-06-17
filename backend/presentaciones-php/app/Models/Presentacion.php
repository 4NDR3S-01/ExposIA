<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;



class Presentacion extends Model
{
    use HasFactory;
    
    protected $table = 'presentaciones';     // Nombre de la tabla en la base de datos
    protected $fillable = ['titulo', 'id_usuario', 'id_tema', 'archivo_pdf'];     // Los campos que pueden ser asignados masivamente

    // Relación: Presentación pertenece a un Usuario (clave foránea id_usuario)
    public function usuario()
    {
        return $this->belongsTo(Usuario::class, 'id_usuario', 'id');
    }

    // Relación: Presentación pertenece a un Tema (clave foránea id_tema)
    public function tema()
    {
        return $this->belongsTo(Tema::class, 'id_tema', 'id');
    }

    // Relación: Presentación tiene muchos Slides (relacionados por id_presentacion)
    public function slides()
    {
        return $this->hasMany(Slide::class, 'id_presentacion', 'id');
    }

    // Relación: Presentación tiene muchas Calificaciones (relacionadas por id_presentacion)
    public function calificaciones()
    {
        return $this->hasMany(Calificacion::class, 'id_presentacion', 'id');
    }
}

