<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    // database/migrations/xxxx_create_presentacions_table.php
public function up()
{
    Schema::create('presentacions', function (Blueprint $table) {
        $table->id('id_presentacion');
        $table->unsignedBigInteger('id_usuario');
        $table->string('titulo');
        $table->string('archivo_pdf');
        $table->date('fecha_subida');
        $table->timestamps();
    });
}

};
