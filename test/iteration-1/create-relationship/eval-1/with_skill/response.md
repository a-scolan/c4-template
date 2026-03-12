No — keep the flow one-way and do **not** draw a return relationship from `worker` back to `uploadService`.

```likec4
uploadService -[async]-> jobQueue 'Queue upload job'
jobQueue -[async]-> worker 'Deliver job'
worker -[writes]-> database 'Persist processing result'
```

Use `-[async]->` for producer → queue and queue → worker. Use `-[writes]->` for the database update rather than `-[calls]->`. If you have acknowledgements or retries, do not model them as a callback relationship from the worker to the producer.
