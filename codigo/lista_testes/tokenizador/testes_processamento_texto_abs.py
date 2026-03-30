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
from modulos.tokenizador.modulos.processamento_textos_abs import ProcessamentoDeTextoABS


class ModeloConcretoTeste(ProcessamentoDeTextoABS):
    def __init__(self, modo_teste=True):
        super().__init__(modo_teste)

    def _recortar_tokens(self, formato, texto):
        return [TokenObject(0, 'tk1', 10, 'utf-8'),TokenObject(0, 'tk2', 10, 'utf-8')]



class TesteProcessamentoTextoABS(unittest.TestCase):
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
                self.CLASSE_TESTADA = ModeloConcretoTeste(modo_teste=True)
        
        # Substitui o caminho do dataset - sempre a classe original no caso a abstrata
        self.CLASSE_TESTADA._ProcessamentoDeTextoABS__dataset = self.dataset_dir
        self.CLASSE_TESTADA._modelo_processamento = "abs"

        self.CLASSE_TESTADA._db_textos.set_arquivo_processado(ArquivoTextoObject(0,'texto1.txt','','trie'))
    
    def tearDown(self):
        """Limpa o ambiente após cada teste"""
        shutil.rmtree(self.temp_dir)
    

    def teste_1(self):
        """Testa se a classe inicializa corretamente em modo teste"""
        self.assertIsNotNone(self.CLASSE_TESTADA)

    def teste_2(self):
        """Testa se a lista de textos é obtida corretamente"""
        lista_textos = self.CLASSE_TESTADA._ProcessamentoDeTextoABS__get_lista_textos()
        self.assertEqual(len(lista_textos), 2)
        self.assertEqual(lista_textos[0][1], "texto1.txt")
        self.assertEqual(lista_textos[1][1], "texto2.txt")
        
        self.assertEqual(lista_textos[0][0], self.dataset_dir / "texto1.txt")
        self.assertEqual(lista_textos[1][0], self.dataset_dir / "texto2.txt")
    
    def teste_3(self):
        """Checa se o texto selecionado já foi processado"""
        res = self.CLASSE_TESTADA._ProcessamentoDeTextoABS__is_texto_processado('texto1.txt', 'trie')
        self.assertEqual(res, True)

    def teste_4(self):
        """Checa se o texto selecionado já foi processado em outro modelo não usado"""
        res = self.CLASSE_TESTADA._ProcessamentoDeTextoABS__is_texto_processado('texto1.txt', 'hex')
        self.assertEqual(res, False)
    
    def teste_5(self):
        """Verifica se o método abstrato _recortar_tokens retorna o valor esperado """
        res = self.CLASSE_TESTADA._recortar_tokens('texto1.txt', 'hex')
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].valor_token, 'tk1')
        self.assertEqual(res[1].valor_token, 'tk2')

    def teste_6(self):
        """Testa erro no caso de não encontrar a pasta de arquivos de texto """
        dataset_dir = Path(self.temp_dir) / "dataset_test_erro"
        self.CLASSE_TESTADA._ProcessamentoDeTextoABS__dataset = dataset_dir
        lista_textos = self.CLASSE_TESTADA._ProcessamentoDeTextoABS__get_lista_textos()
        self.assertEqual(lista_textos, [])

    def teste_7(self):
        "Testa se ocorre erro ao tentar processar o dataset no formato errado"
        with self.assertRaises(ValueError):
            self.CLASSE_TESTADA.processar_dataset_textos(formato='hx', status=True)
    
    def teste_8(self):
        "Testa se processa em utf-8"
        res = self.CLASSE_TESTADA.processar_dataset_textos(formato='utf-8', status=True)
        self.assertEqual(res, True)

    def teste_9(self):
        "Testa se processa em hex"
        res = self.CLASSE_TESTADA.processar_dataset_textos(formato='hex', status=True)
        self.assertEqual(res, True)
        
        