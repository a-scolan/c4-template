Wrong: extend frontend -> api 'streams'

Ici, omettre le kind est incorrect parce que deux relations distinctes avec le même source, target et titre existent déjà (`async` et implicite), donc l’instruction `extend frontend -> api 'streams'` est ambiguë et ne peut pas identifier de façon unique la relation à étendre.

extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }