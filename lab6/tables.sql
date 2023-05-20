create table user(
	user_id int not null auto_increment,
	username varchar(45) not null,
	first_name varchar(45) not null,
	last_name varchar(45) not null,
	email varchar(45) not null,
	password varchar(255) not null,
	phone varchar(20) not null,
	user_status enum('admin', 'user'),
	primary key (user_id));

create table category(
	category_id int not null auto_increment,
	name varchar(45) not null,
	primary key (category_id)
	);

create table ticket(
	ticket_id int not null auto_increment,
	name varchar(45) not null,
	price int not null,
	category_id int not null,
	quantity int not null,
	date datetime not null,
	place varchar(45) not null,
	status enum('available', 'sold out'),
	info varchar(1500) not null,
	primary key (ticket_id),
	constraint fk_ticket_1 foreign key (category_id) references category(category_id) on delete cascade
	);

create table purchase(
	purchase_id int not null auto_increment,
	ticket_id int not null,
	user_id int not null,
	quantity int not null,
	total_price int not null,
	status enum('bought', 'booked', 'canceled'),
	primary key (purchase_id),
	constraint fk_purchase_ticket_1 foreign key (ticket_id) references ticket(ticket_id) on delete cascade,
	constraint fk_purchase_user1 foreign key (user_id) references user(user_id) on delete cascade
	);