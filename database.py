#import psycopg2
import database
import random
x = open('Hackathon - Respostas ao formulário 1.csv','r',encoding='utf-8')
z = x.read()
x.close()
z = z.split('\n')
for i in range(0,5):
    z.pop(0)

lideres = []# tem email,nome,matrícula,telefone,periodo,matriculalider,senha
Alunos_Comuns = []# tem email,nome,matrícula,telefone,periodo,matriculalider,senha
Sem_Grupo = []# tem email,nome,matrícula,telefone,periodo
Monitores = []

connection, cursor = database.connect_to_database()

for i in z:
    temp = i.split(',')
    if len(temp)== 9:# o 1 adicional é a data do registro no temp[0]
        #print('comum')
        if temp[6] == "Sim (Sou líder do grupo)":
            telefone = temp[4]
            telefone_final = '' 
            for i in telefone:
             if i not in '0123456789':
                 pass
             else:
                 telefone_final = telefone_final + i
                
            lideres.append({'email':temp[1],'nome':temp[2],'matricula':temp[3],'telefone':temp[4],'periodo':temp[5],'matriculalider':temp[7],'senha':temp[8]})
        elif temp[6] == "Sim (integrante do grupo)":
            telefone = temp[4]
            telefone_final = '' 
            for i in telefone:
             if i not in '0123456789':
                 pass
             else:
                 telefone_final = telefone_final + i #alunos comuns
            Alunos_Comuns.append({'email':temp[1],'nome':temp[2],'matricula':temp[3],'telefone':temp[4],'periodo':temp[5],'matriculalider':temp[7],'senha':temp[8]})
        else:
            Sem_Grupo.append({'email':temp[1],'nome':temp[2],'matricula':temp[3],'telefone':temp[4],'periodo':temp[5],'matriculalider':0,'senha':0})
         


    else:
        pass#print('incomum',len(temp))
#[[],[],[]]


x = open('Hackathon_Monitor - Respostas ao formulário 1.csv','r',encoding='utf-8')
z = x.read()
x.close()
z = z.split('\n')
for i in range(0,1):
    z.pop(0)

#print(z)

for i in z:

    temp = i.split(',')
    temp2 = i.split(',')
    temp2.pop(0)
    temp2.pop(0)
    temp2.pop(0)
    temp2.pop(0)
    temp3 = []
    for i in temp2[0]:
        if i in '0123456789':
            temp3.append(int(i))
    telefone = temp[3]
    telefone_final = '' 
    for i in telefone:
     if i not in '0123456789':
         pass
     else:
         telefone_final = telefone_final + i
    Monitores.append({'email':temp[1],'nome':temp[2],'telefone':telefone_final,'experiencia':temp3})

#print(Monitores,Alunos_Comuns,Sem_Grupo)
#input()
for m in Monitores:
    database.adicionar_monitor(cursor, connection, m['telefone'], m['experiencia'], m['nome'], m['email'])

for a in Alunos_Comuns:
    database.adicionar_aluno(cursor, connection, a['telefone'], a['matricula'], a['nome'], a['periodo'], a['matriculalider'], a['senha'], a['email'])

for sg in Sem_Grupo:
    database.adicionar_aluno(cursor, connection, sg['telefone'], sg['matricula'], sg['nome'], sg['periodo'], sg['matriculalider'], sg['senha'], sg['email'])

def aleatorizar_lista(lista):
    lista = lista
    lista2 = []
    while len(lista)!=0:
        if len(lista) > 1:
            z = random.randint(0,len(lista)-1)
        else:
            z = 0 
        lista2.append(lista[z])
        lista.pop(z)
    lista = lista2.copy()
    return lista2
        
        
for l in lideres:
    objetivo = l['periodo']
    atingido = False
    possibilidade = False
    Monitores = aleatorizar_lista(Monitores)
    while atingido == False:
        for m in Monitores:
            if objetivo in m:
                database.adicionar_lider(cursor, connection, l['telefone'], l['matricula'], l['nome'], l['periodo'], l['matriculalider'], l['senha'], l['email'], m['telefone'])
                possibilidade = True
                atingido = True
                break

        if possibilidade == False:
            Monitores = aleatorizar_lista(Monitores)
            if len(Monitores) > 1:
                escolhido = Monitores[random.randint(0,len(Monitores)-1)]
            else:
                escolhido = Monitores[0]
            database.adicionar_lider(cursor, connection, l['telefone'], l['matricula'], l['nome'], l['periodo'], l['matriculalider'], l['senha'], l['email'], escolhido['telefone'])
            possibilidade = True
            atingido = True

           
#listaprint = database.listar_monitores(cursor)
#print(listaprint)
#listaprint = database.listar_grupos(cursor)
#print(listaprint)
#listaprint = database.listar_alunos(cursor)
#print(listaprint)
