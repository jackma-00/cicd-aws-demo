# CICD AWS Demo

The goal of this project is to demonstrate a comprehensive CI/CD workflow, which includes integrating new changes into the main (or production) branch and deploying them to the target AWS Lambda environment using Docker containers. 

_This repository contains the infrastructure as well as the assets to run the CICD AWS Demo._

## Continuous Deployment Workflow

This workflow, named **"Production Deploy,"** is designed to automate the deployment of changes to a production environment on AWS. Here's a step-by-step breakdown:

### Trigger
- **Trigger Event**: The workflow is triggered automatically when a previous workflow, named **"Production Test,"** completes successfully. 
- **Branch Condition**: It specifically runs only when the changes have been merged into the `main` branch, ensuring that only stable and tested code reaches production.

### Environment Variables
- **AWS_REGION**: Specifies the AWS region (`eu-north-1`) where the deployment will take place.
- **ECR_REPOSITORY**: Defines the name of the Amazon Elastic Container Registry (ECR) repository (`cicd-aws-demo`) where the Docker images will be stored.

### Permissions
- **Permissions**: The workflow grants `read` access to repository contents, which is necessary for the checkout and other actions.

### Jobs
#### 1. Deploy Job
- **Name**: The job is called **"Deploy"** and runs on the latest Ubuntu environment (`ubuntu-latest`).
- **Environment**: The deployment is tagged as targeting the `production` environment.

### Steps
1. **Checkout**
   - The workflow checks out the repository's code at the latest commit using `actions/checkout@v4`.

2. **Configure AWS Credentials**
   - AWS credentials are configured using `aws-actions/configure-aws-credentials@v1`. This step sets up the necessary authentication to interact with AWS services, using secrets stored in GitHub (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`).

3. **Login to Amazon ECR**
   - The workflow logs in to Amazon ECR (Elastic Container Registry) using `aws-actions/amazon-ecr-login@v1`, which is essential for pushing Docker images to the registry.

4. **Build, Tag, and Push Docker Image**
   - A Docker image is built from the codebase, tagged with the current commit SHA (`github.sha`), and then pushed to the specified ECR repository. The image tag is saved for use in the next deployment step.

5. **Deploy to AWS Lambda**
   - Finally, the workflow deploys the Docker image to an AWS Lambda function. 
   - It installs the necessary Node.js dependencies, bootstraps the AWS Cloud Development Kit (CDK) environment, and executes the deployment using `npx cdk deploy`.

### Summary
This workflow ensures that once the code has passed all tests and is merged into the main branch, it is automatically built into a Docker image and deployed to the production environment on AWS Lambda, leveraging AWS CDK for infrastructure management.

## Stacks 

* **CICDDemoStack**: Lambda function where the handler is a docker image.

## Assets 

* **SEP Project**: Backend pf the [SEP Project](assets/README.md). Python API receiving event planning requests. 

## Requirements

* NodeJs with `npm` ([Developer's Guide](https://nodejs.org/en/download/package-manager#debian-and-ubuntu-based-linux-distributions))
* AWS CLI v2 ([User Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html))
* AWS CDK CLI v2 ([Developer's Guide](https://docs.aws.amazon.com/cdk/v2/guide/cli.html))
* AWS account with [bootstrapping for CDK](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html)
* Amazon ECR credential helper ([Installation](https://github.com/awslabs/amazon-ecr-credential-helper))
* Python3.10.12 with `pip`

## Quickstart for development experiments 

First, get valid AWS credentials with enough permissions to create and deploy Cloudformation stacks.

The deployment configuration (AWS account and AWS region) is hard-coded into the `cicd-demo.ts` deployment file.

Run the make target `install` to install all the npm's dependencies
```shell
make install
```

### Python venv

Step into `assets/` directory and initialize the Python environment 
**Note:** your Python3 version has to be 3.10 in order to assure Lambda function's support
```shell
python3 -m venv .venv
. .venv/bin/activate
```

Install now the Python project's dependencies running the make target
```shell
make install
```

### Lambda function testing

Once the development Lambda function is updated with the new features you can both:
* visit its URL and post the [sample input request](https://cmwluftjden2ekkbflgk7moi4u0ihwuw.lambda-url.eu-north-1.on.aws/docs#/default/new_event_request_event_requests_post) on the end-point `docs/`.
* or do the same but using Postman. 

## Production 

Thanks to the GitHub workflows the code will be automatically tested, built and deployed to the production environment specified in the files themselves as well as GitHub secrets. 

Particularly, the assets' code will be tested while making pull requests to the base GitHub repository. On success of those tests the application and subsequently the Lambda function will be deployed into production. 