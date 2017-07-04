Inqubo demo
============
Docker-compose enabled demo for inqubo automated workflow runner  
https://github.com/domasx2/inqubo  
https://github.com/domasx2/inqubo-ui

## Run
Requires docker & docker-compose to run

```bash
# start rabbitmq, inqubo ui, generate_report & process_order mock services
docker-compose up

# start with multiple instances of mock services
docker-compose up --scale generate_report=3 --scale process_order=3
```
And open http://localhost:3000/
