---
title : "Tạo tài nguyên: ALB và ASG"
date :  "`r Sys.Date()`" 
weight : 2 
chapter : false
pre : " <b> 3.2. </b> "
---

Sau khi hoàn tất quá trình tạo VPC, bạn cần tạo thêm các tài nguyên trong VPC. Trong bài này, mình sẽ tạo những tài nguyên sau:

 - Launch Template: Đây giống như 1 bản vẽ. Những instace được tạo ra từ ASG sẽ giống với bản vẽ này. Và để tạo ra Launch Template với đầy đủ các packages cần thiết, mình sẽ tạo sẵn một AMI

{{% notice note %}}
*Sơ lược về Amazon Machine Image (AMI):* Có thể hiểu AMI là bản vẽ của instance. Khi tạo 1 EC2 instance mới, bạn được hỏi chọn AMI. Đa phần bạn sẽ dùng **base image**, những AMI được cung cấp bởi AWS như là ubuntu, linux hay window. Tuy nhiên, nếu muốn EC2 được tạo với các package có sẵn, ta có thể tạo **custom image**. 
{{% /notice %}}

 - ASG: Tạo ASG bằng Launch Template phía trên
 - ALB: Tạo ALB để điều hướng request


## Tạo Custom AMI và Launch Template
Khi các Instance được khởi tạo từ ASG, chúng cần 1 khuông mẫu (template). Để tạo ra 1 launch template, trước tiên ta cần tạo 1 custom AMI với tất cả package cần thiết.

1. Vào Ec2, chọn **Launch Template** rồi chọn **Create launch template**
![](/images/2023-07-09-22-27-45.png)

2. Đặt tên cho template rồi chọn option **Auto Scaling guidance** để thuận tiện tích hợp với ASG sau này. 
![](/images/2023-07-09-22-30-02.png)

3. Chọn AMI, bấm vào Browse more AMIs
![](/images/2023-07-09-22-31-32.png)

4. Nhập số `238101178196` vào thanh tìm kiếm rồi chọn **Community AMI**, bạn nên thấy 1 AMI với tên như hình dưới. Đây là AMI mình public, chữa sẵn các file chạy server. Nếu thực hiện đúng như các bước trước, đặt biệt là cách đặt tên bucket của S3, bạn có thể sử dụng mà không cần thay đổi gì. 
![](/images/2023-07-09-22-45-00.png)


{{% notice info %}}

Bên trong AMI cài sẵn 1 streamlit server với cổng 8501, đồng thời lưu kết quả vào S3 trong Bucket tên là **job-description-process**, và lấy từ folder tên **indeed-scraper**

{{% /notice %}}

5. Chọn select AMI đó, bạn sẽ được đưa lại chỗ template để tiếp tục. Ở phần **Instance Type** chọn **t2.micro**. Ở phần Key pair chọn 1 key pair mà bạn đã có sẵn để sau này thuận tiện SSH vào instance (tất nhiên là phải qua Bastion Host)
![](/images/2023-07-09-22-48-34.png)

6. Phần Network Settings bạn có thể để trống (không chọn gì cả)
![](/images/2023-07-09-22-54-18.png)


7. Bạn có thể để những phần còn lại default.

8. Ở **Advanced details**, expand ra và chọn vào **Create new IAM profile**, do Frontend app cần 1 vài roles (Truy cập S3 và đọc Ec2). Tạo 1 role mới có các policies như sau
![](/images/2023-07-10-00-17-40.png)

9. Sau khi tạo xong, quay lại template, reload (cái mũi tên tròn bên cạnh) để thấy role vừa tạo và chọn
![](/images/2023-07-10-00-19-03.png)

10.  Sau đó chọn **Create launch template** để tạo template.

## Tạo Auto Scaling Group

1. Vào Ec2, kéo xuống cuối cùng để thấy được ALB.
![](/images/2023-07-09-20-10-07.png)

2. Chọn Create Auto Scaling Group và chọn tên cho ASG. Sau đó trong phần **Launch Template**, chọn Template mà bạn tạo ban nãy, chọn version là Latest
![](/images/2023-07-19-22-49-00.png)

1. Ở tab Network, chọn VPC mà bạn tạo ban nãy. Trong VPC đó, chọn **cả hai Private Subnet** mà bạn tạo ban nãy. Ta sẽ đặt ứng dụng ở Private Subnet để tăng tính bảo mật, Public Subnet chỉ để tạo NAT Gateway và đặt Bastion Host. Bấm next
![](/images/2023-07-09-23-14-06.png) 

1. Ở tab Load Balancing, chọn **Attach to new load balancer** . Bên trong tab mới mở, chọn **Application Load Balancer**, chọn tên cho Load Balancer và chọn **Internet-facing**
![](/images/2023-07-09-23-21-12.png)  

1. Kế đến là phần Network mapping, VPC sẽ được giữ nguyên như của ASG (tất nhiên, ELB để handle traffic vào ASG nên cần phải chung VPC rồi). Bạn cần chọn 2 **Public Subnet** để đặt ELB
![](/images/2023-07-09-23-25-46.png)

1. Ở phần Listener và Routing, chọn **Port** là **8501** cho Streamlit, và chọn **Create a target Group** và đặt tên cho target group
![](/images/2023-07-09-23-29-21.png)

1. Trong phần Health checks, chọn option **Turn on Elastic Load Balancing health checks**. Đồng thời đặt **Health check grace period** là 300s. Đây là thời gian ước lượng để Ec2 khởi động (đây là cách để Ec2 instance tránh bị destroy khi chưa khởi động xong. Nếu User Data khiến instance mất thời gian khởi động, hãy ước lượng thời gian cần thiết để khởi động ở đây).
![](/images/2023-07-09-23-54-26.png)

1. Để phần **Additional settings** như default và bấm Next

2. Groupsize bao gồm 3 phần: **Maximum capacity** để chỉ số instance **tối đa**, **Minimum capacity** là số instance tối thiểu, **Desired capacity** là số instance mà ASG cố giữ ở mức đó.
![](/images/2023-07-10-00-01-22.png)

1.  Để trống phần Scaling policies và chọn Next

2.  Bỏ qua phần **Add notifications** và chọn Next. Bỏ qua tags và next rồi chọn Create Auto Scaling Group

