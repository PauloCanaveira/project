# Calculation of the Enteric Fermentation Methane Emission Factor from Cows

This code calculates the daily enteric methane emission factor (kgCH<sub>4</sub>/cow/day) from cows using the method, equations and coeficients provided by the:

IPCC 2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories

Volume 4 Agriculture, Forestry and Other Land Use

Chapter 10 Emissions fron Livestock and Manure Management[^1]

[^1]: https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch10_Livestock.pdf

The Emission Factor is dependent on the amount of gross energy a cow consumes daily. Since it is very difficult to measure gross energy directly, this method estimates this variable using an hierarchical set of equations and parameters that supply different needs of the animal (e.g., maintenance, activity, pregnancy,...), which in turn are dependent of cow characteristics, management objectives, and types of food ingested. 
The general approach is summarised in the image below:

![image](https://github.com/PauloCanaveira/project/assets/145756932/6e46c100-172a-4d42-95f0-b5c4274c57b1)

## Cow Class

## Reference Cow Weights
