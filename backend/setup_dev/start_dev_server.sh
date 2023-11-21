#!/bin/bash

base="$(cd "$(dirname -- "$1")" >/dev/null; pwd -P)"
docker run -it -d --rm -v $base:/app -p 5000:5000 grimm:dev
