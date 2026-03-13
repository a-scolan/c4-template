Start with these declarations:
identityProvider = System_External 'Identity Provider' {
  technology 'OIDC / SAML'
  description 'Third-party identity provider used to authenticate portal users.'
}
Inside your portal system block:
portalApi = Container_Api 'Portal API' {
  technology 'Node.js, Fastify'
  description 'Internal API that serves portal features and coordinates portal business operations.'
}
That gives you the two elements directly, without getting into relationships or views.
