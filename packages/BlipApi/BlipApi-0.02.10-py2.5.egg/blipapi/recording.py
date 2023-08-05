# -*- coding: utf-8 -*-
# $Id: recording.py 200 2010-04-21 15:51:05Z urzenia $
#
# Blip! (http://blip.pl) communication library.
# Author: Marcin Sztolcman <marcin /at/ urzenia /dot/ net>
# Version: 0.02.10
# Copyright: (r) 2009 Marcin Sztolcman
# License: http://opensource.org/licenses/gpl-license.php GNU Public License v.2

def read (**args):
    """ Get info about record from specified update. """

    if not args.get ('id'):
        raise ValueError ('Update ID is missing.')

    return dict (
        url     = '/users/' + str (args['id']) + '/recording',
        method  = 'get',
    )

