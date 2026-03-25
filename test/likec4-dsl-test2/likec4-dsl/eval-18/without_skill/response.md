No. `extend` on relationships is not a fuzzy match. It must match the existing relationship's identity: the same source, the same target, the same direction, the same relationship kind/operator, and the same title/label when one is present. So `extend frontend -> api 'streams'` does not match `frontend -[async]-> api 'streams'` because `->` and `-[async]->` are different relationship kinds. The extension also needs to resolve to exactly one existing relationship.

Use this instead:

extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
