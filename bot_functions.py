import re
import requests


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

<<<<<<< HEAD
    # If there is a negative number, set this to true
    negative_numbers = False

=======
>>>>>>> d2c4fb1993db0637a0bf7dc20e077e1ae9777b3e
    # Verify the given number is really only a number
    if isinstance(number, int):
        # In case of a negative number:
        if number < 0:
            number *= -1
<<<<<<< HEAD
            negative_numbers = True
=======
>>>>>>> d2c4fb1993db0637a0bf7dc20e077e1ae9777b3e
        elif number == 0:
            number_for_return = unicode_numbers[number]
    else:
        raise TypeError('Given number is not of type int!')

    while number != 0:
        number_for_return = unicode_numbers[number % 10] + number_for_return
        number = int(number / 10)

<<<<<<< HEAD
    if negative_numbers == True:
        number_for_return = '➖' + number_for_return
=======
>>>>>>> d2c4fb1993db0637a0bf7dc20e077e1ae9777b3e
    return number_for_return


def parse_today_ebook():
    """Returns the current ebook from packtpub"""
    # Search for any big Header and return it
    pattern = re.compile(r'<h1>(.+)<\/h1><\/div>')

    # Packt source URL
    source_url_from_packt = 'https://www.packtpub.com/packt/offers/free-learning'

    # Requesting the web page
    headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    r = requests.get(source_url_from_packt, headers=headers)

    # Extracting the book title with some lovely regex.
    book_title = pattern.findall(str(r.text))
    str_to_return = 'The today\'s book is: {}. Find it at {}'.format(
        book_title[0], source_url_from_packt)
    return str_to_return
