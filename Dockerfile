FROM rasa/rasa:3.3.10-full


USER root

RUN pip install black[jupyter] \
    ipykernel \
    pytest \
    isort \
    openai \
    packaging==21.3 \
    rasa_sdk==3.5.1 \
    tenacity \
    isort

RUN apt update && \
    apt install -y git \
        make \
        wget