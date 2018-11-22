def number_to_unicode(number):
    '''
    Converting a digit into a unicode number smiley.
    See more at https://unicode.org/emoji/charts/full-emoji-list.html#keycap.
    '''
    unicode_numbers = {
        0: u'0️⃣',
        1: u'1️⃣',
        2: u'2️⃣',
        3: u'3️⃣',
        4: u'4️⃣',
        5: u'5️⃣',
        6: u'6️⃣',
        7: u'7️⃣',
        8: u'8️⃣',
        9: u'9️⃣',
    }
    number_for_return = u''

    # Verify the given number is really only a number
    if isinstance(number, int):
        # In case of a negative number:
        if number < 0:
            number *= -1
        elif number == 0:
            number_for_return = unicode_numbers[number]
    else:
        raise TypeError('Given number is not of type int!')

    while number != 0:
        number_for_return = unicode_numbers[number % 10] + number_for_return
        number = int(number / 10)

    return number_for_return
