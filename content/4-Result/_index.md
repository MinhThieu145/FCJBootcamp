---
title : "Results"
date :  "`r Sys.Date()`" 
weight : 4 
chapter : false
pre : " <b> 4. </b> "
---
## Results
Congratulations to you. So you have reached the last step. The rest is to enjoy the results.

1. Go back to EC2 and select Load Balancer. 
![](/images/2023-07-10-00-23-58.png)

2. Copy DNS name from the newly created Load Balancer
![](/images/2023-07-10-00-26-31.png)

3. It will look like this
`CDKjobScrapingFrontendlb-1591468448.us-east-1.elb.amazonaws.com`
Add 8501 port to the rear 
`CDKjobScrapingFrontendlb-1591468448.us-East-1.elb.amazonaws.com:8501`

4. If you are on a page like this, congratulations on your success
![](/images/2023-07-10-00-28-26.png)
