Wrong: extend frontend -> api 'streams'
Omitting the kind is wrong because both a typed `-[async]->` and an unkinded `->` relationship exist with the same source, target, and title, so this matcher can select the unkinded relationship instead of the intended async one.
extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
