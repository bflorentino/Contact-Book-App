import pymysql
import userDBCredentials

class Database():

    def __init__(self):

    # We begin the connection with the database
        self.connection = pymysql.connect(
            host = userDBCredentials.host,   #This is the database host
            user =  userDBCredentials.user,   #This is your username 
            password = userDBCredentials.password,  #This is your paswword to connect to host
            db = userDBCredentials.db  #This is the database you want to connect
        ) 
        
    # UserDBCredentials is a file that I created to store in variables my credentials, so they are not
    # visible in this file. You could use your credentials as Strings directly in the params of the connection  as well

        self.cursor = self.connection.cursor()


    def selectContact(self, id: int):

        """ Get an specific contatc from the Contacts table

        Returns:
            [contact]: The selected contact from the query,
            [False]
        """

        sqlCommand = f"Select * from Contacts where contact_id = {id};"

        try:
            self.connection.begin()
            self.cursor.execute(sqlCommand)
            contact = self.cursor.fetchone()
            return contact
        
        except:
            self.connection.rollback()
            return False


    def selectAllContactsName(self):
        
        """ Get all the contacts from the table

        Returns:
            [contacts]: All the selected contacts
            [False]
        """

        self.connection.begin()
        sqlCommand = f"Select Contact_id, Contact_Name, Phone_Number from Contacts order by Contact_Name;"

        try:
            self.connection.begin()
            self.cursor.execute(sqlCommand)
            contacts = self.cursor.fetchall()
            return contacts
        
        except:
            self.connection.rollback()
            return False


    def updateContactInfo(self, columnsToUpdate: list, newData: list, id):
            
            """ Update a contact info with the new data

            Returns:
                True: if the data was updated
                False: if data couldn't be updated
            """

            if len(columnsToUpdate) == 1:
                sqlCommand = f"Update contacts set {columnsToUpdate[0]} = \"{newData[0]}\" where contact_Id = {id};"
            if len(columnsToUpdate) == 2:
                sqlCommand = f"Update contacts set {columnsToUpdate[0]} = \"{newData[0]}\", {columnsToUpdate[1]} = \"{newData[1]}\" where contact_Id = {id};"
            elif len(columnsToUpdate) == 3:
                sqlCommand = f"Update contacts set {columnsToUpdate[0]} = \"{newData[0]}\", {columnsToUpdate[1]} = \"{newData[1]}\", {columnsToUpdate[2]} = \"{newData[2]}\" where contact_Id = {id};"
            elif len(columnsToUpdate) == 4:
                sqlCommand = f"Update contacts set {columnsToUpdate[0]} = \"{newData[0]}\", {columnsToUpdate[1]} = \"{newData[1]}\", {columnsToUpdate[2]} = \"{newData[2]}\", {columnsToUpdate[3]} = \"{newData[3]}\" where contact_Id = {id};"

            try:
                self.connection.begin()
                self.cursor.execute(sqlCommand)
                self.connection.commit()
                return True
        
            except:
                self.connection.rollback()
                return False


    def deleteContactInfo(self, id):

        """ delete a contact 

        Returns:
            True: if data was deleted
            False: if data couldn't be deleted
        """
        
        sqlCommand = f"delete from contacts where contact_Id = {id}"
        
        try:
            self.connection.begin()
            self.cursor.execute(sqlCommand)
            self.connection.commit()
            return True
        
        except:
            self.connection.rollback()
            return False


    def insertContactInfo(self, name, lastName, phoneNumber, email):
        
        """ It inserts a new contact in the tabla

        Returns:
            True: if conctact was correctly inserted,
            False: if contact couldn't be inserted
        """

        if name is not None and phoneNumber is not None:
            id = 1 + self.getLastContact()[0]

            if lastName is None and email is not None:
                sqlCommand = f"insert into Contacts values({id}, \"{name}\", Null, \"{phoneNumber}\", \"{email}\");"
            elif email is None and lastName is not None:
                sqlCommand = f"insert into Contacts values({id}, \"{name}\", \"{lastName}\", \"{phoneNumber}\", Null);"
            elif email is None and lastName is None:
                sqlCommand = f"insert into Contacts values({id}, \"{name}\", Null, \"{phoneNumber}\", Null);"
            else:
                sqlCommand = f"insert into Contacts values({id}, \"{name}\", \"{lastName}\",  \"{phoneNumber}\", \"{email}\");"
                

            try:
                self.connection.begin()
                self.cursor.execute(sqlCommand)
                self.connection.commit()
                self.connection.close()
                return True
            except:
                self.connection.rollback()
                return False


    def getLastContact(self):
        
        """ Get the last contact from the table.

        Returns:
            lastContact: if contact was correctly selected
            False: if it wasn't correctly selected
        """

        sqlCommand = f"select contact_ID from Contacts order by Contact_ID desc limit 1"
        
        try:
            lastContact = self.cursor.execute(sqlCommand)
            lastContact = self.cursor.fetchone()
            
            return lastContact
        
        except:
            return False
