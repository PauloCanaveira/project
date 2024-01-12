class Cow:
    def __init__(self, species:str = "cattle", breed:str = "cruzado", sex:str = "female", objective:str = "beef", feeding_situation:str = "extensive"):
        self.species = species
        self.breed = breed
        self.sex = sex
        self.objective = objective
        self.feeding_situation = feeding_situation
        #changes values by user input only if valid values are inserted
        if self.species_ok(species):
            self.species = species
        if self.breed_ok(breed):
            self.breed = breed
        if self.sex_ok(sex):
            self.sex = sex
        if self.objective_ok(objective):
            self.objective = objective
        if self.feeding_situation_ok(feeding_situation):
            self.feeding_situation = feeding_situation
    
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

    def feeding_situation_ok(self, feeding_situation):
        feeding_situations = ["super-intensive", "intensive", "semi-intensive", "extensive", "super-extensive"]
        if feeding_situation in feeding_situations:
            return True
        else:
            raise ValueError ("feeding situation is not defined")


    def __str__(self):
        return f"cow is defined for {self.species} of breed {self.breed} / {self.sex} producing {self.objective}"

