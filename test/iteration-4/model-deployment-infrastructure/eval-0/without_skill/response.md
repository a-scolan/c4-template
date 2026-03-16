Use the deployment hierarchy Environment -> Zone -> Node_Vm -> Node_App. Your logical containers would normally be something like Container_ReverseProxy or Container_Api for the gateway, Container_Api for the upload service, Container_ProcessingServer for the worker, and Container_Database for MongoDB.

Example structure:
deployment {
  Node_Environment Prod Production {
    #Production
    Zone Dmz DMZ { #Dmz
      Node_Vm gatewayVm API Gateway VM {
        Node_App gatewayApp API Gateway { instanceOf platform.gateway }
      }
    }
    Zone AppTier Application Tier { #AppTier
      Node_Vm uploadVm Upload VM {
        Node_App uploadApp Upload Service { instanceOf platform.uploadService }
      }
    }
    Zone ProcTier Processing Tier { #ProcTier
      Node_Vm workerVm Worker VM {
        Node_App workerApp Processing Worker { instanceOf platform.processingWorker }
      }
    }
    Zone DataTier Data Tier { #DataTier
      Node_Vm mongoVm MongoDB VM {
        Node_App mongoApp MongoDB { instanceOf platform.mongoDb }
      }
    }
  }
}

Link each deployed app to the logical model with instanceOf. The shared cheat sheet says normal application traffic should usually stay in the system model and be inherited in deployment through instanceOf, so you do not usually copy those relationships manually; add deployment relationships only for infrastructure-specific connections.
