class Cow:
    allowed_species = ["cattle"]
    allowed_breeds = ["aberdeen-angus", "alentejana", "arouquesa", 
              "barrosa", "brava-de-lide", "cachena", "charolesa", 
              "cruzado", "limousine", "maronesa", "mertolenga", "minhota", "mirandesa", "preta"]
    allowed_sexes = ["male", "male-castrated", "female"]
    allowed_objectives = ["beef", "milk-low", "milk-medium", "milk-high"]
    allowed_feeding_situations = ["super-intensive", "intensive", "semi-intensive", "extensive", "super-extensive"]

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
    @classmethod
    def species_ok(cls, species):
        if species in cls.allowed_species:
            return True
        else:
            raise ValueError ("input species is not defined")

    @classmethod
    def breed_ok(cls, breed):
        if breed in cls.allowed_breeds:
            return True
        else:
            raise ValueError ("input breed is not defined")
        
    @classmethod
    def sex_ok(cls, sex):
        if sex in cls.allowed_sexes:
            return True
        else:
            raise ValueError ("input sex is not defined")

    @classmethod
    def objective_ok(cls, objective):
        if objective in cls.allowed_objectives:
            return True
        else:
            raise ValueError ("production objective is not defined")

    @classmethod
    def feeding_situation_ok(cls, feeding_situation):
        if feeding_situation in cls.allowed_feeding_situations:
            return True
        else:
            raise ValueError ("feeding situation is not defined")

    def __str__(self):
        return f"cow is defined for {self.species} of breed {self.breed} / {self.sex} producing {self.objective}"

