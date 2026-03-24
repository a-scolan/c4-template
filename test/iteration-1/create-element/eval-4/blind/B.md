Start with one external system and one internal API container:

identityProvider = System_External 'Identity Provider' {
  technology 'OIDC / SAML'
  description 'Third-party identity provider used for authentication.'
}

Then, inside your portal system:

portalApi = Container_Api 'Portal API' {
  technology 'Node.js, Fastify'
  description 'Internal API that serves the portal application and portal backend workflows.'
}

That keeps the identity provider outside the system boundary and the portal API inside it, which is the right placement in this workspace.
