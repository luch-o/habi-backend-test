CREATE TABLE property (
	id integer primary key autoincrement,
	address varchar(120),
	city varchar(32),
	price bigint NOT NULL,
	description TEXT(32767),
	"year" int
);

INSERT INTO property (address,city,price,description,`year`) VALUES
	 ('calle 23 #45-67','bogota',120000000,'Hermoso apartamento en el centro de la ciudad',2000),
	 ('carrera 100 #15-90','bogota',350000000,'Amplio apartamento en conjunto cerrado',2011),
	 ('diagonal 23 #28-21','bogota',270000000,'Apartamento con hermosas vistas',2018),
	 ('calle 23 #45-67','medellin',210000000,'',2002),
	 ('carrera 100 #15-90','medellin',325000000,'Amplio apartamento en conjunto cerrado',2011),
	 ('diagonal 23 #28-21','medellin',270000000,'',NULL),
	 ('','',0,NULL,NULL);
