---
title : "Tạo Webapp Frontend để xem kết quả"
date :  "`r Sys.Date()`" 
weight : 3 
chapter : false
pre : " <b> 3. </b> "
---

## Giới thiệu tổng quan
Nếu bạn đã đến được đây, chúc mừng bạn đã gần như hoàn thành workshop. Ở các phần trước, Crawler đã có thể chạy theo lịch trình và lưu kết quả vào S3. Tuy nhiên, vẫn chưa có cách nào để bạn có thể coi những kết quả ấy một cách thuận tiện, hay chia sẻ những kết quả ấy với người khác. Trong bài này, mình sẽ tiếp tục thiết kế một webapp bằng streamlit để hiển thị kết quả từ S3.

## Giới thiệu về Streamlit
Streamlit là 1 open-source library, dùng python để xây dựng các webapp. Streamlit chủ yếu được dùng để chia sẻ các kết quả của data science. Tuy nhiên, bạn có thể dùng nó để xây dựng các webapp cho mục đích khác. Streamlit có thể chạy trên local hoặc trên cloud. Trong bài này, mình sẽ chạy trên Ec2.

## Thiết kế kiến trúc
Do kiến trúc phần này hơi dài nên mình sẽ đi rất kĩ. Trước hết bạn hãy đọc thật kĩ diagram architecture của phần này. Mình sẽ đi theo thứ tự mà client sẽ đi (tức là đi từ phía client tới phía server).
![](/images/forth.png)

### 1. Application Load Balancer
Đầu tiên, user sẽ truy cập vào DNS của Application Load Balancer (ALB) thông qua trình duyệt. ALB sẽ chuyển hướng request đến các Auto Scaling Group, từ đó truy cập vào app được đặt trong private subnet. Bản thân ALB phải được đặt trong public subnet, vì nó sẽ nhận request từ internet. Còn app sẽ được đặt trong private subnet vì nó sẽ nhận request từ ALB.

{{% notice note %}}
*Sơ lược về dịch vụ AWS Elastic Load Balancer (ELB):*  ELB là dịch vụ cân bằng tải của AWS. Nó cho phép phân phối các request lên các instance để đảm bảm hiệu năng và độ tin cậy. ELB có thể giúp các instance không bị quá tải bằng cách phân chia đều request, hay sử dụng health check để tránh request đến các instance bị lỗi. Trong bài này, mình sẽ sử dụng loại cân bằng tải là **Application Load Balancer**. Đây là cân bằng tải ở layer 7, hỗ trợ phân phối dựa vào header, protocol của request.
{{% /notice %}}

### 2. Auto Scaling Group
Sau khi user truy cập đến DNS của ALB, ALB sẽ chuyển hướng request đến các Auto Scaling Group. Auto Scaling Group (ASG) sẽ chịu trách nhiệm tạo ra các instance để chạy app. Các instance được tạo ra sẽ được đặt trong private subnet.

{{% notice note %}}
*Sơ lược về dịch vụ AWS Auto Scaling Group (ASG):* AWS ASG là dịch vụ cho phép tự động mở rộng hoặc thu hẹp instance dựa trên điều kiện đặt trước và tình trạng của instance. Auto Scaling Group giúp hệ thống không bị qúa tải, cắt giảm chi phí và tăng availability. Auto Scaling Group sẽ tự động tạo thêm các EC2 istance, tăng số lượng EC2 instance khi traffic tăng và giảm số lượng EC2 instance khi traffic giảm, đồng thời thay thế các instance bị lỗi (health check failed). Các Instance này được tạo mới và xoá bỏ 1 cách tự động, nên cần có ELB để điều hướng traffic vào chúng.
{{% /notice %}}

### 3. Thiết kế hệ thống mạng cho app.
Để đảm bảo an toàn, kiến trúc được đặt trong VPC, tách làm 2 AZ. Bạn có thể thấy 2 AZ (us-east-1c và us-east-1d) giống hệt nhau. Đây là để cho hệ thống vẫn hoạt động dù AZ bị sập. Có tổng cộng 4 subnet trong VPC, 2 public và 2 private. Ở 1 trong 2 public subnet, mình đã để 1 Ec2 với mục đích làm Bastion Host. 

{{% notice note %}}
*Bastion Host* là cách bảo vệ hệ thống tốt hơn bằng việc đặt resource trong private subnet, và truy cập từ ngoài sẽ phải đi qua Bastion Host để vào đến bên trong (truy cập SSH, còn lại nếu dùng DNS của ALB thì đi qua ALB).  
{{% /notice %}}
2 Private subnet còn lại, mình đặt ASG. ASG sẽ tự động tạo các Ec2 instance trong 2 private subnet này và điều hướng request của mình từ ngoài vào đó.