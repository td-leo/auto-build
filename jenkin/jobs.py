__author__ = 'xulei'

import jenkins
import random
import logging
class jobs:
    def Build(self, sqlite):

        info_list = sqlite.GetBuildInfo()
        if info_list == None or len(info_list) <= 0:
            return
        server = jenkins.Jenkins('http://127.0.0.1:8081', username='leixu', password='Xl225316644')
	print server
        print server.jobs_count()
        for info in info_list:
            param = {'release:':None, 'type': None, 'channel':None}
            param['release'] = info['release']
            param['type'] = info['type']
            param['channel'] = info['channel']
            identifier = info['identifier']
            param['name'] = info['name']
            logging.debug('Build State:' + info['build'])

            if info['build'] == '1':return

            logging.debug('Trigger Build! identifier:%s, %s' %(identifier, param))

            #server.build_job(job, param)
	    item = self.GetFreeServer(identifier, server)
            server.build_job(item, param)

            '''update version build states, don't build next time'''

            version_id = info['versionid']
            sqlite.UpdateBuildField(version_id)

    def GetFreeServer(self, identifier, server):
	print 'GetFreeServer identifier:%s' %identifier
        job_list = server.get_all_jobs()
        idle_list = []
        busy_list = []
        for job in job_list:
	    job_name = job['name']
            if not job_name.lower().__contains__(identifier):
                continue
            logging.DEBUG('job name:%s' %job_name)
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
        else:
            item = random.choice(busy_list)
        logging.debug('idle server list:%s' %idle_list)
        logging.debug('ramdom free server %s' %item)

	return item

    def Test(self):
        server = jenkins.Jenkins('http://127.0.0.1:8081', username='leixu', password='Xl225316644')
        print server.get_nodes()
	info = server.get_node_info('33-150')
	print info['idle']

if __name__ == '__main__':
    job = jobs()
    job.Test()

