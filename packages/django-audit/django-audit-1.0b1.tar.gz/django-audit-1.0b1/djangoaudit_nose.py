# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2010, 2degrees Limited <egoddard@tech.2degreesnetwork.com>.
# All Rights Reserved.
#
# This file is part of djangoaudit <https://launchpad.net/django-audit/>,
# which is subject to the provisions of the BSD at
# <http://dev.2degreesnetwork.com/p/2degrees-license.html>. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED "AS IS"
# AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST
# INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os

from nose.plugins import Plugin
from pymongo.errors import PyMongoError

# Have to set this here to ensure this is Django-like
os.environ['DJANGO_SETTINGS_MODULE'] =  "tests.fixtures.sampledjango.settings"

from django.conf import settings

from djangoaudit.connection import MONGO_CONNECTION

class DjangoMongoDBPlugin(Plugin):
    """
    Ensure that before any MongoDB tests are run the correct test MongoDB
    environment is setup with a test database and collection and also that
    between cases, the collection is emptied so that no data pollution takes
    place between test cases.
    
    """
    
    name = "django-mongo"
    test_db_name = u'%s_test' % settings.MONGO_DATABASE_NAME
    audit_collection_name = u"audit_data"
    
    def begin(self):
        """
        Ensure that the test database exists and is free from any previous data
        
        """
        
        # This will either get or create the database
        test_db = MONGO_CONNECTION.connection[self.test_db_name]
        
        # Now set this on the MONOGO_CONNECTION:
        MONGO_CONNECTION._database = test_db
        
    def beforeTest(self, test):
        """Ensure that we've got a fresh collection before each test"""
        
        test_db = MONGO_CONNECTION.database
        
        try:
            test_db.drop_collection(self.audit_collection_name)
        except PyMongoError, exc:
            pass
            
        # Now create a fresh auditing collection:
        test_db.create_collection(self.audit_collection_name)
        
    def afterTest(self, test):
        """
        Ensure the auditing collection is torn down after the test completes
        """
        
        try:
            MONGO_CONNECTION.database.drop_collection(self.audit_collection_name)
        except PyMongoError, exc:
            print "Couldn't drop auditing collection. Error was: %s" % exc
        
            
    def finalize(self, result=None):
        """Remove the test database from MongoDB"""
        
        try:
            MONGO_CONNECTION.connection.drop_database(MONGO_CONNECTION.database)
        except PyMongoError, exc:
            print "Couldn't drop test database. Error was: %s" % exc
             