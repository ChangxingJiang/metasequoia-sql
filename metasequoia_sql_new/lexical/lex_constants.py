"""
词法解析器常量集
"""

from metasequoia_sql_new.lexical.lex_states import LexStates

__all__ = [
    "LEX_SKIP_CHARSET",
    "LEX_START_STATE_MAP",
    "LEX_IDENT_MAP",
    "LEX_BIN_CHARSET",
    "LEX_HEX_CHARSET",
    "LEX_E_CHARSET",
    "LEX_BIN_MARK_CHARSET",
    "LEX_HEX_MARK_CHARSET",
]

# 空白字符，包括空格、水平制表符、换行符
LEX_SKIP_CHARSET = {" ", "\t", "\n"}

# 当状态为 LEX_START 时，单个字符的状态转移规则
LEX_START_STATE_MAP = {
    "\x00": LexStates.LEX_EOF,  # NUL (null) 空字符【原则上不会出现】
    "\x01": LexStates.LEX_ERROR,  # SOH (start of headline) 标题开始
    "\x02": LexStates.LEX_ERROR,  # STX (start of text) 正文开始
    "\x03": LexStates.LEX_ERROR,  # ETX (end of text) 正文结束
    "\x04": LexStates.LEX_ERROR,  # EOT (end of transmission) 传输结束
    "\x05": LexStates.LEX_ERROR,  # ENQ (enquiry) 请求
    "\x06": LexStates.LEX_ERROR,  # ACK (acknowledge) 收到通知
    "\x07": LexStates.LEX_ERROR,  # BEL (bell) 响铃
    "\x08": LexStates.LEX_ERROR,  # BS (backspace) 退格键
    "\t": LexStates.LEX_SKIP,  # HT (horizontal tab) 水平制表符【原则上不会出现】
    "\n": LexStates.LEX_SKIP,  # LF (NL line feed, new line) 换行键【原则上不会出现】
    "\x0B": LexStates.LEX_ERROR,  # VT (vertical tab) 垂直制表符
    "\x0C": LexStates.LEX_ERROR,  # FF (NP form feed, new page) 换页符
    "\x0D": LexStates.LEX_ERROR,  # CR (carriage return) 回车键
    "\x0E": LexStates.LEX_ERROR,  # SO (shift out) 不用切换
    "\x0F": LexStates.LEX_ERROR,  # SI (shift in) 切换
    "\x10": LexStates.LEX_ERROR,  # DLE (data link escape) 数据链路转义
    "\x11": LexStates.LEX_ERROR,  # DC1 (device control 1) 设备控制 1
    "\x12": LexStates.LEX_ERROR,  # DC2 (device control 2) 设备控制 2
    "\x13": LexStates.LEX_ERROR,  # DC3 (device control 3) 设备控制 3
    "\x14": LexStates.LEX_ERROR,  # DC4 (device control 4) 设备控制 4
    "\x15": LexStates.LEX_ERROR,  # NAK (negative acknowledge) 拒绝接受
    "\x16": LexStates.LEX_ERROR,  # SYN (synchronous idle) 同步空闲
    "\x17": LexStates.LEX_ERROR,  # ETB (end of trans. block) 结束传输块
    "\x18": LexStates.LEX_ERROR,  # CAN (cancel) 取消
    "\x19": LexStates.LEX_ERROR,  # EM (end of medium) 媒介结束
    "\x1A": LexStates.LEX_ERROR,  # SUB (substitute) 代替
    "\x1B": LexStates.LEX_ERROR,  # ESC (escape) 换码
    "\x1C": LexStates.LEX_ERROR,  # FS (file separator) 文件分割符
    "\x1D": LexStates.LEX_ERROR,  # GS (group separator) 分组符
    "\x1E": LexStates.LEX_ERROR,  # RS (record separator) 记录分割符
    "\x1F": LexStates.LEX_ERROR,  # US (unit separator) 单元分隔符
    " ": LexStates.LEX_SKIP,
    "!": LexStates.LEX_BANG,
    "\"": LexStates.LEX_STRING_OR_DELIMITER,
    "#": LexStates.LEX_COMMENT,
    "$": LexStates.LEX_IDENT,
    "%": LexStates.LEX_PERCENT,
    "&": LexStates.LEX_AMP,
    "'": LexStates.LEX_STRING,
    "(": LexStates.LEX_LPAREN,
    ")": LexStates.LEX_RPAREN,
    "*": LexStates.LEX_STAR,
    "+": LexStates.LEX_PLUS,
    ",": LexStates.LEX_COMMA,
    "-": LexStates.LEX_SUB,
    ".": LexStates.LEX_DOT,
    "/": LexStates.LEX_SLASH,
    "0": LexStates.LEX_ZERO,
    "1": LexStates.LEX_NUMBER,
    "2": LexStates.LEX_NUMBER,
    "3": LexStates.LEX_NUMBER,
    "4": LexStates.LEX_NUMBER,
    "5": LexStates.LEX_NUMBER,
    "6": LexStates.LEX_NUMBER,
    "7": LexStates.LEX_NUMBER,
    "8": LexStates.LEX_NUMBER,
    "9": LexStates.LEX_NUMBER,
    ":": LexStates.LEX_COLON,
    ";": LexStates.LEX_SEMICOLON,
    "<": LexStates.LEX_LT,
    "=": LexStates.LEX_EQ,
    ">": LexStates.LEX_GT,
    "?": LexStates.LEX_QUES,
    "@": LexStates.LEX_AT,
    "A": LexStates.LEX_IDENT,
    "B": LexStates.LEX_IDENT_OR_BIN,
    "C": LexStates.LEX_IDENT,
    "D": LexStates.LEX_IDENT,
    "E": LexStates.LEX_IDENT,
    "F": LexStates.LEX_IDENT,
    "G": LexStates.LEX_IDENT,
    "H": LexStates.LEX_IDENT,
    "I": LexStates.LEX_IDENT,
    "J": LexStates.LEX_IDENT,
    "K": LexStates.LEX_IDENT,
    "L": LexStates.LEX_IDENT,
    "M": LexStates.LEX_IDENT,
    "N": LexStates.LEX_IDENT_OR_NCHAR,
    "O": LexStates.LEX_IDENT,
    "P": LexStates.LEX_IDENT,
    "Q": LexStates.LEX_IDENT,
    "R": LexStates.LEX_IDENT,
    "S": LexStates.LEX_IDENT,
    "T": LexStates.LEX_IDENT,
    "U": LexStates.LEX_IDENT,
    "V": LexStates.LEX_IDENT,
    "W": LexStates.LEX_IDENT,
    "X": LexStates.LEX_IDENT_OR_HEX,
    "Y": LexStates.LEX_IDENT,
    "Z": LexStates.LEX_IDENT,
    "[": LexStates.LEX_ERROR,
    "\\": LexStates.LEX_ERROR,
    "]": LexStates.LEX_ERROR,
    "^": LexStates.LEX_CARET,
    "_": LexStates.LEX_IDENT,
    "`": LexStates.LEX_DELIMITER,
    "a": LexStates.LEX_IDENT,
    "b": LexStates.LEX_IDENT_OR_BIN,
    "c": LexStates.LEX_IDENT,
    "d": LexStates.LEX_IDENT,
    "e": LexStates.LEX_IDENT,
    "f": LexStates.LEX_IDENT,
    "g": LexStates.LEX_IDENT,
    "h": LexStates.LEX_IDENT,
    "i": LexStates.LEX_IDENT,
    "j": LexStates.LEX_IDENT,
    "k": LexStates.LEX_IDENT,
    "l": LexStates.LEX_IDENT,
    "m": LexStates.LEX_IDENT,
    "n": LexStates.LEX_IDENT_OR_NCHAR,
    "o": LexStates.LEX_IDENT,
    "p": LexStates.LEX_IDENT,
    "q": LexStates.LEX_IDENT,
    "r": LexStates.LEX_IDENT,
    "s": LexStates.LEX_IDENT,
    "t": LexStates.LEX_IDENT,
    "u": LexStates.LEX_IDENT,
    "v": LexStates.LEX_IDENT,
    "w": LexStates.LEX_IDENT,
    "x": LexStates.LEX_IDENT_OR_HEX,
    "y": LexStates.LEX_IDENT,
    "{": LexStates.LEX_LBRACE,
    "|": LexStates.LEX_BAR,
    "}": LexStates.LEX_RBRACE,
    "~": LexStates.LEX_TILDE,
    "\x7F": LexStates.LEX_ERROR,  # DEL (delete) 删除
}

# 判断字符是否为 IDENT 的一部分
LEX_IDENT_MAP = {
    ch: state in {LexStates.LEX_IDENT, LexStates.LEX_IDENT_OR_BIN, LexStates.LEX_IDENT_OR_HEX,
                  LexStates.LEX_IDENT_OR_NCHAR, LexStates.LEX_ZERO, LexStates.LEX_NUMBER}
    for ch, state in LEX_START_STATE_MAP.items()
}

# 二进制标识符字符集
LEX_BIN_MARK_CHARSET = {"b", "B"}

# 十六进制标识符字符集
LEX_HEX_MARK_CHARSET = {"x", "X"}

# 指数字符集
LEX_E_CHARSET = {"e", "E"}

# 二进制字符集
LEX_BIN_CHARSET = {"0", "1"}

# 十进制字符集
LEX_OCT_CHARSET = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

# 十六进制字符集
LEX_HEX_CHARSET = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                   "a", "b", "c", "d", "e", "f",
                   "A", "B", "C", "D", "E", "F"}
