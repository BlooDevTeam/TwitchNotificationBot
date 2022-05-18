import discord
import json
from discord.ext import commands, tasks
import requests

intents = discord.Intents(
    guilds=True,
    members=True,
    messages=True
)

bot = discord.Client(intents=intents)


def checkIfUserIsStreaming(username):
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
        with open('twitch.json', 'r') as f:
            twitch = json.load(f)

        channel = bot.get_channel(976532019674742864)
        username = twitch['twitchUsername']
        print(checkIfUserIsStreaming(username))
        if checkIfUserIsStreaming(username):
            if twitch['isLive'] == 0:
                twitch['isLive'] = 1
                print(twitch['isLive'])
                embed = discord.Embed(colour=discord.Colour.purple(),
                                      title=f'🟣 - {username} is live!')
                embed.set_thumbnail(url='https://static-cdn.jtvnw.net/jtv_user_pictures/50dd15e2-beb9-4058-abc1-'
                                        '77a29c6b896b-profile_image-70x70.png')
                embed.add_field(name='Channel:', value=f'https://www.twitch.tv/{username}')
                await channel.send(f"Hey, @everyone! {username} is live! Go check out the stream!")
                await channel.send(embed=embed)
            else:
                pass
        else:
            twitch['isLive'] = 0

        with open('twitch.json', 'w') as f:
            json.dump(twitch, f)
    is_streamer_live.start()



bot.run('OTc2NTQwNTI4OTgyMjI5MDUy.GDW6XV.fpw1BLeIfRPpdyic-HXI_QYpbgJK_wULFFR4ss')

