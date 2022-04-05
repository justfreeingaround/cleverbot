import random

import httpx

from rich.console import Console
from cleverbot import SERVICES, CleverBotClient

console = Console()

url, service_endpoint = random.choice(list(SERVICES.values()))

console.print("Service: {}".format(url))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
}

with console.status("Initialising Cleverbot client"):
    client = CleverBotClient.initialise(httpx.Client(timeout=30.0, headers=headers, follow_redirects=True), url=url, service_endpoint=service_endpoint)

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
