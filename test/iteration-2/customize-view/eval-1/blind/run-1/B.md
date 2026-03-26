view c2_containers {
  include *

  style element.tag == #Api {
    opacity 100%
    border solid
  }

  style element.tag != #Api {
    opacity 20%
  }
}
