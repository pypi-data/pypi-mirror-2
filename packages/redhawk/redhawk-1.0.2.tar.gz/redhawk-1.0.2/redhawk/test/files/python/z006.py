# Test Classes

class Animal:
  pass

class Cat(Animal):
  def MakeSound(self):
    print "Meow"

class Tiger(Animal, Cat):
  def MakeSound(self):
    print "Grrrr"

  def EatPrey(self):
    print "Chomp! Chomp!"

