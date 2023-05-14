import os
import data_backend
from gpt import generate_response
from config import Config
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
config = Config()
app = App(token=config.get("SLACK_BOT_TOKEN"), signing_secret=config.get("SLACK_SIGNING_SECRET"))
client = WebClient(token=config.get("SLACK_BOT_TOKEN"))

# Replace CHANNEL_ID with the ID of the specific channel you want the bot to respond in
SPECIFIC_CHANNEL_ID = "C0577KX8Z7Z"

# @app.message("hello")
@app.event("message")
def handle_message(body, say):
    print("hit!")
    message = body['event']
    channel_id = message["channel"]
    user = message["user"]
    ts = message["ts"]
    if 'thread_ts' in message:
        ts = message["thread_ts"]
    text = message["text"]
    print(body)
    # Check if the message is from the specific channel and not sent by the bot
    if 'bot_profile' not in message:
        # check if we already have something stored with this ts
        messages = data_backend.get(ts)
        if messages:
            if messages['user'] != user:
                return
            messages['conversation'].append({'role': 'user', 'content': text})
        else:
            messages = {'user': user, 'conversation': [{'role': 'user', 'content': text}]}
        try:
            response = generate_response(user, messages)
            messages['conversation'].append({'role': 'assistant', 'content': response})
            data_backend.set(ts, messages)
        except Exception as e:
            print("Error: {}".format(e))
            response = "Sorry, some neurons might be tangled. Please try again later."
        try:
            client.chat_postMessage(
                channel=channel_id,
                text=response,
                thread_ts=message["ts"]
            )
        except SlackApiError as e:
            print("Error posting message: {}".format(e))

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  print("hit!")
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "*Welcome to your _App's Home_* :tada:"
            }
          },
          {
            "type": "divider"
          },
          {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
            }
          },
          {
            "type": "actions",
            "elements": [
              {
                "type": "button",
                "text": {
                  "type": "plain_text",
                  "text": "Click me!"
                }
              }
            ]
          }
        ]
      }
    )

  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")

@app.error
def error_handler(error):
    print("Error: {}".format(error))

if __name__ == "__main__":
    slack_app_token = config.get("SLACK_APP_TOKEN")
    handler = SocketModeHandler(app, slack_app_token)
    handler.start()
    # app.start(port=int(os.environ.get("PORT", 5556)))
