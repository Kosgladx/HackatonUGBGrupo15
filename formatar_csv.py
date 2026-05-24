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
                
            lideres.append({'email':temp[1],'nome':temp[2],'matricula':temp[3],'telefone':temp[4],'periodo':temp[5],'matriculalider':temp[6],'senha':temp[7]})
        elif temp[6] == "Sim (integrante do grupo)":
            telefone = temp[4]
            telefone_final = '' 
            for i in telefone:
             if i not in '0123456789':
                 pass
             else:
                 telefone_final = telefone_final + i
            Alunos_Comuns.append({'email':temp[1],'nome':temp[2],'matricula':temp[3],'telefone':temp[4],'periodo':temp[5],'matriculalider':temp[6],'senha':temp[7]})
        else:
         


    else:
        pass#print('incomum',len(temp))
#[[],[],[]]
 
print(lideres)
print('\n\n\n')
print(Alunos_Comuns)


