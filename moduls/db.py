import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="change me",
    password="change me",
    database="demo_sql_injection"
)
mycursor = mydb.cursor()

def check_doub(user):
    mycursor.execute("SELECT * FROM users WHERE user = %s", (user,))
    if len(mycursor.fetchall()) == 1:
        return True
    else:
        return False
    
def check_login(user, passwd):
    mycursor.execute(
        "SELECT * FROM users WHERE user = %s AND password = %s", (user, passwd))
    myresult = mycursor.fetchall()
    if len(myresult) == 1:
        return True
    else:
        return False

def get_id(user,passwd):
    if check_login(user, passwd):
        mycursor.execute("SELECT id FROM users WHERE user = %s AND password = %s", (user,passwd))
        myresult = mycursor.fetchall()
        if len(myresult) == 1:
            id = myresult[0][0]
            return id
        
def get_info(id):
    mycursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    myresult = mycursor.fetchall()
    if len(myresult) == 1:
        return myresult[0]
    else:
        return False

def add_user(user, passwd):
    mycursor.execute("INSERT INTO users (user, password) VALUES (%s, %s)", (user, passwd))
    mydb.commit()

def update_info(id, passwd, decr,address):
    if passwd != '':
        mycursor.execute("UPDATE users SET password = '" +
                         passwd+"' WHERE id = '"+id+"'")
    if decr != '':
        print("UPDATE users SET decription = '" +
                         decr+"' WHERE id = '"+id+"'")
        mycursor.execute("UPDATE users SET decription = '" +
                         decr+"' WHERE id = '"+id+"'")
        
    if address != '':
        mycursor.execute("UPDATE users SET address = '" +
                         address+"' WHERE id = '"+id+"'")
    mydb.commit()
