def obj_to_post(obj, flag=True):
    """
    obj 의 각 속성을 serialize 해서, dict 로 변환한다.
    serialize: python object --> (기본 타입) int, float, str
    :param obj:
    :param flag: True (모두 보냄, /api/post/99/ 용), False (일부 보냄, /api/post/list/ 용)
    :return:
    """
    post = dict(vars(obj))

    if obj.category:
        post['category'] = obj.category.name
    else:
        post['category'] = 'NoCategory'

    if obj.tags:
        post['tags'] = [t.name for t in obj.tags.all()]
    else:
        post['tags'] = []

    if obj.image:
        post['image'] = obj.image.url
    else:
        post['image'] = 'https://via.placeholder.com/900x300/'

    if obj.updated_at:
        post['updated_at'] = obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        post['updated_at'] = '9999-12-31 00:00:00'

    del post['_state'], post['category_id'], post['created_at'], post['_prefetched_objects_cache']
    if not flag:
        del post['tags'], post['updated_at'], post['description'], post['content']

    return post


def prev_next_post(obj):
    try:
        prevObj = obj.get_previous_by_updated_at()
        prevDict = {
            'id': prevObj.id,
            'title': prevObj.title,
        }
    except obj.DoesNotExist:
        prevDict = {}

    try:
        nextObj = obj.get_next_by_updated_at()
        nextDict = {
            'id': nextObj.id,
            'title': nextObj.title,
        }
    except obj.DoesNotExist:
        nextDict = {}

    return prevDict, nextDict


def obj_to_comment(obj):
    """ comment 객체를 serialize 한다. """
    comment = dict(vars(obj))

    if obj.updated_at:
        comment['updated_at'] = obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        comment['updated_at'] = '9999-12-31 00:00:00'

    del comment['_state'], comment['post_id'], comment['created_at']

    return comment
