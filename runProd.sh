
#!/bin/bash
docker build -f Dockerfile.prod -t vm_docker_flask .
docker run -d --name my_container_flask -p 5000:5000 vm_docker_flask