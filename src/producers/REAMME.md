# Producer Properties
## bootstrap.servers*
## client.id
- used by the brokers to indentify messages sent from the client.
- useful in logging and metrics for quotas

✅ Choosing a good client name
'We are seeing a high rate of authentication failures from IP 102.102.01.01'
vs.
'Looks like the Order Validation service is failing to authenticate. Please take a look'

## acks
## linger.ms
Wait for additional messages to batch within this time period before sending the batch.

By default, this is set 0 => 1 message/ batch

## Message Delivery Time
![alt text](https://learning.oreilly.com/api/v2/epubs/urn%3Aorm%3Abook%3A9781492043072/files/assets/kdg2_0302.png)
