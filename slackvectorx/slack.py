import data_backend
from gpt import generate_response
from healthcheck import run_healthcheck_server
from config import Config
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from threading import Thread

config = Config()
app = App(token=config.get("SLACK_BOT_TOKEN"), signing_secret=config.get("SLACK_SIGNING_SECRET"))
client = WebClient(token=config.get("SLACK_BOT_TOKEN"))

@app.event("message")
def handle_message(body, say):
    print("hit!")
    message = body['event']
    channel_id = message["channel"]
    user_id = message["user"]
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
            if messages['user_id'] != user_id:
                return
            messages['conversation'].append({'role': 'user', 'content': text})
        else:
            # get slack name of the user
            user_info_response = client.users_info(user=user_id)
            user_info = user_info_response['user']
            user_name = user_info['real_name']

            messages = {'user_id': user_id, 'user_name': user_name, 'conversation': [{'role': 'user', 'content': text}]}
        try:
            response = generate_response(messages)
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
    # Start the health check server in a separate thread
    health_check_port = 8080
    t = Thread(target=run_healthcheck_server, args=(health_check_port,))
    t.start()

    #Start slack listener
    slack_app_token = config.get("SLACK_APP_TOKEN")
    handler = SocketModeHandler(app, slack_app_token)
    handler.start()
