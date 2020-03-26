# Harvard College Exulting Group

### Setup
These instructions assume you have Python 3.6 or newer installed.

#### Ubuntu / Mac OS
I have written a script to run all the necessary commands. Simply navigate to this directory in your terminal, and run `source ./init` and the script should create and activate a virtual environment for the server to run. If this doesn't work, you can try running the following commands:
```bash
[[ -d "./environment" ]] || python3 -m venv environment
source ./environment/bin/activate
pip install -r requirements.txt
```

#### Windows
To setup the server, you must create a virtual environment and install all necessary python packages. To do so, open a command prompt, navigate to the current directory, and run the following commands:
```bash
python -m venv environment
environment/Scripts/activate
pip install -r requirements.txt
```
The first command creates the virtual environment, the second command activates it, and the third command installs necessary python packages. You should only ever need to run the first command once.

### Running the Server
To run the server, use ``flask run``. When you are finished, you can exit with ``Ctrl+C`` and run ``deactivate`` to disable the virtual environment. Simply follow the steps above to restart the server.

If you have any questions, feedback, or errors, feel free to email me at [justinwise@college.harvard.edu](justinwise@college.harvard.edu).
