class Pet:
    def __init__(self, id, name, species, age, image_url, adopted, shelter_id, about):
        self.id = id
        self.name = name
        self.species = species
        self.age = age
        self.image_url = image_url
        self.adopted = adopted
        self.shelter_id = shelter_id
        self.about = about

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "image_url": self.image_url,
            "adopted": self.adopted,
            "shelter_id": self.shelter_id,
            "about": self.about
        }
