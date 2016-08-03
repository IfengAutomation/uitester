# 数据增删改查
# 导出成 .sql 文件
import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String, Integer, ForeignKey, Table, MetaData
from sqlalchemy import create_engine
from sqlalchemy import engine
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, relationship
from sqlalchemy.orm import sessionmaker
import pandas as pd

sql_uri = 'sqlite:///D:/DB/casetest.db'
Base = declarative_base()
engine = create_engine(sql_uri, echo=False)
session = scoped_session(sessionmaker(bind=engine))
conn = engine.connect()
metadata = MetaData(conn)


class Model:
    '''
    所有表通用：记录数据创建时间，id主键
    '''
    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime(timezone=True), default=datetime.datetime.now)
    last_modify_time = Column(DateTime(timezone=True), default=datetime.datetime.now)


case_tag_table = Table('case_tag', Base.metadata,
                       Column('case_id', Integer, ForeignKey('case.id')),
                       Column('tag_id', Integer, ForeignKey('tag.id'))
                       )


class Case(Base, Model):
    '''
    记录case信息
    '''
    __tablename__ = 'case'
    name = Column(String(20))
    content = Column(TEXT)
    tags = relationship('Tag', secondary=case_tag_table, backref="case")


class Tag(Base):
    '''
    tag 信息
    '''
    __tablename__ = 'tag'
    DELETE_STATUS = -1
    DEFAULT_STATUS = 0
    id = Column(Integer, primary_key=True)
    name = Column(String(8), unique=True)
    description = Column(TEXT)
    status = Column(Integer, default=DEFAULT_STATUS)


class DBCommandLineHelper:
    def init(self):
        Base.metadata.create_all(engine)

    def insert_tag(self, name, description):
        tag = Tag()
        tag.name = name
        tag.description = description
        session.add(tag)
        session.commit()

    def update_tag(self):
        session.commit()

    def query_tag(self, name):
        '''根据标识名查看未删除tag'''
        name = '%' + name + '%'
        return session.query(Tag).filter(Tag.status == 0, Tag.name.like(name)).all()

    def query_tag_all(self):
        '''查看所有未删除tag'''
        return session.query(Tag).filter(Tag.status == 0).all()

    def delete_tag(self, id):
        '''删除tag'''
        del_tag = session.query(Tag).filter(Tag.id == id, Tag.status == 0).first()
        del_tag.status = -1
        session.commit()

    def insert_case(self, name, content, tags):
        '''插入case'''
        case = Case()
        case.name = name
        case.content = content
        case.tags = tags
        session.add(case)
        session.commit()

    def query_case_by_name(self, name):
        '''查看case'''
        return session.query(Case).filter(Case.name.like('%' + name + '%')).all()

    def query_case_all(self):
        '''查看case'''
        return session.query(Case).all()

    def update_case(self):
        session.commit()

    def delete_case(self, id):
        case = session.query(Case).filter(Case.id == id).first()
        session.delete(case)
        session.commit()

    def get_table_data(self, table_name):
        tbl = Table(table_name, metadata, autoload=True, schema="main")
        sql = tbl.select()
        result = conn.execute(sql)
        return result

    def test_case(self):
        print("case insert")
        tags_list = self.query_tag_all()
        tags = [tags_list[0], tags_list[1]]
        self.insert_case("测试验证点播视频音频播放操作", "测试验证点播视频音频播放操作", tags)
        self.insert_case("测试点播视频已缓存标记", "测试点播视频已缓存标记", tags)
        self.insert_case("测试点播视频缓存多选", "测试点播视频缓存多选", tags)
        self.insert_case("测试验证点播视频播放相关页面内容视频跳转的时候", "测试验证点播视频播放相关页面内容视频跳转的时候", tags)
        print("test query_case_by_name")
        case_list = self.query_case_by_name("测试验证点播")
        for case in case_list:
            print("case name:", case.name)
        print("test query_case_all")
        case_list = self.query_case_all()
        for case in case_list:
            print("case name:", case.name)
        print("test update_case")
        case_list[0].name = "测试验证点播视频音频播放操作x"
        case_list[0].content = "测试验证点播视频音频播放操作x"
        del case_list[0].tags[1]
        self.update_case()
        print("test delete")
        self.delete_case(1)

    def test_tag(self):
        # self.init()
        print("test insert")
        self.insert_tag('主页', '打开app的首页')
        self.insert_tag('点播', '点播视频')
        self.insert_tag('点播-精选', '点播-精选视频')
        self.insert_tag('直播', '直播视频')
        print("test query")
        tag_list = self.query_tag('点播')
        for tag in tag_list:
            print("tag name :", tag.name)
        print("test query_tag_all")
        for tag in tag_list:
            print("tag name :", tag.name)
        tag_list_all = self.query_tag_all()
        print("test update")
        tag_list_all[0].name = "主页-精选"
        self.update_tag()
        print("test del")
        self.delete_tag(3)
        tag_list = self.query_tag_all()
        for tag in tag_list:
            print("tag name :", tag.name)


if __name__ == '__main__':
    dBCommandLineHelper = DBCommandLineHelper()
    # dBCommandLineHelper.init()
    # dBCommandLineHelper.test_tag()
    # dBCommandLineHelper.test_case()
