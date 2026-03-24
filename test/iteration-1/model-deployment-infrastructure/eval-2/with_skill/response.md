Do not invent physical hosts you do not actually own or observe. If production runs on managed Kubernetes, keep the model honest by showing only the layers that are real in your operating model: `Node_Environment` for `Prod`, optionally a meaningful `Zone` if network segmentation matters, then a `Node_Cluster` for the managed Kubernetes cluster, and under that the deployed `Node_App` instances for the workloads you operate.

So the hierarchy can become `Prod -> AppTier/ProdCluster -> Node_App` instead of forcing fake `Node_Vm` entries. Honesty is better than invented infrastructure.

Wire `instanceOf` exactly the same way: each `Node_App` points to the corresponding logical container FQN. That preserves inherited relationships from the logical model. If one deployed runtime unit genuinely serves multiple logical containers as one managed unit, multiple `instanceOf` links are acceptable, but otherwise keep one `Node_App` per logical container.
