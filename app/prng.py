# @file         prng.py
# @description  This file will handle all the requests to /prng
#               The GET request to /prng must have the parameters
#               type and length at all times.
#               Generates pseudo random numbers using the python builtin
#               random number generator.
# @author       Eshan Shafeeq

from app import app
from flask import request
import json
import random

# @function validate_data_type
# @param    data_type   the type of random number to be return to the user
# @return   if the data_type is of a valid type will return true, otherwise false.
def validate_data_type( data_type ):
    if data_type == 'uint8':
        return True
    if data_type == 'uint16':
        return True
    if data_type == 'hex16':
        return True
    return False

# @function validate_numeric_param
# @param    param       The numeric paramter which requires to be validated whether its
#                       its in the acceptable range, and is not None.
# @return   on passing all the validation requrements will return true, else false.
def validate_numeric_param( param ):
    if param == None:
        return False
    if param < 0:
        return False
    if param > 1024:
        return False

    return True

# @function get_random_numbers
# @param    num_max     The maximum value which will be used to generate the random number.
# @param    num_values  The number of random numbers to be generated
# @return   will return an array of random numbers from 0 to num_max. The array size will be
#           num_values
def get_random_numbers( num_max, num_values ):
    return map(lambda x: random.randint(0, num_max), [None] * num_values)

# @function get_random_hex
# @param    num_max     The maximum value which will be used to generate the random hexadecimal.
# @param    num_values  The number of random hexadecimals to be generated
# @return   will return an array of random hexadecimals from 0 to num_max. The array size will be
#           num_values
def get_random_hex( num_max, num_values ):
    return map( lambda x: hex(get_random_numbers( num_max, 1 )[0]), [None] * num_values)

# @function prng_handler
# @param    params      A dictionary of all the parameters recieved via the get request.
# @return   will return false if any problems occur, but otherwise will return the required
#           set of random numbers for the given array size.
def prng_handler( params ):

    if not validate_data_type( params['data_type'] ):
        return False

    if not validate_numeric_param( params['array_length']):
        return False

    # i did not manage to find out what this was just yet!
    #if params['data_type'] == 'hex16':
    #    if not validate_numeric_param( params['block_size']):
    #        return False

    if params['data_type'] == 'uint8':
        return get_random_numbers( 255, params['array_length'] )
    if params['data_type'] == 'uint16':
        return get_random_numbers( 65535, params['array_length'] )
    if params['data_type'] == 'hex16':
        return get_random_hex( 65535, params['array_length'] )


# @function     prng
# @route        /prng
# @description  will handle the requests to /prng, and will call the prng_handler to get the required data
#               for the requested response.
@app.route('/prng', methods=['GET'])
def prng():
    params={}

    try:
        params['data_type']=request.args.get('type')
        params['array_length']=int(request.args.get('length'))
    except Exception as e:
        return json_dumps({'success':False})

    try:
        params['block_size']=int( request.args.get('size'))
    except Exception as e:
        params['block_size']=None

    result = prng_handler( params )
    response={}
    if result == False:
        response['success']=False
    else:
        response['success']=True
        response['type']=params['data_type']
        response['length']=params['array_length']
        response['data']=result

    return json.dumps(response)

