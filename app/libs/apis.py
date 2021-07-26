# -*- coding:utf-8 -*-
apis = {
    'auth':{
        'client':['create_client'],
        'token':['get_token'],
        'verification_code':['verification_code']
    },
    'account':{
        'user':['get_user','delete_user'],
        'group':[]
    },
    'other':{
        'file':['upload_file','file_list','download_file','delete_file']
    }
}