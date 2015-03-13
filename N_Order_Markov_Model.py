#N Order Markov Model
#let's predict some names. :)

def GetNames(names):
    '''gets the list of names I need for the model'''

    infile = open(names, 'r')
    read_lines = infile.readlines()
    infile.close()

    stripped = [read_lines[x].rstrip('\n')
                for x in range(len(read_lines))]

    return stripped


def MarkovModel(name, order, MyModel):
    '''this defines my markov model for any '''

    # need to iterate len of name - order
    # to get 1st letter and expanding to 1st + 1, iteratively

    for i in range(0, len(name) - order):
        curr_letters = name[i:i + order]
        next_letter = name[i+ order]

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

print(ExpandMM(GetNames("namesBoys.txt"), 7))
print(ExpandMM(["Solinari"], 7))
