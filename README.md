#  Solucion prueba técnica para desarrollador Backend

Esta prueba consiste en dos microservicios, uno de consulta de propiedades y uno de "me gusta". Para el primero se proporciona el codigo para un microservicio funcional, y para el segúndo únicamente el diseño.

Requerimientos para el servicio de consulta:
- Los usuarios pueden consultar los inmuebles con los estados "pre_venta", "en_venta", y "vendido".
- Los usuarios pueden filtrar estos inmuebles por: Año de construcción, Ciudad, Estado.
- Los usuarios pueden aplicar varios filtros en la misma consulta.
- Los usuarios pueden ver la siguiente información del inmueble: Dirección, Ciudad, Estado, Precio de Venta, y Descripción.

> Para el servicio de consulta fueron proveidos los datos de conexión a una base de datos existente.

Para el servicio de "Me Gusta":
- Los usuarios pueden darle me gusta a un inmueble en específico y esto debe quedar registrado en la base de datos.
- Los "Me Gusta" son de usuarios registrados, y debe quedar registrado en la base de datos el histórico de "me gusta" de cada usuario y a cuáles inmuebles.

> El servicio de "Me Gusta" es conceptual, no existe el modelo de la base de datos para soportarlo así que en lugar de una impleentación se entrega un diseño.

## Tecnologías Usadas

Para el desarrollo del microservicio de consulta, ante la restricción de utilizar un web framework se opta por desarrollar una aplicación serverless en AWS utilizando serverless framework como herramienta de infraestructura como código. El lenguage de programación utlizado en la función lambda es Python.
