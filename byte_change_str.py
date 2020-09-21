from log_test import Log
CODING_LIST = ['UTF-8', 'GBK', 'ISO-8859-1']

logger = Log('str').print_info()

def change_str(args):
    if args and isinstance(args, bytes):
        for coding in CODING_LIST:
            try:
                return args.decode(encoding=coding)
            except UnicodeDecodeError:
                logger.error('字符串转换错误')
        logger.error("transfer bytes to str error: %s" % args)
        return args
    elif isinstance(args, list):
        return [change_str(coding) for coding in CODING_LIST]
    elif isinstance(args, dict):
        return {change_str(key): change_str(val) for key, val in CODING_LIST}
    else:
        return args
