__author__ = 'xulei'

import jenkins
import random
import logging
import contast
class jobs:
    def Build(self, sqlite):

        info_list = sqlite.GetBuildInfo()
        if info_list == None or len(info_list) <= 0:
            return
        server = jenkins.Jenkins(contast.JENKINS_URL, 
                username=contast.JENKINS_USERNAME, password=contast.JENKINS_PASSWORD)
	print server
        print server.jobs_count()
        for info in info_list:
            param = {'versionname':None, 'buildtype': None,  'versionid':None }
            param['buildtype'] = info['buildtype']
            identifier = info['identifier']
            param['versionname'] = info['versionname']
            logging.debug('Build State:' + info['build'])

            if info['build'] == '1':return

            logging.debug('Trigger Build! identifier:%s, %s' %(identifier, param))

#    item = self.GetFreeServer(identifier, server)
            item = self.GetFixServer(identifier)
            if item == None:
                logging.debug("Please Check Your Server,Maybe You Don't Config!!");
                return

            server.build_job(item, param)
            '''update version build states, don't build next time'''

            version_id = info['versionid']
            sqlite.UpdateBuildField(version_id)

    def GetFreeServer(self, identifier, server):
        item = None
	logging.debug('GetFreeServer identifier:%s' %identifier)
        job_list = server.get_all_jobs()
        idle_list = []
        busy_list = []
        for job in job_list:
	    job_name = job['name']
            if not job_name.lower().__contains__(identifier):
                continue
            logging.debug('job name:%s' %job_name)
            txt = server.get_job_config(job_name)
            node = txt[txt.index('<assignedNode>') + len('<assignedNode>'):txt.index('</assignedNode>')]
            print 'node:%s' %node
            info = server.get_node_info(node)
            if info['idle'] == True:
                idle_list.append(job_name)
            else:
                busy_list.append(job_name)

	if len(idle_list) > 0:
            item = random.choice(idle_list)
        elif len(busy_list) > 0:
            item = random.choice(busy_list)
        logging.debug('idle server list:%s' %idle_list)
        logging.debug('ramdom free server %s' %item)

	return item

    def GetFixServer(self, identifier):

        mapping = [
                    {'iden':'IOT001', 'job':'IOT-157'}]

        server_list = []
        item = None
        for i in mapping:
            if identifier.lower().__eq__(i['iden'].lower()):
                server_list.append(i['job'])

	if len(server_list) > 0:
            item = random.choice(server_list)
        return item


    def Test(self):
        server = jenkins.Jenkins('http://127.0.0.1:8081', username='tdleo', password='1234Qwer')
        print server.get_nodes()
	info = server.get_node_info('33-150')
	print info['idle']

if __name__ == '__main__':
    job = jobs()
    job.Test()

