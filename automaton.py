class Automaton():

    def __init__(self, config_file):
        self.config_file = config_file
        self.states = []
        self.words = []
        self.transitions = []
        print("Hi, I'm an automaton!")

    def validate(self):
        """Return a Boolean

        Returns true if the config file is valid,
        and raises a ValidationException if the config is invalid.

        #
        # comment lines ( skip them )
        #
        Sigma :
            word1
            word2
            ...
        End
        #
        # comment lines ( skip them )
        #
        States :
            state1
            state2
            state3 ,F
            ...
            stateK , S
            ...
        End
        #
        # comment lines ( skip them )
        #
        Transitions :
            stateX, wordY , stateZ
            stateX, wordY , stateZ
            ...
        End
        """
        with open(self.config_file, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):

                # skip comment lines
                if lines[i].startswith('#'):
                    i += 1
                    continue

                # add every word to words array
                if lines[i].startswith('Sigma :'):
                    j = i + 1
                    while j < len(lines) and not lines[j].startswith('End'):
                        self.words.append(lines[j].strip())
                        j += 1
                    i = j     

                # add states to states array
                elif lines[i].startswith('States :'):
                    j = i + 1

                    # number of start and final states
                    startStates = 0
                    finalStates = 0

                    while j < len(lines) and not lines[j].startswith('End'):
                        arr = lines[j].strip().replace(',', ' ').split()

                        # state.start is a bool that indicates if it is a starting state
                        # state.final is a bool that indicates if it is a final state
                        state = {
                            'name': arr[0],
                            'start': 'S' in arr[1:],
                            'final': 'F' in arr[1:]
                        }

                        # increment start and final states counters if necessary
                        startStates += int(state['start'])
                        finalStates += int(state['final'])

                        self.states.append(state)
                        j += 1

                    # raise exception if there is no starting state or more than 1
                    if startStates != 1:
                        raise Exception('Invalid number of starting states: ' + startStates)

                    # raise exception if there is no final state
                    if finalStates == 0:
                        raise Exception('No final states found')

                    i = j
                    
                # add transitions
                elif lines[i].startswith('Transitions :'):
                    self.transitions = {
                        state['name']: {
                            word: [] for word in self.words
                        } for state in self.states
                    }

                    j = i + 1
                    while j < len(lines) and not lines[j].startswith('End'):
                        arr = lines[j].strip().replace(',', ' ').split()

                        # raise exceptions if invalid transitions
                        if len(arr) != 3:
                            raise Exception('Invalid transition\n' + lines[j])

                        if arr[1] not in self.words:
                            raise Exception('Invalid transition\n' + lines[j])

                        firstStateIsValid = False
                        for state in self.states:
                            if state['name'] == arr[0]:
                                firstStateIsValid = True

                        secondStateIsValid = False
                        for state in self.states:
                            if state['name'] == arr[2]:
                                secondStateIsValid = True

                        if not firstStateIsValid or not secondStateIsValid:
                            raise Exception('Invalid transition\n' + lines[j])

                        # add transition to array
                        self.transitions[arr[0]][arr[1]].append(arr[2])
                        
                        j += 1
                    i = j
                
                else:
                    raise Exception('Invalid config file\n' + lines[i])


                i += 1

        return True

    def accepts_input(self, input_str):
        """Return a Boolean

        Returns True if the input is accepted,
        and it returns False if the input is rejected.
        """
        pass

    def read_input(self, input_str):
        """Return the automaton's final configuration
        
        If the input is rejected, the method raises a
        RejectionException.
        """
        pass
    

if __name__ == "__main__":
    a = Automaton('config.txt')
    print(a.validate())
