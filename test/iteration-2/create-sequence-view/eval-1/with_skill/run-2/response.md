That arrow should be corrected.

In a dynamic sequence, do **not** use parent → own-child (`api_container -> api_container.auth_component`). Start from the trigger and show collaborating participants:

```likec4
views 'Use Cases' {
	dynamic view authJourney {
		title 'Auth Journey'
		user -> api_container.auth_component 'Starts authentication'
		api_container.auth_component -> identityProvider 'Checks identity'
		api_container.auth_component -> sessionStore 'Persists session'
		api_container.auth_component -> user 'Authentication outcome'
	}
}
```

Anti-pattern to avoid: parent-to-own-child interactions.
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
