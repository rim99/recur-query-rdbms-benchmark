import id_gen

tag_names = [
    "Mickey Mouse",
    "Bugs Bunny",
    "Homer Simpson",
    "Fred Flintstone",
    "Snoopy",
    "SpongeBob SquarePants",
    "Eric Cartman",
    "Daffy Duck",
    "Winnie-the-Pooh",
    "Charlie Brown",
    "Goofy",
    "Bart Simpson",
    "Donald Duck",
    "Garfield",
    "Woody",
    "Betty Boop",
    "Tom Cat",
    "Jerry Mouse",
    "Scooby Doo",
    "Woody Woodpecker",
    "Hello Kitty",
    "Mighty Mouse",
    "Felix The Cat",
    "Wile E Coyote",
    "Minnie Mouse",
    "Tweety Bird",
    "Pink Panther",
    "Peter Griffin",
    "Porky Pig",
    "Road Runner",
    "George Jetson",
    "Daisy Duck",
    "Elmer Fudd",
    "Popeye",
    "Patrick Star",
    "Sylvester The Cat",
    "Roger Rabbit",
    "Beavis",
    "Butt-Head",
    "Kenny McCormick",
    "Shrek",
    "Tigger",
    "Papa Smurf",
    "Fat Albert",
    "Buzz Lightyear",
    "Ren",
    "Stimpy",
    "Norville “Shaggy” Rogers",
    "Tommy Pickles",
    "Yogi Bear"
]

class Tag:
    def __init__(self, name):
        self.id = id_gen.UUID1.get()
        self.name = name
    def to_record(operator):
        rec = {
            "tag_id": self.id,
            "name": self.name,
            "operator_name": operator
        }
        return rec

class TagGen:
    @staticmethod
    def gen():
        tags = [Tag(name) for name in tag_names]
        return tags

