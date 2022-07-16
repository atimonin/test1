FROM python:3

ARG USER=sample-user
RUN useradd --user-group --create-home --home-dir /${USER} --no-log-init --shell /bin/sh -u 10000 ${USER}
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get clean

WORKDIR /${USER}
USER ${USER}


COPY --chown=${USER} requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY --chown=${USER} ./main.py .

EXPOSE 8000
CMD [ "python", "main.py" ]
