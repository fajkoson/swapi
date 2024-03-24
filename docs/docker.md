# Docker guide:
- Download Docker:
➡ https://www.docker.com/products/docker-desktop/ ⬅
### NOTE: dont forget to enable virtualisation in BIOS.

## How to create container:
```
1. docker --version
2. docker run hello-world 
3. create image (call it from the root folder of the project where Dockerfile is)
docker build -t swapidocker .
4. create kontainer
docker run --name swapicontainer -d swapidocker
5. check status of your container 
docker ps -a
6. check console output of the container 
docker logs swapicontainer
7. stop the container
docker stop swapicontainer
8. remove container when no longer needed 
docker rm swapicontainer
9. remove image when no longer needed
docker rmi swapidocker
```
