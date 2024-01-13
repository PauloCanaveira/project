# Calculation of the Enteric Fermentation Methane Emission Factor from Cows

This code calculates the daily enteric methane emission factor (kgCH<sub>4</sub>/cow/day) from cows using the method, equations and coeficients provided by the:
- IPCC 2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories
  - Volume 4 Agriculture, Forestry and Other Land Use
    - Chapter 10 Emissions from Livestock and Manure Management[^1]

[^1]: https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch10_Livestock.pdf

The Emission Factor is dependent on the amount of gross energy a cow consumes daily. Since it is very difficult to measure gross energy directly, this method estimates this variable using an hierarchical set of equations and parameters that supply different needs of the animal (e.g., maintenance, activity, pregnancy,...), which in turn are dependent of cow characteristics, management objectives, and types of food ingested. 
The general approach is summarised in the image below:

![image](https://github.com/PauloCanaveira/project/assets/145756932/6e46c100-172a-4d42-95f0-b5c4274c57b1)

## Class Cow

A Class was created to define some cow attributes that are relevant to the estimation of the emission factor. 
Class methods were created to guarantee that only certain values are allowed for each attribute. 
The following attributes were created:
- species: describes the species of the animal. Only allows the value "cattle"
- breed: describes the breed of the animal. Allows one value from the list ["aberdeen-angus", "alentejana", "arouquesa","barrosa", "brava de lide", "cachena", "charolesa", "cruzado", "limousine", "maronesa", "mertolenga", "minhota", "mirandesa", "preta"]
- sex: describes the sex of the animal. Allows one value from the list ["male", "female]
- objective: describes the production  objective of the animal (meat or milk production). For milk production defines 3 levels of production. Allows one value from the list ["beef", "milk-low", "milk-medium", "milk-high"]
- feeding_situation: describes the amount of "effort" an animal has to endure to feed itself (animal can be stalled, or grazing in good or bad pastures). Allows one value from the list ["super-intensive", "intensive", "semi-intensive", "extensive", "super-extensive"]

> [!CAUTION]
> Failure to "define" my_cow using these parameters will raise a ValueError 
> Changing these lists will require adaptations in the functions using this information as input.

## Reference Cow Weights

Animal birth size, growth rate and final weight is dependent on the cow's breed and sex.
The most common cow breeds found in Portugal have been caractherised by the Portuguese Environment Agency.
Each breed/sex is characterised by its weight at:
- W_00: weight at birth
- W_04: weight at 4 months
- W_07: weight at 7 months
- W_12: weight at 1 year
- W_24: weight at 2 years
- W_60: weight at 5 years

The folder weight_data contains the file 0_cow_reference_weights_APA.csv with this data.

The auxiliary code weights_per_age_breed_sex.py uses the reference weights above to calculate the 3 weight related variables needed to support the emission factor calculations:
- weight_current: weight of the animal at a specific age (in days)
- weight_gain: daily weight increase of the animal at a specific age (in days)
- weight_mature: weight of a mature (5 years) animal

The folder weight_data contains csv files for the first 7300 days (20 years) for each breed_sex.csv combination

> [!NOTE]
> Information is only available for male/female of the following breeds: aberdeen-angus, alentejana, arouquesa, barrosa, brava de lide, cachena, charolesa, cruzado, limousine, maronesa, mertolenga, minhota, mirandesa, preta.
> Different breeds or different growth rates for these breeds will require creating new breed_sex.csv files
