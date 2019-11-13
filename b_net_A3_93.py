import sys
import json
from itertools import product

class Node():

    def __init__(self, name):
        self.parents = []
        self.children = []
        self.name = name
        self.is_prior = True

        # cpt table
        # for prior nodes:
        #     key is variable's value
        # for conditional nodes:
        #     key is a sorted tuple whose item is (variable, variable's value)
        self.prob_table = {}

    def add_child(self, child):
        """
        Arg:
            child (str): child to add
        """
        self.children.append(child)

    def add_parents(self, parents):
        """
        Arg:
            parents (list of str): list of parent to add
        """
        self.parents.extend(parents)

    def set_is_prior(self, is_prior):
        self.is_prior = is_prior

    def set_prob_table(self, prob_table):
        self.prob_table = prob_table

    def is_prior(self):
        return self.is_prior

    def get_prob(self, value_dict):
        """
        Arg:
            value_dict (dict): variable name to value dictionary
        """
        if self.is_prior:
            key = value_dict[self.name]
        else:
            condition = self.parents + [self.name]
            key = ()
            for c in condition:
                key = key + ((c, value_dict[c]),)
            key = tuple(sorted(key))
        return self.prob_table[key]


class BayesianNetwork(object):
    def __init__(self, structure, values, queries):
        # you may add more attributes if you need
        self.variables = structure["variables"]
        self.dependencies = structure["dependencies"]
        self.conditional_probabilities = values["conditional_probabilities"]
        self.prior_probabilities = values["prior_probabilities"]
        self.queries = queries
        self.answer = []
        self.graph = {}

    def construct_prior_prob_table(self, var):
        """
        Constructs the cpt table. The key is variable's value
        """
        value_dict = self.prior_probabilities[var]
        prob_table = {}
        for key in value_dict:
            prob_table[key] = value_dict[key]
        return prob_table

    def construct_conditional_prob_table(self, var):
        """
        Constructs the cpt table. The key a sorted tuple whose item is (variable, variable's value)
        """
        value_dict_arr = self.conditional_probabilities[var]
        prob_table = {}
        for value_dict in value_dict_arr:
            prob = value_dict['probability']
            key = ()
            for k in value_dict:
                if k != 'probability':
                    if k != 'own_value':
                        key = key + ((k, value_dict[k]),)
                    else:
                        key = key + ((var, value_dict[k]),)
            key = tuple(sorted(key))
            prob_table[key] = prob
        return prob_table

    def construct(self):
        """
        Constructs the bayesian network as a graph.
        """
        for var in self.variables:
            node = Node(var)
            self.graph[var] = node

        for var in self.prior_probabilities:
            self.graph[var].set_prob_table(self.construct_prior_prob_table(var))
            self.graph[var].set_is_prior(True)

        for var in self.dependencies:
            parents = self.dependencies[var]
            self.graph[var].add_parents(parents)
            self.graph[var].set_prob_table(self.construct_conditional_prob_table(var))
            self.graph[var].set_is_prior(False)
            for p in parents:
                self.graph[p].add_child(var)
        # self.printGraph()

    def infer(self):
        for i in self.queries:
            index = i["index"]
            given = i["given"]
            tofind = i["tofind"]
            fixed_variables = [x for x in given] + [x for x in tofind]
            varying_variables = [y for y in self.variables if y not in fixed_variables]
            print(given)
            part1 = self.calculate_prob(given, tofind, fixed_variables, varying_variables)
            print(given)

            fixed_variables = [x for x in given]
            varying_variables = list(set([y for y in self.variables if y not in fixed_variables] + [x for x in tofind]))
            part2 = self.calculate_prob(given, tofind, fixed_variables, varying_variables)
            answer =  part1 / part2
            self.answer.append({"index": index, "answser": answer})
        print(self.answer)
        return self.answer

    def get_every_prob(self, value_dict):
        prob_arr = []
        for var in self.graph:
            node = self.graph[var]
            prob_arr.append(node.get_prob(value_dict))
        return prob_arr

    def calculate_prob(self, given, tofind, fixed_variables, varying_variables):
        all_prob = []
        table_of_variables = given.copy()
        table_of_variables.update(tofind)
        for var in varying_variables:
            table_of_variables[var] = 'True'
        all_possible_truth_values = self.perm(table_of_variables, len(varying_variables))
        # Each pass will mutate one of the vaiables to its opposite. So over many passes, we will get the full complement
        for iteration in range(2 ** len(varying_variables)):
            current_truth_values = all_possible_truth_values[iteration]
            for index, var in enumerate(varying_variables):# setting the varying variables to their new values
                table_of_variables[var] = str(current_truth_values[index])
            prob = self.get_every_prob(table_of_variables)
            all_prob.extend([prob]) # prob here contains all the probabilities of our individual variables
        prob = self.val(all_prob)
        return prob

    def perm(self, tab, length):
        return list(product([True, False], repeat=length))

    def val(self, arr):
        sum = 0
        for i in arr:
            prod = 1
            for j in i:
                prod *= j
            sum += prod
        return sum

    def printGraph(self):
        for var in self.graph:
            node = self.graph[var]
            print("Node: {} Parent: {} Children: {}".format(node.name, node.parents, node.children))


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
