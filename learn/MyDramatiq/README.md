# Dramatiq


[https://dramatiq.io/](https://dramatiq.io/)  
Async task queue that also works on windows.
## Start worker
Start worker with 2 processes and queue specified  
Command run from directory which contains base_case.py
```
dramatiq base_case:rabbitmq_broker -p 2
dramatiq base_case:rabbitmq_broker -p 1 --queues easy1
```

## Links
- [Celery to Dramatiq migration tips](https://blog.narrativ.com/converting-celery-to-dramatiq-a-py3-war-story-23df217b426)

