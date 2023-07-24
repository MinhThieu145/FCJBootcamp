---
title : "Deploy CI/CD pipeline lên AWS"
date :  "`r Sys.Date()`" 
weight : 2
chapter : false
pre : " <b> 1.3 </b> "
---

Sau khi hoàn thành các bước chuẩn bị, thì bạn cũng đã có đầy đủ các file cần thiết để deploy CI/CD pipeline lên AWS. Trong bài này, mình sẽ hướng dẫn bạn cách deploy CI/CD pipeline lên AWS bằng cách sử dụng AWS Codebuild

{{% notice note %}}
*Sơ lược về dịch vụ AWS Codebuild:*  AWS Codebuild cho phép tự động build, test và containerize code của bạn. Codebuild có thể dùng với AWS CodePipeline để tự động deploy sau khi build. Tuy nhiên trong bài này mình chỉ build và push image lên ECR thôi. 
{{% /notice %}}


## Tạo Codebuild Project 

1. Tìm Codebuild trong AWS, chọn **Create build project**
2. Trong phần Project configuration, điền tên project và Description
![](/images/2023-07-09-13-21-09.png) 
3. Ở phần Source, chọn Github là provider
![](/images/2023-07-09-13-23-07.png)
4. Ở phần Repository, chọn **Connect to Github** và chọn repo mà bạn đã tạo ở bước trước. Bạn có thể bị yêu cầu connect với Github ở bước này, nhập password vào kết nối thôi.
![](/images/2023-07-09-13-24-36.png)
5. Tiếp đến phần **Primary source webhook events**, tick options webhook để build bằng webhook, chọn single build và event type là PUSH
![](/images/2023-07-09-13-30-46.png)
6. Trong phần Environment, chọn **Managed image** (Docker image đã bao gồm Operating System rồi, nên phần này thật tế không cần thiết. Nhưng nếu bạn không dùng Docker và cần 1 vài packages thì có thể dùng Custom Image). **Operating System** chọn Ubuntu, **Runtime** là Standard và **version** chọn latest 7.0. **Environment type** chọn Linux không có GPU.

    {{%notice warning%}}
Bạn đặt biệt phải chọn **Privileged** ở phần **Additional configuration**. Nếu không chọn thì sẽ không thể push image lên ECR được.
    {{%/notice%}}
![](/images/2023-07-09-13-39-36.png)

7. Chọn New Role
![](/images/2023-07-09-13-44-52.png)

8. Ở phần Buildspec, chọn Use a buildspec file, và để trống ô name, vì chỉ cần đặt lại tên nếu không để file ở root folder hoặc dùng tên khác
![](/images/2023-07-09-13-48-27.png)

9. Những phần còn lại để nguyên và chọn **Create build project**. Vậy là bạn đã hoàn tất các bước để có 1 pipeline tự động lấy code từ Github, buil docker image và push lên ECR repo.

