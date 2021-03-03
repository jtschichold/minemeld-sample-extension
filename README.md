# minemeld-sample-extension

Sample Extension for MineMeld (10.0a1 and later)

## Introduction

Extensions for MineMeld are basically Python3 packages that could include:
- new node classes
- new prototypes
- new UI components
- new API

This simple extension only includes a [new node class](sample_extension/node.py) and a [new prototype](sample_extension/prototypes/sample_extension.yml).

## Dynamic discovery

MineMeld engine discovers prototypes and node classes using [setuptools entry points](https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html#advertising-behavior). The entry points are listed in the file [minemeld.json](minemeld.json) that should exist in the root of the extension:
- *minemeld_nodes* is the list of node classes provided by the extension
- *minemeld_prototypes* is the list of prototype libraries provided by the extension

## Installation

The easiest way to install the extension is using *pip3* in the virtual environment of the MineMeld engine, check the [Dockerfile](docker/Dockerfile) for an example. The Dockerfile requires a *minemeld:test* image built from the [MineMeld Python3 Dockerfile](https://github.com/jtschichold/minemeld-core/blob/welcome-python3/docker/Dockerfile).

## Build & Run the docker image

To build the MineMeld engine docker image with the extension:
`docker build --force-rm -t minemeld:sample_extension -f docker/Dockerfile .`

To run it:
`docker-compose -f docker/docker-compose.yml up`