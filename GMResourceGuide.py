import json
import re

RESOURCE_FILE="C:\Program Files (x86)\Steam\steamapps\common\Going Medieval\Going Medieval_Data\StreamingAssets\Resources\Resources.json"
BUILDING_FILE="C:\Program Files (x86)\Steam\steamapps\common\Going Medieval\Going Medieval_Data\StreamingAssets\Constructables\Furniture.json"
TRAP_FILE="C:\Program Files (x86)\Steam\steamapps\common\Going Medieval\Going Medieval_Data\StreamingAssets\Constructables\Traps.json"
PRODUCTION_TABLE_FILE="C:\Program Files (x86)\Steam\steamapps\common\Going Medieval\Going Medieval_Data\StreamingAssets\Constructables\ProductionBuildings.json"

#Modes are "TRADING" or "STORAGE"
MODE_TRADING=0
MODE_STORAGE=1

MODE=MODE_TRADING

item_data = []

def get_name(item):
    if "resourceId" in item:
        return item["resourceId"]
    if "id" in item:
        return item["id"]
    return None

def split_at_capital_letters(input_str):
    splitted = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', input_str)).split()
    return splitted

def get_categories(sorting_group):
    splitted = split_at_capital_letters(sorting_group)
    result = str(",").join(splitted)
    return result

for filename in [RESOURCE_FILE,BUILDING_FILE,TRAP_FILE,PRODUCTION_TABLE_FILE]:
    with open(filename,'r') as file:
        file_data = file.read()
        data = json.loads(file_data)
        item_data = item_data + data["repository"]

with open(RESOURCE_FILE,'r') as file:
    file_data = file.read()
    data = json.loads(file_data)
    resources = data["repository"]
    
    if MODE == MODE_TRADING:
        print("Resource,Value,Nutrition,Weight,ValEfficiency,NutritionEfficiency,Categories1,Categories2,Categories3,Categories4")
        for item in item_data:
            name = get_name(item)
            if "weight" in item:
                weight = float(item["weight"])
            else:
                continue
            value = float(item["wealthPoints"])
            nutrition = 0.0
            if "nutrition" in item:
                nutrition = float(item["nutrition"])
            categories = ""
            if "sortingGroup" in item:
                sorting_group = item["sortingGroup"]
                categories = get_categories(sorting_group)
            value_efficiency = value / weight
            nutrition_efficiency = nutrition / weight
            print(str(",").join([name,str(value),str(nutrition),str(weight),str(value_efficiency),str(nutrition_efficiency),categories]))
