<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Slide extends Model
{
    public function presentacion(){
        return $this->belongsTo(Presentacion::class);
    }
}
