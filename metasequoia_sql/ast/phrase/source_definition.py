# pylint: disable=C0302

"""
复制源定义（source definition）
"""

from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.literal import IntLiteral, UserName
    from metasequoia_sql.ast.basic.fixed_enum import EnumTablePrimaryKeyCheckType

__all__ = [
    "SourceDefinitionType",
    "SourceDefinition",
    "SourceHostDefinition",
    "NetworkNamespaceDefinition",
    "SourceBindDefinition",
    "SourceUserDefinition",
    "SourcePasswordDefinition",
    "SourcePortDefinition",
    "SourceConnectRetryDefinition",
    "SourceRetryCountDefinition",
    "SourceDelayDefinition",
    "SourceSslDefinition",
    "SourceSslCaDefinition",
    "SourceSslCapathDefinition",
    "SourceTlsVersionDefinition",
    "SourceTlsCiphersuitesDefinition",
    "SourceSslCertDefinition",
    "SourceSslCipherDefinition",
    "SourceSslKeyDefinition",
    "SourceSslVerifyServerCertDefinition",
    "SourceSslCrlDefinition",
    "SourceSslCrlpathDefinition",
    "SourcePublicKeyDefinition",
    "SourceGetSourcePublicKeyDefinition",
    "SourceHeartbeatPeriodDefinition",
    "IgnoreServerIdsDefinition",
    "SourceCompressionAlgorithmDefinition",
    "SourceZstdCompressionLevelDefinition",
    "SourceAutoPositionDefinition",
    "PrivilegeCheckDefinition",
    "RequireRowFormatDefinition",
    "RequireTablePrimaryKeyCheckDefinition",
    "SourceConnectionAutoFailoverDefinition",
    "AssignGtidsToAnonymousTransactionsDefinition",
    "GtidOnlyDefinition",
    "SourceFileDefinition",
    "SourceLogFileDefinition",
    "SourceLogPosDefinition",
    "RelayLogFileDefinition",
    "RelayLogPosDefinition",
    "SqlBeforeGtids",
    "SqlAfterGtids",
    "SqlAfterMtsGaps",

    # 枚举值
    "EnumAssignGtidsType",
    "AssignGidsDefinition",
]


class SourceDefinitionType(IntEnum):
    """复制源定义类型"""

    HOST = 1  # MASTER_HOST/SOURCE_HOST
    NETWORK_NAMESPACE = 2  # NETWORK_NAMESPACE
    BIND = 3  # MASTER_BIND/SOURCE_BIND
    USER = 4  # MASTER_USER/SOURCE_USER
    PASSWORD = 5  # MASTER_PASSWORD/SOURCE_PASSWORD
    PORT = 6  # MASTER_PORT/SOURCE_PORT
    CONNECT_RETRY = 7  # MASTER_CONNECT_RETRY/SOURCE_CONNECT_RETRY
    RETRY_COUNT = 8  # MASTER_RETRY_COUNT/SOURCE_RETRY_COUNT
    DELAY = 9  # MASTER_DELAY/SOURCE_DELAY
    SSL = 10  # MASTER_SSL/SOURCE_SSL
    SSL_CA = 11  # MASTER_SSL_CA/SOURCE_SSL_CA
    SSL_CAPATH = 12  # MASTER_SSL_CAPATH/SOURCE_SSL_CAPATH
    TLS_VERSION = 13  # MASTER_TLS_VERSION/SOURCE_TLS_VERSION
    TLS_CIPHERSUITES = 14  # MASTER_TLS_CIPHERSUITES/SOURCE_TLS_CIPHERSUITES
    SSL_CERT = 15  # MASTER_SSL_CERT/SOURCE_SSL_CERT
    SSL_CIPHER = 16  # MASTER_SSL_CIPHER/SOURCE_SSL_CIPHER
    SSL_KEY = 17  # MASTER_SSL_KEY/SOURCE_SSL_KEY
    SSL_VERIFY_SERVER_CERT = 18  # MASTER_SSL_VERIFY_SERVER_CERT/SOURCE_SSL_VERIFY_SERVER_CERT
    SSL_CRL = 19  # MASTER_SSL_CRL/SOURCE_SSL_CRL
    SSL_CRLPATH = 20  # MASTER_SSL_CRLPATH/SOURCE_SSL_CRLPATH
    PUBLIC_KEY = 21  # MASTER_PUBLIC_KEY_PATH/SOURCE_PUBLIC_KEY_PATH
    GET_SOURCE_PUBLIC_KEY = 22  # GET_MASTER_PUBLIC_KEY/GET_SOURCE_PUBLIC_KEY
    HEARTBEAT_PERIOD = 23  # MASTER_HEARTBEAT_PERIOD/SOURCE_HEARTBEAT_PERIOD
    IGNORE_SERVER_IDS = 24  # IGNORE_SERVER_IDS
    COMPRESSION_ALGORITHM = 25  # MASTER_COMPRESSION_ALGORITHMS/SOURCE_COMPRESSION_ALGORITHMS
    ZSTD_COMPRESSION_LEVEL = 26  # MASTER_ZSTD_COMPRESSION_LEVEL/SOURCE_ZSTD_COMPRESSION_LEVEL
    AUTO_POSITION = 27  # MASTER_AUTO_POSITION/SOURCE_AUTO_POSITION
    PRIVILEGE_CHECK = 28  # PRIVILEGE_CHECKS_USER
    REQUIRE_ROW_FORMAT = 29  # REQUIRE_ROW_FORMAT
    REQUIRE_TABLE_PRIMARY_KEY_CHECK = 30  # REQUIRE_TABLE_PRIMARY_KEY_CHECK
    SOURCE_CONNECTION_AUTO_FAILOVER = 31  # SOURCE_CONNECTION_AUTO_FAILOVER
    ASSIGN_GTIDS_TO_ANONYMOUS_TRANSACTIONS = 32  # ASSIGN_GTIDS_TO_ANONYMOUS_TRANSACTIONS
    GTID_ONLY = 33  # GTID_ONLY
    LOG_FILE = 34  # MASTER_LOG_FILE/SOURCE_LOG_FILE
    LOG_POS = 35  # MASTER_LOG_POS/SOURCE_LOG_POS
    RELAY_LOG_FILE = 36  # RELAY_LOG_FILE
    RELAY_LOG_POS = 37  # RELAY_LOG_POS
    SQL_BEFORE_GTIDS = 38  # SQL_BEFORE_GTIDS
    SQL_AFTER_GTIDS = 39  # SQL_AFTER_GTIDS
    SQL_AFTER_MTS_GAPS = 40  # SQL_AFTER_MTS_GAPS


class SourceDefinition(Node):
    """复制源定义基类

    Parameters
    ----------
    definition_type : SourceDefinitionType
        复制源定义类型
    """

    __slots__ = ("_definition_type",)

    def __init__(self, definition_type: SourceDefinitionType):
        """初始化复制源定义

        Parameters
        ----------
        definition_type : SourceDefinitionType
            复制源定义类型
        """
        self._definition_type = definition_type

    @property
    def definition_type(self) -> SourceDefinitionType:
        """获取复制源定义类型

        Returns
        -------
        SourceDefinitionType
            复制源定义类型
        """
        return self._definition_type


class SourceHostDefinition(SourceDefinition):
    """主机定义: MASTER_HOST/SOURCE_HOST = value

    Parameters
    ----------
    value : str
        主机地址
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化主机定义

        Parameters
        ----------
        value : str
            主机地址
        """
        super().__init__(SourceDefinitionType.HOST)
        self._value = value

    @property
    def value(self) -> str:
        """获取主机地址

        Returns
        -------
        str
            主机地址
        """
        return self._value


class NetworkNamespaceDefinition(SourceDefinition):
    """网络命名空间定义: NETWORK_NAMESPACE = value

    Parameters
    ----------
    value : str
        网络命名空间
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化网络命名空间定义

        Parameters
        ----------
        value : str
            网络命名空间
        """
        super().__init__(SourceDefinitionType.NETWORK_NAMESPACE)
        self._value = value

    @property
    def value(self) -> str:
        """获取网络命名空间

        Returns
        -------
        str
            网络命名空间
        """
        return self._value


class SourceBindDefinition(SourceDefinition):
    """绑定地址定义: MASTER_BIND/SOURCE_BIND = value

    Parameters
    ----------
    value : str
        绑定地址
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化绑定地址定义

        Parameters
        ----------
        value : str
            绑定地址
        """
        super().__init__(SourceDefinitionType.BIND)
        self._value = value

    @property
    def value(self) -> str:
        """获取绑定地址

        Returns
        -------
        str
            绑定地址
        """
        return self._value


class SourceUserDefinition(SourceDefinition):
    """用户定义: MASTER_USER/SOURCE_USER = value

    Parameters
    ----------
    value : str
        用户名
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化用户定义

        Parameters
        ----------
        value : str
            用户名
        """
        super().__init__(SourceDefinitionType.USER)
        self._value = value

    @property
    def value(self) -> str:
        """获取用户名

        Returns
        -------
        str
            用户名
        """
        return self._value


class SourcePasswordDefinition(SourceDefinition):
    """密码定义: MASTER_PASSWORD/SOURCE_PASSWORD = value

    Parameters
    ----------
    value : str
        密码
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化密码定义

        Parameters
        ----------
        value : str
            密码
        """
        super().__init__(SourceDefinitionType.PASSWORD)
        self._value = value

    @property
    def value(self) -> str:
        """获取密码

        Returns
        -------
        str
            密码
        """
        return self._value


class SourcePortDefinition(SourceDefinition):
    """端口定义: MASTER_PORT/SOURCE_PORT = value

    Parameters
    ----------
    value : int
        端口号表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化端口定义

        Parameters
        ----------
        value : int
            端口号表达式
        """
        super().__init__(SourceDefinitionType.PORT)
        self._value = value

    @property
    def value(self) -> int:
        """获取端口号

        Returns
        -------
        int
            端口号表达式
        """
        return self._value


class SourceConnectRetryDefinition(SourceDefinition):
    """连接重试定义: MASTER_CONNECT_RETRY/SOURCE_CONNECT_RETRY = value

    Parameters
    ----------
    value : int
        连接重试次数表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化连接重试定义

        Parameters
        ----------
        value : int
            连接重试次数表达式
        """
        super().__init__(SourceDefinitionType.CONNECT_RETRY)
        self._value = value

    @property
    def value(self) -> int:
        """获取连接重试次数

        Returns
        -------
        int
            连接重试次数表达式
        """
        return self._value


class SourceRetryCountDefinition(SourceDefinition):
    """重试计数定义: MASTER_RETRY_COUNT/SOURCE_RETRY_COUNT = value

    Parameters
    ----------
    value : int
        重试计数表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化重试计数定义

        Parameters
        ----------
        value : int
            重试计数表达式
        """
        super().__init__(SourceDefinitionType.RETRY_COUNT)
        self._value = value

    @property
    def value(self) -> int:
        """获取重试计数

        Returns
        -------
        int
            重试计数表达式
        """
        return self._value


class SourceDelayDefinition(SourceDefinition):
    """延迟定义: MASTER_DELAY/SOURCE_DELAY = value

    Parameters
    ----------
    value : int
        延迟时间表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化延迟定义

        Parameters
        ----------
        value : int
            延迟时间表达式
        """
        super().__init__(SourceDefinitionType.DELAY)
        self._value = value

    @property
    def value(self) -> int:
        """获取延迟时间

        Returns
        -------
        int
            延迟时间表达式
        """
        return self._value


class SourceSslDefinition(SourceDefinition):
    """SSL 定义: MASTER_SSL/SOURCE_SSL = value

    Parameters
    ----------
    value : int
        SSL 启用状态表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化 SSL 定义

        Parameters
        ----------
        value : int
            SSL 启用状态表达式
        """
        super().__init__(SourceDefinitionType.SSL)
        self._value = value

    @property
    def value(self) -> int:
        """获取 SSL 启用状态

        Returns
        -------
        int
            SSL 启用状态表达式
        """
        return self._value


class SourceSslCaDefinition(SourceDefinition):
    """SSL CA 定义: MASTER_SSL_CA/SOURCE_SSL_CA = value

    Parameters
    ----------
    value : str
        SSL CA 文件路径
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化 SSL CA 定义

        Parameters
        ----------
        value : str
            SSL CA 文件路径
        """
        super().__init__(SourceDefinitionType.SSL_CA)
        self._value = value

    @property
    def value(self) -> str:
        """获取 SSL CA 文件路径

        Returns
        -------
        str
            SSL CA 文件路径
        """
        return self._value


class SourceSslCapathDefinition(SourceDefinition):
    """SSL CAPATH 定义: MASTER_SSL_CAPATH/SOURCE_SSL_CAPATH = value

    Parameters
    ----------
    value : str
        SSL CAPATH 目录路径
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化 SSL CAPATH 定义

        Parameters
        ----------
        value : str
            SSL CAPATH 目录路径
        """
        super().__init__(SourceDefinitionType.SSL_CAPATH)
        self._value = value

    @property
    def value(self) -> str:
        """获取 SSL CAPATH 目录路径

        Returns
        -------
        str
            SSL CAPATH 目录路径
        """
        return self._value


class SourceTlsVersionDefinition(SourceDefinition):
    """TLS 版本定义: MASTER_TLS_VERSION/SOURCE_TLS_VERSION = value

    Parameters
    ----------
    value : str
        TLS 版本
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化 TLS 版本定义

        Parameters
        ----------
        value : str
            TLS 版本
        """
        super().__init__(SourceDefinitionType.TLS_VERSION)
        self._value = value

    @property
    def value(self) -> str:
        """获取 TLS 版本

        Returns
        -------
        str
            TLS 版本
        """
        return self._value


class SourceTlsCiphersuitesDefinition(SourceDefinition):
    """TLS 密码套件定义: MASTER_TLS_CIPHERSUITES/SOURCE_TLS_CIPHERSUITES = value

    Parameters
    ----------
    value : Optional[str]
        TLS 密码套件，None 表示 NULL
    """

    __slots__ = ("_value",)

    def __init__(self, value: Optional[str]):
        """初始化 TLS 密码套件定义

        Parameters
        ----------
        value : Optional[str]
            TLS 密码套件，None 表示 NULL
        """
        super().__init__(SourceDefinitionType.TLS_CIPHERSUITES)
        self._value = value

    @property
    def value(self) -> Optional[str]:
        """获取 TLS 密码套件

        Returns
        -------
        Optional[str]
            TLS 密码套件，None 表示 NULL
        """
        return self._value


class SourceSslCertDefinition(SourceDefinition):
    """SSL 证书定义: MASTER_SSL_CERT/SOURCE_SSL_CERT = value

    Parameters
    ----------
    value : str
        SSL 证书文件路径
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化 SSL 证书定义

        Parameters
        ----------
        value : str
            SSL 证书文件路径
        """
        super().__init__(SourceDefinitionType.SSL_CERT)
        self._value = value

    @property
    def value(self) -> str:
        """获取 SSL 证书文件路径

        Returns
        -------
        str
            SSL 证书文件路径
        """
        return self._value


class SourceSslCipherDefinition(SourceDefinition):
    """SSL 密码定义: MASTER_SSL_CIPHER/SOURCE_SSL_CIPHER = value

    Parameters
    ----------
    value : str
        SSL 密码
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化 SSL 密码定义

        Parameters
        ----------
        value : str
            SSL 密码
        """
        super().__init__(SourceDefinitionType.SSL_CIPHER)
        self._value = value

    @property
    def value(self) -> str:
        """获取 SSL 密码

        Returns
        -------
        str
            SSL 密码
        """
        return self._value


class SourceSslKeyDefinition(SourceDefinition):
    """SSL 密钥定义: MASTER_SSL_KEY/SOURCE_SSL_KEY = value

    Parameters
    ----------
    value : str
        SSL 密钥文件路径
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化 SSL 密钥定义

        Parameters
        ----------
        value : str
            SSL 密钥文件路径
        """
        super().__init__(SourceDefinitionType.SSL_KEY)
        self._value = value

    @property
    def value(self) -> str:
        """获取 SSL 密钥文件路径

        Returns
        -------
        str
            SSL 密钥文件路径
        """
        return self._value


class SourceSslVerifyServerCertDefinition(SourceDefinition):
    """SSL 验证服务器证书定义: MASTER_SSL_VERIFY_SERVER_CERT/SOURCE_SSL_VERIFY_SERVER_CERT = value

    Parameters
    ----------
    value : int
        SSL 验证服务器证书标志表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化 SSL 验证服务器证书定义

        Parameters
        ----------
        value : int
            SSL 验证服务器证书标志表达式
        """
        super().__init__(SourceDefinitionType.SSL_VERIFY_SERVER_CERT)
        self._value = value

    @property
    def value(self) -> int:
        """获取 SSL 验证服务器证书标志

        Returns
        -------
        int
            SSL 验证服务器证书标志表达式
        """
        return self._value


class SourceSslCrlDefinition(SourceDefinition):
    """SSL CRL 定义: MASTER_SSL_CRL/SOURCE_SSL_CRL = value

    Parameters
    ----------
    value : str
        SSL CRL 文件路径
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化 SSL CRL 定义

        Parameters
        ----------
        value : str
            SSL CRL 文件路径
        """
        super().__init__(SourceDefinitionType.SSL_CRL)
        self._value = value

    @property
    def value(self) -> str:
        """获取 SSL CRL 文件路径

        Returns
        -------
        str
            SSL CRL 文件路径
        """
        return self._value


class SourceSslCrlpathDefinition(SourceDefinition):
    """SSL CRLPATH 定义: MASTER_SSL_CRLPATH/SOURCE_SSL_CRLPATH = value

    Parameters
    ----------
    value : str
        SSL CRLPATH 目录路径
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化 SSL CRLPATH 定义

        Parameters
        ----------
        value : str
            SSL CRLPATH 目录路径
        """
        super().__init__(SourceDefinitionType.SSL_CRLPATH)
        self._value = value

    @property
    def value(self) -> str:
        """获取 SSL CRLPATH 目录路径

        Returns
        -------
        str
            SSL CRLPATH 目录路径
        """
        return self._value


class SourcePublicKeyDefinition(SourceDefinition):
    """公钥定义: MASTER_PUBLIC_KEY_PATH/SOURCE_PUBLIC_KEY_PATH = value

    Parameters
    ----------
    value : str
        公钥文件路径
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化公钥定义

        Parameters
        ----------
        value : str
            公钥文件路径
        """
        super().__init__(SourceDefinitionType.PUBLIC_KEY)
        self._value = value

    @property
    def value(self) -> str:
        """获取公钥文件路径

        Returns
        -------
        str
            公钥文件路径
        """
        return self._value


class SourceGetSourcePublicKeyDefinition(SourceDefinition):
    """获取源公钥定义: GET_MASTER_PUBLIC_KEY/GET_SOURCE_PUBLIC_KEY = value

    Parameters
    ----------
    value : int
        获取源公钥标志表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化获取源公钥定义

        Parameters
        ----------
        value : int
            获取源公钥标志表达式
        """
        super().__init__(SourceDefinitionType.GET_SOURCE_PUBLIC_KEY)
        self._value = value

    @property
    def value(self) -> int:
        """获取源公钥标志

        Returns
        -------
        int
            获取源公钥标志表达式
        """
        return self._value


class SourceHeartbeatPeriodDefinition(SourceDefinition):
    """心跳周期定义: MASTER_HEARTBEAT_PERIOD/SOURCE_HEARTBEAT_PERIOD = value

    Parameters
    ----------
    value : Literal
        心跳周期数值字面量
    """

    __slots__ = ("_value",)

    def __init__(self, value: "IntLiteral"):
        """初始化心跳周期定义

        Parameters
        ----------
        value : IntLiteral
            心跳周期数值字面量
        """
        super().__init__(SourceDefinitionType.HEARTBEAT_PERIOD)
        self._value = value

    @property
    def value(self) -> "IntLiteral":
        """获取心跳周期数值字面量

        Returns
        -------
        IntLiteral
            心跳周期数值字面量
        """
        return self._value


class IgnoreServerIdsDefinition(SourceDefinition):
    """忽略服务器 ID 定义: IGNORE_SERVER_IDS = (list)

    Parameters
    ----------
    server_id_list : list
        服务器 ID 列表，None 表示空列表
    """

    __slots__ = ("_server_id_list",)

    def __init__(self, server_id_list: List[int]):
        """初始化忽略服务器 ID 定义

        Parameters
        ----------
        server_id_list : List[int]
            服务器 ID 列表
        """
        super().__init__(SourceDefinitionType.IGNORE_SERVER_IDS)
        self._server_id_list = server_id_list

    @property
    def server_id_list(self) -> List[int]:
        """获取服务器 ID 列表

        Returns
        -------
        List[int]
            服务器 ID 列表
        """
        return self._server_id_list


class SourceCompressionAlgorithmDefinition(SourceDefinition):
    """压缩算法定义: MASTER_COMPRESSION_ALGORITHMS/SOURCE_COMPRESSION_ALGORITHMS = value

    Parameters
    ----------
    value : str
        压缩算法名称
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化压缩算法定义

        Parameters
        ----------
        value : str
            压缩算法名称
        """
        super().__init__(SourceDefinitionType.COMPRESSION_ALGORITHM)
        self._value = value

    @property
    def value(self) -> str:
        """获取压缩算法名称

        Returns
        -------
        str
            压缩算法名称
        """
        return self._value


class SourceZstdCompressionLevelDefinition(SourceDefinition):
    """ZSTD 压缩级别定义: MASTER_ZSTD_COMPRESSION_LEVEL/SOURCE_ZSTD_COMPRESSION_LEVEL = value

    Parameters
    ----------
    value : int
        ZSTD 压缩级别表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化 ZSTD 压缩级别定义

        Parameters
        ----------
        value : int
            ZSTD 压缩级别表达式
        """
        super().__init__(SourceDefinitionType.ZSTD_COMPRESSION_LEVEL)
        self._value = value

    @property
    def value(self) -> int:
        """获取 ZSTD 压缩级别

        Returns
        -------
        int
            ZSTD 压缩级别表达式
        """
        return self._value


class SourceAutoPositionDefinition(SourceDefinition):
    """自动位置定义: MASTER_AUTO_POSITION/SOURCE_AUTO_POSITION = value

    Parameters
    ----------
    value : int
        自动位置标志表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化自动位置定义

        Parameters
        ----------
        value : int
            自动位置标志表达式
        """
        super().__init__(SourceDefinitionType.AUTO_POSITION)
        self._value = value

    @property
    def value(self) -> int:
        """获取自动位置标志

        Returns
        -------
        int
            自动位置标志表达式
        """
        return self._value


class PrivilegeCheckDefinition(SourceDefinition):
    """权限检查定义: PRIVILEGE_CHECKS_USER = value

    Parameters
    ----------
    user : Optional[str]
        用户名，None 表示 NULL
    """

    __slots__ = ("_user",)

    def __init__(self, user: Optional["UserName"]):
        """初始化权限检查定义

        Parameters
        ----------
        user : Optional[UserName]
            用户名，None 表示 NULL
        """
        super().__init__(SourceDefinitionType.PRIVILEGE_CHECK)
        self._user = user

    @property
    def user(self) -> Optional["UserName"]:
        """获取用户名

        Returns
        -------
        Optional[UserName]
            用户名，None 表示 NULL
        """
        return self._user


class RequireRowFormatDefinition(SourceDefinition):
    """要求行格式定义: REQUIRE_ROW_FORMAT = value

    Parameters
    ----------
    value : int
        要求行格式标志表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化要求行格式定义

        Parameters
        ----------
        value : int
            要求行格式标志表达式
        """
        super().__init__(SourceDefinitionType.REQUIRE_ROW_FORMAT)
        self._value = value

    @property
    def value(self) -> int:
        """获取要求行格式标志

        Returns
        -------
        int
            要求行格式标志表达式
        """
        return self._value


class RequireTablePrimaryKeyCheckDefinition(SourceDefinition):
    """要求表主键检查定义: REQUIRE_TABLE_PRIMARY_KEY_CHECK = value

    Parameters
    ----------
    check_type : int
        表主键检查类型
    """

    __slots__ = ("_check_type",)

    def __init__(self, check_type: "EnumTablePrimaryKeyCheckType"):
        """初始化要求表主键检查定义

        Parameters
        ----------
        check_type : EnumTablePrimaryKeyCheckType
            表主键检查类型
        """
        super().__init__(SourceDefinitionType.REQUIRE_TABLE_PRIMARY_KEY_CHECK)
        self._check_type = check_type

    @property
    def check_type(self) -> "EnumTablePrimaryKeyCheckType":
        """获取表主键检查类型

        Returns
        -------
        EnumTablePrimaryKeyCheckType
            表主键检查类型
        """
        return self._check_type


class SourceConnectionAutoFailoverDefinition(SourceDefinition):
    """源连接自动故障转移定义: SOURCE_CONNECTION_AUTO_FAILOVER = value

    Parameters
    ----------
    value : int
        自动故障转移标志表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化源连接自动故障转移定义

        Parameters
        ----------
        value : int
            自动故障转移标志表达式
        """
        super().__init__(SourceDefinitionType.SOURCE_CONNECTION_AUTO_FAILOVER)
        self._value = value

    @property
    def value(self) -> int:
        """获取自动故障转移标志

        Returns
        -------
        int
            自动故障转移标志表达式
        """
        return self._value


class EnumAssignGtidsType(IntEnum):
    """分配 GTIDs 给匿名事务的类型枚举值"""

    OFF = 1  # OFF
    LOCAL = 2  # LOCAL
    UUID = 3  # TEXT_STRING (UUID)


class AssignGidsDefinition(Node):
    """分配 GTIDs 给匿名事务的定义"""

    __slots__ = (
        "_assign_type",
        "_uuid",
    )

    def __init__(self,
                 assign_type: EnumAssignGtidsType,
                 uuid: Optional[str] = None):
        """初始化分配 GTIDs 给匿名事务的定义

        Parameters
        ----------
        assign_type : EnumAssignGtidsType
            分配类型
        uuid : Optional[str], optional
            UUID 值，仅当 assign_type 为 UUID 时使用
        """
        self._assign_type = assign_type
        self._uuid = uuid

    @property
    def assign_type(self) -> EnumAssignGtidsType:
        """获取分配类型

        Returns
        -------
        EnumAssignGtidsType
            分配类型
        """
        return self._assign_type

    @property
    def uuid(self) -> Optional[str]:
        """获取 UUID 值

        Returns
        -------
        Optional[str]
            UUID 值，仅当 assign_type 为 UUID 时有效
        """
        return self._uuid


class AssignGtidsToAnonymousTransactionsDefinition(SourceDefinition):
    """分配 GTIDs 给匿名事务定义: ASSIGN_GTIDS_TO_ANONYMOUS_TRANSACTIONS = value

    Parameters
    ----------
    assign : AssignGidsDefinition
        分配信息
    """

    __slots__ = ("_assign",)

    def __init__(self, assign: AssignGidsDefinition):
        """初始化分配 GTIDs 给匿名事务定义

        Parameters
        ----------
        assign : AssignGidsDefinition
            分配信息
        """
        super().__init__(SourceDefinitionType.ASSIGN_GTIDS_TO_ANONYMOUS_TRANSACTIONS)
        self._assign = assign

    @property
    def assign(self) -> AssignGidsDefinition:
        """获取分配信息

        Returns
        -------
        AssignGidsDefinition
            分配信息
        """
        return self._assign


class GtidOnlyDefinition(SourceDefinition):
    """GTID ONLY 定义: GTID_ONLY = value

    Parameters
    ----------
    value : int
        GTID ONLY 标志表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化 GTID ONLY 定义

        Parameters
        ----------
        value : int
            GTID ONLY 标志表达式
        """
        super().__init__(SourceDefinitionType.GTID_ONLY)
        self._value = value

    @property
    def value(self) -> int:
        """获取 GTID ONLY 标志

        Returns
        -------
        int
            GTID ONLY 标志表达式
        """
        return self._value


class SourceFileDefinition(SourceDefinition):
    """源文件定义基类"""

    __slots__ = ()


class SourceLogFileDefinition(SourceFileDefinition):
    """源日志文件定义: MASTER_LOG_FILE/SOURCE_LOG_FILE = value

    Parameters
    ----------
    value : str
        日志文件名
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化源日志文件定义

        Parameters
        ----------
        value : str
            日志文件名
        """
        super().__init__(SourceDefinitionType.LOG_FILE)
        self._value = value

    @property
    def value(self) -> str:
        """获取日志文件名

        Returns
        -------
        str
            日志文件名
        """
        return self._value


class SourceLogPosDefinition(SourceFileDefinition):
    """源日志位置定义: MASTER_LOG_POS/SOURCE_LOG_POS = value

    Parameters
    ----------
    value : int
        日志位置表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化源日志位置定义

        Parameters
        ----------
        value : int
            日志位置表达式
        """
        super().__init__(SourceDefinitionType.LOG_POS)
        self._value = value

    @property
    def value(self) -> int:
        """获取日志位置

        Returns
        -------
        int
            日志位置表达式
        """
        return self._value


class RelayLogFileDefinition(SourceFileDefinition):
    """中继日志文件定义: RELAY_LOG_FILE = value

    Parameters
    ----------
    value : str
        中继日志文件名
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化中继日志文件定义

        Parameters
        ----------
        value : str
            中继日志文件名
        """
        super().__init__(SourceDefinitionType.RELAY_LOG_FILE)
        self._value = value

    @property
    def value(self) -> str:
        """获取中继日志文件名

        Returns
        -------
        str
            中继日志文件名
        """
        return self._value


class RelayLogPosDefinition(SourceFileDefinition):
    """中继日志位置定义: RELAY_LOG_POS = value

    Parameters
    ----------
    value : int
        中继日志位置表达式
    """

    __slots__ = ("_value",)

    def __init__(self, value: int):
        """初始化中继日志位置定义

        Parameters
        ----------
        value : int
            中继日志位置表达式
        """
        super().__init__(SourceDefinitionType.RELAY_LOG_POS)
        self._value = value

    @property
    def value(self) -> int:
        """获取中继日志位置

        Returns
        -------
        int
            中继日志位置表达式
        """
        return self._value


class SqlBeforeGtids(SourceDefinition):
    """数据源定义：SQL_BEFORE_GTIDS

    Parameters
    ----------
    value : str
        SQL_BEFORE_GTIDS 值
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化 SQL_BEFORE_GTIDS 定义

        Parameters
        ----------
        value : str
            SQL_BEFORE_GTIDS 值
        """
        super().__init__(SourceDefinitionType.SQL_BEFORE_GTIDS)
        self._value = value

    @property
    def value(self) -> str:
        """获取 SQL_BEFORE_GTIDS 值

        Returns
        -------
        str
            SQL_BEFORE_GTIDS 值
        """
        return self._value


class SqlAfterGtids(SourceDefinition):
    """数据源定义：SQL_AFTER_GTIDS

    Parameters
    ----------
    value : str
        SQL_AFTER_GTIDS 值
    """

    __slots__ = ("_value",)

    def __init__(self, value: str):
        """初始化 SQL_AFTER_GTIDS 定义

        Parameters
        ----------
        value : str
            SQL_AFTER_GTIDS 值
        """
        super().__init__(SourceDefinitionType.SQL_AFTER_GTIDS)
        self._value = value

    @property
    def value(self) -> str:
        """获取 SQL_AFTER_GTIDS 值

        Returns
        -------
        str
            SQL_AFTER_GTIDS 值
        """
        return self._value


class SqlAfterMtsGaps(SourceDefinition):
    """数据源定义：SQL_AFTER_MTS_GAPS"""

    __slots__ = ()

    def __init__(self):
        """初始化 SQL_AFTER_MTS_GAPS 定义"""
        super().__init__(SourceDefinitionType.SQL_AFTER_MTS_GAPS)
