#!/bin/bash

# 
scp -r -i ~/.ssh/alison_cloud_deployment.pem \
  *.py requirements.txt Dockerfile seeds templates static \
  ec2-user@13.135.74.68:~/book_store

# Log in to EC2
ssh -i ~/.shh/alison_cloud_deployment.pem ec2-user@13.135.74.68

