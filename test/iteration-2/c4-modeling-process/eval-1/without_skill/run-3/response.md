No, not by default.

Decision rule for C3:
- Do C3 when internal container structure is necessary to answer design questions.
- Skip C3 when C2 already communicates enough for current decisions.

Create C3 if at least one is true:
- Internal complexity is non-trivial
- Risks/compliance/security require internal traceability
- Performance/reliability design depends on internal components
- Multiple teams need clear component ownership

Otherwise keep the model lean at C2 and add C3 later if needed.