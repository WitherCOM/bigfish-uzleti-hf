CREATE DATABASE IF NOT EXISTS metabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'metabase'@'%' IDENTIFIED BY 'metabase';
GRANT ALL PRIVILEGES ON metabase.* TO 'metabase'@'%' IDENTIFIED BY 'metabase';

CREATE DATABASE IF NOT EXISTS bigfish CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'bigfish'@'%' IDENTIFIED BY 'bigfish';
GRANT ALL PRIVILEGES ON bigfish.* TO 'bigfish'@'%' IDENTIFIED BY 'bigfish';

use bigfish;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS balances;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS categories;

CREATE TABLE IF NOT EXISTS categories (
	category_id bigint auto_increment primary key,
	category_name varchar(100) not null
);

CREATE TABLE IF NOT EXISTS accounts (
	account_id varchar(36)  primary key,
	currency varchar(3) not null,
	nick_name varchar(70),
	type enum('Personal', 'Business') not null,
	subtype enum('CurrentAccount','Loan','Savings') not null
);

CREATE TABLE IF NOT EXISTS transactions (
	transaction_id varchar(36)  primary key,
	account_id varchar(36) not null,
	original_amount double not null,
	currency varchar(3) not null,
	calculated_amount double not null,
	booking_date_time timestamp not null,
	value_date_time timestamp,
	indicator enum('Debit', 'Credit') not null,
	status enum ('Booked', 'Pending') not null,
	proprietary_bank_issuer varchar(35),
	proprietary_bank_code varchar(35),
	transaction_information varchar(500),
	category_id bigint,
	CONSTRAINT fk_category_transactions
		FOREIGN KEY (category_id) 
		REFERENCES categories(category_id),
	CONSTRAINT fk_accounts_transactions
		FOREIGN KEY (account_id) 
		REFERENCES accounts(account_id)
);

CREATE TABLE IF NOT EXISTS balances (
	balance_id varchar(36)  primary key,
	account_id varchar(36) not null,
	original_amount double not null,
	calculated_amount double not null,
	day date not null,
	CONSTRAINT fk_account_balances
		FOREIGN KEY (account_id) 
		REFERENCES accounts(account_id)
);