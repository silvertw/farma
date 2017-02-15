Pedidos de Farmacia
===================
Se presentará una pantalla que contendrá un listado con todos los *Pedidos de Farmacia* que se encuentren registrados en el sistema hasta la fecha.

.. image:: _static/pedidosfarmacia.png
   :align: center

Junto con el listado, se ofrecerán un conjunto de funcionalidades que permitirán manipular estos *Pedidos de Farmacia*.
Estas funcionalidades son:

- :ref:`Alta Pedido <alta-pf>`
- :ref:`Ver Detalles <ver-detalles-pf>`
- :ref:`Ver Remitos <ver-remitos-pf>`
- :ref:`Formulario de Búsqueda <formulario-busqueda-pf>`

.. _alta-pf:

Alta Pedido
-----------
Si el usuario desea crear un nuevo *Pedido de Farmacia*, deberá presionar el botón ``Alta``.

.. image:: _static/btnaltapedfarm.png
   :align: center

A continuación el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/altapedfarm.png
   :align: center

En este punto el usuario deberá seleccionar la fecha en que llegó el pedido y la farmacia que lo realizó. A continuación deberá presionar el botón ``Crear Pedido``.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
    En este punto, las posibles causas de errores son:

        - La farmacia ingresada no existe.
        - La fecha no existe.
        - La fecha ingresada esta fuera del rango válido.

Una vez presionado el botón ``Crear Pedido``, se mostrará la siguiente pantalla:

.. image:: _static/detallespedfarm.png
   :align: center

Esta pantalla es la encargada de visualizar aquellos detalles que se irán asociando al *Pedido de Farmacia*.
La misma ofrece las siguientes funcionalidades:

    - :ref:`Agregar Detalle <agregar-detalle-pf>`
    - :ref:`Modificar Detalle <modificar-detalle-pf>`
    - :ref:`Eliminar Detalle <eliminar-detalle-pf>`
    - :ref:`Registrar Pedido <registrar-pedido-pf>`

.. _agregar-detalle-pf:

Agregar Detalle
+++++++++++++++
Si el usuario desea agregar un detalle al *Pedido de Farmacia*, deberá presionar el botón ``Alta Detalle``.

.. image:: _static/btnadddetallepedfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/newdetallepedfarm.png
   :align: center

En esta parte, se presentará un formulario que el usuario deberá completar para poder dar de alta un nuevo detalle.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
    En este punto, las posibles causas de errores son:

        - No se seleccionó un medicamento.
        - No se ingresó una cantidad.
        - La cantidad ingresada no posee un formato correcto.
        - La cantidad ingresada es menor a cero.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar`` y el sistema se encargara de agregar el nuevo detalle al pedido.
El usuario podrá seguir dando de alta nuevos detalles, hasta donde considere necesario. Una vez que esto suceda deberá presionar el botón ``Cerrar`` y la ventana emergente desaparecerá.

.. _modificar-detalle-pf:

Modificar Detalle
+++++++++++++++++
Si el usuario desea modificar un detalle del *Pedido de Farmacia*, deberá seleccionar el detalle que desea actualizar y presionar el botón ``Modificar Detalle``.

.. image:: _static/btnupddetallepedfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/upddetallepedfarm.png
   :align: center

En esta parte, se presentará un formulario con la información actual del detalle y el usuario deberá actualizar aquella que considere necesaria.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará.
    En este punto, las posibles causas de errores son:

        - No se ingresó una cantidad.
        - La cantidad ingresada no posee un formato correcto.
        - La cantidad ingresada es menor a cero.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar`` y el sistema se encargará de actualizar la información de dicho detalle.

.. _eliminar-detalle-pf:

Eliminar Detalle
++++++++++++++++
Si el usuario desea eliminar un detalle del *Pedido de Farmacia*, deberá seleccionar el detalle que desea eliminar y presionar el botón ``Baja Detalle``.

.. image:: _static/btndeldetallepedfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/deldetallepedfarm.png
   :align: center

En esta parte el usuario deberá decidir si confirma la eliminación del detalle o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.

.. _registrar-pedido-pf:

Registrar Pedido
++++++++++++++++
Si el usuario desea registrar el *Pedido de Farmacia*, deberá presionar el botón ``Registrar``.

.. image:: _static/btnregpedfarm.png
   :align: center

.. ATTENTION::
    El sistema siempre validará que la información del *Pedido a de Farmacia* sea correcta. En caso de que esta información sea incorrecta el sistema lo informará.
    En este punto, las posibles causas de errores son:

        - El pedido no contiene detalles
        - El pedido ya ha sido registrado anteriormente

Una vez presionado el botón ``Registrar``, el sistema se encargará de crear el *Pedido de Farmacia* y se mostrará la siguiente ventana emergente (modal).

.. image:: _static/regpedfarm.png
   :align: center

.. _ver-detalles-pf:

Ver Detalles
------------
Si el usuario desea ver los detalles de un *Pedido de Farmacia*, deberá seleccionar el botón de **Acción** asociado a dicho pedido y presionar la pestaña ``Ver Detalles``.

.. image:: _static/btndetallespedfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/verdetallespedfarm.png
   :align: center

Esta ventana mostrará todos los detalles del *Pedido de Farmacia* seleccionado.

.. _ver-remitos-pf:

Ver Remitos
-----------
Si el usuario desea ver los remitos asociados a un *Pedido de Farmacia*, deberá seleccionar el botón de **Acción** asociado a dicho pedido y presionar la pestaña ``Ver Remitos``.

.. image:: _static/btnremitospedfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/remitospedfarm.png
   :align: center

Esta ventana mostrará todos los remitos vinculados al *Pedido de Farmacia* seleccionado.

.. NOTE::
    En caso de que el pedido no tenga remitos asociados el sistema lo informará.

El usuario tendra la opción de visualizar un remito en PDF, presionanado el boton ``Descargar`` asociado a él.

.. image:: _static/remitopedidofarmacia.png
   :align: center

<<<<<<< HEAD
.. _notific:

=======
>>>>>>> 4ce2293ba82133da628a2a37e202a2baa199dea6
Notificaciones
--------------
En el caso de que se halla producido un pedido desde un mobile, mientras el sistema no estaba siendo atendido, se producira una notificacion como la siguiente:

.. image:: _static/notificacionDePedidoMobile.png
   :align: center


.. image:: _static/notificacionDePedidoMobileMini.png
   :align: center

Al presionar en el boton ``Ver`` se desplegaran los nuevos pedidos:

.. image:: _static/notificacionDePedidoMobileVer.png
   :align: center

<<<<<<< HEAD

Pedidos con Faltantes distribuidos
----------------------------------
Cuando una farmacia hace un pedido (pequeño de hasta 20 productos) y no tenemos stock en drogueria pero si en Farmacia, podemos optar por pedir a la farmacia el envio del faltante.
En este caso el pedido de ejemplo tenia un pendiente de 10.

.. image:: _static/pendientes1.png
   :align: center

Para completarlo debemos presionar en el boton de ``Intentar completar con farmacias`` y luego ``Busqueda en Farmacia``.

.. image:: _static/pendientes2.png
   :align: center

Por defecto nos dara cual es el movimiento de medicamentos optimo. Pero si queremos podemos elejir de farmacias.

.. image:: _static/pendientes3-1.png
   :align: center

Nos aparecera un cartel de confirmacion.

.. image:: _static/pendienteConfirm.png
   :align: center

Sino la otra opcion es:

.. image:: _static/pendientes3-2.png
   :align: center

Al presionar nos mostrara un modal con informacion de donde el sistema ha encontrado stock para quitar:

.. image:: _static/pendientes4.png
   :align: center

Aqui podremos elejir de que farmacia quitar. A modo de ayuda tenemos colores Rojo y Verde que nos ayudan a saber si me exedi en la cantidad.
El sistema no permite que la cantidad sea mayor.

.. image:: _static/pendiente5.png
  :align: center

.. image:: _static/pendiente6.png
   :align: center

Una vez lista la cantidad de cada uno a quitar presionamos el boton de Registrar.

.. image:: _static/pendienteConfirm.png
   :align: center



=======
>>>>>>> 4ce2293ba82133da628a2a37e202a2baa199dea6
Reportes
--------
Si el usuario desea visualizar y/o generar reportes de estadisticas en relacion a los *Pedidos de Farmacia*, debera seleccionar el boton de **Reportes**.

.. image:: _static/reportespedfar.png
   :align: center

Esta funcionalidad cuenta con 2 modalidades:

    - :ref:`Top 10 farmacias con mayor demanda de medicamentos <top10-meds-pf>`
    - :ref:`Top 10 farmacias con mayor demanda de pedidos <top10-peds-pf>`

 .. _top10-meds-pf:

Top 10 farmacias con mayor demanda de medicamentos
++++++++++++++++++++++++++++++++++++++++++++++++++
Si el usuario desea que los reportes se generen en base al volumen de medicamentos pedidos por cada farmacia, debera presionar la opcion ``Top 10 farmacias con mayor demanda de medicamentos``.

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

.. _top10-peds-pf:

Top 10 farmacias con mayor demanda de pedidos
+++++++++++++++++++++++++++++++++++++++++++++
Si el usuario desea que los reportes se generen en base a la cantidad de pedidos realizados por cada farmacia, debera presionar la opcion ``Top 10 farmacias con mayor demanda de pedidos``.

.. image:: _static/top10pedspedfar.png
   :align: center

Al hacerlo, se mostrara la siguiente pantalla:

.. image:: _static/pantallatop10pedspedfar.png
   :align: center

Si el usuario desea ajustar el rango de fecha sobre el cual se genera el reporte puede hacerlo utilizando la modalidad de filtrado por fechas:
El usuario tendrá que ingresar los parámetros de búsqueda en el formulario, y presionar el botón ``Filtrar``.

.. NOTE::
    Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará la informacion historica completa.

.. image:: _static/fechastop10pedspedfar.png
   :align: center

Si el usuario desea exportar el resultado generado a una planilla de Excel, debera presionar el ícono de excel.

.. image:: _static/xlstop10pedspedfar.png
   :align: center

Si el usuario desea exportar el resultado en un formato de imagen PNG, JPEG, PDF o SVG, debera presionar el boton de herramientas de exportacion y seleccionar la opcion correspondiente.

.. image:: _static/btnexptop10pedspedfar.png
   :align: center

.. _formulario-busqueda-pf:

Formulario de Búsqueda
----------------------
Si el usuario desea visualizar sólo aquellos *Pedidos de Farmacia* que cumplan con algunos criterios en específico, deberá utilizar el formulario de búsqueda.

.. image:: _static/busquedapedfarm.png
   :align: center

Este formulario cuenta con dos modalidades:

    - Búsqueda simple: permite buscar los *Pedidos de Farmacia* por farmacia.
    - Búsqueda avanzada: permite buscar los *Pedidos de Farmacia* por farmacia, fecha desde, fecha hasta y estado del pedido.

.. NOTE::
    Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará todos los *Pedidos de Farmacia*.

Podremos seleccionar desde el siguiente boton los posibles estados a buscar:

.. image:: _static/btnEstadosBusq1.png
   :align: center

Al presionar veremos algo como lo siguiente:

.. image:: _static/btnEstadosBusq2.png
   :align: center

El usuario tendrá que ingresar los parámetros de búsqueda en el formulario, y presionar el botón ``Buscar``. El sistema visualizará aquellos *Pedidos de Farmacia* que cumplan con todas las condiciones especificadas.

Si el usuario desea limpiar los filtros activos, deberá presionar el boton ``Limpiar``.

.. image:: _static/limpiarpedfarm.png
   :align: center