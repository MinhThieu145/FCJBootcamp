---
title : "Thiết kế AWS Batch và S3 để chạy crawler và lưu kết quả"
date :  "`r Sys.Date()`" 
weight : 2 
chapter : false
pre : " <b> 2 </b> "
---

## Giới thiệu tổng quan

Chúc mừng các bạn đã hoàn thành phần 1 của workshop. Trong phần này, mình sẽ thiết kế AWS Batch để có thể tự động lấy các image từ ECR repo mà mình đã làm ở phần trước và chạy theo lịch trình có sẵn. Mình cũng sẽ tạo S3 bucket để lưu kết quả. Những dịch vụ mà mình sẽ sử dụng trong bài này:

- **AWS Batch:** Để chạy task crawler của mình
- **AWS S3:** Để lưu trữ kết quả
- **AWS EventBridge:** Để chạy task theo lịch trình. Do nếu chỉ dùng AWS Batch, bạn sẽ phải submit job thủ công. Nên mình sẽ dùng EventBridge để tự động submit job vào Batch theo lịch trình có sẵn
- **AWS Lambda:** Tuy EventBridge có thể đặt lịch trình. Tuy nhiên, để có thêm nhiều tính năng, mình sẽ dùng Lambda để submit job vào Batch. Lambda sẽ được trigger bởi EventBridge một cách vô cùng dễ dàng. Và tự Lambda, mình sẽ dùng boto3 để kết nối với Batch và submit job.

## Giới thiệu về AWS Batch
AWS Batch là 1 dịch vụ serverless, cho phép bạn chạy các Batch job. AWS Batch sẽ tự động scale các node nhỏ hơn. Giúp bạn tiết kiệm chi phí và chạy job nhanh hơn. Mình sẽ đi qua từng phần của AWS Batch:

 - **Compute Environment:** Đây là nơi để bạn chọn compute resource phù hợp với nhu cầu của bạn. Do Batch là dịch vụ serverless nên bạn sẽ không phải setup quá nhiều
 - **Job queue:** 1 queue để chứa các job. Khi bạn submit job vào Batch, các job sẽ nằm trong queue
 - **Job definition:** là *định nghĩa* của job. Bạn có thể tưởng tượng đây là bản vẽ của job mà bạn muốn thực hiện. Khi muốn thực hiện **job definition** này, thì bạn submit nó vào queue.

## Giới thiệu về S3
Đây là dịch vụ khá nổi tiếng của AWS. S3 là dịch vụ lưu trữ dạng object. S3 có thể lưu các định dạng file khác nhau, code, video hay hình ảnh,...
