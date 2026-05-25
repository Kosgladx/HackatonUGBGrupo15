import keyboard
import mouse
import pyperclip
import time
import database

connection, cursor = database.connect_to_database()

def listar_telefones_grupos(cursor):
    grupos = database.execute_query(cursor, "SELECT id,monitor FROM grupos WHERE monitor IS NOT NULL AND id != 0")
    alunos = [[] for _ in range(len(grupos))]
    for i, grupo in enumerate(grupos):
        grupo_alunos = database.execute_query(cursor, "SELECT telefone FROM alunos WHERE grupo = %s", (grupo[0],))
        alunos[i] = grupo_alunos + [grupo[1]]
    return alunos


def listar_telefones(cursor):
    return database.execute_query(cursor, "SELECT telefone FROM alunos ") + database.execute_query(cursor, "SELECT telefone FROM monitores ")



def formatar_numero_txt():
    mouse.move(0,0)
    time.sleep(0.2)
    mouse.click('left')
    time.sleep(0.5)
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.2)
    keyboard.press_and_release('ctrl+c')    
    time.sleep(0.5)#0.2 para 0.5
    txt = pyperclip.paste()
    time.sleep(0.5)#0.2 para 0.5
   # mouse.move(310, 365)#descelecionar parte aparentemente totalmente desnecessária
   # time.sleep(0.2)
   # mouse.click('left')
   # time.sleep(0.2)
   # mouse.move(0,0)
   # time.sleep(0.2)
   # mouse.click("left")
   # time.sleep(0.1)
    #print(txt)
    #input('pare')

    txt = txt.split('Novo contato')
    txt = txt[1].split('\n')
    txt = txt[5]
    #print(txt)
    if txt[-1] =='\r':
        txt = txt[:-1]
    return txt
 
def analizar_tela(): # Analiza a tela do whatsapp para determinar o caso
#Os casos são 1,2,3 e 4.
#O caso 1 quer dizer que você não precisa clicar e pode trocar para o próximo.
#O caso 2 quer dizer que a conta não existe no whatsapp, logo o número é inválido.
#O caso 3 quer dizer que o número é válido mas você não o tem adicionado, o que não é um problema.
#O caso 4 é não ter nenhuma mensagem, nesse caso ou o número é inválido, ou a pessoa colocou o +55 (código do país)
    
    caso1 = "Esse número de telefone já está na sua lista de contatos. "

    caso2 ="""Esse número de telefone não está no WhatsApp. Use seu dispositivo principal para enviar um convite."""

    caso3 = """Esse número de telefone já está no WhatsApp."""

    
    mouse.move(0,0)
    time.sleep(0.2)
    mouse.click('left')
    time.sleep(0.2)
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.2)
    keyboard.press_and_release('ctrl+c')    
    time.sleep(0.4)#0.2 para 0.4
    txt = pyperclip.paste()
    time.sleep(0.4)#0.2 para 0.4
    #print(txt)
    if caso1 in txt:
        return 1
    elif caso2 in txt:
        return 2
    elif caso3 in txt:
        return 3
    else:
        return 4
    
def analizar_numero(numero): # analiza um número individual, aqui vai o texto do número
                     #Se o Caso 2 ocorrer, é enviado ao banco o número da pessoa cujo número é inválido.

                     #Se o Caso 4 ocorrer o programa clica denovo no número aperta home, espera um tempo aperto 2 right_arrow e 2 backspace e depois analiza novamente
                     #Caso o erro 4 ou o erro 2 se repita, o número é inválido e será enviado para o banco.
    envio = {'numero':'','estado':''} # o número é o número após ser colocano no whatsapp e o estado contem o estado que vai em analizar_telefones ou seja, valido,invalido
    numero = numero
    mouse.move(310, 365)
    time.sleep(0.2)
    mouse.click('left')
    time.sleep(0.2)
    pyperclip.copy(numero)
    time.sleep(0.2)
    keyboard.press_and_release('ctrl+a')
    time.sleep(0.2)
    keyboard.press_and_release('backspace') # remove qualquer campo que esteja faltando
    time.sleep(0.2)
    keyboard.press_and_release('ctrl+v') # coloca o número no campo
    time.sleep(0.2)
    numero_definitivo = formatar_numero_txt()# número que será enviado como resposta
    time.sleep(0.2)
    #print(numero_definitivo)
    #input('1')
    resposta = analizar_tela() # Recebe 1 dos casos
    #print(resposta)
    if resposta == 1:
        envio['numero'] = numero_definitivo
        envio['estado'] = 'valido'
        return envio
    
    if resposta == 2:
        envio['numero'] = numero_definitivo
        envio['estado'] = 'invalido'
        return envio

    if resposta == 3:
        envio['numero'] = numero_definitivo
        envio['estado'] = 'valido'
        return envio

    if resposta == 4:
        mouse.move(310, 365)
        time.sleep(0.2)
        mouse.click('left')
        time.sleep(0.2)
        keyboard.press_and_release('home')
        time.sleep(0.5)
        keyboard.press_and_release('right_arrow')
        time.sleep(0.1)
        keyboard.press_and_release('right_arrow')
        time.sleep(0.1)
        keyboard.press_and_release('backspace')
        time.sleep(0.1)
        keyboard.press_and_release('backspace')
        time.sleep(0.2)
        numero_definitivo = formatar_numero_txt()# número que será enviado como resposta
        time.sleep(0.2)
        
        resposta_definitiva = analizar_tela()
        if resposta_definitiva == 2 or resposta_definitiva == 4:
            envio['numero'] = numero_definitivo
            envio['estado'] = 'invalido'
            return envio
        else:
            envio['numero'] = numero_definitivo
            envio['estado'] = 'valido'
            return envio
        
def analizar_telefones(telefones): # todo o processo de análise dos números, recebe uma lista de telefones
    telefones = telefones
    numeros = {} # onde ficam guardados todos os números de whatsapp
    retorno = {'validos':{},'repetidos':{},'invalidos':{}}
    for numero in telefones:
        recebimento = analizar_numero(numero) # envia um dos números para análize e recebe o número com o estado
        if recebimento['estado'] == 'invalido':
            if recebimento['numero'] not in retorno['invalidos']:
              retorno['invalidos'][recebimento['numero']]  = 1
            else:
              retorno['invalidos'][recebimento['numero']]  = retorno['invalidos'][recebimento['numero']] +1
        else:
            if recebimento['numero'] not in numeros:
                numeros[recebimento['numero']] = 1
            else:
                numeros[recebimento['numero']] = numeros[recebimento['numero']]+1

    for valores_finais in numeros: #Entre todos os números busca por duplicatas e as separa dos números válidos.
     #print(numeros)
     #print(valores_finais)
     #print(type(numeros))
     #print(retorno)
     #print(type(numeros[valores_finais]))

     if numeros[valores_finais] == 1:

         retorno['validos'][valores_finais] = 1


     else:

        if valores_finais not in retorno['repetidos']:
            
            retorno['repetidos'][valores_finais] = numeros[valores_finais] # aqui se coloca quantas vezes aquele número apareceu
            
        else:
            retorno['repetidos'][valores_finais] = retorno['repetidos'][valores_finais] + 1 # Pensando bem eu acho que isso nunca vai acontecer com essa lógica, mas vou deixar aqui assim mesmo.
            
    return retorno



telefones = listar_telefones(cursor)
temp = []
for i in telefones:
    temp.append(i[0])
telefones = temp.copy()

print(telefones)

print('abra o whatsapp, clique em novo contato, abra um grupo ao lado ou converça com alguém e clique na parte superior para aparecerem os detalhes')
print('após isso aperte insert para iniciar')
keyboard.wait('insert') # Aqui se inicia a validação dos números

dados_numeros = analizar_telefones(telefones)

for d in dados_numeros['invalidos']: # Envio dos telefones inválidos
    telefone_final = ""
    for formatar in d:
        if formatar in '0123456789':
            telefone_final+formatar
    formatar = telefone_final
    database.adicionar_semwhats(connection, cursor, formatar)

for r in dados_numeros['repetidos']: # Envio dos telefones repetidos
    telefone_final = ""
    for formatar in r:
        if formatar in '0123456789':
            telefone_final+formatar
    formatar = telefone_final
    database.adicionar_semwhats(connection, cursor, formatar)

    
print(dados_numeros) # dados_numeros contém todos os números válidos, repetidos e inválidos separados.
mouse.move(88, 61)
time.sleep(0.2)
mouse.click('left')
mouse.move(205, 193)
time.sleep(0.2)
mouse.click('left')

#dados números enviado para o banco de dados
#Para enviar os telefones para o banco tem que se retirar os ' ' e o'-', no caso retirar todo e qualquer catacter.

for i in dados_numeros['validos']: # Inserindo os números de telefone no grupo principal
    pyperclip.copy(i)
    time.sleep(0.2)
    keyboard.press_and_release('ctrl+v')
    time.sleep(1)
    keyboard.press_and_release('enter')
    time.sleep(1)
    
    
mouse.move(246, 667) # Indo para próxima etapa
time.sleep(0.2)
mouse.click('left')    
time.sleep(0.2)# Vai para a tela com o nome do grupo
x = open('configurar.txt','r',encoding='utf-8')
dados = x.read() # Buscando o arquivo com as configurações do usuário.
x.close()
dados = eval(dados)
pyperclip.copy(dados['nome_grupo_geral'])
time.sleep(0.2)
keyboard.press_and_release('ctrl+v') # Escrevendo o nome do grupo no grupo
time.sleep(0.2)

mouse.move(234, 518)#Tela de permição dos grupos
time.sleep(0.2)
mouse.click('left')
time.sleep(1)

mouse.move(392, 165)#Desativar edição de elementos do grupo
time.sleep(0.2)
mouse.click('left')
time.sleep(1)

mouse.move(395, 381)#Desativar autoridade para convidar novos membros
time.sleep(0.2)
mouse.click('left')
time.sleep(1)

mouse.move(92, 64)#Voltar para a tela de nomear o grupo
time.sleep(0.2)
mouse.click('left')
time.sleep(5)

mouse.move(256, 614)#Criar o Grupo Central
time.sleep(0.2)
mouse.click('left')
time.sleep(10)

input('Ponto do fim da funcionalidade')
#grupos = telefones =listar_telefones_grupos(cursor) #recebe os dados dos grupos (números) para fazer o mesmo processo que o feito acima porém com modificações no nome do grupo
#for g in grupos:
