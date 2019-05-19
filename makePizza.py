import random, datetime, PIL, os, io
from random import shuffle
from time import clock
from PIL import Image, ImageEnhance, ImageOps

extra = ["This pizza is then burnt to a crisp.",
"This pizza is then deepfried.",
"This pizza has been fitted with RGB lights.",
"This pizza is suitable for the whole family.",
"This pizza is gluten free.",
"This recipe has been passed through generations.",
"Best served with one of BartenderBot's drinks.",
"Best served cold.",
"Best served hot."
"Best served over ice.",
"Best before: {}.".format(datetime.date.fromordinal(random.randint(725000, 740000)))]
nothing = ['welcome to the void', "There's nothing for you.", 'Check out another pizza.']
andArr = ['and', 'finished off with', 'topped with', 'with some', 'with addition of']

def formatString(ingredients, halves, isDouble):
    s = ""
    x = 0
    for ingredient in ingredients:
        s1 = ''
        if isDouble[x]:
            s1 += 'double '
        if halves[x] != 'whole':
            s1 += halves[x] + ' '
        if random.random() > 0.9:
            s1 += 'vegan '
        if x == 0:
            s1 = s1.capitalize()
        if s == '' and s1 == '' and ingredient[0] > 'Z' and x == 0:
            s1 += ingredient.capitalize()
        else:
            s1 += ingredient

        if x < len(ingredients) - 2:
            s1 += ', '
        elif x == len(ingredients) - 2:
            s1 += ' ' + random.choice(andArr) + ' '
        else:
            s1 += '.'
        
        s += s1
        x += 1
    return s

def makePizza(loc, isDiscord):
    with open(os.path.join(loc, 'pizza.txt'), encoding='utf-8-sig') as f:
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

        if i == 0 and random.random() > 0.995 and not isDiscord:
            ingredientId = 'previous'
            ingredients.append('previous pizza, just a bit smaller')
            halves.append("whole")
            isDouble.append(False)
        else:
            shuffle(ingredientsIds)
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
        
    extraS = ""
    if random.random() > 0.85:
        randomChoice = random.randint(0, len(extra) - 1)
        if randomChoice == 0:
            print("Burning to a crisp...")
            #pizzaImage = burn(pizzaImage)
        elif randomChoice == 1:
            print("Deepfrying...")
            pizzaImage = deepfry(pizzaImage)
        elif randomChoice == 2:
            print("Fitting some sweet RGB lights...")
            pizzaImage = fitRGBLights(pizzaImage, loc)
        extraS = "\n" + extra[randomChoice]

    buffer = None
    if (not isDiscord):
        pizzaImage.save(os.path.join(loc, 'pizza2.png'))
    else:
        buffer = io.BytesIO()
        pizzaImage.save(buffer, 'png')

    return formatString(ingredients, halves, isDouble) + extraS, buffer

def addIngredient(loc, pizzaImage, ingredient, half, isDouble):
    if(ingredient != 'previous'):
        ingredientImg = Image.open(os.path.join(loc, 'ingredients', ingredient, str(ingredient + '_' + half + '.png')))
        pizzaImage = Image.alpha_composite(pizzaImage, ingredientImg)
        if (isDouble):
            ingredientImg = ingredientImg.rotate(random.randint(10, 15) * (1 if random.random() > 0.5 else -1))
            pizzaImage = Image.alpha_composite(pizzaImage, ingredientImg)
    else:
        ingredientImg = Image.open(os.path.join(loc, 'pizza2.png'))
        size = 1463, 954
        ingredientImg.thumbnail(size, Image.ANTIALIAS)
        toPaste = Image.new("RGBA", pizzaImage.size, (0, 0, 0, 0))
        toPaste.paste(ingredientImg, (85, 37), ingredientImg)
        pizzaImage = Image.alpha_composite(pizzaImage, toPaste)

    return pizzaImage
    
#TODO
def burn(pizzaImage):
    r, g, b, a = pizzaImage.split()
    pizzaImage = ImageEnhance.Brightness(pizzaImage).enhance(0.1)
    pizzaImage = ImageEnhance.Contrast(pizzaImage).enhance(8)
    return pizzaImage

def deepfry(pizzaImage):
    r, g, b, a = pizzaImage.split()
    pizzaImage = Image.merge('RGB', (r, g, b))
    pizzaImage = ImageOps.posterize(pizzaImage, 2)
    pizzaImage = ImageEnhance.Brightness(pizzaImage).enhance(1.2)
    pizzaImage = ImageEnhance.Contrast(pizzaImage).enhance(2)
    pizzaImage = ImageEnhance.Color(pizzaImage).enhance(2)
    pizzaImage = ImageEnhance.Sharpness(pizzaImage).enhance(100)
    r, g, b = pizzaImage.split()
    pizzaImage = Image.merge('RGBA', (r, g, b, a))
    return pizzaImage

def fitRGBLights(pizzaImage, loc):
    rgbLights = Image.open(os.path.join(loc, 'rgb.png'))
    pizzaImage = Image.alpha_composite(rgbLights, pizzaImage)
    return pizzaImage