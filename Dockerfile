FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

# Install CUDA compiler
# -> Some PyTorch plugins may require this
RUN conda install -c nvidia cuda-nvcc -y


# Module + dependencies
WORKDIR "/app"

COPY requirements.txt .
COPY cepad cepad
RUN pip install -r requirements.txt

# Runs python as unbuffered so that logs appear when
# running using the `docker run` command
CMD ["python", "-u", "cepad/main.py"]
