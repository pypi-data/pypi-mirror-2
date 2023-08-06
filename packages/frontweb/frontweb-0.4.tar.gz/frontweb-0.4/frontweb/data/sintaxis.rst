Sintáxis
========

Esta página incluye algunas pruebas sobre
la sintaxis de *RestructuredText*, el lenguaje
de *markup* que usamos en **frontweb**.


Formato
-------

- **negrita**.
- *italica*.
- ``codigo monoespaciado``.


Listas
------

- uno
- dos
    - sub-item de dos
    - otro sub-item de dos
- tres


Tablas
------

+---------+------------------------+
| Mes     | Temperatura registrada |
+=========+========================+
| Enero   | 34                     |
+---------+------------------------+
| Febrero | 32                     |
+---------+------------------------+
| Marzo   | 30                     |
+---------+------------------------+
| ...     | ...                    |
+---------+------------------------+

Imágenes
--------


.. image:: images/manzana.png
    :class: noborder


Código
------

Se puede usar pygments para colorear el código:

.. code-block:: python

    import os
    print os.path.join("directorio", "archivo")

.. code-block:: c

    int main(void)
    {
        printf("Hola mundo\n");
        return 0;
    }


O directamente sin colores::

    Texto sin colores
    en varias lineas.
