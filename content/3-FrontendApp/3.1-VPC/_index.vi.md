---
title : "Thiết kế môi trường mạng"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 3.1. </b> "
---

Bước đầu tiên chính là thiết kế môi trường mạng cho app. Như đã để cập trước đó, đây là những tài nguyên mình sẽ tạo:
 - 2 public subnet, 2 private subnet
 - 1 VPC
 - 1 Internet Gateway
 - 1 NAT Gateway (có thể tạo 2 NAT Gateway nếu muốn an toàn hơn - mỗi NAT ở 1 subnet)
 - S3 Endpoint để truy cập S3 mà không cần đi qua NAT Gateway

## Setup VPC và subnet

1. Chọn VPC, Create VPC. Chọn vào option **VPC and more**. Đặt tên cho VPC. Bạn có thể để defaul CIDR: 10.0.0.0/16, bạn cũng có thể thay CIDR để tăng giảm số lượng IP trong VPC. Bạn có thể để IPV6 như default (không dùng IPV6)
![](/images/2023-07-09-19-21-49.png)

1. **Number of Availability Zones:** số AZ mà VPC sẽ được tạo. Theo diagram, mình sẽ để 2 AZ. Bạn cũng có thể chọn Customize AZs để chọn sang những AZ khác (default là us-east-1a và us-east-1b nếu dùng us-east-1)
![](/images/2023-07-09-19-30-53.png)

1. **Number of public subnets:** bao nhiêu public subnet trong VPC. Mình cần 2 public subnet (mỗi AZ 1 public subnet) nên sẽ để 2. Đồ thị ở bên phải cũng chỉ rõ ra từng phần của public subnet: mỗi AZ có 1 subnet, subnet được thông qua Route table để nối đến Internet Gateway.
![](/images/2023-07-09-19-33-45.png)

1. **Number of private subnets:** bao nhiêu private subnet trong VPC. Mình cũng cần 2 private (1 AZ 1 private). Nếu chọn 4, bạn có thể thấy số lượng private subnet tăng lên 1 ở mỗi AZ 
![](/images/2023-07-09-19-36-30.png)

1. **Customize subnets CIDR blocks:** Bạn có thể điều chỉnh thông số này để tăng giảm số địa chỉ IP mỗi subnet. Hiện tại, mỗi submet có 4096 IP
![](/images/2023-07-09-19-39-17.png)

1. **NAT gateways ($)** Đây là phần khá tốn kém. Nếu muốn an toàn và đúng theo diagram, bạn có thể chọn **1 per AZ** để mỗi AZ có 1 NAT. Bạn cũng có thể chọn **In 1 AZ** để chỉ tạo 1 NAT gateway cho cả 2 private subnet.

2. **VPC endpoints** Nên chọn để giảm chi phí truy cập S3. Do nếu bạn dùng boto3 mà không có Endpoint thì phải buộc đi qua NAT (do dữ liệu truyền ra internet). Việc có Endpoint sẽ giảm chi phí này NAT (nếu thực sự không cần Internet) và phí data transfer.

3. **DNS option** chọn cả 2 options

4.  Chọn **Create VPC** để hoàn thành.


