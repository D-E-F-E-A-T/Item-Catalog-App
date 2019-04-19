#Item Catalog Project

##About
This is a Udacity Full stack Project, it's an application that provides a list of movies within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Requirements
-   [VirtualBox](https://www.virtualbox.org/)
-   [Vagrant](https://www.vagrantup.com/)
-   [Python 2.7](https://www.python.org/)
-   [sqlalchemy_utils](http://initd.org/psycopg/docs/install.html)
-   [Bash terminal(for windows machine)](https://git-scm.com/downloads)
-   [Google Chrome](https://www.google.com/chrome/?brand=CHBD&gclid=Cj0KCQjw4-XlBRDuARIsAK96p3DW6f6PEkMr3F6pRf5j55RnMkc4H5VdnjfjVdfqmuG04VKRDK7ej8kaAktLEALw_wcB&gclsrc=aw.ds)

## Getting things ready
1. Install Python
2. Install Virtual Box
3. Install Vagrant 
4. Install sqlachemy_utils
5. Clone or download the Vagrant VM configuration file from [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm)
6. Clone or download this repo

## Run the application 
1. Extract Vagrant VM configuration file
2. Extract and move the repo to Vagrant folder within the extracted Vagrant VM configuration file
3. Open terminal and cd the Vagrant VM configuration file
3. run this two commands :
    >vagrant up
    >vagrant ssh
to run the virtual machine
4. cd the vagrant folder then the repo folder : cd vagrant/ItemCatalogFinalProject
5. run : python app.py
6. open google chrome and visit http://localhost:5000/
