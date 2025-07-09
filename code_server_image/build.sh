#!/usr/bin/bash

docker build --build-arg USER=mrkein --build-arg UID=1000 --build-arg GID=1000 -f Dockerfile -t vscode:4.89.1-python3.10 .

