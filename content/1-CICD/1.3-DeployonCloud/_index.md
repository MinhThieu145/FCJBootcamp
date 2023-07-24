---
title : "CICD"
date :  "`r Sys.Date()`" 
weight : 2
chapter : false
pre : " <b> 1.3 </b> "
---
![](/images/2023-07-09-08-35-11.png)

## Khái niệm CICD
CICD là quá trình tích hợp, update code thường xuyên. Có thể nhanh chóng build, test và deploy 1 cách liên tục. Trong bài workshop này, mình sẽ làm 1 pipeline để tự lấy code từ Github khi có thay đổi, build thành **docker image** và đẩy vào ECR.

## Setup Github và Scraper cho Indeed
Để thuận tiện thì mình sẽ cung cấp link Github: https://github.com/MinhThieu145/Job-Scraper-Home.git. Bạn cần clone repo này về máy và upload lên github của riêng mình.

```
git clone https://github.com/MinhThieu145/Job-Scraper-Home.git
```

Do workshop này tập trung vào Cloud, nên mình sẽ không đi sâu vào từng phần trong rep. Một số file bạn nên hiểu

### 1. File buildspec.yml


```yaml

version: 0.2

phases:
  pre_build:
    commands:
      - echo "Logging in to ECR"
      - aws --version
      - AWS_DEFAULT_REGION=us-east-1
      - AWS_ACCOUNT_ID=238101178196
      - IMAGE_TAG=latest
      - REPOSITORY_URI=238101178196.dkr.ecr.us-east-1.amazonaws.com/indeed-scraper
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com

  build:
    commands:
      - echo "Building the Docker image..."
      - docker build -t $REPOSITORY_URI:$IMAGE_TAG .
      - docker push $REPOSITORY_URI:$IMAGE_TAG

  post_build:
    commands:
      - echo "Updating ECS service..."
      - echo "End of script"

artifacts:
  files:
    - '**/*'
  name: artifacts

```

File này cực kì quan trọng, vì nó dùng để push image lên ECR trong Codebuild. Buildspec được chia làm 3 phase, pre_build, build và post_build. Theo mình thì 3 phase chủ yếu để cho clean và phòng lỗi, bạn hoàn toàn có thể dồn gần hết code vào 1 phase.

#### Pre_build
Trong phase **pre_build**, mình setup 1 số phần quan trọng như 

- **AWS_DEFAULT_REGION:** region mà bạn dùng cho bài workshop này, mình dùng us-east-1 (virginia)
- **AWS_ACCOUNT_ID:** Account ID tài khoản AWS của ban, có thể tìm được ở phần account
![lol](/images/2023-07-09-09-52-36.png)
- **IMAGE_TAG**: Tag của image mà bạn muốn lấy trong ECR. Trong quá trình build, bạn sẽ update image nhiều lần, mỗi lần là tag + 1. Nên tag latest giúp bạn lấy image mới nhất
- **REPOSITORY_URI:** link của ECR repo chứa image, mình sẽ tạo ngay ở phía dưới.

#### Tạo ECR repo 
Bạn cần tìm ECR -> chọn Create repository. Các setting bạn để như sau
![](/images/2023-07-09-09-56-40.png)

- **Visibility:** Chọn chế độ private. Mình từng gặp lỗi không thể pull image được nếu để là public, nên recommend đặt là private
- **Repository name:** Đặt tên cho repo, bạn có thể thấy được link repo. Link 1 repo được viết như sau:
```
238101178196.dkr.ecr.us-east-1.amazonaws.com/indeed-scraper
```
- Trong đó dãy số đứng đầu là account Id của bạn
- Sau chữ 'ecr' là region sử dụng
- và cuối cùng là tên bạn tự đặt, của mình là `indeed-scraper`

Ở 3 options còn lại, bạn có thể để là disable
![](/images/2023-07-09-10-07-01.png)

Sau khi tạo xong, bạn có thể copy URI của repo vừa tạo và paste vào file buildspec
![](/images/2023-07-09-10-14-49.png)

#### Build
Bên trong phase này, mình để các code chính, tức là code liên quan đến việc build và push lên ECR.
- `docker build -t $REPOSITORY_URI:$IMAGE_TAG .` Đừng quên có 1 dấu chấm sau chữ IMAGE_TAG đấy. Dòng này dùng để build Docker image và set tag là **latest**
- `docker push $REPOSITORY_URI:$IMAGE_TAG` Dùng để push image lên ECR repo

#### Post_build
Cả 2 dòng lệnh đều dùng để log ra console để thông báo hoàn thành

### Dockerfile
```docker

# based image: Ubuntubased. BTW, for the PYTHON:3.9 like you used last time. It used the Debianbased image

FROM public.ecr.aws/docker/library/ubuntu:22.04

# install a few things
RUN apt-get update && apt-get install -y \
    bash \
    git \
    curl \
    software-properties-common \
    pip \
    && rm -rf /var/lib/apt/lists/*

# workdir
WORKDIR /srv

# Copy the requirements.txt file first, for separate dependency resolving and downloading
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install chrome broswer
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable

# add the main.py
COPY main.py .

# add scraper
COPY scraper.py .

# add job_description_analyzer
COPY job_description_analyzer.py .

ENTRYPOINT [ "python3" , "main.py" ]

```
Sơ lược qua file dockerfile, những gì mình làm trong file bao gồm:
 - `FROM public.ecr.aws/docker/library/ubuntu:22.04` Mình sẽ dùng Ubuntu 22.04 cho base image 
 - Dòng tiếp theo để update và upgrade lại packages, cài pip và software properties. Sẽ có 1 số cái không có tác dụng trong project lần này do mình lấy từ template
 - Cài các packages qua file requirements.txt
 - Cài chromebrowswer, do mình sẽ scrap bằng selenium và chrome
 - copy các file main.py, scraper.py và # add job_description_analyzer.py




