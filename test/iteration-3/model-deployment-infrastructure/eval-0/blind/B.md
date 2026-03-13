Follow the deployment hierarchy that the shared spec already defines: `Node_Environment` for the environment, generic `Zone` for security/network segments, `Node_Vm` for each VM, and `Node_App` for each deployed software instance. For your case, a good production shape is:

deployment {
  Node_Environment Prod 'Production' {
    #Production
    Zone Dmz 'DMZ' { #Dmz
      Node_Vm gatewayVm 'API Gateway VM' {
        Node_App gatewayApp { instanceOf docPlatform.apiGateway }
      }
    }
    Zone AppTier 'Application Tier' { #AppTier
      Node_Vm uploadVm 'Upload Service VM' {
        Node_App uploadApp { instanceOf docPlatform.uploadService }
      }
    }
    Zone ProcTier 'Processing Tier' { #ProcTier
      Node_Vm workerVm 'Processing Worker VM' {
        Node_App workerApp { instanceOf docPlatform.processingWorker }
      }
    }
    Zone DataTier 'Data Tier' { #DataTier
      Node_Vm mongoVm 'MongoDB VM' {
        Node_App mongoApp { instanceOf docPlatform.mongoDb }
      }
    }
  }
}

The `instanceOf` target should be the logical container from the system model, for example gateway/upload as `Container_Api` or similar service containers, worker as `Container_ProcessingServer` or `Container_Webapp`, and MongoDB as `Container_Database`. You normally do not copy ordinary app-to-app relationships manually into deployment. Model those once in the logical model and let deployment inherit them through `instanceOf`. Add explicit deployment relationships only for deployment-specific links such as ingress hops, monitoring, backups, firewall-only flows, or other infrastructure connections.
