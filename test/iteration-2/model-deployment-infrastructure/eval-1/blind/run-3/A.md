For `Dmz -> AppTier -> ProcTier -> DataTier` with firewall policy details, this skill is only the baseline.

Best action: switch to **`structure-deployment-tiers`** for the tiered-zone design and inter-tier firewall modeling. Keep using this skill for naming, hierarchy hygiene, VM/Node_App structure, and `instanceOf` wiring.

Practical split:

- Here (`model-deployment-infrastructure`): Environment/Zone/VM/App hierarchy + VM naming + descriptions.
- Next (`structure-deployment-tiers`): tier topology and firewall flow rules between zones.