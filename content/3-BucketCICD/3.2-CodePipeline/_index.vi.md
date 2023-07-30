---
title : "Deploy Codepipeline"
date :  "`r Sys.Date()`" 
weight : 2 
chapter : false
pre : " <b> 3.2. </b> "
---

1. Vào AWS Codepipeline, chọn Create Pipeline

![](/content/3-BucketCICD/3.2-CodePipeline/images/2023-07-29-22-25-19.png)

2. Chọn tên cho pipeline, chọn **New service Role**, chọn Role name

![](/content/3-BucketCICD/3.2-CodePipeline/images/2023-07-29-22-29-14.png)

3. Chọn Source là Github (version 1). Connect to Github. Bạn sẽ được yêu cầu đăng nhập vào Github và cấp quyền cho AWS Codepipeline. Ở phần **Change detection options** chọn Github webhook. 

![](/content/3-BucketCICD/3.2-CodePipeline/images/2023-07-29-23-02-39.png)

4. Chọn next. Bạn cần chọn tên cho Build, chọn region tuỳ ý. Ở phần Project name, bạn chọn Creating project để tạo project mới Codebuild

![](/content/3-BucketCICD/3.2-CodePipeline/images/2023-07-29-23-10-10.png)

5. Chọn tên cho Codebuild. Trong phần Environment chọn Managed image, chọn Operating System là Ubuntu. Image chọn `standard:7.0` và chọn **Always use the latest image for this runtime**. Chọn Environment là Linux (không cần tới GPU). Bỏ qua tick priviledge vì không cần build Docker

![](/content/3-BucketCICD/3.2-CodePipeline/images/2023-07-29-23-16-19.png)

6. Ở phần Service Role, bạn cần CodeBuild có quyền để upload lên S3. Nên bạn cần quay lại IAM Role, Tạo 1 Role mới cho phép ghi vào S3

![](/content/3-BucketCICD/3.2-CodePipeline/images/2023-07-29-23-28-07.png)

7. Tiếp đến là phần buildspec. Để có thể build được Hugo, bạn tạo 1 file `buildspec.yml` trong project rồi dùng file sau nhé:

```yaml
version: 0.2

phases:
  pre_build:
    commands:
      # Install Hugo on Ubuntu
        - sudo apt update
        - sudo apt install hugo -y

  build:
    commands:
    # Translate and update the _index.md files in their respective locations
        - hugo


  post_build:
    commands:
      # Build the Hugo project

      # Get the S3 bucket name from environment variable
        - s3_bucket_name="workshop-1.5"

      # Empty the bucket before pushing the new content
        - aws s3 rm "s3://$s3_bucket_name/" --recursive

      # Upload public folder to S3
        - aws s3 cp public/ "s3://your-s3-bucket-name/" --recursive --exclude "public/*" --include "public/*.*"

```

Giải thích:
- ở phần prebuild, mình có 2 commands để update apt và cài đặt hugo
- ở phần build, mình chạy lệnh `hugo` để build website thành folder public
- ở phần postbuildm mình upload folder public lên S3. Bạn cần diền tên của bucket vừa tạo vào variable s3_bucket_name

8. Sau đó, chọn Continute to CodePipeline để quay lại Codepipeline. Chọn Next

9. Bạn Skip Deploy Stage để sang phần review, rồi chọn Create pipeline nhé


