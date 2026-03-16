Assuming the elements already exist in your model, a clean LikeC4 dynamic-view skeleton is:
views {
  dynamic view login_journey {
    title 'Login journey'
    include user, webApp, api, primaryDb, notificationService

    user -> webApp 'Open login form and submit credentials'
    webApp -> api 'POST /login'
    api -> primaryDb 'Read user and verify credentials'
    api -> notificationService 'Send login notification'
    api -> webApp 'Return session or token'
    webApp -> user 'Show signed-in state'
  }
}
If the notification is asynchronous in your model, make that underlying relationship `async` rather than `calls`.
