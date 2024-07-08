#Main software file. It loads the arguments, the configuration, 

import argparse




def get_args():
    # Get the arguments
    parser = argparse.ArgumentParser(description='Dark Data Search toolkit, version 3, software developed for the search and analysis of dark data at LDCS/LDMX.', formatter_class=argparse.RawDescriptionHelpFormatter)

    # Add the arguments
    #Retrive the RSE to use for the dark data search
    parser.add_argument('--rse', dest='rse', action='store', help='RSE to use for the dark data search', required=True)

    args = parser.parse_args()
    return args