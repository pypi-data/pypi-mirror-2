#!/usr/bin/python2.4
# -*- coding: utf-8 -*-
#
# Copyright 2010 Google Inc. All Rights Reserved.

"""Simple command-line example for Moderator.

Command-line application that exercises the Google Moderator API.
"""

__author__ = 'jcgregorio@google.com (Joe Gregorio)'

import gflags
import httplib2
import logging
import sys

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS
FLOW = OAuth2WebServerFlow(
    client_id='433807057907.apps.googleusercontent.com',
    client_secret='jigtZpMApkRxncxikFpR+SFg',
    scope='https://www.googleapis.com/auth/moderator',
    user_agent='moderator-cmdline-sample/1.0')

gflags.DEFINE_enum('logging_level', 'ERROR',
    ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    'Set the level of logging detail.')


def main(argv):
  try:
    argv = FLAGS(argv)
  except gflags.FlagsError, e:
    print '%s\\nUsage: %s ARGS\\n%s' % (e, argv[0], FLAGS)
    sys.exit(1)

  logging.getLogger().setLevel(getattr(logging, FLAGS.logging_level))

  storage = Storage('moderator.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid == True:
    credentials = run(FLOW, storage)

  http = httplib2.Http(cache=".cache")
  http = credentials.authorize(http)

  service = build("moderator", "v1", http=http)

  series_body = {
      "data": {
        "description": "Share and rank tips for eating healthy and cheap!",
        "name": "Eating Healthy & Cheap",
        "videoSubmissionAllowed": False
        }
      }
  series = service.series().insert(body=series_body).execute()
  print "Created a new series"

  topic_body = {
      "data": {
        "description": "Share your ideas on eating healthy!",
        "name": "Ideas",
        "presenter": "liz"
        }
      }
  topic = service.topics().insert(seriesId=series['id']['seriesId'],
                            body=topic_body).execute()
  print "Created a new topic"

  submission_body = {
      "data": {
        "attachmentUrl": "http://www.youtube.com/watch?v=1a1wyc5Xxpg",
        "attribution": {
          "displayName": "Bashan",
          "location": "Bainbridge Island, WA"
          },
        "text": "Charlie Ayers @ Google"
        }
      }
  submission = service.submissions().insert(seriesId=topic['id']['seriesId'],
      topicId=topic['id']['topicId'], body=submission_body).execute()
  print "Inserted a new submisson on the topic"

  vote_body = {
      "data": {
        "vote": "PLUS"
        }
      }
  service.votes().insert(seriesId=topic['id']['seriesId'],
                   submissionId=submission['id']['submissionId'],
                   body=vote_body)
  print "Voted on the submission"


if __name__ == '__main__':
  main(sys.argv)
