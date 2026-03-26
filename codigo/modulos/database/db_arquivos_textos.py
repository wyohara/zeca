from datetime import date
import sqlite3
from modulos.database.database_abs import DatabaseABS

class ArquivoTextoObject():
    def __init__(self, id=0, nome='', descricao='',  modelo_processamento=''):
        '''
        Classe que controla a database de arquivos processados para gerar tokens
            Args:
                modo_teste: define se o banco de dados será no modo teste (em memória)
        '''
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.modelo_processamento = modelo_processamento
    
    def __str__(self):
        return f"Arquivo de texto do tipo ArquivoTextoObject\n\t>id {self.id} - '{self.nome}' e modelo '{self.modelo_processamento}'"
    
    def validar_nome(self):
        return len(self.nome) > 0 and isinstance(self.nome, str)
    
    def validar_processamento(self):
        return len(self.modelo_processamento) > 0 and isinstance(self.modelo_processamento, str)


class DatabaseArquivosTextos(DatabaseABS):
    def __init__(self, modo_teste=False):
        super().__init__(modo_teste)

    def get_lista_nomes_arquivos_processados(self, modelo_processamento='')->list[str]:
        cursor = self.db.cursor()
        if modelo_processamento != '':
            cursor.execute("SELECT nome FROM ArquivoProcessado WHERE modelo_processamento=?", (modelo_processamento,))
        else:
            cursor.execute("SELECT nome FROM ArquivoProcessado")

        resultado = cursor.fetchall()
        cursor.close()
        nomes = []
        for r in resultado:
            nomes.append(r[0])
        return nomes
    
    def set_arquivo_processado(self, arq_texto:ArquivoTextoObject) -> int:
        '''
        Insere um arquivo de texto no banco de dados de arquivos processados.
            Args:
                arq_texto (ArquivoTextoObject): Objeto contendo os dados do arquivo a ser inserido.
                    O objeto deve conter os atributos:
                    - nome: Nome do arquivo
                    - descricao: Descrição do conteúdo
                    - modelo_processamento: Modelo utilizado no processamento
            
            Returns:
                Optional[int]: ID do registro inserido no banco de dados em caso de sucesso.
                None: se houver violação de integridade.
            
            Raises:
                sqlite3.IntegrityError: Se ocorrer um erro de banco de dados relacionado a integridade.
                ValueError: Se ocorrer um erro de integridade no objeto
        '''
        try:
            cursor = self.db.cursor()
            valores = (arq_texto.nome, arq_texto.descricao, arq_texto.modelo_processamento)
            
            # caso insira um arquivo com id ocorre erro de integridade
            if arq_texto.id >0:
                raise sqlite3.IntegrityError
            
            # validando os campos de nome e arquivo processado
            if not(arq_texto.validar_nome() and arq_texto.validar_processamento()):
                raise ValueError
                        
            sql = "INSERT INTO ArquivoProcessado (nome, descricao, modelo_processamento) VALUES (?,?,?)"
            cursor.execute(sql, valores)
            self.db.commit()
            resposta = cursor.lastrowid
            cursor.close()
            return resposta
        except sqlite3.IntegrityError:
            return 0
        except ValueError:
            return -1
        
    def get_texto_processado(self, nome, modelo_processamento) -> ArquivoTextoObject:
        '''
        Busca um arquivo de texto processado pelo nome do arquivo e método de processamento.
            Args:
                nome: Nome do arquivo
                modelo_processamento: Modelo utilizado no processamento
            
            Returns:
                Optional[ArquivoTextoObject]: Objeto contendo os dados do arquivo de texto
                None: se houver violação de integridade ou nenhum resultado.
            
            Raises:
                sqlite3.IntegrityError: Se ocorrer um erro de banco de dados relacionado a integridade.
        '''
        try:
            cursor = self.db.cursor()
            sql = "SELECT * FROM ArquivoProcessado WHERE nome=? and modelo_processamento=?"
            cursor.execute(sql, (nome,modelo_processamento))
            r = cursor.fetchone()
            cursor.close()
            if r is not None:
                resultado = ArquivoTextoObject(r[0], r[1], r[2], r[3])
                return resultado
            else:
                return None
        except sqlite3.IntegrityError:
            return None
