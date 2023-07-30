---
title : "Thiết kế S3 Bucket"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 3.1. </b> "
---

Để host được website trên S3, trước nhất ta cần 1 public bucket

1. Vào AWS S3, chọn Create Bucket. Chọn tên cho bucket và chọn region (dù S3 là dịch vụ global, bạn vẫn phải chọn region)

![](/images/2023-07-29-13-28-07.png)

2. Bucket Ownership bạn tắt ACL đi. Trong phần Public Access bạn uncheck đi phần **Block all public access**. Sau khi bạn uncheck, sẽ có một khung cảnh báo, bạn chọn vào là **acknowledge that...**. Đây chỉ để xác nhận lại rằng bạn muốn bucket này public thật. 

![](/images/2023-07-29-13-31-51.png)

3. Bạn có thể bật Bucket version nếu muốn (dù thật ra không cần thiết vì bạn deploy từ github lên rồi mà, có gì có thể dùng github revert lại). Để phần encerytion và bucket key như default rồi chọn Create bucket

![](/images/2023-07-29-13-33-35.png)

4. Sau khi tạo xong, bạn chọn vào bucket vừa tạo, chọn tab **Permissions** 

![](/images/2023-07-29-13-35-16.png)

5. Trong phần bucket policy, bạn cần paste JSON như sau. Bạn cần thay thế **awsworkshop1tran** bằng tên bucket của bạn. Buket policy nhìn khá tương tự với policy mà bạn đã tạo lúc nãy đúng không? Đúng vậy, nó cũng là một policy, nhưng nó được attach vào bucket, chứ không phải là một policy riêng biệt. Trong phần action, bạn thấy có **s3:GetObject**. Đây là một action của S3, nó cho phép user có thể lấy được object từ bucket. Trong phần resource, bạn thấy có **arn:aws:s3:::awsworkshop1tran/\***. Đây là một ARN của S3 bucket. Bạn có thể tham khảo thêm về ARN của S3 tại [đây](https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#arn-syntax-s3). Trong phần này, \* có nghĩa là tất cả các object trong bucket. Nếu bạn muốn chỉ cho phép user lấy được một object cụ thể, bạn có thể thay \* bằng tên object đó. Ví dụ, nếu bạn muốn cho phép user lấy được object có tên là **index.html**, bạn có thể thay \* bằng **index.html**.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::awsworkshop1tran/*"
        }
    ]
}
```

6. Vậy là bucket của bạn đã được public rồi. Tu>y nhiên, nó vẫn chưa thể host được website. Để host static web, bạn vào phần Properties, kéo xuống dưới cùng. Ở đó, bạn sẽ thấy phần Static Website Hosting, chọn Edit rồi chọn Enable

![](/images/2023-07-29-13-45-40.png)

7. Sau khi enable, bạn sẽ có 2 phần cần điền là: Index document và Error document - optional. Index document là tên của file index của website. Khi dùng Hugo, tên file index của website là **index.html**. Error document là tên của file error của website. Trong hugo, tên file error của website là **404.html**. Sau khi điền xong, bạn chọn Save changes

![](/images/2023-07-29-13-47-46.png)

8. Vậy là bucket của bạn đã sẵn sàng rồi. Sau khi Save, bạn có thể kéo xuống 1 lần nữa, sẽ có 1 đường link xuất hiện. Đây là đường link của website của bạn. Bạn có thể truy cập vào đường link này để xem website của bạn. Tuy nhiên, website của bạn vẫn chưa có gì cả 
![](/images/2023-07-29-13-48-59.png)