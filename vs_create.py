import argparse
from avi.sdk.avi_api import ApiSession
from requests import urllib3

urllib3.disable_warnings()

#Get Api Session
api = ApiSession.get_session('10.10.30.63','admin','Admin@123',tenant='admin', api_version="17.2.10")

c = 0
try:
    for i in range(1,254):
         for j in range(1,254):
            c += 1
            print str(c) + ': ',
            pool = 'pool-%d.%d' %(i,j)
            addr = '10.92.%d.%d' %(i,j)

            resp = api.get_object_by_name('pool', pool)
            if resp == None:
                #Create Pool_obj to pass in POST request
                pool_obj = {'name': pool, 'servers': [ { 'ip' : { 'addr': addr, 'type': 'V4' }}]}
                resp = api.post('pool', data=pool_obj)
                if resp.status_code in range(200, 299):
                    print pool + ' created',
                else:
                    print pool + ' failed to created',
            else:
                print pool + ' already exists ',

            #Getting the Refernce for the Pool
            pool_obj = api.get_object_by_name('pool', pool)
            pool_ref = api.get_obj_ref(pool_obj)

            #Creating SERVICE_OBJ
            services_obj = [{'port': 80, 'enable_ssl': False}]

            vs_name = 'my_vs-%d.%d' %(i,j)
            addr2 = '10.91.%d.%d' %(i,j)

            resp2 = api.get_object_by_name('virtualservice', vs_name)
            if resp2 == None:
                #Creating VS OBJ
                vs_obj = {'name': vs_name, 'vip' : [ {'ip_address': {'addr': addr2, 'type': 'V4'}}], 'services': services_obj, 'pool_ref': pool_ref}
                #Posting VS OBJ
                resp3 = api.post('virtualservice', data=vs_obj)
                if resp3.status_code in range(200, 299):
                    print vs_name + ' created'
                else:
                    print vs_name + ' failed to created'
            else:
                print vs_name + ' already exists'

except KeyboardInterrupt:
    print '\nScript killed by user'
