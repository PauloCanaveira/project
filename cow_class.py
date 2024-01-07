class Cow:
    def __init__(self, species:str = "cattle", breed:str = "cruzado", sex:str = "female", objective:str = "beef-cow", lactating:str = "no", pregnant:str = "no", castrate:str = "no"):
        self.species = species
        self.breed = breed
        self.sex = sex
        self.objective = objective
        self.lactating = lactating
        self.pregnant = pregnant
        self.castrate = castrate
        #changes values by user input only if valid values are inserted
        if self.species_ok(species):
            self.species = species
        if self.breed_ok(breed):
            self.breed = breed
        if self.sex_ok(sex):
            self.sex = sex
        if self.objective_ok(objective):
            self.objective = objective
        if self.lactating_ok(lactating):
            self.lactating = lactating
        if self.pregnant_ok(pregnant):
            self.pregnant = pregnant
        if self.castrate_ok(castrate):
            self.castrate = castrate
    
    #functions to check if user values are valid
    def species_ok(self, species):
        if self.species == "cattle":
            return True
        else:
            raise ValueError ("input species is not defined")

    def breed_ok(self, breed):
        cow_breeds = ["aberdeen-angus", "alentejana", "arouquesa", 
              "barrosa", "brava de lide", "cachena", "charolesa", 
              "cruzado", "limousine", "maronesa", "mertolenga", "minhota", "mirandesa", "preta"]
        if breed in cow_breeds:
            return True
        else:
            raise ValueError ("input breed is not defined")
        
    def sex_ok(self, sex):
        sexes = ["male", "female"]
        if sex in sexes:
            return True
        else:
            raise ValueError ("input sex is not defined")

    def objective_ok(self, objective):
        objectives = ["beef", "milk-low", "milk-medium", "milk-high"]
        if objective in objectives:
            return True
        else:
            raise ValueError ("production objective is not defined")


    def lactating_ok(self, lactating):
        if self.sex == "female" and lactating == "yes":
            return True
        else:
            return False

    def pregnant_ok(self, pregnant):
        if self.sex == "female" and pregnant == "yes":
            return True
        else:
            return False
        
    def castrate_ok(self, castrate):
        if self.sex == "male" and castrate == "yes":
            return True
        else:
            return False

    def __str__(self):
        return f"cow is defined for {self.species} of breed {self.breed} / {self.sex} with {self.age} days of life with {self.weightmature}kg at maturity"

