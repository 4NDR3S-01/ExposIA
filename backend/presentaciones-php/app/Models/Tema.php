<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Tema extends Model
{
    public function presentaciones(){
        return $this->hasMany(Presentacion::class);
    }
}
