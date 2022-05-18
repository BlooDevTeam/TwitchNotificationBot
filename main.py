import discord
import json
from discord.ext import commands, tasks
import requests

intents = discord.Intents(
    guilds=True,
    members=True,
    messages=True
)

bot = commands.Bot(command_prefix="prefix here", intents=intents)


def checkIfUserIsStreaming(username):
    """
    A function that checks if a Twitch user with the provided username is live. If the user is live it returns true, otherwise returns false.
    """
    
    url = "https://gql.twitch.tv/gql"
    query = """query($login: String) {
  user(login: $login) {
    stream {
      id
    }
  }
}"""
    return True if requests.post(
        url,
        json={"query": query, "variables": {"login": username}},
        headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"}).json()['data']['user']['stream'] else False


@bot.event
async def on_ready():
    """
    Prints to the console when the bot is active
    """

    print('\033[32m' + "Status: active")
    
    
    @tasks.loop(seconds=10)
    async def is_streamer_live():
        # Loading the twitch.json config file.
        with open('twitch.json', 'r') as f:
            twitch = json.load(f)
            
        channel = bot.get_channel("your channel id here")
        
        # Setting the value of the 'twitchUsername' key of the twitch.json to the username variable.
        username = twitch['twitchUsername']
        
        # Checking if the streamer is live.
        if checkIfUserIsStreaming(username):
            # Since we loop through the function every 10 seconds, we don't want ev every time to send a message to the channel, so we use a variable in the json
            # to check if we already sent a message.
            if twitch['isLive'] == 0:
                twitch['isLive'] = 1
                
                # Creating an embed message.
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      title=f'🟣 - {username} is live!')
                embed.set_thumbnail(url="url for twitch profile picture")
                embed.add_field(name='Channel:', value=f'https://www.twitch.tv/{username}')
                
                # Sending the embed message to the provided channel.
                await channel.send(f"Hey, @everyone! {username} is live! Go check out the stream!")
                await channel.send(embed=embed)
            else:
                pass
        else:
            twitch['isLive'] = 0
        
        # Commiting the changes we made to the twitch.json file.
        with open('twitch.json', 'w') as f:
            json.dump(twitch, f)
    # Starting the loop of the function.
    is_streamer_live.start()

# Run the bot.
bot.run('your bot token here')

