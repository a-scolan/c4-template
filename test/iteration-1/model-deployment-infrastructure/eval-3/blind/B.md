No—those two edges should usually **not** be added in `deployment.c4` for normal application traffic.

For ordinary service-to-service communication, put the protocol and optional port on the **system-model relationship**, for example:

```likec4
webApp -> apiApp 'Calls API' {
  technology 'HTTPS'
}

apiApp -> mongoDb 'Reads and writes metadata' {
  technology 'MongoDB'
}
```

If you need to show a non-default port, keep that detail on the logical relationship too, for example `technology 'HTTP/8080'`.

The deployment instances inherit those logical relationships through `instanceOf`, so you do not normally restate them again between deployed nodes.

Use deployment relationships only when the edge is truly infrastructure-specific, such as:

- monitoring or observability side channels
- database replication or backup flows
- bastion or admin access
- explicit network hops through a load balancer, firewall, proxy, or broker that matter operationally

So in your example, keep the app-to-app communication in the system model, and reserve deployment edges for the runtime wiring that exists only at infrastructure level.