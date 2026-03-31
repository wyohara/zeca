from datetime import date
import sqlite3
from modulos.database.database_abs import DatabaseABS
from modulos.constantes.constante_tokenizador import ConstanteTokenizador
from modulos.tokenizador.modulos.ferramentas_tokenizador import FerramentasTokenizador


class TokenObject():
    def __init__(self, id=0, valor_token='', quantidade=0, formato='',token_fixo=0):
        self.id=id
        self.valor_token=valor_token
        self.quantidade=quantidade
        self.formato=formato
        self.token_fixo=token_fixo
    
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


class DatabaseTokens(DatabaseABS, FerramentasTokenizador):
    def __init__(self, modo_teste=False):
        '''
        Classe que controla a database de tokens
            Args:
                modo_teste: define se o banco de dados será no modo teste (em memória)
        '''
        super().__init__(modo_teste)
        self.__definir_tokens_fixos()

    def __definir_tokens_fixos(self)->int:
        TOKENS = [',', '?', '!', '{', '}', '[', ']', '(', ')', ';', '_', '/', '|', '@', '#', '\'', '’', '"', '”', '-', '—', '...', '.',# Originais (sem duplicar com os que vêm depois)
                  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',# Letras minúsculas
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',# Letras maiúsculas
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',# Números
                  '+', '-', '*', '/', '%', '**', '//', # Operadores aritméticos
                  '==', '!=', '<', '>', '<=', '>=',# Operadores de comparação
                  'and', 'or', 'not',# Operadores lógicos
                  '=', '+=', '-=', '*=', '/=', '%=', '**=', '//=',# Operadores de atribuição
                  '&', '|', '^', '~', '<<', '>>',# Operadores bitwise
                  ':', ';', '@', '$', '`', ' ',# Símbolos e pontuação (apenas os que não estão nos originais)
                  '->', ':='# Outros operadores
                ]
        tks =[]
        for tk in TOKENS:
            for form in ConstanteTokenizador.FORMATO_TEXTO.LISTA:
                if form ==ConstanteTokenizador.FORMATO_TEXTO.HEX:
                    tk = self.converter_texto_para_hex(tk)
                elif form ==ConstanteTokenizador.FORMATO_TEXTO.UTF8:
                    tk = self.converter_hex_para_texto(tk)
                tks.append((tk, 1, form, True))
        cursor = self.db.cursor()
        sql = """INSERT INTO Token (valor_token, quantidade, formato, token_fixo) VALUES (?, ?, ?, ?)
                ON CONFLICT(valor_token, formato) DO UPDATE SET
                    quantidade = 1 ;"""
        cursor.executemany(sql, tks)
        self.db.commit()

        # Obtém o último ID inserido/afetado para evitar conflito 
        cursor.execute("SELECT last_insert_rowid()")
        resposta = cursor.fetchone()[0]
        return resposta
    


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
                tokens.append(TokenObject(id=r[0], valor_token=r[1], quantidade=r[2], formato=r[3]))
            return tokens
        except sqlite3.IntegrityError:
            return None
        except ValueError:
            return -1
    
    def get_lista_valores_tokens(self, formato:str)->list[str]:
        '''
        Método que retorna uma lista de tokens do banco de dados ordenados do maior para o menor por formato

        Params:
            formato: formato hex ou utf-8
        Return:
            list[str]: lista de tokens ordenados do maior para o menor
        '''
        lista_tokens = []
        
        if formato not in ConstanteTokenizador.FORMATO_TEXTO.LISTA:
            return -1
        else:
            cursor = self.db.cursor()
            cursor.execute("SELECT valor_token FROM Token WHERE formato=? ORDER BY LENGTH(valor_token) DESC;", (formato,))
            resultado = cursor.fetchall()
            cursor.close()

            for r in resultado:
                lista_tokens.append(r[0])
            return lista_tokens

    
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


    def inserir_tokens(self, lista_tokens:list[TokenObject], tam_bloco=1000):
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
                INSERT INTO Token (valor_token, quantidade, formato, token_fixo) 
                VALUES (?, ?, ?, ?)
                ON CONFLICT(valor_token, formato) DO UPDATE SET
                    quantidade = quantidade + ? 
                WHERE formato=?
            """
            
            for i in range(0, len(lista_tokens), tam_bloco):
                bloco = lista_tokens[i:i + tam_bloco]
                dados_bloco = []
                
                for tk in bloco:
                    
                    if tk.validar_formato() and tk.validar_quantidade() and tk.validar_valor_token():
                        dados_bloco.append((
                            tk.valor_token,
                            tk.quantidade,
                            tk.formato,
                            tk.token_fixo,
                            tk.quantidade,
                            tk.formato
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

