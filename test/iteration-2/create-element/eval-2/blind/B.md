Break it into three concerns.

For the element declarations, use existing workspace kinds:

```likec4
virusScanProvider = System_External 'Virus Scan Provider' {
  technology 'Third-party malware scanning API'
  description 'External service that scans uploaded files for malware'
}

scanApi = Container_Api 'Scan API' {
  technology 'Node.js, Express'
  description 'Internal API that submits files for scanning and returns scan results'
}
```

Then handle the rest separately:

- The arrows belong in relationship declarations between the relevant elements.
- The C2 diagram belongs in a container view definition.

So keep this step focused on declaring the two elements first, and add relationships and the C2 view as separate modeling steps.