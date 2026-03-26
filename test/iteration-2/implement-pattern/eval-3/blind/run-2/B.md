# Eval-3 — Implement DMZ Security Zone Pattern (Baseline, Run 2)

## Prompt

> Implement a DMZ security zone pattern. Add a Web Application Firewall (WAF) and a reverse proxy in a demilitarized zone in front of the application tier. Use appropriate element kinds and tags from the shared specification and model the traffic flow from the internet through the security boundary.

---

## Response

The DMZ pattern isolates external-facing components. I'll add WAF and load balancer to screen traffic before it reaches the application tier.

### Model additions

```likec4
model {
  externalUser = Actor_Person 'External User'

  system AppSystem 'App System' {
    loadBalancer = Container_Loadbalancer 'Load Balancer' {
      technology 'HAProxy'
      description 'Distributes incoming traffic'
    }

    wafLayer = Container_Waf 'WAF' {
      technology 'AWS WAF'
      description 'Blocks malicious requests'
    }

    webApp = Container_Webapp 'Web Application' {
      technology 'Django'
    }

    dbServer = Container_Database 'DB Server' {
      technology 'MySQL'
    }

    externalUser -> loadBalancer 'HTTPS' { technology 'HTTPS' }
    loadBalancer -> wafLayer 'Forwards traffic' { technology 'HTTP' }
    wafLayer -> webApp 'Filtered requests' { technology 'HTTP' }
    webApp -> dbServer 'Queries' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view security_view of AppSystem {
    title 'DMZ / Security Tier'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- `Container_Waf` used correctly this run
- `Container_Loadbalancer` used for the entry point
- But `#Dmz` zone tag and `Zone` deployment node not used for grouping
- Missing `#Security` and `#Ingress` tag annotations
