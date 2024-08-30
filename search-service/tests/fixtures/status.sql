CREATE TABLE status (
	id integer primary key autoincrement,
	name varchar(32),
	label varchar(64)
);

INSERT INTO status (name,label) VALUES
	 ('comprando','Imueble en proceso de compra'),
	 ('comprado','Inmueble en propiedad de Habi'),
	 ('pre_venta','Inmueble publicado en preventa'),
	 ('en_venta','Inmueble publicado en venta'),
	 ('vendido','Inmueble vendido');
