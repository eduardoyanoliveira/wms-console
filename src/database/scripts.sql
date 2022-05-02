CREATE TABLE tbl_storehouse (
	id serial primary key,
	name varchar(70)
); 

CREATE TABLE tbl_product (
	id serial primary key ,
	description varchar,
	width decimal,
	height integer,
	len decimal,
	weight decimal,
	price decimal,
	cubic_volume decimal
);

CREATE TABLE tbl_address(
	storehouse_id integer,
	street_number integer,
	block_number integer,
	building_number integer,
	apartment_number integer,
	product_id integer,
	product_qty decimal
);

ALTER TABLE tbl_address ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES tbl_product(id);
ALTER TABLE tbl_address ADD CONSTRAINT fk_storehouse_id FOREIGN KEY (storehouse_id) REFERENCES tbl_storehouse(id);