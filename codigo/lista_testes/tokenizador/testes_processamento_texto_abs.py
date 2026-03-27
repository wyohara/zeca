# test_processamento_texto.py
import unittest
from pathlib import Path
import tempfile
import shutil
from abc import ABC
import sys
from unittest.mock import MagicMock

from modulos.database.db_arquivos_textos import DatabaseArquivosTextos
from modulos.database.db_tokens import DatabaseTokens,TokenObject
from modulos.tokenizador.modulos.processamento_textos_abs import ProcessamentoDeTextoABS
from modulos.tokenizador.modulos.processamento_texto_trie import ProcessamentoTextoTrie


class ModeloConcretoTeste(ProcessamentoDeTextoABS):
    def __init__(self, modo_teste=True):
        super().__init__(modo_teste)

    def _recortar_tokens(self, formato, texto):
        return [TokenObject(0, 'tk1', 10, 'utf-8',''),TokenObject(0, 'tk2', 10, 'utf-8','')]


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
        self.CLASSE_TESTADA._modelo_processamento = "trie"
    
    def tearDown(self):
        """Limpa o ambiente após cada teste"""
        shutil.rmtree(self.temp_dir)
    

    def teste_1_deve_inicializar_com_modo_teste(self):
        """Testa se a classe inicializa corretamente em modo teste"""
        self.assertIsNotNone(self.CLASSE_TESTADA)
        self.assertTrue(self.CLASSE_TESTADA._ProcessamentoDeTextoABS__modo_teste)

    def test_2_deve_listar_textos_do_dataset(self):
        """Testa se a lista de textos é obtida corretamente"""
        lista_textos = self.CLASSE_TESTADA._ProcessamentoDeTextoABS__get_lista_textos()
        self.assertEqual(len(lista_textos), 2)
        self.assertEqual(lista_textos[0][1], "texto1.txt")
        self.assertEqual(lista_textos[1][1], "texto2.txt")
        
        self.assertEqual(lista_textos[0][0], self.dataset_dir / "texto1.txt")
        self.assertEqual(lista_textos[1][0], self.dataset_dir / "texto2.txt")