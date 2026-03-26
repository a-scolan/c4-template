view c2_containers {
  autoLayout LeftRight
  include *

  // single anchor to keep the actor visually on the left without brittle rank chains
  user -> webapp
}
