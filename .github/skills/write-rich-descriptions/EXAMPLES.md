# write-rich-descriptions Examples Reference

Comprehensive templates and patterns for system and deployment model descriptions.

## System Model Templates

### Service Template - Minimal (Recommended Baseline)

```likec4
apiService = Container_Service 'API Gateway' {
  #backend #api #critical
  technology 'Go / Gin Framework 1.20'
  
  description """
    Central API gateway handling authentication, rate limiting, and routing.
    
    **Responsibilities:**
    - JWT authentication for all requests
    - Rate limiting (1000 req/min per client)
    - Route to microservices
  """
}
```

**This is sufficient.** No metadata needed—just technology + responsibilities.

### Service Template - With Optional Details (If Needed)

```likec4
apiService = Container_Service 'API Gateway' {
  #backend #api #critical
  technology 'Go / Gin Framework 1.20'
  
  link https://docs.company.com/api-gateway 'API Docs'
  link https://github.com/company/api-gateway 'Source Code'
  
  description """
    Central API gateway handling authentication, rate limiting, and routing.
    
    **Responsibilities:**
    - JWT authentication for all requests
    - Rate limiting (1000 req/min per client)
    - Route to microservices
    
    **Dependencies:**
    - Redis (session cache)
    - PostgreSQL (API keys)
  """
  
  metadata {
    owner 'alice@company.com'
  }
}
```

### Service Template - Comprehensive (Optional; Only If Querying by Field)

```likec4
apiService = Container_Service 'API Gateway' {
  #backend #api #critical
  technology 'Go / Gin Framework 1.20'
  
  link https://docs.company.com/api-gateway 'API Docs'
  
  description """
    Central API gateway handling authentication, rate limiting, and routing.
    
    **Responsibilities:**
    - JWT authentication
    - Rate limiting (1000 req/min)
    - Route to microservices
    
    **Performance:**
    - Response time: <50ms (p99)
    - Throughput: 10,000 req/sec
  """
  
  metadata {
    owner 'alice@company.com'
    team 'Platform'  // Only if you filter/query by team
    regions ['us-east-1', 'us-west-2']  // Only if multi-region matters
    dependencies ['redis', 'postgresql']  // Only if auto-doc needs this
  }
}
```

**Add metadata only if you actually query/filter by those fields.**

### Service Template (Message Queue Consumer) - Minimal

```likec4
workerService = Container_Service 'Background Worker' {
  #backend #async
  technology 'Python 3.11 / Celery'
  
  description """
    Asynchronous task processor consuming jobs from RabbitMQ.
    
    **Responsibilities:**
    - Consume file processing jobs
    - Virus scan using ClamAV
    - Encrypt files with AES-256
    - Store encrypted files
  """
}
```

**Metadata completely optional.** Only add if you track ownership or have specific automation needs.
```

### Database Container - Minimal

```likec4
database = Container_Database 'Primary Database' {
  #data #postgresql #critical
  technology 'PostgreSQL 14'
  
  description """
    Primary transactional database.
    
    **Stores:**
    - User accounts and profiles
    - File metadata
    - API keys and tokens
  """
}
```

**No metadata needed.** SLA/RTO/RPO belong on the **System level** (if important), not individual containers.
```

### Component Template - Minimal

```likec4
validateModule = Component 'File Validator' {
  #validation #security
  technology 'TypeScript'
  
  description """
    Validates uploaded files against policies.
    
    **Validations:**
    - File size: max 5GB
    - MIME type: allowlist (pdf, docx, xlsx, png, jpg)
    - ClamAV: virus check
  """
}
```

**Components rarely need metadata.** Just technology + quick description of what it validates or does.
```

### When to Add Metadata (Rare)

Only if you **filter/query** by the field:

```likec4
authModule = Component 'JWT Authenticator' {
  #security #auth #critical
  technology 'TypeScript / jsonwebtoken'
  
  description """
    JWT token generation, validation, and refresh.
    
    **Capabilities:**
    - Generate access tokens (15min expiry)
    - Generate refresh tokens (7 days)
    - Validate signatures
  """
  
  metadata {
    owner 'alice@company.com'  // Only if you auto-assign tickets/ownership
  }
}
```

**Drop the extra metadata** (complexity, test_coverage, security_audit). These belong in your testing/CI pipeline, not the model.
```

## Deployment Model Templates

### Environment Template

```likec4
Production = Environment 'Production' {
  description """
    Production environment serving live customer traffic.
    
    | Property | Value |
    |:---------|:------|
    | Cloud Provider | AWS |
    | Region | us-east-1, us-west-2 |
    | Availability | 99.99% SLA |
    | Monitoring | CloudWatch + Prometheus |
    | Backup | Daily snapshots, 30-day retention |
  """
  
  metadata {
    cloud_provider 'AWS'
    regions ['us-east-1', 'us-west-2']
    sla '99.99%'
    monitoring_services ['CloudWatch', 'Prometheus', 'Grafana']
    backup_retention '30 days'
  }
}
```

### Zone Template (Network Tier)

```likec4
AppTier = Zone "Application Tier (VLAN 101: 10.1.0.0/24)" {
  description """
    Production microservices deployment zone.
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 101 |
    | Network | 10.1.0.0/24 |
    | Gateway | 10.1.0.1 |
    | DNS | 10.0.0.10, 10.0.0.11 |
    | NTP | 10.0.0.20 |
    | Monitoring Port | 9090 |
    | Capacity | 10 Gbps link to core |
    
    **Firewall Rules:**
    - Inbound: DMZ (443, 8080), Monitoring (9090)
    - Outbound: Data Tier (5432, 6379), Processing Tier (5672)
    - Deny: All other traffic
    
    **Purpose:**
    - Host customer-facing microservices
    - Handle API requests from DMZ
    - Connect to backend data services
  """
  
  metadata {
    vlan '101'
    network '10.1.0.0/24'
    gateway '10.1.0.1'
    dns_servers ['10.0.0.10', '10.0.0.11']
    ntp_server '10.0.0.20'
    monitoring_port '9090'
    capacity '10 Gbps'
    purpose 'Production microservices'
  }
}
```

### Zone Template (DMZ)

```likec4
DmzTier = Zone "DMZ (VLAN 50: 192.168.50.0/24)" {
  description """
    Internet-facing demilitarized zone with reverse proxies and load balancers.
    
    | Property | Value |
    |:---------|:------|
    | VLAN | 50 |
    | Network | 192.168.50.0/24 |
    | Gateway | 192.168.50.1 |
    | Public IPs | 203.0.113.10 - 203.0.113.20 |
    | WAF | Cloudflare Enterprise |
    | DDoS Protection | L3/L4/L7 |
    
    **Security:**
    - Strict ingress filtering (ports 80, 443 only)
    - TLS 1.3 required
    - No direct access to internal tiers
    - All traffic proxied through load balancers
  """
  
  metadata {
    vlan '50'
    network '192.168.50.0/24'
    gateway '192.168.50.1'
    public_ip_range '203.0.113.10-203.0.113.20'
    waf 'Cloudflare Enterprise'
    ddos_protection 'L3/L4/L7'
  }
}
```

### VM Template (Application Server) - Minimal

```likec4
ProdApiVm = Node_Vm "prod-api-vm" {
  #Deployment
  technology "Go + Docker"
  
  description """
    API Gateway service handling customer requests.
    
    | Property | Value |
    |:---------|:------|
    | eth0 | 10.1.0.10/24 |
    | OS | Ubuntu 22.04 LTS |
    | CPU | 4 vCPU |
    | RAM | 8 GB |
    | Disk | 200 GB SSD |
    | Service Port | 8080 |
    | RTO | 5 min |
  """
  
  metadata {
    eth0 '10.1.0.10/24'
    os 'Ubuntu 22.04 LTS'
    cpu '4 vCPU'
    ram '8 GB'
    disk '200 GB SSD'
    rto '5 min'
  }
  
  apiApp = Node_App "API Gateway" {
    instanceOf vault.apiService
  }
}
```

**This is sufficient.** Skip extra metadata (eth1, kernel, swap, health_check details, etc.).
```

### VM Template (Database Server) - Minimal

```likec4
ProdDbVm = Node_Vm "prod-db-vm" {
  #Deployment #Critical
  technology "PostgreSQL 14"
  
  description """
    Primary database server with streaming replication.
    
    | Property | Value |
    |:---------|:------|
    | eth0 | 10.2.0.10/24 |
    | eth1 | 10.2.1.10/24 (replication) |
    | OS | Ubuntu 22.04 LTS |
    | CPU | 8 vCPU |
    | RAM | 32 GB |
    | Disk | 500 GB SSD RAID 10 |
    | Application | PostgreSQL 14 |
    | Service Port | 5432 |
    | RTO | 2 min |
    | RPO | 30 sec |
  """
  
  metadata {
    eth0 '10.2.0.10/24'
    eth1 '10.2.1.10/24'
    os 'Ubuntu 22.04'
    cpu '8 vCPU'
    ram '32 GB'
    disk '500 GB SSD RAID 10'
    app 'PostgreSQL 14'
    rto '2 min'
    rpo '30 sec'
  }
  
  dbApp = Node_App "Primary Database" {
    instanceOf vault.database
  }
}
```

**Keep metadata sparse:** only fields ops teams actually query/filter by.
```

### VM Template (Worker Server) - Minimal

```likec4
ProdWorkerVm = Node_Vm "prod-worker-vm" {
  technology "Python + Docker"
  
  description """
    Background worker processing async jobs from RabbitMQ.
    
    | Property | Value |
    |:---------|:------|
    | eth0 | 10.3.0.20/24 |
    | OS | Ubuntu 22.04 LTS |
    | CPU | 4 vCPU |
    | RAM | 16 GB |
    | Disk | 100 GB SSD |
    | RTO | 10 min |
  """
  
  metadata {
    eth0 '10.3.0.20/24'
    os 'Ubuntu 22.04'
    cpu '4 vCPU'
    ram '16 GB'
    disk '100 GB SSD'
    rto '10 min'
  }
  
  workerApp = Node_App "Background Worker" {
    instanceOf vault.workerService
  }
}
```
```

### VM Template (Load Balancer) - Minimal

```likec4
ProdLbVm = Node_Vm "prod-lb-vm" {
  technology "HAProxy 2.6"
  
  description """
    Load balancer distributing traffic to API servers.
    
    | Property | Value |
    |:---------|:------|
    | eth0 | 192.168.50.10/24 (DMZ) |
    | eth1 | 10.1.0.5/24 (app tier) |
    | OS | Ubuntu 22.04 LTS |
    | CPU | 2 vCPU |
    | RAM | 4 GB |
    | Disk | 50 GB SSD |
    | Application | HAProxy 2.6 |
    | RTO | 10 sec (VRRP failover) |
  """
  
  metadata {
    eth0 '192.168.50.10/24'
    eth1 '10.1.0.5/24'
    os 'Ubuntu 22.04'
    cpu '2 vCPU'
    ram '4 GB'
    disk '50 GB SSD'
    app 'HAProxy 2.6'
    rto '10 sec'
  }
  
  lbApp = Node_App "Load Balancer" {}
}
```
```

### VM Template (Monitoring Server) - Skip Metadata

```likec4
MonitoringVm = Node_Vm "monitoring-vm" {
  technology "Prometheus + Grafana"
  
  description """
    Central monitoring and alerting infrastructure.
    
    | Property | Value |
    |:---------|:------|
    | eth0 | 10.4.0.30/24 |
    | OS | Ubuntu 22.04 LTS |
    | CPU | 4 vCPU |
    | RAM | 16 GB |
    | Disk | 1 TB SSD (90-day retention) |
    | Services | Prometheus, Grafana |
  """
  
  prometheusApp = Node_App "Prometheus" {}
  grafanaApp = Node_App "Grafana" {}
}
```

**No metadata needed** — the table is all ops teams need.
```

## Zone vs. VM Comparison

### Zone Description (Defines Network Segment)

```likec4
AppTier = Zone "Application Tier (VLAN 101: 10.1.0.0/24)" {
  description """
    | VLAN | Network | Gateway | DNS | Monitoring Port |
    |------|---------|---------|-----|---|
    | 101 | 10.1.0.0/24 | 10.1.0.1 | 10.0.0.10 | 9090 |
  """
  
  metadata {
    vlan '101'
    network '10.1.0.0/24'
    gateway '10.1.0.1'  // ← Zone defines gateway
    dns '10.0.0.10'
    monitoring_port '9090'
  }
}
```

**Gateway belongs in zone** — it defines the default route for all VMs in that subnet.

### VM Description (Inherits Zone's Gateway)

```likec4
ProdApiVm = Node_Vm "prod-api-vm" {
  description """
    | eth0 | 10.1.0.12/24 |  ← ONLY the NIC; gateway implicit to zone
    | OS | Ubuntu 22.04 |
    | CPU | 2 vCPU |
  """
  
  metadata {
    eth0 '10.1.0.12/24'
    // NO gateway here — inherited from zone
    os 'Ubuntu 22.04'
    cpu '2 vCPU'
  }
}
```

**VMs omit gateway** — it's implicit from the zone they're in. Only include gateway in VM if multi-homed or policy routing requires explicit configuration.

## Multi-Homed Network Example

### VM with Multiple Network Interfaces

```likec4
EdgeGatewayVm = Node_Vm "edge-gateway-vm" {
  technology "pfSense Firewall"
  
  description """
    Edge firewall/router connecting DMZ to internal tiers.
    
    | Property | Value |
    |:---------|:------|
    | eth0 | 192.168.50.1/24 (DMZ interface) |
    | eth1 | 10.1.0.1/24 (App tier interface) |
    | eth2 | 10.2.0.1/24 (Data tier interface) |
    | OS | pfSense 2.7 (FreeBSD) |
    | CPU | 2 vCPU |
    | RAM | 4 GB |
    | Disk | 50 GB SSD |
    | Routing | Static routes + OSPF |
    | Firewall | Stateful inspection, IDS/IPS |
    | Default Gateway | 192.168.50.254 (ISP router) |
    | RTO | 5 min (standby firewall failover) |
  """
  
  metadata {
    eth0 '192.168.50.1/24'
    eth1 '10.1.0.1/24'
    eth2 '10.2.0.1/24'
    os 'pfSense 2.7'
    cpu '2 vCPU'
    ram '4 GB'
    disk '50 GB SSD'
    routing_protocol 'static-ospf'
    firewall_features 'stateful-inspection-ids-ips'
    default_gateway '192.168.50.254'  // ← Explicit because multi-homed
    rto '5 min'
  }
}
```

**Multi-homed VMs include default gateway** explicitly because they connect to multiple networks.

## Dynamic View Descriptions

### Dynamic View Template

```likec4
views 'Use Cases' {
  dynamic view uploadFlow {
    title 'Upload Workflow'
    description """
      Complete file upload flow from user action to encrypted storage.
      
      **Flow Steps:**
      1. User uploads file via web UI
      2. Browser sends multipart POST to API Gateway
      3. API Gateway authenticates JWT token
      4. Upload Service validates file (fail-fast)
      5. Valid file queued to RabbitMQ (FileValidated event)
      6. Worker consumes job asynchronously
      7. Worker scans file with ClamAV (fail on malware)
      8. Worker encrypts file with AES-256
      9. Worker stores encrypted file in MinIO
      10. Worker saves metadata to MongoDB
      11. Worker publishes FileStoredEvent
      
      **Failure Scenarios:**
      - Auth failure → 401 Unauthorized (no processing)
      - Validation failure → 400 Bad Request (no queue)
      - Virus detected → Job failed, user notified via email
      - Storage failure → Retry 3x with exponential backoff
      - Max retries exceeded → Dead-letter queue, alert on-call
      
      **Performance:**
      - Synchronous validation: <1s (fail-fast)
      - Async processing time: <30s average (5GB files)
      - Full end-to-end: <2min for 5GB file
      
      **SLA:**
      - Upload API availability: 99.9%
      - Processing success rate: 99.99%
      - Max processing time: 5min (p99)
    """
    
    customer -> browser 'Upload file'
    browser -> apiGateway 'POST /api/upload (multipart)'
    apiGateway -> authModule 'Validate JWT'
    apiGateway -> uploadService 'Forward request'
    uploadService -> uploadService 'Validate file (size, type, format)'
    uploadService -> queue 'Publish FileValidated'
    workerService -> queue 'Consume job'
    workerService -> clamAV 'Scan for viruses'
    clamAV -> workerService 'Clean result'
    workerService -> encryptionModule 'Encrypt AES-256'
    workerService -> minioStorage 'Store encrypted file'
    minioStorage -> workerService 'Stored confirmation'
    workerService -> database 'Save metadata (status: READY)'
    workerService -> queue 'Publish FileStoredEvent'
  }
}
```

## Minimal VM Examples

### Lightweight Application Server

```likec4
DevApiVm = Node_Vm "dev-api-vm" {
  description """
    | eth0 | 10.100.0.10/24 |
    | OS | Ubuntu 22.04 |
    | CPU | 1 vCPU |
    | RAM | 2 GB |
  """
  
  metadata {
    eth0 '10.100.0.10/24'
    os 'Ubuntu 22.04'
    cpu '1 vCPU'
    ram '2 GB'
  }
}
```

**Only include properties that matter** — minimal VMs don't need extensive specs.

### Database Server (Detailed)

```likec4
ProdPrimaryDb = Node_Vm "prod-primary-db" {
  description """
    | eth0 | 10.2.0.10/24 |
    | eth1 | 10.2.1.10/24 (replication) |
    | OS | Ubuntu 22.04 |
    | CPU | 16 vCPU |
    | RAM | 64 GB |
    | Disk | 2 TB SSD RAID 10 |
    | Application | PostgreSQL 14 |
    | Replication | Streaming async |
    | RTO | 2 min |
    | RPO | 30 sec |
  """
  
  metadata {
    eth0 '10.2.0.10/24'
    eth1 '10.2.1.10/24'
    os 'Ubuntu 22.04'
    cpu '16 vCPU'
    ram '64 GB'
    disk '2 TB SSD RAID 10'
    app 'PostgreSQL 14'
    replication 'streaming-async'
    rto '2 min'
    rpo '30 sec'
  }
}
```

**Critical infrastructure gets detailed specs** — DBs, monitoring, load balancers warrant comprehensive documentation.

## Advanced Metadata Patterns

### Complex SLO Configuration (YAML)

```likec4
apiService = Container_Service 'API Gateway' {
  metadata {
    team 'Platform'
    slo_config '''
      availability:
        target: 99.9%
        measurement_window: 30d
      latency:
        target_p50: 50ms
        target_p95: 200ms
        target_p99: 500ms
      error_rate:
        target: 0.1%
        exclude_client_errors: true
      throughput:
        expected: 10000 req/s
        peak: 50000 req/s
    '''
  }
}
```

### Deployment Configuration (JSON)

```likec4
workerService = Container_Service 'Background Worker' {
  metadata {
    deployment_config '''
      {
        "replicas": 3,
        "resources": {
          "cpu": "2",
          "memory": "4Gi",
          "storage": "20Gi"
        },
        "env": "production",
        "scaling": {
          "min_replicas": 2,
          "max_replicas": 10,
          "cpu_threshold": 75
        },
        "health_check": {
          "path": "/health",
          "interval": "30s",
          "timeout": "5s",
          "retries": 3
        }
      }
    '''
  }
}
```

### Grouped Contact Channels

```likec4
apiService = Container_Service 'API Gateway' {
  metadata {
    team 'Platform'
    owner 'alice@company.com'
    contact_channels ['platform@company.com', '#platform-team', '+1-555-0100']
    escalation_contacts ['alice@company.com', 'bob@company.com', 'carol@company.com']
    on_call_rotation 'pagerduty-platform-schedule'
  }
}
```

### Compliance and Audit Metadata

```likec4
database = Container_Database 'Customer Data Store' {
  metadata {
    compliance_tags ['PCI-DSS', 'SOC2', 'GDPR', 'HIPAA']
    data_classification 'PII'
    encryption_at_rest true
    encryption_in_transit true
    audit_logging true
    data_retention_days 2555  // 7 years
    last_security_audit '2024-01-15'
    penetration_test_passed '2024-02-01'
  }
}
```

## File Organization Patterns

### Single-File Project

```
project/
  model.c4                        # Elements + descriptions together
```

### Multi-File Project (Recommended)

```
project/
  system-model.c4                 # Elements with metadata blocks
  system-views.c4                 # Views referencing system elements
  deployment.c4                   # Deployment nodes with markdown tables + metadata
  deployment-views.c4             # Deployment views
```

**Benefits:**
- Separation of system vs. deployment descriptions
- Easier to maintain metadata vs. tables
- Clear file-to-context mapping
