---
title : "Hoàn tất, Chạy CDK và Dọn dep"
date :  "`r Sys.Date()`" 
weight : 5
chapter : false
pre : " <b> 6.4. </b> "
---

Vậy là bạn hoàn thành được phần bonus của workshop này rồi. Sau khi hiểu các khái niệm cơ bản và các hoạt động của từng file. Bạn có thể bắt đầu tạo hệ thống bằng CDK rồi. 

## 1. Đảm bảo rằng bạn đã chuẩn bị đầy đủ 

 - Hãy vào file .env và thay đổi tuỳ vào môi trường của bạn. Đây thường là những tài nguyên mình không tạo bằng CDK được.
 - Hãy chắc rằng mình đã login vào AWS và vào tài khoản github chứa code crawler của bạn

## 2. Chạy CDK
- Bạn có thể chạy lệnh sau trong IDE để vào môi trường CDK `source .venv/bin/activate`
- Sau khi vào môi trường CDK, bạn có thể chạy lệnh sau để cài đặt các thư viện cần thiết `$ pip install -r requirements.txt`
- Sau đó, bạn có thể synth ra các file Cloudformation bằng lệnh sau: `cdk synth`
- Nếu như được yêu cầu bootstrap, bạn có thể chạy lệnh sau: `cdk bootstrap`
- Cuối cùng là deploy lên bằng lệnh sau: `cdk deploy --all` để chạy tất cả stack

## 3. Dọn dẹp

Sau khi chạy xong, nếu muốn xoá tất cả các tài nguyên, bạn có thể chạy lệnh sau: `cdk destroy --all`, Nhanh hơn rất nhiều so với thủ công đúng không