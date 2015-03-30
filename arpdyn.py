import boto.dynamodb2
from boto.dynamodb2.table import Table

try:
    from arpdynsettings import CONFIG
except ImportError:
    CONFIG['region'] = 'us-west-1'
    CONFIG['keyid'] = '<aws_access_key_id>'
    CONFIG['keysecret'] = '<aws_secret_access_key>'

# Uses your ``aws_access_key_id`` & ``aws_secret_access_key`` from either a
# config file or environment variable & the default region.
def makeusertable():
    return Table.create('users', schema=[
        HashKey('username'), # defaults to STRING data_type
        RangeKey('last_name'),
    ], throughput={
        'read': 5,
        'write': 15,
    }, global_indexes=[
        GlobalAllIndex('EverythingIndex', parts=[
            HashKey('account_type'),
        ],
        throughput={
            'read': 1,
            'write': 1,
        })
    ],
    connection=boto.dynamodb2.connect_to_region(
        CONFIG['region'],
        aws_access_key_id=CONFIG['keyid'],
        aws_secret_access_key=CONFIG['keysecret'])
    )

def opentable():
    return Table('mac', 
        connection=boto.dynamodb2.connect_to_region(
            CONFIG['region'],
            aws_access_key_id=CONFIG['keyid'],
            aws_secret_access_key=CONFIG['keysecret'])
        )

mac = opentable()

