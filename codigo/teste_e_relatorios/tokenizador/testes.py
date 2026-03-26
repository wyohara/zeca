from lib.database.db_arquivos_textos import DatabaseArquivosTextos, ArquivoTextoObject
from lib.database.db_tokens import DatabaseTokens, TokenObject
from lib.tokenizador.modulos import processamento_texto_trie

class TesteDatabase():

    def teste_database_arquivosTexto(self):
        db = DatabaseArquivosTextos(modo_teste=True)
        print("-----------"*10)
        print("Testando DatabaseArquivosTextos")
        print("     TESTE DE INSERÇÃO")
        print (">> Teste inserindo arquivo válido")
        resultado = db.set_arquivo_processado(ArquivoTextoObject(0,'tk1','','trie'))
        assert resultado is not None
        assert resultado > 0
        print(f' >>> OK: {resultado}')

        print (">> [erro de integridade] - inserindo arquivo com id ")
        resultado = db.set_arquivo_processado(ArquivoTextoObject(12,'tk1','','trie'))
        assert resultado is -1
        print(f' >>> OK: {resultado}')
        
        print (">> [erro de integridade] - inserindo arquivo com nome vazio ")
        resultado = db.set_arquivo_processado(ArquivoTextoObject(12,'','','trie'))
        assert resultado is -1
        print(f' >>> OK {resultado}')

        print (">> [erro de integridade] - inserindo arquivo com modo de processamento vazio ")
        resultado = db.set_arquivo_processado(ArquivoTextoObject(12,'','','trie'))
        assert resultado is -1
        print(f' >>> OK {resultado}')


        print("\n     TESTE DE SELEÇÃO")        
        print (">> Busca válida")
        resultado = db.get_texto_processado(nome='tk1', modelo_processamento='trie')
        assert resultado.nome == 'tk1'
        assert resultado.modelo_processamento == 'trie'
        print(f' >>> OK {resultado}')

        print (">> Busca sem modelo de processamento")
        resultado = db.get_texto_processado(nome='tk1', modelo_processamento='')
        assert resultado == None
        print(f' >>> OK {resultado}')

        print (">> Busca sem nome")
        resultado = db.get_texto_processado(nome='', modelo_processamento='trie')
        assert resultado == None
        print(f' >>> OK {resultado}')

        print (">> Busca inválida")
        resultado = db.get_texto_processado(nome=67, modelo_processamento=2)
        assert resultado == None
        print(f' >>> OK {resultado}')

        print (">> Buscando todos os aquivos processados")
        db.set_arquivo_processado(ArquivoTextoObject(0,'tk2','','bag'))
        resultado = db.get_lista_nomes_arquivos_processados()
        assert resultado == ['tk1','tk2']
        print(f' >>> OK {resultado}')

        print (">> Buscando todos os aquivos processados com o modelo 'bag'")
        resultado = db.get_lista_nomes_arquivos_processados(modelo_processamento='bag')
        assert resultado == ['tk2']
        print(f' >>> OK {resultado}')

    def teste_database_tokenizador(self):
        print("-----------"*10)
        print("Testando DatabaseTokens")
        db = DatabaseTokens(modo_teste=True)

        print("     TESTE DE INSERÇÃO")
        print (">> Teste inserindo lista de arquivo válido")
        resultado = db.inserir_tokens([
            TokenObject(valor_token='tk1', quantidade=1, formato='utf-8'),
            TokenObject(valor_token='tk2', quantidade=2, formato='utf-8')])
        assert resultado == 2
        print(f' >>> OK {resultado}')

        print (">> Teste inserindo token que já existe")
        resultado = db.inserir_tokens([TokenObject(0, 'tk1',100,'utf-8')])
        assert resultado == 2
        print(f' >>> OK {resultado}')

        print (">> [Erro de integridade] Teste inserindo token inválido - arquivo fora do array")
        resultado = db.inserir_tokens(TokenObject(0, 'tk2',1,'utf-8'))
        assert resultado == -1
        print(f' >>> OK {resultado}')
        
        print (">> [Erro de integridade] Teste inserindo token inválido - token vazio")
        resultado = db.inserir_tokens([TokenObject(valor_token='', quantidade=0, formato='')])
        assert resultado == -2
        print(f' >>> OK {resultado}')
        
        print (">> [Erro de integridade] Teste inserindo token inválido - token com erro no valor")
        resultado = db.inserir_tokens([TokenObject(valor_token='', quantidade=1, formato='utf-8')])
        assert resultado == -2
        print(f' >>> OK {resultado}')
        
        print (">> [Erro de integridade] Teste inserindo token inválido - token com erro na quantidade")
        resultado = db.inserir_tokens([TokenObject(valor_token='tk3', quantidade=-1, formato='utf-8')])
        assert resultado == -2
        print(f' >>> OK {resultado}')
        
        print (">> [Erro de integridade] Teste inserindo token inválido - token com erro na quantidade")
        resultado = db.inserir_tokens([TokenObject(valor_token='tk3', quantidade=-1, formato='utf-8')])
        assert resultado == -2
        print(f' >>> OK {resultado}')

        print("     TESTE DE get_tokens")
        print (">> recuperando tokens")
        resultado = db.get_tokenObjects(formato='utf-8', quantidade=10)
        assert len(resultado) == 2 and isinstance(resultado[1], TokenObject) and isinstance(resultado[0], TokenObject)
        print(f' >>> OK {resultado}')

        
        print (">> [Erro de Integridade] recuperando tokens sem formato")
        resultado = db.get_tokenObjects(formato='', quantidade=10)
        assert resultado == -1
        print(f' >>> OK {resultado}')

        print (">> [Erro de Integridade] recuperando tokens sem quantidade")
        resultado = db.get_tokenObjects(formato='', quantidade=0)
        assert resultado == -1
        print(f' >>> OK {resultado}')

        print (">> [Erro de Integridade] recuperando tokens com formato desconhecido")
        resultado = db.get_tokenObjects(formato='utf', quantidade=0)
        assert resultado == []
        print(f' >>> OK {resultado}')