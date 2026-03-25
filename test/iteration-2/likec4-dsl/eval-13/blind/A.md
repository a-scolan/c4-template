model { api = service 'API' #critical { technology 'Node.js' } }

Why the original is invalid: `technology 'Node.js'` is a complete property statement, and `#critical` cannot be appended after it inside the block. In LikeC4, tags belong on the element declaration, not as trailing tokens after a property statement.
