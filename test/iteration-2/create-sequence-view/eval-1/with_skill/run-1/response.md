Good catch to question that.

`api_container -> api_container.auth_component` is the wrong pattern in a dynamic view because it models parent → own-child interaction.

Use the initiating actor and the real collaborating elements instead, inside `views 'Use Cases'`:

```likec4
views 'Use Cases' {
	dynamic view authenticationFlow {
		title 'Authentication Flow'
		user -> api_container.auth_component 'Submits credentials'
		api_container.auth_component -> identityProvider 'Validates credentials'
		api_container.auth_component -> sessionStore 'Creates session'
		api_container.auth_component -> user 'Returns authenticated result'
	}
}
```

Critical anti-pattern: avoid parent-to-own-child arrows in dynamic steps.
## Correcting Parent → Own-Child in a Dynamic View

The pattern `api_container -> api_container.auth_component` is the **parent → own-child anti-pattern** and must not appear in a dynamic view.

### Why it's wrong

A dynamic view shows **message flow between actors**. A container calling one of its own child components represents internal implementation detail — there is no meaningful external sender in the flow.

### Fix: Start from the real initiator

```likec4
// ❌ Wrong
api_container -> api_container.auth_component 'Authenticates'

// ✅ Correct: begin from the actual external caller
user -> api_container.auth_component 'Sends credentials'
api_container.auth_component -> directoryService 'Validates token'
api_container.auth_component -> api_container.sessionManager 'Creates session'
```

Replace `api_container` as the source with the **actual external actor or upstream element** that triggers authentication. The child component (`auth_component`) becomes the first receiver in the chain.
