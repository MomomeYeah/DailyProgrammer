# http://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/

def main():
    hex_input = raw_input("Enter Hex Numbers: ")
    output = ""
    for i in hex_input.split(" "):
        for bit in range(8):
            output += "x" if (int(i, 16) << bit) & (1 << 7) else " "
        output += "\n"
    print output

main()

# better solution
'''from string import maketrans

def main():
    bin2x = maketrans('01',' X')
    for hexvalue in raw_input().split():
        print "{0:08b}".format(int(hexvalue, 16)).translate(bin2x)'''