<h1 align="center">CleverBot</h1>

<p align="center">A free and open-source client to CleverBot with an optional <code>async</code> support.</p>

<p align="center">
The CleverBot API is wildly expensive. For developers who want to first test the client over their own variety of projects, it is an unnecessary expense.
</p>

<p align="center">
Sure, you can test the bot in multiple websites but that is not <i>your</i> project. It is limiting in terms of use case and external plugins such as your own fancy cache system and ratelimits.
</p>

<h3 align="center">Usage</h3>

Copy the `cleverbot` package to your project directory.

```py
"""
This is a basic demonstration.
"""
import httpx
import random

from cleverbot import SERVICES, CleverBotClient

url, service_endpoint = random.choice(list(SERVICES.values()))
"""
We randomise the services to reduce the chances of service errors.
"""

client = CleverBotClient.initialise(httpx.Client(), url=url, service_endpoint=service_endpoint)

print(client.communicate("Hello babe!"))
```

See <a href="./example-dpy_cog.py">the discord.py Bot Cog</a> implementation to get a knowledge of how the client may be used with async.

See <a href="./example-cli.py">the `rich` cli</a> implementation to get a knowledge of how the client may be used in cli.


<h3 align="center">Disclaimer</h3>

<p align="center">
You can utilise this project but remember, this is a test suite. It'll often throw out unexpected results; basically <code>None</code>. That's the cost of "free". (You can easily handle this.)
</p>

<p align="center">
The developers of this project are not responsible for consequences that is brought in to the user by the project. Buy the required package from the <a href="https://www.cleverbot.com/api/">official CleverBot API</a> if you want to use CleverBot commercially.
</p>
