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
docker build -f docker/Dockerfile.service -t service --build-arg OPENAI_API_KEY=sk-eFGTf_3Yr4CEI8p_iaVQeSMfUkxGDggpjxFJW1roq0T3BlbkFJnlGhvwqgqzXGNz_jkY_BtRpfJP2qO5f3DQRRsc7CkA .

```

```
docker build -f docker/Dockerfile.app -t app --build-arg AGENT_URL=localhost:80 .
```



```
docker run -d -p 80:80 --name agent_service service

docker run -d -p 80:80 --name agent_service_v2 --env OPENAI_API_KEY=sk-eFGTf_3Yr4CEI8p_iaVQeSMfUkxGDggpjxFJW1roq0T3BlbkFJnlGhvwqgqzXGNz_jkY_BtRpfJP2qO5f3DQRRsc7CkA service

```


```
docker run -d -p 8502:8501 --name streamlit_app --env AGENT_URL=http://localhost:80 app

```

# GCP

build image:

```
docker build -f docker/Dockerfile.service -t gcr.io/hackology-439121/agent-service .

```