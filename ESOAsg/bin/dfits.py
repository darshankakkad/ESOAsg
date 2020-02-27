#!/usr/bin/env python3

import argparse

from astropy import coordinates
from astropy import units as u
# import numpy as np

from ESOAsg.core import download_archive
from ESOAsg import msgs
from ESOAsg import __version__

# from IPython import embed


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=r"""
        This macro mimic the behaviour of ESO's `dfits` and `grep`, i.e. to show on terminal (and on a file if
        requested) the header of a fits file. If the option `check_cards` is enabled, only the selected list of header
        cards will be printed (i.e., the result of:
        > `dfits test.fits | grep PRODCATG > test_header.txt `
        and of
        > `dfits.py -i test.fits -c ['PRODCATG'] -o test_header.txt`
        should be identical.
        
        This uses ESOAsg version {:s}
        """.format(__version__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EXAMPLES)

    parser.add_argument('-i', '--input_fits', nargs='+', type=str, default=None,
                        help='Fits file name form which read the header')
    parser.add_argument('-hn', '--hdu_number', nargs='+', type=int, default=0,
                        help='select from which HDU you are getting the header. See `fitsfiles` in `ESOAsg.core` for '
                             'further details.')
    parser.add_argument('-c', '--cards', nargs='+', type=str, default=None,
                        help='List of header cards to be extracted')
    parser.add_argument('-o', '--output_text', nargs='+', type=str, default=None,
                        help='Result will be saved in this text file')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    return parser.parse_args()


EXAMPLES = r"""
        Example:
        dfits.py -i test.fits -c ['PRODCATG'] -o test_header.txt
        """

if __name__ == '__main__':
    args = parse_arguments()
    msgs.start()
    msgs.info('RA and Dec query for ESO archival data')
    msgs.newline()
    position = coordinates.SkyCoord(ra=args.ra_deg*u.degree, dec=args.dec_deg*u.degree, frame='fk5')
    result_from_query = download_archive.query_from_radec(position, args.radius)
    if args.instrument_name is not None:
        if len(args.instrument_name) > 1:
            msgs.error('Too many instrument. Only one allowed')
        instrument_name = str(args.instrument_name[0])
        msgs.info('Limit search to {} only data'.format(instrument_name))
        select_by_instrument = (result_from_query['instrument_name'].data == instrument_name.encode('ascii'))
        download_archive.download(result_from_query['dp_id'][select_by_instrument])
    if len(result_from_query['dp_id']) > 0:
        download_archive.download(result_from_query['dp_id'])
    msgs.end()
