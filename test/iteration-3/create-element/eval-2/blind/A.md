Start with the element declarations:
virusScanProvider = System_External 'Virus Scan Provider' {
  technology 'HTTPS API'
  description 'Third-party malware scanning service used before file acceptance.'
}
Inside your existing system block:
scanApi = Container_Api 'Scan API' {
  technology 'Node.js, Fastify'
  description 'Internal API that submits files for scanning and exposes scan results.'
}
Then use `create-relationship` for the arrows and `design-view` for the C2 view. This skill handles the element declarations first.
