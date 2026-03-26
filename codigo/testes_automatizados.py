from teste_e_relatorios.database.teste_database import TesteDatabase
from teste_e_relatorios.tokenizador.testes_processamento_trie import teste_processamento_trie
from teste_e_relatorios.database.teste_database import teste_processamento_texto_db


if __name__ == "__main__":
    #teste_database = TesteDatabase()
    #teste_database.teste_database_arquivosTexto()
    #teste_database.teste_database_tokenizador()
    teste_processamento_texto_db()
    teste_processamento_trie()