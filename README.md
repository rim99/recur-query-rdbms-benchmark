This script is to generate PSR data for 15 operators. Usually, it takes around 10 minutes to insert all data into DB. We can comment out some operators if we want to generate less data.

## How to generate

```
docker-compose start postgres mysql 
```

then run

```
docker-compose run generator 
```


## login in console

### MySQL

```
mysql psr -u someone -p
```
password: `passme`

### PostgreSQL

```
psql postgres postgres
```