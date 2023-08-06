Como instalar pilas en windows
==============================


Dependencias
============

python
------


Ir a:

http://www.python.org/download/releases/2.6/


y  bajar la version:

	- Windows X86-64 MSI Installer (2.6)


.. image:: python.png


e instalar:

.. image:: pyinstall.png


Configurar rutas
----------------

Ve a las propiedades de sistema, pulsando el boton
derecho del mouse sobre "mi pc" y luego propiedades.

Luego ve a "avanzado" y "variables de entorno".

.. image:: preferencias.png

Tiene que abrirse una nueva ventana, ahi cambia
el valor de la variable path y coloca la ruta del
directorio de python:

.. image:: path1.png

Tienes que agregar este texto al principio
de la cadena::

	C:\Python26\Scripts;C:\Python26;


.. image:: path2.png



setuptools
----------

Luego puedes ir al sitio pypi e instalar setuptools:

http://pypi.python.org/pypi/setuptools#windows

Tienes que descargar la version 2.6 para windows:

.. image:: shot1.png

Instalando pilas
----------------

Luego tienes que ir al interprete del sistema, menu
inicio ejecutar:

.. image:: menu.png


y escribir el comando "cmd":

.. image:: cmd.png


y una vez que estas en la ventana del interprete
ejecuta el comando "easy_install -U pilas":

.. image:: install.png


Este comando es util que lo tengas anotado, porque
las versiones de pilas salen con frecuencia, y ese
comando solita al servidor la version nueva. Es
recomendable que ejecutes ese comando cada vez
que quieras una version nueva de pilas.



box2d
-----

Tienes que descargar e instalar:

http://pypi.python.org/pypi/Box2D/2.0.2b1

.. image:: box2d.png

readline
---------


Luego instala:

http://pypi.python.org/pypi/pyreadline/1.6.1



SFML
----

ir a la pagina: http://www.sfml-dev.org/download.php

y descargar la version 1.6 de pysfml para la version 2.6
de python

.. image:: sfml.png

puedes ver los pasos mas detallados por aqui:

http://www.examplelab.com.ar/sfml/instalar_sfml_en_windows.rst


Cairo
-----

Tienes que ir al siguiente sitio, y descargar e instalar
la version para python 2.6:

http://ftp.gnome.org/pub/GNOME/binaries/win32/pycairo/1.8/

Luego descarga los siguientes archivos, y busca la DLLs para
copiar en el directorio: C:\Python26\Lib\site-packages\cairo


- http://wxpython.org/cairo/cairo_1.8.6-1_win32.zip
- http://wxpython.org/cairo/libpng_1.2.34-1_win32.zip
- http://wxpython.org/cairo/zlib123-dll.zip 


pygame
-------


Ir a http://www.pygame.org/download.shtml
y descargar la version para python 2.6

.. image:: pygame.png

Probando
--------


Hagamos la primer prueba.

Abre el comando "cmd" nuevamente, ejecuta python y
luego escribe el siguiente codigo:

.. code-block:: python

	import pilas
	pilas.iniciar()
	actor = pilas.actores.Pingu()
	
.. image:: full.png


IDEs recomendados
-----------------


Perfecto, hasta ahora hemos configurado lo basico para
comenzar, el siguiente paso es instalar alguna herramienta
para que escribir tus juegos sea mas sencilla y productiva.

Hay dos herramientas interesantes para programar, IDLE y
IEP


IDLE
----

IDLE es una consola interactiva para que puedas
comenzar a hacer tus primeras pruebas con pilas.

La aplicacion se inicia desde el menu inicio - python 2.6 - IDLE:

.. image:: idle.png

Algo interesante de IDLE es que colorea el codigo
mientras escribes y ademas autocompleta codigo.
 
 
IEP
---

Otro entorno recomendable es IEP, 
esta aplicacion te ayuda a escribir programas y tiene muy
buenas caracteristicas:

.. image:: ide.png

Para instalar la aplicacion tienes que ir a la web del
proyecto:

http://code.google.com/p/iep/

y descargar la version para windows:

   http://iep.googlecode.com/files/iep-2.3.win32.exe
	
	
ten en cuenta que luego de correr un script (con la tecla F5)
tienes que lanzar nuevamente el interprete pulsando CTRL+p

Hagamos una prueba, puedes escribir tu programa interactivamente
para ir investiando un poco pilas. Inicia IEP, vas a ver
algo como esto:

.. image:: iep_base.png


Luego escribe algunas sentencias de pilas, y observa el autocompletado:

.. image:: iep_completado.png

Incluso puedes seguir escribiendo el programa e ir interactuando
con la ventana de pilas:

.. image:: iep_full.png

Por ultimo, para hacer juegos mas completos
puedes ir a la parte inferior de la ventana y
pulsar el boton derecho, ahi puedes seleccioanr
la opcion "crear proyecto":

.. image:: nuevoproyecto.png

luego puedes ir creando
archivos dentro del proyecto, nuevamente pulsando
el boton derecho, y completar tu espacio de trabajo
modularizando los componentes del juego:


recuerda que tienes que usar la tecla F5 para
ejecutar tu juego.


.. image:: iep_en_proyecto.png