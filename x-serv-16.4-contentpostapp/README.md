# X-Serv-16.4-contentPostApp
Ejercicio 16.4 - Clase contentPostApp

## Enunciado

Esta ejercicio parte de la clase <b>contentApp</b> (ejercicio 16.3), basada en el esquema de clases definido en el ejercicio <a href="https://github.com/CursosWeb/X-Serv-14.5-ServAplicaciones">Clase servidor de aplicaciones</a>, sirve el contenido almacenado en un diccionario Python. La clave del diccionario es el nombre de recurso a servir, y el valor es el cuerpo de la página HTML correspondiente a ese recurso.

En este ejercicio se pide modificar <b>contentApp</b> en <b>contentPostApp</b>. En este caso, la clase permite la actualización del contenido mediante peticiones HTTP POST. 

Para probarla, se puede usar el add-on de Firefox llamado <i>Poster</i>, aunque también deberá funcionar con <a href="http://www.w3.org/TR/html4/interact/forms.html">formularios HTML</a>.

En definitiva, se pide que cuando se reciba un GET pidiendo cualquier recurso, se buscará en el diccionario de contenidos, y si existe, se servirá. En cualquier caso (exista o no exista el contenido en cuestión) se servirá en la misma página un formulario que permitirá actualizar el contenido del diccionario (o crear una nueva entrada, si no existía) mediante un POST.

## Forma de entrega

Este ejercicio no requiere ser entregado.
