CREATE TABLE `dptos`(
    'id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' text,
    'URL' text,
    'divisa' text, 
    'precio' INTEGER,
    'desc' text,
    'ubicacion' text,
    'source' text,
    'disponible' BOOLEAN DEFAULT 1,
    'fecha_creacion' date,
    'fecha_modificacion' date
)