## 1. Put your credentials into the .env file.

ACCESS_TOKEN=...
CONSUMER_KEY=...
CONSUMER_SECRET=...
ACCESS_TOKEN_SECRET=...

## 2. Create the vt image.
```terminal
docker build -t vt ./vistrends/
```

## 3. Run docker compose with docker-compose.yml.
```terminal
docker-compose up
```

## 4. You can have an access to the dynamic of data obtaining.
```terminal
http://localhost:8000/
```

### 5. You can see an image from database (image file must exist).
```terminal
http://localhost:11071/image?img=17:49:36_22.02.2019.png
```
