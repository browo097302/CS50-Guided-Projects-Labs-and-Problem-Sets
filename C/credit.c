#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int length = 0;
    long cardnumber;
    do
    {
    cardnumber = get_long("enter card number: ");
    }
    while(cardnumber < 0);

    int card2, card4, card6, card8, card10, card12, card14, card16;
        card2 = ((cardnumber % 100)/10)*2;
        card4 = ((cardnumber % 10000)/1000)*2;
        card6 = ((cardnumber % 1000000)/100000)*2;
        card8 = ((cardnumber % 100000000)/10000000)*2;
        card10 = ((cardnumber % 10000000000)/1000000000)*2;
        card12 = ((cardnumber % 1000000000000)/100000000000)*2;
        card14 = ((cardnumber % 100000000000000)/10000000000000)*2;
        card16 = ((cardnumber % 10000000000000000)/1000000000000000)*2;

        card2 = (card2 % 100 /10) + (card2 % 10);
        card4 = (card4 % 100 /10) + (card4 % 10);
        card6 = (card6 % 100 /10) + (card6 % 10);
        card8 = (card8 % 100 /10) + (card8 % 10);
        card10 = (card10 % 100 /10) + (card10 % 10);
        card12 = (card12 % 100 /10) + (card12 % 10);
        card14 = (card14 % 100 /10) + (card14 % 10);
        card16 = (card16 % 100 /10) + (card16 % 10);

    long visa = cardnumber;
    long master = cardnumber;
    long amex = cardnumber;

    int sum1 = card2 + card4 + card6 + card8 + card10 + card12 + card14 + card16;
    int card1, card3, card5, card7, card9, card11, card13, card15;
        card1 = (cardnumber % 10);
        card3 = (cardnumber % 1000)/100;
        card5 = (cardnumber % 100000)/10000;
        card7 = (cardnumber % 10000000)/1000000;
        card9 = (cardnumber % 1000000000/100000000);
        card11 = (cardnumber % 100000000000/10000000000);
        card13 = (cardnumber % 10000000000000/1000000000000);
        card15 = (cardnumber % 1000000000000000/100000000000000);



    int sum2 = card1 + card3 + card5 + card7 + card9 + card11 + card13 + card15;
    int sum3 = sum1 + sum2;

    if((sum3 % 10) != 0)
    {
    printf("%s\n","INVALID");
    return 0;
    }
    while (cardnumber > 0)
    {
        cardnumber = cardnumber/10;
        length++;
    }

    // find out if card is visa
    while( visa >= 10 )
    {
        visa /= 10;
    }
        if(visa == 4 && (length == 13 || length ==16))
        {
            printf("%s\n", "VISA");
            return 0;
        }
    // find out if card is amex
    while( amex >10000000000000)
        {
        amex /= 10000000000000;
        }
        if( length == 15 && (amex == 34 || amex == 37))
        {
            printf("%s\n", "AMEX");
            return 0;
        }
        // identify if master
    while ( master > 100000000000000)
        {
        master /= 100000000000000;
        }
        if( length == 16 && (master >= 51 && master <=55))
        {
            printf("%s\n","MASTERCARD");
            return 0;
        }
        else
        printf("%s\n","INVALID");
        return 0;
}
