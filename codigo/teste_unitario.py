from lista_testes.database.teste_database_arquivo_textos import TesteDatabaseArquivoTextos
from lista_testes.database.teste_database_tokens import TesteDatabaseTokens
from lista_testes.tokenizador.testes_processamento_texto_abs import TesteProcessamentoTextoABS
from lista_testes.tokenizador.testes_processamento_texto_trie import TesteProcessamentoTextoTrie
from lista_testes.tokenizador.teste_tokenizador import TesteTokenizador
import unittest
import sys

TESTES = [TesteDatabaseArquivoTextos, TesteDatabaseTokens, TesteProcessamentoTextoABS, 
          TesteProcessamentoTextoTrie, TesteTokenizador]


if __name__ == "__main__":
    for i, teste_suite in enumerate(TESTES):
        teste = unittest.TestLoader().loadTestsFromTestCase(teste_suite)
        
        # Executa os testes com verbosidade
        test_runner = unittest.TextTestRunner(verbosity=2)
        result = test_runner.run(teste)
        
        # Retorna código de saída apropriado
        if not result.wasSuccessful():
            sys.exit(1)
    
    sys.exit(0)