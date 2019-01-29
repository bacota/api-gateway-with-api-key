`deploy.sh` is a bash script that deploys the lambda
There are variables at the top that need to be edited before running.

Prerequisites

1. Install aws command line tools  https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html

2. Install sam (Serverless Application Model) https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

3. (Optional) Install jq for the last step, that just prints the url in the api endpoint

Then edit variables at the top of the script.   And run it.  This is what it does:

``sam build``

Puts everything, including libraries listed in `requirements.txt` into a directory `.aws-sam/build`.  (This is a new feature - much easier than virtualenv).   But, strangely, the next steps ignore this directory unless you cd into the directory, so the script cd's.

The next step  processes the cloudformation template `template.yml`, zips up the necessary files, uploads them to s3, and creates a new cloudformation template `output.yml` referencing the zip file in s3.

The next step uses `output.yml` to create cloudformation stack.  You can look at the stack on the console.  or use the aws cli.

The last line of the script uses jq to extract the url of the api gateway endpoint that was created.  You can test it using something like: 

``curl  -H 'X-Api-Key: <whatever>' -X POST   -d "type=1" "https://ls4l55ry8h.execute-api.us-east-1.amazonaws.com/Prod/test"``



*GOTCHA #1*  The VPC into which the lambda is deployed must have a VPC Endpoint for S3.  I'll try to add a script for making one if it doesn't already exist, but it can be done through the console  https://www.cloudberrylab.com/resources/blog/creating-and-accessing-amazon-s3-vpc-endpoint/

*GOTCHA #2" The config.ini has to be uploaded to the correct bucket and *make sure it's readable* by the Lambda.  You might have to add a permission to the role created for the lambda.  
