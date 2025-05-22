<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Calificacion extends Model
{
    public function usuario(){
        return $this->belongsTo(Usuario::class);
    }

    public function presentacion(){
        return $this->belongsTo(Presentacion::class);
    }
}
