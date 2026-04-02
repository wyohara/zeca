import unittest
from unittest.mock import MagicMock

from modulos.database.db_tokens import DatabaseTokens,TokenObject
from modulos.tokenizador.modulos.tokenizador import Tokenizador


class TesteTokenizador(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)        
    
    def setUp(self):
        self.mock_db_tokens = MagicMock(spec=DatabaseTokens)
                
        with unittest.mock.patch('modulos.tokenizador.modulos.tokenizador.DatabaseTokens', return_value=self.mock_db_tokens):
            self.CLASSE_TESTADA = Tokenizador(quantidade=1000)
        self.CLASSE_TESTADA._Tokenizador__montar_tokens(quantidade=1000)
        
    
    def teste_1(self):
        """Testa se a classe inicializa corretamente em modo teste"""
        self.assertIsNotNone(self.CLASSE_TESTADA)
    
    def teste_1_2(self):
        """Testa se a classe falha em iniciar com quantidade negativa"""
        with self.assertRaises(ValueError):
            Tokenizador(quantidade=-1)
    
    def teste_1_3(self):
        """Testa se a classe inicia somente os tokens fixos com quantidade menor que os tokens fixos"""
        self.assertGreater(len(Tokenizador(quantidade=1)._Tokenizador__tokens),118)

    def teste_2(self):
        "Testa se foi definido o maior token"        
        self.assertGreater(self.CLASSE_TESTADA._Tokenizador__maior_token,0)
    
    def teste_3(self):
        'Testa se foi criado os dicionários de tokens'
        self.assertEqual(len(self.CLASSE_TESTADA._Tokenizador__rev_tokens),119)
        self.assertEqual(len(self.CLASSE_TESTADA._Tokenizador__tokens),119)
    
    def teste_4(self):
        'Testa a conversao de texto em tokens'
        res = self.CLASSE_TESTADA.transformar_texto_em_tokens('salabim')
        self.assertEqual(res,[42, 24, 35, 24, 25, 32, 36])
    
    def teste_5(self):
        'Testa a conversao de tokens para texto'
        res = self.CLASSE_TESTADA.transformar_tokens_em_texto([42, 24, 35, 24, 25, 32, 36] )
        self.assertEqual(res, ['s', 'a', 'l', 'a', 'b', 'i', 'm'])

    def teste_6(self):
        'Testa a conversao de tokens para texto concatenado.'
        res = self.CLASSE_TESTADA.transformar_tokens_em_texto([42, 24, 35, 24, 25, 32, 36] , concatenar=True)
        self.assertEqual(res, 'salabim')

