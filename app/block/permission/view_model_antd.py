# -*- coding:utf-8 -*-
from flask import current_app
from app.view_model.ui_structure.antd_struct import AntdPageBase,AntdListBase
from .view_model import MenuViewModel



# menu
class MenuAntdCollection(AntdListBase):
        
    def fillantd(self,original):
        antdoriginal={}
        antdoriginal['dataSource']=[MenuViewModel(menu) for menu in original['menus']]
        antdoriginal['meta']={
            'total':len(original),
            'pageSize':original['pageSize'] or current_app.config['PER_PAGE'],
            'current':original['current'] or 1
        }
        antdoriginal['page']={'title':'菜单','type':'menuList','searchBar':True}
        antdoriginal['tableColumn']==[
            {'title':'NO','dataIndex':'id','key':'id','hideInColumn':False,'type':'text'},
            {'title':'父级','dataIndex':'parent_id','key':'parent_id','hideInColumn':True,'type':'text'},
            {'title':'名称','dataIndex':'name','key':'name','hideInColumn':False,'type':'text'},
            {'title':'备注','dataIndex':'remark','key':'remark','hideInColumn':False,'type':'text'},
            {'title':'图标','dataIndex':'icon','key':'icon','hideInColumn':True,'type':'text'},
            {'title':'路径','dataIndex':'path','key':'path','hideInColumn':False,'type':'text'},
            {'title':'组件','dataIndex':'component','key':'component','hideInColumn':True,'type':'text'},
            {'title':'排序','dataIndex':'sort','key':'sort','hideInColumn':True,'type':'text'},
            {'title':'创建时间','dataIndex':'create_time','key':'create_time','hideInColumn':False,'type':'datetime'},
            {'title':'操作','dataIndex':'actions','key':'actions','hideInColumn':False,'type':'actions','actions':[
                {'component':'button','text':'编辑','type':'primary','action':'modal','uri':'\/api\/v1\/menu\/:id','mehtod':'put'},
                {'component':'button','text':'删除','type':'default','action':'delete','uri':'\/api\/v1\/menu\/delete','mehtod':'delete'}
            ]}
        ]
        antdoriginal['tableToolBar']=[
            {'component':'button','text':'新建','type':'primary','action':'modal','id':'add','uri':'/api/v1/menu','mehtod':'post'},
            {'component':'button','text':'刷新','type':'default','action':'reload'}
        ]
        antdoriginal['batchToolBar']=[
            {'component':'button','text':'批量删除','type':'danger','action':'delete','uri':'\/api\/v1\/menu\/delete'}
        ]
        antdoriginal['message']=original['message']
        antdoriginal['success']=original['success']
        self.fill(antdoriginal)



class MenuAntdPage(AntdPageBase):
        
    def fillantd(self,original):
        antdoriginal={}
        antdoriginal['dataSource']=MenuViewModel(original)
        antdoriginal['page']={'title':"编辑",'type':"edit"}
        antdoriginal['tabs']=[
            {
                'name':"menu",
                'title':"菜单",
                'data':[
                    {'title':'NO','dataIndex':'id','key':'id','type':'text','disabled':True},
                    {'title':'父级','dataIndex':'parent_id','key':'parent_id','type':'text','disabled':False},
                    {'title':'名称','dataIndex':'name','key':'name','type':'text','disabled':False},
                    {'title':'备注','dataIndex':'remark','key':'remark','type':'text','disabled':False},
                    {'title':'图标','dataIndex':'icon','key':'icon','type':'text','disabled':False},
                    {'title':'路径','dataIndex':'path','key':'path','type':'text','disabled':False},
                    {'title':'组件','dataIndex':'component','key':'component','type':'text','disabled':False},
                    {'title':'排序','dataIndex':'sort','key':'sort','type':'text','disabled':False}
                ]
            }
        ]
        antdoriginal['actions']=[
            {
                'name':'actions',
                'title':'操作',
                'data':[
                    {
                        'component':'button',
                        'text':'重置',
                        'type':'dashed',
                        'action':'reset'
                    },
                    {
                        'component':'button',
                        'text':'取消',
                        'type':'default',
                        'action':'cancel'
                    },
                    {
                        'component':'button',
                        'text':'提交',
                        'type':'primary',
                        'action':'submit'
                    }
                ]
            }
        ]
        antdoriginal['message']=original['message']
        antdoriginal['success']=original['success']
        self.fill(antdoriginal)
