module.exports = {
  "production": {
    "pg":{
      "user":      "cadasta",
      "password":  "cadasta",
      "server":    "{{ db_host }}",
      "port":      "5432",
      "database":  "cadasta",
      "escapeStr": 'anystr'
    },
    "apiPort": "3000",
    "hostIp":  "0.0.0.0",
    "s3" : {
      "bucket": "{{ s3_bucket }}",
      "domain": "https://s3-{{ aws_region }}.amazonaws.com",
      "useEC2MetadataCredentials": true
    },
    "ona": {
      "host": "{{ apache_survey_url }}",
      "port": 80
    }
  }
};
