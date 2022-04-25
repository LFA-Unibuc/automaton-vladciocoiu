class Automaton():

    def __init__(self, config_file):
        self.config_file = config_file
        self.states = {}
        self.words = []
        self.transitions = []

    def validate(self):
        with open(self.config_file, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):

                # skip comment lines
                if lines[i].strip().startswith('#'):
                    i += 1
                    continue

                # add every word to words array
                if lines[i].strip().startswith('Sigma :') or lines[i].strip().startswith('Sigma:'):
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith('End'):
                        if not len(lines[j].strip()) or lines[j].strip().startswith('#'):
                            j += 1
                            continue
                        self.words.append(lines[j].strip())
                        j += 1
                    i = j     

                # add states to states array
                elif lines[i].strip().startswith('States :') or lines[i].strip().startswith('States:'):
                    j = i + 1

                    while j < len(lines) and not lines[j].strip().startswith('End'):
                        if not len(lines[j].strip()) or lines[j].strip().startswith('#'):
                            j += 1
                            continue
                        arr = lines[j].strip().replace(',', ' ').split()

                        # state.start is a bool that indicates if it is a starting state
                        # state.final is a bool that indicates if it is a final state
                        state = {
                            'start': 'S' in arr[1:],
                            'final': 'F' in arr[1:]
                        }

                        self.states[arr[0]] = state
                        j += 1

                    i = j
                    
                # add transitions
                elif lines[i].strip().startswith('Transitions :') or lines[i].strip().startswith('Transitions:'):
                    self.transitions = {
                        state: {
                            word: [] for word in self.words
                        } for state in self.states
                    }

                    j = i + 1
                    while j < len(lines) and not lines[j].strip().startswith('End'):
                        if not len(lines[j].strip()) or lines[j].strip().startswith('#'):
                            j += 1
                            continue
                        arr = lines[j].strip().replace(',', ' ').split()

                        if len(arr) != 3:
                            # raise Exception('Invalid transition\n' + lines[j].strip())
                            return False

                        if arr[1] not in self.words:
                            # raise Exception('Invalid transition\n' + lines[j].strip())
                            return False

                        firstStateIsValid = False
                        for state in self.states:
                            if state == arr[0]:
                                firstStateIsValid = True

                        secondStateIsValid = False
                        for state in self.states:
                            if state == arr[2]:
                                secondStateIsValid = True

                        if not firstStateIsValid or not secondStateIsValid:
                            # raise Exception('Invalid transition\n' + lines[j].strip())
                            return False

                        # add transition to array
                        self.transitions[arr[0]][arr[1]].append(arr[2])
                        
                        j += 1
                    i = j
                
                else:
                    return False
                    # raise Exception('Invalid config file\n' + lines[i].strip())


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
