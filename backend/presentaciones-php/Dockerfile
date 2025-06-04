# Usa una imagen oficial de PHP con Apache
FROM php:8.2-apache

# Instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    git unzip zip curl libpq-dev libonig-dev libxml2-dev libzip-dev \
    && docker-php-ext-install pdo pdo_mysql zip

# Instala Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Copia los archivos del proyecto al contenedor
COPY . /var/www/html

WORKDIR /var/www/html

# Ejecuta composer install para generar la carpeta vendor
RUN composer install --no-dev --optimize-autoloader

# Otorga permisos
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

# Habilita mod_rewrite
RUN a2enmod rewrite

# Expone el puerto
EXPOSE 80

# Comando para iniciar Laravel
CMD ["php", "artisan", "serve", "--host=0.0.0.0", "--port=80"]
