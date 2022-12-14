# Sine Wave Simulator
A series of utilities to simulate multiple sine waves and visualize the
combination of waves and resulting spectrum.

## Starting

### Start Kafka
To start Kafka, first start docker desktop, then run the compose file:
```
cd simulator/broker
docker compose up .
```

### Start Simulating Sine Waves
Run the example:
```
python examples/example_combine.py
```

### Visualize
```
bokeh serve waves.py --show
```
