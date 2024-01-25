#!/usr/bin/env python3

import sys
import getopt
from PIL import Image as img

# ASCII generator with 24-bit colours (requires 'pillow' -> e.g. APT package 'python3-willow')

DEFAULT_MAX = 100


class Colours:
    WELCOME1 = "\x1b[38;2;235;216;52m"
    WELCOME2 = "\x1b[38;2;52;183;235m"
    WELCOME3 = "\x1b[38;2;235;52;107m"
    BOLD = "\u001b[1m"
    RESET = "\u001b[0m"


def usage(name="ascii-wiz.py"):
    print(
        f"""
Usage:  {name} -i <inputfile> [ optional configuration ]

Configuration:

        -s --size           Set max width/height
        -b --background     Use background colouring
           --colour         Disable colours
"""
    )


def welcome(colours):
    if colours:
        print(
            f"""{Colours.BOLD}
                {Colours.WELCOME2}_ _                  {Colours.WELCOME3}_     
               {Colours.WELCOME2}(_|_)                {Colours.WELCOME3}(_)     
{Colours.WELCOME1}  __ _ ___  _{Colours.WELCOME2}__ _ _        __ {Colours.WELCOME3}     _ _ ____
{Colours.WELCOME1} / _` / __|/ {Colours.WELCOME2}__| | |  ____ \ \{Colours.WELCOME3} /\ / / |_  /
{Colours.WELCOME1}| (_| \__ \ ({Colours.WELCOME2}__| | | |____| \ {Colours.WELCOME3}V  V /| |/ / 
{Colours.WELCOME1} \__,_|___/\_{Colours.WELCOME2}__|_|_|         \{Colours.WELCOME3}_/\_/ |_/___|

        {Colours.RESET}"""
        )
    else:
        print(
            f"""
                _ _                  _     
  __ _ ___  ___(_|_)       __      _(_)____
 / _` / __|/ __| | |  ____ \ \ /\ / / |_  /
| (_| \__ \ (__| | | |____| \ V  V /| |/ / 
 \__,_|___/\___|_|_|         \_/\_/ |_/___|

        """
        )


def handle_arg(argv):
    arg_list = []
    inputfile = ""
    u_size = -1
    colours = True
    background = False

    try:
        opts, args = getopt.getopt(
            argv, "hi:s:b", ["input=", "size=", "colour", "background"]
        )
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-s", "--size"):
            u_size = int(arg)
        elif opt in ("-b", "--background"):
            background = True
        elif opt == "--colour":
            colours = False

    welcome(colours)

    arg_list.append(inputfile)
    arg_list.append(u_size)
    arg_list.append(colours)
    arg_list.append(background)

    return arg_list


def converter(filename, u_size, colours, background):
    chars = [
        "$",
        "@",
        "B",
        "%",
        "8",
        "&",
        "W",
        "M",
        "#",
        "*",
        "o",
        "a",
        "h",
        "k",
        "b",
        "d",
        "p",
        "q",
        "w",
        "m",
        "Z",
        "O",
        "0",
        "Q",
        "L",
        "C",
        "J",
        "U",
        "Y",
        "X",
        "z",
        "c",
        "v",
        "u",
        "n",
        "x",
        "r",
        "j",
        "f",
        "t",
        "/",
        "\\",
        "|",
        "(",
        ")",
        "1",
        "{",
        "}",
        "[",
        "]",
        "?",
        "-",
        "_",
        "+",
        "~",
        "<",
        ">",
        "i",
        "!",
        "l",
        "I",
        ";",
        ":",
        ",",
        '"',
        "^",
        "`",
        "'",
        ".",
        " ",
    ]
    ascii_string = []

    with img.open(filename) as image:
        size = image.size
        # compensate roughly 2 * char_w = char_h (most monospaced fonts)
        w, h = size[0], size[1] / 2
        ratio = w / h

        if u_size > 0 and (u_size < w or u_size < h):
            if ratio >= 1:
                n_size = (u_size, int(u_size / ratio))
            else:
                n_size = (int(u_size * ratio), u_size)
        elif w > DEFAULT_MAX or h > DEFAULT_MAX:
            if ratio >= 1:
                n_size = (DEFAULT_MAX, int(DEFAULT_MAX / ratio))
            else:
                n_size = (int(DEFAULT_MAX * ratio), DEFAULT_MAX)
        else:
            n_size = (w, h)

        print(f"Original size: {str(size)}")
        print(f"Fixed aspect ratio: {round(ratio, 6)}")
        print(f"Fixed ASCII size: {str(n_size)}\n\n")

        image = image.resize(n_size)

        for p in image.getdata():
            # calculate intensity based on rgb value
            x = int(p[0]) + int(p[1]) + int(p[2])
            normalized = int(round(x * 69 / 765))

            if colours:
                # convert each rgb value to ansi
                if background:
                    ansi_c = (
                        rgb_to_ansi_background(p)
                        + rgb_to_ansi_letter(p)
                        + chars[normalized]
                    )
                else:
                    ansi_c = rgb_to_ansi_letter(p) + chars[normalized]

                ascii_string.append(ansi_c)
            else:
                ascii_string.append(chars[normalized])

    return ascii_string, n_size


def rgb_to_ansi_letter(rgb):
    r, g, b = rgb[0], rgb[1], rgb[2]
    return f"\x1b[38;2;{r};{g};{b}m"


def rgb_to_ansi_background(rgb):
    r, g, b = rgb[0], rgb[1], rgb[2]
    return f"\u001b[48;2;{r};{g};{b}m"


def print_ascii(width, ascii_string):
    n = 0
    for c in ascii_string:
        if n % width == 0:
            n += 1
            print(Colours.RESET)
            continue
        n += 1
        print(c, end="")

    print(Colours.RESET + "\n")


def main(argv):
    args = handle_arg(argv)
    filename = args[0]
    u_size = args[1]
    colours = args[2]
    background = args[3]

    ascii_string, n_size = converter(filename, u_size, colours, background)
    print_ascii(n_size[0], ascii_string)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage(sys.argv[0])
        sys.exit(1)
    main(sys.argv[1:])
