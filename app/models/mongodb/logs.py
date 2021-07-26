from app.models.mongodb.base import Base,db


class Logs(Base):
    """ meta = {
        # 数据库名
        "db_alias": "dev_fua",
        # 表名
        'collection': 'requestlogs',
        # id排序
        'ordering': ['-id'],
        # 自动修改表内容
        'strict': True
    } """
    user = db.StringField()
    ip = db.StringField()
    path = db.StringField()
    host = db.StringField()
    method = db.StringField()
    params = db.StringField()


'''
https://www.cnblogs.com/clbao/p/11640658.html
查询所有数据使用 all() 方法

todos = Todo.objects().all()
查询满足某些条件的数据

task = 'cooking'
todo = Todo.objects(task=task).first()

添加数据使用 save() 方法

todo1 = Todo(task='task 1', is_completed=False)
todo1.save()

排序使用 order_by() 方法

todos = Todo.objects().order_by('create_at')

更新数据需要先查找数据，然后再更新

task = 'task 1'
todo = Todo.objects(task=task).first()  # 先查找
if not todo:
    return "the task doesn't exist!"

todo.update(is_completed=True)   # 再更新

删除数据使用 delete() 方法：先查找，再删除

task = 'task 6'
todo = Todo.objects(task=task).first()  # 先查找
if not todo:
    return "the task doesn't exist!"

todo.delete()   # 再删除

分页可结合使用 skip() 和 limit() 方法

skip_nums = 1
limit = 3

todos = Todo.objects().order_by(
    '-create_at'
).skip(
    skip_nums
).limit(
    limit
)

使用 paginate() 方法

def view_todos(page=1):
    todos = Todo.objects.paginate(page=page, per_page=10)

''' 