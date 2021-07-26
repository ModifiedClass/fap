class RootPage:
    success=False
    message=''
    data={}


class RespList(RootPage):

    dataSource=[]
    field={}
    layout={}
    tableColumn=[]
    column={}
    tableToolBar=[]
    batchToolBar=[]
    meta={}
    page={}


class RespPage(RootPage):

    page={}
    layout={}
    tabs=[]
    tab={}
    actions=[]
    dataSource={}