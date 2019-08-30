import math
import np


class NeuralLayer():
    #fully connected NN Layer
    activation_function = None
    node_count = 0
    previous_layer_node_count = 0
    weights = None #list of lists

    def __init__(self, node_count, previous_layer_node_count, activation_function=sigmoid):
        self.activation_function       = activation_function
        self.node_count                = node_count
        self.previous_layer_node_count = previous_layer_node_count
        weights = np.zeros((node_count,previous_layer_node_count+1)) # +1 for bias input

    def set_weights(self,weights):
        """
            @param weights : array of weights (matriz planchada)
        """
        if len(weights) != n_rows(self.weights)*n_columns(self.weights):
            raise Exception("Input weights do not match layer weight count.")

        k = 0
        for i in range(n_rows(self.weights)):
            for j in range(n_columns(self.weights)):
                self.weights[i,j] = weight[k]
                k = k+1

    def process_inputs(self,inputs):
        if len(inputs) != self.previous_layer_node_count:
            raise Exception("Given xValues do not match layer input count.")
        bias = np.array((1,1),np.float32)
        input = np.concatenate((input,bias),axis=1) # add bias as input value
        LC = np.matmul(self.weights, inputs.transpose()).transpose()[0] # aplicacion de ponderaciones a la entrada de cada neuron
        return np.array(list(map(lambda x: self.activation_function(x),LC))) # aplicacion de la funcion de activacion

    def deep_copy(self):
        newNL = NeuralLayer(node_count = self.node_count,
                            previous_layer_node_count = self.previous_layer_node_count,
                            activation_function = self.activation_function)
        newNL.weights = np.copy(self.weights)
        return newNL

    def set_random_weights(self,min_value, max_value):
        self.weights = np.random.uniform(low=min_value,
                                         high=max_value,
                                         size=self.weights.shape)

    def get_weight_count(self):
        return n_rows(self.weights)*n_columns(self.weights)





class NeuralNetwork():
    layers = None #list
    topology = None #list
    weight_count = 0 #int

    def __init__(self,topology):
        """
         @param topology : node count on each layer. [input_layer,hide_layer_0,...,hide_layer_n,output_layer]
        """
        self.topology = topology
        self.weight_count = 0
        for l in range(1,len(topology)):
            new_layer = NeuralLayer(node_count=topology[l],
                                    previous_layer_node_count = topology[l-1])
            self.weight_count = self.weight_count + new_layer.get_weight_count()
            layers.append(new_layer)

    def process_inputs(self,inputs):
        for layer in self.layers:
            inputs = layer.process_inputs(inputs)
        return inputs

    def set_random_weights(self,min_value,max_value):
        for layer in layers:
            layer.set_random_weights(min_value,max_value)

    def get_topology_copy(self):
        newNL = NeuralNetwork(self.topology)
        for i in range(len(self.layers)):
            newNL.layers[i].activation_function = self.layers[i].activation_function
        return newNL

    def deep_copy(self):
        newNL = NeuralNetwork(self.topology)
        for i in range(len(self.layers)):
            newNL.layers[i] = self.layers[i].deep_copy()
        return newNL

    








def n_rows(mat):
    return len(mat)

def n_columns(mat):
    return len(mat[0])

def sigmoid(x):
  return 1 / (1 + math.exp(-x))
