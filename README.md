# Brandenburg


### Prepare your local environment

If you have already [pipenv](https://docs.pipenv.org) installed go to the run command or then install pipenv as showed on docs.

Then, install dev dependencies.

```
    pipenv install --dev
```

Inside of the project run the command to activate your environment

```
    pipenv shell
```

#### Running tests

```bash
    pipenv run test
```


#### To run locally

## API

````bash
    python api.py
````


#### Redis is the cache ;)

However, if you want to access the API you can just run the docker command and the API and WORKER will be up and
running in seconds. 

```
    docker-compose up -d
```


### Deployment

This app depends on some environment variables to run properly. 
You could see all of them in [config.py](config.py)


#### API Documentation

```
    http://127.0.0.1:8000/swagger/
```

#### Make a resquest
I have used [httpie](https://httpie.org/).

Get token

```bash
    http 127.0.0.1:8000/v1/leads/token/ 

```

send to Salesforce Marketing cloud

```bash
    http POST 127.0.0.1:8000/v1/leads/16db0bd3-579a-4a61-80b7-99f798013ee2 name=anitta email=anitta2@agrorede1.com phone_number=11912341678
```

Any problems or doubts, please feel free to contact me.

