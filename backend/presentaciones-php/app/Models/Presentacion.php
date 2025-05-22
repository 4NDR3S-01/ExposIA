<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Presentacion extends Model
{
    public function usuario(){
        return $this->belongsTo(Usuario::class);
    }

    public function tema(){
        return $this->belongsTo(Tema::class);
    }

    public function slides(){
        return $this->hasMany(Slide::class);
    }

    public function calificaciones(){
        return $this->hasMany(Calificacion::class);
    }
}
