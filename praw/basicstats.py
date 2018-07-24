from prawtools.stats import SubredditStats

from prawtools.stats import logger as lg
import logging

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logger = logging.getLogger('prawcore')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

logger2 = logging.getLogger('prawtools')
logger2.setLevel(logging.DEBUG)
logger2.addHandler(handler)
#lg.setLevel(logging.DEBUG)


def basic_stats(srs):
    """Return a markdown representation of simple statistics."""
    comment_score = sum(comment.score for comment in srs.comments)
    if srs.comments:
        comment_duration = (srs.comments[-1].created_utc -
                            srs.comments[0].created_utc)
        comment_rate = srs._rate(len(srs.comments), comment_duration)
    else:
        comment_rate = 0

    submission_duration = srs.max_date - srs.min_date
    submission_rate = srs._rate(len(srs.submissions),
                                submission_duration)
    submission_score = sum(sub.score for sub in srs.submissions.values())

    # values = [('Total', len(srs.submissions), len(srs.comments)),
    #           ('Rate (per day)', '{:.2f}'.format(submission_rate),
    #            '{:.2f}'.format(comment_rate)),
    #           ('Unique Redditors', len(srs.submitters),
    #            len(srs.commenters)),
    #           ('Combined Score', submission_score, comment_score)]
    #
    values = [len(srs.submissions), len(srs.comments),submission_rate,comment_rate,
              len(srs.submitters),len(srs.commenters),submission_score, comment_score,submission_duration / 86400.]

    #retval = 'Period: {:.2f} days\n\n'.format(submission_duration / 86400.)
    #retval += '||Submissions|Comments|\n:-:|--:|--:\n'
    #for quad in values:
    #    retval += '__{}__|{}|{}\n'.format(*quad)
    #return retval + '\n'
    return values







srs = SubredditStats('eos', None, None)

#srs.max_date = 3600*24
#srs.run(1,10,10)

callback = srs.fetch_recent_submissions
view = int(1)
srs.fetch_submissions(callback, view)
stats = basic_stats(srs)

print (stats)
