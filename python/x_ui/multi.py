from sqlalchemy import Column, String, create_engine, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


class Inbounds(Base):
    __tablename__ = 'inbounds'
    id = Column(String(20), primary_key=True)
    remark = Column(String(20))
    port = Column(String(20))
    listen = Column(String(20))
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
    print(inbound.id, inbound.remark, inbound.port, inbound.listen, inbound.protocol, inbound.settings, inbound.stream_settings, inbound.tag)

# 关闭session:
session.close()