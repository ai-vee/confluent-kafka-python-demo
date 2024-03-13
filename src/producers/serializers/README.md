# Consume
## ❗️ Message outputs are not parsed correctly without passing deserializer
``` sh
confluent kafka topic consume --from-beginning topic-user-avro
```

> ��y consulting
> ��abc consulting
> 
> ��y consulting"y@consulting.come
> ��y consulting"y@consulting.come

## ✅ Fix

``` sh
confluent kafka topic consume --from-beginning topic-user-avro --value-format avro
```