# 🎯 Enabling Smart Batching

to increase throughput, higher compressiom ratio while maintaining very low latency. This can be achieved via the below configurations.

## linger.ms
Wait for additional messages to batch within this time period before sending the batch.

By default, this is set 0 => 1 message/ batch

{% hint style="warning" %} Unlike Java's a ProducerConfig class, Python uses a dict object for configuration. Ensure you provide the right key-value pairs correctly -- refer to ProducerConfig Class Documentation. {% endhint %}