# cepad

This repository contains a CUDA-Enabled Pub/Sub application in
Docker (cepad)

## Setup

### System requirements

### Environment setup

Create a virtual environment using `venv`.

```bash python -m venv .venv

# .venv is ignored by .gitignore ```

## Usage

There are two components in this repository. One of them is a worker
that subscribes to a Redis server and publishes images to it after
it processes each one of them. The other component allows to send
messages and save the received images locally.

To run the image processor, use this script:

```bash python cepad/main.py ```

TO run the image sender/receiver, use this other script:

```bash python script/send_and_receive.py ```

