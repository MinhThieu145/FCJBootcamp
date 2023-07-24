---
title : "Thiết kế AWS Batch"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 2.1 </b> "
---

Trong bước này, chúng ta sẽ setup 1 AWS Batch hoàn chỉnh để chạy job. Để sử dụng AWS Batch, bạn cần tạo các components mà mình đã đề cập ở bài trước:
 - Compute Environments
 - Job Queues
 - Job Definitions

## Batch Wizard 
Để thuận tiện hơn thì nên sử dụng wizard thay vì tạo từng components riêng lẻ. Vào AWS Batch, chọn Wizard. Nếu bạn muốn có nhiều lựa chọn có thể dùng EC2, hoặc EKS nếu dùng Kubernete. Nhưng để thuận tiện, mình sẽ dùng Fargate. 
![](/images/2023-07-09-16-30-24.png)

## Compute Environment
1. Chọn tên cho compute env
![](/images/2023-07-09-16-33-46.png)

2. **Spot Instance** có thể giúp tiết kiệm chi phí, thế nhưng những task chạy bằng spot instance có thể bị ngắt đoạn giữa chừng, chỉ nên dùng nếu task ngắn hoặc có thể thay thể bởi những job khác. Mình sẽ chọn không trong bài này. Đồng thời chọn vCPU tối đa, có thể để 4 vCPU.
![](/images/2023-07-09-16-36-32.png)

3. Đến bước Network Configuration, bạn có thể setup như sau
- Tạo 1 **VPC** với 1 **public subnet**
- Nhớ tạo thêm Internet Gateway và Route table để Subnet truy cập được vào internet
- Tạo 1 **security group** cho compute env, mở outbound traffic ra internet (default là mở rồi nên không cần sửa)
- Thêm các phần đã tạo vào compute env
![](/images/2023-07-09-16-43-52.png)

4. Chọn next để tạo compute env

## Job Queue
1. Chọn tên cho job queue
2. Đặt **Priority** là 1. Đây là thứ tự ưu tiên, trong trường hợp bạn có nhiều job queue trong **cùng một compute env**, job queue có priority cao sẽ được chạy trước.
![](/images/2023-07-09-16-46-28.png)

## Job Definition
1. Chọn tên và timeout cho job definition. **Timeout** là thời gian chạy tối đa của 1 job. Nếu job chạy quá thời gian này thì sẽ bị dừng. Mình ước lượng job của mình cần ít hơn 15 phút nên mình để 15 phút (900s).
![](/images/2023-07-09-16-48-18.png)

2. Fargate, bạn để **version** là LATEST, bật **Public IP** vì job cần truy cập vào Internet. **Ephemeral storage** là dung lượng của Fargate, để từ 21GB đến 200GB. Execution role để giúp cho task của bạn có thể truy cập vào ECR để pull image từ đó, đọc Secret từ Secret Manager và 1 vài role low level.
![](/images/2023-07-09-16-52-35.png)

3. trong Container configuration, ở phần image, bạn cần vào ECR, copy URI của ECR repo mà bạn tạo trước đó
![](/images/2023-07-09-17-05-30.png)
Paste vào phần **Image** của Batch Wizard và **thêm latest vào phía sau** để có thể lấy image mới nhất 
![](/images/2023-07-09-17-08-53.png)

4. Phần tiếp theo là command. Bạn có thể thêm command cho Docker Image của bạn. Command này sẽ **không** overwrite CMD hay ENTRYPOINT trong docker của bạn, mà sẽ thêm vào. Vì mình không cần thêm gì nên sẽ để default, câu lệnh default chỉ để in ra Hello World
![](/images/2023-07-09-17-15-14.png)

5. Có vẻ hơi kì lạ khi có tận 2 role trong phần job definition, tuy nhiên, theo [lời giải thích](https://repost.aws/questions/QU73a6ZU6RQg-CNJ-25i_i_Q/which-role-do-i-have-to-use-for-the-fargate-tasks-on-aws-batch) tại đây. Nếu Task của bạn cần quyền high level hơn như truy cập S3(những quyền mà không phải task nào cũng cần), thì bạn có thể để ở **job role**, còn những quyền thấp hơn như pull image từ ECR thì có thể cố định ở **execution role**. Task của mình cần truy cập vào S3 nên sẽ tạo 1 role Full Access S3, tuy nhiên nếu không cần gì ngoài chạy task thì bạn có thể đê trống (chọn None). Đồng thời bạn cần chọn vCPU và Memory
![](/images/2023-07-09-17-25-46.png)

6. Chọn tên cho Job của bạn. Khi mà chạy thì tên này sẽ được hiển thị.
![](/images/2023-07-09-17-29-22.png)

7. Sau khi hoàn thành, chọn Review và Create Resource. Vậy là bạn đã hoàn thành việc setup AWS Batch. Để kiểm tra, bạn có thể vào Job Definition và chọn Submit new Job

