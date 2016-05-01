# Subway Sounds

This repository contains code for the real-time story Subway Sounds, completed for the class Storytelling with Streaming Data at Columbia University in Spring 2016.

## Dependencies

### System dependencies

This project has two non-standard dependencies:

- [Redis](http://redis.io/)
- [websocketd](http://websocketd.com/)

Please install these before attempting to run this locally. This project was developed using Redis version 3.0.5 and websocketd 0.2.11. We cannot guarantee compatibility with other versions of these software packages, although we use relatively basic funcionality from both, so it should be fairly tolerant to different versions.

### Python dependencies

The Python dependencies are listed in `requirements.txt`. You can install them in one go using the following command:

```
pip install -r requirements.txt
```

## System structure

Here is a sketch of the system's structure:

(insert photo from presentation)

## To Run

### Start the backend

To start the simulated MTA stream of sound intensities, use the following command.

```
python 0_streaming_server/playback.py | python 0_streaming_server/server.py
```

### Start the ingestor

**Note**: before you start the ingestor, make sure you have started the Redis server and that it is serving over the default port.

```
python 1_ingestor/ingest.py | python 1_ingestor/store.py
```

### Start the view server

Run the following command to start the view server, which is a websocket pumping out updates to the stream.

```
websocketd --port 6999 python 2_view_server/viewserver.py
```

### Start the frontend

Finally, you can start the front-end server using the following command.

```
cd 3_frontend && ./run_server
```

Navigate your browser to localhost:8000 to view the story, updating in (simulated) real time.