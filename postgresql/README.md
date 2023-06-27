# Additional steps to use a local PostgreSQL instance.

## Set up local PostgreSQL instance
* Local PostgreSQL with the required extensions installed, an admin console (Adminer) and PostgREST (with Swagger)
```bash
docker compose -f docker-compose-postgresql.yml up --build 
```
* Once the containers are up, you can access Adminer Console at http://localhost:9090.

## Create a named schema for quivr
1. Execute below script
```sql
create schema quivr;
```
2. Remove the public schema.
3. Set the named schema created above as the default schema.

## Run the following migration scripts on the database in the `quivr` schema, via Adminer
[Creation Script 1](../scripts/tables.sql)

## Setting up PostgREST
### Setting up permissions
> **NOTE:** We'll be setting up an anonymous user that can perform all CRUD operations. To setup separate users for different operations, refer to [PotgREST documentation](https://postgrest.org/en/stable/index.html).

Execute the below SQL queries.
```sql
-- Authenticator role that can impersonate
create role authenticator noinherit login password 'mysecretpassword';

-- Anonymous user with read-write permissions
create role quivr_anon nologin;

grant usage on schema quivr to quivr_anon;
grant all on quivr.chats to quivr_anon;
grant all on quivr.stats to quivr_anon;
grant all on quivr.summaries to quivr_anon;
grant all on quivr.users to quivr_anon;
grant all on quivr.vectors to quivr_anon;

grant quivr_anon to authenticator;
```
> **NOTE:** The anonymous user created in the SQL scripts, `quivr_anon` is passed as an environment variable to PostgREST in the `docker-compose-postgresql.yml` Docker Compose file. If you change the user, make the change in the Compose file as well.

### Accessing the REST endpoints
The PostgREST Swagger endpoint is now available at http://localhost:8080.

The PostgREST server is available at http://localhost:4000. Accessing the _root_ endpoint will list all the APIs being served by PostgREST.ds
