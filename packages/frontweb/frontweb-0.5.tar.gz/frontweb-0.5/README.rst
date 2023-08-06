========
FrontWeb
========

FrontWeb es una herramienta para crear sitios web personales, como
wikis o blogs, pero que usa un enfoque distinto a otras
herramientas:

- Te permite focalizar tu atención en el contenido del sitio usando 
  restructured text.
- Se integra a controles de versiones (mercurial o git).
- Funciona sobre django, para que lo puedas integrar a otras aplicaciones.


Instalación
-----------

Antes de continuar necesitas tener instalado:

    - python
    - python-docutils
    - django

La forma mas directa de instalar la aplicación
es usando el siguiente comando::

    sudo easy_install frontweb

Pero, si eres un desarrollador y quieres modificar el
código de frontweb, otra opción es descargar todo
el código fuente de la aplicación y luego usar
el script ``setup.py`` con el siguiente
comando::

    sudo python setup.py develop

Este comando instala frontweb en tu máquina, pero
asociada al directorio en dónde has descargado
todo el código fuente.

Cómo utilizarlo
===============

Primero tienes que crear un directorio para tu
sitio web, y luego invocar al comando ``init``::

    mkdir mi_web
    cd mi_web

    frontweb init


Una vez ejecutado el comando verá que tiene archivos nuevos
en el directorio.

- El archivo ``config.ini`` le permite definir el nombre del sitio y varios
  parámetros de configuración.
- El directorio ``data`` todos los archivos que conforman su sitio web.
- El directorio ``plugins`` tiene todos los complementos que se pueden utilizar.


¿Cómo puedo ejecutar la aplicación?
===================================

En ambientes de desarrollo o en las primeras pruebas
puedes ejecutar el siguiente comando::

    frontweb run

Este comando tomará algunos datos de configuración
del archivo ``config.ini``. Modifica este archivo
según tus preferencias.


Créditos
========

Los iconos del proyecto ha sido creados por Matthieu James: 

    http://tiheum.deviantart.com/art/Faenza-Icons-173323228 
    (Bajo la licencia GPL v3)
