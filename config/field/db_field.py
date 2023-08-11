
class BASIC:
    ID = "id"
    NAME = "name"
    DESC = "desc"
    LABEL = "label"
    MODULE = "module"
    MODULE_ID = "module_id"
    LABEL_ID_LIST = "label_id_list"
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
    ENVIRONMENT_ID = "environment_id"

    CASE = "case"

class CASE(BASIC):
    TERMINATION = "termination"
    VARIABLE = "variable"
    PLAN_ID = "planId"
    STEP = "step"

class STEP(BASIC):
    NUMBER = "number"
    STEP_TYPE = "step_type"
    TYPE = "type"
    TERMINATION = "termination"
    PARAMS = "params"
    SLEEP = "sleep"
    CASE_ID = "caseId"

    RETRY = "retry"

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
    TYPE = "type"
    PARAMS = "params"

class ENVIRONMENT(BASIC):
    VALUE = "value"



class RETRY:
    INTERVAL = "interval"
    TIMES = "times"
    JUMP = "jump"

class PLUGIN:
    TYPE = "type"
    PARAMS = "params"

    LOGIN = "login"
    RANDOM = "random"
    PG_DB = "pg_db"


class HANDLERS_TYPE:
    ASSERTS = "asserts"
    EXTRACT = "extract"
    CALC = "calculate"
    EXT_ASSERT = "ext_asserts"
class STEP_TYPE:
    REQUEST = "request"
    PLUGIN = "plugIn"

class POST_TYPE:
    JSON = "json"
    UPLOAD = "upload"
    FORM = "form"

class RES_TYPE:
    HTML = "html"
    JSON = "json"
    TEXT = "text"

    DOWN = "down"

class UPLOAD:
    FILE_FIELDS = "file_fields"
    PARAMS = "params"
    FILE_ID = "file_id"
    FILE_TYPE = "file_type"

    FORM_DATA = "form-data"

class LOGIN_PLUG:
    USER_NAME = "user_name"
    PASS_WORD = "pass_word"
    VENV = "venv"
    COOKIES_FIELD = "cookies_field"
    CODE = "code"
    HOST = "host"

class HOST:
    TEST = "https://d-k8s-sso-fp.bigfintax.com"
    REPORT_SERVER = "http://0.0.0.0:9000/user_report"
    LOG_SERVER = "http://0.0.0.0:9000/log_server"


class OTHER:
    BASICS = "basics"
    CHU_LI_QI = "处理器"
    YANG_ZHENG_QI = "验证器"
    TI_QU_QI = "提取器"
    TI_QU__YAN_ZHENG_QI = "提取验证器"
    JI_SUN_QI = "计算器"
    BU_ZHOU_CHAN_JIAN = "步骤插件"
    CE_SI_JI_HUA = "测试计划"
    CE_SI_YONG_LI = "测试用例"
    YONG_LI_BU_ZHOU = "步骤"
    JIE_KOU_QING_QIU = "接口请求"
    JIE_GUO_BAO_GAO = "结果报告"

class RANDOM:
    RANDOM_TYPE = "random_type"  # 类型 STR：随机的大写字符串，str随机的小写字符串，Str随机的大小写字符串，int随机的数字字符串【可能出现："0001558"】
    LENGTH = "length"  # 长度
    GET_FIELD = "get_field"  # 保留字段

    RANDOM_STR = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    RANDOM_str = "abcdefghijklmnopqrstuvwxyz"
    RANDOM_int = "1234567890"

class PG_DB:
    HOST = "host"
    USER = "user"
    PASSWORD = "password"
    DB_NAME = "db_name"
    SQL = "SQL"
    PORT = "port"
    FIELD_LIST = "field_list"

    ROW = "row"
    COL = "col"
    FIELD = "field"
    RESPONSE = "response"

class CALC:
    FIELD = "field"
    VALUE_LEFT = "value_left"
    VALUE_RIGHT = "value_right"
    FUNC = "func"


class EXTRACT:
    FIELD = "field"
    PATH = "path"
    CONDITION = "condition"
    iCONDITION = "iCondition"
    TYPE = "type"
    VALUE = "value"

class ASSERTS:
    VALUE_LEFT = "value_left"
    VALUE_RIGHT = "value_right"
    FUNC = "func"