# Harvard College Exulting Group

### Setup
These instructions assume you have Python 3.6 or newer installed.

#### Ubuntu / Mac OS
I have written a script to run all the necessary commands. Simply navigate to this directory in your terminal, and run the following command:
```source ./init/unix```
The script should create and activate a virtual environment for the server to run. If this doesn't work, you can try running the following commands:
```bash
[[ -d "./environment" ]] || python3 -m venv environment
source ./environment/bin/activate
pip install -r requirements.txt
```

#### Windows
To use my setup script, navigate to this directory in a command prompt and run
```init/windows```
If this doesn't work, or you get any error, you can try running the commands manually:
```bash
python -m venv environment
environment/Scripts/activate
pip install -r requirements.txt
```
The first command creates the virtual environment, the second command activates it, and the third command installs necessary python packages. You should only ever need to run the first command once.

### Running the Server
To run the server, use ``flask run``. The website is hosted at [http://localhost:5000/](http://localhost:5000). To submit your own content, navigate to [http://localhost:5000/login](http://localhost:5000/login) and click the link to create your own account. You will have to provide that master password (``iamtheinvisiblehand``) to prove your not a hacker/marxist. Once you have logged in, you will be redirected to [http://localhost:5000/submit](http://localhost:5000/submit), where you can submit new content. The original [HCCG](http://harvardconsulting.org) website doesn't really have articles, so this website will support three types of content:

##### Pages
These are webpages from the original website that have not yet been implemented. Currently, the website gives a 404 error for these webpages. (It used to redirect to random wikipedia pages, but I thought the 404 errors would be more consistent). These pages support html syntax, and once you submit a page, you can navigate to it by accessing the corresponding url, or clicking the corresponding link in the top menu.

##### Clients
Adding a client will add their picture to the list of clients on the homepage, and add their comment as a testimonial on the clients page.

##### Analyst
Adding an analyst will add them to the analysts overview page at [http://localhost:5000/analysts/overview](http://localhost:5000/analysts/overview).

When you are finished, you can exit with ``Ctrl+C`` and run ``deactivate`` to disable the virtual environment. Simply follow the steps above to restart the server.

I hope you enjoy this website! If you have any questions, feedback, or errors, feel free to email me at [justinwise@college.harvard.edu](justinwise@college.harvard.edu).
