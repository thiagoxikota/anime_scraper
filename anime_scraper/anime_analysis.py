import json
from statistics import mean, median, stdev
import matplotlib.pyplot as plt
import datetime

# Carregar os dados do arquivo JSON
with open('anime_data.json', 'r', encoding='utf-8') as json_file:
    anime_data = json.load(json_file)

# Análise 1: Distribuição de Notas (Scores)
scores = [anime['score'] for anime in anime_data]
average_score = mean(scores)
median_score = median(scores)
std_dev_score = stdev(scores)

print(f'Análise 1: Distribuição de Notas (Scores)')
print(f'Média: {average_score:.2f}')
print(f'Mediana: {median_score:.2f}')
print(f'Desvio Padrão: {std_dev_score:.2f}')
print('\n')

# Análise 2: Relação entre Classificação e Número de Episódios
episode_scores = [(anime['Number_of_episodes'], anime['score']) for anime in anime_data if anime['Number_of_episodes'] is not None]
episode_scores.sort(key=lambda x: x[0])  # Ordenar por número de episódios

print(f'Análise 2: Relação entre Classificação e Número de Episódios')
for episodes, score in episode_scores:
    print(f'Episódios: {episodes}, Score: {score:.2f}')
print('\n')

# Análise 3: Evolução ao Longo do Tempo
date_scores = [(datetime.datetime.strptime(anime['Start_date'], "%m/%Y"), anime['score']) for anime in anime_data if anime['Start_date'] is not None]
date_scores.sort(key=lambda x: x[0])  # Ordenar por data de início

dates, scores = zip(*date_scores)

plt.figure(figsize=(10, 6))
plt.plot(dates, scores, marker='o')
plt.title('Análise 3: Evolução ao Longo do Tempo')
plt.xlabel('Data de Início')
plt.ylabel('Score')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
