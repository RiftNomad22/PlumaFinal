import nextcord
from nextcord.ext import commands

class MessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.awaiting_form = False
        self.tk = None
        self.name = None
        self.email = None
        self.issue = None
        self.date = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("!foll") and not self.awaiting_form:
            ch_ID = 1128601896257605632
            user = message.author
            dm = await user.create_dm()
            self.tk = "foll"
            if message.channel.id == ch_ID:
                content = message.content.split('-')
                self.name = content[1].strip()
                self.email = content[2].strip()
                self.issue = content[3].strip()
                self.date = content[4].strip()
                if len(content) == 5:
                    embed = nextcord.Embed(title='Follow-up request',
                                           description=f'Is this correct?\n'
                                                       f'\n{self.name} has a follow-up request from {self.email} regarding {self.issue} sent on {self.date}.',
                                           color=nextcord.Color.green())
                    msg = await dm.send(embed=embed)
                    await msg.add_reaction("✅")
                    await msg.add_reaction("❎")
                    self.awaiting_form = True  # Set awaiting_form to True to prevent multiple triggers
                else:
                    pass

    @commands.command()
    async def foll(self, ctx):
        pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.tk == "foll":
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
                                    dm = f"{self.name} has a follow-up request from {self.email} regarding {self.issue} sent on {self.date}"
                                    await member.send(dm)
                    else:
                        pass

def setup(bot):
    bot.add_cog(MessageCog(bot))
