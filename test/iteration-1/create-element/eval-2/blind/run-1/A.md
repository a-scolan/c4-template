Use `create-element` for both declarations, `create-relationship` for the arrows, and `design-view` for the C2 view.

Start the elements like this:

virusScanProvider = System_External 'Virus Scan Provider' {
  technology 'HTTPS API'
  description 'Third-party malware scanning service.'
}

Then, inside the owning system:

scanApi = Container_Api 'Scan API' {
  technology 'Node.js, Fastify'
  description 'Submits files for scanning and returns scan results.'
}

So the split is: elements -> `create-element`, arrows -> `create-relationship`, C2 view -> `design-view`.
