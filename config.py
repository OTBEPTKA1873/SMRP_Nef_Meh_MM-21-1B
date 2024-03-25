DB_USER = "admin"
DB_PASSWORD = "31415"
DB_HOST = "localhost"  # вместо localhost ip к хосту
DB_PORT = 5432
DB_NAME = "components_db"

# Для создания контейнера: docker run --name ComponentsBase -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=31415 -e POSTGRES_DB=components_db -p 5432:5432 -d postgres
