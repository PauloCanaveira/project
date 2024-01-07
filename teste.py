import pandas as pd
import os
import numpy as np 

#defines a class cow with variables: species, breed, sex, age, lactating, pregnant, castrate
from cow_class import Cow  

diet_types = ["milk", "pasture good quality", "pasture bad quality", "straw", "hay", "sillage", "concentrates"]
diet_situations = ["suckling", "super-intensive", "intensive", "semi-intensive", "extensive", "super-extensive"]
objectives = ["beef", "milk-low", "milk-medium", "milk-high"]

def main():
    x = food_de("extensive")
    y = food_de("suckling")
    z = food_de("super-intensive")
    print (x)
    print (y)
    print (z)

def food_de(diet):
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


if __name__ == "__main__":
    main()
