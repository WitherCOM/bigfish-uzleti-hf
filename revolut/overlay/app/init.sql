drop table if exists revolut_users;
create table revolut_users (
	id bigint auto_increment primary key,
	token_id varchar(255) unique,
	access_token varchar(255) unique,
	expires_at datetime
);
