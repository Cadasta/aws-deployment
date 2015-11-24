// Settings that don't vary with deployment environment here
var settings = {};

settings.useRollbar = {{ api_use_rollbar }};
settings.rollbarKey =  "{{ api_rollbar_key }}";

module.exports = settings;
