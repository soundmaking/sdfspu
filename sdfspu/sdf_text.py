import string
import random


def randstring(k_=32):
    """ well behaving random string
    :returns: string sans stuff what might mess up a python str or upset pylint
    """
    chars = '!$%&*+-=?@^_~'
    chars += string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=k_))


def split_name(a_name):
    """
    If only one word given, return it as last.
    If more than two words given, return all but last as first.
    examples = {
        'ok simple': ('ok', 'simple'),
        'solo': ('', 'solo'),
        'three part name': ('three part', 'name'),
        'name with-hyphen': ('name', 'with-hyphen'),
        '': ('', '')
        }
    :param a_name: str
    :return: ('first', 'last')
    """
    try:
        a_split = a_name.split()
        last = a_split[-1]
        first = ' '.join(a_split[:-1])
        if not len(first) or not last:
            # no_first_name_count += 1
            first = ''
        return first, last
    except IndexError:
        return '', ''
# end def split_name()


def obsc_email(email_address):
    """
    'something@example.com' -> 'som...@e...'
    """
    ls = email_address.strip().split('@')
    return ls[0][0:3] + '...@' + ls[1][0] + '...'


# def path_is_url(path):
#     """
#     returns True when input (assumed string) starts either http:// Or https:/
#     """
#     return path[0:4] == 'http' and path[6] == '/'
