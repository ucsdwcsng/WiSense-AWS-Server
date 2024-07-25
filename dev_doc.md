## EC2 termination protection should be used if necessary

## setup DB requirement
1. Installing Boto3
```
pip install boto3
```
2. need to put Boto3 in the working directory 

```
pip install boto3 -t .
```

3. csi msgs come with 1024 columns

4. DB throughput should be set!

### data collection script

simpler vers.: 
    RPi will put packet info on dynamoDB, and put csi in CSV. In the entry from dynamoDB, there will be pointer to the CSV file uploaded to the s3bucket, with row number. 
    so data will be at 2*count + 1 and 2*count + 2
ultimate vers.: from DB there's hyperlink pointer to the corresponding s3 buckets. In DB there's basic info for packets, except csi.