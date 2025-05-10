# Inicilizar el proyecto de forma local 

**En consola**
php artisan serve

**En el navegador**
http://127.0.0.1:8000

# Método HTTP	Ruta                Acción en el controlador	Descripción
GET             /categorias	        index	                    Listar todas las categorías
POST	        /categorias	        store	                    Crear una nueva categoría
GET	            /categorias/{id}	show	                    Mostrar una categoría específica
PUT/PATCH	    /categorias/{id}	update	                    Actualizar una categoría existente
DELETE	        /categorias/{id}	destroy	                    Eliminar una categoría específica