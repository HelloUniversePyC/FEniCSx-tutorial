# fenicsxtutorial practice

## Sources
[Medium Tutorial](https://medium.com/@abolfazl.dmg/topology-optimization-with-fenicsx-a-step-by-step-guide-b603a237dd61)


# Docker Build
```bash
docker compose build --no-cache
```
# Start Docker Container
```bash
docker compose up -d
```

# Run Code in Docker Shell 
```bash
docker compose exec fenicsxtutorial bash
```
Now you can run any files/command normally within an interactive shell

# Run Jupter Notebook file
```bash
docker compose run --rm fenicsxtutorial python3 src/problems/<file_name>
```

# Debugging
```bash
docker compose ps
```
Inspect Running Container Status
