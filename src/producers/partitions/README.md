# Kafka Builtin Paritioners
- Round Robin: < kafka2.3
- Sticky Partitioner: >= kafka 2.4

## Round Robin Paritioner
Pros:
- Even distribution
Cons:
- More batches due to 1 message/ batch and 1 batch/ partition
- More requests => higher latency

## Sticky Paritioner
*We stick to a partition until the batch is full or linger.ms has elapsed*
Pros:
- Effective use of resources because of larger batch => batch.size is likely to be reached
- Reduced latency
- Overtime, records are still spread evenly across paritions ?
