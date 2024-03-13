# Confluent CLI
## Create resources
### Create a confluent cluster
``` sh
confluent kafka cluster create ksql_cluster --cloud "aws" --re
gion "ap-southeast-2"

+----------------------+--------------------------------------------------------------+
| Current              | false                                                        |
| ID                   | lkc-qpmnr6                                                   |
| Name                 | ksql_cluster                                                 |
| Type                 | BASIC                                                        |
| Ingress Limit (MB/s) | 250                                                          |
| Egress Limit (MB/s)  | 750                                                          |
| Storage              | 5 TB                                                         |
| Provider             | aws                                                          |
| Region               | ap-southeast-2                                               |
| Availability         | single-zone                                                  |
| Status               | PROVISIONING                                                 |
| Endpoint             | SASL_SSL://pkc-ldvj1.ap-southeast-2.aws.confluent.cloud:  9092 |
| REST Endpoint        | https://pkc-ldvj1.ap-southeast-2.aws.confluent.cloud:443     |
+----------------------+--------------------------------------------------------------+
```



## Setup & Prep Steps
Tutorial: https://www.youtube.com/watch?v=oI7VAS9KSS4&t=4s
### Login
``` zsh
confluent login
````

### Configure environment
```
confluent environment list             

  Current |     ID     |        Name        | Stream Governance Package  
----------+------------+--------------------+----------------------------
          | env-r2px59 | learn-kafka-python | ESSENTIALS                 
  *       | env-xr2y3k | default            | ESSENTIALS   
```
E.g: Using *learn-kafka-python* with id *env-r2px59*
``` sh
confluent environment use env-r2px59 
```

### Configure Cluster
``` sh
confluent kafka cluster list
confluent kafka cluster use lkc-1nvqgz
```

### Configure API key
``` sh
# Store API in in local CLI state
confluent api-key store <key> <secret>
# Use the key over the selected cluster
confluent api-key use <key> --resource <cluster_id>
```

### Consumer CLI
#### Consume
``` sh
confluent kafka topic consume <topic_name> --from-beginning
```

#### Reset Offset
