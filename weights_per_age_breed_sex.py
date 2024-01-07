import pandas as pd
import os 

#define the subfolder that contains both the input file and will contain the output files
subfolder_name = "weight_data"

cow_breeds = ["aberdeen-angus"]#, "alentejana", "arouquesa", "barrosa", "brava de lide", "cachena", "charolesa", "cruzado", "limousine", "maronesa", "mertolenga", "minhota", "mirandesa", "preta"]
cow_sexes = ["female"]#, "male"]
ages = list(range(1,7301))


def calculate_weights(age, cow_breed, cow_sex):
    csv_file_path = os.path.join(subfolder_name, '0_cow_reference_weights_APA.csv')
    # read the file with the reference weights per breed and sex at specific ages (in months) used by APA
    df = pd.read_csv(csv_file_path, delimiter=";", header = 0)
    #select the correct line for a specific breed/sex combination
    column_headers = df.columns.tolist()
    select_animal = df.loc[(df["animal_breed"] == cow_breed) & (df["animal_sex"] == cow_sex)] 
    selected = select_animal.values[0].tolist()
    weight_ref_ages = [1,122,213,365,730,1824]
    #create a dictionary with the selected weights. Weights are represented by a key = column headers and a tuple ()
    #the tuple contains [0] the weight in kg and [1] the age of the animal in days 
    animal_ref_weights = {}
    for i in range(len(column_headers)):
        if i >= 3:
            j = i-3
            animal_ref_weights[column_headers[i]] = [selected[i],weight_ref_ages[j]]   
        else: 
            animal_ref_weights[column_headers[i]] = selected[i]

    #determines the mature weight 
    weight_mature = animal_ref_weights['W_60'][0]

    #derermines the weight gain
    if age <= animal_ref_weights["W_04"][1]:
        weight_gain = (animal_ref_weights["W_04"][0] - animal_ref_weights["W_00"][0]) / (animal_ref_weights["W_04"][1] - animal_ref_weights["W_00"][1])
    elif age <= animal_ref_weights["W_07"][1]:
        weight_gain = (animal_ref_weights["W_07"][0] - animal_ref_weights["W_04"][0]) / (animal_ref_weights["W_07"][1] - animal_ref_weights["W_04"][1])     
    elif age <= animal_ref_weights["W_12"][1]:
        weight_gain = (animal_ref_weights["W_12"][0] - animal_ref_weights["W_07"][0]) / (animal_ref_weights["W_12"][1] - animal_ref_weights["W_07"][1])     
    elif age <= animal_ref_weights["W_24"][1]:
        weight_gain = (animal_ref_weights["W_24"][0] - animal_ref_weights["W_12"][0]) / (animal_ref_weights["W_24"][1] - animal_ref_weights["W_12"][1])     
    elif age <= animal_ref_weights["W_60"][1]:
        weight_gain = (animal_ref_weights["W_60"][0] - animal_ref_weights["W_24"][0]) / (animal_ref_weights["W_60"][1] - animal_ref_weights["W_24"][1])
    elif age > animal_ref_weights["W_60"][1]:
        weight_gain = 0

    #determines the current weight
    if age <= animal_ref_weights["W_04"][1]:
        weight_current = animal_ref_weights["W_00"][0] + (age - 1) * weight_gain
    elif age <= animal_ref_weights["W_07"][1]:
        weight_current = animal_ref_weights["W_04"][0] + (age - animal_ref_weights["W_04"][1]) * weight_gain
    elif age <= animal_ref_weights["W_12"][1]:
        weight_current = animal_ref_weights["W_07"][0] + (age - animal_ref_weights["W_07"][1]) * weight_gain
    elif age <= animal_ref_weights["W_24"][1]:
        weight_current = animal_ref_weights["W_12"][0] + (age - animal_ref_weights["W_12"][1]) * weight_gain
    elif age <= animal_ref_weights["W_60"][1]:
        weight_current = animal_ref_weights["W_24"][0] + (age - animal_ref_weights["W_24"][1]) * weight_gain
    elif age > animal_ref_weights["W_60"][1]:
        weight_current = animal_ref_weights["W_60"][0]

    return weight_mature, weight_current, weight_gain


for breed in cow_breeds:
    for sex in cow_sexes:
        data = {"cow_age": ages, "cow_breed": breed, "cow_sex": sex}

        weights = pd.DataFrame(data)

        # Calculate weights for each combination of age, animal sex, and animal breed
        weights[['weight_mature', 'weight_current', 'weight_gain']] = weights.apply(lambda row: calculate_weights(row['cow_age'], row['cow_breed'], row['cow_sex']), axis=1).apply(pd.Series)

        # Specify the path to the CSV file in the subfolder
        csv_file_path = os.path.join(subfolder_name, f"{breed}_{sex}.csv")
        # Write the DataFrame to a CSV file in the subfolder
        weights.to_csv(csv_file_path, index=False)

        # Display the DataFrame
        print(f"{breed}_{sex}.csv is done!")