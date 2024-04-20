#!/bin/sh
rm -rf package
mkdir -p package
pip install -r requirements.txt --force-reinstall --target ./package --only-binary=:all: --platform manylinux1_x86_64 --upgrade
pip install pydantic --force-reinstall --target ./package  --only-binary=:all: --platform manylinux1_x86_64 --upgrade
cp ./lambda_function.py ./package/lambda_function.py