import database

connection, cursor = database.connect_to_database()

listar = database.listar_monitores(cursor)
for monitor in listar:
    print(monitor)

database.adicionar_monitor(cursor, connection, "11987654321", [1,3,4], "João Silva", "jsilva@gmail.com")
database.adicionar_monitor(cursor, connection, "11987654322", [2,4,5], "Maria Oliveira", "maria.oliveira@gmail.com")

listar = database.listar_monitores(cursor)
print(listar)
for monitor in listar:
    print(monitor)

database.close_database_connection(connection, cursor)