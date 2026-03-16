No. Do not add a return relationship from worker back to uploadService unless the worker really sends a callback or makes a real call back to it. Model the actual async flow instead:
uploadService -[async]-> jobQueue 'Publishes upload job'
worker -[async]-> jobQueue 'Consumes upload job'
worker -[writes]-> database 'Stores upload result'
