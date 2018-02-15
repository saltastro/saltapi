This read me assume that you have python 3.5+ installed

# Installation

Cloning the repository.
On terminal or cmd. 
`cd` to the directory you want to work on with assumption that the directory is `home/development/` 

```
cd home/development/
git clone https://github.com/saltastro/saltapi.git

``` 

This will clone the repository to your machine. A directory will be created with the name `saltapi`

cd to the `home/development/saltapi/` dir 
```bazaar
cd home/development/saltapi/
```
Create virtual Environments and activate it, assumes that you have python3 virtualenv installed

```
   virtualenv -p python3 venv
   pip install --upgrade virtualenv
   source venv/bin/activate
```

and install reqirements.txt 

```bazaar
pip install -r reqirements.txt
```
# Environment variables
The app will require some Environment variables to be set
`API_USER, API_HOST, API_PASSWORD, API_DATABASE, MODE, DATABASE_URI `
which are the connection to the sdb, for development I am using sdb sandbox
```
    API_USER = sdb user
    API_HOST = sdb host
    API_PASSWORD = sdb password
    API_DATABASE = sdb database name
    PROPOSALS_DIR = directory containing all the proposal content
    SECRET_TOKEN_KEY = secret key for signing tokens
    SENTRY_DSN = URI for logging with Sentry
```

The URL stored in `SENTRY_DSN` must be obtained from [Sentry](https://docs.sentry.io). `SENTRY_DSN` is optional; if it isn't set, exceptions will be logged to the command line.

Now ready to start the graphql

to start the server

Make sure you are still in directory `home/development/saltapi/`  and Virtual environment is activated.

```bazaar
Run command.

python3 run.py
```

This will run on [http://127.0.0.1:5001/](http://127.0.0.1:5001). See about api on 
[http://127.0.0.1:5001/about](http://127.0.0.1:5001/about) to learn how to use this saltapi


# GraphQL Query

Graphql will only return what you asked for or an error.

On saltapi what ever you are querying for, a semester must be provided to improve the speed of query. 
i.e you can only query data belonging to provided semester  

### Query

```
{
  proposals(semester:"2017-2"){
    proposalcode{
      proposalCode
    }
  }
}
```

above query will return a json object. 

```
{
  "data": {
    "proposals": [
      {
        "proposalcode": {
          "ProposalCode": "2015-2-MLT-006"
        }
      },
      {
        "proposalcode": {
          "ProposalCode": "2016-2-MLT-001"
        }
      }, ... list continue ...
    ]
  }
}
```

You can learn more about graphql query on [graphql querys link](http://graphql.org/learn/queries/)

