# 数据增删改查
# 导出成 .sql 文件
import datetime
import logging
import os

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String, Integer, ForeignKey, Table, MetaData
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import or_

from uitester import config

logger = logging.getLogger('UiTester')
logger.setLevel(logging.DEBUG)


class DB:
    Base = declarative_base()
    db_path = os.path.abspath(os.path.join(config.app_dir, 'casetest.db'))
    sql_uri = 'sqlite:///{}'.format(db_path)
    db_file_exists = os.path.exists(db_path)
    engine = create_engine(sql_uri, echo=False)
    conn = engine.connect()
    metadata = MetaData(conn)
    session = scoped_session(sessionmaker(bind=engine))


class Model:
    '''
    所有表通用：记录数据创建时间，id主键
    '''
    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime(timezone=True), default=datetime.datetime.now)
    last_modify_time = Column(DateTime(timezone=True), default=datetime.datetime.now)


case_tag_table = Table('case_tag', DB.Base.metadata,
                       Column('case_id', Integer, ForeignKey('case.id')),
                       Column('tag_id', Integer, ForeignKey('tag.id'))
                       )


class Case(DB.Base, Model):
    '''
    记录case信息
    '''
    __tablename__ = 'case'
    name = Column(String(20))
    content = Column(TEXT)
    tags = relationship('Tag', secondary=case_tag_table, backref="case")


class Tag(DB.Base):
    '''
    tag 信息
    '''
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(8), unique=True)
    description = Column(TEXT)


class DBCommandLineHelper:
    def __init__(self):
        if not DB.db_file_exists:
            DB.Base.metadata.create_all(DB.engine)

    def insert_tag(self, name, description):
        tag = Tag()
        tag.name = name
        tag.description = description
        DB.session.add(tag)
        DB.session.commit()
        return tag

    def update_tag(self):
        DB.session.commit()

    def query_tag_by_name(self, is_accurate, name):
        '''根据标识名查看未删除tag'''
        if is_accurate == False:
            name = '%' + name + '%'
            return DB.session.query(Tag).filter(Tag.name.like(name)).all()
        else:
            return DB.session.query(Tag).filter(Tag.name == name).first()

    def query_tag_by_id(self, id):
        '''根据标识名查看tag'''
        return DB.session.query(Tag).filter(Tag.id == id).first()

    def query_tag_all(self):
        '''查看所有tag'''
        return DB.session.query(Tag).all()

    def delete_tag(self, id):
        '''删除tag'''
        del_tag = DB.session.query(Tag).filter(Tag.id == id).first()
        DB.session.delete(del_tag)
        DB.session.commit()

    def insert_case_with_tags(self, name, content, tags):
        '''插入case'''
        case = Case()
        case.name = name
        case.content = content
        case.tags = tags
        DB.session.add(case)
        DB.session.commit()
        return case

    def insert_case_with_tagnames(self, name, content, tag_names_list, add_tag_names_list=None):
        '''插入case'''
        case = Case()
        case.name = name
        case.content = content
        tags = []
        if tag_names_list:
            select = or_(*[Tag.name == tag_name for tag_name in tag_names_list])
            tags = DB.session.query(Tag).filter(select).all()
        if add_tag_names_list:
            for tag_name in add_tag_names_list:
                tag = Tag(name=tag_name, description='')
                tags.append(tag)
        self.insert_case_with_tags(name, content, tags)
        case.tags = tags
        DB.session.add(case)
        DB.session.commit()
        return case

    def query_case_by_id(self, id):
        return DB.session.query(Case).filter(Case.id == id).first()

    def query_case_by_name(self, name):
        '''查看case'''
        return DB.session.query(Case).filter(Case.name.like('%' + name + '%')).all()

    def query_case_by_tag_names(self, tag_names_list):
        '''根据标识名查看case'''
        select = []
        for tag_name in tag_names_list:
            select.append(Case.tags.any(name=tag_name))
        return DB.session.query(Case).filter(*select).order_by(Case.last_modify_time.desc()).all()

    def query_case_all(self):
        '''查看case'''
        return DB.session.query(Case).order_by(Case.last_modify_time.desc()).all()

    def update_case(self, case_id, case_name, case_content, tag_names_list, add_tag_names_list=None):
        case = DB.session.query(Case).filter(Case.id == case_id).first()
        case.name = case_name
        case.content = case_content
        tags = []
        if tag_names_list:
            select = or_(*[Tag.name == tag_name for tag_name in tag_names_list])
            tags = DB.session.query(Tag).filter(select).all()
        if add_tag_names_list:
            for tag_name in add_tag_names_list:
                tag = Tag(name=tag_name, description='')
                tags.append(tag)
        case.tags = tags
        DB.session.commit()

    def delete_case(self, id):
        case = DB.session.query(Case).filter(Case.id == id).first()
        DB.session.delete(case)
        DB.session.commit()

    def get_table_data(self, table_name):
        tbl = Table(table_name, DB.metadata, autoload=True, schema="main")
        sql = tbl.select()
        result = DB.conn.execute(sql)
        return result

    def get_table_data_by_cases_id(self, cases_id):
        result = {}
        case_sql = 'SELECT * FROM main."case" where id in (#cases_id#)'.replace('#cases_id#', cases_id)
        case_result = DB.conn.execute(case_sql)
        result['case'] = case_result
        case_tag_sql = 'SELECT * FROM main.case_tag where case_id in (#cases_id#)'.replace(
            '#cases_id#', cases_id)
        case_tag_result = DB.conn.execute(case_tag_sql)
        result['case_tag'] = case_tag_result
        tag_sql = 'SELECT DISTINCT tag.id,tag.name,tag.description from main.tag ,main.case_tag' \
                  ' where  tag.id = case_tag.tag_id and case_id in (#cases_id#)'.replace('#cases_id#', cases_id)
        tag_result = DB.conn.execute(tag_sql)
        result['tag'] = tag_result
        return result

    def insert_case_tag(self, case_id, tag_id):
        '''插入case'''
        case_tag = case_tag_table
        case_tag.case_id = case_id
        case_tag.tag_id = tag_id
        DB.session.add(case_tag)
        DB.session.commit()
        return case_tag

    def test_case(self):
        logger.debug("case insert")
        tags_list = self.query_tag_all()
        tags = [tags_list[0], tags_list[1]]
        self.insert_case_with_tagnames("测试验证点播视频音频播放操作", "测试验证点播视频音频播放操作", tags)
        self.insert_case_with_tagnames("测试点播视频已缓存标记", "测试点播视频已缓存标记", tags)
        self.insert_case_with_tagnames("测试点播视频缓存多选", "测试点播视频缓存多选", tags)
        self.insert_case_with_tagnames("测试验证点播视频播放相关页面内容视频跳转的时候", "测试验证点播视频播放相关页面内容视频跳转的时候", tags)
        logger.debug("test query_case_by_name")
        case_list = self.query_case_by_name("测试验证点播")
        for case in case_list:
            logger.debug("case name:", case.name)
        logger.debug("test query_case_all")
        case_list = self.query_case_all()
        for case in case_list:
            logger.debug("case name:", case.name)
        logger.debug("test update_case")
        case_list[0].name = "测试验证点播视频音频播放操作x"
        case_list[0].content = "测试验证点播视频音频播放操作x"
        # del case_list[0].tags[1]
        self.update_case()
        logger.debug("test delete")
        # self.delete_case(1)

    def test_tag(self):
        # self.init()
        logger.debug("test insert")
        self.insert_tag('主页', '打开app的首页')
        self.insert_tag('点播', '点播视频')
        self.insert_tag('点播-精选', '点播-精选视频')
        self.insert_tag('直播', '直播视频')
        logger.debug("test query")
        tag_list = self.query_tag_by_name(False, '点播')
        for tag in tag_list:
            logger.debug("tag name :", tag.name)
        logger.debug("test query_tag_all")
        for tag in tag_list:
            logger.debug("tag name :", tag.name)
        tag_list_all = self.query_tag_all()
        logger.debug("test update")
        tag_list_all[0].name = "主页-精选"
        self.update_tag()
        logger.debug("test del")
        # self.delete_tag(3)
        tag_list = self.query_tag_all()
        for tag in tag_list:
            logger.debug("tag name :", tag.name)


if __name__ == '__main__':
    dBCommandLineHelper = DBCommandLineHelper()
    # dBCommandLineHelper.delete_tag(1)
    # dBCommandLineHelper.init()
    # dBCommandLineHelper.test_tag()
    # dBCommandLineHelper.test_case()
    # dBCommandLineHelper.delete_tag(1)
    # var = dBCommandLineHelper.query_case_by_tag_name("点播")
    # print(var)
