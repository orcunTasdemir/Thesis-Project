from ANN import AgentNeuralNetwork


class Agent:

    facing_directions = [0, 1, 2, 3]

    name: str = "agent"
    neuralNetwork: AgentNeuralNetwork = AgentNeuralNetwork()
    energy: float = 30.0
    age: int = 0
    x: int = None
    y: int = None
    facing_direction: int = None

    def __init__(
        self,
        name=name,
        neural_network=neuralNetwork,
        energy=energy,
        age=age,
        x=x,
        y=y,
        facing_direction=facing_direction,
    ):

        self.name = name
        self.neuralNetwork = neural_network
        self.energy = energy
        self.age = age
        self.x = x
        self.y = y
        self.facing_direction = facing_direction