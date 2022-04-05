"""
Using the free Cleverbot via a Discord Bot Cog.
"""

import random
import httpx
from cleverbot import SERVICES, CleverBotClient
from discord.ext import commands

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
}

class CleverBotCog(commands.Cog):

    def __init__(self):
        self.clients = {}

    async def get_client(self, identifier) -> 'CleverBotClient':
        
        if identifier not in self.clients:
            url, service_endpoint = random.choice(SERVICES.values())
            self.clients[identifier] = await CleverBotClient.initialise(httpx.AsyncClient(headers=headers, timeout=30.0, follow_redirects=True), url=url, service_endpoint=service_endpoint)
            
        return self.clients[identifier]

    @commands.group(aliases=['cb'], invoke_without_command=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def cleverbot(self, ctx: commands.Context, *, query: 'str'):
        """
        Communicate with the free Cleverbot.
        """
        client = await self.get_client(ctx.author.id)
        response = await client.acommunicate(query)

        if response is not None:
            return await ctx.send(response)
        
        return await ctx.send("API did not respond as expected; please retry after a while.")

    @cleverbot.error
    async def on_cleverbot_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"CleverBot is on cooldown for {error.retry_after:.2f} seconds.")
        raise error

def setup(bot):
    bot.add_cog(CleverBotCog())
