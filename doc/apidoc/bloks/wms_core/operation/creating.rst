Creating Operations
~~~~~~~~~~~~~~~~~~~
This Operations take no Goods records as inputs, and have one or
several of them as outcomes.

Model.Wms.Operation.Arrival
---------------------------
.. autoclass:: anyblok_wms_base.bloks.wms_core.operation.arrival.Arrival

   .. raw:: html

      <h3>Fields and their semantics</h3>

   .. autoattribute:: id
   .. autoattribute:: goods_type
   .. autoattribute:: goods_code
   .. autoattribute:: goods_properties

   .. raw:: html

      <h3>Specific members</h3>

   .. autoattribute:: inputs_number

   .. raw:: html

      <h3>Mandatory methods of Operation subclasses</h3>

   .. automethod:: after_insert
   .. automethod:: execute_planned
