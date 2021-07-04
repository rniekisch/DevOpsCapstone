#!/usr/bin/env bash

## Run eksctl to create the kubernetes cluster
eksctl create cluster \
--name capstone-cluster \
--region us-west-2 \
--nodegroup-name capstone-workers \
--node-type t2.medium \
--nodes 2