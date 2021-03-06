#!/bin/bash

#################################################################
# Create mercure from scratch in Docker environment
#################################################################
#
# Make sure to change the configuration below, as they are most
# likely different for your environment
#
# Once you are happy, simply run this script to build mercure
# See docker/docker-compose.yml for a sample script
#
#################################################################

#################################################################
# CONFIG SECTION
#################################################################
# Change prefix to your own Docker prefix if you want to make 
# your own custom build
PREFIX="mercureimaging"
TAG=${MERCURE_TAG:-latest}
# Define where mercure is going to store things
# You can redefine types of volumes in docker/docker-compose.yml
MERCUREBASE=/opt/mercure
DATADIR=$MERCUREBASE/data
CONFIGDIR=$MERCUREBASE/config
DBDIR=$MERCUREBASE/db
MERCURESRC=./

#################################################################
# BUILD SECTION
#################################################################
docker build -t $PREFIX/mercure-base:latest -f docker/base/Dockerfile .
docker build docker/ui -t $PREFIX/mercure-ui:$TAG
docker build docker/bookkeeper -t $PREFIX/mercure-bookkeeper:$TAG
docker build docker/cleaner -t $PREFIX/mercure-cleaner:$TAG
docker build docker/dispatcher -t $PREFIX/mercure-dispatcher:$TAG
docker build docker/processor -t $PREFIX/mercure-processor:$TAG
docker build docker/receiver -t $PREFIX/mercure-receiver:$TAG
docker build docker/router -t $PREFIX/mercure-router:$TAG
