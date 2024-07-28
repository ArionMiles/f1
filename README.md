# f1

This is a simple script to change my room's smart bulbs during a live F1 stream. The colors are based on the P1 driver's team colors. The colors should change in near real-time however it all depends on how fast or how slow the live timing feed is.

The bulbs are controlled entirely by sending instructions over the LAN. Currently only Wipro smart bulbs are supported since that's all I have.

F1's Live Timing feed operates over SignalR protocol which is unauthenticated so you **don't** need an F1TV or F1TV Pro account to use this.

## Setup

### Prerequisites
You need:
1. Python (v3.9 specifically, due to constraints by fasft1's live-timing implementation)
2. Poetry (`python3 -m pip install poetry`)
2. Some tuya compatible smart bulbs.
    - I have a couple of Wipro bulbs which are compatible.
    - See [tinytuya](https://github.com/jasonacox/tinytuya) for instructions on generating your `data/devices.json`

### Getting started

```
# Install all dependencies
poetry install

# Start venv
poetry shell

# Start runner
python3 main.py

# If you need debug logs
LOG_LEVEL=DEBUG python3 main.py
```

- `python3 -m tinytuya wizard` should help create `devices.json` which you can move under `data/`

## Why python?

I usually prefer Go and hate Python with a passion. But, I needed something quick, and the libraries for interfacing with my smart bulbs and streaming the live timing data are readily available.

