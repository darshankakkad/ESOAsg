"""
Module that performs some useful and basic checks
"""

# import sys
import numpy as np
import shutil
import urllib
import os.path

from astropy.io import fits

# ESOAsg imports
from ESOAsg import msgs
from ESOAsg import default


def from_bytes_to_string(input_in_bytes):
    r"""Given an input in `bytes` return it the corresponding `str`

    This is mainly to deal with the fact that TAP queries return a list in bytes format that might be annoying. If
    the input is already a `str` nothing is changed.

    Args:
        input_in_bytes (`bytes`)
            Input in bytes

    Returns:
        output_as_str (`str`)
            Output converted to a string
    """
    if isinstance(input_in_bytes, (str, np.str)):
        output_as_str = input_in_bytes
    elif isinstance(input_in_bytes, bytes):
        output_as_str = np.str(input_in_bytes.decode("utf-8"))
    else:
        msgs.error('Unable to understand the format of the entry: {}'.format(type(input_in_bytes)))
    return output_as_str


def remove_non_ascii(text_string):
    r"""Replace non ascii characters from a string

    Args:
        text_string (`str`):
            input string from which the non ascii characters will be removed

    Returns:
        text_string_cleaned ('str'):
            string from which the non ASCII characters have been removed.

    """
    text_string_cleaned = "".join(character for character in text_string if 31 < ord(character) < 123)
    text_string_cleaned.replace('\\', '').strip()
    return text_string_cleaned


def check_disk_space(min_disk_space=np.float32(default.get_value('min_disk_space'))):
    r"""
    Given a limit in GB in the variable min_disk_space the macro returns `True` if there is enough space and rises
    an error otherwise.

    Args:
        min_disk_space (`numpy.float32`):
            Size of free space on disk required

    Returns:
        enough_space (`numpy.bool`):
            True if there is enough space on disk
    """
    total, used, free = shutil.disk_usage("./")
    total = total / (1024**3)
    used = used / (1024**3)
    free = free / (1024**3)
    msgs.info('Your disk has: Total: {0:.2f} GB, Used: {0:.2f} GB, Free: {0:.2f} GB'.format(total, used, free))
    if free > min_disk_space:
        enough_space = np.bool(1)
    else:
        enough_space = np.bool(0)
        msgs.error('Not enough space on disk')
    return enough_space


def connection_to_website(url, timeout=1):   # written by Ema 05.03.2020
    r"""Check there is an active connection to a website

    Args:
        url (`str`):
            link to the website you want to check
        timeout (`int`, `float`):
            timeout waiting for the website to respond

    Returns:
         is_active (`boolean`):
            `True` if there is an active connection, `False` and error raised if not.

    """
    # Checks for url
    assert isinstance(url, str), 'The url needs to be a string'
    if url.startswith('www'):
        url_clean = 'http://'+url
        msgs.warning('Modifying url to: {}'.format(url_clean))
    else:
        url_clean = url

    request = urllib.request.Request(url_clean)
    try:
        urllib.request.urlopen(request, timeout=timeout)
    except urllib.error.HTTPError as err:
        msgs.warning('HTTP Error: {}'.format(err.code))
        is_active = False
    except urllib.error.URLError as err:
        msgs.warning('URL Error: {}'.format(err.reason))
        is_active = False
    else:
        is_active = True
    return is_active


def fits_file_is_valid(fits_file):  # Written by Ema 05.03.2020
    r"""Check if a file exists and has a valid extension

    Args:
        fits_file (`str`):
            fits file you would like to check

    Returns:
        is_fits (`boolean`):
            `True` if exists `False` and warning raised if not.

    """
    is_fits = True

    # Checks for url
    assert isinstance(fits_file, str), 'input fits needs to be a string'
    # Check for ending
    if not fits_file.endswith('.fits') and not fits_file.endswith('.fits.fz') and not fits_file.endswith('.fits.gz'):
        msgs.warning('File: {} does not end with `fits` or `fits.fz` or `fits.gz`'.format(fits_file))
        is_fits = False
    # Check for existence
    if not os.path.exists(fits_file):
        msgs.warning('File: {} does not exists'.format(fits_file))
        is_fits = False

    return is_fits


def image2d_is_valid(image2d):  # Written by Ema 12.03.2020
    r"""Check if a 2D image is valid

    Args:
        image2d (np.array):
            image that you would like to check

    Returns:
        is_image2d (`boolean`):
            `True` if a valid 2D image `False` and error raised if not.
    """
    is_image2d = True

    # Checks if it is a numpy array
    assert isinstance(image2d, np.ndarray), 'The image is not a `numpy array`'
    # Check for dimensions
    if not image2d.ndim == 2:
        msgs.warning('The image is not two dimensional (NDIM={})'.format(image2d.ndim))
        is_image2d = False

    return is_image2d


def table_is_valid(table):  # Written by Ema 08.04.2020
    r"""Check if a table is valid

    Args:
        table (`fits.BinTableHDU` or `fits.TableHDU`):
            table that you would like to check

    Returns:
        is_table (`boolean`):
            `True` if a valid table format `False` and error raised if not.
    """
    is_table = True

    # Checks if it is an astropy table
    assert isinstance(table, (fits.BinTableHDU, fits.TableHDU)), 'The table is not a `fits.BinTableHDU` or a `fits.TableHDU`'

    return is_table


def header_is_valid(header):
    r"""Check if an header is valid

    """
    is_header = True

    # Check if is a fits.header
    assert isinstance(header, fits.Header), 'The header is not an instance of `astropy.fits.io.header`'
    if len(header) == 0:
        msgs.warning('Empty Header')
        is_header = False

    return is_header

'''
def single_value_to_list(single_value):
    """This is useful to transform single strings, integers, floats into python lists. Can be used when the
    input to a function is given by the `parse_arguments()`

    Args:
        single_value: (str, float, int):
            This is the argument you want to have as a list

    Returns:
        list_value: (list)
            List containing the values given in input
    """
    print(single_value)
    print(type(single_value))
    if type(single_value) is 'list':
        list_value = single_value
    elif isinstance(single_value, str):
        list_value = [single_value]
    else:
        print('Noting')
        list_value = single_value
    print(' ')
    print(list_value)
    print(type(list_value))
    return list_value



# ToDo:
def check_instrument(instrument):
    """Given an instrument name, it checks if it is
    a valid entry

    Args:
        instrument (str):
            Instrument name you want to check

    Returns:
        is_instrument (np:bool):
            True if it is a valid instrument
    """
    instrument_list = ['MUSE', 'SINFONI']
    if instrument in instrument_list:
        is_instrument = True
    else:
        is_instrument = False
        msgs.error('Wrong instrument name')
    return is_instrument
'''
