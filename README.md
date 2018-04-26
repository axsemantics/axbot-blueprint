# General

__This code is solely for exemplary purposes. This is not production-ready code, so use at your own risk.__

Axbot-blueprint is a django project that connects the dialogflow webservice for natural language understanding with the AX Semantics webservice for automated text generation.

This project uses docker, nginx, gunicorn and django. The default settings of this tools were slightly changed to speed up the development process. __For production you have to check the settings and configure them appropriately (e.g: remote/cloud database).__



# Prerequisite

1. install [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1)
2. install [docker-compose](https://docs.docker.com/compose/install/#prerequisites)

## Authentification

1. Enter the __Refresh Token__ that belongs to your _AX Semantics_ account to your app. It gives your app the permission to communicate with AX Semantics.
    - go to [AX Semantics cockpit](https://cockpit.ax-semantics.com/)
    - go to your profile settings
    - select __Advanced settings__
    - click _API access_
    - copy the __Refresh Token__
    - set the _refresh_token_ in your app
        + navigate to the views.py file in your app directory
        e.g.: ../axbot-blueprint/axbot/YOURAPP/views.py
        + in the code, search for the class ...Bot(AX)
        + paste the __refresh token__ as value for the variable refresh_token
    
    - Documentation: https://documentation.ax-semantics.com/v2/api/authentification

## Instant Generation API

1. Activate _Instant Generation Endpoints_ for your account.
    - go to [AX Semantics cockpit](https://cockpit.ax-semantics.com/)
     - go to your profile settings   
    - select __Advanced settings__
    - click on the switch for _Instant Generation Endpoints_
2. Create an _Instant Generation Endpoint_ for your project.
    - switch into your AX Semantics project 
    - click the _gear symbol_ next to the project name in the top left corner
    - select the _Instant Generation Endpoints_ entry
    - click the green button __create a new instant generation endpoint__
    - fill out fields
        + webhookurl pattern: $DOMAINNAME/$APPNAME/axwebhook/ 
        + e.g.: www.example.de/myfirstapp/axwebhook/
    - configure the endpoint
        + Delivery Format : text
        + Used Ruleset Version: draft for testing, publish for production
    - set the instant generation endpoint id in your app
        + copy the __ID__ from the _Instant Generetion Endpoints_ 
        + navigate to the views.py file in your app directory
        e.g.: ../axbot-blueprint/axbot/YOURAPP/views.py
        + in the code, search for the class ..AxWebhook(AxWebhook)
        + paste the __ID__ as value for the variable instant_id
    - set the instant generation endpoint webhook secret in your app
        + copy the __webhook secret__ from the _Instant Generetion Endpoints_ 
        + navigate to the views.py file in your app directory
        e.g.: ../axbot-blueprint/axbot/YOURAPP/views.py
        + in the code, search for the class AxWebhook(View)
        + paste the  __webhook secret__ as value for the variable webhooksecret

    - Documentation: https://documentation.ax-semantics.com/v2/api/instant-generation
    - Dev-Docs: https://developers.ax-semantics.com/v2/instant-generation-requests/instant-request-api


# Dialogflow Fulfillment

1. Configure your Dialogflow Agent to use the AX Semantics webservice
    - got to your dialogflow project/agent
    - select the fulfillment menu
    - enter the endpoint (url) of your project as webhook url in dialogflow e.g.: www.example.de/myfirstapp/text/
    - press __SAVE__!
    - activate the  _fulfillment_ option in your intents
        + select the intent menu
        + open your intent(s)
        + scroll to the section __Fulfillment__
        + press the button __Enable webhook call for this intent__
        + __SAVE__!
## For local testing

1. use the tool [ngrok](https://ngrok.com/)
    - start ngrok
        + use the port that you configured in docker (we set port 8000)
    - use the generated ngrok-url as webhook url in dialogflow (e.g. https://123456.ngrok.io/YOURAPPNAME/text/)
# Setup

Before you start to build and run the docker you need to create and insert a [SECRET_KEY](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SECRET_KEY)
```
cd axbot-blueprint/axbot/axbot/settings/
vim base.py
```


## dev/test


```
cd axbot-blueprint
docker-compose build --pull
docker-compose pull
docker-compose run --rm web python3 manage.py reset_db
docker-compose run --rm web python3 manage.py migrate
docker-compose up -d
```
## deploy

-  configure the docker port in docker-compose.deploy.yml to your enviroment
    + at the moment the port is only mapped to localhost:8000
    + use your preferred webserver and proxy it to localhost:8000 

```
cd axbot-blueprint
sudo docker-compose -f docker-compose.deploy.yml build --pull
sudo docker-compose -f docker-compose.deploy.yml pull
docker-compose -f docker-compose.deploy.yml run --rm django python3 manage.py reset_db
sudo docker-compose -f docker-compose.deploy.yml run --rm django python3 manage.py migrate
sudo docker-compose -f docker-compose.deploy.yml up -d
```

- optional:  
`docker-compose run --rm web createsuperupser`