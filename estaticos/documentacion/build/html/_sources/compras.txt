Compras
=======

Si el usuario desea registrar la *Compra de medicamentos a un Laboratorio*, deberá presionar el sub-item ``Compras``.

.. image:: _static/btncompras.png
   :align: center

A continuación el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/compras.png
   :align: center

En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta un nuevo *Usuario*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - Uno o más campos vacíos.
        - Uno o más campos con un formato incorrecto.
        - El nombre de usuario ya existe.
        - Las contraseñas no coinciden.
     
Una vez completado el formulario, el usuario tendrá que presionar el boton ``Registrar`` y el sistema se encargará de dar de alta el nuevo usuario.

Reportes
--------
Si el usuario desea visualizar y/o generar reportes de estadisticas en relacion a las *Ventas*, debera seleccionar el boton de **Reportes**.

.. image:: _static/reportespedfar.png
   :align: center

Esta funcionalidad cuenta con la modalidad de:

    - :ref:`Top 10 Monto de Compras a Laboratorio <top10-mont-compr-pf>`

 .. _top10-mont-compr-pf:

Top 10 Monto de Compras a Laboratorio
+++++++++++++++++++++++++++++++++++++
Si el usuario desea que los reportes se generen en base al volumen de ventas general, debera presionar la opcion ``Top 10 Monto de Compras a Laboratorio``.

.. image:: _static/top10medspedfar.png
   :align: center

Al hacerlo, se mostrara la siguiente pantalla:

.. image:: _static/pantallatop10medspedfar.png
   :align: center

Si el usuario desea ajustar el rango de fecha sobre el cual se genera el reporte puede hacerlo utilizando la modalidad de filtrado por fechas:
El usuario tendrá que ingresar los parámetros de búsqueda en el formulario, y presionar el botón ``Filtrar``.

.. NOTE::
    Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará la informacion historica completa.

.. image:: _static/fechastop10medspedfar.png
   :align: center

Si el usuario desea exportar el resultado generado a una planilla de Excel, debera presionar el ícono de excel.

.. image:: _static/xlstop10medspedfar.png
   :align: center

Si el usuario desea exportar el resultado en un formato de imagen PNG, JPEG, PDF o SVG, debera presionar el boton de herramientas de exportacion y seleccionar la opcion correspondiente.

.. image:: _static/btnexptop10medspedfar.png
   :align: center