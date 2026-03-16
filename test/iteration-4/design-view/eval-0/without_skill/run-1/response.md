Following the workspace layout, put the model in `projects/template/system-model.c4` and the view in `projects/template/system-views.c4`, or mirror that same pair in the project folder you are working on.

Use `Actor_Person` for the user, `System_External` for the third-party email provider, and model your own application as a system with C2 containers inside it. A clean skeleton is:

In `system-model.c4`:
customer = Actor_Person User
emailService = System_External Email Service

uploadPlatform = System_New Upload Platform {
  web = Container_Webapp Web Application { technology ... }
  api = Container_Api Upload API { technology ... }
  db = Container_Database Metadata DB { technology ... }
}

customer -[uses]-> uploadPlatform.web Starts upload { technology Manual }
uploadPlatform.web -[calls]-> uploadPlatform.api Submits files { technology HTTPS }
uploadPlatform.api -[writes]-> uploadPlatform.db Stores metadata { technology SQL }
uploadPlatform.api -[calls]-> emailService Sends notification { technology SMTP }

In `system-views.c4`, create one container view for `uploadPlatform` that includes `customer`, `emailService`, and `uploadPlatform.*`, with `autoLayout LeftRight`.

For drill-down, make the web application the entry point to a second, more detailed view later. In practice: keep the C2 view centered on `uploadPlatform.web`, then add a separate web-app-focused view when you define its internal components. Also, use `System_External` for the email provider rather than modeling it as one of your own containers.
