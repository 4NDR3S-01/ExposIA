# backend/presentaciones-php/Dockerfile
FROM php:8.2-apache

# Instala dependencias del sistema y extensiones necesarias
RUN apt-get update && apt-get install -y \
    git zip unzip curl libpq-dev libonig-dev libxml2-dev libzip-dev \
    && docker-php-ext-install pdo pdo_mysql zip

# Instala Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Copia los archivos del proyecto
COPY . /var/www/html

WORKDIR /var/www/html

# Da permisos a Laravel
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# Habilita mod_rewrite para Apache
RUN a2enmod rewrite

# Expone el puerto 80
EXPOSE 80

# Comando para iniciar Laravel
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=80"]
