from app import app
from flask import request
import json
import random


def validate_data_type( data_type ):
    if data_type == 'uint8':
        return True
    if data_type == 'uint16':
        return True
    if data_type == 'hex16':
        return True
    return False

def validate_numeric_param( param ):
    if param == None:
        return False
    if param < 0:
        return False
    if param > 1024:
        return False

    return True

def get_random_numbers( num_max, num_values ):
    return map(lambda x: random.randint(0, num_max), [None] * num_values)

def get_random_hex( num_max, num_values ):
    return map( lambda x: hex(get_random_numbers( num_max, 1 )[0]), [None] * num_values)

def prng_handler( params ):

    if not validate_data_type( params['data_type'] ):
        return False

    if not validate_numeric_param( params['array_length']):
        return False

    #if params['data_type'] == 'hex16':
    #    if not validate_numeric_param( params['block_size']):
    #        return False

    if params['data_type'] == 'uint8':
        return get_random_numbers( 255, params['array_length'] )
    if params['data_type'] == 'uint16':
        return get_random_numbers( 65535, params['array_length'] )
    if params['data_type'] == 'hex16':
        return get_random_hex( 65535, params['array_length'] )



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

