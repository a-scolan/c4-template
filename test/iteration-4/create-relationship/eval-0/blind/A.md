Use a system-model relationship, for example:
webApp -[calls]-> api 'Calls backend API' {
  technology 'HTTPS'
}
The relationship type is calls; it belongs on the system-model relationship between the two containers. The protocol or interaction detail, such as HTTPS, belongs in the relationship technology.
