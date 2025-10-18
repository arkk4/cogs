import discord
from redbot.core import commands, app_commands
from faker import Faker
from faker_stalker_names.uk_UA import Provider as StalkerNamesProvider


fake = Faker()
fake.add_provider(StalkerNamesProvider)

class Stalkify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def generate_stalker_name(self, name_type, fraction):
        if name_type == 'first':
            name = fake.stalker_first_name(name_type=fraction)
        elif name_type == 'last':
            name = fake.stalker_last_name(name_type=fraction)
        else:
            name = fake.stalker_name(name_type=fraction)

        return name

    async def execute_stalkify(self, ctx, name_type:str, fraction:str):
        new_name = await self.generate_stalker_name(name_type,fraction)
        user_roles = [role.name for role in ctx.user.roles]
        if name_type == 'with_append':
            if user_roles:
                name_type = 'full'
                new_name = await self.generate_stalker_name(name_type,fraction)
                latest_role = user_roles[-1]
                new_name = f"{latest_role} {new_name}"
        if name_type == 'last':
            if user_roles:
                latest_role = user_roles[-1]
                new_name = f"{latest_role} {new_name}"
        try:
            await ctx.user.edit(nick=new_name)
            await ctx.response.send_message(f'Твоє сталкерське поганяло: {new_name}')
        except discord.HTTPException as e:
            error_message = e.text
            error_code = e.code
            print(f"Error {error_code}: {error_message}")
            await ctx.response.send_message(f"Виникла помилка: {error_code} - {error_message}")

    @app_commands.command()
    @app_commands.describe(
        name_type='Тип генерації (повне, кличка, лише ім\'я)',
        fraction='Фракція (сталкер або бандит)',
    )
    @app_commands.choices(
        name_type=[
            discord.app_commands.Choice(name='Повне ім\'я', value='full'),
            discord.app_commands.Choice(name='Кличка', value='last'),
            discord.app_commands.Choice(name='Ім\'я', value='first'),
            discord.app_commands.Choice(name='Повне + твоя роль', value='with_append')
        ],
        fraction=[
            discord.app_commands.Choice(name='Сталкер', value='stalker'),
            discord.app_commands.Choice(name='Бандит', value='bandit')
        ]
    )
    async def stalkify(self, ctx, name_type: str, fraction: str):
        await self.execute_stalkify(ctx, name_type, fraction)

    @app_commands.command()
    @app_commands.describe(
        name_type='Тип генерації (повне, кличка, лише ім\'я)',
        fraction='Фракція (сталкер або бандит)'
    )
    @app_commands.choices(
        name_type=[
            discord.app_commands.Choice(name='Повне ім\'я', value='full'),
            discord.app_commands.Choice(name='Ім\'я', value='first'),
            discord.app_commands.Choice(name='Кличка', value='last')
        ],
        fraction=[
            discord.app_commands.Choice(name='Сталкер', value='stalker'),
            discord.app_commands.Choice(name='Бандит', value='bandit')
        ]
    )
    async def generate(self, ctx, name_type: str, fraction: str):
        new_name = await self.generate_stalker_name(name_type, fraction)
        await ctx.response.send_message(f'Згенероване ім\'я: {new_name}')

def setup(bot):
    bot.add_cog(Stalkify(bot))
