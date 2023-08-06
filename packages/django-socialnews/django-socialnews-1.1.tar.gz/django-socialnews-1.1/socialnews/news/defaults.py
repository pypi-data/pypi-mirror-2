KARMA_COST_NEW_TOPIC = 0
KARMA_COST_NEW_LINK = 0
SITE = 'reddit.com'

MAX_CHANGE_PER_VOTE = 10

DEFAULT_PROFILE_KARMA = 20
CREATORS_KARMA_PER_VOTE = 1
DAMP_FACTOR = 1.1
DAMPEN_POINTS_AFTER = 100
TOP_TOPICS_ON_MAINPAGE = 3
NEW_TOPICS_ON_MAINPAGE = 3
TAGS_ON_MAINPAGE = 3
DATE_FORMAT = '%Y-%m-%d'

CALCULATE_RELATED_AFTER = [10, 20, 50]
MAX_RELATED_LINKS = 10
MIN_VOTES_IN_RELATED = 5

LINKS_PER_PAGE = 15
UNALLOWED_TOPIC_NAMES = ['my', 'new', 'about', 'aboutus', 'help', 'up', 'down', 'user', 'admin', 'foo', 'logout', 'register', 'site_media', 'dummy', 'subscribe', 'unsubscribe', 'search', 'buttons', 'recommended', 'createtopics', 'topics', 'tag', 'feeds', 'save', 'upcomment', 'downcomment']

#For Stats Page
TOP_TOPICS = 10
TOP_USERS = 10
TOP_LINKS = 10


#Recommnded for users

#Defaults for cron jobs
sample_corpus_location = 'c:/corpus.db'
log_file = 'c:/log.log'
calculate_recommended_timediff = 60 * 60 #1 hours
min_links_submitted = 5
min_links_liked = 5
max_links_in_corpus = 100000