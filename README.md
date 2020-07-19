# Brandenburg

## Concepts

`Important`: This project is following the [12factor.net](https://12factor.net/) principles


## Dependencies API

- Google Cloud Platform or AWS account 
- [Docker](https://docs.docker.com/get-docker/) (Optional)
- Python 3.7+ (pyenv)
- Pip (Pipenv)

### Optional (FaaS)
- Twilio Account (SMS, Whatsapp)
- Salesforce Marketing Cloud
- Sendgrid (Email)
- AWS (SES, SNS)
- Zenvia (SMS, Whatsapp)


## DEV Mode

`Important`:
    - This section is about [config](https://12factor.net/config)
    - This script has been tested on macOS and Linux(Debian like)
    - You could see all environment variables in [config.py](brandenburg/config.py)
 
Inside of the project you have to run the following commands.
It will check and install all dependencies as needed.
```
script/bootstrap
```

Copy `example.env` to `dev.env` and set the variables though.

#### Running tests

```bash
script/test
```


#### To run locally

## API

````bash
script/server
````

### Deployment

`Important`: This API is ready to deploy anywhere. However, we are using Heroku to do this job as easy as possible.


### API on Heroku



#### API Documentation

```bash
http://127.0.0.1:8000/docs/
```

#### Make a resquest
I have used [httpie](https://httpie.org/) to do this job.

Getting a token

```bash
http 127.0.0.1:8000/v1/leads/token/ 
```

Sending to Salesforce Marketing cloud

```bash
http POST 127.0.0.1:8000/v1/leads/16db0bd3-579a-4a61-80b7-99f798013ee2 name=anitta email=anitta2@agrorede1.com phone_number=11912341678
```

Any problems or doubts, please feel free to contact me.


