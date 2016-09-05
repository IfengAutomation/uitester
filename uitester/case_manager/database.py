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

    # def update_tag(self):
    #     DB.session.commit()

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

    def batch_insert_case_with_tags(self, case_list):
        for case in case_list:
            DB.session.add(case)
        DB.session.commit()

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
        # case.tags = tags
        # DB.session.add(case)
        # DB.session.commit()
        return case



    def query_case_by_id(self, id):
        return DB.session.query(Case).filter(Case.id == id).first()

    def query_case_by_name(self, is_accurate, name):
        '''查看case'''
        if is_accurate == False:
            name = '%' + name + '%'
            return DB.session.query(Case).filter(Case.name.like('%' + name + '%')).all()
        else:
            return DB.session.query(Case).filter(Case.name == name).first()

    def query_case_by_tag_names(self, tag_names_list):
        '''根据标识名查看case'''
        select = []
        for tag_name in tag_names_list:
            select.append(Case.tags.any(name=tag_name))
        return DB.session.query(Case).filter(*select).order_by(Case.last_modify_time.desc()).all()

    def query_case_all(self):
        '''查看case'''
        return DB.session.query(Case).order_by(Case.last_modify_time.desc()).all()

    def update_case(self, case_id, case_name, case_content, tag_names_list,
                    add_tag_names_list=None):  # todo 改成前端修改case 本函数直接commit
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
        return case

    def delete_case(self, id):
        case = DB.session.query(Case).filter(Case.id == id).first()
        DB.session.delete(case)
        DB.session.commit()

    def get_table_data(self, table_name):
        tbl = Table(table_name, DB.metadata, autoload=True, schema="main")
        sql = tbl.select()
        result = DB.session.execute(sql)
        return result

    def get_table_data_by_cases_id(self, cases_id):
        result = {}
        case_sql = 'SELECT * FROM main."case" where id in (#cases_id#)'.replace('#cases_id#', cases_id)
        case_result = DB.session.execute(case_sql)
        result['case'] = case_result
        case_tag_sql = 'SELECT * FROM main.case_tag where case_id in (#cases_id#)'.replace(
            '#cases_id#', cases_id)
        case_tag_result = DB.session.execute(case_tag_sql)
        result['case_tag'] = case_tag_result
        tag_sql = 'SELECT DISTINCT tag.id,tag.name,tag.description from main.tag ,main.case_tag' \
                  ' where  tag.id = case_tag.tag_id and case_id in (#cases_id#)'.replace('#cases_id#', cases_id)
        tag_result = DB.session.execute(tag_sql)
        result['tag'] = tag_result
        return result
