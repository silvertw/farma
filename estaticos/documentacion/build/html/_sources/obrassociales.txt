Obras Sociales
=========
Se presentará una pantalla que contendrá un listado con todas las *Obras Sociales* que se encuentren registradas en el sistema hasta la fecha.

.. image:: _static/obrassociales.png
   :align: center

Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular estas *Obras Sociales*.

Estas funcionalidades son:

    - :ref:`Alta Obra Social <alta-obrasocial>`
    - :ref:`Modificar Obra Social <modificar-obrasocial>`
    - :ref:`Eliminar Obra Social <eliminar-obrasocial>`
    - :ref:`Formulario de Búsqueda <formulario-busqueda-obrasocial>`
    
.. _alta-obrasocial:

Alta Obra Social
-------------
Si el usuario desea crear una nueva *Obra Social*, deberá presionar el botón ``Alta``.

.. image:: _static/btnaltaobrasocial.png
   :align: center

A continuación el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/altaobrasocial.png
   :align: center

En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta una nueva *Obra Social*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - Uno o más campos obligatorios vacíos.
        - Uno o más campos con un formato incorrecto.
        - El CUIT ingresado ya se encuentra asociado a otra organización.
     
Una vez completado el formulario, el usuario tendrá dos opciones: 
    
    - Presionar el botón ``Guardar y Volver``.
    - Presionar el botón ``Guardar y Continuar``.

El botón ``Guardar y Volver`` permite guardar la *Obra Social* en el sistema y volver a la pantalla
principal de *Obra Social*..

El botón ``Guardar y Continuar`` permite guardar la *Obra Social* en el sistema y seguir dando de alta nuevas *Obra Social*.

.. _modificar-obrasocial:

Modificar Obra Social
------------------
Si el usuario desea modificar los datos de una *Obra Social*, deberá seleccionar el botón de **Acción** asociado a la *Obra Social* y presionar la pestaña ``Modificar``.

.. image:: _static/btnmodificarfarm.png
   :align: center

Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/modificarfarm.png
   :align: center

En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados a la *Obra Social*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - Uno o más campos obligatorios vacíos.
        - Uno o más campos con un formato incorrecto.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar Cambios`` y el sistema se encargara de actualizar los datos de la *Obra Social* seleccionada.


.. _eliminar-obrasocial:
   
Eliminar Obra Social
-----------------
Si el usuario desea eliminar una *Obra Social*, deberá seleccionar el botón de **Acción** asociado a la *Obra Social* y presionar la pestaña ``Eliminar``.

.. image:: _static/btneliminarfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/eliminarfarm.png
   :align: center

En esta parte el usuario deberá decidir si confirma la eliminación de la *Obra Social* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.

.. NOTE::
    Aquellas *Obras Sociales* que cumplan las siguientes condiciones **NO** podrán ser eliminadas:

        - Esten asociadas a un Pedido de Obra Social que aún no ha sido completamente enviado.

    El sistema se encargará de informar al usuario las razones por las cuales la *Obra Social* seleccionada no puede eliminarse. En dicho caso, el sistema mostrara una ventana emergente (modal) como esta:
    
    .. image:: _static/fallaeliminarfarm.png
       :align: center

.. _formulario-busqueda-obrasocial:

Formulario de Búsqueda
----------------------
Si el usuario desea visualizar sólo aquellas *Obras Sociales* que cumplan con algunos criterios en específico, deberá utilizar el formulario de búsqueda.

.. image:: _static/busquedafarm.png
   :align: center

Este formulario cuenta con dos modalidades:

    - Búsqueda simple: permite buscar las *Obras Sociales* por razon social.
    - Búsqueda avanzada: permite buscar las *Obras Sociales* por razon social, localidad.

.. NOTE::
    Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará todas las *Obras Sociales*.

El usuario tendrá que ingresar los parámetros de búsqueda en el formulario, y presionar el botón ``Buscar``. El sistema visualizará aquellas *Obras Sociales* que cumplan con todas las condiciones especificadas.

Si el usuario desea limpiar los filtros activos, deberá presionar el boton ``Limpiar``.

.. image:: _static/limpiarfarm.png
   :align: center