#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright(c) 2015 Nippon Telegraph and Telephone Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import MySQLdb
import argparse
import subprocess


SHOW_CMD = ("mysql --host=%s --database=vm_ha "
            "--user=%s --password=%s "
            "-e\"SELECT "
            "create_at,"
            "update_at,"
            "notification_id,"
            "notification_type,"
            "notification_regionID,"
            "notification_hostname,"
            "notification_uuid,"
            "notification_time,"
            "notification_eventID,"
            "notification_eventType,"
            "notification_detail,"
            "notification_startTime,"
            "notification_endTime,"
            "notification_tzname,"
            "notification_daylight,"
            "notification_cluster_port,"
            "progress,"
            "recover_by "
            "FROM notification_list "
            "WHERE deleted = 0 "
            "AND (progress = 0 OR progress = 3)\";")


class NotificationStatusManager(object):
    def __init__(self):
        parser = argparse.ArgumentParser(prog='notification_status_manage.py', add_help=False)
        parser.add_argument('--mode', help='list')
        parser.add_argument('--db-user', help='mysql user name')
        parser.add_argument('--db-password', help='mysql user password')
        parser.add_argument('--db-host', help='mysql host name')

        args = parser.parse_args()

        if not self._check_args(args):
            parser.print_help()
            return

        msg = "notification status manage execution start"
        print msg

        try:
            count = self._get_notification_list_count(
                args.db_user, args.db_password, args.db_host)
            if count == 0:
                print "notification_list is empty"                        
            else:
                show_cmd = SHOW_CMD % (
                    args.db_host, args.db_user, args.db_password)
                subprocess.call(show_cmd, shell=True)
        except:
            # 全ての例外を握りつぶすのよくない
            msg = "notification status manage execution failure"
            print msg

        msg = "notification status manage execution end"
        print msg

    def _check_args(self, args):
        if args.mode != "list":
            return False

        if (args.db_user is None
         or args.db_password is None
         or args.db_host is None):
            return False

    def _db_connect(self,
                    mysql_user_name,
                    mysql_user_password,
                    mysql_host_name):
        db = MySQLdb.connect(host=mysql_host_name,
                             db='vm_ha',
                             user=mysql_user_name,
                             passwd=mysql_user_password,
                             charset='utf8')
        return db

    def _get_notification_list_count(self,
                                  mysql_user_name,
                                  mysql_user_password,
                                  mysql_host_name):
        db = self._db_connect(args.db_user,
                              args.db_password,
                              args.db_host)
        cursor = db.cursor(MySQLdb.cursors.DictCursor)
        sql = ("SELECT * FROM notification_list "
               "WHERE deleted = 0 "
               "AND (progress = 0 OR progress = 3)")
        try:
            row_cnt = cursor.execute(sql)
            return row_cnt
        except:
            msg = "notification_list select failed"
            print msg
            raise
        finally:
            db.close()

if __name__ == '__main__':
    NotificationStatusManager()


##########################################################################################
#
#(command)
#
#[python notification_status_manage.py --mode list --db-user root --db-password openstack --db-host localhost]
#
##########################################################################################

