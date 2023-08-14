import nextcord
import sqlite3
from nextcord.ext import commands

# global vars
FName = None
MName = None
LName = None
empID = None
empSex = None
empCont = None
empEmail = None
empSub = None
empFnd = None
empSch = None
empStat = None
schExt = None
empDes = None
empPos = None
empDeg = None
empSub = None
fr = None
to = None
min = None
days = None
empCourse = None
empMaj = None
schName = None
ext = None
schAdd = None
schDist = None
schMail = None
tick = None


# main class
class Verify(commands.Cog):
    def __init__(self, bot):
        self.awaiting_form = None
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        global empID, FName, MName, LName, empCont, empEmail, empSex, empDes, empPos,empStat, empDeg, empCourse, empMaj, tick, empSch, schID, schName, schExt, schAdd, schMail, schDist, chFnd, empSub, days, fr, to

        if message.content == '!verify' and not self.awaiting_form:
            tick = "verify"  # Set the tick here if needed in other parts of the code
            ch_ID = 1128601896257605632
            if message.channel.id == ch_ID:
                user = message.author
                dm_channel = await user.create_dm()
                verified_role = nextcord.utils.get(user.roles, name="VERIFIED")
                # check if user is verified
                if verified_role:
                    await dm_channel.send("You are already verified!")
                    return
                else:
                    # if user is not verified
                    user = message.author
                    dm_channel = await user.create_dm()
                    flag = False
                    while flag != True:
                        await dm_channel.send('Please enter your Employee ID:')
                        emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                        empID = emp.content
                        char_count = len(empID)
                        if char_count == 7 and emp.content.isdigit():
                            flag = True
                        else:
                            await dm_channel.send('Invalid Employees ID. Please try again.')
                            pass

                user = message.author
                dm_channel = await user.create_dm()
                # Employee Name
                await dm_channel.send('Please enter your first name:')
                emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                FName = emp.content

                await dm_channel.send('Please enter your middle name:')
                emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                MName = emp.content

                await dm_channel.send('Please enter your last name:')
                emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                LName = emp.content
                # employee gender
                flag = False
                while flag != True:
                    await dm_channel.send('Please enter your gender: [M or F]')
                    emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                    empSex = emp.content
                    char_count = len(empSex)
                    if char_count == 1 and empSex == "M" or empSex == "F":
                        flag = True
                    else:
                        await dm_channel.send('Invalid reply. Please enter your gender.')
                        pass
                # employee contact number
                flag = False
                while flag != True:
                    await dm_channel.send('Please enter your contact number:')
                    sch_id_msg = await self.bot.wait_for('message', check=lambda m: m.author == user)
                    empCont = sch_id_msg.content
                    char_count = len(empCont)
                    if char_count == 11 and sch_id_msg.content.isdigit():
                        flag = True
                    else:
                        await dm_channel.send('Invalid contact number. Please try again.')
                        flag = False
                        pass
                # employee email
                flag = False
                while flag != True:
                    await dm_channel.send('Please enter your DepEd email:')
                    emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                    empEmail = emp.content
                    if "@deped.gov.ph" in empEmail:
                        flag = True
                    else:
                        await dm_channel.send('Invalid email. Please try again.')
                        flag = False
                        pass
                connection = sqlite3.connect('masterlist.db')
                cursor = connection.cursor()
                await dm_channel.send('What degree have you attained?')
                cursor.execute("SELECT * from degree")
                results = cursor.fetchall()
                formatted_results = '\n'.join([f"{row[0]} ---- \"{row[1]}\"" for row in results])

                embed = nextcord.Embed(title="Degree",
                                       description=formatted_results,
                                       color=nextcord.Color.random())
                await dm_channel.send(embed=embed)
                emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                empDeg = emp.content
                cursor.execute(f"SELECT degName from degree WHERE degID = {empDeg}")
                results = cursor.fetchone()
                print(f'{results}')
                cursor.close()
                empDeg = results[0]
                empDeg = empDeg.strip("()'")

                embed = nextcord.Embed(title="Choose Course",
                                       description=f'Is your course a degree in art or in science?\n'
                                                   f'\n [1 or 2]'
                                                   f'\n'
                                                   f'1 ---- Science\n'
                                                   f'2 ---- Art',
                                       color=nextcord.Color.random())
                await dm_channel.send(embed=embed)
                emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                flag = emp.content
                connection = sqlite3.connect('masterlist.db')
                cursor = connection.cursor()
                if flag == "1":
                    empCourse = "Science"
                    await dm_channel.send('Please enter the ID that corresponds to your Specialization:')
                    cursor.execute("SELECT courseID, courseName from course WHERE courseID LIKE '1%'")
                    results = cursor.fetchall()
                    formatted_results = '\n'.join([f"{row[0]} ---- \"{row[1]}\"" for row in results])
                    formatted_results += "\n0 ---- \"Others\""

                    embed = nextcord.Embed(title="Course IDs",
                                           description=formatted_results,
                                           color=nextcord.Color.random())
                    await dm_channel.send(embed=embed)
                    emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                    empMaj = emp.content

                elif flag == "2":
                    empCourse = "Art"
                    await dm_channel.send('Please enter the ID that corresponds to your course:')
                    cursor.execute("SELECT courseID, courseName from course WHERE courseID LIKE '2%'")
                    results = cursor.fetchall()
                    formatted_results = '\n'.join([f"{row[0]} ---- \"{row[1]}\"" for row in results])

                    embed = nextcord.Embed(title="Course IDs",
                                           description=formatted_results,
                                           color=nextcord.Color.random())
                    await dm_channel.send(embed=embed)
                    emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                    empMaj = emp.content

                    cursor.execute(f"SELECT courseName from course WHERE courseID = {empMaj}")
                    results = cursor.fetchone()
                    print(f'{results}')
                    cursor.close()
                    connection.close()
                    empMaj = results[0]
                    empMaj = empMaj.strip("()'")

                flag = True
                while flag:
                    await dm_channel.send('Please enter your school ID:')
                    emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                    empSch = emp.content
                    char_count = len(empSch)
                    if char_count == 6 and empSch.isdigit():
                        flag = False
                    else:
                        await dm_channel.send('Invalid response. Please enter your School ID.')
                        pass
                connection = sqlite3.connect('masterlist.db')
                cursor = connection.cursor()
                cursor.execute("SELECT schName FROM school WHERE schoolID = ?", (empSch,))
                result = cursor.fetchone()

                if result is None:
                        await dm_channel.send('There is no record about this school. Please help me record '
                                              'this providing more data.')
                        await dm_channel.send('Please enter School Name:')
                        emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                        schName = emp.content

                        await dm_channel.send('Please enter School Address:')
                        emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                        schAdd = emp.content

                        await dm_channel.send('Please enter School Email:')
                        emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                        schMail = emp.content

                        await dm_channel.send('Please enter your district:')
                        emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                        schDist = emp.content

                        flag = True
                        while flag:
                            await dm_channel.send('Is your school an extension? [Y or N]')
                            emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                            schExt = emp.content
                            char_count = len(schExt)
                            if char_count == 1 and (schExt == "Y" or schExt == "N"):
                                flag = False
                            else:
                                await dm_channel.send('Invalid response. Please only enter Y or N.')
                                pass
                                embed = nextcord.Embed(title="Checking of data",
                                                       description=f'Please check if the data provided is correct?\n'
                                                                   f'\n'
                                                                   f'\n'
                                                                   f'School ID: {empSch}\n'
                                                                   f'School Name: {schName}\n'
                                                                   f'Is Extention: {schExt}\n'
                                                                   f'School Address: {schAdd}\n'
                                                                   f'District: {schDist}\n'
                                                                   f'School Email: {schMail}',
                                                       color=nextcord.Color.random())
                                await dm_channel.send(embed=embed)
                                await dm_channel.send('Is the information provided correct? [Y or N]')
                                emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                                flg = emp.content
                                if flg == "Y":
                                    cursor.execute(
                                        "INSERT INTO school (schoolID, schName, extension, email, address, region, "
                                        "division, district) VALUES (?, ?, ?, ?, ?, 'XII', 'South Cotabato', ?)",
                                        (empSch, schName, schExt, schMail, schAdd, schDist))
                                    connection.commit()
                                    cursor.close()
                                    await dm_channel.send('This data is now stored in our data base.')
                                elif flg == "N":
                                    await dm_channel.send('You have cancelled this transaction. If you want to start again please use the token again.')
                else:
                    connection = sqlite3.connect('masterlist.db')
                    cursor = connection.cursor()
                    cursor.execute(f"SELECT schName, district from school WHERE schoolID = {empSch}")
                    results = cursor.fetchone()
                    print(f'{results}')
                    cursor.close()
                    connection.close()
                    schName = results[0]
                    schName = schName.strip("()'")
                    schDist = results [1]
                    schDist = schDist.strip("()'")

                flag = False
                while flag != True:
                    await dm_channel.send('Are you a Non- Teaching Employee?[Y or N]')
                    emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                    empDes = emp.content
                    char_count = len(empDes)
                    if char_count == 1 and empDes == "Y" or empDes == "N":
                        flag = True
                    else:
                        await dm_channel.send('Invalid response. Please enter Y or N.')
                        pass

                await dm_channel.send('Please enter your full position: [ex: Administrative Officer II, '
                                      'Master Teacher I]')
                emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                empPos = emp.content

                await dm_channel.send('Please enter your nature of appointment: [Permanent or etc.]')
                emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                empStat = emp.content

                if empDes == "N":
                    more = True
                    while flag:
                        connection = sqlite3.connect('masterlist.db')
                        cursor = connection.cursor()
                        await dm_channel.send('Please enter subject your are teaching:')
                        cursor.execute("SELECT * from subject")
                        results = cursor.fetchall()
                        formatted_results = '\n'.join([f"{row[0]} ---- \"{row[1]}\"" for row in results])

                        embed = nextcord.Embed(title="Subjects",
                                               description=formatted_results,
                                               color=nextcord.Color.random())
                        await dm_channel.send(embed=embed)
                        emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                        empSub = emp.content

                        await dm_channel.send('Please enter days: (M, T, W, TH, or F. If multiple, separate with comma)')
                        emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                        days = emp.content

                        await dm_channel.send('Please enter starting time of this subject:')
                        emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                        fr = emp.content

                        await dm_channel.send('Please enter ending time of this subject:')
                        emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                        to = emp.content

                        await dm_channel.send('Please enter total minutes of the subject:')
                        emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                        min = emp.content

                        await dm_channel.send('Are you teaching more subjects? [Y or N]')
                        emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                        if emp.content == "N":
                            more = False
                            connection = sqlite3.connect('masterlist.db')
                            cursor = connection.cursor()
                            cursor.execute(
                                "INSERT INTO tch_subj (EmpID, SubID, Day, From, To, Min), VALUES (?, ?, ?, ?, ?, ?)",
                                (empID, empSub, days, fr, to, min))
                            connection.commit()
                            cursor.close()
                        else:
                            connection = sqlite3.connect('masterlist.db')
                            cursor = connection.cursor()
                            cursor.execute(
                                "INSERT INTO tch_subj (EmpID, SubID, Day, From, To, Min), VALUES (?, ?, ?, ?, ?, ?)",
                                (empID, empSub, days, fr, to, min))
                            connection.commit()
                            cursor.close()
                            pass
                connection = sqlite3.connect('masterlist.db')
                cursor = connection.cursor()
                await dm_channel.send('Please enter your fund source:')
                cursor.execute("SELECT * from fund")
                results = cursor.fetchall()
                formatted_results = '\n'.join([f"{row[0]} ---- \"{row[1]}\"" for row in results])

                embed = nextcord.Embed(title="Fund Source",
                                       description=formatted_results,
                                       color=nextcord.Color.random())
                await dm_channel.send(embed=embed)
                emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                empFnd = emp.content
                cursor.execute(f"SELECT fundsrc from fund WHERE fundID = {empFnd}")
                results = cursor.fetchone()
                empFnd = results[0]
                empFnd = empFnd.strip("()'")

                embed = nextcord.Embed(title="Checking of data",
                                       description=f'Please check if the data provided is correct, before we store it in our database.\n'
                                                   f'\n'
                                                   f'\n'
                                                   f'Employee ID: {empID}\n'
                                                   f'Employee Name: {LName}, {FName} {MName}\n'
                                                   f'Gender: {empSex}\n'
                                                   f'School Deployed (ID): {empSch}\n'
                                                   f'Employee Contact No.: {empCont}\n'
                                                   f'Employee DepEd Email: {empEmail}'
                                                   f'\n'
                                                   f'\n Employment Status: {empStat}\n'
                                                   f'Non- Teaching: {empDes}\n'
                                                   f'Position: {empPos}\n'
                                                   f'Fund Source: {empFnd}'
                                                   f'\n'
                                                   f'\n Attained Degree: {empDeg}\n'
                                                   f'\n Course Taken (ID and Desc.): {empCourse}\n'
                                                   f'\n Majorship (If Any): {empMaj}\n'
                                                   f'I can not show you subjects that you entered recently. But using !search prompt, you can.',
                                       color=nextcord.Color.random())
                await dm_channel.send(embed=embed)

                await dm_channel.send('Is the information provided correct? [Y or N]')
                emp = await self.bot.wait_for('message', check=lambda m: m.author == user)
                flg = emp.content
                if flg == "Y":
                    cursor.execute("INSERT INTO teachers (EmpID, Fname, Mname, Lname, Sex, ContNo, Email, FndSrc, Pos, NatApp, Degree, "
                        "Major, SchID, SchName, Reg, Dist) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'XII', ?)",
                        (empID, FName, MName, LName, empSex, empCont, empEmail, empFnd, empPos, empStat, empDeg, empMaj,
                        empSch, schName, schDist))
                    connection.commit()
                    cursor.close()
                    await dm_channel.send('This data is now stored in our data base.')
                elif flg == "N":
                    await dm_channel.send('You have cancelled this transaction. If you want to start again '
                                          'please use the token again.')

                    # Assign the role to the user
                role_id = 1139372299196317777  # Replace with the actual role ID
                role = message.guild.get_role(role_id)
                if role:
                    await user.add_roles(role)
                    await dm_channel.send(f"You've been assigned the role: {role.name}")


    @commands.command()
    async def verify(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Verify(bot))