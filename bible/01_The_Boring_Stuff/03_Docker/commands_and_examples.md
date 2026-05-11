# Docker: Commands And Examples

## Commands

```bash
docker build -t learning-bot:latest .
docker run --rm learning-bot:latest
docker ps
docker logs <container_id>
docker stop <container_id>
docker rm <container_id>
```

## Worked Example

```bash
docker build -t btc-tools .
docker run --rm btc-tools python src/data_loader.py
```
