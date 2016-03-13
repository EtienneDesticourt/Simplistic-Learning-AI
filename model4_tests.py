from model4 import Being

def testIntegrate():
    print("Testing concept integration.")
    B = Being()
    assert(B.concepts == [])
    assert(B.associations.shape == (0,))
    #Test first concept add
    B.integrate("testConcept1")
    assert(B.concepts == ["testConcept1"])
    assert(B.associations.shape == (1,1))
    assert(B.associations[0][0] == 0)
    #Test next concept add
    B.integrate("testConcept2")
    assert(B.concepts == ["testConcept1", "testConcept2"])
    assert(B.associations.shape == (2,2))
    assert(B.associations[0][0] == 0)
    assert(B.associations[0][1] == 0)
    assert(B.associations[1][0] == 0)
    assert(B.associations[1][1] == 0)    
    print("Concept integration succesful.")

def testCalcAssociationWeight():
    print("Testing association weight calculation.")
    B = Being()
    #This is what we want the function to do no matter the specific formula
    w = B.calcAssociationWeight(0)
    assert(w == 0)
    w = B.calcAssociationWeight(10000)
    assert(w <= 1 and w > 0.99)
    print("Association weight calculation succesful.")

def testCalcAssociationNumber():
    print("Testing association number calculation.")
    B = Being()
    w = B.calcAssociationWeight(0)
    n = B.calcAssociationNumber(w)
    assert(n == 0)
    w = B.calcAssociationWeight(10000)
    n = B.calcAssociationNumber(w)
    assert(n > 9999.9 and n < 10000.1)
    print("Association number calculation succesful.")
    
testIntegrate()
testCalcAssociationWeight()
testCalcAssociationNumber()


