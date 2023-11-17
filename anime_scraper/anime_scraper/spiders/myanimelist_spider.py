import scrapy
import json
import re

 # Para rodar "scrapy crawl myanimelist"
class MyAnimeListSpider(scrapy.Spider):
    name = 'myanimelist'
    start_urls = ['https://myanimelist.net/topanime.php']
    collected_items = 0
    limit = 1000
    current_rank = 0
    collected_data = []

    def parse(self, response):
        for anime in response.css('tr.ranking-list'):
            self.current_rank += 1
            title = anime.css('h3 a::text').get()
            score_text = anime.css('.score .text::text').get()

            # Se o título e o texto do score existirem, adicione ao item
            if title and score_text:
                # Converta o texto do score para float
                score = float(score_text)
                item = {
                    'title': title,
                    'score': score,
                    'rank': self.current_rank,
                }
                additional_data_info = self.extract_additional_data_info(anime.get())
                item.update(additional_data_info)

                self.collected_data.append(item)
                self.collected_items += 1

                if self.collected_items >= self.limit:
                    self.logger.info(f'Limite de {self.limit} animes atingido. Encerrando.')
                    self.save_to_json()
                    return

        next_page = response.css('a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def extract_additional_data_info(self, additional_data):
        # Expressões regulares para extrair informações específicas
        episodes_pattern = re.compile(r'TV \((\d+) eps\)')
        date_pattern = re.compile(r'(\w{3}) (\d{4}) - (\w{3}) (\d{4})?')
        members_pattern = re.compile(r'(\d+,\d+) members')

        # Busca pelas informações na string
        episodes_match = episodes_pattern.search(additional_data)
        date_match = date_pattern.search(additional_data)
        members_match = members_pattern.search(additional_data)

        # Extrai os resultados das correspondências
        num_episodes = int(episodes_match.group(1)) if episodes_match else None
        start_month, start_year, end_month, end_year = date_match.groups() if date_match else (None, None, None, None)
        num_members = int(members_match.group(1).replace(',', '')) if members_match else None

        # Converte os nomes dos meses para os números correspondentes
        months_mapping = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
                          'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

        start_month = months_mapping.get(start_month, start_month)
        end_month = months_mapping.get(end_month, end_month)

        # Formata as datas como MM/YYYY
        start_date_formatted = f'{start_month}/{start_year}' if start_month and start_year else None
        end_date_formatted = f'{end_month}/{end_year}' if end_month and end_year else None

        # Retorna um dicionário com as informações extraídas
        return {
            'Number_of_episodes': num_episodes,
            'Start_date': start_date_formatted,
            'End_date': end_date_formatted,
            'Number_of_members': num_members
        }

    def save_to_json(self):
        filename = 'anime_data.json'
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(self.collected_data, json_file, ensure_ascii=False, indent=4)
        self.logger.info(f'Dados salvos em {filename}')
