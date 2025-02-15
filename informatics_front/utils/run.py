import os
import gzip
import codecs
from enum import Enum

contest_path = '/home/judges/contests_var/'
protocols_path = 'var/archive/xmlreports'
audit_path = 'var/archive/audit'
sources_path = 'var/archive/runs'
output_path = 'var/archive/output'


class EjudgeStatuses(Enum):
    OK = 0
    CE = 1
    RE = 2
    TL = 3
    PE = 4
    WA = 5
    CF = 6
    PARTIAL = 7
    AC = 8
    IGNORED = 9
    DISQUALIFIED = 10
    PENDING = 11
    ML = 12
    SECURITY_ERROR = 13
    STYLE_VIOLATION = 14
    WALL_TIME_LIMIT_EXCEEDED = 15
    PENDING_REVIEW = 16
    REJECTED = 17
    SKIPPED = 18
    RUNNING = 96
    COMPILING = 98
    IN_QUEUE = 377
    RMATICS_SUBMIT_ERROR = 520


def read_file_unknown_encoding(file_name, size=255):
    try:
        f = codecs.open(file_name, 'r', encoding='utf-8')
        res = f.read(size)
    except UnicodeDecodeError as err:
        error_str = str(err)
        f = codecs.open(file_name, 'r', encoding='koi8-r')
        res = f.read(size)
    return res


def get_protocol_from_file(filename):
    if os.path.isfile(filename):
        myopen = open
    else:
        filename += '.gz'
        myopen = gzip.open
    try:
        xml_file = myopen(filename, 'rb', encoding='utf-8')
        try:
            xml_file.readline()
            xml_file.readline()
            res = xml_file.read()
            try:
                return str(res, encoding='UTF-8')
            except TypeError:
                return res
        except Exception as e:
            return str(e)
    except IOError as e:
        return str(e)


def lazy(func):
    """
    A decorator function designed to wrap attributes that need to be
    generated, but will not change. This is useful if the attribute is
    used a lot, but also often never used, as it gives us speed in both
    situations.
    """
    def cached(self, *args):
        name = "_"+func.__name__
        try:
            return getattr(self, name)
        except AttributeError as e:
            pass

        value = func(self, *args)
        setattr(self, name, value)
        return value
    return cached


def get_protocol_from_file(filename):
    if os.path.isfile(filename):
        myopen = open
    else:
        filename += '.gz'
        myopen = gzip.open
    try:
        xml_file = myopen(filename, 'r')
        try:
            xml_file.readline()
            xml_file.readline()
            res = xml_file.read()
            try:
                return str(res, encoding='UTF-8')
            except TypeError:
                return res
        except:
            return ''
    except IOError:
        return ''


def get_string_status(s):
    return {
        "OK" : "OK",
        "WA" : "Неправильный ответ",
        "ML" : "Превышение лимита памяти",
        "SE" : "Security error",
        "CF" : "Ошибка проверки,<br/>обратитесь к администраторам",
        "PE" : "Неправильный формат вывода",
        "RT" : "Ошибка во время выполнения программы",
        "TL" : "Превышено максимальное время работы",
        "WT" : "Превышено максимальное общее время работы",
        "SK" : "Пропущено"
    }[s]


def get_lang_ext_by_id(lang_id):
    langs = {
        1: ".pas",
        2: ".c",
        3: ".cpp",
        8: ".dpr",
        23: ".py",
        24: ".pl",
        18: ".java",
        25: ".cs",
        26: ".rb",
        22: ".php",
        27: ".py",
        28: ".hs",
        30: ".pas",
        29: ".bas",
        31: ".1c"
    }
    return langs.get(lang_id, str())


def get_lag_exts():
    return [".pas", ".c", ".cpp", ".dpr", ".py", ".pl", ".java",
            ".cs", ".rb", ".php", ".py", ".hs", ".pas", ".bas", ".1c"]


def get_lang_name_by_id(lang_id):
    lang_names = {
        1: "Free Pascal 2.6.2",
        2: "GNU C 11.2",
        3: "GNU C++ 11.2",
        7: "Turbo Pascal",
        8: "Borland Delphi 6 - 14.5",
        9: "Borland C",
        10: "Borland C++",
        18: "Java JDK 1.7",
        22: "PHP 5.2.17",
        23: "Python 2.7",
        24: "Perl 5.10.1",
        25: "Mono C# 2.10.8.0",
        26: "Ruby 1.8.7",
        27: "Python 3.3",
        28: "Haskell GHC 7.4.2",
        29: "FreeBASIC 1.00.0",
        30: "PascalABC 1.8.0.496",
        31: "1C 8.3"
    }
    return lang_names.get(lang_id, str())


def submit_path(tp, contest_id, submit_id):
    # path to archive file with path to archive directory = tp, look up audit_path etc constants
    return os.path.join(
        contest_path,
        '0' * (6 - len(str(contest_id))) + str(contest_id),
        tp,
        to32(submit_id // 32 // 32 // 32 % 32),
        to32(submit_id // 32 // 32 % 32),
        to32(submit_id // 32 % 32),
        '0' * (6 - len(str(submit_id))) + str(submit_id)
    )


def safe_open(path, tp, encoding=None):
    """
    Function to open file with path is equal to parameter path. It tries to open as plain file,
    then as gz archive. Returnes a filelike object.
    """
    try:
        file = open(path, tp, encoding=encoding)
    except FileNotFoundError as e:
        file = gzip.open(path + '.gz', tp, encoding=encoding)
    return file


def to32(num):
    if num < 10:
        return str(num)
    else:
        return chr(ord('A') + num - 10)
