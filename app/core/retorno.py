from core.models import *
from core.functions import *
from zipfile import ZipFile
import os

retornos = [
    '000026.02',
    '000025.03',
    '000035.01',
    '000026.03',
    '000025.04',
    '000027.02',
    '000021.02',
    '000028.02',
    '000036.02',
    '000016.02',
    '000015.02',
    '000022.03',
    '000024.03',
    '000067.02',
    '000026.23',
    '000064.02',
    '000015.15',
    '000014.02',
    '000013.08',
    '000076.08',
    '000024.19',
    '000029.08',
    '000019.08',
    '000041.02',
    '000058.15',
    '000027.18',
    '000049.08',
    '000035.19',
    '000036.18',
    '000066.08',
    '000025.22',
    '000063.09',
    '000015.21',
    '000103.02',
    '000094.08',
    '000055.09',
    '000030.12',
    '000069.02',
    '000024.25',
    '000029.12',
    '000076.14',
    '000019.13',
    '000013.13',
    '000035.25',
    '000024.28',
    '000025.28',
    '000066.14',
    '000063.15',
    '000064.07',
    '000049.14',
    '000044.07',
    '000094.13',
    '000015.27',
    '000055.15',
    '000012.08',
    '000030.18',
    '000014.03',
    '000038.08',
    '000087.02',
    '000024.32',
    '000013.18',
    '000076.19',
    '000056.11',
    '000019.20',
    '000034.07',
    '000011.09',
    '000017.08',
    '000018.08',
    '000012.11',
    '000094.19',
    '000055.20',
    '000015.33',
    '000038.14',
    '000056.16',
    '000013.24',
    '000076.24',
    '000019.25',
    '000017.14',
    '000034.12',
    '000018.13',
    '000011.15',
    '000036.21',
    '000081.16',
    '000075.10',
    '000053.14',
    '000066.25',
    '000028.10',
    '000063.25',
    '000064.17',
    '000049.25',
    '000062.07',
    '000057.13',
    '000052.10',
    '000042.12',
    '000097.08',
    '000093.08',
    '000050.11',
    '000683.02',
    '000015.39',
    '000055.25',
    '000014.04',
    '000069.03',
    '000076.29',
    '000013.29',
    '000056.22',
    '000019.30',
    '000038.20',
    '000054.10',
    '000034.17',
    '000017.20',
    '000011.20',
    '000018.18',
    '000086.02',
    '000010.12',
    '000036.22',
    '000053.19',
    '000075.14',
    '000049.30',
    '000092.02',
    '000066.30',
    '000028.15',
    '000070.09',
    '000064.21',
    '000062.12',
    '000052.15',
    '000083.09',
    '000050.15',
    '000055.29',
    '000012.21',
    '000087.09',
    '000061.09',
    '000015.44',
    '000013.33',
    '000067.12',
    '000056.28',
    '000076.34',
    '000038.24',
    '000098.10',
    '000054.15',
    '000084.07',
    '000039.14',
    '000018.22',
    '000034.21',
    '000017.25',
    '000011.24',
    '000033.07'
]

modelo = ''

with open('Ficha.rtf', 'r') as file:
    modelo = file.read()

medico = {
    '100': 'MARIA LUCIENE SANTOS',
    '101': 'DAULER DE SOUZA',
    '': ''
}

os.chdir('retornos')

with ZipFile('Retornos.zip', 'w') as zip:
    for entrada in retornos:
        ent = Entrada.objects.get(codmovimento=entrada)
        print(f'Retorno {entrada}, encontrado no sisac: {ent}')
        print(f'Buscar pelo paciente pelo código: {ent.codpaciente.pk}')
        pac = Cadpaciente.objects.get(codpaciente=ent.codpaciente.pk)
        print(f'Paciente encontrado: {pac}')
        texto = modelo.replace('PACIENTE', pac.paciente)
        texto = texto.replace('EMPRESA', 'HOSPITAL ONCOLOGICO DE ARACAJU')
        texto = texto.replace('SEXO', pac.sexo)
        texto = texto.replace('PROFISSAO', pac.profissao)
        texto = texto.replace('RG', pac.rg)
        texto = texto.replace('EC', pac.ec)
        texto = texto.replace('DATANASC', pac.datanasc.strftime("%d/%m/%Y"))
        texto = texto.replace('DATAENT', ent.datahoraent.strftime("%d/%m/%Y"))
        texto = texto.replace('IDADE', pac.idade)
        texto = texto.replace('PESO', pac.peso)
        texto = texto.replace('ALTURA', pac.altura)
        texto = texto.replace('TELEFONE', pac.telefone2)
        texto = texto.replace('END', pac.endereco)
        texto = texto.replace('BAIRRO', pac.bairro)
        texto = texto.replace('CIDADEPAC', pac.cidade)
        texto = texto.replace('CEP', pac.cep)
        texto = texto.replace('CODIGO', entrada)
        texto = texto.replace('MATRICULA', pac.matricula)
        texto = texto.replace('TITULAR', pac.paciente)
        texto = texto.replace('MEDICO', medico[ent.codmedico])
        with open(f'{entrada} - {pac.paciente}.rtf', 'w') as file:
            file.write(texto)
            zip.write(f'{entrada} - {pac.paciente}.rtf')
    
os.chdir('..')
