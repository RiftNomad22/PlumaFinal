import nextcord
from nextcord.ext import commands


class DocRequest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.awaiting_form = False
        self.sch_name = None
        self.sch_ID = None
        self.learner = None
        self.lrn = None
        self.issue = None
        self.originID = None
        self.origin = None
        self.tk = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == '!docs' and not self.awaiting_form:
            self.tk = "docs"
            ch_ID = 1128601896257605632
            if message.channel.id == ch_ID:
                user = message.author
                dm_channel = await user.create_dm()
                await dm_channel.send('I heard read that you need assistance with something. \n Please fill-out this form for me to help you.')

                await dm_channel.send(' Please enter your school:')
                name_msg = await self.bot.wait_for('message', check=lambda m: m.author == user)
                self.sch_name = name_msg.content

                flag = False
                while flag != True:
                    await dm_channel.send(' Please enter your School ID :')
                    sch_id_msg = await self.bot.wait_for('message', check=lambda m: m.author == user)
                    self.sch_ID = sch_id_msg.content
                    char_count = len(self.sch_ID)
                    if char_count == 6 and sch_id_msg.content.isdigit():
                        flag = True
                    else:
                        await  dm_channel.send(' Invalid School ID. Please try again.')
                        flag = False
                        pass

                await dm_channel.send(' Please enter the name of the learner:')
                issue_msg = await self.bot.wait_for('message', check=lambda m: m.author == user)
                self.learner = issue_msg.content

                flag = False
                while flag != True:
                    await dm_channel.send(' Please enter the name of the learners LRN:')
                    issue_msg = await self.bot.wait_for('message', check=lambda m: m.author == user)
                    self.lrn = issue_msg.content
                    char_count = len(self.lrn)
                    if char_count == 12 and issue_msg.content.isdigit():

                        flag = True
                    else:
                        await dm_channel.send(' Please re-enter the name of the learners LRN:')
                        flag = False
                        pass

                flag = False
                while flag != True:
                    await dm_channel.send(' Please enter the School ID of the concerning school:')
                    sch_id_msg = await self.bot.wait_for('message', check=lambda m: m.author == user)
                    self.originID = sch_id_msg.content
                    char_count = len(self.originID)
                    if char_count == 6 and sch_id_msg.content.isdigit():
                        flag = True
                    else:
                        await  dm_channel.send(' Invalid School ID. Please try again.')
                        flag = False
                        pass

                await dm_channel.send('Please enter the school of the concerning school:')
                origin_msg = await self.bot.wait_for('message', check=lambda m: m.author == user)
                self.origin = origin_msg.content

                embed = nextcord.Embed(title='Checking of info',
                                       description=f"Lets double check the request you are asking."
                                                   f"\n"
                                                   f"\n"
                                                   f"CALLING THE ATTENTION OF: \n"
                                                   f"School: {self.sch_name}\n"
                                                   f"School ID: {self.sch_ID}\n"
                                                   f"Division: South Cotabato\n"
                                                   f"Region: XII\n"
                                                   f"Learner's name: {self.learner}\n"
                                                   f"LRN: {self.lrn}\n"
                                                   f"Issue/Concern: {self.issue}\n"
                                                   f"\n"
                                                   f"Receiving School: {self.origin}\n"
                                                   f"School ID: {self.originID}\n"
                                                   f"Division: South Cotabato\n"
                                                   f"Region:XII\n",
                                       color=nextcord.Color.green())
                embed.description += "\nDone = ✅"
                embed.description += "\nDeclined = ❎"
                msg = await dm_channel.send(embed=embed)
                await msg.add_reaction("✅")
                await msg.add_reaction("❎")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.tk == "docs":
            if reaction.emoji == "✅" and user != self.bot.user:
                if reaction.message.embeds:
                    embed = reaction.message.embeds[0]
                    embed.description = "This request has been approved. Now sending to everyone concerned."
                    await reaction.message.edit(embed=embed)
                    channel_id = 1128889131951460363
                    channel = self.bot.get_channel(channel_id)
                    embed = nextcord.Embed(title='An issue has to be resolved!',
                                           description=f"CALLING THE ATTENTION OF: \n"
                                                       f"School: {self.origin}\n"
                                                       f"School ID: {self.originID}\n"
                                                       f"Division: South Cotabato \n"
                                                       f"Region: XII\n"
                                                       f"Learner's name: {self.learner}\n"
                                                       f"LRN: {self.lrn}\n"
                                                       f"Issue/Concern: {self.issue}\n"
                                                       f"\n"
                                                       f"Receiving School: {self.origin}\n"
                                                       f"School ID: {self.originID}\n"
                                                       f"Division: South Cotabato\n"
                                                       f"Region:XII\n",
                                           color=nextcord.Color.green())
                    await channel.send(embed=embed)
            elif reaction.emoji == "❎" and user != self.bot.user:
                if reaction.message.embeds:
                    embed = reaction.message.embeds[0]
                    embed.description = "This request has been declined.\nYou can request again or contact the Admin for further details."
                    await reaction.message.reply(embed=embed)
        else:
            pass

    @commands.command()
    async def docs(self, ctx):
        pass

def setup(bot):
    bot.add_cog(DocRequest(bot))
