---
title : "Cấu hình AWS Budget"
date :  "`r Sys.Date()`" 
weight : 3
chapter : false
pre : " <b> 2.2 </b> "
---

Sau khi hoàn thành chuẩn bị role, bạn cần cấu hình budget để cảnh báo khi chi phí vượt ngưỡng và apply policy khi vượt quá ngưỡng quy định.

1. Bạn vào AWS, tìm AWS Budgets, sẽ thấy giao diện như sau. Như bạn đã thấy, tháng này mình lố budget 'sương sương' 1364%, do mình chỉ cho budget là 5$ thôi. 

![](/images/2023-07-29-11-39-06.png)

2. Chọn Create budget, bạn sẽ thấy màn hình setup budget. Mình cần nhiều hơn mức template nên chọn Customize bạn nhé

![](/images/2023-07-29-11-41-20.png)

3. Trong phần Budget Type, bạn có thể thấy có 4 phần. 
- Cost Budget: monitor chi phí của AWS tháng đó. Mình sẽ sử dụng option này nhé
- Usage Budget: monitor usage của AWS tháng đó. Ví dụ như bạn monitor Ec2 instance chạy bao nhiêu giờ,...
- Saving Plan và Reservation: mình sẽ để phần này lại sau
- 
![](/images/2023-07-29-11-44-29.png)

4. Sau khi chọn Next, bạn cần đặt tên cho Budget của mình. Sau đó xuống tab, Set budget amount, bạn có thể thấy các lựa chọn như:
- Period: theo ngày, tháng, năm hay quí. MÌnh muốn theo tháng nhé
- Budget renewal type: Bạn có muốn renew lại mỗi tháng không (AWS charge tiền mỗi tháng nhé). Hay là không bao giờ renew (Expiring Budget). Mình chọn là **Recurring budget**
- Start month: tháng bắt đầu
- Budgeting method: mình sẽ để là Fixed (cố định)
- Enter your budgeted amount ($): bạn muốn mình dùng bao nhiêu 1 tháng. Mình sẽ cho bản thân 20 usd nhé
 
![](/images/2023-07-29-11-49-28.png)

5. Phần dưới là Budget scope, mình sẽ chọn là **All AWS service**. Nhưng nếu bạn muốn áp dụng budget cho riêng 1 service, budget theo tag,... thì chọn phần Filter nhé. 

![](/images/2023-07-29-11-51-06.png)

6. Sau khi chọn Next, bạn sẽ cần chọn tiếp các thresholds (các mức) mà bạn muốn nhận cảnh báo. Chọn **Add an alert threshold** để bắt đầu nhé.

![](/images/2023-07-29-11-52-18.png)

7. Threshold đầu tiên mà mình muốn nhận cảnh báo là khi chi phí vượt quá 50% budget. Ở dòng đầu, bạn có thể thấy các phần như:
- Threshold: ô đầu tiên để nhập giá trị, bạn có 1 dropdown bên cạnh để chọn giá trị này nghĩa là percentage (theo phần trăm budget) hay là giá trị fixed cứng. 
- Trigger: Bạn muốn được notify khi threshold này là **actual** hay **forecast**. Do AWS có thể dự đoán budget cuối tháng của bạn dựa vào chi phí hiện tại, nên bạn có thể chọn forecast để nhận cảnh báo sớm hơn.

Sau khi chọn xong sẽ có phần summary để đọc lại

![](/images/2023-07-29-11-55-42.png)

8. Email recipients, nhập email mà bạn muốn gửi thông báo khi vượt ngưỡng vào đây nhé. Mình sẽ nhập email mình

![](/images/2023-07-29-11-57-10.png)

9. Tuy nhiên, đó mới là 1 threshold, mình cần thêm mức 75% và 100& nữa. Nên bạn có thể tạo thêm bằng cách chọn vào **Add alert threshold** ở góc trái ấy. Tạo xong bạn chọn Next, mình đã tạo 3 mức threshold như sau

![](/images/2023-07-29-11-59-19.png)

10. Nhưng cảnh báo là chưa đủ, mình muốn chặn access vào resource để không phát sinh thêm chi phí. Bạn chọn vào phần **Action** của shrehold mà bạn muốn. Bạn sẽ thấy màn hình yêu cầu IAM role. Đây là role giúp cho AWS Budget thực hiện action của bạn. Chọn vào **manually create an IAM role**

11. Bạn sẽ được đưa đến màn hình tạo Role. Chọn vào Create role nhé.

![](/images/2023-07-29-12-09-20.png)

12. Chọn là AWS Service và ở phần Use case, tìm **Budget** ở dropdown và chọn vào **Budget** nhé. Sau đó chọn Next

![](/images/2023-07-29-12-10-25.png)

13. Chọn vào Create Policies nhé. Sau đó lại chọn vào JSON để tạo policy bằng JSOn

![](/images/2023-07-29-12-32-57.png)

1.  Mình cần tạo 1 policy cho phép AWS Budget có thể gán polcies cho user của mình. Bạn có thể đọc thêm ở [đây](https://docs.aws.amazon.com/cost-management/latest/userguide/billing-example-policies.html#example-budgets-IAM-SCP). Mình sẽ copy từ website của AWS và paste vào editor của mình

![](/images/2023-07-29-12-35-34.png)

15. Sau đó bạn đặt tên và hoàn thành việc tạo role nhé
![](/images/2023-07-29-12-37-29.png)

16. Sau đó quay lại phần role (thường là tab bên trái á) và tìm cái policies bạn mới tạo và chọn rồi chọn Next

![](/images/2023-07-29-12-38-42.png)

17. Sau đó đặt tên cho Role rồi Next nhé. Sau cùng quay lại nơi ban đầu, chọn nút reload rồi chọn Role bạn vừa tạo nhé

![](/images/2023-07-29-12-42-53.png)

18. Cuối cùng, chọn IAM Policy trong phần action type, rồi chọn policy full deny mà bạn tạo lúc đầu. Chọn user là admin (đây là tên tài khoản user bạn đã tạo).

![](/images/2023-07-29-12-44-46.png)

19. Chọn Yes khi hỏi bạn có muốn chạy tự động action này không (tất nhiên rồi). Vẫn dùng alert cũ (là alert 100% budget nếu bạn làm như mình). Sau đó chọn Next và Create Budget sau khi review

![](/images/2023-07-29-12-45-46.png)

20. Chúc mừng. Vậy là bạn đã hoàn tất tạo budget, đảm bảo bản thân không bị "hố" rồi