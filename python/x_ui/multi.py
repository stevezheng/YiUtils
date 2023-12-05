from sqlalchemy import Column, String, create_engine, Text, Integer, Numeric
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class Inbounds(Base):
    __tablename__ = 'inbounds'
    id = Column(String(20), primary_key=True)
    user_id = Column(Integer())
    up = Column(Integer())
    down = Column(Integer())
    total = Column(Integer())
    remark = Column(String(20))
    enable = Column(Numeric())
    expiry_time = Column(Integer())
    autoreset = Column(Numeric())
    port = Column(String(20))
    protocol = Column(Text())
    settings = Column(Text())
    stream_settings = Column(Text())
    tag = Column(Text())


# 初始化数据库连接:
engine = create_engine('sqlite:///x-ui.db')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 创建session对象:
session = DBSession()

inbounds = session.query(Inbounds).all()
for inbound in inbounds:
    print(inbound.id, inbound.remark, inbound.port, inbound.protocol, inbound.settings, inbound.stream_settings, inbound.tag)

payload = Inbounds(
    id="20",
    user_id=1,
    remark="test",
    port="45001",
    protocol="vmess",
    tag="jp0003",
    settings='''{
  "clients": [
    {
      "id": "0a47facc-8b1e-41b8-8051-141a941d369e",
      "email": "l7Ts.love@xray.com",
      "alterId": 0,
      "total": 0,
      "expiryTime": 0
    }
  ],
  "disableInsecureEncryption": false
}''',
    stream_settings='''{
  "network": "ws",
  "security": "tls",
  "tlsSettings": {
    "serverName": "jp2ipv2.fsluck.com",
    "minVersion": "1.2",
    "maxVersion": "1.3",
    "cipherSuites": "",
    "certificates": [
      {
        "ocspStapling": 36000,
        "certificateFile": "/root/.acme.sh/jp2ipv2.fsluck.com_ecc/fullchain.cer",
        "keyFile": "/root/.acme.sh/jp2ipv2.fsluck.com_ecc/jp2ipv2.fsluck.com.key"
      }
    ],
    "alpn": [
      "h2",
      "http/1.1"
    ]
  },
  "wsSettings": {
    "path": "/",
    "headers": {
      "Host": "jp2ipv2.fsluck.com"
    },
    "acceptProxyProtocol": "false"
  }
}''',
)

session.add(payload)
session.commit()

# 关闭session:
session.close()