# pipenv install flask-redis
from flask_redis import FlaskRedis

db = FlaskRedis()

"""
1.配置集群
app.config['REDIS_CLUSTER'] = [
    {'host': '127.0.0.1', 'port': '7000'},
    {'host': '127.0.0.1', 'port': '7001'},
    {'host': '127.0.0.1', 'port': '7002'},
]
app.redis_cluster = StrictRedisCluster(startup_nodes=app.config['REDIS_CLUSTER'])

2.配置主从
# redis哨兵
app.config['REDIS_SENTINELS'] = [
    ('127.0.0.1', '26380'),
    ('127.0.0.1', '26381'),
    ('127.0.0.1', '26382'),
]
app.config['REDIS_SENTINEL_SERVICE_NAME'] = 'mymaster'
_sentinel = Sentinel(app.config['REDIS_SENTINELS'])
app.redis_master = _sentinel.master_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])
app.redis_slave = _sentinel.slave_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])

# Cache Aside
# 用户信息缓存
def user_info_cache(user_id):
    redis_key = 'user:{}:profile'.format(user_id)
    ret_data = current_app.redis_cluster.get(redis_key)
    if ret_data:
        # 如果存在数据，直接返回
        return json.loads(ret_data.decode())
    else:
        user = User.query.get(user_id)
        user_data = {
            "user_id": user.id,
            "mobile": user.mobile,
            "user_name": user.name,
            "photo": user.profile_photo
        }
        current_app.redis_cluster.setex(redis_key, 10 + random.randint(1, 30), json.dumps(user_data))
        return user_data


缓存工具
class UserProfileCache(object):
    def __init__(self, user_id):
        self.key = 'user:{}:profile'.format(user_id)
        self.user_id = user_id

    def save(self, user=None, force=False):

        # 使用redis集群做为缓存层
        rc = current_app.redis_cluster

        # 从数据库查询用户信息
        user = User.query.options(load_only(User.name,
                                            User.mobile,
                                            User.profile_photo,
                                            User.is_media,
                                            User.introduction,
                                            User.certificate)) \
            .filter_by(id=self.user_id).first()

        # 用户不存在返回None
        if user is None:
            # 如果用户为空，设置为-1，防止缓存攻击
            rc.setex(self.key, constants.UserProfileCacheTTL.get_val(), -1)
            return None

        # 组装用户信息数据
        user_data = {
            'mobile': user.mobile,
            'name': user.name,
            'photo': user.profile_photo or '',
            'is_media': user.is_media,
            'intro': user.introduction or '',
            'certi': user.certificate or '',
        }

        # 添加填充字段
        user_data = self._fill_fields(user_data)
        try:
            # 把用户信息设置到redis集群缓存中
            rc.setex(self.key, constants.UserProfileCacheTTL.get_val(), json.dumps(user_data))
        except RedisError as e:
            current_app.logger.error(e)
        return user_data

    def get(self):
        rc = current_app.redis_cluster
        try:
            # 从集群中获取用户数据
            ret = rc.get(self.key)
        except RedisError as e:
            # 如果连接redis异常，写日志，把ret设置为None, 继续从数据库中获取数据
            current_app.logger.error(e)
            ret = None
        if ret:
            # 缓存中有用户数据(命中)
            user_data = json.loads(ret)
        else:
            # 缓存中没有获取到用户信息，从数据库中获取
            user_data = self.save(force=True)

        if not user_data['photo']:
            # 如果没有用户头像，设置默认头像
            user_data['photo'] = constants.DEFAULT_USER_PROFILE_PHOTO
        # 组装完整的头像链接
        user_data['photo'] = current_app.config['QINIU_DOMAIN'] + user_data['photo']
        return user_data

    def _fill_fields(self, user_data):
        user_data['art_count'] = UserArticlesCountStorage.get(self.user_id)
        user_data['follow_count'] = UserFollowingsCountStorage.get(self.user_id)
        user_data['fans_count'] = UserFollowersCountStorage.get(self.user_id)
        user_data['like_count'] = UserLikedCountStorage.get(self.user_id)
        return user_data

    def clear(self):
        try:
            current_app.redis_cluster.delete(self.key)
        except RedisError as e:
            current_app.logger.error(e)

    def exists(self):
        rc = current_app.redis_cluster

        try:
            # 从redis获取用户数据
            ret = rc.get(self.key)
        except RedisError as e:
            current_app.logger.error(e)
            ret = None

        if ret is not None:
            # 如果获取到的用户数据为-1，证明用户不存在，只是为了防止缓存攻击而设置为-1
            return False if ret == b'-1' else True
        else:
            # 缓存中未查到，再从数据库中查询
            user_data = self.save(force=True)
            if user_data is None:
                # 用户不存在
                return False
            else:
                # 用户存在
                return True


用户关注信息缓存
def following_cache(user_id):
    key = {"user:{}:followings".format(user_id)}
    relations = Relation.query.options(
        load_only(Relation.target_user_id, Relation.utime)
    ).filter(
        Relation.user_id == user_id,
        Relation.relation == Relation.RELATION.FOLLOW
    ).order_by(Relation.utime.desc()).all()
    followings = []
    cache = []
    for relation in relations:
        # 组装关注列表. [target_user_id1, target_user_id2]
        followings.append(relation.target_user_id)
        # 组装zadd命令要用到的数据. [score1, member1, socre2, member2]
        cache.append(relation.utime.timestamp())
        cache.append(relation.target_user_id)

    pl = current_app.redis_cluster.pipeline()
    if cache:
        try:
            pl.delete(key)
            # zadd(self.key, score1, member1, score2, member2)
            pl.zadd(key, *cache)
            # 设置缓存时间
            pl.expire(key, 5 * 60)
            results = pl.execute()
            if results[0] and not results[1]:
                pl.delete(key)
        except RedisError as e:
            current_app.logger.error(e)
    else:
        # 如果不存在关注列表，也往redis中插入一条，member为-1(防止缓存攻击)
        pl.zadd(key, 1, -1)
        pl.expire(key, 5 * 60)

    return followings

缓存工具
class UserFollowingCache(object):
    def __init__(self, user_id):
        self.key = 'user:{}:following'.format(user_id)
        self.user_id = user_id

    def save(self):
        rc = current_app.redis_cluster
        # redis中没有关注数据，再从数据库中查询
        ret = Relation.query.options(load_only(Relation.target_user_id, Relation.utime)) \
            .filter_by(user_id=self.user_id, relation=Relation.RELATION.FOLLOW) \
            .order_by(Relation.utime.desc()).all()

        followings = []
        cache = []
        for relation in ret:
            # 组装关注列表. [target_user_id1, target_user_id2]
            followings.append(relation.target_user_id)
            # 组装zadd命令要用到的数据. [score1, member1, socre2, member2]
            cache.append(relation.utime.timestamp())
            cache.append(relation.target_user_id)

        if cache:
            # 如果存在关注数据，把关注列表数据缓存到redis集群中
            try:
                # 使用pipeline执行redis事务
                pl = rc.pipeline()
                # zadd(self.key, score1, member1, score2, member2)
                pl.zadd(self.key, *cache)
                # 设置缓存时间
                pl.expire(self.key, constants.UserFollowingsCacheTTL.get_val())
                # 执行redis事务
                pl.execute()
            except RedisError as e:
                current_app.logger.error(e)
        else:
            # 如果不存在关注列表，也往redis中插入一条，member为-1(防止缓存攻击). 在获取用户信息的时候过滤一下即可
            rc.zadd(self.key, 1, -1)
            rc.expire(self.key, constants.UserFollowingsCacheTTL.get_val())

        return followings

    def get(self):
        rc = current_app.redis_cluster

        try:
            # 获取用户所有的关注id列表
            ret = rc.zrevrange(self.key, 0, -1)
        except RedisError as e:
            current_app.logger.error(e)
            ret = None

        if ret:
            # 从redis中获取到的都是bytes数据类型，用户id是整形，需要转换再返回
            followings = []
            for uid in ret:
                # 把-1过滤掉
                target_user_id = int(uid)
                if target_user_id != -1:
                    followings.append(target_user_id)
            return followings
        else:
            # 如果redis中没有获取到，再从数据库中查询
            followings = self.save()
            return followings

    def update(self, target_user_id, timestamp, increment=1):

        更新用户的关注缓存数据
        :param target_user_id: 被关注的目标用户
        :param timestamp: 关注时间戳
        :param increment: 增量
        :return:

        rc = current_app.redis_cluster

        try:
            # increment > 0表示关注，< 0 表示取消关注
            if increment > 0:
                rc.zadd(self.key, timestamp, target_user_id)
            else:
                rc.zrem(self.key, target_user_id)
        except RedisError as e:
            current_app.logger.error(e)


"""
