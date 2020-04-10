# ddd_bot
Joke Telegram bot I use in a friends group chat

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
3. in the `src` folder put a file named `dancan_msgs.txt`. It must contain lines of ''text messages'', since those are needed to generate fake text with the `/dancantext` command
4. Install dependencies with `pipenv install`
5. Type `pipenv shell`
6. Run the bot by giving the command `python main.py` or `python3 main.py`. That's it :)

## Commands
* `/start`
* `/help`
* `/dancanize`: reply to a text message with this command to get a picture with the replied text in it.
* `/dancantext`: generates and sends a fake text message. The message looks like it's written by the person who wrote the texts in the `dancan_msgs.txt` file.

## Other actions
* `AutoRespond`: when messages contain certain words, the bot will respond accordingly.
