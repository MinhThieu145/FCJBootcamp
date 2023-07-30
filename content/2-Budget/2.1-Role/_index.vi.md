---
title : "Tạo Deny IAM Policy cho user"
date :  "`r Sys.Date()`" 
weight : 1 
chapter : false
pre : " <b> 2.1 </b> "
---

1. Bạn vào lại màn hình chính của AWS IAM, chọn Policies
![](/images/2023-07-29-11-26-43.png)

2. Bạn đang cần tìm 1 policy để deny truy cập vào tất cả resource, nhưng policy đó hiện không có sẵn và bạn cần tự tạo. Bạn chọn vào Create policy để tạo policy mới
![](/images/2023-07-29-11-27-30.png)

3. Ở góc phải, bạn sẽ thấy 2 chữ là JSON và Visual. Chọn vào JSON nhé, sẽ ra như sau:
![](/images/2023-07-29-11-28-31.png)

4. Phần Policy Editor cho phép bạn sửa và thêm Statement cho Policy. Mình sẽ giải thích từng phần như sau:
- Sid: đây là tên của policy đó, bạn có thể chọn vào **Add new Statement** (ngay góc trái) để thêm policy mới. Nhưng vì chỉ tạo 1 policy nên mình sẽ để mặc định là **Statement1**
- Effect: là hiệu lực của policy, có 2 giá trị là **Allow** và **Deny**. Trong trường hợp này, mình sẽ chọn **Deny**
- Action: Đây là những 'việc' mà bạn không hay được làm. Ví dụ như bạn có thể cho một người quyền xem các Lambda Function có sẵn, nhưng không cho thêm Lambda mới vào. Mình cũng sẽ chọn là `*` để tất cả các Action đều bị deny.
- Resource: Đây là phần mà bạn sẽ chọn resource nào sẽ bị deny. Mình sẽ chọn là `*` để tất cả các resource đều bị deny.
Sau khi hoàn tất, Policy của mình nhìn như sau:
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "Statement1",
			"Effect": "Deny",
			"Action": ["*"],
			"Resource": ["*"]
		}
	]
}

```

5. Sau đó chọn Next. Bạn có thêm Policy name và Description ở phần này. Bạn cũng có thể thấy phần mô tả của policy. Như policy này, nó đã **Explicit deny (384 of 384 services)** tức là từ chối truy cập vào tất cả các dịch vụ của AWS. Bạn chọn Next để tiếp tục. 

6. Vậy là bạn đã tạo xong policy để deny tất cả rồi! 