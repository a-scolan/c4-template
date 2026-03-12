view applications {
  style * {
    color muted
  }

  style * where kind is Container_Api
     or kind is Container_Api_Geo {
    color primary
  }
}