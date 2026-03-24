A direct starting point is:
`identityProvider = System_External 'Identity Provider'`
`mySystem { portalApi = Container_Api 'Portal API' }`
That keeps the third-party provider external and the portal API internal, without solving relationships yet.
