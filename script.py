import csv
import re
from IPython.display import display
from natasha import (
    Segmenter,
    MorphVocab,
    PER,
    NamesExtractor,
    NewsNERTagger,
    NewsEmbedding,
    Doc
)

hello_message = r'(здравствуйте|привет|добрый|приветствую|Добрый|Здравствуйте|Привет|Приветствую|добрый\sдень)'
end_message = r'(До\sсвидания|до\sсвидания|всего\sдоброго|Всего\sдоброго|всего\sхорошего|хорошего\sвечера)'
name_company = r'(диджитал\sбизнес|китобизнес)'

my_dict = {}
dialogues = set()
len_dialogues = {}


### Открытие исходого документа и фильтрация отбор реплик "менеджера"

def openDocument():

    my_file = input('Введите путь к файлу для парсинга: \n')
    with open(my_file, 'r', encoding='utf-8') as file:
        data = csv.reader(file, delimiter=",")
        for row in data:
            if row[2] == 'manager':
                my_dict.setdefault(row[0].strip('" '),[]).append(row[3].strip('" '))
            dialogues.add(row[0])
        len_dialogues['Количество диалогов'] = (len(dialogues) - 1)



### Сохрание каждого диалога со стороны менеджера в отдельный файл для удобного просмотра

def saveDialogues():


    for i in range(len_dialogues['Количество диалогов']):
        with open(f"output{i}.txt", "w", encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(my_dict[str(i)])


### Отображение имени менеджера
'''
Использовал библиотеку Natasha для поиска имен, в данном тексте сработала не лучшим способом
'''

def managerName():

    emb = NewsEmbedding()
    segmenter = Segmenter()
    morph_vocab = MorphVocab()
    ner_tagger = NewsNERTagger(emb)
    names_extractor = NamesExtractor(morph_vocab)

    doc = Doc(text.title())
    doc.segment(segmenter)
    doc.tag_ner(ner_tagger)

    for span in doc.spans:
        span.normalize(morph_vocab)
    {_.text: _.normal for _ in doc.spans}


    for span in doc.spans:
        if span.type == PER:
            span.extract_fact(names_extractor)

    names = {_.normal: _.fact.as_dict for _ in doc.spans if _.fact}


    display(f'Файл output{i}.txt \nИмя менеджера {names}')

### Поиск реплики, где менеджер поздоровался

'''
Дальше использовал регулярки, так как Natasha не умеет искать по следующим необходимым критериям
Поэтому реализовал вручную
'''

def find_startMessage():

    results = re.findall(hello_message, text)
    if results:
        print(f'Менеджер поздоровался, {results}')
    else:
        print('Менеджер не поздоровался!!')


###Поиск названия компании

def find_companyName():

    results = re.findall(name_company, text)

    if results:
        print(f'Название компании, {results}')
    else:
        print('Компанию не назвали!!')



###Поиск реплики, где менеджер попрощался

def find_endMessage():

    results = re.findall(end_message, text)
    if results:
        print(f'Менеджер попрощался, {results} \n -----------------')
    else:
        print(f'Менеджер не попрощался!! \n -----------------')


openDocument()
saveDialogues()
for i in range(len_dialogues['Количество диалогов'] - 1):
    file = open(f"output{i}.txt", 'r', encoding='utf-8')
    text = file.read()
    managerName()
    find_startMessage()
    find_companyName()
    find_endMessage()
