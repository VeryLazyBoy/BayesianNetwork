# BayesianNetwork

Bayesian networks are a type of probabilistic graphical model that uses Bayesian inference for probability computations. 
Bayesian networks aim to model conditional dependence, and therefore causation, by representing conditional dependence by edges in a directed acyclic graph. 
Through these relationships, one can efficiently conduct inference on the random variables in the graph through the use of factors.

![bn](http://zyrocks.win/images/bn.png)


In this assignment, I am required to implement a Bayesian network, given the structure in the form of
variables and dependencies. Additionally, I need to determine the joint probability given the prior and
conditional probabilities.

# Input

`structure.json`
```json
{
   "variables": {
        "Burglary": ["True","False"],
        "Earthquake": ["True","False"],
        "Alarm": ["True","False"],
        "JohnCalls": ["True","False"],
        "MaryCalls": ["True","False"]
    },
   "dependencies": {
        "Alarm": ["Burglary","Earthquake"],
        "JohnCalls": ["Alarm"],
        "MaryCalls": ["Alarm"]
    }
}
```

`values.json`
```json
{
  "prior_probabilities": {
    "Burglary": {
      "True": 0.01,
      "False": 0.99
    },
    "Earthquake": {
      "True": 0.02,
      "False": 0.98
    }
  },
  "conditional_probabilities": {
    "Alarm": [
      {
        "Burglary": "True",
        "Earthquake": "True",
        "own_value": "True",
        "probability": 0.95
      },
      {
        "Burglary": "True",
        "Earthquake": "True",
        "own_value": "False",
        "probability": 0.05
      },
      {
        "Burglary": "False",
        "Earthquake": "True",
        "own_value": "True",
        "probability": 0.29
      },
      {
        "Burglary": "False",
        "Earthquake": "True",
        "own_value": "False",
        "probability": 0.71
      },
      {
        "Burglary": "True",
        "Earthquake": "False",
        "own_value": "True",
        "probability": 0.94
      },
      {
        "Burglary": "True",
        "Earthquake": "False",
        "own_value": "False",
        "probability": 0.06
      },
      {
        "Burglary": "False",
        "Earthquake": "False",
        "own_value": "True",
        "probability": 0.001
      },
      {
        "Burglary": "False",
        "Earthquake": "False",
        "own_value": "False",
        "probability": 0.999
      }
    ],
    "JohnCalls": [
      {
        "Alarm": "True",
        "own_value": "True",
        "probability": 0.9
      },
      {
        "Alarm": "True",
        "own_value": "False",
        "probability": 0.1
      },
      {
        "Alarm": "False",
        "own_value": "True",
        "probability": 0.05
      },
      {
        "Alarm": "False",
        "own_value": "False",
        "probability": 0.95
      }
    ],
    "MaryCalls": [
      {
        "Alarm": "True",
        "own_value": "True",
        "probability": 0.7
      },
      {
        "Alarm": "True",
        "own_value": "False",
        "probability": 0.3
      },
      {
        "Alarm": "False",
        "own_value": "True",
        "probability": 0.01
      },
      {
        "Alarm": "False",
        "own_value": "False",
        "probability": 0.99
      }
    ]
  }
}

```

`qureies.json`
```json
[
  {
    "index": 1,
    "given": {
      "Alarm": "False"
    },
    "tofind": {
      "MaryCalls": "True"
    }
  },
  {
    "index": 2,
    "given": {
      "Burglary": "False",
      "Earthquake": "True"
    },
    "tofind": {
      "Alarm": "False"
    }
  }
]
```

# Output

```
[
  {
    " index ": 1,
    " answer ": 0.01
  },
  {
    " index ": 2,
    " answer ": 0.71
  }
]
```
