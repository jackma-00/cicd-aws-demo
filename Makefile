.PHONY: install bootstrap synth deploy 

install:
	npm install

bootstrap: 
	cdk bootstrap

synth: 
	cdk synth

deploy: 
	cdk deploy

all: install bootstrap synth deploy 