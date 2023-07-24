---
title : "Setup repo cho AWS ECR"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 1.2 </b> "
---

Chúc mừng bạn đã chuẩn bị xong Github repo của mình. Đây sẽ repo để chứa crawler của bạn và dùng trong CI/CD pipeline sau này. Trong bài này, mình sẽ tạo AWS ECR repo để chứa image sau khi build xong từ Codebuild.
{{% notice note %}}
*Sơ lược về dịch vụ AWS ECR:* Đây là 1 dịch vụ của AWS, cho phép quản lý, lưu trữ và triển khai các container. Dịch vụ này được dùng với các dịch vụ chạy Conatiner như AWS ECS, AWS EKS, AWS Fargate, AWS Batch,... Trong bài workshop này thì mình dùng AWS ECR cùng với AWS Batch
{{% /notice %}}

## Tạo repo trên AWS ECR

Lên AWS, tìm AWS ECR -> chọn Create repository. Các setting bạn để như sau
- **Visibility:** Chọn chế độ private. Mình từng gặp lỗi không thể pull image được nếu để là public, nên recommend đặt là private
- **Repository name:** Đặt tên cho repo, bạn có thể thấy được link repo. 

![](/images/2023-07-09-09-56-40.png)

Trong phần **Repository name**, bạn sẽ thấy một chỗ để điền tên. Phần còn lại chính là URI dẫn tới repo của bạn. Mình sẽ đặt tên repo là *indeed-scraper*, nên link dẫn tới repo của mình sẽ là:
```yaml
238101178196.dkr.ecr.us-east-1.amazonaws.com/indeed-scraper
```
Bạn có thể thấy link được tách làm nhiều phần. Trong đó, dãy số đứng đầu `238101178196` là account Id của bạn. Sau chữ `ecr` là region sử dụng. Mình sử dụng region là **us-east-1**. Cuối cùng là tên bạn tự đặt, của mình là `indeed-scraper`

Ở 3 options còn lại, bạn có thể để là disable
![](/images/2023-07-09-10-07-01.png)

Sau khi tạo xong, bạn có thể copy URI của repo vừa tạo và paste vào file **buildspec.yml** ở bước 2. Đây là phần mình bảo để trống ban nãy do chưa tạo repo
![](/images/2023-07-09-10-14-49.png)
