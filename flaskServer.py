import math
from pomegranate import *
import flask

def bayesianNetwork(gotPerformance,gotLearnerState):
        performance = DiscreteDistribution({'Poor': 1. / 5, 'Moderate': 1. / 5, 'Good': 1. / 5, 'VeryGood': 1. / 5,
                                    'Excellent': 1. / 5})
        learnerState = ConditionalProbabilityTable(
            [['Poor', 'Beginner', 0.80],
             ['Poor', 'Intermediate', 0.15],
             ['Poor', 'Expert', 0.05],
             ['Moderate', 'Beginner', 0.65],
             ['Moderate', 'Intermediate', 0.30],
             ['Moderate', 'Expert', 0.05],
             ['Good', 'Beginner', 0.35],
             ['Good', 'Intermediate', 0.55],
             ['Good', 'Expert', 0.10],
             ['VeryGood', 'Beginner', 0.15],
             ['VeryGood', 'Intermediate', 0.50],
             ['VeryGood', 'Expert', 0.35],
             ['Excellent', 'Beginner', 0.15],
             ['Excellent', 'Intermediate', 0.35],
             ['Excellent', 'Expert', 0.60]], [performance])
        contentComplexity = ConditionalProbabilityTable(
            [['Poor', 'Beginner', 'Low', 0.86],
             ['Poor', 'Beginner', 'Medium', 0.11],
             ['Poor', 'Beginner', 'High', 0.03],
             ['Poor', 'Intermediate', 'Low', 0.82],
             ['Poor', 'Intermediate', 'Medium', 0.14],
             ['Poor', 'Intermediate', 'High', 0.04],
             ['Poor', 'Expert', 'Low', 0.76],
             ['Poor', 'Expert', 'Medium', 0.18],
             ['Poor', 'Expert', 'High', 0.06],
             ['Moderate', 'Beginner', 'Low', 0.61],
             ['Moderate', 'Beginner', 'Medium', 0.29],
             ['Moderate', 'Beginner', 'High', 0.10],
             ['Moderate', 'Intermediate', 'Low', 0.52],
             ['Moderate', 'Intermediate', 'Medium', 0.36],
             ['Moderate', 'Intermediate', 'High', 0.12],
             ['Moderate', 'Expert', 'Low', 0.42],
             ['Moderate', 'Expert', 'Medium', 0.44],
             ['Moderate', 'Expert', 'High', 0.14],
             ['Good', 'Beginner', 'Low', 0.21],
             ['Good', 'Beginner', 'Medium', 0.61],
             ['Good', 'Beginner', 'High', 0.18],
             ['Good', 'Intermediate', 'Low', 0.10],
             ['Good', 'Intermediate', 'Medium', 0.70],
             ['Good', 'Intermediate', 'High', 0.20],
             ['Good', 'Expert', 'Low', 0.10],
             ['Good', 'Expert', 'Medium', 0.65],
             ['Good', 'Expert', 'High', 0.25],
             ['VeryGood', 'Beginner', 'Low', 0.08],
             ['VeryGood', 'Beginner', 'Medium', 0.56],
             ['VeryGood', 'Beginner', 'High', 0.36],
             ['VeryGood', 'Intermediate', 'Low', 0.07],
             ['VeryGood', 'Intermediate', 'Medium', 0.51],
             ['VeryGood', 'Intermediate', 'High', 0.42],
             ['VeryGood', 'Expert', 'Low', 0.06],
             ['VeryGood', 'Expert', 'Medium', 0.44],
             ['VeryGood', 'Expert', 'High', 0.50],
             ['Excellent', 'Beginner', 'Low', 0.04],
             ['Excellent', 'Beginner', 'Medium', 0.28],
             ['Excellent', 'Beginner', 'High', 0.68],
             ['Excellent', 'Intermediate', 'Low', 0.03],
             ['Excellent', 'Intermediate', 'Medium', 0.19],
             ['Excellent', 'Intermediate', 'High', 0.78],
             ['Excellent', 'Expert', 'Low', 0.03],
             ['Excellent', 'Expert', 'Medium', 0.10],
             ['Excellent', 'Expert', 'High', 0.87]], [performance, learnerState])

        d1 = State(performance, name="performance")
        d2 = State(learnerState, name="learnerState")
        d3 = State(contentComplexity, name="contentComplexity")

        # Building the Bayesian Network
        network = BayesianNetwork("Learner Classifier With Bayesian Networks")
        network.add_states(d1, d2, d3)
        network.add_edge(d1, d3)
        network.add_edge(d1, d2)
        network.add_edge(d2, d3)
        network.bake()

        if(gotLearnerState=='N/A'):
                #beliefs = network.predict_proba({'performance' : gotPerformance})
                #beliefs = map(str, beliefs)
                #result = ("n".join( "{}t{}".format( state.name, str(belief) ) for state, belief in zip( network.states, beliefs )))
                result = network.predict([[gotPerformance,None,None]])
        else:
                beliefs = network.predict_proba({'learnerState' : gotLearnerState, 'performance' : gotPerformance})
                beliefs = map(str, beliefs)
                result = network.predict([[gotPerformance,gotLearnerState,None]])
      
        return result

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_request():
        userPerformance = (flask.request.form['performance'])
        learnerState = (flask.request.form['learnerState'])
        result = bayesianNetwork(userPerformance,learnerState)
        print(result[0][2])
        contentComplexity = result[0][2]
        
        return contentComplexity

app.run(host="0.0.0.0", port=5000, debug=True)


