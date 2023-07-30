---
title : "Dùng SDK và CLI với Translate"
date :  "`r Sys.Date()`" 
weight : 3
chapter : false
pre : " <b> 4.2. </b> "
---

## Dùng AWS Translate với SDK

1. Bạn có thể sử dụng boto3 để tương tác với AWS SDK. Mình sẽ sử dụng Python, nhưng boto3 cũng có thể sử dụng với Java hay Java.

2. Để sử dụng SDK với AWS boto3, bạn cần tạo 1 file python và import boto3

```python
import boto3
```

3. Tiếp đến, bạn cần gọi translate client và sử dụng các hàm có sẵn của AWS Translate. Ở đây mình sẽ sử dụng hàm translate_text để dịch 1 đoạn text từ tiếng việt sang tiếng anh. Nhớ chú ý rằng translate_text có giới hạn, chỉ có thể dịch 10000 bytes.
 
```python

```python
translate = boto3.client('translate')

result = translate.translate_text(Text="Chào mọi người", 
            SourceLanguageCode="vi", TargetLanguageCode="en")
```

4. Nếu muốn dịch dài hơn, bạn cần dùng hàm translate_document. Hàm này có thể dịch các file .txt, .docx và .html. Ở đây mình sẽ dịch 1 file .txt từ tiếng việt sang tiếng anh.

```python
translate = boto3.client('translate')


result = translate.translate_document(
    Document={
            "Content": data,
            "ContentType": "text/html"
        },
    SourceLanguageCode='vi',
    TargetLanguageCode='en',
)
```

Bạn sẽ thấy rằng lần này hơi khác so với lần trước. Để dịch document, bạn không phải chỉ cung cấp Content (biến data) mà còn phải chọn ContentType. Có 3 loại ContentType: `text/html`, `text/plain` và `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (đối với file .docx).
Còn lại thì tương tự như translate_text

5. Tuy nhiên, kết quả trả về chưa phải là content bạn muốn, nó được trả về trong object. Để extract object, bạn sẽ lấy TranslatedDocument từ object và parse ra file.

```python
if “TranslatedDocument” in result:
  fileName = localFile.split(“/”)[-1]
  tmpfile = f”{args.TargetLanguageCode}-{fileName}”
  with open(tmpfile, ‘w’, encoding=’utf-8′) as f:

  f.write(str(result[“TranslatedDocument”][“Content”]))

```

## Dùng AWS Translate với CLI
1. Để sử dụng AWS Translate với CLI, bạn cần cài đặt AWS CLI. Bạn có thể kiểm tra bản thân có cài đặt AWS CLI chưa bằng cách gõ lệnh sau:

```bash
aws --version
```

2. Nếu chưa cài đặt, bạn có thể cài đặt bằng cách gõ lệnh sau:

```bash
pip install awscli
```

3. Sau khi cài đặt xong, bạn cần cấu hình AWS CLI. Bạn có thể cấu hình bằng cách gõ lệnh sau:

```bash
aws configure
```

4. Bạn cần nhập Access Key ID, Secret Access Key, Default region name và Default output format. Bạn có thể lấy Access Key ID và Secret Access Key bằng cách vào AWS Console, chọn IAM, chọn Users, chọn User mà bạn muốn lấy Access Key ID và Secret Access Key. Sau đó chọn tab Security credentials, chọn Create access key. Bạn có thể chọn Show Access Key để xem Access Key ID và Secret Access Key. Bạn có thể chọn Download .csv file để tải file chứa Access Key ID và Secret Access Key về.

5. Sau khi cấu hình xong, bạn có thể sử dụng AWS CLI với AWS Translate. Bạn có thể sử dụng lệnh sau để dịch 1 đoạn text từ tiếng việt sang tiếng anh. Bạn có thể thấy nó khá tương tự với hàm translate_text của boto3.

```bash
aws translate translate-text --text "Chào mọi người" --source-language-code vi --target-language-code en
```

6. Tất nhiên, bạn cũng có thể sử dụng lệnh sau để dịch 1 file .txt từ tiếng việt sang tiếng anh. Bạn có thể thấy nó khá tương tự với hàm translate_document của boto3.

```bash
aws translate translate-document –source-language-code vi –target-language en
–document-content fileb://source-lang.txt
–document ContentType=text/plain
–query “TranslatedDocument.Content”
–output text | base64
–decode > target-lang.txt

```
Tuy khá tương tự với aws_translate của boto3, tuy nhiên, điểm khác biệt chính là phần document-content. Sau chữ `file://`, bạn cần thêm path dẫn tới file của bạn vào đây. Còn lại thì tương tự như aws_translate của boto3.


