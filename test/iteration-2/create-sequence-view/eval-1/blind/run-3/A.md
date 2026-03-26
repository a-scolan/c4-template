Correct approach: replace parent→child with actor-triggered, action-focused steps in `views 'Use Cases'`.

```likec4
views 'Use Cases' {
	dynamic view loginAuthSequence {
		title 'Login Authentication Sequence'
		user -> api_container.auth_component 'Provides credentials'
		api_container.auth_component -> identityProvider 'Verifies credentials'
		api_container.auth_component -> sessionStore 'Stores auth session'
		api_container.auth_component -> user 'Returns success/failure'
	}
}
```

Critical anti-pattern: `api_container -> api_container.auth_component` in a dynamic view.
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
