import random, datetime, PIL, os, io
from time import clock
from PIL import Image

extra = ["This recipe has been passed through generations.", "Best served with one of BartenderBot's drinks.", "Best served cold.", "This pizza is then burnt to a crisp.", "This pizza is then deep fried.", "Best served over ice.", "Best before: {}.".format(datetime.date.fromordinal(random.randint(720000, 780000))), "Best seved hot."]
nothing = ['welcome to the void', "There's nothing for you.", 'Check out another pizza.']
andArr = ['and', 'finished off with', 'topped with', 'with some', 'with addition of']

def formatString(ingredients, halves, isDouble):
    s = ""
    x = 0
    for ingredient in ingredients:
        if isDouble[x]:
            s += 'double '
        if halves[x] != 'whole':
            s += halves[x] + ' '
        if x == 0:
            s = s.capitalize()

        if ingredient[0] > 'Z' and s == '' and x == 0:
            s += ingredient.capitalize()
        else:
            s += ingredient

        if x < len(ingredients) - 2:
            s += ', '
        elif x == len(ingredients) - 2:
            s += ' ' + random.choice(andArr) + ' '
        else:
            s += '.'
        
        x += 1
    return s

def makePizza(loc, isDiscord):
    with open(os.path.join(loc, 'pizza.txt'), encoding='utf-8') as f:
        textFile = f.read()
    lines = textFile.splitlines()
    ingredientsDict = {}

    for line in lines:
        split = line.split(" ", 1)
        ingredientsDict[split[0]] = split[1]
    
    ingredientsAmmout = random.randint(1, 5)
    ingredientsIds = list(ingredientsDict)
    ingredients = []
    halves = []
    isDouble = []
    pizzaImage = Image.open(os.path.join(loc, 'pizza.png'))

    for i in range(ingredientsAmmout):

        if i == 0 and random.random() > 0.99 and not isDiscord:
            ingredientId = 'previous'
            ingredients.append('previous pizza, just a bit smaller')
            halves.append("whole")
            isDouble.append(False)
        else:
            ingredientId = random.choice(ingredientsIds)
            ingredients.append(ingredientsDict[ingredientId])
            ingredientsDict.pop(ingredientId)
            ingredientsIds.pop(ingredientsIds.index(ingredientId))

            halvesValue = random.random()
            doubleValue = random.random()
            if halvesValue < 0.6:
                halves.append("whole")
            elif halvesValue < 0.8:
                halves.append("right")
            else:
                halves.append("left")

            if doubleValue < 0.85:
                isDouble.append(False)
            else:
                isDouble.append(True)
        
        pizzaImage = addIngredient(loc, pizzaImage, ingredientId, halves[i], isDouble[i])
        
    if (not isDiscord):
        pizzaImage.save(os.path.join(loc, 'pizza2.png'))
    else:
        buffer = io.BytesIO()
        pizzaImage.save(buffer, 'png')

    extraS = ""
    if random.random() > 0.9:
        extraS = random.choice(extra)
    return formatString(ingredients, halves, isDouble) + " " + extraS, buffer

def addIngredient(loc, pizzaImage, ingredient, half, isDouble):
    if(ingredient != 'previous'):
        ingredientImg = Image.open(os.path.join(loc, 'ingredients', ingredient, str(ingredient + '_' + half + '.png')))
        pizzaImage = Image.alpha_composite(pizzaImage, ingredientImg)
        if (isDouble):
            ingredientImg = ingredientImg.rotate(random.randint(10, 15))
            pizzaImage = Image.alpha_composite(pizzaImage, ingredientImg)
    else:
        ingredientImg = Image.open(os.path.join(loc, 'pizza2.png'))
        size = 1463, 954
        ingredientImg.thumbnail(size, Image.ANTIALIAS)
        toPaste = Image.new("RGBA", pizzaImage.size, (0, 0, 0, 0))
        toPaste.paste(ingredientImg, (85, 37), ingredientImg)
        pizzaImage = Image.alpha_composite(pizzaImage, toPaste)

    return pizzaImage
