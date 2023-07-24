---
title : "Xây dựng workshop bằng CDK"
date :  "`r Sys.Date()`" 
weight : 6
chapter : false
pre : " <b> 6. </b> "
---

## Giới thiệu tổng quát
Đây là phần bonus của workshop này. Bạn sẽ được hướng dẫn xây dựng lại workshop này bằng CDK. 

{{% notice note %}}
*Sơ lược về CDK:* Đây là 1 dịch vụ của AWS, cho phép xây dựng và triển khai các tài nguyên AWS bằng code. CDK hỗ trợ nhiều ngôn ngữ như Python, Javascript, Typescript, Java, C#,... Trong bài workshop này thì mình sẽ dùng CDK với Python. CDK tạo các stack trong Cloudformation để triển khai tài nguyên. Nên nếu gặp lỗi hay cần giám sát, bạn có thể vào AWS Cloudformation.
{{% /notice %}}

## Chuẩn bị 
1. Đầu tiên, bạn cần clone github repo chứa code CDK về. Bạn có thể dùng lệnh sau:
```bash
git clone -b cdk https://github.com/MinhThieu145/FCJBootcamp.git 
```
2. Sau đó, bạn cần setup AWS CLI để tương tác với Resource. Nếu bạn sử dụng pip thì có thể sử dụng lệnh sau để install AWS CLI: `pip install awscli`. Để kiểm tra thì bạn có thể dùng lệnh: `aws --version`
3. Sau đó, bạn cần đăng nhập vào tài khoản AWS của mình. Bạn có thể dùng lệnh sau: `aws configure`. Lệnh này sẽ yêu cầu bạn nhập Access Key và Secret Key. Bạn có thể lấy 2 key này ở phần IAM trên AWS Console.
4. Vào AWS IAM, chọn User và chọn Add User
5. Chọn User name -> Next
6. Trong tab Permission, chọn Attach policies directly -> Tìm và chọn AdministratorAccess -> Next
7. Chọn Create user

8. Vào lại IAM -> User và chọn user bạn vừa tạo. Chọn vào tab Security Credential
![](/images/2023-07-20-01-34-39.png)
9. Kéo xuống phần **Access Key** và chọn Create access key
10. Chọn **Use case** là Command Line Interface (CLI) -> Tick confirmation -> Next
11. Chọn Create access key
12. Bên cạnh nút **Done** chọn Download .csv. File này sẽ chứa Access Key và Secret Key của bạn. Bạn cũng có thể copy trực tiếp **Access Key** và **Secret access key** từ console
![](/images/2023-07-20-01-38-41.png)

13. Vào lại IDE của bạn, mở terminal lên và chạy lệnh `aws configure`. Nếu đã cài CLI thì sẽ có prompt hỏi access key và Secret access key. Paste vào là xong. Bạn cũng có thể chọn region đúng với region đang sử dụng
![](/images/2023-07-20-01-41-14.png)

14. Vậy là bạn đã hoàn thành việc đang nhập vào tài khoản AWS của mình. Bây giờ bạn có thể chạy CDK được rồi.   