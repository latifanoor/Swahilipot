drop table if exists entries;
create table entries(
	id integer primary key autoincrement,
	fullname text not null,
	phone_number integer not null,
	ocupation text not null,
	gender text not null
	);