<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;


class Slide extends Model
{
    use HasFactory;
    
    protected $table = 'slides';     // Nombre de la tabla en la base de datos
    protected $fillable = ['numero_slide', 'imagen_slide', 'texto_slide', 'id_presentacion'];     // Campos que se pueden asignar masivamente

    // Relación: un Slide pertenece a una Presentación (clave foránea id_presentacion)
    public function presentacion()
    {
        return $this->belongsTo(Presentacion::class, 'id_presentacion', 'id');
    }
}
