I would start with these direct declarations:
identityProvider = System_External 'Identity Provider'
portalApi = Container_Api 'Portal API'

If portalApi belongs under an existing system, place that line inside the system block.
