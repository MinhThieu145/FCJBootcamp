---
title : "Giới thiệu và Chuẩn bị"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 1 </b> "
---

## Giới thiệu tổng quát
Chào mừng các bạn đến với Workshop 1 "phẩy" 5. Đây là 1 phần phụ của workshop 1. Trong worshop nhỏ này, mình sẽ hướng dẫn các bạn làm 2 việc khá là cần thiết cho việc làm lab của các bạn:

### 1. Cấu hình AWS Budget để cảnh báo và ngăn chặn việc tốn thêm chi phí
Phần 1 của bài lab sẽ là về cách các bạn có thể cấu hình phần cành báo cho tài khoản của bạn. Đồng thời, khi vượt qua ngưỡng đó, bạn có thể gắn IAM role vào tài khoản admin để ngăn bản thân tiếp tục "phá".

{{% notice warning %}}
Đây là phần bạn tuyệt đối không được bỏ qua. Dù bạn bắt đầu làm lab hay đã làm 1 vài bài rồi, thì cũng tuyệt đối không được làm tiếp trước khi thực hiện phần này. Mình báo trước rồi đấy nhé!
{{% /notice %}}


### 2. CI/CD pipeline để tự động build và deploy hugo website
Phần 2 của bài lab sẽ đi qua từng bước cần thiết để có thể tự động build và deploy website lên S3. Hiện tại, mỗi lần muốn update website viết bằng Hugo theme, mình sẽ phải build lại rồi upload thủ công lên S3. Đây là việc tốn công sức và không cần thiết. Nên mình sẽ đi qua cách tự động phần này bằng CodePipeline và CodeBuild.


## Giới thiệu dịch vụ
Trong workshop này, mình sẽ đi qua 3 dịch vụ chính: 

**1. AWS IAM (AWS Identity and Access Management)**

Đây là 1 dịch vụ rất quan trọng của AWS, cho phép các bạn quản lý:
- user: những người mà bạn cho phép truy cập vào tài khoản AWS của bạn
- role: cấu hình quyền truy cập của các user và service của AWS. Trong bài lab này thì mình sẽ cấu hình admin access và "admin deny" (thật ra là deny full các dịch vụ)
- policy: cấu hình chi tiết quyền truy cập của các user và role. Trong bài lab này thì mình sẽ cấu hình policy cho user admin và user admin deny

**2. AWS CodePipeline** 

Đây là dịch vụ CI/CD của AWS, cho phép các bạn tự động test, build và deploy code. Trong bài lab này, mình sẽ fetch code từ Github, build và deploy lên S3.

**3. AWS S3**

Đây là dịch vụ lưu trữ của AWS, cho phép các bạn lưu trữ các file, folder, object. Nhưng nó cũng có chức năng cho phép host static web. Vì vậy, mình sẽ sử dụng S3 để host website của mình.
