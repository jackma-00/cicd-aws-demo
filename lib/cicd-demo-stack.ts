import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Repository } from "aws-cdk-lib/aws-ecr";
import { DockerImageCode, DockerImageFunction, FunctionUrlAuthType } from "aws-cdk-lib/aws-lambda";
import { AnyPrincipal, Role } from "aws-cdk-lib/aws-iam";
import { Duration } from "aws-cdk-lib";

export interface CICDDemoStackProps extends cdk.StackProps {
  repoTag: string;
}

export class CICDDemoStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: CICDDemoStackProps) {
    super(scope, id, props);

    // ECR Repository where our Lambda function takes the code
    const repo = Repository.fromRepositoryName(this, "cicd-aws-demo", "cicd-aws-demo");

    // Define the Lambda function resource
    const lambdaFunction = new DockerImageFunction(this, "CICDDemoLambda", {
      code: DockerImageCode.fromEcr(repo, {
        tagOrDigest: props.repoTag, // The image tag corresponding to the image we want to load into our Lambda Function
      }),
      functionName: this.stackName,
      timeout: Duration.seconds(60),
    });

    // Add an end-point to the lambda function
    const endpoint = lambdaFunction.addFunctionUrl({
      authType:  FunctionUrlAuthType.NONE, // AWS_IAM: Only authenticated IAM users and roles can make requests to your function URL.
    });

    // Grant permission to the URL to be invoked 
    endpoint.grantInvokeUrl(new Role(this, "role", {
      assumedBy: new AnyPrincipal(), // note: this role is too permissive, use a relevant existing role or reduce the principal scope
    }));
  }
}