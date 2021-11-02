import scrapy


# https://nintendo.fandom.com/wiki/Legendary_Pok%C3%A9mon
LEGENDARY = list(map(lambda x: x.lower(), [
    'Articuno', 'Zapdos', 'Moltres', 'Mewtwo', 'Mew',
    'Raikou', 'Entei', 'Suicune', 'Lugia', 'Ho-Oh', 'Celebi',
    'Regirock', 'Regice', 'Registeel', 'Latias', 'Latios', 'Kyogre', 'Groudon', 'Rayquaza', 'Jirachi', 'Deoxys',
    'Uxie', 'Mesprit', 'Azelf', 'Dialga', 'Palkia', 'Heatran', 'Regigigas', 'Giratina', 'Cresselia', 'Phione', 'Manaphy', 'Darkrai', 'Shaymin', 'Arceus',
    'Victini', 'Cobalion', 'Terrakion', 'Virizion', 'Tornadus', 'Thundurus', 'Reshiram', 'Zekrom', 'Landorus', 'Kyurem', 'Keldeo', 'Meloetta', 'Genesect',
    'Xerneas', 'Yveltal', 'Zygarde', 'Diancie', 'Hoopa', 'Volcanion',
    'Type: Null', 'Silvally', 'Tapu Koko', 'Tapu Lele', 'Tapu Bulu', 'Tapu Fini', 'Cosmog', 'Cosmoem', 'Solgaleo', 'Lunala', 'Nihilego', 'Buzzwole', 'Pheromosa', 'Xurkitree', 'Celesteela', 'Kartana', 'Guzzlord', 'Necrozma', 'Magearna', 'Marshadow', 'Poipole', 'Naganadel', 'Stakataka', 'Blacephalon', 'Zeraora', 'Meltan', 'Melmetal',
    'Zacian', 'Zamazenta', 'Eternatus', 'Kubfu', 'Urshifu', 'Zarude', 'Regieleki', 'Regidrago', 'Glastrier', 'Spectrier', 'Calyrex'
]))


class NationalSpider(scrapy.Spider):
    name = 'national'
    start_urls = ['https://pokemondb.net/pokedex/national']

    def parse(self, response):
        gens = response.css('.infocard-list')
        for i in range(len(gens)):
            gen = gens[i]
            for card in gen.css('.infocard'):
                image = card.css('.img-sprite').attrib['data-src']
                number = int(card.css('small::text').get()[1:])
                name = card.css('.ent-name::text').get()
                href = card.css('a.ent-name').attrib['href']
                item = {
                    'generation': i+1,
                    'number': number,
                    'name': name,
                    'image': image,
                    'href': href,
                }
                yield response.follow('https://pokemondb.net' + href, callback=self.parse_item, cb_kwargs={'item': item})

    def parse_item(self, response, item):
        tables = response.css('.vitals-table')
        types = tables[0].css('tbody tr:nth-child(2) .type-icon::text').getall()
        type1 = types[0]
        type2 = types[1] if len(types) > 1 else ''
        height = float(tables[0].css('tbody tr:nth-child(4) td::text').get().split()[0])
        weight = float(tables[0].css('tbody tr:nth-child(5) td::text').get().split()[0])

        catch_rate = int(tables[1].css('tr:nth-child(2) td::text').get().strip())

        egg_groups = tables[2].css('tr:nth-child(1) td a::text').getall()
        egg_group1 = egg_groups[0]
        egg_group1 = "" if egg_group1 == 'Undiscovered' else egg_group1
        egg_group2 = egg_groups[1] if len(egg_groups) > 1 else ''
        gender = tables[2].css('tr:nth-child(2) td')
        if len(gender.css('span').getall()) > 1:
            has_gender = True
            male = float(gender.css('span::text').get().split()[0].rstrip('%'))
        else:
            has_gender = False
            male = ''

        stats = tables[3].css('tbody')
        hp = int(stats.css('tr:nth-child(1) .cell-num')[0].css('::text').get())
        hp_min = int(stats.css('tr:nth-child(1) .cell-num')[1].css('::text').get())
        hp_max = int(stats.css('tr:nth-child(1) .cell-num')[2].css('::text').get())

        attack = int(stats.css('tr:nth-child(2) .cell-num')[0].css('::text').get())
        attack_min = int(stats.css('tr:nth-child(2) .cell-num')[1].css('::text').get())
        attack_max = int(stats.css('tr:nth-child(2) .cell-num')[2].css('::text').get())

        defense = int(stats.css('tr:nth-child(3) .cell-num')[0].css('::text').get())
        defense_min = int(stats.css('tr:nth-child(3) .cell-num')[1].css('::text').get())
        defense_max = int(stats.css('tr:nth-child(3) .cell-num')[2].css('::text').get())

        sp_atk = int(stats.css('tr:nth-child(4) .cell-num')[0].css('::text').get())
        sp_atk_min = int(stats.css('tr:nth-child(4) .cell-num')[1].css('::text').get())
        sp_atk_max = int(stats.css('tr:nth-child(4) .cell-num')[2].css('::text').get())

        sp_def = int(stats.css('tr:nth-child(5) .cell-num')[0].css('::text').get())
        sp_def_min = int(stats.css('tr:nth-child(5) .cell-num')[1].css('::text').get())
        sp_def_max = int(stats.css('tr:nth-child(5) .cell-num')[2].css('::text').get())

        speed = int(stats.css('tr:nth-child(6) .cell-num')[0].css('::text').get())
        speed_min = int(stats.css('tr:nth-child(6) .cell-num')[1].css('::text').get())
        speed_max = int(stats.css('tr:nth-child(6) .cell-num')[2].css('::text').get())

        total = int(tables[3].css('tfoot .cell-total b::text').get())
        is_legendary = item['name'].lower() in LEGENDARY

        yield {
            'generation': item['generation'],
            'number': item['number'],
            'name': item['name'],
            'image': item['image'],
            'type1': type1,
            'type2': type2,
            'height': height,
            'weight': weight,
            'catch_rate': catch_rate,
            'egg_group1': egg_group1,
            'egg_group2': egg_group2,
            'has_gender': has_gender,
            'male': male,
            'hp': hp,
            'hp_min': hp_min,
            'hp_max': hp_max,
            'attack': attack,
            'attack_min': attack_min,
            'attack_max': attack_max,
            'defense': defense,
            'defense_min': defense_min,
            'defense_max': defense_max,
            'sp_atk': sp_atk,
            'sp_atk_min': sp_atk_min,
            'sp_atk_max': sp_atk_max,
            'sp_def': sp_def,
            'sp_def_min': sp_def_min,
            'sp_def_max': sp_def_max,
            'speed': speed,
            'speed_min': speed_min,
            'speed_max': speed_max,
            'total': total,
            'is_legendary': is_legendary,
        }
