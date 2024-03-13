# ksql Quickstart
## Docker
https://ksqldb.io/quickstart.html?_ga=2.76905109.1454369345.1709431648-68509756.1709095362&_gac=1.217680356.1709684517.CjwKCAiAopuvBhBCEiwAm8jaMTL5rL9fb-XBzYAf_aQ8lMfpfC_weaBik0hivTmUUu2MAQ4YCmMnIRoCwmAQAvD_BwE

```
docker-compose up -d
docker-compose ps
NAME              IMAGE                                             COMMAND                  SERVICE           CREATED          STATUS          PORTS
broker            confluentinc/cp-kafka:7.6.0                       "/etc/confluent/dock…"   broker            14 seconds ago   Up 13 seconds   0.0.0.0:9092->9092/tcp, 0.0.0.0:9101->9101/tcp
connect           cnfldemos/cp-server-connect-datagen:0.6.4-7.6.0   "/etc/confluent/dock…"   connect           14 seconds ago   Up 12 seconds   0.0.0.0:8083->8083/tcp, 9092/tcp
control-center    confluentinc/cp-enterprise-control-center:7.6.0   "/etc/confluent/dock…"   control-center    14 seconds ago   Up 12 seconds   0.0.0.0:9021->9021/tcp
ksql-datagen      confluentinc/ksqldb-examples:7.6.0                "bash -c 'echo Waiti…"   ksql-datagen      14 seconds ago   Up 12 seconds   
ksqldb-cli        confluentinc/cp-ksqldb-cli:7.6.0                  "/bin/sh"                ksqldb-cli        14 seconds ago   Up 12 seconds   
ksqldb-server     confluentinc/cp-ksqldb-server:7.6.0               "/etc/confluent/dock…"   ksqldb-server     14 seconds ago   Up 12 seconds   0.0.0.0:8088->8088/tcp
rest-proxy        confluentinc/cp-kafka-rest:7.6.0                  "/etc/confluent/dock…"   rest-proxy        14 seconds ago   Up 12 seconds   0.0.0.0:8082->8082/tcp
schema-registry   confluentinc/cp-schema-registry:7.6.0             "/etc/confluent/dock…"   schema-registry   14 seconds ago   Up 13 seconds   0.0.0.0:8081->80

docker exec -it ksqldb-cli ksql http://ksqldb-server:8088
```
## Confluent Cloud
### Create ksqlCluster
💡 `credential-identity` can be found at Confluent Cloud > Accounts > Settings > Identity

``` sh
confluent ksql cluster create my-ksql-cluster-1 --credential-identity u-1krjz6

[WARN] Confirm that the users or service accounts that will interact with this cluster have the required privileges to access Schema Registry.
+-------------------------+--------------------------------------------------------------+
| ID                      | lksqlc-d1735z                                                |
| Name                    | my-ksql-cluster-1                                            |
| Topic Prefix            | pksqlc-383k8o                                                |
| Kafka                   | lkc-1nvqgz                                                   |
| Storage                 | 500                                                          |
| Endpoint                | https://pksqlc-383k8o.ap-southeast-2.aws.confluent.cloud:443 |
| Status                  | PROVISIONED                                                  |
| Detailed Processing Log | true                                                         |
+-------------------------+--------------------------------------------------------------+
```
### Work on ksqlCluster
#### Create API Key
``` sh 
export KSQL_CLUSTER_ID=lksqlc-d1735z
confluent api-key create --resource $KSQL_CLUSTER_ID
+------------+------------------------------------------------------------------+
| API Key    | J564VN67RYH5GKUK                                                 |
| API Secret | J+NQRRqwBr8bhL4kI48ZL//3uPkBhqhnw+n0ylTgfjrkWUcA4/F+/NAqoUToz2qS |
+------------+------------------------------------------------------------------+
```

#### Set variables
``` sh
export KSQL_API_KEY="J564VN67RYH5GKUK"
export KSQL_API_SECRET="J+NQRRqwBr8bhL4kI48ZL//3uPkBhqhnw+n0ylTgfjrkWUcA4/F+/NAqoUToz2qS"
export KSQL_ENDPOINT="https://pksqlc-383k8o.ap-southeast-2.aws.confluent.cloud:443"
```

#### Start an interactive ksqlDB CLI
```
docker run --rm -it confluentinc/ksqldb-cli:0.29.0 ksql \
       -u $KSQL_API_KEY \
       -p $KSQL_API_SECRET \
       "$KSQL_ENDPOINT"
```
### ksql
#### Set session parameters

``` sql
SET 'auto.offset.reset'='earliest';
```

#### JSON
<details>
<summary> Sample Data </summary>

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30,
    "rating": 1,
    "address": {
      "street": "123 Main St",
      "city": "Anytown",
      "state": "CA",
      "zip": "12345"
    }
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "age": 25,
    "rating": 1,
    "address": {
      "street": "456 Maple Ave",
      "city": "Somewhere",
      "state": "NY",
      "zip": "67890"
    }
  },
  {
    "id": 3,
    "name": "Bob Johnson",
    "email": "bob.johnson@example.com",
    "age": 35,
    "rating": 2,
    "address": {
      "street": "789 Oak Dr",
      "city": "Elsewhere",
      "state": "TX",
      "zip": "11223"
    }
  },
  {
    "id": 4,
    "name": "Alice Williams",
    "email": "alice.williams@example.com",
    "age": 28,
    "rating": 4,
    "address": {
      "street": "321 Pine St",
      "city": "Here",
      "state": "FL",
      "zip": "44556"
    }
  },
  {
    "id": 5,
    "name": "Charlie Brown",
    "email": "charlie.brown@example.com",
    "age": 32,
    "rating": 5,
    "address": {
      "street": "654 Elm St",
      "city": "There",
      "state": "WA",
      "zip": "77889"
    }
  }
]

```
</details>

<details>
<summary> ksql Stream </summary>

``` sh
ksql> create stream userprofile_stream (id int, name varchar, email varchar, age int, rating int, address varchar) with (value_format='JSON', KAFKA_TOPIC='topic-use
rprofile-0');

 Message        
----------------
 Stream created 
----------------
ksql> select * from userprofile_stream;
+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+
|ID                       |NAME                     |EMAIL                    |AGE                      |RATING                   |ADDRESS                  |
+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+
|1                        |John Doe                 |john.doe@example.com     |30                       |1                        |{"street":"123 Main St","|
|                         |                         |                         |                         |                         |city":"Anytown","state":"|
|                         |                         |                         |                         |                         |CA","zip":"12345"}       |
Query Completed
Query terminated
ksql> select * from userprofile_stream;
+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+
|ID                       |NAME                     |EMAIL                    |AGE                      |RATING                   |ADDRESS                  |
+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+
|1                        |John Doe                 |john.doe@example.com     |30                       |1                        |{"street":"123 Main St","|
|                         |                         |                         |                         |                         |city":"Anytown","state":"|
|                         |                         |                         |                         |                         |CA","zip":"12345"}       |
Query Completed
Query terminated
ksql> select * from userprofile_stream emit changes;
+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+
|ID                       |NAME                     |EMAIL                    |AGE                      |RATING                   |ADDRESS                  |
+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+-------------------------+
|1                        |John Doe                 |john.doe@example.com     |30                       |1                        |{"street":"123 Main St","|
|                         |                         |                         |                         |                         |city":"Anytown","state":"|
|                         |                         |                         |                         |                         |CA","zip":"12345"}       |
|2                        |Jane Smith               |jane.smith@example.com   |25                       |1                        |{"street":"456 Maple Ave"|
|                         |                         |                         |                         |                         |,"city":"Somewhere","stat|
|                         |                         |                         |                         |                         |e":"NY","zip":"67890"}   |
^CQuery terminated
```
</details>

#### Tumbling Window
- Fixed-duration time window
- No overlaps

#### Hopping Window
- Fixed-duration time window
- A 'hop' interval (e.g. 1min) => overlaps

#### Session Window
- No fixed duration
- Windows based on durations of activity
- Windows separated by gaps of inactivity

# ksql Server in Production
 Property                                                   | Scope | Default override | Effective Value                                                                                                                                                                                                                                                                                                               
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
 enable.fips                                                | KSQL  | SERVER           | false                                                                                                                                                                                                                                                                                                                         
 ksql.access.validator.enable                               | KSQL  | SERVER           | on                                                                                                                                                                                                                                                                                                                            
 ksql.assert.schema.default.timeout.ms                      | KSQL  |                  | 1000                                                                                                                                                                                                                                                                                                                          
 ksql.assert.topic.default.timeout.ms                       | KSQL  |                  | 1000                                                                                                                                                                                                                                                                                                                          
 ksql.authorization.cache.expiry.time.secs                  | KSQL  |                  | 30                                                                                                                                                                                                                                                                                                                            
 ksql.authorization.cache.max.entries                       | KSQL  |                  | 10000                                                                                                                                                                                                                                                                                                                         
 ksql.cast.strings.preserve.nulls                           | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.client.ip_port.configuration.enabled                  | KSQL  | SERVER           | true                                                                                                                                                                                                                                                                                                                          
 ksql.connect.basic.auth.credentials.file                   | KSQL  |                  |                                                                                                                                                                                                                                                                                                                               
 ksql.connect.basic.auth.credentials.reload                 | KSQL  |                  | false                                                                                                                                                                                                                                                                                                                         
 ksql.connect.basic.auth.credentials.source                 | KSQL  |                  | NONE                                                                                                                                                                                                                                                                                                                          
 ksql.connect.request.headers.plugin                        | KSQL  | SERVER           | io.confluent.ksql.ccloud.connect.headers.KsqlCloudConnectHeadersExtension                                                                                                                                                                                                                                                     
 ksql.connect.request.timeout.ms                            | KSQL  | SERVER           | 60000                                                                                                                                                                                                                                                                                                                         
 ksql.connect.url                                           | KSQL  | SERVER           | https://confluent.cloud:443/api/connect/v1/environments/env-r2px59/clusters/lkc-1nvqgz                                                                                                                                                                                                                                        
 ksql.connect.worker.config                                 | KSQL  |                  |                                                                                                                                                                                                                                                                                                                               
 ksql.create.or.replace.enabled                             | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.deployment.type                                       | KSQL  | SERVER           | confluent                                                                                                                                                                                                                                                                                                                     
 ksql.endpoint.migrate.query                                | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.error.classifier.regex                                | KSQL  |                  |                                                                                                                                                                                                                                                                                                                               
 ksql.extension.dir                                         | KSQL  |                  | ext                                                                                                                                                                                                                                                                                                                           
 ksql.fetch.remote.hosts.max.timeout.seconds                | KSQL  |                  | 10                                                                                                                                                                                                                                                                                                                            
 ksql.functions.collect_list.limit                          | KSQL  | SERVER           | [hidden]                                                                                                                                                                                                                                                                                                                      
 ksql.functions.collect_set.limit                           | KSQL  | SERVER           | [hidden]                                                                                                                                                                                                                                                                                                                      
 ksql.headers.columns.enabled                               | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.hidden.topics                                         | KSQL  |                  | _confluent.*,__confluent.*,_schemas,__consumer_offsets,__transaction_state,connect-configs,connect-offsets,connect-status,connect-statuses                                                                                                                                                                                    
 ksql.insert.into.values.enabled                            | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.internal.topic.min.insync.replicas                    | KSQL  | SERVER           | 2                                                                                                                                                                                                                                                                                                                             
 ksql.internal.topic.replicas                               | KSQL  | SERVER           | 3                                                                                                                                                                                                                                                                                                                             
 ksql.json_sr.converter.deserializer.enabled                | KSQL  | SERVER           | false                                                                                                                                                                                                                                                                                                                         
 ksql.lambdas.enabled                                       | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.metastore.backup.location                             | KSQL  | SERVER           | /mnt/data/data/ksql-command-backups                                                                                                                                                                                                                                                                                           
 ksql.metrics.extension                                     | KSQL  | SERVER           | io.confluent.cloud.ksql.engine.metrics.KsqlMetricsExtensionImpl                                                                                                                                                                                                                                                               
 ksql.metrics.tags.custom                                   | KSQL  | SERVER           | logical_cluster_id:lksqlc-d1735z                                                                                                                                                                                                                                                                                              
 ksql.nested.error.set.null                                 | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.new.query.planner.enabled                             | KSQL  |                  | false                                                                                                                                                                                                                                                                                                                         
 ksql.output.topic.name.prefix                              | KSQL  | SERVER           | pksqlc-383k8o                                                                                                                                                                                                                                                                                                                 
 ksql.persistence.default.format.key                        | KSQL  |                  | KAFKA                                                                                                                                                                                                                                                                                                                         
 ksql.persistence.default.format.value                      | KSQL  |                  | NULL                                                                                                                                                                                                                                                                                                                          
 ksql.persistence.wrap.single.values                        | KSQL  |                  | NULL                                                                                                                                                                                                                                                                                                                          
 ksql.persistent.prefix                                     | KSQL  |                  | query_                                                                                                                                                                                                                                                                                                                        
 ksql.properties.overrides.denylist                         | KSQL  | SERVER           | ksql.streams.num.stream.threads,ksql.suppress.buffer.size,ksql.suppress.enabled                                                                                                                                                                                                                                               
 ksql.pull.queries.enable                                   | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.cleanup.shutdown.timeout.ms                     | KSQL  |                  | 30000                                                                                                                                                                                                                                                                                                                         
 ksql.query.error.max.queue.size                            | KSQL  |                  | 10                                                                                                                                                                                                                                                                                                                            
 ksql.query.persistent.active.limit                         | KSQL  | SERVER           | 40                                                                                                                                                                                                                                                                                                                            
 ksql.query.persistent.max.bytes.buffering.total            | KSQL  | SERVER           | 838860800                                                                                                                                                                                                                                                                                                                     
 ksql.query.pull.enable.standby.reads                       | KSQL  | SERVER           | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.pull.forwarding.timeout.ms                      | KSQL  |                  | 20000                                                                                                                                                                                                                                                                                                                         
 ksql.query.pull.interpreter.enabled                        | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.pull.limit.clause.enabled                       | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.pull.max.allowed.offset.lag                     | KSQL  |                  | 9223372036854775807                                                                                                                                                                                                                                                                                                           
 ksql.query.pull.max.concurrent.requests                    | KSQL  | SERVER           | 2147483640                                                                                                                                                                                                                                                                                                                    
 ksql.query.pull.max.hourly.bandwidth.megabytes             | KSQL  | SERVER           | 190                                                                                                                                                                                                                                                                                                                           
 ksql.query.pull.max.qps                                    | KSQL  | SERVER           | 1000000                                                                                                                                                                                                                                                                                                                       
 ksql.query.pull.metrics.enabled                            | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.pull.range.scan.enabled                         | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.pull.router.thread.pool.size                    | KSQL  |                  | 50                                                                                                                                                                                                                                                                                                                            
 ksql.query.pull.stream.enabled                             | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.pull.table.scan.enabled                         | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.pull.thread.pool.size                           | KSQL  |                  | 50                                                                                                                                                                                                                                                                                                                            
 ksql.query.push.v2.alos.enabled                            | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.push.v2.catchup.consumer.msg.window             | KSQL  |                  | 50                                                                                                                                                                                                                                                                                                                            
 ksql.query.push.v2.continuation.tokens.enabled             | KSQL  |                  | false                                                                                                                                                                                                                                                                                                                         
 ksql.query.push.v2.enabled                                 | KSQL  |                  | false                                                                                                                                                                                                                                                                                                                         
 ksql.query.push.v2.interpreter.enabled                     | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.push.v2.latest.reset.age.ms                     | KSQL  |                  | 30000                                                                                                                                                                                                                                                                                                                         
 ksql.query.push.v2.max.catchup.consumers                   | KSQL  |                  | 5                                                                                                                                                                                                                                                                                                                             
 ksql.query.push.v2.max.hourly.bandwidth.megabytes          | KSQL  | SERVER           | 950                                                                                                                                                                                                                                                                                                                           
 ksql.query.push.v2.metrics.enabled                         | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.push.v2.new.latest.delay.ms                     | KSQL  |                  | 5000                                                                                                                                                                                                                                                                                                                          
 ksql.query.push.v2.registry.installed                      | KSQL  | SERVER           | true                                                                                                                                                                                                                                                                                                                          
 ksql.query.retry.backoff.initial.ms                        | KSQL  |                  | 15000                                                                                                                                                                                                                                                                                                                         
 ksql.query.retry.backoff.max.ms                            | KSQL  |                  | 900000                                                                                                                                                                                                                                                                                                                        
 ksql.query.status.running.threshold.seconds                | KSQL  |                  | 300                                                                                                                                                                                                                                                                                                                           
 ksql.query.transient.max.bytes.buffering.total             | KSQL  | SERVER           | 104857600                                                                                                                                                                                                                                                                                                                     
 ksql.queryanonymizer.cluster_namespace                     | KSQL  | SERVER           | pksqlc-383k8o.498986                                                                                                                                                                                                                                                                                                          
 ksql.queryanonymizer.logs_enabled                          | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.readonly.topics                                       | KSQL  |                  | _confluent.*,__confluent.*,_schemas,__consumer_offsets,__transaction_state,connect-configs,connect-offsets,connect-status,connect-statuses                                                                                                                                                                                    
 ksql.runtime.feature.shared.enabled                        | KSQL  |                  | false                                                                                                                                                                                                                                                                                                                         
 ksql.schema.registry.url                                   | KSQL  | SERVER           | https://psrc-10dzz.ap-southeast-2.aws.confluent.cloud                                                                                                                                                                                                                                                                         
 ksql.security.extension.class                              | KSQL  | SERVER           | io.confluent.cloud.ksql.security.KsqlCloudSecurityExtension                                                                                                                                                                                                                                                                   
 ksql.service.id                                            | KSQL  | SERVER           | pksqlc-383k8o                                                                                                                                                                                                                                                                                                                 
 ksql.shared.runtimes.count                                 | KSQL  |                  | 2                                                                                                                                                                                                                                                                                                                             
 ksql.sink.window.change.log.additional.retention           | KSQL  |                  | 1000000                                                                                                                                                                                                                                                                                                                       
 ksql.source.table.materialization.enabled                  | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.streams.application.server                            | KSQL  | SERVER           | https://ksql-0.ksql.pksqlc-383k8o.svc.cluster.local:9199                                                                                                                                                                                                                                                                      
 ksql.streams.auto.offset.reset                             | KSQL  | SESSION          | earliest                                                                                                                                                                                                                                                                                                                      
 ksql.streams.bootstrap.servers                             | KSQL  | SERVER           | SASL_SSL://kafka-0.kafka.pkc-ldvj1.svc.cluster.local:9074,kafka-1.kafka.pkc-ldvj1.svc.cluster.local:9074,kafka-2.kafka.pkc-ldvj1.svc.cluster.local:9074                                                                                                                                                                       
 ksql.streams.cache.max.bytes.buffering                     | KSQL  |                  | 10485760                                                                                                                                                                                                                                                                                                                      
 ksql.streams.commit.interval.ms                            | KSQL  | SERVER           | 3000                                                                                                                                                                                                                                                                                                                          
 ksql.streams.consumer.default.api.timeout.ms               | KSQL  | SERVER           | 300000                                                                                                                                                                                                                                                                                                                        
 ksql.streams.consumer.request.timeout.ms                   | KSQL  | SERVER           | 300000                                                                                                                                                                                                                                                                                                                        
 ksql.streams.default.deserialization.exception.handler     | KSQL  | SERVER           | io.confluent.ksql.errors.LogMetricAndContinueExceptionHandler                                                                                                                                                                                                                                                                 
 ksql.streams.default.production.exception.handler          | KSQL  | SERVER           | io.confluent.ksql.errors.ProductionExceptionHandlerUtil$LogAndContinueProductionExceptionHandler                                                                                                                                                                                                                              
 ksql.streams.delivery.timeout.ms                           | KSQL  | SERVER           | 1800000                                                                                                                                                                                                                                                                                                                       
 ksql.streams.metric.reporters                              | KSQL  | SERVER           | io.confluent.telemetry.reporter.TelemetryReporter                                                                                                                                                                                                                                                                             
 ksql.streams.num.standby.replicas                          | KSQL  |                  | 0                                                                                                                                                                                                                                                                                                                             
 ksql.streams.num.stream.threads                            | KSQL  |                  | 1                                                                                                                                                                                                                                                                                                                             
 ksql.streams.producer.acks                                 | KSQL  |                  | all                                                                                                                                                                                                                                                                                                                           
 ksql.streams.producer.compression.type                     | KSQL  | SERVER           | snappy                                                                                                                                                                                                                                                                                                                        
 ksql.streams.producer.max.block.ms                         | KSQL  | SERVER           | 300000                                                                                                                                                                                                                                                                                                                        
 ksql.streams.producer.request.timeout.ms                   | KSQL  | SERVER           | 300000                                                                                                                                                                                                                                                                                                                        
 ksql.streams.producer.retries                              | KSQL  |                  | 2147483647                                                                                                                                                                                                                                                                                                                    
 ksql.streams.repartition.purge.interval.ms                 | KSQL  | SERVER           | 300000                                                                                                                                                                                                                                                                                                                        
 ksql.streams.replication.factor                            | KSQL  | SERVER           | 3                                                                                                                                                                                                                                                                                                                             
 ksql.streams.request.timeout.ms                            | KSQL  | SERVER           | 20000                                                                                                                                                                                                                                                                                                                         
 ksql.streams.retry.backoff.ms                              | KSQL  | SERVER           | 500                                                                                                                                                                                                                                                                                                                           
 ksql.streams.rocksdb.config.setter                         | KSQL  | SERVER           | io.confluent.ksql.rocksdb.KsqlBoundedMemoryRocksDBConfigSetter                                                                                                                                                                                                                                                                
 ksql.streams.sasl.jaas.config                              | KSQL  | SERVER           | [hidden]                                                                                                                                                                                                                                                                                                                      
 ksql.streams.sasl.mechanism                                | KSQL  | SERVER           | PLAIN                                                                                                                                                                                                                                                                                                                         
 ksql.streams.security.protocol                             | KSQL  | SERVER           | SASL_SSL                                                                                                                                                                                                                                                                                                                      
 ksql.streams.security.providers                            | KSQL  | SERVER           | io.confluent.kafka.server.plugins.ssl.ConfluentTrustProviderCreator                                                                                                                                                                                                                                                           
 ksql.streams.shutdown.timeout.ms                           | KSQL  | SERVER           | 300000                                                                                                                                                                                                                                                                                                                        
 ksql.streams.ssl.cipher.suites                             | KSQL  | SERVER           | TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,TLS_DHE_RSA_WITH_AES_256_GCM_SHA384,TLS_DHE_RSA_WITH_AES_128_GCM_SHA256 
 ksql.streams.ssl.enabled.protocols                         | KSQL  |                  | TLSv1.2,TLSv1.3                                                                                                                                                                                                                                                                                                               
 ksql.streams.ssl.endpoint.identification.algorithm         | KSQL  | SERVER           |                                                                                                                                                                                                                                                                                                                               
 ksql.streams.ssl.key.password                              | KSQL  | SERVER           | [hidden]                                                                                                                                                                                                                                                                                                                      
 ksql.streams.ssl.keystore.location                         | KSQL  | SERVER           | /mnt/sslcerts/pkcs.p12                                                                                                                                                                                                                                                                                                        
 ksql.streams.ssl.keystore.password                         | KSQL  | SERVER           | [hidden]                                                                                                                                                                                                                                                                                                                      
 ksql.streams.ssl.keystore.type                             | KSQL  | SERVER           | PKCS12                                                                                                                                                                                                                                                                                                                        
 ksql.streams.ssl.trustmanager.algorithm                    | KSQL  | SERVER           | ConfluentTls                                                                                                                                                                                                                                                                                                                  
 ksql.streams.state.dir                                     | KSQL  | SERVER           | /mnt/data/data/ksql-state                                                                                                                                                                                                                                                                                                     
 ksql.streams.topology.optimization                         | KSQL  | SERVER           | all                                                                                                                                                                                                                                                                                                                           
 ksql.suppress.buffer.size.bytes                            | KSQL  |                  | -1                                                                                                                                                                                                                                                                                                                            
 ksql.suppress.enabled                                      | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.timestamp.throw.on.invalid                            | KSQL  |                  | false                                                                                                                                                                                                                                                                                                                         
 ksql.transient.prefix                                      | KSQL  |                  | transient_                                                                                                                                                                                                                                                                                                                    
 ksql.transient.query.cleanup.service.enable                | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.transient.query.cleanup.service.initial.delay.seconds | KSQL  |                  | 600                                                                                                                                                                                                                                                                                                                           
 ksql.transient.query.cleanup.service.period.seconds        | KSQL  |                  | 600                                                                                                                                                                                                                                                                                                                           
 ksql.udf.collect.metrics                                   | KSQL  |                  | false                                                                                                                                                                                                                                                                                                                         
 ksql.udf.enable.security.manager                           | KSQL  | SERVER           | false                                                                                                                                                                                                                                                                                                                         
 ksql.udfs.enabled                                          | KSQL  | SERVER           | false                                                                                                                                                                                                                                                                                                                         
 ksql.variable.substitution.enable                          | KSQL  |                  | true                                                                                                                                                                                                                                                                                                                          
 ksql.websocket.connection.max.timeout.ms                   | KSQL  |                  | 3600000                                                                                                                                                                                                                                                                                                                       
 metric.reporters                                           | KSQL  | SERVER           | io.confluent.telemetry.reporter.TelemetryReporter                                                                                                                                                                                                                                                                             
--------------------------------------------------------------------------------------------------------------------------------------------------------------------
ksql> 








