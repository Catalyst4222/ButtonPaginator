import discord
# from discord import InvalidArgument
import discord_slash.model
from discord.ext import commands

import asyncio
from typing import List, Optional, Union, Tuple

# from discord_components import (
#     Button,
#     ButtonStyle,
#     InteractionType,
# )
# from discord_components import Interaction

from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component

from .errors import MissingAttributeException, InvaildArgumentException

EmojiType = List[Union[discord.Emoji, discord.Reaction, discord.PartialEmoji, str]]


class Paginator:
    def __init__(
            self,
            bot: Union[
                discord.Client,
                discord.AutoShardedClient,
                commands.Bot,
                commands.AutoShardedBot,
            ],
            ctx: ComponentContext,
            contents: Optional[List[str]] = None,
            embeds: Optional[List[discord.Embed]] = None,
            timeout: int = 30,
            use_extend: bool = False,
            only: Optional[discord.User] = None,
            basic_buttons: Optional[EmojiType] = None,
            extended_buttons: Optional[EmojiType] = None,
            left_button_style: Union[int, ButtonStyle] = ButtonStyle.green,
            right_button_style: Union[int, ButtonStyle] = ButtonStyle.green,
            auto_delete: bool = False,
    ) -> None:
        self.bot = bot
        self.context = ctx
        self.contents = contents
        self.embeds = embeds
        self.timeout = timeout
        self.use_extend = use_extend
        self.only = only
        self.basic_buttons = basic_buttons or ["⬅", "➡"]
        self.extended_buttons = extended_buttons or ["⏪", "⏩"]
        self.left_button_style: int = left_button_style
        self.right_button_style: int = right_button_style
        self.auto_delete = auto_delete
        self.page = 1
        self._left_button = self.basic_buttons[0]
        self._right_button = self.basic_buttons[1]
        self._left2_button = self.extended_buttons[0]
        self._right2_button = self.extended_buttons[1]
        self._message: Optional[discord_slash.model.SlashMessage] = None

        if not issubclass(type(bot),
                          (discord.Client, discord.AutoShardedClient, commands.Bot, commands.AutoShardedBot)):
            raise TypeError(
                "This is not a discord.py related bot class.(only <discord.Client, <discord.AutoShardedClient>, "
                "<discord.ext.commands.Bot>, <discord.ext.commands.AutoShardedBot>) "
            )

        if contents is None and embeds is None:
            raise MissingAttributeException("Both contents and embeds are None.")

        if not isinstance(timeout, int):
            raise TypeError("timeout must be int.")

        if len(self.basic_buttons) != 2:
            raise InvaildArgumentException(
                "There should be 2 elements in basic_buttons."
            )
        if extended_buttons is not None:
            if len(self.extended_buttons) != 2:
                raise InvaildArgumentException(
                    "There should be 2 elements in extended_buttons"
                )

        if left_button_style == ButtonStyle.URL or right_button_style == ButtonStyle.URL:
            raise TypeError(
                "Can't use <discord_component.ButtonStyle.URL> type for button style."
            )

    async def go_previous(self, ctx: ComponentContext) -> None:
        if self.page == 1:
            return
        self.page -= 1
        if self.contents is None:
            await ctx.edit_origin(embed=self.embeds[self.page - 1],
                                  components=(await self.make_buttons()))
            # await payload.respond(
            #     type=InteractionType.UpdateMessage,
            #     embed=self.embeds[self.page - 1],
            #     components=(await self.make_buttons()),
            # )
        else:
            await ctx.edit_origin(content=self.contents[self.page - 1],
                                  components=(await self.make_buttons()))
            # await payload.respond(
            #     type=InteractionType.UpdateMessage,
            #     content=self.contents[self.page - 1],
            #     components=(await self.make_buttons()),
            # )

    async def go_next(self, ctx: ComponentContext) -> None:
        if self.embeds is not None:
            if self.page != len(self.embeds):
                self.page += 1
                await ctx.edit_origin(embed=self.embeds[self.page - 1],
                                      components=(await self.make_buttons()))
                # await payload.respond(
                #     type=InteractionType.UpdateMessage,
                #     embed=self.embeds[self.page - 1],
                #     components=(await self.make_buttons()),
                # )
            elif self.contents is not None:
                if self.page != len(self.contents):
                    self.page += 1
                    await ctx.edit_origin(content=self.contents[self.page - 1],
                                          components=(await self.make_buttons()))
                    # await payload.respond(
                    #     type=InteractionType.UpdateMessage,
                    #     content=self.contents[self.page - 1],
                    #     components=(await self.make_buttons()),
                    # )

    async def go_first(self, ctx: ComponentContext) -> None:
        if self.page == 1:
            return
        self.page = 1

        if self.contents is None:
            await ctx.edit_origin(content=self.embeds[self.page - 1],
                                  components=(await self.make_buttons()))
            # await payload.respond(
            #     type=InteractionType.UpdateMessage,
            #     embed=self.embeds[self.page - 1],
            #     components=(await self.make_buttons()),
            # )
        else:
            await ctx.edit_origin(content=self.contents[self.page - 1],
                                  components=(await self.make_buttons()))
            # await payload.respond(
            #     type=InteractionType.UpdateMessage,
            #     content=self.contents[self.page - 1],
            #     components=(await self.make_buttons()),
            # )

    async def go_last(self, ctx: ComponentContext) -> None:
        if self.embeds is not None:
            if self.page != len(self.embeds):
                self.page = len(self.embeds)
                await ctx.edit_origin(content=self.contents[self.page - 1],
                                      components=(await self.make_buttons()))
                # await payload.respond(
                #     type=InteractionType.UpdateMessage,
                #     embed=self.embeds[self.page - 1],
                #     components=(await self.make_buttons()),
                # )
        elif self.contents is not None:
            if self.page != len(self.contents):
                self.page = len(self.contents)
                await ctx.edit_origin(content=self.contents[self.page - 1],
                                      components=(await self.make_buttons()))
                # await payload.respond(
                #     type=InteractionType.UpdateMessage,
                #     content=self.contents[self.page - 1],
                #     components=(await self.make_buttons()),
                # )

    def button_check(self, ctx: ComponentContext) -> bool:
        if ctx.author_id == self.bot.user.id:
            return False
        # if ctx.origin_message_id != self.context.message.id: # TODO
        #     return False
        print(str(self.only.__repr__()))
        if self.only is not None:
            if ctx.author_id != self.only.id:
                return False

        # if not self.component.id.endswith("_click"):
        #     return False
        return True

    async def start(self) -> None:
        if self.contents is None:
            self._message = await self.context.send(
                embed=self.embeds[self.page - 1],
                components=(await self.make_buttons()),
            )
        else:
            self._message = await self.context.send(
                content=self.contents[self.page - 1],
                components=(await self.make_buttons()),
            )
        while True:
            try:
                _task = asyncio.ensure_future(wait_for_component(self.bot, check=self.button_check,
                                                                 messages=self._message
                                                                 ))
                done, pending = await asyncio.wait(
                    [_task], return_when=asyncio.FIRST_COMPLETED, timeout=self.timeout
                )
                for i in pending:
                    i.cancel()

                if len(done) == 0:
                    raise asyncio.TimeoutError

                res = done.pop().result()
                await self.handle_paginaion(res)

            except asyncio.TimeoutError:
                pass

    async def handle_paginaion(self, ctx: ComponentContext):  # reworked to use slash custom_id
        if self.use_extend:
            if ctx.custom_id == "_extend_left_click":
                await self.go_first(ctx)
            elif ctx.custom_id == "_left_click":
                await self.go_previous(ctx)
                await self.context.send(self.only.id)
            elif ctx.custom_id == "_right_click":
                await self.go_next(ctx)
                await self.context.send(self.only.id)
            elif ctx.custom_id == "_extend_right_click":
                await self.go_last(ctx)
        else:
            if ctx.custom_id == "_left_click":
                await self.go_previous(ctx)
            elif ctx.custom_id == "_right_click":
                await self.go_next(ctx)

    async def disable_check(self) -> Tuple[bool, bool]:  # Looks good, sike, fails with content
        if self.page == 1 and (len(self.embeds or self.contents)) == 1:
            right_disable = True
            left_disable = True
        elif self.page == 1 and not (len(self.embeds or self.contents)) == 1:
            right_disable = False
            left_disable = True
        elif self.page == (len(self.embeds or self.contents)):
            right_disable = True
            left_disable = False
        else:
            right_disable = False
            left_disable = False

        return right_disable, left_disable

    async def make_buttons(self) -> list:  # Reworked
        """Creates the actionrows and buttons"""
        right_disable, left_disable = await self.disable_check()
        if self.use_extend:
            buttons = [create_actionrow(
                create_button(
                    style=self.left_button_style,
                    label=self._left2_button,
                    custom_id="_extend_left_click",
                    disabled=left_disable,
                ),
                create_button(
                    style=self.left_button_style,
                    label=self._left_button,
                    custom_id="_left_click",
                    disabled=left_disable,
                ),
                create_button(
                    style=ButtonStyle.gray,
                    label=f"Page {str(self.page)} / {str(len(self.embeds))}",
                    custom_id="_show_page",
                    disabled=True,
                ),
                create_button(
                    style=self.right_button_style,
                    label=self._right_button,
                    custom_id="_right_click",
                    disabled=right_disable,
                ),
                create_button(
                    style=self.right_button_style,
                    label=self._right2_button,
                    custom_id="_extend_right_click",
                    disabled=right_disable,
                ),
            )]
        else:
            buttons = [create_actionrow(
                create_button(
                    style=self.left_button_style,
                    label=self._left_button,
                    custom_id="_left_click",
                    disabled=left_disable,
                ),
                create_button(
                    style=ButtonStyle.gray,
                    label=f"Page {str(self.page)} / {str(len(self.embeds or self.contents))}",
                    custom_id="_show_page",
                    disabled=True,
                ),
                create_button(
                    style=self.right_button_style,
                    label=self._right_button,
                    custom_id="_right_click",
                    disabled=right_disable,
                ),
            )]

        return buttons
