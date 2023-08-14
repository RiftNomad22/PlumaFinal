import nextcord
from nextcord.ext import commands

class AccessCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.awaiting_form = False
        self.tk = None
        self.name = None
        self.uname = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("!access") and not self.awaiting_form:
            ch_ID = 1128601896257605632
            user = message.author
            dm = await user.create_dm()
            self.tk = "access"
            if message.channel.id == ch_ID:
                content = message.content.split('-')
                self.name = content[1].strip()
                self.uname = content[2].strip()
                if len(content) == 3:
                    embed = nextcord.Embed(title='Access request',
                                           description=f'Is this correct?\n'
                                                       f'\n{self.name} requests resetting {self.uname} account password.',
                                           color=nextcord.Color.green())
                    msg = await dm.send(embed=embed)
                    await msg.add_reaction("✅")
                    await msg.add_reaction("❎")
                    self.awaiting_form = True  # Set awaiting_form to True to prevent multiple triggers
                else:
                    pass

    @commands.command()
    async def access(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.tk == "access":
            if reaction.emoji == "✅" and user != self.bot.user:
                if reaction.message.embeds:
                    embed = reaction.message.embeds[0]
                    embed.description = "This request has been approved. Now sending to everyone concerned."
                    await reaction.message.edit(embed=embed)
                    server = self.bot.get_guild(1125364377080569927)  # Access bot instance using self.bot
                    if server is not None:
                        admin_roles = ["Admin"]  # Make admin_roles a list
                        for member in server.members:
                            for role in member.roles:
                                if role.name in admin_roles:
                                    dm = f"{self.name} requests resetting {self.uname} account password."
                                    await member.send(dm)
                    else:
                        pass

def setup(bot):
    bot.add_cog(AccessCog(bot))
