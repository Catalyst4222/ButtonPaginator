<div align="center">
    <div>
        <h1>Button Paginator</h1>
        <span> <a href="https://pypi.org/project/discord-py-slash-command/"><img src="https://github.com/discord-py-slash-commands/discord-py-interactions/blob/master/.github/discordpyslashlogo.png" alt="discord-py-slash-command logo" height="10" style="border-radius: 50%"></a>
        With discord-py-slash-command</span>
    </div>
    <div>
    </div>
    <div>
        <h3>Button paginator using discord_slash</h3>
    </div>
</div>

## Welcome!
It's a paginator for discord-py-slash-command! 
Thanks to the original creators khk4912 (khk4912 /EZPaginator) and decave27 (decave27/ButtonPaginator)!

This project is open source ⭐, feel free to take inspiration from the code

The library being used has an [official discord server](https://discord.gg/KkgMBVuEkx), so if you have a question about how it works, feel free to ask it on this server.
## Install
```
pip install --upgrade dpy-slash-button-paginator
```

## Example
```py
from ButtonPaginator import Paginator
from discord.ext import commands
from discord_slash import SlashCommand
import discord

bot = commands.Bot("your prefix")
slash = SlashCommand(bot)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.command()
async def button(ctx):
    embeds = [discord.Embed(title="Page1"), discord.Embed(title="Page3"), discord.Embed(title="Page3")]
    contents = ["Text 1", "Text2", "Text3"]
    e = Paginator(bot=bot,
                  ctx=ctx,
                  header="An example paginator",
                  embeds=embeds,
                  contents=contents,
                  only=ctx.author)
    await e.start()

bot.run("your token")
```

## License
This project is under the MIT License.

## Contribute
Anyone can contribute to this by forking the repository, making a change, and create a pull request!

But you have to follow these to PR.
+ Use the black formatter.
+ Use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/).
+ Test.

## Thanks to
+ [khk4912](https://github.com/khk4912/EZPaginator) - Original Paginator developer
+ [decave27](https://github.com/decave27/ButtonPaginator) - Creator of the discord-components paginator that this was based on
+ LordOfPolls, fl0w, eunwoo, and everyone else who works on the [discord-py-slash-command lib](https://github.com/discord-py-slash-commands/discord-py-interactions)
