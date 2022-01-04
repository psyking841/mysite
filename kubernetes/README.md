## Deploy in Kubernetes
```
kubectl apply -f ./postgres-deployment.yaml

kubectl apply -f ./web-deployment.yaml
```


Login to db pod and run
```commandline
kubectl exec -it postgres-c84d65d45-ccf9n -- /bin/bash
```
Then

```commandline
psql postgres postgres
```

Then 
```sql
CREATE TABLE public."newsfeed"
(
    "ID" SERIAL,
    news_source character varying COLLATE pg_catalog."default",
    title character varying COLLATE pg_catalog."default",
    link character varying COLLATE pg_catalog."default",
    description character varying COLLATE pg_catalog."default",
    pub_date timestamp with time zone,
    article_type character varying COLLATE pg_catalog."default",
    language character varying COLLATE pg_catalog."default",
    sentiment character varying COLLATE pg_catalog."default",
    CONSTRAINT "newsfeed_pkey" PRIMARY KEY ("ID")
)
```

ALso need to add the node's public ID (go to the cloud console to see it) in the `DJANGO_ALLOWED_HOSTS`. 

## Run with crawler
1. Deploy DB in cluster
2. Deploy crawler into cluster (this is another project). It will create a table call `theora_newsfeed` table in DB.
3. Deploy web app in cluster
