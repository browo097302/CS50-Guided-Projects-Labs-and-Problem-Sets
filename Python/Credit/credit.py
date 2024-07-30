import cs50

def get_card_number():
            card_number = cs50.get_string("enter card number: ")
            card_number_length = len(card_number)
            if card_number_length not in [13, 15, 16]:
                print("INVALID")
                return None
            else:
                return card_number

card_number = get_card_number()

start = len(card_number) - 2
end = -1
total = 0
subnumber = card_number[start:end:-2]
for char in subnumber:
    lunn_number = int(char) * 2
    if lunn_number < 10:
        total += lunn_number
    else:
        lunn_number = lunn_number - 9
        total += lunn_number


if total % 10 == 0:
    if int(card_number[:2]) in [34,37]  and len(card_number) == 15:
        print("AMEX")
    elif int(card_number[:2]) in [51,52,53,54,55] and len(card_number) == 16:
        print("MASTERCARD")
    elif int(card_number[0]) == 4 and len(card_number) in [13,16]:
        print("VISA")
else:
    print("INVALID")












