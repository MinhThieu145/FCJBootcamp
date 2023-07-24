---
title : "Giới thiệu và Chuẩn bị"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 1 </b> "
---

## Giới thiệu tổng quát
Chào mừng các bạn đến với Workshop 1. Trong bài workshop này, mình sẽ thiết kế kiến trúc cho 1 crawler đơn giản để bạn có thể crawl job postings trên Indeed. Bài lab này sẽ chia làm 3 phần chính:

### 1. Thiết kế Pipeline CI/CD
Phần 1 của bài lab sẽ là về qui trình CI/CD của crawler. Mình sẽ sử dụng **CodeBuild** để tự động lấy code từ Githubm từ đó build Docker image cho crawler và tự động đẩy image vào ECR. Phần kiến trúc sẽ thiết kế như sau:

![](/images/third.png)

### 2. Thiết kế kiến trúc cho crawler
Phần 2 của bài lab, cũng là phần chính, sẽ là về việc chạy crawler dưới dạng Docker image bằng **Fargate**. Mình cũng sẽ cung cấp code cho crawler. Crawler được viết bằng Python và Selenium. Bạn cũng có thể mở rộng để tạo crawler cho các website khác hoặc sửa đổi crawler hiện tại theo ý muốn. Phần kiến trúc bao gồm **AWS EventBridge** để có thể chạy crawler theo lịch trình, **AWS Lambda** để gửi job definition vào job queue trong **AWS Batch**. Sau khi hoàn thành sẽ chứa kết quả vào S3. Kiến trúc thiết kế như sau:

![](/images/second.png)

### 3. Thiết kế 1 webapp front-end để hiển thị kết quả
Phần 3 của bài lab sẽ chú trọng vào việc thiết kế 1 high-availability (sẵn sàng cao) webapp để hiển thị kết quả crawler. Mình sẽ sử dụng Streamlit và viết bằng Python. Webapp sẽ được đặt trong Ec2. Kiến trúc thiết kế như sau:
![](/images/forth.png)

