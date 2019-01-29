#!/bin/bash

#Install aws command line tools -
#https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

#and sam (Serverless Application Model)
#https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

#The last step uses jq to print the url in api gateway

#You can find the stack in cloud formation
STACK_NAME=api-key

#This is a staging bucket -- the lambda and it's dependencies are zipped up and uploaded to this bucket
BUCKET=vivi-lambda-test-east

#The config.ini goes here
CONFIG_BUCKET=vivi-lambda-test-east

#This subnet should have access to the database
#GOTCHA: The VPC containing this
SUBNET_ID=subnet-ecc447b4

#The lambda wants to be assigned a security group id .. make sure it has access to the database
SECURITY_GROUP_ID=sg-7a9ce202

#New feature!  Put everything, including libraries listed in requirements.txt into a directory ".aws-sam/build"
sam build

#But, strangely, the next steps ignore this directory unless you cd into it
cd .aws-sam/build

#Processes the cloudformation template, zips up the necessary files, uploads to s3, and creates
#a new cloudformation file ("output.yml") referencing the zip file in s3
sam package --output-template-file output.yml --s3-bucket ${BUCKET}

#And finally, create the cloudformation stack
aws cloudformation deploy --template-file output.yml --capabilities CAPABILITY_NAMED_IAM --stack-name ${STACK_NAME} --parameter-overrides "ConfigBucketName=${CONFIG_BUCKET}" "SubnetId=${SUBNET_ID}" "SecurityGroupId=${SECURITY_GROUP_ID}"

#This step plucks the url out of the api gateway
aws cloudformation describe-stacks --stack-name ${STACK_NAME} | jq '.Stacks[0].Outputs[0].OutputValue'

#You can read the endpoint from above and use
#curl  -H 'X-Api-Key: <whatever>' -X POST   -d "type=1" "https://ls4l55ry8h.execute-api.us-east-1.amazonaws.com/Prod/test"
