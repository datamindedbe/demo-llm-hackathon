#!/bin/sh
cd part_3_going_to_production
rm -rf package
rm package.zip
mkdir -p package
pip install -r requirements.txt --force-reinstall --target ./package --only-binary=:all: --platform manylinux1_x86_64 --upgrade
pip install pydantic --force-reinstall --target ./package  --only-binary=:all: --platform manylinux1_x86_64 --upgrade
pip install pydantic_core --force-reinstall --target ./package  --only-binary=:all: --platform manylinux1_x86_64 --upgrade
cd package q
zip -r ../package.zip .
cd ..
zip package.zip lambda_function.py
# zip package.zip config.py
# zip -r package.zip src
# aws --profile $AWS_PROFILE_NAME --region eu-central-1 lambda update-function-code \
#     --function-name  TODO_FUNCTION_NAME \
#     --zip-file fileb://package.zip