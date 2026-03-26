Yes, this is the correct skill for naming. For your full requirement (hierarchy + rich descriptions + `instanceOf`), use this naming guidance and apply it in a full deployment model.

```likec4
deployment {
  Prod = Node_Environment "Production" {

    Dmz = Zone "DMZ (VLAN 100: 10.0.0.0/24)" {
      ProdApigwVm = Node_Vm "prod-apigw-vm" {
        technology "Kong"
        description """
          Edge gateway

          | Property | Value |
          |:---------|:------|
          | eth0 | 10.0.0.10/24 |
          | CPU | 4 vCPU |
          | RAM | 8 GB |
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
          Upload endpoint

          | Property | Value |
          |:---------|:------|
          | eth0 | 10.1.0.12/24 |
          | CPU | 2 vCPU |
          | RAM | 4 GB |
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
          Async processing

          | Property | Value |
          |:---------|:------|
          | eth0 | 10.2.0.15/24 |
          | CPU | 4 vCPU |
          | RAM | 8 GB |
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
          Database node

          | Property | Value |
          |:---------|:------|
          | eth0 | 10.3.0.16/24 |
          | CPU | 4 vCPU |
          | RAM | 16 GB |
        """
        mongoApp = Node_App "MongoDB" {
          instanceOf corePlatform.documentDb
        }
      }
    }
  }
}
```