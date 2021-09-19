This script is to generate PSR data for 15 operators. Usually, it takes around 10 minutes to insert all data into DB. We can comment out some operators if we want to generate less data.

## How to generate

```
docker-compose up postgres mysql -d
```

then run

```
docker-compose up generator 
```


## login DB in console

### MySQL

```
docker exec -it psr_data_benchmark_mysql_1  /bin/bash -c "mysql psr -u someone -p"
```
password: `passme`

### PostgreSQL

```
docker exec -it psr_data_benchmark_postgres_1 /bin/bash -c "psql postgres postgres"
```