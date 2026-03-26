import numpy as np

from modulos.embeding.modulos.tensor import Tensor
from modulos.embeding.modulos.tensor_foward import TensorFoward
from modulos.embeding.modulos.tensor_backward import TensorBackward

class Embeding():
    def __init__(self):
        super().__init__()
        
        #valores iniciais
        self.__tensor = Tensor()

        # Listas para armazenar variáveis intermediárias de cada cabeça
        self.head_out_list = []

    def foward(self, valor_entrada:np):
        return TensorFoward().foward(tensor=self.__tensor, valor_entrada=valor_entrada)
    
    def backward(self, valor_entrada:np, valor_saida:np):
        return TensorBackward().backward(self.__tensor, valor_entrada, valor_saida)

    def gerar_loss(self, valor_saida, x2_norm):
        loss = np.mean((x2_norm - valor_saida) ** 2)
        print(f"Loss inicial (num_heads={self.__tensor.num_heads}): {loss:.6f}")

