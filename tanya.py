import argparse

def write_output(output_file, summary):
    with open(output_file, "a", encoding='UTF-8') as file:
        file.write(summary)

def medals(team, year, output_file=None):
    medals_list = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
    file = "athlete_events.tsv"

    found_team = False
    found_year = False
    found_medals = False

    with open(file, "r", encoding='UTF-8') as file:
        header = file.readline().rstrip('\n').split('\t')
        YEAR = header.index("Year")
        TEAM = header.index("Team")
        NOC = header.index("NOC")
        NAME = header.index("Name")
        EVENT = header.index("Event")
        MEDAL = header.index("Medal")

        counter=0
        for line in file:
            row = line.rstrip('\n').split('\t')
            if (row[TEAM] == team or row[NOC] == team):
                found_team = True
            if row[YEAR]==year:
                found_year = True

            if (row[TEAM]==team or row[NOC]==team) and row[YEAR]==year and row[MEDAL] != "NA":
                found_medals = True
                name, event, medal = row[NAME], row[EVENT], row[MEDAL]
                medals_list[medal] +=1

                if counter < 10:
                    print(f"{name}; {event}: {medal}")
                    counter += 1

                if output_file and counter <=10:
                    write_output(output_file, f"{name}; {event}: {medal}\n")
        if not found_team:
            print(f"!!ERROR. WE CAN NOT FOUND {team}!!")
        elif not found_year:
            print(f"!!THERE WERE NO OLYMPICS IN {year}!!")
        elif not found_medals:
            print(f"!!NO MEDALS FOR THE {team} in {year} FOUND!!")
        else:
            summary =(
                f"Gold: {medals_list['Gold']}\n"
                f"Silver: {medals_list['Silver']}\n"
                f"Bronze: {medals_list['Bronze']}\n"
            )
            print(summary)

        if output_file:
            write_output(output_file, summary)

def overall(file, countries):
    country_medals = {country: {'Gold': 0, 'Silver': 0, 'Bronze': 0, 'Years': {}} for country in countries}
    with open(file, "r", encoding='utf-8') as file:
        header = file.readline().rstrip('\n').split('\t')
        YEAR = header.index("Year")
        TEAM = header.index("Team")
        NOC = header.index("NOC")
        MEDAL = header.index("Medal")

        for line in file:
            row = line.rstrip('\n').split('\t')
            for country in countries:
                if (row[TEAM] == country or row[NOC] == country) and row[MEDAL] != 'NA':
                    medal = row[MEDAL]
                    year = row[YEAR]
                    country_medals[country][medal] += 1

                    if year not in country_medals[country]["Years"]:
                        country_medals[country]["Years"][year] = 0
                    country_medals[country]["Years"][year] += 1

    for country in countries:
        if country_medals[country]["Years"]:
            best_year = max(country_medals[country]["Years"], key=country_medals[country]["Years"].get)
            total_medals = sum(country_medals[country]["Years"].values())
            print(f"The best year for {country} was {best_year} when {country} won {country_medals[country]["Years"][best_year]} medals")
            print(
                f"Total medals for {country}: {total_medals} (Gold: {country_medals[country]['Gold']}, Silver: {country_medals[country]['Silver']}, Bronze: {country_medals[country]['Bronze']})\n"
            )
        else:
            print(f"No medals found for {country}")


parser = argparse.ArgumentParser(description="Olympic medals")
file = "athlete_events.tsv"





def total(year):
    file = "athlete_events.tsv"
    medals_by_country = {}

    with open(file, "r", encoding="utf-8") as file:
        header = file.readline().rstrip('\n').split('\t')
        YEAR = header.index("Year")
        TEAM = header.index("Team")
        MEDAL = header.index("Medal")

        found_year = False
        for line in file:
            row = line.rstrip('\n').split('\t')
            if row[YEAR] == year:
                found_year = True
                if row[MEDAL] != "NA":
                    country = row[TEAM]
                    medal = row[MEDAL]
                    if country not in medals_by_country:
                        medals_by_country[country] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
                    medals_by_country[country][medal] += 1

        if not found_year:
            print(f"!!THERE WERE NO OLYMPICS IN {year}")
        else:
            for country, counts in medals_by_country.items():
                print(f"{country} - Gold: {counts['Gold']}, Silver: {counts['Silver']}, Bronze: {counts['Bronze']}")

def load_data(file):
    data = []
    with open(file, "r", encoding='UTF-8') as f:
        header = f.readline().rstrip('\n').split('\t')
        for line in f:
            row = line.rstrip('\n').split('\t')
            data.append(dict(zip(header, row)))
        return data

def load_data(file):
    data = []
    with open(file, "r", encoding='UTF-8') as f:
        header = f.readline().rstrip('\n').split('\t')
        for line in f:
            row = line.rstrip('\n').split('\t')
            data.append(dict(zip(header, row)))
    return data

def find_best_year(data, country):
    best_year = None
    max_medals = 0
    for year in set(row['Year'] for row in data if row['Team'] == country):
        medals = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
        for row in data:
            if row['Team'] == country and row['Year'] == year:
                medal = row['Medal'].capitalize()
                if medal in medals:
                    medals[medal] += 1
        total_medals = sum(medals.values())
        if total_medals > max_medals:
            max_medals = total_medals
            best_year = year
    return best_year

def find_worst_year(data, country):
    worst_year = None
    min_medals = float('inf')
    for year in set(row['Year'] for row in data if row['Team'] == country):
        medals = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
        for row in data:
            if row['Team'] == country and row['Year'] == year:
                medal = row['Medal'].capitalize()
                if medal in medals:
                    medals[medal] += 1
        total_medals = sum(medals.values())
        if total_medals < min_medals:
            min_medals = total_medals
            worst_year = year
    return worst_year

def average_medals(data, country):
    total_medals = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
    years = set(row['Year'] for row in data if row['Team'] == country)
    for year in years:
        medals = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
        for row in data:
            if row['Team'] == country and row['Year'] == year:
                medal = row['Medal'].capitalize()
                if medal in medals:
                    medals[medal] += 1
        for medal_type, count in medals.items():
            total_medals[medal_type] += count
    if years:
        average_medals = {medal_type: count / len(years) for medal_type, count in total_medals.items()}
    else:
        average_medals = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
    return average_medals

def interactive_mode(file):
    data = load_data(file)
    while True:
        country = input("Enter country (or 'exit'): ")
        if country.lower() == 'exit':
            break
        best = find_best_year(data, country)
        worst = find_worst_year(data, country)
        avg_medals = average_medals(data, country)
        print(f"The best year for {country}: {best}")
        print(f"The worst year for {country}: {worst}")
        print(f"Average amount of medals: {avg_medals}")

parser.add_argument("-medals", nargs=2, help="Country of team and year of Olympics")
parser.add_argument("-output", help = "Name of file where summary will be saved")
parser.add_argument("-overall", nargs="+", help = "Write all of countries that you want to check" )
parser.add_argument("-total", type=str, help="Year for total medal count")
parser.add_argument("-interactive", action="store_true", help="Interactive mode")

args = parser.parse_args()

if args.medals:
    team, year = args.medals
    output_file = args.output
    medals(team, year, output_file)

elif args.overall:
    countries = args.overall
    overall(file, countries)

elif args.total:
    total(args.total)

elif args.interactive:
    interactive_mode(file)

