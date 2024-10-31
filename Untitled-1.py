Playerf = {
    "battleship": ["battleship", "images/ships/battleship/battleship.png", (125, 600), (40, 195), 4, "images/ships/battleship/battleshipgun.png", (0.4, 0.125), [-0.525, -0.34, 0.67, 0.49]],
    "cruiser": ["cruiser", "images/ships/cruiser/cruiser.png", (200, 600), (40, 195), 2, "images/ships/cruiser/cruisergun.png", (0.4, 0.125), [-0.36, 0.64]],
    "destroyer": ["destroyer", "images/ships/destroyer/destroyer.png", (275, 600), (30, 145), 2, "images/ships/destroyer/destroyergun.png", (0.5, 0.15), [-0.52, 0.71]],
    "patrol boat": ["patrol boat", "images/ships/patrol boat/patrol boat.png", (425, 600), (20, 95), 0, "", None, None],
    "submarine": ["submarine", "images/ships/submarine/submarine.png", (350, 600), (30, 145), 1, "images/ships/submarine/submarinegun.png", (0.25, 0.125), [-0.45]],
    "carrier": ["carrier", "images/ships/carrier/carrier.png", (50, 600), (45, 245), 0, "", None, None],
    "rescue ship": ["rescue ship", "images/ships/rescue ship/rescue ship.png", (500, 600), (20, 95), 0, "", None, None]
}

for name in Playerf.keys():
    print(f"{name.center(20, ' ')}\n")  # Center the name with padding
    print(f"{Playerf[name][1].center(40)}")
    print(f"{str(Playerf[name][2]).center(40)}")
    print(f"{str(Playerf[name][3]).center(40)}")
    print(f"{str(Playerf[name][4]).center(40)}")
    print(f"{Playerf[name][5].center(40)}" if Playerf[name][5] else "No gun image".center(40))
    print(f"{str(Playerf[name][6]).center(40)}" if Playerf[name][6] else "No gun offset".center(40))
    print(f"{str(Playerf[name][7]).center(40)}" if Playerf[name][7] else "No gun coordinates".center(40))
    print("\n" + "="*40 + "\n")  # Separator for each ship
