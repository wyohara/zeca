import unittest
from modulos.database.db_tokens import DatabaseTokens, TokenObject
from modulos.database.database_abs import DatabaseABS
from modulos.tokenizador.modulos.ferramentas_tokenizador import FerramentasTokenizador as ft

class TesteDatabaseTokens(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
    
    def setUp(self):
        "Configurando o ambiente de teste"
        self.CLASSE_TESTADA = DatabaseTokens(modo_teste=True)        
        self.CLASSE_TESTADA.inserir_tokens([TokenObject(valor_token='tk1', quantidade=10),
                                            TokenObject(valor_token='tk2', quantidade=2)])

   
    def tearDown(self):
        "Resetando o teste antes de cada testagem"
        DatabaseABS._db_instance = None
    
    
    def teste_1(self):
        'Inserindo lista de tokens válida - sem tokens fixos'
        resultado = self.CLASSE_TESTADA.inserir_tokens([TokenObject(valor_token='tk3', quantidade=1)])
        self.assertGreaterEqual(resultado, 3)
    
    def teste_2(self):
        'Inserindo token que existe - incrementando a quantidade'        
        resultado = self.CLASSE_TESTADA.inserir_tokens([TokenObject(valor_token='tk1', quantidade=10)])
        busca = self.CLASSE_TESTADA.get_token('tk1')
        
        self.assertGreaterEqual(resultado,2)
        self.assertEqual(busca.quantidade, 20)
    
    def teste_3(self):
        'Inserindo token com valor vazio'
        with self.assertRaises(ValueError):
            resultado = self.CLASSE_TESTADA.inserir_tokens([TokenObject(valor_token='', quantidade=1)])
    
    def teste_4(self):
        'Inserindo token com quantidade vazia'
        with self.assertRaises(ValueError):
            resultado = self.CLASSE_TESTADA.inserir_tokens([TokenObject(valor_token='tk3', quantidade=0)])
    
    def teste_5(self):
        'Recuperando lista de tokens'
        resultado = self.CLASSE_TESTADA.get_tokenObjects(quantidade=2)
        self.assertEqual(len(resultado),2 )
        self.assertEqual(resultado[0].valor_token, ft.texto_para_hex('tk1'))
        self.assertEqual(resultado[1].valor_token, ft.texto_para_hex('tk2'))

    def teste_6(self):
        'Recuperando lista de tokens sem quantidade'
        resultado = self.CLASSE_TESTADA.get_tokenObjects( quantidade=0)
        self.assertEqual(resultado, [])

    def teste_7(self):
        'Recuperando os tokens fixos'
        resultado = self.CLASSE_TESTADA.get_tokens_fixos()
        self.assertEqual(len(resultado), 119)
    
    def teste_8(self):
        'Recuperando lista de todos os tokens somente com os valores'
        resultado = self.CLASSE_TESTADA.get_lista_valores()
        self.assertEqual(len(resultado), 2)

    def teste_9(self):
        'Recuperando token pelo valor'
        resultado = self.CLASSE_TESTADA.get_token('tk1')
        self.assertEqual(resultado.valor_token, ft.texto_para_hex('tk1'))
    
    def teste_10(self):
        'Recuperando token pelo valor porém vazio'
        with self.assertRaises(ValueError):
            resultado = self.CLASSE_TESTADA.get_token(None)