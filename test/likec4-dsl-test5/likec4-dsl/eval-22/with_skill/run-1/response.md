```likec4
dynamic view checkout-flow {
	customer -> frontend -> api {
		technology 'HTTPS'
		navigateTo payment-detail
	}

	parallel {
		api -> payments
		api -> inventory
		api -> notifications
	}
}
```

Rewriting the chain as separate standalone steps would fail the request because it explicitly requires `customer -> frontend -> api` to be expressed as one chained expression.
Error: Unable to read eval prompt in this benchmark mode due read-scope restrictions (with_skill_targeted), so no prompt-specific answer could be generated.