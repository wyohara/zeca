from modulos.database.db_arquivos_textos import DatabaseArquivosTextos, ArquivoTextoObject
from modulos.database.database_abs import DatabaseABS
import unittest


class TesteDatabaseArquivoTextos(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)


    def setUp(self):
        "Configurando o ambiente de teste"
        self.CLASSE_TESTADA = DatabaseArquivosTextos(modo_teste=True)

   
    def tearDown(self):
        "Resetando o teste antes de cada testagem"
        DatabaseABS._db_instance = None

    def teste_1(self):
        '''Testa se o teste iniciou corretamente'''
        self.assertIsNotNone(self.CLASSE_TESTADA)
        self.assertTrue(self.CLASSE_TESTADA._DatabaseABS__modo_teste)

    def teste_2(self):
        '''Testa se a classe insere com sucesso um objeto válido'''
        arq = ArquivoTextoObject(0,'texto_1','','trie')
        resultado = self.CLASSE_TESTADA.set_arquivo_processado(arq)
        self.assertEqual(resultado, 1)

    def teste_3(self):
        '''Testa se a classe insere com sucesso um objeto válido'''
        arq = ArquivoTextoObject(0,'texto_1','','trie')
        resultado = self.CLASSE_TESTADA.set_arquivo_processado(arq)
        self.assertEqual(resultado, 1)

    def teste_4(self):
        '''Testa se a classe não permite salvar objeto com id'''
        arq = ArquivoTextoObject(id=1,nome='texto_1',descricao='',modelo_processamento='trie')
        resultado = self.CLASSE_TESTADA.set_arquivo_processado(arq)
        self.assertEqual(resultado, 0)

    def teste_5(self):
        '''Testa se a classe não permite salvar nome vazio'''
        arq = ArquivoTextoObject(id=0,nome='',descricao='',modelo_processamento='trie')
        resultado = self.CLASSE_TESTADA.set_arquivo_processado(arq)
        self.assertEqual(resultado,-1)
    
    def teste_6(self):
        '''Testa se a classe não permite salvar nome com modelo_processamento vazio'''
        arq = ArquivoTextoObject(id=0,nome='texto_1',descricao='',modelo_processamento='')
        resultado = self.CLASSE_TESTADA.set_arquivo_processado(arq)
        self.assertEqual(resultado,-1)
    
    

    def __adicionar_valores_para_teste(self):
        arquivo_texto = [ArquivoTextoObject(id=0,nome='texto_1',modelo_processamento='trie'),
                         ArquivoTextoObject(id=0,nome='texto_2',modelo_processamento='bag')]
        for arq in arquivo_texto:
            self.CLASSE_TESTADA.set_arquivo_processado(arq)

    def teste_7(self):
        '''Testa se a classe recupera um arquivo válido'''        
        self.__adicionar_valores_para_teste()

        resultado = self.CLASSE_TESTADA.get_texto_processado(nome='texto_1', modelo_processamento='trie')
        self.assertEqual(resultado.nome, 'texto_1')
        self.assertEqual(resultado.modelo_processamento, 'trie')

    def teste_8(self):
        'Testa se a classe recupera um arquivo sem modelo de processamento'
        self.__adicionar_valores_para_teste()

        resultado = self.CLASSE_TESTADA.get_texto_processado(nome='texto_1', modelo_processamento='')
        self.assertEqual(resultado, None)
    
    def teste_9(self):
        'Testa se a classe recupera um arquivo com modelo de processamento inválido'
        self.__adicionar_valores_para_teste()

        resultado = self.CLASSE_TESTADA.get_texto_processado(nome='texto_1', modelo_processamento='tri')
        self.assertEqual(resultado, None)

    def teste_10(self):
        'Testa se a classe recupera um arquivo sem nome'
        self.__adicionar_valores_para_teste()

        resultado = self.CLASSE_TESTADA.get_texto_processado(nome='', modelo_processamento='trie')
        self.assertEqual(resultado, None)
    
    def teste_11(self):
        'Testa se a classe recupera o nome de todos os arquivos de textos'
        self.__adicionar_valores_para_teste()

        resultado = self.CLASSE_TESTADA.get_lista_nomes_arquivos_processados()
        self.assertEqual(resultado, ['texto_1', 'texto_2'])
    
    def teste_12(self):
        'Testa se a classe recupera o nome de todos os arquivos de textos com modelo "trie"'
        self.__adicionar_valores_para_teste()
        
        resultado = self.CLASSE_TESTADA.get_lista_nomes_arquivos_processados(modelo_processamento="trie")
        self.assertEqual(resultado, ['texto_1'])