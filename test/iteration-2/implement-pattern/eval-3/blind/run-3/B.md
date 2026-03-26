# Eval-3 — Implement DMZ Security Zone Pattern (Baseline, Run 3)

## Prompt

> Implement a DMZ security zone pattern. Add a Web Application Firewall (WAF) and a reverse proxy in a demilitarized zone in front of the application tier. Use appropriate element kinds and tags from the shared specification and model the traffic flow from the internet through the security boundary.

---

## Response

Adding a security boundary with WAF + reverse proxy in the DMZ tier. This shields the application containers from direct internet exposure.

### Model additions

```likec4
model {
  user = Actor_Person 'User'

  system Portal 'Customer Portal' {
    proxy = Container_ReverseProxy 'Reverse Proxy' {
      technology 'Caddy'
      description 'TLS termination and routing'
    }

    firewall = Container 'WAF' {
      technology 'CloudFlare WAF'
      description 'Web application firewall for threat protection'
    }

    api = Container_Api 'API' {
      technology 'Go'
    }

    store = Container_Database 'Store' {
      technology 'PostgreSQL'
    }

    user -> firewall 'HTTPS request' { technology 'HTTPS' }
    firewall -> proxy 'Allowed traffic' { technology 'HTTPS' }
    proxy -> api 'Routes to API' { technology 'HTTP' }
    api -> store 'Reads/writes' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view portal_view of Portal {
    title 'Security Boundary Pattern'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- `Container_ReverseProxy` used for proxy but `Container` used for WAF (should be `Container_Waf`)
- Traffic traversal order slightly incorrect (WAF should come before proxy ideally)
- No deployment-level DMZ zone grouping
- Missing `#Dmz`, `#Security`, `#Networking` tags throughout
