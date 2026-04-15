import csv

def to_csv(file_name, content):

    if content:
        columns = content[0].keys()

        try:
            # open in write mode ('w')
            # newline='' avoid white lines on windowns
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                # create the writer's object configuring the columns names
                writer = csv.DictWriter(file, fieldnames=columns)

                # first line with columns names
                writer.writeheader()

                # write all the data
                writer.writerows(content)
                
            print(f"Arquivo '{file_name}' salvo com sucesso!")
        except IOError as e:
            print(f"Erro ao salvar o arquivo: {e}")
    else:
        print("A lista de resultados está vazia.")