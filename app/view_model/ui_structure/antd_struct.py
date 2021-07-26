# -*- coding:utf-8 -*-

class AntdListBase:
    def __init__(self):
        self.message=''
        self.success=False
        self.data={}

    def fill(self,original):
        dataSource=original['dataSource']
        meta=original['meta']
        page=original['page']
        layout={
            'tableColumn':original['tableColumn'],
            'tableToolBar':original['tableToolBar'],
            'batchToolBar':original['batchToolBar']
        }

        self.message=original['message']
        self.success=original['success']
        self.data={
            'dataSource':dataSource,
            'layout':layout,
            'meta':meta,
            'page':page
        }




class AntdPageBase:
    def __init__(self):
        self.message=''
        self.success=False
        self.data={}
    
    def fill(self,original):
        dataSource=original['dataSource']
        page=original['page']
        layout={
            'tabs':original['tabs'],
            'actions':original['actions']
        }

        self.message=original['message']
        self.success=original['success']
        self.data={
            'dataSource':dataSource,
            'layout':layout,
            'page':page
        }