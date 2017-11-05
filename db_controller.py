import sqlite3

def connection():
    return sqlite3.connect('nevera')

def close_connection(con):
    con.commit()
    con.close()

def request_products():
    con = connection()
    c = con.cursor()
    db_info = c.execute('SELECT nombre FROM productos')
    lista_productos = []
    for row in db_info:
        lista_productos.append(row[0])
    close_connection(con)
    print("LISTA DE PRODUCTOS: "+str(lista_productos))
    return lista_productos

def comprar(user_id,producto):
    con = connection()
    c = con.cursor()
    c.execute('SELECT precio FROM productos WHERE nombre=?',(producto,))
    db_info = c.fetchall()
    precio = db_info[0][0]
    print(precio)
    c.execute('SELECT dinero FROM Usuarios WHERE id=?',(user_id,))
    db_info = c.fetchall()
    dinero = round(db_info[0][0] - precio,2)
    c.execute('UPDATE Usuarios SET dinero = ? WHERE id=?',(dinero,user_id))
    close_connection(con)
    return dinero

def crear_usuario(user_id):
    con = connection()
    c = con.cursor()
    c.execute('INSERT INTO Usuarios VALUES (?,?)',(user_id,0.0))
    close_connection(con)

def get_dinero(user_id):
    con = connection()
    c = con.cursor()
    c.execute('SELECT dinero FROM Usuarios WHERE id=?',(user_id,))
    db_info = c.fetchall()
    dinero_usuario = db_info[0][0] 
    close_connection(con)
    return dinero_usuario

def add_dinero(user_id,cantidad):
    con = connection()
    c = con.cursor()
    c.execute('SELECT dinero FROM Usuarios WHERE id=?',(user_id,))
    db_info = c.fetchall()
    dinero_usuario = round(db_info[0][0] + cantidad,2)
    c.execute('UPDATE Usuarios SET dinero = ? WHERE id=?',(dinero_usuario,user_id))
    close_connection(con)
    return dinero_usuario
    


def is_registered(user_id):
    con = connection()
    c = con.cursor()
    c.execute('SELECT id FROM Usuarios WHERE id=?',(user_id,))
    db_info = c.fetchall()
    #print(db_info)
    if len(db_info) == 0:
        print('No existe el usuario {}'.format(user_id))
        close_connection(con)
        return False
    print('Existe el usuario con {}'.format(user_id))
    close_connection(con)
    return True

