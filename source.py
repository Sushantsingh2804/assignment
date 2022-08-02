import sqlite3
from prettytable import PrettyTable
import re
import datetime


#DATABASE CONNECTION
connection = sqlite3.connect("Sales.db")

#TABLE CREATION
connection.execute('''  CREATE TABLE IF NOT EXISTS USER (
                        USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        USER_NAME TEXT,
                        USER_PASSWORD TEXT,
                        ACCOUNT_TYPE INTEGER,
                        PHONE_NUMBER TEXT,
                        EMAIL TEXT
                    );''')
connection.execute('''  CREATE TABLE IF NOT EXISTS PRODUCT(
                        PRODUCT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        NAME TEXT,
                        COST FLOAT,
                        STOCK INTEGER
                    );''')
connection.execute('''  CREATE TABLE IF NOT EXISTS INVOICE(
                        INVOICE_NUMBER TEXT PRIMARY KEY,
                        USER_ID INTEGER,
                        FOREIGN KEY (USER_ID) REFERENCES USER(USER_ID)
                    );''')
connection.execute('''  CREATE TABLE IF NOT EXISTS ORDER_DETAILS(
                        INVOICE_NUMBER TEXT,
                        PRODUCT_ID INTEGER,
                        QUANTITY INTEGER,
                        FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT(PRODUCT_ID),
                        FOREIGN KEY (INVOICE_NUMBER) REFERENCES USER(INVOICE)
                    );''')
connection.execute('''  CREATE TABLE IF NOT EXISTS ORDER_STATUS(
                        INVOICE_NUMBER TEXT,
                        DATE_TIME TEXT,
                        STATUS TEXT,
                        FOREIGN KEY (INVOICE_NUMBER) REFERENCES USER(INVOICE)
                    );''')


def add_user(type):
    while True:
        try:
            getname = input("Enter Name- ")
            regex = '[A-Za-z]{2,25}'
            if not(re.search(regex,getname)):
                print("Please enter a valid name")
                print("-----------------------------------------------------------------------------------")
                continue
            getemail = input("Enter Email id- ")
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if not(re.search(regex,getemail)):
                print("Please enter a valid email")
                print("-----------------------------------------------------------------------------------")
                continue
            cursor = connection.cursor()
            query = "SELECT * FROM USER WHERE EMAIL='"+ getemail +"'"
            result = cursor.execute(query).fetchall()
            if len(result)>0:
                print("The email already exist try with a different email")
                print("-----------------------------------------------------------------------------------")
                continue
            getPhone = input("Enter phone number- ")
            regex = "[6-9][0-9]{9}"
            if not(re.search(regex,getPhone)):
                print("Please enter a valid phone number")
                print("-----------------------------------------------------------------------------------")
                continue
            getpassword = input("Enter a password- ")
            confirmpassword = input("Confirm password- ")
            if getpassword != confirmpassword:
                print("Password don't match try again")
                print("-----------------------------------------------------------------------------------")
                continue
            getType = int(type)
            connection.execute("INSERT INTO USER (USER_NAME,USER_PASSWORD,ACCOUNT_TYPE,PHONE_NUMBER,EMAIL) VALUES('"+ getname +"','"+ getpassword +"',"+ str(getType) +",'"+getPhone+"','"+ getemail +"')")
            connection.commit()
            print("Entry Successful")
            print("-----------------------------------------------------------------------------------")
            query = "SELECT USER_ID FROM USER WHERE EMAIL='"+ getemail +"'"
            result = cursor.execute(query).fetchall()
            if getType == 1:
                print("======================== Login Successful ========================")
                user(result[0][0])
            elif getType == 2:
                print("======================== User added Successfully ========================")
            break
        except e:
            print(e)

def update_user(userid):
    print("What would you like to edit:- ")
    print("-----------------------------------------------------------------------------------")
    print("1. Name")
    print("2. Password")
    print("3. Email")
    print("4. Phone Number")
    print("5. Go Back")
    print("-----------------------------------------------------------------------------------")
    choice=int(input("Enter your choice- "))
    while True:
        if choice == 1:
            getname = input("Enter Name- ")
            regex = '[A-Za-z]{2,25}'
            if not(re.search(regex,getname)):
                print("Please enter a valid name")
                print("-----------------------------------------------------------------------------------")
                continue
            else:
                connection.execute("UPDATE USER SET USER_NAME='"+ getname +"' WHERE USER_ID="+ userid)
                connection.commit()
                break
        elif choice == 2:
            getpassword = input("Enter a password- ")
            confirmpassword = input("Confirm password- ")
            if getpassword != confirmpassword:
                print("Password don't match try again")
                print("-----------------------------------------------------------------------------------")
                continue
            else:
                connection.execute("UPDATE USER SET USER_PASSWORD='"+ getpassword +"' WHERE USER_ID="+ str(userid))
                connection.commit()
                break
        elif choice == 3:
            getemail = input("Enter Email id- ")
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if not(re.search(regex,getemail)):
                print("Please enter a valid email")
                print("-----------------------------------------------------------------------------------")
                continue
            cursor = connection.cursor()
            query = "SELECT * FROM USER WHERE EMAIL='"+ getemail +"'"
            result = cursor.execute(query).fetchall()
            if len(result)>0:
                print("The email already exist try with a different email")
                print("-----------------------------------------------------------------------------------")
                continue
            else:
                connection.execute("UPDATE USER SET EMAIL='"+ getemail +"' WHERE USER_ID="+ str(userid))
                connection.commit()
                break
        elif choice == 4:
            getPhone = input("Enter phone number- ")
            regex = "[6-9][0-9]{9}"
            if not(re.search(regex,getPhone)):
                print("Please enter a valid phone number")
                print("-----------------------------------------------------------------------------------")
                continue
            else:
                connection.execute("UPDATE USER SET PHONE_NUMBER='"+ getPhone +"' WHERE USER_ID="+ str(userid))
                connection.commit()
                break
        elif choice == 5:
            return
        else:
            print("Please Enter a correct value")

def inventory(userid):
    while True:
        print("Select an option from the Menu:- ")
        print("-----------------------------------------------------------------------------------")
        print("1. View Product")
        print("2. View Products with low stock")
        print("3. Add Product")
        print("4. Edit Product")
        print("5. Delete Product")
        print("6. Edit your details")
        print("7. Back to Main Menu")
        print("-----------------------------------------------------------------------------------")
        choice=int(input("Enter your choice- "))
        if choice == 1:
            result = connection.execute("SELECT p.PRODUCT_ID,p.NAME,p.COST,p.STOCK FROM PRODUCT p ")
            table = PrettyTable(["PRODUCT-ID","PRODUCT NAME","COST","QUANTITY IN STOCK"])
            for i in result:
                table.add_row([i[0],i[1],i[2],i[3]])
            print(table)
            print("-----------------------------------------------------------------------------------")
        elif choice == 2:
            result = connection.execute("SELECT p.PRODUCT_ID,p.NAME,p.COST,p.STOCK FROM PRODUCT p WHERE p.STOCK < 15")
            table = PrettyTable(["PRODUCT-ID","PRODUCT NAME","COST","QUANTITY IN STOCK"])
            for i in result:
                table.add_row([i[0],i[1],i[2],i[3]])
            print(table)
            print("-----------------------------------------------------------------------------------")
        elif choice == 3:
            getname = input("Enter the name of the product- ")
            getcost = input("Enter the cost of the product- ")
            getstock = input("Enter the stock available- ")
            connection.execute("INSERT INTO PRODUCT (NAME,COST,STOCK) VALUES('"+ getname +"',"+ getcost +","+ getstock +")")
            connection.commit()
        elif choice == 4:
            getid=input("Please enter the id of the product you want to edit-")
            print("What would you like to edit-")
            print("-----------------------------------------------------------------------------------")
            print("1. Product Name")
            print("2. Product Cost")
            print("3. Stock available")
            print("-----------------------------------------------------------------------------------")
            c=int(input("Enter your choice- "))
            if c == 1:
                getvalue=input("Enter the updated value- ")
                connection.execute("UPDATE PRODUCT SET NAME='"+ getvalue +"' WHERE PRODUCT_ID="+ getid)
                connection.commit()
            elif c == 2:
                getvalue=input("Enter the updated value- ")
                connection.execute("UPDATE PRODUCT SET COST='"+ getvalue +"' WHERE PRODUCT_ID="+ getid)
                connection.commit()
            elif c == 3:
                getvalue=input("Enter the updated value- ")
                connection.execute("UPDATE PRODUCT SET STOCK='"+ getvalue +"' WHERE PRODUCT_ID="+ getid)
                connection.commit()
            else:
                print("incorrect choice")
        elif choice == 5:
            getid=input("Please enter the id of the product you want to delete-")
            connection.execute("DELETE FROM PRODUCT WHERE PRODUCT_ID="+ getid)
            connection.commit()
            print("Deleted Successfully")
            print("-----------------------------------------------------------------------------------")
        elif choice == 6:
            update_user(userid)
        elif choice == 7:
            return
        else:
            print("Please Enter a correct value")

def user(userid):
    while True:
        print("Select an option from the Menu:- ")
        print("-----------------------------------------------------------------------------------")
        print("1. View Product")
        print("2. Purchase Product")
        print("3. View Purchase History")
        print("4. Update your details")
        print("5. Back to Main Menu")
        print("-----------------------------------------------------------------------------------")
        choice=int(input("Enter your choice- "))
        if choice == 1:
            result = connection.execute("SELECT p.PRODUCT_ID,p.NAME,p.COST FROM PRODUCT p")
            table = PrettyTable(["PRODUCT-ID","PRODUCT NAME","COST"])
            for i in result:
                table.add_row([i[0],i[1],i[2]])
            print(table)
            print("-----------------------------------------------------------------------------------")
        elif choice == 2:
            cart(userid)
        elif choice == 3:
            result = connection.execute("SELECT i.INVOICE_NUMBER,p.NAME,p.COST,i.QUANTITY,(p.COST*i.QUANTITY) AS TOTAL_AMOUNT FROM  INVOICE i LEFT JOIN USER u ON i.USER_ID=u.USER_ID LEFT JOIN PRODUCT p ON i.PRODUCT_ID=p.PRODUCT_ID WHERE u.USER_ID='"+str(userid)+"'")
            table = PrettyTable(["INVOICE_NUMBER","PRODUCT NAME","COST","QUANTITY","TOTAL_AMOUNT"])
            for i in result:
                table.add_row([i[0],i[1],i[2],i[3],i[4]])
            print(table)
            print("-----------------------------------------------------------------------------------")
        elif choice == 4:
            update_user(userid)
        elif choice == 5:
            return
        else:
            print("Please Enter a correct value")

def admin():
    while True:
        print("Select an option from the Menu:- ")
        print("-----------------------------------------------------------------------------------")
        print("1. View Users")
        print("2. Add Users")
        print("3. Delete User")
        print("4. Password reset")
        print("5. Back to Main Menu")
        print("-----------------------------------------------------------------------------------")
        choice=int(input("Enter your choice- "))
        if choice == 1:
            result = connection.execute("Select * FROM USER WHERE ACCOUNT_TYPE != 0")
            table = PrettyTable(["USER NAME","USER TYPE","PHONE NUMBER","EMAIL"])
            for i in result:
                if i[3] == 1:
                    type="USER"
                elif i[3] == 2:
                    type="INVENTORY MANAGER"
                table.add_row([i[1],type,i[4],i[5]])
            print(table)
            print("-----------------------------------------------------------------------------------")
        elif choice == 2:
            add_user(2)
        elif choice == 3:
            getid = input("Enter the users id you wish to delete- ")
            connection.execute("DELETE FROM USER WHERE USER_ID="+getid)
            connection.commit()
            print("Deleted Successfully")
            print("-----------------------------------------------------------------------------------")
        elif choice == 4:
            getid = input("Enter the users id you wish to reset- ")
            connection.execute("UPDATE USER SET USER_PASSWORD='12345' WHERE USER_ID="+ getid)
            connection.commit()
            print("Reset Successfully")
            print("-----------------------------------------------------------------------------------")
        elif choice == 5:
            return
        else:
            print("Please Enter a correct value")

def cart(userid):
    cart=[]
    item={"Product-id":0,"quantity":0}
    while True:
        print("Select an option from the Menu:- ")
        print("-----------------------------------------------------------------------------------")
        print("1. Add item to Cart")
        print("2. View Cart")
        print("3. Delete Item")
        print("4. Check out")
        print("5. Back to Main Menu")
        print("-----------------------------------------------------------------------------------")
        choice=int(input("Enter your choice- "))
        if choice == 1:
            while True:
                getid = input("Enter the product id you would like to purchase- ")
                cursor = connection.cursor()
                query = "SELECT p.PRODUCT_ID,p.NAME,p.COST FROM PRODUCT p WHERE PRODUCT_ID="+ getid
                result = cursor.execute(query).fetchall()
                if len(result)>0:
                    table = PrettyTable(["PRODUCT-ID","PRODUCT NAME","COST"])
                    for i in result:
                        table.add_row([i[0],i[1],i[2]])
                    print(table)
                    print("-----------------------------------------------------------------------------------")
                    print("1. Confirm")
                    print("2. Select again")
                    print("3. Back")
                    c=int(input("Enter the choice-"))
                    if c==1:
                        getquantity = input("Enter the quantity- ")
                        query = "SELECT p.STOCK FROM PRODUCT p WHERE PRODUCT_ID="+ getid
                        result = cursor.execute(query).fetchall()
                        stock = result[0][0]
                        if int(stock) < int(getquantity):
                            print("The item is out of stock")
                            continue
                        else:
                            incart=False
                            for i in cart:
                                if i["Product-id"] == getid:
                                    i["quantity"]=i["quantity"]+int(getquantity)
                                    incart=True
                            if not incart:
                                item["Product-id"]=getid
                                item["quantity"]=int(getquantity)
                                cart.append(item)
                            print("ITEM ADDED SUCCESSFULLY")
                            print("-----------------------------------------------------------------------------------")
                            break
                    elif c==2:
                        continue
                    elif c==3:
                        break
                    else:
                        print("Enter a correct choice")
                else:
                    print("Wrong ID item not found")
                    print("-----------------------------------------------------------------------------------")

        elif choice == 2:
            if len(cart)>0:
                total=0
                table = PrettyTable(["PRODUCT-ID","PRODUCT NAME","COST","QUANTITY","AMOUNT"])
                for i in cart:
                    query = "SELECT p.NAME,p.COST FROM PRODUCT p WHERE PRODUCT_ID="+ i["Product-id"]
                    result = cursor.execute(query).fetchall()
                    for r in result:
                        table.add_row([i["Product-id"],r[0],r[1],i["quantity"],int(i["quantity"])*int(r[1])])
                        total=total+(int(i["quantity"])*int(r[1]))

                print(table)
                print("Total ammount = ",total)
            else:
                print("The Cart is empty")
        elif choice == 3:
            if len(cart)>0:
                Exit = False
                while not Exit:
                    incart=False
                    getid = input("Enter the product id you would like to remove- ")
                    for i in cart:
                        if i["Product-id"] == getid:
                            incart=True
                            query = "SELECT p.PRODUCT_ID,p.NAME,p.COST FROM PRODUCT p WHERE PRODUCT_ID="+ getid
                            result = cursor.execute(query).fetchall()
                            if len(result)>0:
                                table = PrettyTable(["PRODUCT-ID","PRODUCT NAME","COST"])
                                for r in result:
                                    table.add_row([r[0],r[1],r[2]])
                                    print(table)
                                print("-----------------------------------------------------------------------------------")
                                print("1. Confirm")
                                print("2. Select again")
                                c=int(input("Enter the choice-"))
                                if c==1:
                                    getquantity = input("Enter the quantity- ")
                                    if i["quantity"]<=int(getquantity):
                                        i["quantity"] = 0
                                        cart.remove(i)
                                    else:
                                        i["quantity"]=i["quantity"]-int(getquantity)
                                    Exit = True
                                    print("ITEM REMOVED SUCCESSFULLY")
                                    print("-----------------------------------------------------------------------------------")
                                elif c==2:
                                    incart=True
                                    break

                                else:
                                    print("Enter a correct choice")
                    if not incart:
                        Exit = True
                        print("Item not in cart")
                        print("-----------------------------------------------------------------------------------")
            else:
                print("The Cart is empty")
        elif choice == 4:
            if len(cart)>0:
                cursor = connection.cursor()
                query = "Select COUNT(*) FROM INVOICE"
                result = cursor.execute(query).fetchall()
                invoice_id = "UON"+datetime.datetime.now().strftime("%Y%m%d%H%M")+str(result[0][0])
                connection.execute("INSERT INTO INVOICE (INVOICE_NUMBER,USER_ID) VALUES ('"+ invoice_id +"','"+ str(userid) +"')")
                connection.commit()
                cursor = connection.cursor()

                for i in cart:
                    connection.execute("INSERT INTO ORDER_DETAILS(INVOICE_NUMBER,PRODUCT_ID,QUANTITY) VALUES('"+ invoice_id +"','"+ str(i["Product-id"])+"','"+ str(i["quantity"]) +"')")
                    connection.commit()
                    query = "SELECT p.STOCK FROM PRODUCT p WHERE PRODUCT_ID="+ i["Product-id"]
                    result = cursor.execute(query).fetchall()
                    getvalue= int(result[0][0])-int(i["quantity"])
                    connection.execute("UPDATE PRODUCT SET STOCK='"+ str(getvalue) +"' WHERE PRODUCT_ID="+ i["Product-id"])
                    connection.commit()
                viewbill(invoice_id,userid)
                return
            else:
                print("The Cart is empty")

        elif choice == 5:
            return
        else:
            print("Please Enter a correct value")

def viewbill(invoice_id,userid):
    total=0
    cursor = connection.cursor()
    query = "SELECT USER_NAME FROM USER WHERE USER_ID='"+ str(userid) +"'"
    result = cursor.execute(query).fetchall()
    date=datetime.datetime(int(invoice_id[3:7]),int(invoice_id[7:9]),int(invoice_id[9:11]),int(invoice_id[11:13]),int(invoice_id[13:15])).strftime("%d-%m-%Y  %H:%M")
    print("###################################################################################")
    print("Invoice Number- ",invoice_id)
    print("User Name- ",result[0][0])
    print("Date and Time- ",date)
    print("-----------------------------------------------------------------------------------")
    table = PrettyTable(["PRODUCT NAME","COST","QUANTITY","AMOUNT"])
    query = "SELECT p.NAME,p.COST,o.QUANTITY,(o.QUANTITY*p.COST) FROM PRODUCT p LEFT JOIN ORDER_DETAILS o ON p.PRODUCT_ID=o.PRODUCT_ID WHERE o.INVOICE_NUMBER="+ invoice_id
    result = cursor.execute(query).fetchall()
    for i in result:
        table.add_row([i[0],i[1],i[2],i[3]])
        total=total+int(i[3])
    print(table)
    print("-----------------------------------------------------------------------------------")
    print("Total bill ammount = ",total)
    print("###################################################################################")




while True:
    print("Select an option from the Menu:- ")
    print("-----------------------------------------------------------------------------------")
    print("1. Login")
    print("2. Register")
    print("3. Help")
    print("4. Exit")
    print("-----------------------------------------------------------------------------------")
    choice=int(input("Enter your choice- "))
    #login
    if choice == 1:
        while True:
            getemail = input("Enter your email- ")
            getpassword = input("Enter your password- ")
            cursor = connection.cursor()
            query = "SELECT * FROM USER WHERE EMAIL='"+ getemail +"'"
            result = cursor.execute(query).fetchall()
            if len(result) == 0:
                print("The email does not exist")
                print("-----------------------------------------------------------------------------------")
                continue
            if result[0][2]!=getpassword:
                print("Wrong password try again")
                print("-----------------------------------------------------------------------------------")
                continue
            if result[0][3] == 1:
                print("======================== Login Successful ========================")
                user(result[0][0])
            elif result[0][3] == 2:
                print("======================== Login Successful ========================")
                inventory(result[0][0])
            elif result[0][3] == 0:
                print("======================== Login Successful ========================")
                admin()
            break
    #Register
    elif choice == 2:
        add_user(1)
    elif choice == 3:
        print("For any queries and password reset please mail at:- admin@123.com")
    elif choice == 4:
        break
    else:
        print("Please Enter a correct value")
    #Exit
