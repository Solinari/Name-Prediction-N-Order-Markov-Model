#N Order Markov Model
#let's predict some names. :)

import random

def GetNames(names):
    '''gets the list of names I need for the model'''

    infile = open(names, 'r')
    read_lines = infile.readlines()
    infile.close()

    stripped = [read_lines[x].rstrip('\n')
                for x in range(len(read_lines))]


    return stripped


def MarkovModel(name, order, MyModel):
    '''this defines my markov model for any such order.'''

    # need to iterate len of name - order
    # to get 1st letter and expanding to 1st + 1, iteratively

    for i in range(0, len(name) - order):
        curr_letters = name[i:i + order]
        next_letter = name[i + order]

        #create a dict entry for the newest combination not yet in the model
        if curr_letters not in MyModel:
            MyModel[curr_letters] = {}

        # now the entry within the entry of the dict for letters after
        # the latest letter found, which would be 1 at first
        if next_letter not in MyModel[curr_letters]:
            MyModel[curr_letters][next_letter] = 1

        # found a combination already in the dict, so increment it
        else:
            MyModel[curr_letters][next_letter] += 1

    return MyModel




#print(MarkovModel("aaaaaaaaaaabbbbbbb", 7))
#print(GetNames("namesBoys.txt"))

def ExpandMM(nameslist, order):
    '''now pass my list of names into here,
    and expand the model on every single new name
    by repassing the same model'''

    # we're going to pass this empty dict as our model to update through the markov models
    # I BELIEVE this captures all the transitional states in the hash form....I think..
    ExpandedModel = {}

    # markov model for each order i == 1 to i == order
    for i in range(1, order + 1):

        curr_order = i

        # run the model at each increment of i up untill i == order
        for j in range(len(nameslist)):

            ExpandedModel = MarkovModel(nameslist[j], curr_order, ExpandedModel)

    return ExpandedModel

#print(ExpandMM(GetNames("namesBoys.txt"), 7))
#print(ExpandMM(["avacadoo"], 9))



# Test to confirm frequency numbers to proabilities
# These are just some slices I pulled from the full output of the boys names
##test = { 'Gi': {'o': 3, 'a': 2, 'l': 2, 'd': 1},
##         'N': {'e': 3, 'i': 10, 'a': 7, 'o': 4},
##         'st': {'e': 2, 'o': 13, 'i': 11, 'a': 3, 'u': 2}}
##
##
##for key in test:
##    print(test[key])
##    print(test[key].values())
##    theSum = sum(test[key].values())
##    print(theSum)
##
##    for lilkey in test[key]:
##        print(lilkey)
##        print(test[key][lilkey])
##        test[key][lilkey] = float(test[key][lilkey] / theSum)
##        print(test[key][lilkey])
##
### cofirm that this works
##for key in test:
##    print(test[key])
##    print(test[key].values())
##    theSum = sum(test[key].values())
##    print(theSum)



def freq2prob(markovfreq):
    '''this function goes through all the inner hashes
    and converts the number of copies each inner key was found(the value)
    to a probability that sums to 1 for that inner hash. this is stochasticity
    I don't know if this is row or column though...since this is N dimensions..'''

    # for every fragment in the expanded markov matrix sum its frequencies
    for frag in markovfreq:
        
        fragSum = sum(markovfreq[frag].values())

        # then set each value within that fragment to float(value/sum)
        for subfrag in markovfreq[frag]:

            markovfreq[frag][subfrag] = float(markovfreq[frag][subfrag] / fragSum)

    return markovfreq

#print(freq2prob(ExpandMM(GetNames("namesBoys.txt"), 7)))


def weighted_choice(picks):
    '''This will chose a key from the subdict
    based on the probability value of it's key'''

    #I know this sums to 1 for this model, but doing this anyways
    tot = sum(weight for pick, weight in picks)

    #a random float between 0 and 1
    rand = random.uniform(0, tot)

    #start at 0
    upto = 0

    # think of this for key, value in dict.items()
    for pick, weight in picks:
        
        # if the last upto plus this weight is greater than rand
        # then return a picked letter and increment upto by the last weight found
        # this is interesting because these hashes change every run..
        if upto + weight > rand:
            return pick

        upto += weight


# some chosen slice sums to 1.
# now lets build a weight random generation model
# to select elements with their proabilitstic weights accounted for
##test2 = {'F': {'e': 0.17647058823529413,
##              'a': 0.058823529411764705,
##              'i': 0.23529411764705882,
##              'l': 0.058823529411764705,
##              'r': 0.47058823529411764}}
##
##for key in test2:
##    print(test2[key].items())
##
##    # class object dict_items
##    print(type(test2[key].items()))
##    #print(sum(test2[key].values()))
##    print("Random pick is:  ")
##    print(weighted_choice(test2[key].items()))
##
##    for key2 in test2[key]:
##        #inner keys are strings
##        print(key2)
##        #inner values are floats
##        print(test2[key][key2])

def generateNames(order, minlen, maxlen, number, nameslist):
    ''' use all above functions to generate new names not in the names list passed
    a number of times equal to number'''

    myList = GetNames(nameslist)

    MyMarkovModel = freq2prob(ExpandMM(myList, order))
    keys = list(MyMarkovModel.keys())

    # these are all that I can start with intitially
    starts = [keys[x]
              for x in range(len(keys))
              if keys[x].istitle() == True]
    

    names = []

    chosen = ''

    while number > 0:

        name = ''

        while len(name) < minlen:

            # we start with a randomly chosen beginning
            # since these don't have weights on them
            # because they cannot be entailed from
            # any such char before them
            if len(name) == 0:
                begin = random.choice(starts)
                name += begin
                chosen = begin
                print(name)

            # append something if it's still less than minlen
            # weighted_choice(test2[key].items())
            pick = weighted_choice(MyMarkovModel[chosen].items())
            name += pick
            chosen = pick
            print(name)

        #build the rest of the name
        while len(name) <= maxlen:
            pick = weighted_choice(MyMarkovModel[chosen].items())
            name += pick
            chosen = pick
            print(name)
        
        names.append(name)
        number -= 1

        print(names)

generateNames(10, 4, 8, 10, "namesGirls.txt")

def Go():
    '''props user for UI calls'''


    while True:

        User = str(input("Please enter B to begin Name Prediction or Q to quit\n"))
        User = User.upper()
                         
        if User == "Q":
            break
                         
        if User == "B":

            #order
            Order = int(input("Please enter a positive integer between 1 and 15 for the Order of the markov model's name prediction:\n\n \n\n"))

            #min length name
            minLen = int(input("Please enter a positive interger beweteen 3 and 15 for the minimum length of the name\n\n"))

            #max length name

            maxLen= int(input("Please enter a positive interger beweteen 3 and 15 for the minimum length of the name\n\n"))

            if 1 <= Order <= 10 and 3 <= minLen <= 15 and minLen < maxLen:

                # Gender
                Gender = str(input("Please enter:\n\n - M for the male names set\n\n - F for the female names set\n\n"))
                Gender = Gender.upper()
                
                # number of names

                numOfNames = int(input("Finally, how many names would you like me to generate?\n\n"))
                

                if Gender == "F":

                    # call female list
                    generateNames(Order, minLen, maxLen, Gender, numOfNames, "namesGirls.txt")
                    continue
                                  
                if Gender == "M":

                    # call male list
                    generateNames(Order, minLen, maxLen, Gender, numOfNames, "namesBoys.txt")
                    continue
                
                if  Gender != "F" or Gender != "M":
                    continue

        if User != "C" or User != "Q":
            continue

    print("Good Bye!")


#Go()
