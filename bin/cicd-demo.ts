#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { CICDDemoStack } from '../lib/cicd-demo-stack';

// The updated image tag is read at every new deployment forcing the deploy of a new docker image
const repoTag = process.env.IMAGE_TAG ? `${process.env.IMAGE_TAG}` : "0be904945eef0f9ae8d900df255508c3fceb12ab";

const app = new cdk.App();

new CICDDemoStack(app, 'CICDDemoLambda', {
  repoTag: repoTag,
  env: { account: '403097528197', region: 'eu-north-1' },
});