1. **Probable error category**
   - Relationship-scope mixup (logical vs deployment) + duplicated inherited traffic.

2. **Root cause**
   - In `model {}`, protocol was used as relationship type (`-[https]->`) instead of a logical kind with `technology`.
   - The same app traffic was redefined between deployed instances, creating duplication/noise.

3. **Verification step**
   - In logical model, confirm arrows use valid model kinds (`calls`, `reads`, `writes`, `async`, `uses`).
   - In deployment, check whether instance-to-instance edge duplicates an existing model relationship via `instanceOf`.

4. **Minimal fix**

```likec4
model {
  webapp -[calls]-> api 'Browser traffic' {
    technology 'HTTPS'
  }
}

deployment {
  // Keep instanceOf wiring; remove duplicated webapp->api deployment edge
}
```