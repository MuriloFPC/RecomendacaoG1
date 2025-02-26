Train the models
================



```
make train
```
or

```
python -m src.Models.Orchestrator
```

This will train the models and save them in the models directory.

Run the models
================

```
make run
```
or

```
python3 -m uvicorn src.Api.main:app --reload
```

This will start the server and you can access the API at http://localhost:8000

curl example:
```
POST http://127.0.0.1:8000/recomendation
Content-Type: application/json

{
  "newsId": "61e07f64-cddf-46f2-b50c-ea0a39c22050",
  "userId": "2c1080975e257ed630e26679edbe4d5c850c65f3e09f655798b0bba9b42f2110"
}
```