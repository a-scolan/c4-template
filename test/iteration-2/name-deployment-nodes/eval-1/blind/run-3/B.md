Yes, this is the right naming skill. It defines exactly how to name environment/zone/VM nodes consistently.

You asked for full hierarchy + Markdown infra specs + `instanceOf`; here is a complete sample with those requirements:

```likec4
deployment {
  Prod = Node_Environment "Production" {
    Dmz = Zone "DMZ (VLAN 100: 10.0.0.0/24)" {
      ProdApigwVm = Node_Vm "prod-apigw-vm" {
        technology "API Gateway"
        description """
          Gateway and TLS termination

          | Property | Value |
          |:---------|:------|
          | eth0 | 10.0.0.10/24 |
          | CPU | 4 vCPU |
          | RAM | 8 GB |
          | Port | 443 |
        """
        apigwApp = Node_App "API Gateway" {
          instanceOf corePlatform.apiGateway
        }
      }
    }

    AppTier = Zone "Application Tier (VLAN 101: 10.1.0.0/24)" {
      ProdUploadVm = Node_Vm "prod-upload-vm" {
        technology "Node.js"
        description """
          Upload service

          | Property | Value |
          |:---------|:------|
          | eth0 | 10.1.0.12/24 |
          | CPU | 2 vCPU |
          | RAM | 4 GB |
          | Port | 3001 |
        """
        uploadApp = Node_App "Upload Service" {
          instanceOf corePlatform.uploadService
        }
      }
    }

    ProcTier = Zone "Processing Tier (VLAN 102: 10.2.0.0/24)" {
      ProdWorkerVm = Node_Vm "prod-worker-vm" {
        technology "Python"
        description """
          Worker processing jobs

          | Property | Value |
          |:---------|:------|
          | eth0 | 10.2.0.15/24 |
          | CPU | 4 vCPU |
          | RAM | 8 GB |
          | Port | 8080 |
        """
        workerApp = Node_App "Worker" {
          instanceOf corePlatform.worker
        }
      }
    }

    DataTier = Zone "Data Tier (VLAN 103: 10.3.0.0/24)" {
      ProdDatabaseVm = Node_Vm "prod-database-vm" {
        technology "MongoDB"
        description """
          MongoDB primary

          | Property | Value |
          |:---------|:------|
          | eth0 | 10.3.0.16/24 |
          | CPU | 4 vCPU |
          | RAM | 16 GB |
          | Port | 27017 |
        """
        mongoApp = Node_App "MongoDB" {
          instanceOf corePlatform.documentDb
        }
      }
    }
  }
}
```