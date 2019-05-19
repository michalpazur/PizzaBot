import discord, makePizza, random, os, datetime
from discord.ext import commands

bot = commands.Bot(command_prefix='*')
token = '<DISCORD_TOKEN>'
loc = '<YOUR_PROJECT_LOCATION>'

@bot.listen()
async def on_ready():
    print('---PizzaBot is now online---' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '---')
    game = discord.Game('*pizzahelp')
    await bot.change_presence(status = discord.Status.online, activity = game)

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    if 'pizza' in message.content.lower().split():
        await message.add_reaction('🍕')
    if 'pizza time' in message.content.lower():
        await message.channel.send("```It's pizza time! 🍕```")

@bot.command()
async def pizza(ctx):
    await ctx.trigger_typing()
    pizza = makePizza.makePizza(loc, True)
    print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print(pizza[0])
    pizza[1].seek(0)
    await ctx.send(pizza[0], file = discord.File(pizza[1], 'pizza.png'))

@bot.command()
async def pizzasubmit(ctx, *ingredients):
    if len(ingredients) == 0:
        await ctx.trigger_typing()
        await ctx.send('Try typing something 🤔')
        return
    with open(os.path.join(loc, 'list.txt'), encoding = 'utf-8') as file:
        ingredientsList = file.read().splitlines()
    ingredientsList[0] = ingredientsList[0].capitalize()
    ingredient = ' '.join(ingredients).lower()
    for x in range(len(ingredientsList)):
        ingredientsList[x] = ingredientsList[x].lower()
        
    if (ingredient in ingredientsList):
        await ctx.trigger_typing()
        await ctx.send(ingredient + ' has already been submited :(')
    else:
        await ctx.trigger_typing()
        await ctx.send(str(ingredient + ' has been submited, thanks!').capitalize())
        with open(os.path.join(loc, 'list.txt'), 'a', encoding = 'utf-8') as file:
            file.write(ingredient + '\n')

@bot.command()
async def pizzahelp(ctx):
    await ctx.trigger_typing()
    embed = discord.Embed(title = "PizzaBot Help", description = "Use the '*' prefix to access PizzaBot's commands.", color = 0x95d6ff)
    embed.add_field(name = 'pizza', value = 'Generates a yummy pizza 😋', inline = False)
    embed.add_field(name = 'pizzasubmit', value = 'Help to create PizzaBot by submitting your own toppings.', inline = False)
    embed.add_field(name = 'pizzahelp', value = 'Displays this message.', inline = False)
    embed.add_field(name = 'About PizzaBot:', value = 'Facebook: https://www.facebook.com/pizzabot55/' + '\nTotal ingredients: 81.\nLast update: 2019-05-18.\nCreated by @kolorowytoster#8336, local time: {} (UTC +2).\nSource code available on GitHub: https://github.com/kolorowytoster/PizzaBot'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '\nAdd me to your server: https://bit.ly/2w9n6e0', inline = False)
    await ctx.send(embed = embed)

bot.run(token)