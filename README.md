# DSPConfiguration
## A serverless script that shares internal DSP configurations with their account managers.
This script is used to help account managers gain access to key informations about their accounts that aren't accessible to them via SDX. The project does the following:
* Pulls data from the internal SDX Admin API.
* Parses the key paramers the Account managers need to have.
* Sends an emai with the DSP configurations.
Note: this lambda function will be triggered every other week by AWS Evebridge so that AMs will have latest data.

## How to Deploy on AWS
The lambda function is deployed from a container image that is stored in AWS ECR. For that you will need access to the registry.
1. Clone the repository
2. Update code
3. Create an environment variable for the image registry
```bash
export ECR_URL= "<AWSAccountId>.dkr.ecr.us-east-1.amazonaws.com/dsp-configuration"
```
3. Build a new image
```bash
docker build -t dsp-script .
```
4. Tag your new image
```bash
 docker tag dsp-script:latest $ECR_URL:latest
```
5. Log into ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin "<AWSAccountId>.dkr.ecr.us-east-1.amazonaws.com"
```
6. Push code to AWS ECR
```bash
docker push $ECR_URL:latest
```
