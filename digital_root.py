# http://www.reddit.com/r/dailyprogrammer/comments/1berjh/040113_challenge_122_easy_sum_them_digits/

def sum_digits(val):
    sum = 0
    while val:
        sum += val % 10
        val /= 10
    return sum

def main():
    val = int(raw_input("Enter Number: "))
    sum = sum_digits(val)
    while sum % 10 != sum:
        print sum
        sum = sum_digits(sum)

    print sum

main()