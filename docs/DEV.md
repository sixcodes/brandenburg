# Dev mode


- habilitar o pubsub no gCP
- criar as credenciais e projeto
- configurar envVARS
- executar

## Heroku deploy

```shell
    heroku buildpacks:set https://github.com/heroku/heroku-buildpack-python\#v134
```

pipenv, version 2018.05.18

functions-framework --target salesforce --signature-type event --debug

echo '{"context": {"eventId": "some-eventId", "timestamp":
"some-timestamp","eventType":"some-eventType", "resource": "some-resource"}, "data": {"data":
"b2s="}}' | http POST 127.0.0.1:8080/
