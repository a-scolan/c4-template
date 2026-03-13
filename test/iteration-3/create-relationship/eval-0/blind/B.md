Use a system-model relationship like:
webApp -[calls]-> api 'Makes API requests' {
  technology 'HTTPS'
}
The relationship type belongs inside the arrow as `-[calls]->`; the protocol belongs in the relationship block as `technology 'HTTPS'`.
