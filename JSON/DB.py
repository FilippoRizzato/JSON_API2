import mysql.connector
import json

def read_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key.strip()] = value.strip()
    return config

def get_connection():
    config = read_config('config.txt')
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    return cursor, conn


    
def get_product_by_id(product_id):
    cursor, conn = get_connection()
    cursor.execute("SELECT * FROM rizzato_filippo_API.products WHERE id = %s", (product_id, ))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    return product
def get_all():
    cursor, conn = get_connection()
    cursor.execute("SELECT * FROM rizzato_filippo_API.products")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return  results
def insert(marca, nome, prezzo):
    cursor, conn = get_connection()
    cursor.execute("insert into rizzato_filippo_API.products(nome, prezzo, marca)values (%s, %s, %s)", (nome, prezzo, marca,))
    conn.commit()
    cursor.close()
    conn.close()
    product = get_product_by_id(cursor.lastrowid)
    return product

def delete(id):
    ricerca =  get_product_by_id(id)
    print(ricerca)
    if ricerca:
        query = "DELETE FROM rizzato_filippo_API.products WHERE id = %s"
        bind = (str(id),)
        cursor, conn = get_connection()
        cursor.execute(query, bind)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return True
    else:
        return False
# creo un metodo per ogni verbo
def update(product_id, data):
    cursor, conn = get_connection()  
    cursor.execute("UPDATE rizzato_filippo_API.products SET nome = %s, marca = %s, prezzo = %s WHERE id = %s", (data["data"]["attributes"]['nome'], data["data"]["attributes"]["marca"], data["data"]["attributes"]["prezzo"], product_id, ))
    conn.commit()
    cursor.close()
    conn.close()
    product = get_product_by_id(product_id)
    return product
    

    

    
if __name__ == "__main__":
    get_product_by_id(5)
    get_all()