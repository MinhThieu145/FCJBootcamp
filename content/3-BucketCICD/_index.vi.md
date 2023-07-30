---
title : "Tạo CI/CD Pipeline cho Hugo website"
date :  "`r Sys.Date()`" 
weight : 3 
chapter : false
pre : " <b> 3. </b> "
---

## Giới thiệu tổng quan
Trong phần này, mình sẽ đi qua từng bước để để deploy website lên S3 bằng CodePipeline và CodeBuild. Để thực hiện bài lab này, trước tiên bạn cần upload code lên Github. 

## Kiến trúc tổng quan
Code sau khi đuoọc push lên Github, sẽ được CodePipeline fetch về, sau đó sẽ được build bằng CodeBuild, và cuối cùng sẽ được deploy lên S3.

![](/images/HugoCICD.png)

