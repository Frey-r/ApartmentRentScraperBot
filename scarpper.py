import pandas as pd
import sqlite3
import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_PATH, 'sql', 'bdd.db')
SQL_CREATE_PATH = os.path.join(BASE_PATH, 'sql', 'create.sql')
RESULTS_PATH = os.path.join(BASE_PATH, 'resultados','dptos.xlsx')
min_price = 1
max_price = 450000
URLS = [
    f'https://www.portalinmobiliario.com/arriendo/departamento/_DisplayType_M_OrderId_PRICE_PriceRange_{min_price}CLP-{max_price}CLP_NoIndex_True_item*location_lat:-33.44989281004803*-33.38426922283824,lon:-70.62558878061164*-70.49255121347296',
    f'https://www.portalinmobiliario.com/arriendo/departamento/_DisplayType_M_OrderId_PRICE_PriceRange_{min_price}CLP-{max_price}CLP_NoIndex_True_item*location_lat:-33.464620342562576*-33.448221880457425,lon:-70.58875006050337*-70.5554906687187',
    f'https://www.portalinmobiliario.com/arriendo/departamento/_DisplayType_M_OrderId_PRICE_PriceRange_{min_price}CLP-{max_price}CLP_NoIndex_True_item*location_lat:-33.48058616976933*-33.464190728099474,lon:-70.58943670601118*-70.55617731422652',
    f'https://www.portalinmobiliario.com/arriendo/departamento/_DisplayType_M_OrderId_PRICE_PriceRange_{min_price}CLP-{max_price}CLP_NoIndex_True_item*location_lat:-33.48986677432309*-33.48781773332511,lon:-70.65524582964187*-70.65108840566879'
]

def check_table():
    """
        Check if the table exists in the database
        If not, create it
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM dptos')
    except sqlite3.OperationalError:
        create_table()
    
def create_table():
    """
        Create the table in the database
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript(open(SQL_CREATE_PATH).read())
    conn.commit()
    conn.close()

def check_disponibilities(source, options):
    """
        Check if the options are in the database
        If not, set them to False
        If they are, set them to True
        :param source: the source of the options
        :param options: the options to check (departments)
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    current_names = []
    c.execute('SELECT id, name FROM dptos WHERE source=? AND disponible=1', (source,))
    db_records = c.fetchall()
    if len(db_records) == 0:
        conn.close()
        return
    for option in options:
        name = option.text.split('\n')[0]
        current_names.append(name)
    for record in db_records:
        if record[1] not in current_names:
            c.execute('UPDATE dptos SET disponible=0 WHERE id=?', (record[0],))
    conn.commit()
    conn.close()    

def insert_departament(name, url, divisa, precio, desc, ubicacion, source):
    """
        Insert a department in the database
        :param name: the name of the department
        :param url: the url of the department
        :param divisa: the currency of the department
        :param precio: the price of the department
        :param desc: the description of the department
        :param ubicacion: the location of the department
        :param source: the source of the department
    """
    conn = sqlite3.connect(DB_PATH)
    check_table()
    c = conn.cursor()
    c.execute('SELECT * FROM dptos WHERE name=? and source=?', (name,source))
    if c.fetchone() is None:
        c.execute('''
            INSERT INTO dptos (name, URL, divisa, precio, desc, ubicacion, source, fecha_creacion, fecha_modificacion) 
            VALUES (?,?,?,?,?,?,?,?,?)
            ''', (name, url, divisa, precio, desc, ubicacion, source, time.strftime('%Y-%m-%d'), time.strftime('%Y-%m-%d')))
    else:
        c.execute('''
            UPDATE dptos 
            SET name=?, URL=?, divisa=?, precio=?, desc=?, ubicacion=?, source=?, fecha_creacion=?, fecha_modificacion=? 
            WHERE name=? AND source=?
            ''', (name, url, divisa, precio, desc, ubicacion, source, time.strftime('%Y-%m-%d'), time.strftime('%Y-%m-%d'), name, source))
    conn.commit()
    conn.close()

def scrap(urlSource,isToExcel = False):
    """
        Scrap the departments from the urlSource
        :param urlSource: the url of the departments
        :param isToExcel: if the departments should be saved in an excel file
    """
    DRIVER.get(urlSource)
    WebDriverWait(DRIVER, .5).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-search-map-list__item')))
    opciones = DRIVER.find_elements(By.CLASS_NAME, 'ui-search-map-list__item')
    check_table()
    check_disponibilities(urlSource, opciones)
    for opcion in opciones:
        text = opcion.text.split('\n')
        url = opcion.find_elements(By.CLASS_NAME,'ui-search-result__main-image-link')[0].get_attribute('href')
        name = text[0]
        divisa = text[1]
        precio = text[2]
        desc = text[3]
        ubicacion = text[4]
        if text[3].split(' ')[0] == 'Publicado':
            desc = text[4]
            ubicacion = text[5]
        insert_departament(name, url, divisa, precio, desc, ubicacion, urlSource)
    #to excel
    if isToExcel:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query('SELECT * FROM dptos where disponible=1', conn)
        df.to_excel(RESULTS_PATH,index=False)
        conn.close()


if __name__ == '__main__':
    isToExcel = True if input('Save the results in an excel file? (y/n)\n- ').upper() == 'Y' else False
    DRIVER = webdriver.Firefox()
    for url in URLS:
        scrap(url,isToExcel = isToExcel)
        print(f'Scrapped {url}')
    print('waiting for the driver to close')
    DRIVER.quit()
    print('Done')
    