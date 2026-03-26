# Eval-3 — Implement DMZ Security Zone Pattern (Baseline, Run 1)

## Prompt

> Implement a DMZ security zone pattern. Add a Web Application Firewall (WAF) and a reverse proxy in a demilitarized zone in front of the application tier. Use appropriate element kinds and tags from the shared specification and model the traffic flow from the internet through the security boundary.

---

## Response

I will add a WAF and reverse proxy to sit between the internet zone and the application tier, forming a DMZ.

### Model additions

```likec4
model {
  internet = Actor_Person 'Internet User' {
    description 'Public user accessing the system over internet'
  }

  system SecurePlatform 'Secure Platform' {
    waf = Container 'Web Application Firewall' {
      technology 'ModSecurity'
      description 'Inspects and filters HTTP traffic'
    }

    reverseProxy = Container 'Reverse Proxy' {
      technology 'Nginx'
      description 'Terminates SSL and forwards clean traffic'
    }

    appServer = Container_Webapp 'Application Server' {
      technology 'Spring Boot'
      description 'Business logic'
    }

    db = Container_Database 'Database' {
      technology 'PostgreSQL'
    }

    internet -> waf 'HTTPS request' { technology 'HTTPS' }
    waf -> reverseProxy 'Filtered traffic' { technology 'HTTP' }
    reverseProxy -> appServer 'Forwarded request' { technology 'HTTP' }
    appServer -> db 'Data access' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view dmz_view of SecurePlatform {
    title 'DMZ Security Zone'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- Used generic `Container` instead of `Container_Waf` and `Container_ReverseProxy` from shared spec
- Missing `#Dmz`, `#Security`, `#Ingress` tags that define the security zone
- Zone grouping not used (should use `Zone` deployment node for DMZ boundary)
- Traffic flow modeled correctly but without typed relationship kindsModel this as two separate interactions: outbound payment creation and inbound webhook callback.

- Internal payment initiator: `Container_Api`
- External Stripe: `System_External` (and `#Saas` if desired)
- Internal webhook receiver: `Container_Api` endpoint/service

Recommended pattern:

```likec4
paymentsApi = Container_Api 'Payments API' {
  #Internal
}

webhookApi = Container_Api 'Payment Webhook Endpoint' {
  #Internal
}

stripe = System_External 'Stripe' {
  #External
  #Saas
}

paymentsApi -[calls]-> stripe 'Create payment intent' {
  technology 'HTTPS'
}

stripe -[calls]-> webhookApi 'Payment confirmation webhook' {
  technology 'HTTPS'
}
```

To avoid implying a synchronous return, do not model the confirmation as an immediate response edge back to `paymentsApi` from the first call. Keep the webhook as an independent inbound event path.