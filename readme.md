# cepad

This repository contains a **C**UDA-**E**nabled **P**ub/Sub **A**pplication in
**D**ocker (cepad)

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

You should see something similar to the following `nvidia-smi` output:

<details>
<summary>
Click here to see the sample `nvidia-smi` output.
</summary>

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 510.54       Driver Version: 510.54       CUDA Version: 11.6     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ...  Off  | 00000000:09:00.0 Off |                  N/A |
| 27%   29C    P8     6W / 180W |     11MiB /  8192MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   1  NVIDIA GeForce ...  Off  | 00000000:41:00.0 Off |                  N/A |
|  0%   36C    P8    18W / 250W |    586MiB / 11264MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A      1288      G                                       4MiB |
|    0   N/A  N/A    166699      G                                       4MiB |
|    1   N/A  N/A      1288      G                                     102MiB |
|    1   N/A  N/A    166699      G                                     448MiB |
|    1   N/A  N/A    166828      G                                      12MiB |
|    1   N/A  N/A    167726      G                                       9MiB |
+-----------------------------------------------------------------------------+
```
</details>

### Environment setup

Create a virtual environment using `venv`.

```bash

python -m venv .venv # .venv is ignored by .gitignore
source .venv/bin/activate
pip install -r requirements.txt

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
