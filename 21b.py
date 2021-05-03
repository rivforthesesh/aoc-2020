# allergens
# each ingredient has at most one allergen
# each allergen is present in exactly one ingredient

# input
with open('21.txt', 'r') as file:
    input = file.read()

# turn the input into a list
input_list = list(input.split('\n'))

# get list of line infos
line_infos = []
# and *unique* ingredients and allergens
ingredients = set([])
allergens = set([])

# fill in line_infos with dicts with two keys:
    # ingredients has a set of ingredients
    # allergens has a set of allergens
while len(input_list) > 0:
    line_info = {}
    line = input_list.pop(0)
    # 'zjgxg nsvfk jpvfc qtc (contains soy, sesame)'
    tmp = line.replace(')','').split(' (contains ')
    # ['zjgxg nsvfk jpvfc qtc', 'soy, sesame']
    line_info['ingredients'] = tmp[0].split(' ')
    # ['zjgxg', 'nsvfk', 'jpvfc', 'qtc']
    line_info['allergens'] = tmp[1].split(', ')
    # ['soy', 'sesame']
    line_infos.append(line_info)
    # now add on any new ingredients/allergens
    ingredients = ingredients.union(set(line_info['ingredients']))
    allergens = allergens.union(set(line_info['allergens']))

# union - for each allergen, we want a list of ingredients that are ALWAYS present
#           in a list where this allergen is present
allergen_dict = {}
for allergen in allergens:
    allergen_dict[allergen] = set(ingredients)
    # go through each line
    for line_info in line_infos:
        # if this allergen is in this list
        if allergen in line_info['allergens']:
            # add in any new ingredients
            allergen_dict[allergen] = allergen_dict[allergen].intersection(line_info['ingredients'])

# intersection - for each ingredient, we want a list of allergens that are ALWAYS present
#                   in a list where this ingredient is present
ingredient_dict = {}
for ingredient in ingredients:
    ingredient_dict[ingredient] = set(allergens)
    # go through each line
    for line_info in line_infos:
        # if this allergen is in this list
        if ingredient in line_info['ingredients']:
            # take intersection
            ingredient_dict[ingredient] = ingredient_dict[ingredient].intersection(line_info['allergens'])

# time to match
ia_pairs = [] # (ingredient, allergen)
while len(ia_pairs) < len(allergens):
    # go through each allergen
    for a in allergens:
        # if it has not been paired
        if not a in [ia[1] for ia in ia_pairs]:
            # see if this allergen has only one ingredient
            a_ingredients = allergen_dict[a]
            if len(a_ingredients) == 1:
                # add ia pair
                i = list(a_ingredients)[0]
                ia_pairs.append((i, a))
                # remove i from other allergen lists
                for b in [b for b in allergens if not b == a]:
                    if i in allergen_dict[b]:
                        b_ingredients = allergen_dict[b]
                        b_ingredients.remove(i)
                        allergen_dict[b] = b_ingredients
                # remove a from other ingredient lists
                for j in [j for j in ingredients if not j == i]:
                    if a in ingredient_dict[j]:
                        j_allergens = ingredient_dict[j]
                        j_allergens.remove(a)
                        ingredient_dict[j] = j_allergens

# get allergens listed alphabetically
allergens_ordered = sorted(list(allergens))
# put the ingredients in this order
ingredients_ordered = []
for a in allergens_ordered:
    ingredients_ordered += [ia[0] for ia in ia_pairs if ia[1] == a]
# join
part_b = ','.join(ingredients_ordered)
print('part b:',part_b)