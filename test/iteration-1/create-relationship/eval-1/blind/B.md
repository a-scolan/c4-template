Model it as a one-way async flow:

```likec4
uploadService -[async]-> jobQueue 'Publishes upload job'
jobQueue -[async]-> worker 'Delivers job'
worker -[writes]-> database 'Stores upload result'
```

Do **not** add a return relationship from `worker` back to `uploadService` just to show an ACK or internal completion signal.

Use `-[async]->` for producer-to-queue and queue-to-consumer messaging, and use `-[writes]->` when the worker persists data. Only add a reverse relationship if there is a separate, real callback or API interaction you need to model.