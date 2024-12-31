# BrettBot
World's greatest Discord bot. Designed for a Discord server with some friends.

### Updating Requirements.txt:

Before pushing a change, update requirements.txt. Doing so ensures the bot can run once its libraries are updated. You can update requirements.txt to use the libraries you've added using the terminal in Pycharm.

First, execute the command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process" in the terminal to prevent permissions issues.

Then, activate your virtual environment using ".\activate.ps1" from the current working directory.

Finally, execute "pip freeze > requirements.txt" to update requirements.txt with the libraries you've added.