import pandas as pd
import os
import numpy as np 
import matplotlib.pyplot as plt

# defines a class cow with variables: species, breed, sex, objetive
from cow_class import Cow  

# defines some management pre-defined options that will be needed in calculations
breeds = ["aberdeen-angus", "alentejana", "arouquesa", 
              "barrosa", "brava-de-lide", "cachena", "charolesa", 
              "cruzado", "limousine", "maronesa", "mertolenga", "minhota", "mirandesa", "preta"]
sexes = ["male", "male-castrated", "female"]
feeding_situations = ["super-intensive", "intensive", "semi-intensive", "extensive", "super-extensive"]
objectives = ["beef", "milk-low", "milk-medium", "milk-high"]
diet_types = ["milk", "pasture good quality", "pasture bad quality", "straw", "hay", "sillage", "concentrates"]
diet_situations = ["suckling", "super-intensive", "intensive", "semi-intensive", "extensive", "super-extensive"]

# age of first pregnancy in days (18 months)
preg_start = 547 
# duration of pregancy in days
preg_duration = 283
# period between pregnancies in days (14 months)
preg_between = 427
# age period where calf drinks milk only in days (12 weeks)
age_milk = 84

def main():
    # defines the instance of "Cow" for which the Emission Factor will be calculated
    user_breed = input(f"please provide the animal breed from whithin this list: {breeds}: ").lower().replace(" ", "")
    user_sex = input(f"please provide the animal sex from whithin this list: {sexes}: ").lower().replace(" ", "")
    user_objective = input(f"please provide the production objective for the animal from whithin this list: {objectives}: ").lower().replace(" ", "")
    user_feeding_situation = input(f"please provide the feeding situation for the animal from whithin this list: {feeding_situations}: ").lower().replace(" ", "")
    my_cow = Cow("cattle",user_breed,user_sex, user_objective, user_feeding_situation)

    # define the subfolder that contains the input weight file
    # read CSV file containing the daily weights of specific cow breed / sex combination
    subfolder_weight_name = "weight_data"
    csv_weight_path = os.path.join(subfolder_weight_name, f"{my_cow.breed}_{my_cow.sex}.csv")
    df = pd.read_csv(csv_weight_path, header = 0)

    # extract a specific Column as a Pandas Series and converting to a numpy array
    age = df["cow_age"].to_numpy()
    sex = df["cow_sex"].to_numpy()
    w_mature = df["weight_mature"].round(decimals=0).to_numpy()
    w_current = df["weight_current"].round(decimals=2).to_numpy()
    w_gain = df["weight_gain"].round(decimals=4).to_numpy()

    # create additional numpy vectors with cow characteristics needed for the calculations
    feeding_situation = np.full(len(age), my_cow.feeding_situation)
    objective = np.full(len(age), my_cow.objective)
    pregnant = is_pregnant(age)
    # duration of the lactation period in days
    if my_cow.objective == "beef":
        lact_duration = 182
    else:
        lact_duration = 305
    lactating = is_lactating(age, lact_duration)
    if my_cow.sex == "male-castrated":
        castrate = np.full(len(age), "yes")
    else:
        castrate = np.full(len(age), "no")    

    # maintenance
    cf_maintenance = cf_m(age, sex, lactating, castrate)
    ne_maintenance = ne_m(cf_maintenance, w_current)
    # growth
    cf_growth = cf_g(sex, castrate)
    ne_growth = ne_g(w_mature, w_current, w_gain, cf_growth)
    # activity
    cf_activity = cf_a(feeding_situation)
    ne_activity = ne_a(ne_maintenance,cf_activity)
    # pregnancy
    cf_pregnant = cf_p(pregnant, sex)
    ne_pregnant = ne_p(cf_pregnant,ne_maintenance)
    # lactation
    milk_production = milk_p(objective, lactating, sex)
    milk_fat = milk_f(objective, lactating, sex)
    milk_protein = milk_prot(objective, lactating, sex)
    ne_lactation = ne_l(milk_production, milk_fat)
    # diet and digestability
    diet = diet_type(age,feeding_situation)
    diet_digestibility = diet_de(diet)
    # additional factors for EF calculation
    rem_maintenance = rem(diet_digestibility)
    reg_growth = reg(diet_digestibility)
    y_methane = y_m(diet_digestibility)
    # estimate gross energy needed based on previous factors and calculations
    gross_energy = ge(ne_maintenance, ne_activity, ne_growth, ne_lactation, ne_pregnant, rem_maintenance, reg_growth, diet_digestibility)
    
    # emission factor calculation
    ent_ferm_factor = ef_entfer(gross_energy, y_methane)

    # save the results for my_cow in a csv file  
    # Create a pandas DataFrame containing the results for all varibles/vectors that supported the calculation
    df = pd.DataFrame({"age": age, "sex": sex, "castrate": castrate,
                       "weight_current": w_current, "weight_gain": w_gain, "weight_mature": w_mature,
                       "cf_maintenance": cf_maintenance, "ne_maintenance": ne_maintenance, 
                       "cf_growth": cf_growth, "ne_growth": ne_growth, 
                       "feeding_situation": feeding_situation, "cf_activity": cf_activity, "ne_activity": ne_activity,
                       "is_pregnant": pregnant, "cf_pregnant": cf_pregnant, "ne_pregnant": ne_pregnant,
                       "is_lactating": lactating, "milk_production": milk_production, "milk_fat": milk_fat, "milk protein": milk_protein, "ne_lactation": ne_lactation,
                       "diet": diet, "digestibility_diet": diet_digestibility,
                       "REM": rem_maintenance, "REG": reg_growth, 
                       "Ym": y_methane, "gross_energy": gross_energy,
                       'EF_CH4_ent_ferm': ent_ferm_factor})
    # Specify the subfolder and CSV file name
    subfolder = "output_data"
    csv_output_name = f"{my_cow.breed}_{my_cow.sex}_{my_cow.objective}_{my_cow.feeding_situation}_EF.csv"
    # Create the subfolder if it doesn't exist
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    # Create the full CSV file path
    csv_file_path = os.path.join(subfolder, csv_output_name)
    # Write the DataFrame to the CSV file
    df.to_csv(csv_file_path, index=False)

    print("Enteric fermentation CH4 emission =", ent_ferm_factor)

    # create a line plot with emission factor
    plt.plot(age, ent_ferm_factor, label = "Enteric fermentation methane emission")
    plt.xlabel("Age of animal (days)")
    plt.ylabel("Methane emission (kgCH4/day)")
    plt.title("Enteric fermentation methane emission")
    plt.legend()
    subfolder = "output_data"
    graph_name = f"{my_cow.breed}_{my_cow.sex}_{my_cow.objective}_{my_cow.feeding_situation}_EF_ent_ferm.png"
    plt.savefig(os.path.join(subfolder, graph_name), format='png')

    # create a stacked line plot with net energies
    plt.plot(age, ne_maintenance, label = "Net-energy for maintenance")
    plt.plot(age, ne_activity, label = "Net-energy for activity")
    plt.plot(age, ne_growth, label = "Net-energy for growth")
    plt.plot(age, ne_pregnant, label = "Net-energy for pregnancy")
    plt.plot(age, ne_lactation, label = "Net-energy for lactation")
    plt.xlabel("Age of Animal (days)")
    plt.ylabel("Net-energy (MJ/day)")
    plt.title("Net-energy needed for different purposes")
    plt.legend()
    subfolder = "output_data"
    graph_name = f"{my_cow.breed}_{my_cow.sex}_{my_cow.objective}_{my_cow.feeding_situation}_Net_energy.png"
    plt.savefig(os.path.join(subfolder, graph_name), format='png')
    
# calculate net-energy needed for animal maintenance from IPCC equation 10.3; unit: MJ/day
def ne_m(cf_m, w_current):

    ne_m = np.round((cf_m * np.power(w_current,0.75)), 3)
    return ne_m
# assign maintenance coeficient to "category" from IPCC defaults table 10.4; unit MJ/day/kg
def cf_m(age, sex, lactating, castrate):
    # IPCC available categories = ["cattle_bufalo", "cattle_bufalo_lactating", "cattle_bufalo_bulls"]
    cf_m_array = np.where((sex == "female") & (lactating == "yes"), 0.386, 
        np.where((sex == "male") & (castrate == "no") & (age > 730), 0.370, 
         0.322))
    return cf_m_array

# calculate net-energy needed for animal growth from IPCC equation 10.6; unit: MJ/day
def ne_g(w_mature, w_current, w_gain, cf_growth):
    ne_g_array = np.round(22.02 * (np.power(w_current/(cf_growth*w_mature),0.75) * np.power(w_gain, 1.097)), decimals=3)
    return ne_g_array
# assign growth coeficient to animal from IPCC defaults notes to IPCC equation 10.6; unit: dimensionless
def cf_g(sex, castrate):
    # IPCC available categories = ["females", "castrates", "bulls"]
    cf_g_array = np.where((sex == "female"), 0.8, 
        np.where((sex == "male-castrate") & (castrate == "yes"), 1, 
         1.2))
    return cf_g_array

# calculate net-energy needed for daily activity of the animal from IPCC equation 10.4; unit: MJ/day
def ne_a(ne_maintenance,cf_activity):
    ne_a = np.round(cf_activity * ne_maintenance, decimals=3)
    return ne_a
# assign an activity coeficient to feeding situation from IPCC defaults Table 10.5; unit: dimensionless
def cf_a(feeding_situation):
    # IPCC available categories = ["stall", "rich pasture", "grazing large areas"]
    feeding_defaults_cf_a = [0.00, 0.17, 0.36]
    # share of time spent in ["stall", "rich pasture", "grazing large areas"]
    feeding_shares = {"super-intensive": [0.95, 0.05, 0.00],
                        "intensive": [0.80, 0.20, 0.00],
                        "semi-intensive": [0.50, 0.50, 0.00],
                        "extensive": [0.00, 0.70, 0.30],
                        "super-extensive": [0.00, 0.30, 0.70]}
    # calculates cf_a for all feeding situations
    cf_a_feeding_situation = {}
    for feeding_sit in feeding_situations:
        cf_a = 0
        for i in range(len(feeding_defaults_cf_a)):
            cf_a += feeding_defaults_cf_a[i] * feeding_shares[feeding_sit][i]
        cf_a_feeding_situation[feeding_sit] = round(cf_a, ndigits=3)
    # create a NumPy array using the values from the dictionary
    cf_a_array = np.array([cf_a_feeding_situation[x] for x in feeding_situation])
    return cf_a_array

# calculate net-energy needed for animal pregnancy from IPCC equation 10.13; unit: MJ/day
def ne_p(cf_pregnant,ne_maintenance):
    ne_p = np.round(cf_pregnant * ne_maintenance, decimals=3)
    return ne_p
# assign pregnancy coeficient from IPCC defaults Table 10.7; unit: dimensionless
def cf_p(pregnant, sex):
    cf_p_array = np.where((pregnant == "yes") & (sex == "female"), 0.1, 0.0)
    return cf_p_array
# determine if the cow is pregnant or not at a specific age
def is_pregnant(age):
    pregnant_periods = []
    start = preg_start
    a = 1
    while a <= len(age):
        end = start + preg_duration
        pregnant_periods.append([start, end])
        start += preg_between
        a = end+1
    pregnant = np.full(len(age), "no", dtype='<U3')
    for start, end in pregnant_periods:
        pregnant[start-1:end] = "yes"
    return pregnant

# calculate net-energy needed for lactation from IPCC equation 10.8; unit: MJ/day
def ne_l(milk_production, milk_fat):
    ne_l = milk_production * (1.47 + 0.4 * milk_fat)
    return ne_l
# determine if the cow is lactating or not at a specific age
def is_lactating(age, lact_duration):
    lactating_periods = []
    start = preg_start + preg_duration + 1
    a = 1
    while a <= len(age):
        end = start + lact_duration
        lactating_periods.append([start, end])
        start += preg_between
        a = end + 1
    lactating = np.full(len(age), "no", dtype='<U3')
    for start, end in lactating_periods:
        lactating[start-1:end] = "yes"
    return lactating
# assigns milk production in kg/day according to production objective and milk productivity
# low: assuming 5500kg per lactation over 305 days
# medium: assuming 7900kg per lactation over 305 days
# high: assuming 11000kg per lactation over 305 days
def milk_p(objective, lactating, sex):
    milk_p_array = np.where((objective == "beef") & (sex == "female") & (lactating == "yes"), 3,
                    np.where((objective == "milk-low") & (sex == "female") & (lactating == "yes"), 18, 
                    np.where((objective == "milk-medium") & (sex == "female") & (lactating == "yes"), 26.2,
                    np.where((objective == "milk-high") & (sex == "female") & (lactating == "yes"), 36, 0))))
    return milk_p_array
# assigns milk fat content in percent [0-100] according to production objective and milk productivity
def milk_f(objective, lactating, sex):
    milk_f_array = np.where((objective == "beef") & (sex == "female") & (lactating == "yes"), 4, 
                    np.where((objective == "milk-low") & (sex == "female") & (lactating == "yes"), 4, 
                    np.where((objective == "milk-medium") & (sex == "female") & (lactating == "yes"), 4,
                    np.where((objective == "milk-high") & (sex == "female") & (lactating == "yes"), 4, 0))))
    return milk_f_array
# assigns milk protein content in percent [0-100] according to production objective and milk productivity
def milk_prot(objective, lactating, sex):
    milk_prot_array = np.where((objective == "beef") & (sex == "female") & (lactating == "yes"), 3.5, 
                    np.where((objective == "milk-low") & (sex == "female") & (lactating == "yes"), 3.5, 
                    np.where((objective == "milk-medium") & (sex == "female") & (lactating == "yes"), 3.5,
                    np.where((objective == "milk-high") & (sex == "female") & (lactating == "yes"), 3.5, 0))))
    return milk_prot_array

# assigns a diet type to the cow according to age of the animal
def diet_type(age,feeding_situation):
    # available diet_types = 
    # ["milk", "pasture good quality", "pasture bad quality", "straw", "hay", "sillage", "concentrates"]
    age_conditions = [(age <= age_milk), (age_milk <= age)]
    diet_t = ["suckling", feeding_situation]
    diet_type_array = np.select(age_conditions, diet_t)
    return diet_type_array

#calculates the digestibility of the diet at each age
def diet_de(diet):
    # available categories = ["milk", "pasture good quality", "pasture bad quality", "straw", "hay", "sillage", "concentrates"]
    diet_defaults_de = [99,70,45,45,58,67,85]
    # share of food types in each feeding situation
    diet_shares = {"suckling": [0.9, 0.05, 0, 0, 0, 0, 0.05],
            "super-intensive": [0, 0.1, 0, 0, 0.1, 0.3, 0.5],
            "intensive": [0, 0.25, 0, 0, 0.15, 0.3, 0.3],
            "semi-intensive": [0, 0.35, 0, 0, 0.15, 0.25, 0.25],
            "extensive": [0.0, 0.5, 0.3, 0.05, 0.05, 0.1, 0],
            "super-extensive": [0.0, 0.4, 0.6, 0, 0, 0, 0]}
    # calculates digestibility for all feeding situations
    de_diet_situation = {}
    for diet_sit in diet_situations:
        de = 0
        for i in range(len(diet_defaults_de)):
            de += diet_defaults_de[i] * diet_shares[diet_sit][i]
        de_diet_situation[diet_sit] = round(de, ndigits=3)
    # create a NumPy array using the values from the dictionary
    de_array = np.array([de_diet_situation[x] for x in diet])
    return de_array

# calculate ratio of net-energy available in a diet for maintenance to digestible energy from IPCC equation 10.14; unit: dimensionless
def rem(diet_digestibility):
    rem = np.round((1.123 - (0.004092 * diet_digestibility) + (0.00001126 * (diet_digestibility**2)) - (25.4 / diet_digestibility)), 5)
    return rem

# calculate ratio of net-energy available for growth in a diet to digestible energy from IPCC equation 10.15; unit: dimensionless
def reg(diet_digestibility):
    reg = np.round((1.164 - (0.00516 * diet_digestibility) + (0.00001308 * (diet_digestibility**2)) - (37.4 / diet_digestibility)), 5)
    return reg

# assign methane conversion factor from IPCC defaults Table 10.12; unit: % 0-100
def y_m(diet_digestibility):
    y_m_conditions = [(diet_digestibility <= 62), (diet_digestibility > 62) & (diet_digestibility <= 72), (diet_digestibility > 72)]
    y_m_defaults = [7.0, 6.3, 4.0]
    y_m_array = np.select(y_m_conditions, y_m_defaults)
    return y_m_array

# calculate gross energy ingested from IPCC equation 10.16; unit: MJ/day 
def ge(ne_maintenance, ne_activity, ne_growth, ne_lactation, ne_pregnant, rem_maintenance, reg_growth, diet_digestibility):
    gross_energy = np.round(((((ne_maintenance + ne_activity + ne_lactation + ne_pregnant)/rem_maintenance) + (ne_growth/reg_growth))/(diet_digestibility/100)), 3)
    return gross_energy

# calculate methane emission factor from IPCC equation 10.21; unit kgCH4/head/day
def ef_entfer(gross_energy, y_methane):
    ef_entfer_array = np.round(((gross_energy * (y_methane/100)) / 55.65), 3)
    return ef_entfer_array

if __name__ == "__main__":
    main()