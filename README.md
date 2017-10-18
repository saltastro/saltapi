this read me assume that you have python 3.5+ installed

# Installation

Cloning the repository.
On terminal or command line 
`cd` to the directory you want to work with assumption that the directory is `home/tac_developer/tac_dir/`  on and run command

```
cd home/tac_developer/tac_dir/
git clone https://github.com/saltastro/tacprocess.git
``` 

This will clone the repository to your machine

cd to the `cd tacprocess/` dir 
```bazaar
cd tacprocess/
```
create virtual Environments and activate it, assumes that you have python3 virtualenv installed

```
   virtualenv -p python3 venv
   pip install --upgrade virtualenv
   source venv/bin/activate
```

and install reqirements.txt 

```bazaar
pip install -r reqirements.txt

# Enironment valiables
the app will require some Enironment valiables to be set
`SANDBOX_USER, SANDBOX_HOST, SANDBOX_PASSWORD, SANDBOX_DATABASE, FLASK_DEBUG `
which are the connection to the sdb, for development I am using sdb sandbox
```
    SANDBOX_USER = sdb user
    SANDBOX_HOST = sdb host
    SANDBOX_PASSWORD = sdb password
    SANDBOX_DATABASE = sdb database name
    FLASK_DEBUG = 1 for development (This will activate GraphiQL for viewing data in a browser)
```

now you are up and ready

to start rhe server from `tacprocess/` dir 
cd to `server` dir and run `app.py` with python3
```bazaar
cd server\
python3 app.py
```

This will run on [http://127.0.0.1:5001/graphql](http://127.0.0.1:5001/graphql) if `FLASK_DEBUG = 1`
else you will have to provide a query like [http://127.0.0.1:5001/graphql?query={proposals(semester:"2017-2"){proposalCode}}](http://127.0.0.1:5001/graphql?query={proposals(semester:"2017-2"){proposalCode}})
which will return a list of proposal code of semester 2017-2 explained below


# GraphQL Query

assuming that `FLASK_DEBUG = 1` (on development.)

With graphql you query what you need in a structure you need it.

For this api what ever you are queiring for, a semester must be provided to impove the speed of query.

### Query

```
{
  viewer {
    proposals(semester:"2017-2"){
      proposalCode
    }
  }
}
```

this will return a json object 

```
{
  "viewer": {
    "data": {
      "proposals": [
        ...List of proposal code of that semester...
      ]
    }
  }
}
```

assume server is started.

going to [http://127.0.0.1:5001/graphql](http://127.0.0.1:5001/graphql) you will see what are the other thing to query 
for and type of data it is and other filters of data. Clicking `Docs` then `Query` it will show you other thing to query for
and arguments

```
{
  viewer {
    proposals(semester:"2017-2", partnerCode:"RSA"){
      proposalCode
      targets{
        name
        coordinates{
          ra
          dec
        }      
      }
    }
  }
}
```

the above Query will return 

```
{
  "viewer": {
    "data": {
        "proposals": [
            ...List of proposal code of that semester...
            ...List of targets per proposal: {
                Target name
                Coordinates of target :{
                RA
                DEC
                }
            }...
        ]
    }
  }
}
```

you can learn more about graphql querys on [graphql querys link](http://graphql.org/learn/queries/)

