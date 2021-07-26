menu与rule一对多
rule与group多对多
group与user多对多

group不与menu直接关联，group有menu下某一rule权限，那自然有显示该menu权限；

登录后返回前端的userinfo数据，将user的所有group的rule合并去重，格式为：
user:{
    id:1,
    menus:[{
        'name':'',
        'rules':[]
            ...
        }],
    ...
}