---
title : "Complete, Run CDK and Clean dep"
date :  "`r Sys.Date()`" 
weight : 5
chapter : false
pre : " <b> 6.4. </b> "
---

You have completed the bonus section of this workshop. After understanding the basic concepts and operations of each file. You can start creating the system with CDK. 

## 1. Make sure you are fully prepared 

- Go to the.env file and change it depending on your environment. These are usually resources I can't create with CDK.
- Make sure you have logged into AWS and go to your github account containing your crawler code

## 2. Run CDK
- You can run the following command in the IDE to enter the CDK environment `source .venv/bin/activate`
- After entering the CDK environment, you can run the following command to install the required libraries `$ pip install -r requirements.txt`
- You can then synth out Cloudformation files with the following command: `cdk synth`
- If bootstrap is required, you can run the following command: `cdk bootstrap`
- Finally deploy using the following command: `cdk deploy --all` to run all stacks

## 3. Cleanup

After running, if you want to delete all resources, you can run the following command: `cdk destroy --all`, much faster than manually, right?
