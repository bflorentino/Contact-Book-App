
Create database phonebook;

Use phonebook;

Create Table Contacts(
Contact_ID int primary key not null,
Contact_Name varchar(50) not null,
Last_Name varchar(50),
Phone_Number varchar(12) not null Constraint Phone_Chars_Length check(length(Phone_Number) = 12),
Email varchar(50)
);
