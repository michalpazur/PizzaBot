import random, datetime, PIL, os
from time import clock
from PIL import Image

extra = ["Best served cold.", "This pizza is then burned to a crisp.", "This pizza is then deep fried.", "Best served over ice.", "Best before: {}.".format(datetime.date.fromordinal(random.randint(720000, 780000))), "Best seved hot."]
nothing = ['welcome to the void', "There's nothing for you.", 'Check out another pizza.']
andArr = ['and', 'finished off with', 'topped with', 'with some']

def formatString(ingredients, halves, isDouble):
    s = ""
    x = 0
    for ingredient in ingredients:
        if len(ingredients) > 1:
            if x != len(ingredients) - 1:
                if isDouble[x]:
                    s += 'double '
                if halves[x] != 'whole':
                    s += halves[x] + ' '
                s += ingredient + ', ' 
            else:
                s = s.rstrip(', ')
                s += ' ' + random.choice(andArr) + ' '
                if isDouble[x]:
                    s += 'double '
                if halves[x] != 'whole':
                    s += halves[x] + ' '
                s += ingredient + '.'
            
            x += 1

        elif len(ingredients) == 1:
            if isDouble[x]:
                    s += 'double '
            if halves[x] != 'whole':
                s += halves[x] + ' ' 
            s += ingredient + '.'
        else:
            s += random.choice(nothing)
            #not possible for now
    s = s.replace('  ', ' ').capitalize()
    print(s)
    return s

def makePizza(loc):
    with open(os.path.join(loc, 'pizza.txt')) as f:
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

        if doubleValue < 0.8:
            isDouble.append(False)
        else:
            isDouble.append(True)
        
        pizzaImage = addIngredient(loc, pizzaImage, ingredientId, halves[i], isDouble[i])
        
    pizzaImage.save(os.path.join(loc, 'pizza2.png'))
    extraS = ""
    if random.random() > 0.8:
        extraS = random.choice(extra)
    returnString = formatString(ingredients, halves, isDouble) + " " + extraS
    print(returnString)
    return returnString

def addIngredient(loc, pizzaImage, ingredient, half, isDouble):
    ingredientImg = Image.open(os.path.join(loc, 'ingredients', ingredient, str(ingredient + '_' + half + '.png')))
    pizzaImage = Image.alpha_composite(pizzaImage, ingredientImg)
    if (isDouble):
        ingredientImg = ingredientImg.rotate(random.randint(10, 15))
        pizzaImage = Image.alpha_composite(pizzaImage, ingredientImg)
    return pizzaImage