Prefer autoLayout lr first, and only add one anchor if the actor still drifts:

view c2_containers of mySystem {
  autoLayout lr
}

Optional single anchor:

view c2_containers of mySystem {
  autoLayout lr
  rank user -> mySystem.webapp
}
