def match_couples(boys, girls):
    if len(boys) != len(girls):
        print("Внимание, кто-то может остаться без пары.")
        return
    sorted_boys = sorted(boys)
    sorted_girls = sorted(girls)
    print("Идеальные пары:")
    for boy, girl in zip(sorted_boys, sorted_girls):
        print(f"{boy} и {girl}")
boys1 = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
girls1 = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']
match_couples(boys1, girls1)

print()
boys2 = ['Peter', 'Alex', 'John', 'Arthur', 'Richard', 'Michael']
girls2 = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']
match_couples(boys2, girls2)
