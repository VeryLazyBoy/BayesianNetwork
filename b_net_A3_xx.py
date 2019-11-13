import sys
import json
from itertools import product

class BayesianNetwork(object):
    def __init__(self, structure, values, queries):
        # you may add more attributes if you need
        self.variables = structure["variables"]
        self.dependencies = structure["dependencies"]
        self.conditional_probabilities = values["conditional_probabilities"]
        self.prior_probabilities = values["prior_probabilities"]
        self.queries = queries
        self.answer = []

    def construct(self):

        print()


    def infer(self):
        for i in self.queries:
            print(i)
            index = i["index"]
            given = i["given"]
            tofind = i["tofind"]
            fixed_variables = [x for x in given] + [x for x in tofind]
            varying_variables = [y for y in self.variables if y not in fixed_variables]
            part1 = self.actual_work(given, tofind, fixed_variables, varying_variables)
            part1 = self.val(part1)
            print("Part1: ", part1)
            fixed_variables = [x for x in given]
            varying_variables = [y for y in self.variables if y not in fixed_variables] + [x for x in tofind]
            part2 = self.actual_work(given, tofind, fixed_variables, varying_variables)
            part2 = self.val(part2)
            print("Part2: ", part2)
            answer =  (part1 / part2) * 2
            print()
            self.answer.append({"index": index, "answser": answer})
        print(self.answer)
        return self.answer

    def actual_work(self, given, tofind, fixed_variables, varying_variables):
        all_prob = []
        table_of_variables = given.copy()
        table_of_variables.update(tofind)
        for var in varying_variables:
            table_of_variables[var] = 'True'
        print(table_of_variables)
        all_possible_truth_values = self.perm(table_of_variables, len(varying_variables))
        # Each pass will mutate one of the vaiables to its opposite. So over many passes, we will get the full complement
        for iteration in range(2 ** len(varying_variables)):
            prob = []
            current_truth_values = all_possible_truth_values[iteration]
            current_table = table_of_variables.copy()
            for index, var in enumerate(varying_variables):# setting the varying variables to their new values
                table_of_variables[var] = str(current_truth_values[index])
            # We start calculating their probabilites
            #Case 1: The variable is a prior
            for var in table_of_variables:
                if var in self.prior_probabilities:
                    p = self.prior_probabilities[var][table_of_variables[var]]
                    prob.append(p)
                    print("I am appending: {} for variable: {}".format(p, var))
            #Case 2: The variable is a conditional.
            for var in table_of_variables:
                if var in self.conditional_probabilities and var in self.dependencies:
                    list_of_dependents = self.dependencies[var]
                    prob_list = self.conditional_probabilities[var]
                    for combo in prob_list: # finding the particular combination of values that matches what we have
                        wrongCombo = False
                        filtered_dict = {k:v for (k,v) in combo.items() if "probability" not in k}
                        for key in filtered_dict:
                            if key == "own_value":
                                if filtered_dict[key] != table_of_variables[var]:
                                    wrongCombo=True
                                    break
                                continue
                            if filtered_dict[key] != table_of_variables[key]:
                                wrongCombo=True
                                break
                        if not wrongCombo:
                            p = combo["probability"]
                            prob.append(p)
                            print("I am appending: {} for variable: {}".format(p, var))
                            break
            all_prob.extend([prob]) # prob here contains all the probabilities of our individual variables
            print()
        print("All_prob: ", all_prob)
        return all_prob


    def perm(self, tab, length):
        return list(product([True, False], repeat=length))

    def val(self, arr):
        sum = 0
        for i in arr:
            prod = 1
            for j in i:
                prod *= j
            print("prod: ", prod)
            sum += prod
        return sum





# "given" : {"Burglary": "False", "Earthquake": "True"},
# "tofind" : {"Alarm": "False"}



def main():
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 4:
        print ("\nUsage: python b_net_A3_xx.py structure.json values.json queries.json \n")
        raise ValueError("Wrong number of arguments!")

    structure_filename = sys.argv[1]
    values_filename = sys.argv[2]
    queries_filename = sys.argv[3]

    try:
        with open(structure_filename, 'r') as f:
            structure = json.load(f)
        with open(values_filename, 'r') as f:
            values = json.load(f)
        with open(queries_filename, 'r') as f:
            queries = json.load(f)

    except IOError:
        raise IOError("Input file not found or not a json file")

    # testing if the code works
    b_network = BayesianNetwork(structure, values, queries)
    b_network.construct()
    answers = b_network.infer()



if __name__ == "__main__":
    main()
