import unittest
from modulos.database.db_tokens import DatabaseTokens, TokenObject
from modulos.database.database_abs import DatabaseABS

class TesteDatabaseTokens(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
    
    def setUp(self):
        "Configurando o ambiente de teste"
        self.CLASSE_TESTADA = DatabaseTokens(modo_teste=True)        
        self.CLASSE_TESTADA.inserir_tokens([TokenObject(valor_token='tk1', quantidade=10, formato='utf-8'),
                                            TokenObject(valor_token='tk2', quantidade=2, formato='utf-8')])

   
    def tearDown(self):
        "Resetando o teste antes de cada testagem"
        DatabaseABS._db_instance = None
    
    def teste_1(self):
        'Inserindo lista de tokens válida'
        resultado = self.CLASSE_TESTADA.inserir_tokens([TokenObject(valor_token='tk3', quantidade=1, formato='utf-8')])
        self.assertEqual(resultado, 3)
    
    def teste_2(self):
        'Inserindo token que existe e incrementando a quantidade'        
        resultado = self.CLASSE_TESTADA.inserir_tokens([TokenObject(valor_token='tk1', quantidade=10, formato='utf-8')])
        busca = self.CLASSE_TESTADA.get_token('tk1')
        self.assertEqual(resultado,2)
        self.assertEqual(busca.quantidade, 20)

    
    def teste_3(self):
        'Inserindo token fora da lista'
        resultado = self.CLASSE_TESTADA.inserir_tokens(TokenObject(valor_token='tk3', quantidade=1, formato='utf-8'))
        self.assertEqual(resultado, -1)
    
    def teste_4(self):
        'Inserindo token com valor vazio'
        resultado = self.CLASSE_TESTADA.inserir_tokens(TokenObject(valor_token='', quantidade=1, formato='utf-8'))
        self.assertEqual(resultado, -1)
    
    def teste_5(self):
        'Inserindo token com quantidade vazia'
        resultado = self.CLASSE_TESTADA.inserir_tokens(TokenObject(valor_token='tk3', quantidade=0, formato='utf-8'))
        self.assertEqual(resultado, -1)

    def teste_6(self):
        'Inserindo token com quantidade vazia'
        resultado = self.CLASSE_TESTADA.inserir_tokens(TokenObject(valor_token='tk3', quantidade=0, formato='utf-8'))
        self.assertEqual(resultado, -1)
    
    def teste_7(self):
        'Recuperando lista de tokens'
        resultado = self.CLASSE_TESTADA.get_tokenObjects(formato='utf-8', quantidade=2)
        self.assertEqual(len(resultado),2 )
        self.assertEqual(resultado[0].valor_token, 'tk1')
        self.assertEqual(resultado[1].valor_token, 'tk2')

    def teste_7(self):
        'Recuperando lista de tokens sem formato'
        resultado = self.CLASSE_TESTADA.get_tokenObjects(formato='', quantidade=2)
        self.assertEqual(resultado, -1)

    def teste_8(self):
        'Recuperando lista de tokens sem quantidade'
        resultado = self.CLASSE_TESTADA.get_tokenObjects(formato='utf-8', quantidade=0)
        self.assertEqual(resultado, -1)
    
    def teste_8(self):
        'Recuperando lista de tokens com formato desconhecido'
        resultado = self.CLASSE_TESTADA.get_tokenObjects(formato='utf', quantidade=10)
        self.assertEqual(resultado, [])