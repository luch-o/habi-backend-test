CREATE TABLE status_history (
	id integer primary key autoincrement,
	property_id int NOT NULL,
	status_id int NOT NULL,
	update_date TIMESTAMP(26) NOT NULL,
	foreign key (property_id) references property(id),
	foreign key (status_id) references status(id)
);

INSERT INTO status_history (property_id,status_id,update_date) VALUES
	 (1,1,'2021-04-10 22:23:56'),
	 (1,2,'2021-04-11 22:23:56'),
	 (1,3,'2021-04-12 22:23:56'),
	 (2,1,'2021-04-09 22:23:56'),
	 (2,2,'2021-04-10 22:23:56'),
	 (2,3,'2021-04-11 22:23:56'),
	 (2,4,'2021-04-12 22:23:56'),
	 (3,1,'2021-04-12 22:26:25'),
	 (3,2,'2021-04-12 22:26:34'),
	 (3,3,'2021-04-12 22:26:54'),
	 (3,4,'2021-04-12 22:27:06'),
	 (3,5,'2021-04-12 22:27:20'),
	 (4,1,'2021-04-10 22:23:56'),
	 (4,2,'2021-04-11 22:23:56'),
	 (4,3,'2021-04-12 22:23:56'),
	 (5,1,'2021-04-09 22:23:56'),
	 (5,2,'2021-04-10 22:23:56'),
	 (5,3,'2021-04-11 22:23:56'),
	 (5,4,'2021-04-12 22:23:56'),
	 (6,1,'2021-04-12 22:26:25'),
	 (6,2,'2021-04-12 22:26:34'),
	 (6,3,'2021-04-12 22:26:54'),
	 (6,4,'2021-04-12 22:27:06'),
	 (6,5,'2021-04-12 22:27:20');
