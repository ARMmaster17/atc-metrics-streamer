# Atc-Metrics-Streamer (AMS)
Send metrics from Traffic Ops to a Kafka topic for ingest into Logstash/Elasticsearch or any other platform of your choosing.

# Getting Started
## Setup (dev)
1. Ensure that you are running the latest version of Docker and Docker Compose, and you have at least 5 GB of RAM dedicated to your Docker instance.
2. Run the following:
```bash
git clone https://github.com/ARMmaster17/atc-metrics-streamer.git
export TO_SERVER=traffic-ops.example.com
export TO_USER=admin
export TO_PASSWORD=password
docker-compose up
```

## Setup (production)
1. Ensure that the following environment variables are set:

| Key           | Description                                                                                 |
|---------------|---------------------------------------------------------------------------------------------|
| KAFKA_SERVERS | Comma-separated list of Kafka FQDNs with port number (e.g. `kafka1:9200,kafka2:92000,...`). |
| KAFKA_TOPIC   | Kafka topic to write metrics.                                                               |
| TO_SERVER     | FQDN (no schema or port) of your Traffic Ops instance.                                      |
| TO_USER       | Username to authenticate with Traffic Ops.                                                  |
| TO_PASSWORD   | Password to authenticate with Traffic Ops.                                                  |

2. Build the container with `docker build -t atc-metrics-streamer .`
3. Run AMS with `docker run -d -e KAFKA_SERVERS -e KAFKA_TOPIC -e TO_SERVER -e TO_USER -e TO_PASSWORD atc-metrics-streamer`

# Usage
## Customizing Aggregated Metrics
To change what metrics get sent through to Kafka, you can edit `traffic_ops/MetricsDTO.py` and modify the constructor to add new metrics. For example, this is how you would track the metric `load_average`:

```python
self.__data['load_average'] = data['load_average']
```

Customizing these metrics through JSON/YAML is coming soon.