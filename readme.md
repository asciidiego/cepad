# cepad

This repository contains a CUDA-Enabled Pub/Sub application in
Docker (cepad)

## Setup

### System requirements

- You have installed and configured Docker.
- You have installed Nvidia drivers.
- You have installed `nvidia-container-toolkit`.

A way of knowing that you meet the pre-requisites is executing
the following command:

```bash

sudo docker run --rm --gpus all pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime nvidia-smi

```

### Environment setup

Create a virtual environment using `venv`.

```bash

python -m venv .venv # .venv is ignored by .gitignore

```

## Usage

There are two components in this repository. One of them is a worker
that subscribes to a Redis server and publishes images to it after
it processes each one of them. The other component allows to send
messages and save the received images locally.

To run the image processor, use this script:

```bash

python cepad/main.py

```

To run the image sender/receiver, use this other script:

```bash

python script/send_and_receive.py

```

## Graphical explanation

Below, you can see an event diagram of the program flow. If the
diagram does not render correctly, check the README.md raw file.

```

                          > 0. Subscribes to 'image_res' topics

                                  > 1. User sends prompt

                                   ┌───────────────────┐
                                   │                   │  7. Receives images through 'image_res' topic
                                   │  Python Process   │
                                ┌──┤     (Client)      ├─┐   and saves it
                                │  │                   │ │
                                │  └───────────────────┘ │
                                │                        │
                                │                        │
                          ┌─────┴─────┐           ┌──────┴────┐
                          │           │           │           │
  > 3. Publish to 'jobs'  │  Pub/Sub  │           │   Queue   │   > 2. Posts to 'jobs' queue
                          │           │           │           │
                          └─────┬─────┘           └─────┬─────┘
                                │                       │
                                │                       │
                                │                       │
                                │                       │
                                │                       │
                                │  ▲                    │
> 4. Sub triggers queue fetch   │  │ 6. Send image as   │         > 5. All nodes pop the queue to try to get
                                │  │                    │
                                │  │ bytes through the  │              the latest job. Jobs are served on a
                                │  │                    │
                                │  │ 'image_res' topic  │              first come first served basis.
                                │                       │
                          ┌─────┴───────────────────────┴──────┐
                          │                                    │
                          │       Worker Group                 │
                          │                                    │
                          │         ┌────────────────┐         │
                          │         │                │         │
                          │         │ Worker Node #1 │         │
                          │         │                │         │
                          │         └────────────────┘         │   > 0. Subscribes to 'jobs' topic
                          │                                    │
                          │         ┌────────────────┐         │
                          │         │                │         │
                          │         │ Worker Node #2 │         │
                          │         │                │         │
                          │         └────────────────┘         │
                          │                                    │
                          └────────────────────────────────────┘

```
