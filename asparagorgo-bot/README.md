# asparagorgo_bot
Telegram bot for the white asparagus festival Asparagorgo.

## How to use
1. Clone the repository with `git clone`.
2. Enter in the `asparagorgo-bot` folder and create two folders and a text file:
   * `resources`: inside this folder put a json file named `config.json` with the bot token, e.g.:

      ```
      {
        "token": "XXXXXXXXX:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
      ```
   * `images`: here you have to put pictures used by the bot (look at the bot commands for more info).
   * `num_of_users.txt`: write `0` in it. Every time a new user will `/start` the bot, the number in this file will increase by 1.
3. Install dependencies with `pipenv install`.
4. Type `pipenv shell`.
5. Run the bot by giving the command `python main.py` or `python3 main.py`.

## Commands
* `/start`
* `/help`
* `/info`: menu with informations about the festival.
