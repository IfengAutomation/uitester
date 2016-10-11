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

Base = declarative_base()


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


class CaseData(Base):
    __tablename__ = 'case_data'
    id = Column(Integer, primary_key=True)
    data = Column(TEXT)
    init_data = ''


class Case(Base, Model):
    '''
    记录case信息
    '''
    __tablename__ = 'case'
    name = Column(String(20))
    content = Column(TEXT)
    tags = relationship('Tag', secondary=case_tag_table, backref="case")
    data_relation = Column(TEXT)
    data = []


class Tag(Base):
    '''
    tag 信息
    '''
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(8), unique=True)
    description = Column(TEXT)


class DB:
    db_path = os.path.abspath(os.path.join(config.app_dir, 'casetest.db'))
    sql_uri = 'sqlite:///{}'.format(db_path)
    db_file_exists = os.path.exists(db_path)
    engine = create_engine(sql_uri, echo=False)
    conn = engine.connect()
    metadata = MetaData(conn)
    session = scoped_session(sessionmaker(bind=engine))
    if not db_file_exists:
        Base.metadata.create_all(engine)
    db_file_exists = os.path.exists(db_path)


class DBCommandLineHelper:
    def insert_tag(self, name, description):
        tag = Tag()
        tag.name = name
        tag.description = description
        DB.session.add(tag)
        DB.session.commit()
        return tag

    def update_tag(self):
        DB.session.commit()

    def query_tag_by_name(self, name):
        return DB.session.query(Tag).filter(Tag.name == name).first()

    def fuzzy_query_tag_by_name(self, name):
        name = '%' + name + '%'
        return DB.session.query(Tag).filter(Tag.name.like(name)).all()

    def query_tag_by_id(self, id):
        '''根据标识名查看tag'''
        return DB.session.query(Tag).filter(Tag.id == id).first()

    def query_tag_all(self):
        '''查看所有tag'''
        return DB.session.query(Tag).all()

    def delete_tag_by_name(self, name):
        '''删除tag'''
        tag = DB.session.query(Tag).filter(Tag.name == name).first()
        cases = self.query_case_by_tag_names([name])
        for case in cases:
            case.tags.remove(tag)
        DB.session.delete(tag)
        DB.session.commit()

    def delete_tag(self, id):
        '''删除tag'''
        DB.session.query(Tag).filter(Tag.id == id).delete()
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
        return self.insert_case_with_tags(name, content, tags)

    def query_case_by_id(self, id):
        return DB.session.query(Case).filter(Case.id == id).first()

    def query_case_by_name(self, is_accurate, name):
        '''查看case'''
        if is_accurate == False:
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

    def query_no_tag_case(self):
        return DB.session.query(Case).filter(Case.tags == None).order_by(Case.last_modify_time.desc()).all()

    def update_case(self):
        DB.session.commit()

    def delete_case(self, id):
        case = DB.session.query(Case).filter(Case.id == id).first()
        case.tags.clear()
        DB.session.delete(case)
        DB.session.commit()

    def batch_delete_case(self, ids):
        cases = DB.session.query(Case).filter(Case.id.in_(ids)).all()
        for case in cases:
            case.tags.clear()
            DB.session.delete(case)
        # DB.session.query(Case).filter(Case.id.in_(ids)).delete(synchronize_session=False)
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
        case_data_sql = "SELECT cd.* FROM case_data cd,  (SELECT data_relation FROM 'case' WHERE id in (#cases_id#))t WHERE t.data_relation  like  '%'''  || cd.id || '''%'  ".replace(
            '#cases_id#', cases_id)
        case_data_result = DB.session.execute(case_data_sql)
        result['case_data'] = case_data_result
        return result

    def query_case_data(self, id):
        case_data = DB.session.query(CaseData).filter(CaseData.id == id).one()
        return case_data

    def update_case_data(self, id, data):
        case_data = DB.session.query(CaseData).filter(CaseData.id == id).one()
        case_data.data = data
        DB.session.commit()

    def insert_case_data(self, data):
        case_data = CaseData()
        case_data.data = data
        DB.session.add(case_data)
        DB.session.commit()
        return case_data

    def delete_case_data(self, id):
        DB.session.query(CaseData).filter(CaseData.id == id).delete()
        DB.session.commit()

    def batch_delete_case_data(self, delete_data_ids):
        DB.session.query(CaseData).filter(CaseData.id.in_(delete_data_ids)).delete(synchronize_session=False)
        DB.session.commit()
