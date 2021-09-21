This testing project relies on `docker-compose` and `JDK` locally.

The python scripts are to generate PSR data for 15 operators. Usually, it takes around 10 minutes to insert all data into DB. We can comment out some operators to generate less data.

# Config

Majority of configuration can be found at `docker-compose.yml` as container environment variables. 

## How to generate

```
docker-compose up -d postgres mysql mariadb
```

then run

```
docker-compose run generator 
```

## login DB in console

### MySQL

```
docker exec -it psr_data_benchmark_mysql_1  /bin/bash -c "mysql psr -u someone -p"
```
password: `passme`

### MariaDB

```
docker exec -it psr_data_benchmark_mariadb_1  /bin/bash -c "mysql psr -u someone -p"
```
password: `passme`

### PostgreSQL

```
docker exec -it psr_data_benchmark_postgres_1 /bin/bash -c "psql postgres postgres"
```

## Testing

To compile testing jar, execute command under `consumer` folder

```
./sbt assembly
```

The fat jar `testing.jar` will be built under `consumer/target/scala_2.13/`.

Then execute command at root

```
docker-compose run consumer 
```