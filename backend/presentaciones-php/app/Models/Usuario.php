<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Usuario extends Model
{
    public function presentaciones(){
        return $this->hasMany(Presentacion::class);
    }

    public function calificaciones(){
        return $this->hasMany(Calificacion::class);
    }
}
