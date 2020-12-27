## Setup DB
Run Postgres DB:
```
docker run -d \
    --name my-postgres \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v /Users/shengyip/Workspace/mysite/db_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:12
```
Run PgAdmin:
```
docker run -p 80:80 \
     -e 'PGADMIN_DEFAULT_EMAIL=psyking841@gmail.com' \
     -e 'PGADMIN_DEFAULT_PASSWORD=mysecretpassword' \
     -d dpage/pgadmin4
```
For how to connect to service on the host machine from container, see [this page](https://docs.docker.com/docker-for-mac/networking/#use-cases-and-workarounds).
Basically, using `host.docker.internal` in stead of `localhost`.

To switch to postgres DB, using following settings:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        "HOST": 'localhost',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword'
    }
}
```
and init the db by running  
```
python manage.py migrate
```

## Apply changes to models
If you have changes to your models, run
```
python manage.py makemigrations
```
By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, you’ve made new ones) and that you’d like the changes to be stored as a migration.
For details, see [this link](https://docs.djangoproject.com/en/3.1/intro/tutorial02/#activating-models).
Then you can use either migrate or sqlmigrate to apply the changes.

## Admin portal
An `admin` account has already been created. The password is `mysecretpassword`.