create table user (
    user_id INT UNSIGNED AUTO_INCREMENT primary key ,
    username varchar(100) not null unique ,
    password varchar(100) not null ,
    role varchar(100) not null
)