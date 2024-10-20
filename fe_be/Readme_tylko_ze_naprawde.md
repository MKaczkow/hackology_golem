project id: hackology-439121


# Local

```
docker build -f docker/Dockerfile.service -t sevice .
```

```
docker build -f docker/Dockerfile.app -t app .
```
AGENT_URL

```
docker build -f docker/Dockerfile.service -t service --build-arg OPENAI_API_KEY=<> .

```

```
docker build -f docker/Dockerfile.app -t app --build-arg AGENT_URL=localhost:80 .
```



```
docker run -d -p 80:80 --name agent_service service

docker run -d -p 80:80 --name agent_service_v2 --env OPENAI_API_KEY=<> service

```


```
docker run -d -p 8502:8501 --name streamlit_app --env AGENT_URL=http://localhost:80 app

```

# GCP

build image:

```
docker build -f docker/Dockerfile.service -t gcr.io/hackology-439121/agent-service .

```

docker build -f docker/Dockerfile.service -t service_local --build-arg OPENAI_API_KEY=sk-<> .

docker run service_local --env OPENAI_API_KEY=<>


# GCP frfr

docker build --platform linux/amd64 -f docker/Dockerfile.service -t service --build-arg OPENAI_API_KEY=<> .

docker build --platform linux/amd64 -f docker/Dockerfile.app -t app .


docker tag service gcr.io/hackology-439121/agent-service

docker tag app gcr.io/hackology-439121/streamlit-app


docker push gcr.io/hackology-439121/agent-service

docker push gcr.io/hackology-439121/streamlit-app


https://agent-service-13471092088.europe-north1.run.app