Wrong: extend frontend -> api 'streams'
Because two relationships share the same source, target, and title, omitting the kind is wrong here: it can match the unkinded relationship instead of the intended `async` one.
extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
