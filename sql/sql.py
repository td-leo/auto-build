__author__ = 'xulei'

#encoding:utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import MySQLdb
import utils.contast
import logging
import os
import time
import contast


class sql:

    db = ""
    cursor = ""

    def __init__(self):
        self._connect()

    def _connect(self):

        global  db
        db = MySQLdb.connect("localhost", contast.REDMINE_SQL_USER, 
                contast.REDMINE_SQL_PASSWORD, contast.REDMINE_DATABASE_NAME, charset='utf8')

    def _query(self, sql):

        global cursor, db
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            db.close


    def GetAllIssueByProjects(self, project_id):

        global db
        cursor = db.cursor()
        cursor.execute('select * from issues where project_id=69;')
        datas = cursor.fetchall()

        for data in datas:
            print data[1]
            print cursor.rowcount,"rows in tatal"
        cursor.close()

    def GetAllProject(self):

        projects =[]
        global db
        cursor = db.cursor()
        cursor.execute('select id from projects where identifier="romtest" ')
        datas = cursor.fetchall()

        for data in datas:
            projects.append(data[0])
        cursor.close()
        return projects


    def GetLastedVesionByProjects(self, project_id):

        project_version = []
        global db
        cursor = db.cursor()
        cursor.execute('select id from versions where project_id=%s order by effective_date asc' %(project_id))
        datas = cursor.fetchall()

        for data in datas:
            if int(self.GetVersionCustomValueByColumn(data[0], 'build')) == 1:
                continue
            project_version.append(project_id)
            project_version.append(data[0])
            break;
        cursor.close()
        return project_version

    def GetProjectsByVersion(self):
        projects = []
        global db
        cursor = db.cursor()
        cursor.execute('select distinct project_id from versions')
        datas = cursor.fetchall()
        for data in datas:
            projects.append(data[0])
        cursor.close()
        return projects


    def CreateReleaseNoteDir(self, romid):

        identifier = self.GetInfoByProjectID(project_id)[1]
        release_path = os.path.join('/home/ubuntu', identifier)
        release_path = os.path.join(release_path, romid)
        if os.path.exists(release_path):
            logging.debug('[CreateReleaseNoteDir] already exists')
        else:
            os.system("mkdir -p %s" %release_path)

        note_file = os.path.join(release_path,'ReleaseNote.txt')
        logging.debug('[CreateReleaseNoteDir] note_file:%s' %note_file)
        return note_file

    def GetCompleteProject(self, project_id, version_id):

        unresolve_id = self.getNewId()
        global db
        cursor = db.cursor()
        cursor.execute('select status_id,description from issues where project_id=%s and fixed_version_id =%s' %(project_id, version_id))

        datas = cursor.fetchall()
        ''' adjust whether complete projects all issues must be @resolve or @close '''

        '''[already build version do not continue]'''
        version_data = self.GetCustomValueByVersionID(version_id)
        for value in version_data:
            if value[0] == self.GetBuildIdFromCustomFields() and value[1] == '1':
                return None
            elif value[0] == self.GetRomIdFromCustomFields():
                romid = value[1]

        for data in datas:
            if int(data[0]) == unresolve_id:
                return None


        return (project_id)

    def GetAllCompleteProjects(self):

        all_projects = self.GetProjectsByVersion()
        all_pro_ver = []
        complete_pro_id = []
        for project in all_projects:
            pro_ver = self.GetLastedVesionByProjects(project)
            if len(pro_ver) > 0:all_pro_ver.append(pro_ver)

        for i in all_pro_ver:
            id[0] = self.GetCompleteProject(i[0], i[1])
            if id[0] != None:
                one = []
                one.append(id[0])
                one.append(i[1])
                one.append(id[1])
                complete_pro_id.append(one)

        logging.debug('[GetAllCompleteProjects]:%s' %complete_pro_id)
        return complete_pro_id


    def getNewId(self):
	'''
 	'python support chinese problem, so return directly'
        global db
        cursor = db.cursor()
        cursor.execute('select id from issue_statuses where name = "New"')
        datas = cursor.fetchall()
        cursor.close()
        return datas[0][0]
	'''	
	return 1;

    ''' trigger jenkins paramater '''

    def GetBuildInfo(self):
        info_list = []
        project_list = self.GetAllCompleteProjects()
        if project_list == None:
	    logging.INFO('[GetBuildInfo] no project ready to build now !!')
	    return
        for project_id, version_id in project_list:

            version_data = self.GetCustomValueByVersionID(version_id)
            project_data = self.GetCustomValueByProjectID(project_id)

            param = {}
            for value in version_data:
                if value[0] == self.GetTypeIdFromCustomFields():
                    param['buildtype'] = value[1]
                elif value[0] == self.GetBuildIdFromCustomFields():
                    param['build'] = value[1]
                elif value[0] == self.GetRomIdFromCustomFields():
                    param['romid'] = value[1]

            param['identifier'] = self.GetInfoByProjectID(project_id)[1]

            param['versionid'] = version_id
            param['projectid'] = project_id
            param['versionname'] = self.GetNameByVersionID(version_id)

            info_list.append(param)

	logging.debug('[GetBuildInfo] project ready to build now:%s' %info_list)
        return info_list


    def GetInfoByProjectID(self, project_id):
        global db
        cursor = db.cursor()
        cursor.execute('select name, identifier from projects where id = %s' %(project_id) )
        datas = cursor.fetchall()
        cursor.close()
        return datas[0][0], datas[0][1]

    def GetNameByVersionID(self, version_id):
        global db
        cursor = db.cursor()
        cursor.execute('select name from versions where id = %s' %(version_id) )
        datas = cursor.fetchall()
        cursor.close()
        return datas[0][0]


    def GetVersionCustomValueByColumn(self, version_id, column):

        id = self.GetIdFromVersionCustomFields(column)
        global db
        cursor = db.cursor()
        cursor.execute("select value from custom_values where custom_field_id =%s and customized_id = %s and customized_type = 'Version'" %(id, version_id))
        datas = cursor.fetchall()
        cursor.close()
        return datas[0][0]


    def GetCustomValueByVersionID(self, version_id):
        global db
        cursor = db.cursor()
        cursor.execute("select custom_field_id, value from custom_values where customized_id = %s and customized_type = 'Version'" %(version_id))
        datas = cursor.fetchall()
        cursor.close()
        return datas

    def GetCustomValueByProjectID(self, project_id):
        global db
        cursor = db.cursor()
        cursor.execute("select custom_field_id, value from custom_values where customized_id = %s and customized_type = 'Project'" %(project_id))
        datas = cursor.fetchall()
        cursor.close()
        return datas


    def GetIdFromVersionCustomFields(self, column):
        global db
        cursor = db.cursor()
        cursor.execute("select id from custom_fields where name='%s' and type='VersionCustomField'" %(column))
        datas = cursor.fetchall()
        cursor.close()
        return datas[0][0]

    def GetBuildIdFromCustomFields(self):
        global db
        cursor = db.cursor()
        cursor.execute("select id from custom_fields where name='build' and type='VersionCustomField'")
        datas = cursor.fetchall()
        cursor.close()
        return datas[0][0]

    def GetTypeIdFromCustomFields(self):
        global db
        cursor = db.cursor()
        cursor.execute("select id from custom_fields where name='type' and type='VersionCustomField'")
        datas = cursor.fetchall()
        cursor.close()
        return datas[0][0]

    def GetReleaseIdFromCustomFields(self):
        global db
        cursor = db.cursor()
        cursor.execute("select id from custom_fields where name='release' and type='VersionCustomField'")
        datas = cursor.fetchall()
        cursor.close()
        return datas[0][0]

    def GetRomIdFromCustomFields(self):
        global db
        cursor = db.cursor()
        cursor.execute("select id from custom_fields where name='romid' and type='VersionCustomField'")
        datas = cursor.fetchall()
        cursor.close()
        return datas[0][0]


    def UpdateBuildField(self, version_id):

        global db
        cursor = db.cursor()
        cursor.execute("update custom_values set value=1 where customized_id=%s and customized_type='Version' and custom_field_id=%s" %(version_id, self.GetBuildIdFromCustomFields()))
        db.commit()
        cursor.close()



