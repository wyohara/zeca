# test_processamento_texto.py
import unittest
from pathlib import Path
import tempfile
import shutil
from abc import ABC
import sys
from unittest.mock import MagicMock

from modulos.database.db_arquivos_textos import DatabaseArquivosTextos, ArquivoTextoObject
from modulos.database.db_tokens import DatabaseTokens,TokenObject
from modulos.tokenizador.modulos.processamento_texto_trie import ProcessamentoTextoTrie




class TesteProcessamentoTextoTrie(unittest.TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)        
        self._modelo_processamento = 'teste'
    
    def setUp(self):
        """Configura o ambiente de teste antes de cada teste"""
        # Cria diretório temporário para dataset
        self.temp_dir = tempfile.mkdtemp()
        self.dataset_dir = Path(self.temp_dir) / "dataset_test"
        self.dataset_dir.mkdir()

        # Cria arquivos de teste
        self.arquivo1 = self.dataset_dir / "texto1.txt"
        self.arquivo1.write_text("Este é um texto de teste.", encoding="utf-8")
        
        self.arquivo2 = self.dataset_dir / "texto2.txt"
        self.arquivo2.write_text("Outro texto para testar.", encoding="utf-8")

        # Mock das dependências
        self.mock_db_arquivos = MagicMock(spec=DatabaseArquivosTextos)
        self.mock_db_tokens = MagicMock(spec=DatabaseTokens)

        # Substitui as dependências
        with unittest.mock.patch('modulos.database.db_arquivos_textos.DatabaseArquivosTextos', return_value=self.mock_db_arquivos):
            with unittest.mock.patch('modulos.database.db_tokens.DatabaseTokens', return_value=self.mock_db_tokens):
                self.CLASSE_TESTADA = ProcessamentoTextoTrie(modo_teste=True)
        
        # Substitui o caminho do dataset - sempre a classe original no caso a abstrata
        self.CLASSE_TESTADA._ProcessamentoDeTextoABS__dataset = self.dataset_dir
        self.CLASSE_TESTADA._modelo_processamento = "abs"

        self.CLASSE_TESTADA._ProcessamentoDeTextoABS__db_textos.set_arquivo_processado(ArquivoTextoObject(0,'texto1.txt','','trie'))
    
    def tearDown(self):
        """Limpa o ambiente após cada teste"""
        shutil.rmtree(self.temp_dir)
    

    def teste_1(self):
        """Testa se a classe inicializa corretamente em modo teste"""
        self.assertIsNotNone(self.CLASSE_TESTADA)

    def teste_2(self):
        """Testa se o split é feito corretamente em um caso válido - UTF-8"""
        resultado = self.CLASSE_TESTADA._ProcessamentoTextoTrie__get_palavras_recortadas('casa', 'utf-8')
        self.assertEqual(resultado, ['casa'])

    def teste_3(self):
        """Testa se o split é feito corretamente em um caso válido hex"""
        resultado = self.CLASSE_TESTADA._ProcessamentoTextoTrie__get_palavras_recortadas('primeiro teste', 'hex')
        self.assertEqual(resultado, ['7072696d6569726f','7465737465'])
    
    def teste_4(self):
        """Testa se o split é feito corretamente em um caso inválido de formato"""
        with self.assertRaises(ValueError):
            self.CLASSE_TESTADA._ProcessamentoTextoTrie__get_palavras_recortadas('primeiro teste', 'utf')
    
    def teste_4(self):
        """Testa se o split é feito corretamente em um caso de texto vazio"""
        with self.assertRaises(ValueError):
            self.CLASSE_TESTADA._ProcessamentoTextoTrie__get_palavras_recortadas('', 'utf-8')
    
    def teste_5(self):
        """Testa se é criada uma árvore trie no formato válido em utf-8"""
        esperado = {'c': {'a': {'s': {'a': {'fim': 1}}}}}
        resultado = self.CLASSE_TESTADA._ProcessamentoTextoTrie__montar_arvore_trie('casa', {}, 'utf-8')
        self.assertEqual(resultado, esperado)
    
    def teste_6(self):
        """Testa se é criada uma árvore trie no formato válido com sufixo diferente em utf-8"""
        esperado = {'a': {'m': {'o': {'r': {'fim': 1}}, 'fim': 2, 'a': {'r': {'fim': 1}}}}}
        palavra = 'amor amar'
        palavras = self.CLASSE_TESTADA._ProcessamentoTextoTrie__get_palavras_recortadas(palavra, 'utf-8')
        resultado = {}
        for p in palavras:
            resultado = self.CLASSE_TESTADA._ProcessamentoTextoTrie__montar_arvore_trie(p, resultado, 'utf-8')
        self.assertEqual(resultado, esperado)
    
    def teste_7(self):
        """Testa se é criada uma árvore trie no formato válido em hex"""
        esperado = {'63': {'61': {'73': {'61': {'fim': 1}}}}}
        palavra = 'casa'
        palavras = self.CLASSE_TESTADA._ProcessamentoTextoTrie__get_palavras_recortadas(palavra, 'hex')
        resultado = {}
        for p in palavras:
            resultado = self.CLASSE_TESTADA._ProcessamentoTextoTrie__montar_arvore_trie(p, {}, 'hex')
        self.assertEqual(resultado, esperado)
    
    def teste_8(self):
        """Testa se é criada uma árvore trie no formato válido com sufixo diferente em utf-8"""
        esperado = {'61': {'6d': {'6f': {'72': {'fim': 1}}, 'fim': 2, '61': {'72': {'fim': 1}}}}}
        palavra = 'amor amar'
        palavras = self.CLASSE_TESTADA._ProcessamentoTextoTrie__get_palavras_recortadas(palavra, 'hex')
        resultado = {}
        for p in palavras:
            resultado = self.CLASSE_TESTADA._ProcessamentoTextoTrie__montar_arvore_trie(p, resultado, 'hex')
        self.assertEqual(resultado, esperado)
    
    def teste_9(self):
        """Testa se é criada uma lista de objetos validos"""
        dicionario_base = {'c': {'a': {'s': {'a': {'fim': 1}}}}}
        esperado = ['casa']
        resultado = self.CLASSE_TESTADA._ProcessamentoTextoTrie__montar_lista_tokens(dicionario_base, 'utf-8')

        for r in resultado:
            self.assertTrue(r.valor_token in esperado)
            self.assertTrue(r.quantidade > 0)
            self.assertEqual(r.formato, 'utf-8')
    
    def teste_10(self):
        """Testa se é criada uma lista de objetos validos com sufixo diferente"""
        dicionario_base = {'a': {'m': {'o': {'r': {'fim': 1}}, 'fim': 2, 'a': {'r': {'fim': 1}}}}}
        esperado = ['am', 'r', 'ar']
        resultado = self.CLASSE_TESTADA._ProcessamentoTextoTrie__montar_lista_tokens(dicionario_base, 'utf-8')
        for r in resultado:
            self.assertTrue(r.valor_token in esperado)
            self.assertTrue(r.quantidade > 0)
            self.assertEqual(r.formato, 'utf-8')
    
    