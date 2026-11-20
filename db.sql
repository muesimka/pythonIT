FOR EACH ROW
set NEW.name=ifnull(new.name,concat('user_', uuid()));

insert into users(name, email, password)
values('-', 'test@email.com', '1234');

select * from users;


CREATE TABLE `academy`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(254) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);
