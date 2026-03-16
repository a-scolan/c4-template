Use reads when the target is a data store and the interaction is data retrieval. Use calls for synchronous service-to-service API calls. Since Redis and PostgreSQL are stores here, model them as reads.
Example:
retrievalService -[reads]-> redis 'Checks cache'
retrievalService -[reads]-> postgres 'Loads record on miss' {
  technology 'PostgreSQL'
}
If the service also updates either store, add separate writes relationships for those mutations.
