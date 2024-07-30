from cs50 import get_string


card_number = get_string("enter card number: ")

reverse_order = card_number[ ::-1]
lunn_number1 = sum([(int(x) * 2) // 10 + ((int(x)* 2) % 10) for x in reverse_order[1::2]])
lunn_number2 = sum([int(x) for x in reverse_order[0::2]])
total = lunn_number1 + lunn_number2



if total % 10 == 0:
    if int(card_number[:2]) in [34,37]  and len(card_number) == 15:
        print("AMEX")
    elif int(card_number[:2]) in [51,52,53,54,55] and len(card_number) == 16:
        print("MASTERCARD")
    elif int(card_number[0]) == 4 and len(card_number) in [13,16]:
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")
