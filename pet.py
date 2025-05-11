
class pet:
    def __init__(self,id,name,age,species,image,adopted=False):
        self.id=id
        self.name=name
        self.age=age
        self.species=species
        self.image=image
        self.adopted=adopted


    def adopt(self):
        self.adopted=True

        