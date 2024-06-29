# T2V-Serve ![Docker Image Version](https://img.shields.io/docker/v/egordm/t2v-serve)

A simple webserver for serving embeddings using a huggingface model.

* Compatible with weaviate
* Uses sentence embeddings under the hood (tried with onnx, but didn't get a performance boost)
* Has a batch embedding endpoint for faster processing
* Support for GPU's

## Usage
```bash
docker run -it -p 8080:8080 --gpus all egordm/t2v-serve:bge-base-en-v1.5
```

Example in docker compose:
```yaml
  embeddings-service:
    image: egordm/t2v-serve:bge-base-en-v1.5
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [ gpu ]
```

Then just make your requests
```http request
###
POST localhost:8080/vectors
Content-Type: application/json

{
    "text": "I am a sentence for which I would like to get its embedding."
}

###
POST localhost:8080/vectors/batch
Content-Type: application/json

[
  {
    "text": "I am a sentence for which I would like to get its embedding.z"
  },
  {
    "text": "I am a sentence for which I would like to get its embedding."
  },
  {
    "text": "I am a sentence for which I would like to get its embedding."
  }
]
```

## Configuration
Supported environment variables:
* `MODEL_NAME`: The name of the model to use. Default: `BAAI/bge-base-en-v1.5`
* `BATCH_SIZE`: The batch size to use for the batch endpoint. If a bigger batch is posted, it is split up. Default: `64`
* `USE_GPU`: Noop for now. If there is a GPU available, it will be used. Default: `False`