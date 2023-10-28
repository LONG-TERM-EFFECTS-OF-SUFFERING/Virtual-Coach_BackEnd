# Virtual Coah (BackEnd)

## Set up

1. Clone the repository to your local machine.

2. Configuration of the virtual environment.

	You can use [**venv**](https://docs.python.org/es/3.8/library/venv.html) (a module that comes with Python 3.3 or higher versions) for this purpose:

	1. Create it: `python -m venv <envname>`.

		> I recommend creating it in the root folder of the project.

	2. Activate it.

		- Bash or ZSH: `source <envname>/bin/activate`.

		- CMD: `<envname>\Scripts\activate.bat`.

		- PowerShell: `<envname>\Scripts\Activate.ps1`.

	> To exit the virtual environment use the `deactivate` command.

3. Install the project requirements: `pip install -r <requirements file>`.

	> Remember to do it inside the virtual environment.

4. Ask for the `.env` file.

	> This file contains all the credentials needed to connect to the project database.

5. Run the BackEnd.

	1. `python manage.py makemigrations`.

	2. `python manage.py migrate`.

	3. `python manage.py runserver`.

## Endpoints

All endpoints are specified in the url files of the applications (in the case of application routines). Sumarizing we have:
