from datetime import date
import sqlite3
from modulos.database.database_abs import DatabaseABS
from modulos.constantes.constante_tokenizador import ConstanteTokenizador


class TokenObject():
    def __init__(self, id=0, valor_token='', quantidade=0, formato=''):
        self.id=id
        self.valor_token=valor_token
        self.quantidade=quantidade
        self.formato=formato
    
    def __str__(self):
        return f"Arquivo de tokens tipo TokenObject\n\t>id {self.id} - '{self.valor_token}', modelo '{self.quantidade}', formato '{self.formato}'"
    
    def get_tamanho_token(self):
        return len(self.valor_token)
    
    def validar_valor_token(self):
        return len(self.valor_token)>0 and isinstance(self.valor_token, str)
    
    def validar_quantidade(self):        
        return self.quantidade>0 and isinstance(self.quantidade, int)
    
    def validar_formato(self):        
        return self.formato in ConstanteTokenizador.FORMATO_TEXTO.LISTA


class DatabaseTokens(DatabaseABS):
    def __init__(self, modo_teste=False):
        '''
        Classe que controla a database de tokens
            Args:
                modo_teste: define se o banco de dados será no modo teste (em memória)
        '''
        super().__init__(modo_teste)

    def get_tokenObjects(self, formato:str, quantidade=10000)-> list[TokenObject]:
        '''
        Recupera uma lista de tokens do banco de dados
            Args:
                formato: formato dos tokens recuperados 'hex' e 'utf-8'
                quantidade: tamanho do bloco de tokens recuperado
            
            Returns:
                list[TokenObject]: lista de tokens
                None: se houver violação de integridade.
                -1: se formato inválido
            
            Raises:
                sqlite3.IntegrityError: Se ocorrer um erro de banco de dados relacionado a integridade.
                valueError: formato ou quantidade inválidos
        '''        
        try:
            if not (len(formato)>0 and isinstance(formato, str)):
                raise ValueError
            
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM Token WHERE formato=? ORDER BY quantidade DESC LIMIT ?;", (formato, quantidade,))
            resultado = cursor.fetchall()
            cursor.close()
            tokens = []

            for r in resultado:
                tokens.append(TokenObject(id=r[0], valor=r[1], quantidade=r[2], formato=r[3]))
            return tokens
        except sqlite3.IntegrityError:
            return None
        except ValueError:
            return -1
    
    def get_token(self, valor_token:str)->TokenObject:
        '''
        Recupera uma lista de tokens do banco de dados pelo valor do token
            Args:
                valor_token: valor do token
            
            Returns:
                list[TokenObject]: lista de tokens
                None: se houver violação de integridade.
                -1: se formato inválido
            
            Raises:
                sqlite3.IntegrityError: Se ocorrer um erro de banco de dados relacionado a integridade.
                valueError: formato ou quantidade inválidos
        '''
        try:
            if not (len(valor_token)>0 and isinstance(valor_token, str)):
                raise ValueError
            
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM Token WHERE valor_token=?;", (valor_token,))
            resultado = cursor.fetchone()
            cursor.close()

            return TokenObject(id=resultado[0], valor_token=resultado[1], quantidade=resultado[2], formato=resultado[3])
        except sqlite3.IntegrityError:
            return None
        except ValueError:
            return -1


    def inserir_tokens(self, token_list:list[TokenObject], bloco=1000):
        '''
        Insere uma lista de tokens no banco de dados de arquivos processados.
            Args:
                token_list (list[TokenObject]): lista de Objetos tokens
                    O objeto deve conter os atributos:
                    - valor: Valor do token
                    - quantidade: número de ocorrencias
                    - formato: formato do token ('utf-8' ou 'hex')
                    - data_criacao: data de criação
                bloco: tamanho do bloco inserido no banco de dados. Evita sobrecarregar a memória
            
            Returns:
                Optional[int]: ID do registro inserido no banco de dados em caso de sucesso.
                None: se houver violação de integridade.
            
            Raises:
                sqlite3.IntegrityError: Se ocorrer um erro de banco de dados relacionado a integridade.
                TypeError: Se ocorrer a informação não estiver em uma lista.
                ValueError: Erro de integridade nos objetos
        '''
        try:
            cursor = self.db.cursor()
            sql = """
                INSERT INTO Token (valor_token, quantidade, formato) 
                VALUES (?, ?, ?) 
                ON CONFLICT(valor_token) DO UPDATE SET
                    quantidade = quantidade + ?;
            """
            
            for i in range(0, len(token_list), bloco):
                bloco = token_list[i:i + bloco]
                dados_bloco = []
                
                for tk in bloco:
                    
                    if tk.validar_formato() and tk.validar_quantidade() and tk.validar_valor_token():
                        dados_bloco.append((
                            tk.valor_token,
                            tk.quantidade,
                            tk.formato,
                            tk.quantidade
                        ))
                    else:
                        raise ValueError  
                cursor.executemany(sql, dados_bloco)
            self.db.commit()

            # Obtém o último ID inserido/afetado para evitar conflito 
            cursor.execute("SELECT last_insert_rowid()")
            resposta = cursor.fetchone()[0]
            return resposta
        except sqlite3.IntegrityError:
            return None
        except TypeError:
            return -1
        except ValueError:
            return -2

