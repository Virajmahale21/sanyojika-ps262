# AICTE Sanyojika - Asynchronous Messaging & DLQ Topology

**Specification Code:** AICTE-MSG-DLQ-2026-V1  
**Broker Target:** Apache Kafka / RabbitMQ Streams  
**SLA Guarantee:** At-Least-Once Delivery with Idempotent Deduplication

---

## 1. Message Broker Architecture

```mermaid
flowchart LR
    GW[REST Gateway Ingestion] -->|Publish Event| Topic[grievance.intake.events]
    Topic --> Consumer[AI Overlap Detection Worker]
    Consumer -->|Process OK| DB[(PostgreSQL)]
    Consumer -->|Retry 3x on Failure| RetryQueue[grievance.intake.retry]
    RetryQueue -->|Exceeded Retries| DLQ[grievance.intake.dlq]
    DLQ --> Alert[SRE On-Call Pager & Manual Inspection]
```

---

## 2. Exponential Backoff & Dead-Letter Queue (DLQ)
- **Retry Attempts:** 3 iterations
- **Backoff Formula:** $T_{retry} = T_{base} 	imes 2^{attempt} + 	ext{jitter}$ (where $T_{base} = 5	ext{s}$)
- **DLQ Retention:** 14 days in durable storage for manual replay
- **Monitoring Trigger:** Alert triggered if DLQ message count exceeds 5 in a rolling 1-hour window
