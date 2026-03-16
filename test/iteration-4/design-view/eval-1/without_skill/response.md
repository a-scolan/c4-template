Aligned with the shared deployment conventions, use `Node_Environment` for production, generic `Zone` nodes tagged `#Dmz`, `#AppTier`, and `#DataTier`, and deploy service instances with `Node_Vm` + `Node_App` + `instanceOf`.

Example skeleton:

deployment {
  Node_Environment Prod Production {
    #Production

    Zone Dmz DMZ {
      #Dmz #Deployment #Networking
      edgeFw = Infra_Fw Edge Firewall
      webVm = Node_Vm Web VM {
        webApp = Node_App Web Application {
          instanceOf uploadPlatform.web
        }
      }
    }

    Zone AppTier Application Tier {
      #AppTier #Deployment #Service
      apiVm = Node_Vm API VM {
        apiApp = Node_App Upload API {
          instanceOf uploadPlatform.api
        }
      }
    }

    Zone DataTier Data Tier {
      #DataTier #Deployment #Persistence
      dbVm = Node_Vm Database VM {
        dbApp = Node_App Metadata DB {
          instanceOf uploadPlatform.db
        }
      }
    }

    webVm -[https]-> apiVm Ingress traffic
    apiVm -[sql]-> dbVm Reads and writes metadata
  }
}

deployment view prod_infra {
  title Production Infrastructure
  include * where tag is #Production
  autoLayout TopBottom
}

That matches the shared specs: PascalCase public names, environment-level `#Production`, tier tags for DMZ/App/Data, and infrastructure links expressed with deployment relationships.
