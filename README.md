## Setup DB
Run Postgres DB:
```
docker run -d \
    --name my-postgres \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v /Users/shengyip/Workspace/mysite/db_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
```
Run PgAdmin if you need UI:
```
docker run -p 80:80 \
     -e 'PGADMIN_DEFAULT_EMAIL=psyking841@gmail.com' \
     -e 'PGADMIN_DEFAULT_PASSWORD=mysecretpassword' \
     -d dpage/pgadmin4
```

For how to connect to service on the host machine from container, see [this page](https://docs.docker.com/docker-for-mac/networking/#use-cases-and-workarounds).
Basically, 
1. Go to localhost:80 in browser
2. Login PGAdmin using above credential in docker command
3. Create connection but using `host.docker.internal` in stead of `localhost` for host.
4. Username: postgres; password is in docker command.

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

## Build dockerfile
```
docker build -t psyking841/mysite:latest .
```

## Run docker compose
```
docker-compose -f docker-compose.yaml up -d
# tear down
# docker-compose -f docker-compose.yaml down
```

## Access IBM COS image via pre-signed URL
First, config [AWS CLI](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-uhc-hmac-credentials-main)
[Link](https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-presign-url)
Current iamge [private link](https://s3.private.us.cloud-object-storage.appdomain.cloud/cloud-object-storage-dsx-cos-standard-g57/me.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=66bf90ffef924a379679da395b5581aa%2F20220103%2Fus-east%2Fs3%2Faws4_request&X-Amz-Date=20220103T034608Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=3fd79c1b5c207884874aa95d8f72cc011694155ab89b15b48d0303ff562f5538)


# The whole process to deploy Theora
```
# DB
kubectl apply -f kubernetes/postgres-deployment.yaml

# Switch to crawler project - wsj-pipeline
kubectl apply -f kubernetes/deployment.yaml

# Switch to web project
kubectl apply -f kubernetes/web-deployment.yaml

# If using No-IP domain, remember to point that domain to the new IP.
```

If there is changes to the code, including changes to about me
```
# remove older image, if any, using `docker images`
docker rmi -f c0ed9c6e9198

# Build docker image and push to registry
docker build -t psyking841/mysite .
docker tag psyking841/mysite icr.io/shengyipan/mysite
docker push icr.io/shengyipan/mysite

# deploy k8s
```