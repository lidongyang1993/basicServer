
class BASIC:
    ID = "id"
    NAME = "name"
    DESC = "desc"
    LABEL = "label"
    MODULE = "module"
    UPDATED_TIME = "updated_time"
    CREATED_TIME = "created_time"
    UPDATE_USER = "update_user"
    CREATE_USER = "create_user"
    IS_USER = "is_user"


class METHOD:
    POST = "POST"
    GET = "GET"

class PLAN(BASIC):
    CASE_ID = "case_id"
    VARIABLE = "variable"
    ENVIRONMENT = "environment"


    CASE = "case"

class CASE(BASIC):
    TERMINATION = "termination"
    VARIABLE = "variable"

    STEP = "step"

class STEP(BASIC):
    NUMBER = "number"
    STEP_TYPE = "step_type"
    TERMINATION = "termination"
    PARAMS = "params"
    SLEEP = "SLEEP"


    HANDLERS = "handlers"


class REQUEST:  # 接口数据
    HOST = "host"  # 测试环境服务
    URL = "url"  # 接口整合url-不用理会
    PATH = "path"  # 接口路径
    POST_TYPE = "post_type"  # post类型【json or form】
    REQ_TYPE = "req_type"  # post类型【json or form】
    RES_TYPE = "response_type"  # 结果类型【html or json】
    METHOD = "method"  # 请求方法【post， get， put……】
    DATA = "data"  # 请求数据，json格式
    HEADERS = "headers"  # 请求头，非必要，json格式
    COOKIES = "cookies"  # 保留字段

class REQ_RES_TYPE:
    HTML = "html"
    JSON = "json"
    FORM = "form"

class HANDLERS(BASIC):
    HANDLERS_TYPE = "handlers_type"
    PARAMS = "PARAMS"

class ENVIRONMENT(BASIC):
    VALUE = "value"


