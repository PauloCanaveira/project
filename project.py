import pandas as pd
import os

#defines a class cow with variables: species, breed, sex, age, lactating, pregnant, castrate
from cow_class import Cow  

# define time spent by cow in different situations
feeding_situations = ["stall", "rich pasture", "grazing large areas"]
# feeding_shares must add 1
feeding_shares = [0.4, 0.6, 0]

food_types = ["milk", "pasture good quality", "pasture bad quality", "straw", "hay", "sillage", "concentrates"]
food_digestability =[99,70,45,45,58,67,85]

#food_shares must add 1
food_shares = [0,0.50,0.10,0,0,0.20,0.2]

def get_age_weights(my_cow):
    # read the file with the weights per breed, sex and age
    subfolder_weight_name = "weight_data"
    csv_file_path = os.path.join(subfolder_weight_name, f"{my_cow.breed}_{my_cow.sex}.csv")
    df = pd.read_csv(csv_file_path, header = 0)
    #select the correct line for a specific age
    column_headers = df.columns.tolist()
    select_animal = df[df["cow_age"] == my_cow.age]
    selected = select_animal.values[0].tolist()
    animal_age_weights = {}
    for i in range(len(column_headers)):
        animal_age_weights[column_headers[i]] = selected[i]
    weight_mature = animal_age_weights["weight_mature"]
    weight_current = animal_age_weights["weight_current"]
    weight_gain = animal_age_weights["weight_gain"]
    return weight_mature, weight_current, weight_gain

milk_prod = 3
milk_fat = 4
milk_prot = 3.5


# calculate emissions from IPCC equation 10.19
def cow_entfer():
    emission = ef_entfer() * 365
    return emission

# calculate methane emission factor from IPCC equation 10.21; unit kgCH4/head/day
def ef_entfer(my_cow):
    ef_entfer = (ge(my_cow) * (y_m(my_cow)/100)) / 55.65
    return ef_entfer

# calculate gross energy ingested from IPCC equation 10.16; unit: MJ/day 
def ge(my_cow):
    gross_energy = (((ne_m(my_cow) + ne_a(my_cow) + ne_l(my_cow) + ne_p(my_cow))/rem(my_cow))+(ne_g(my_cow)/reg(my_cow)))/(food_de(my_cow)/100)
    return gross_energy

# calculate net-energy needed for animal maintenance from IPCC equation 10.3; unit: MJ/day
def ne_m(my_cow):
    weight_current = get_age_weights(my_cow)[1]
    ne_m = cf_m(my_cow) * (weight_current**0.75)
    return ne_m

# assign maintenance coeficient to "category" from IPCC defaults table 10.4; unit MJ/day/kg
def cf_m(my_cow):
    # IPCC available categories = ["cattle_bufalo", "cattle_bufalo_lactating", "cattle_bufalo_bulls"]
    if my_cow.sex == "female" and my_cow.lactating == "yes":
        cf_m = 0.386
    elif my_cow.sex == "male" and my_cow.castrate == "no" and my_cow.age > 730:
        cf_m = 0.370
    else:
        cf_m = 0.322
    return cf_m

# calculate net-energy needed for daily activity of the animal from IPCC equation 10.4; unit: MJ/day
def ne_a(my_cow):
    ne_a = cf_a(my_cow) * ne_m(my_cow)
    return ne_a

# assign activity coeficient to feeding situation from IPCC defaults Table 10.5; unit: dimensionless
def cf_a(my_cow):
    cf_a = feeding_shares[0] * 0 + feeding_shares[1] * 0.17 + feeding_shares[2] * 0.36
    return cf_a

# calculate net-energy needed for animal growth from IPCC equation 10.6; unit: MJ/day
def ne_g(my_cow):
    weight_mature = get_age_weights(my_cow)[0]
    weight_current = get_age_weights(my_cow)[1]
    weight_gain = get_age_weights(my_cow)[2]
    ne_g = 22.02 * ((weight_current / (cf_g(my_cow)*weight_mature))**0.75) * (weight_gain**1.097)
    return ne_g

# assign growth coeficient to animal from IPCC defaults notes to IPCC equation 10.6; unit: dimensionless
def cf_g(my_cow):
    # options = ["females", "castrates", "bulls"]
    if my_cow.sex == "female":
        cf_g = 0.8
    elif my_cow.sex == "male" and my_cow.castrate == "yes":
        cf_g = 1
    else:
        cf_g = 1.2
    return cf_g

# calculate net-energy needed for lactation from IPCC equation 10.8; unit: MJ/day
def ne_l(my_cow):
    if my_cow.lactating == "yes":
        ne_l = milk_prod * (1.47 + 0.4 * milk_fat)
    else:
        ne_l = 0
    return ne_l

# calculate net-energy needed for animal pregnancy from IPCC equation 10.13; unit: MJ/day
def ne_p(my_cow):
    ne_p = cf_p(my_cow) * ne_m(my_cow)
    return ne_p

# assign pregnancy coeficient from IPCC defaults Table 10.7; unit: dimensionless
def cf_p(my_cow):
    if my_cow.pregnant == "yes":
        cf_p = 0.1
    else:
        cf_p = 0.0
    return cf_p

# calculate average food digestability by weighted average of different food types; unit: % 0-100
def food_de(my_cow):
    de = 0
    for i in range(len(food_types)):
        de += food_digestability[i] * food_shares[i]
    return de

# calculate ratio of net-energy available in a diet for maintenance to digestible energy from IPCC equation 10.14; unit: dimensionless
def rem(my_cow):
    rem = 1.123 - (0.004092 * food_de(my_cow)) + (0.00001126 * (food_de(my_cow)**2)) - (25.4 / food_de(my_cow)) 
    return rem

# calculate ratio of net-energy available for growth in a diet to digestible energy from IPCC equation 10.15; unit: dimensionless
def reg(my_cow):
    reg = 1.164 - (0.00516 * food_de(my_cow)) + (0.00001308 * (food_de(my_cow)**2)) - (37.4 / food_de(my_cow))
    return reg

# assign methane conversion factor from IPCC defaults Table 10.12; unit: % 0-100
def y_m(my_cow):
    if food_de(my_cow) <= 62:
        y_m = 7.0
    elif 62 < food_de(my_cow) < 72:
        y_m = 6.3
    else:
        y_m = 4.0 
    return y_m

def main():
    my_cow = Cow()
    
    day_emissions = []
    day_weight = []
    day_weight_gain = []
    while my_cow.age <= 7300:
        day_em = ef_entfer(my_cow)
        day_w_current = get_age_weights(my_cow)[1]
        day_w_gain = get_age_weights(my_cow)[2]
        day_emissions.append(round(day_em, ndigits=2))
        day_weight.append(round(day_w_current,ndigits=1))
        day_weight_gain.append(round(day_w_gain,ndigits=1))
        my_cow.age += 1
    print (day_emissions)
    print (day_weight)
    print (day_weight_gain)

