import random

import httpx

from rich.console import Console
from cleverbot import SERVICES, CleverBotClient

console = Console()

url, service_endpoint = random.choice(list(SERVICES.values()))

console.print("Service: {}".format(url))

with console.status("Initialising Cleverbot client"):
    client = CleverBotClient.initialise(httpx.Client(), url=url, service_endpoint=service_endpoint)

console.print("Initialised Cleverbot client @ {}".format(client.service_url))

user_input = None

while user_input != '':
    with console.status("Communicating to Cleverbot"):
        response = client.communicate(user_input or '')

    if response is None:
        console.print("[red bold]Cleverbot did not respond as expected; please retry after a while.[/]")
    else:
        console.print("[green bold]Cleverbot response:[/] {}".format(response))

    user_input = console.input("[cyan bold]Send a message: [/]")
