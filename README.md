# README

A fully containerized AWS Lambda function using Python 3.11, Faker, Boto3, and S3 — built and deployed through a CodePipeline → CodeBuild → ECR → Lambda workflow. All sensitive data is stored in a secure KMS-encrypted S3 bucket.

## Features
-AWS Lambda container image (Python 3.11)
-Faker-generated user and company data
-Secure data writes to S3 (KMS-encrypted)
-CI/CD pipeline with CodePipeline and CodeBuild
-Image artifacts stored in ECR
-Auto-build on GitHub push
-Infrastructure defined in CloudFormation

# Repo Structure
```
lambda-faker-api/
├── app/
│   └── lambda_function.py
├── Dockerfile
├── requirements.txt
├── buildspec.yml
├── secure-s3-with-kms.yaml
└── README.md
```