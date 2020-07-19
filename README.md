# Brandenburg

## Concepts

`Important`: This project is following the [12factor.net](https://12factor.net/) principles


## Dependencies API

- Google Cloud Platform or AWS account 
- [Docker](https://docs.docker.com/get-docker/) (Optional)
- Python 3.7+ (pyenv)
- Pip (Pipenv)

### Optional (FaaS)
- Twillio Account (SMS, Whatsapp)
- Salesforce Marketing Cloud
- Sendgrid (Email)
- AWS (SES, SNS)
- Zenvia (SMS, Whatsapp)


# DEV Mode

`Important`:
    - This section is about [config](https://12factor.net/config)
    - This scripts was tested on MacOS and Linux(Debian like)
    - You could see all environment varibles in [config.py](brandenburg/config.py)
 

Inside of the project run the following commands.
This will check and install all dependencies as needed.

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

`Important`: This API is ready to deploy anywhere, however we are using heroku to do this job easily as posible.


### API on heroku



#### API Documentation

```
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

