FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

# Install CUDA compiler
# Some PyTorch plugins may require this
RUN conda install -c nvidia cuda-nvcc -y

WORKDIR "/app"

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-u", "cepad/main.py"]
