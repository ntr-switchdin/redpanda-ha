# RedPanda HA Demo

```sh
docker compose up

```

wait for messaging to start...
look for: `Leader Broker ID: {id}`
then shoot the messenger

```sh
docker compose stop redpanda-{id}

```

In a minute or so the consumer should move to the new leader and catch up all the msgs it missed


## TODO
- gotta be careful of dev mode auto topic creation because it can race and create a topic with 1 replica
