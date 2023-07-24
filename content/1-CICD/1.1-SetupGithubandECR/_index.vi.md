---
title : "Chuẩn bị Github Repo "
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 1.1 </b> "
---

Trong bài này, các bạn sẽ chuẩn bị các files cần thiết cho các bài sau. Mình sẽ đi qua từng phần. Trong bài lab này, mình sẽ sử dụng VSCode để chuẩn bị đầy đủ các file ở môi trường local và đẩy lên Github. Mình cũng sử dùng Console để deploy kiến trúc lên cloud. Ở phần 2 của bài workshop, mình sẽ chỉ cách các bạn có thể deploy lên bằng CDK (Cloud Development Kit) nếu bạn muốn học thêm về IaC.

## Chuẩn bị crawler và push lên Github
Trước hết, bạn cần chuẩn bị các file crawler và đẩy lên Github. Đây sẽ là crawler mà chúng ta sẽ deploy lên cloud. Bạn hãy vào link Github sau: [Github Crawler](https://github.com/MinhThieu145/Job-Scraper-Home.git). Sau khi vào rồi hãy clone repo này về máy của bạn. Bạn có thể clone bằng cách chạy lệnh sau:

```
git clone -b indeed-scraper https://github.com/MinhThieu145/Job-Scraper-Home.git
```

Nếu như bạn bị lỗi ở câu lệnh trên, hãy thử dùng:

```
git --version
```
Nếu như bạn thấy kết quả trả về hiển thị rõ git version. Thì bạn đã cài git thành công. Nếu không, bạn cần cài git trước khi clone repo. Bạn có thể cài git bằng cách tham khảo link sau [Cách cài Github cho VsCode](https://www.geeksforgeeks.org/how-to-install-git-in-vs-code/). Sau khi clone hoàn tất, bạn sẽ có 1 repo như sau:

```markdown
📦Job-Scraper-Home
 ┣ 📂.git
 ┣ 📂__pycache__
 ┣ 📂result
 ┣ 📜.gitignore
 ┣ 📜buildspec.yml
 ┣ 📜dockerfile
 ┣ 📜exploration.ipynb
 ┣ 📜job_description_analyzer.py
 ┣ 📜main.py
 ┣ 📜requirements.txt
 ┗ 📜scraper.py
```

Mình sẽ đi qua từng file và folder mà bạn cần biết trong repo này:

### 1. main.py và scraper.py
Đầu tiên là file **main.py**. File có nhiệm vụ chạy file scraper.py và chứa kết quả trong 1 folder tên là result (sẽ tạo folder mới nếu không tồn tại). Sau cùng, script sẽ đẩy tất cả files trong folder result lên S3.

```python
# import indeed scraper
import scraper

# import analyze data function
import job_description_analyzer

# some other libraries
import os
import pandas as pd

# main function
def main():

    # clean the result folder
    # get current dir
    current_dir = os.getcwd()

    # get the result folder if exit
    try:
        # if the result folder exists
        result_dir = os.path.join(current_dir, 'result')
        # delete all the files in the result folder
        for file in os.listdir(result_dir):
            os.remove(os.path.join(result_dir, file))

        
    except:
        # create a new folder called result
        os.mkdir('result')
        result_dir = os.path.join(current_dir, 'result')


    # run the scraper
    scraper.main()

    # get the result from a folder called result

    # loop through the result folder
    for file in os.listdir(result_dir):
        # if that is a csv file
        if file.endswith('.csv'):
            # read with pandas
            df = pd.read_csv(os.path.join(result_dir, file))

            # if the dataframe is not empty
            if not df.empty:
                # pass that to the analyze data function
                job_description_analyzer.main(df=df, df_name=file.split('.')[0])
                    


if __name__ == "__main__":
    main()


```

 Nếu bạn đọc kĩ code, bạn sẽ thấy main.py loop qua tất cả file đuôi **.csv** trong folder result và gọi 1 function khác trong **job_description_analyzer.py** trước khi đẩy lên S3. Lý do là vì mình đã cắt ngắn repo đi nhiều. Ban đầu crawler sẽ có nhiệm vụ như sau.

- main.py sẽ lên S3 để tìm các crawlers (mỗi website là 1 crawler khác nhau) và chạy các crawler này.
- Các crawler này sau khi chạy xong đều sẽ lưu kết quả vào folder result. - Sau đó, file job_description_analyzer.py có nhiệm vụ extract những từ khoá và những thông tin quan trọng bằng GPT API, trước khi lưu kết quả lại
- Cuối cùng, cả kết quả scrap ban đầu và sau khi xử lý được đẩy lên S3. 

Do quá trình này khá lâu, dễ hỏng và không hiệu quả khi gần như xử lý hoàn toàn bằng code. Nếu bạn muốn thử làm lại, bạn có thể sử dụng AWS Step Function và AWS SNS để decouple các phần, nhằm đảm bảo thứ tự thực hiện và độ ổn định của Pipeline. Nhưng trong bài lab này mình sẽ không đi qua phần đó

### 2. dockerfile và requirements.txt
Đây là 2 files cần thiết để có thể build 1 docker image từ code. Trong File **dockerfile**, mình đã

- Sử dụng based image là **Ubuntu:22.04**. Nhưng bạn có thể sử dụng những base image khác, miễn là có cài sẵn Python3. Nếu không bạn sẽ phải tự cài đặt Python3
- Cài đặt và update pip để tải cài các package cần thiết cho crawler. Tên của các package này được lưu trong file **requirements.txt**. Trong bài lab này, mình đã sử dụng boto3 để có thể gọi các API của AWS, openai để có thể gọi API của GPT3 (có thể bỏ vì không dùng nữa), pandas để xử lý dữ liệu, selenium để có thể chạy crawler và webdriver_manager để có thể tự động tải driver cho selenium. Tất cả các packages này đều được lưu trong file requirements.txt. Bạn có thể thêm bớt các packages này tùy theo ý muốn.

```r
boto3==1.26.165
openai==0.27.7
pandas==1.5.3
selenium==4.10.0
tenacity==8.2.2
webdriver_manager==3.8.6
```
- Cài đặt Chrome browser cho image. 
- Cuối cùng là Copy các file vào docker image

Bạn có thể đọc dockerfile của mình ở đây

```dockerfile
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

# okay now pip
RUN apt-get -y update
RUN pip install --upgrade pip

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
### 3. buildspec.yml
Còn 1 file nữa mà bạn cần chú ý, đó là file **buildspec.yml**. File này cực kì quan trọng, vì nó hướng dẫn cho AWS Codebuild cách build image của bạn. Buildspec được chia làm 3 phase, pre_build, build và post_build. 

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

Trong phase **pre_build**, mình đã lưu các biến môi trường như sau:

- **AWS_DEFAULT_REGION:** region mà bạn dùng cho bài workshop này, mình dùng us-east-1 (virginia)
- **AWS_ACCOUNT_ID:** Account ID tài khoản AWS của ban, có thể tìm được ở phần account
![lol](/images/2023-07-09-09-52-36.png)
- **IMAGE_TAG**: Tag của image mà bạn muốn lấy trong ECR. Trong quá trình build, bạn sẽ update image nhiều lần, mỗi lần là tag + 1. Nên tag latest giúp bạn lấy image mới nhất
- **REPOSITORY_URI:** link của ECR repo chứa image, mình sẽ tạo ngay ở phía dưới.
- Dòng cuối cùng của phase là để mình authenticate script của mình, giúp mình có thể thực hiện các lệnh trong Docker như Push hay Pull image từ Ecr.
  
Trong phase **build**, mình sẽ build image và push lên ECR repo. 

- `docker build -t $REPOSITORY_URI:$IMAGE_TAG .` mình build image và set tag là **latest**. Đây là biến IMAGE_TAG mình set từ trước. Nhớ đừng quên có 1 dấu chấm sau chữ IMAGE_TAG đấy.
- `docker push $REPOSITORY_URI:$IMAGE_TAG` mình push Docker image mình vừa build lên Ecr repo. Ở đoạn này, nếu làm theo mình thì bạn sẽ bị vướn mắc do mình chưa tạo repo, vì vậy bạn có thể để trống biến này, và đọc tiếp phần sau để biết cách tạo repo.
  
Cuối cùng là phase **post_build**. Mình chỉ log ra console để thông báo hoàn thành. Phase này hoàn toàn không thực hiện lệnh gì cả.

## Deploy Github repo lên Github.
Sau khi hoàn thành việc chuẩn bị các file, việc tiếp theo là đẩy repo lên Github. Đầu tiên, bạn cần mở folder mà bạn vừa clone repo về. Trong VSCode sẽ nhìn như thế này
![](/images/2023-07-19-18-32-06.png)

1. Kiểm tra xem bạn đã có git chưa bằng `git --version`. Tiếp đến, bạn cần remove file **.git** khỏi folder do folder vẫn liên kết với repo Github của mình. Dùng lệnh này để remove file .git `rm -rf .git`. Sau đó bạn cần tạo repo mới trên Github của mình. 
2. `git init -b main` để khởi tạo repo mới. 
3. `git add .` để add tất cả các file trong folder vào repo
4. `git commit -m "Initial commit"` để commit các file vừa add vào repo
5. Lên tài khoản github của bạn, tạo 1 repo mới và copy URL 
6. `git remote add origin <URL>` để add repo mới vào local repo của bạn
7. `git push -u origin main` để push repo lên Github. Nếu bạn bị lỗi, hãy thử `git push -f origin main` để force push.
8. Sau khi push xong, bạn có thể thấy repo của bạn đã được update