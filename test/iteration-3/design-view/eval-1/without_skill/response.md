Use the same split: deployment model in `projects/template/system-model.c4`, deployment view in `projects/template/system-views.c4` under `views 'Deployment'`. Reuse the shared node kinds from `projects/shared/spec-deployment.c4` (`Node_Environment`, `Zone`, `Infra_Fw`, `Node_Vm`, `Node_App`) and the semantic tags `#Production`, `#Dmz`, `#AppTier`, `#DataTier`.

Deployment skeleton:
deployment {
  Node_Environment prod 'Production' {
    #Production

    Zone dmz 'DMZ' {
      #Dmz
      edgeFw = Infra_Fw 'Edge Firewall'
      webVm = Node_Vm 'Web VM' {
        #Service #Ingress
        webApp = Node_App 'Web Application Instance' {
          instanceOf mySystem.webapp
        }
      }
    }

    Zone appTier 'Application Tier' {
      #AppTier
      apiVm = Node_Vm 'API VM' {
        #Service
        apiApp = Node_App 'API Instance' {
          instanceOf mySystem.api
        }
      }
    }

    Zone dataTier 'Data Tier' {
      #DataTier
      dbVm = Node_Vm 'Database VM' {
        #Persistence #Data
        dbApp = Node_App 'Database Instance' {
          instanceOf mySystem.database
        }
      }
    }
  }
}

View skeleton:
views 'Deployment' {
  deployment view prod_infrastructure {
    title 'Production Infrastructure'
    include * where tag is #Production
    include * where tag is #Dmz
    include * where tag is #AppTier
    include * where tag is #DataTier
    autoLayout TopBottom
  }
}

That matches the workspace conventions: logical containers stay in C2, deployment nodes point back to them with `instanceOf`, and tier colors come from the shared deployment tags instead of ad-hoc styling.
