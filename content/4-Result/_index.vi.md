---
title : "Kết quả"
date :  "`r Sys.Date()`" 
weight : 4 
chapter : false
pre : " <b> 4. </b> "
---
## Kết quả
Chúc mừng bạn. Vậy là bạn đã đến được bước cuối cùng rồi. Việc còn lại là tận hưởng thành quả thôi

1. Vào lại Ec2, chọn Load Balancer. 
![](/images/2023-07-10-00-23-58.png)

2. Copy DNS name từ Load Balancer vừa tạo
![](/images/2023-07-10-00-26-31.png)

3. Nó sẽ trông như thế này
`CDKJobScrapingFrontendLB-1591468448.us-east-1.elb.amazonaws.com`
Thêm cổng 8501 vào phía sau 
`CDKJobScrapingFrontendLB-1591468448.us-east-1.elb.amazonaws.com:8501`

4. Nếu bạn ra được trang như thế này thì chúc mừng bạn đã thành công
![](/images/2023-07-10-00-28-26.png)