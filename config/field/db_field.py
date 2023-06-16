class BASIC:
    ID = "id"
    NAME = "name"
    COMMENT = "comment"
    LABEL = "label"
    LABEL_NAME = "label_name"
    MODULE_NAME = "module_name"
    MODULE_ID = "module_id"
    MODULE = "module"
    UPDATED_TIME = "updated_time"
    CREATED_TIME = "created_time"
    UPDATE_USER = "update_user"
    CREATE_USER = "create_user"
    IS_USER = "is_user"
    DESC = "desc"

    created_time = "created_time"
    updated_time = "updated_time"
    create_user = "create_user"
    update_user = "update_user"



class STEP:
    NUMBER = "number"
    STEP_TYPE = "step_type"
    WAIT = "wait"

    INTERFACE = "interface"
    CASE_ID = "case_id"
    HANDLERS = "handlers"

    AREA = "area"
    OPERATE = "operate"



class METHOD:
    POST = "POST"
    GET = "GET"


class UI_AREA(BASIC):
    LOCATE_PARAMS = "locate_params"
    LOCATE_TYPE = "locate_type"
    STEP_ID = "step_id"


class UI_OPERATE(BASIC):
    ACTION = "action"
    PARAMS = "params"
    OPERATE_TYPE = "operate_type"
    SLEEP = "sleep"
    STEP_ID = "step_id"

class PLAN(BASIC):
    CASE_ID = "case_id"
    CASE = "case"
    VARIABLE = "variable"
    ENVIRONMENT = "environment"

class CASE(BASIC):
    PLAN_ID = "plan_id"
    STEP = "step"
    NUMBER = "number"
    CASE_TYPE = "case_type"
    VARIABLE = "variable"

class INTER_FACE(BASIC):
    NUMBER = "number"
    STEP = "step"
    DOC_URL = "doc_url"
    STEP_ID = "step_id"
    HOST = "host"
    PATH = "path"
    METHOD = "method"
    HEADERS = 'headers'
    PARAMS = "params"
    COOKIES = "cookies"

class PLUGIN(BASIC):
    PARAMS = "params"

class HANDLERS(BASIC):
    STEP_ID = "step_id"
    HANDLERS_TYPE = "handlers_type"
    PARAMS = "PARAMS"


class ENVIRONMENT(BASIC):
    VALUE = "value"

class CASE_TYPE:
    FACE = "face"
    UI = "UI"



class PLAN_TYPE:
    FACE = "face"
    UI = "UI"

