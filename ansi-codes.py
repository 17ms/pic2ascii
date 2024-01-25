#!/usr/bin/env python3

# A script to convert RGB to ansi escape codes


while True:
    colour = input("R G B (empty to exit): ")

    if colour == "":
        print("")
        break

    r, g, b = colour.split()
    ansi_box = f"\u001b[48;2;{r};{g};{b}m"
    ansi_letter = f"\x1b[38;2;{r};{g};{b}m"
    end_c = "\u001b[0m"
    bold = "\u001b[1m"

    print(f"\nColour: \\x1b[38;2;{r};{g};{b}m")
    print(f"Background: \\u001b[48;2;{r};{g};{b}m\n")

    print(
        f"""
        {bold}{ansi_letter}ABCDE      {ansi_box}ABCDE{end_c}
        {bold}{ansi_letter}FGHIJ      {ansi_box}FGHIJ{end_c}
        {bold}{ansi_letter}KLMNO      {ansi_box}KLMNO{end_c}
    
    """
    )
