import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()
# Import data
mydata = pd.read_csv("dataset.csv")

class CreateNeuron():
    def __init__(self, numOfNeurons, numPerNeuron):
        self.synapticWeights = 2 * np.random.random((numPerNeuron, numOfNeurons)) - 1

class ANN():
    def __init__(self, hiddenLayer, outputLayer):
        self.hiddenLayer = hiddenLayer
        self.outputLayer = outputLayer
        
    def sigmoid (self, x): 
        return 1/(1 + np.exp(-x))      # activation function

    def sigmoid_(self, x): 
        return x * (1 - x)

    def trainNetwork(self, trainX, trainY, iterations):
        for i in range(0, iterations):
            hiddenLayerOutput, outputLayerOutput = self.evaluate(trainX)

            # Calculate error to groud truth
            outputLayerError = trainY - outputLayerOutput
            # How far it is off
            outputLayerDelta = outputLayerError * self.sigmoid_(outputLayerOutput)
            
            # Calculate the error to the groud truth of the hidden layer
            hiddenLayerError = outputLayerDelta.dot(self.outputLayer.synapticWeights.T)
            hiddenLayerDelta = hiddenLayerError * self.sigmoid_(hiddenLayerOutput)

            # Work out adjustment for the weights
            hiddenLayerAdjustment = trainX.T.dot(hiddenLayerDelta)
            outputLayerAdjustment = hiddenLayerOutput.T.dot(outputLayerDelta)

            # Change the weightings
            self.hiddenLayer.synapticWeights += hiddenLayerAdjustment
            self.outputLayer.synapticWeights += outputLayerAdjustment

    def evaluate(self, inputs):
        hiddenLayerOutput = self.sigmoid(np.dot(inputs, self.hiddenLayer.synapticWeights))
        outputLayerOutput = self.sigmoid(np.dot(hiddenLayerOutput, self.outputLayer.synapticWeights))

        return hiddenLayerOutput, outputLayerOutput
    
    def showWeights(self):
        print "Hidden Layer Weights:"
        print self.hiddenLayer.synapticWeights
        print "Output Layer Weights:"
        print self.outputLayer.synapticWeights

def cleandata(mydata):
    trainX = mydata.sample(frac=0.9)
    testX = mydata.drop(trainX.index)
    trainY = []
    testY = []

    for type in trainX.Class:
        if type == "Diabetes":
            trainY.append([1])
        elif type == "DR":
            trainY.append([0])

    for type in testX.Class:
        if type == "Diabetes":
            testY.append([1])
        elif type == "DR":
            testY.append([0])

    trainY = np.array(trainY)
    testY  = np.array(testY)

    trainX = trainX.drop("Class", axis=1) # Remove the identifying class
    trainX = np.array((trainX-trainX.min())/(trainX.max()-trainX.min())) # Normalize to 0 
    testX  = testX.drop("Class", axis=1) # Remove the identifying class
    testX  = np.array((testX-testX.min())/(testX.max()-testX.min())) # Normalize to 0 

    return trainX, trainY, testX, testY


def visualise_data(mydata):
    # Visualise data

    print mydata.describe()
    print ("Empty values: {}.".format(mydata.isnull().values.any()))

    diabetes   = mydata[mydata.Class == "Diabetes"]
    nodiabetes = mydata[mydata.Class == "DR"] 

    data = [diabetes.PressureA, nodiabetes.PressureA]

    plt.figure()
    ax1 = plt.subplot(121)
    plt.boxplot(data, labels = ["Diabetes", "No Diabetes"])


    ax2 = plt.subplot(122)
    pt = sns.kdeplot(diabetes.Tortuosity, shade=True, label="Diabetes")
    pt = sns.kdeplot(nodiabetes.Tortuosity, shade=True, label="No Diabetes")

    plt.show()
    print mydata


if __name__ == "__main__":

    #Init
    np.random.seed(1)

    print "Initialising"
    hiddenLayer = CreateNeuron(2, 10)
    outputLayer = CreateNeuron(1, 2)

    neuralNetwork = ANN(hiddenLayer, outputLayer)
    
    neuralNetwork.showWeights()

    trainX, trainY, testX, testY = cleandata(mydata)

    print "Training"

    neuralNetwork.trainNetwork(trainX, trainY, 60000)

    neuralNetwork.showWeights()

    print "Testing: "

    hiddenData, outputData = neuralNetwork.evaluate(testX)
    print testY
    for i in outputData:
        print "%.15f" % i[0]

