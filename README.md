# The backend project for Mr Spice, built with Flask
## see [mrspice-ionic](https://github.com/nigel-smk/mrspice-ionic) for the frontend project
## mrspice-cli is a command line tool used to pre-process the recipe data. This part of the project is currently closed-source. Feel free to request access to view the repository on bitbucket.


# Getting Started

## Python Environment Management
- I recommend installing [conda](https://conda.io/docs/user-guide/install/index.html)
    - it allows you to create project-specific environments in which you can install packages
    - kind of similar to npm
- read the docs on how to [create a new environment and activate it](https://conda.io/docs/user-guide/getting-started.html#managing-envs)
    - environments are where you "install" packages, similar to npm
- once you have your environment setup and activated, use `pip` to install the modules in `requirements.txt`
    - `pip install -r requirements.txt`

## MongoDB
- [install MongoDB Community Edition](https://docs.mongodb.com/manual/administration/install-community/)
- [familiarize yourself with the mongo shell](https://docs.mongodb.com/manual/mongo/#working-with-the-mongo-shell)
    - you will use it to create/view databases and run test queries
- create a new database (config_template.py defaults to `yummly` for the name)
```
use yummly
```
- [create a dev user for the database](https://docs.mongodb.com/manual/reference/method/db.createUser/#create-user-with-roles)
```
use yummly
db.createUser(
    {
        user: "dev",
        pwd: "dev",
        roles: [ 
            {
                role: "readWrite", 
                db: "yummly"
            }
        ]
    }
)
```
- [import the data dump into your database](https://docs.mongodb.com/manual/reference/program/mongorestore/#bin.mongorestore)
    - you will need to make a request to the project owner for the data dump file

## Setup your Config
- copy the `config_template.py` contents to a file called `config.py`
    - you will not need the yummly api key to get started so don't worry about it just yet

## Postman
- import the postman collection



#### To investigate
Foodpairing by flavour
http://www.foodpairing.com/en/home

Flavour Network paper
http://www.nature.com/articles/srep00196

Datasets
https://www.kaggle.com/c/whats-cooking/data
https://datahub.io/dataset/recipe-dataset

