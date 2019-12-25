# ddd_bot
Joke Telegram bot I use in a friend group chat

## How to use
1. Clone the repository with `git clone`.
2. Enter in the `ddd_bot` folder and create two folders:
   * `resources`: inside this folder put a json file named `config.json` with the bot token, e.g.:

      ```
      {
        "token": "XXXXXXXXX:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
      ```
   * `images`: here you have to put pictures used by the bot. E.g.: for the command `/dancanize`, put a picture named `base.jpg`.
3. Run the bot by going in the main folder and giving the command `python main.py` or `python3 main.py`. That's it :)

## Commands
* `/help`
* `/dancanize`: reply to a text message with this command to get a picture with the replied text in it.
