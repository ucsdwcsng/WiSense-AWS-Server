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

5. link to s3 bucket dev https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingBucket.html


### data collector script

 - In DB there's basic info for packets, except csi.

 - RPi will put packet info on dynamoDB, and put csi in a binary file. In the entry from dynamoDB, there will be file_name to the bynary file uploaded to the s3bucket, with row number. So real arrays will be at `2*row* colPerRow` and imag arrays wil be at `2*row*colPerRow + 1`


 ### data reader script
 - query data from dynamoDB by taking inputs of a start time and an end time. Returns a CSV file of those data and a txt file with all required binary files with `file_name` and `bucket_name`. 

 - Has an option to download needed binary files automatically 

 ### binary reader script 
 - takes a csv file, find csi from `/binary_data`, and insert real and imag csi to the csv file. 

