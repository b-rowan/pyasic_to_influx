# pyasic_to_influx

`pyasic_to_influx` is designed to be a simple, dockerized setup of a miner monitor using influxdb.

To start, make sure you have docker installed.

Once docker is installed, run with `docker compose up -d`.

Once the daemonized task is running, access it on `localhost:8086`.

The default username is `admin`, and the default password is `password123`.

All of this can be configured in `.env`.