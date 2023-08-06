import datetime
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import html as html_utils
from askbot import const
from askbot.models import base
from askbot.models.user import EmailFeedSetting

class VoteManager(models.Manager):
    def get_up_vote_count_from_user(self, user):
        if user is not None:
            return self.filter(user=user, vote=1).count()
        else:
            return 0

    def get_down_vote_count_from_user(self, user):
        if user is not None:
            return self.filter(user=user, vote=-1).count()
        else:
            return 0

    def get_votes_count_today_from_user(self, user):
        if user is not None:
            today = datetime.date.today()
            return self.filter(user=user, voted_at__range=(today, today + datetime.timedelta(1))).count()
        else:
            return 0


class Vote(base.MetaContent, base.UserContent):
    VOTE_UP = +1
    VOTE_DOWN = -1
    VOTE_CHOICES = (
        (VOTE_UP,   u'Up'),
        (VOTE_DOWN, u'Down'),
    )

    vote           = models.SmallIntegerField(choices=VOTE_CHOICES)
    voted_at       = models.DateTimeField(default=datetime.datetime.now)

    objects = VoteManager()

    class Meta(base.MetaContent.Meta):
        unique_together = ('content_type', 'object_id', 'user')
        db_table = u'vote'

    def __unicode__(self):
        return '[%s] voted at %s: %s' %(self.user, self.voted_at, self.vote)

    def is_upvote(self):
        return self.vote == self.VOTE_UP

    def is_downvote(self):
        return self.vote == self.VOTE_DOWN

    def is_opposite(self, vote_type):
        assert(vote_type in (self.VOTE_UP, self.VOTE_DOWN))
        return self.vote != vote_type

    def cancel(self):
        """cancel the vote
        while taking into account whether vote was up
        or down

        return change in score on the post
        """
        #importing locally because of circular dependency
        from askbot import auth
        score_before = self.content_object.score
        if self.vote > 0:
            # cancel upvote
            auth.onUpVotedCanceled(self, self.content_object, self.user)

        else:
            # cancel downvote
            auth.onDownVotedCanceled(self, self.content_object, self.user)
        score_after = self.content_object.score

        return score_after - score_before


class FlaggedItemManager(models.Manager):
    def get_flagged_items_count_today(self, user):
        if user is not None:
            today = datetime.date.today()
            return self.filter(user=user, flagged_at__range=(today, today + datetime.timedelta(1))).count()
        else:
            return 0

class FlaggedItem(base.MetaContent, base.UserContent):
    """A flag on a Question or Answer indicating offensive content."""
    flagged_at     = models.DateTimeField(default=datetime.datetime.now)

    objects = FlaggedItemManager()

    class Meta(base.MetaContent.Meta):
        unique_together = ('content_type', 'object_id', 'user')
        db_table = u'flagged_item'

    def __unicode__(self):
        return '[%s] flagged at %s' %(self.user, self.flagged_at)

#todo: move this class to content
class Comment(base.MetaContent, base.UserContent):
    comment = models.CharField(max_length = const.COMMENT_HARD_MAX_LENGTH)
    added_at = models.DateTimeField(default = datetime.datetime.now)
    html = models.CharField(max_length = const.COMMENT_HARD_MAX_LENGTH, default='')

    _urlize = True
    _use_markdown = False
    _escape_html = True

    class Meta(base.MetaContent.Meta):
        ordering = ('-added_at',)
        db_table = u'comment'

    #these two are methods
    parse = base.parse_post_text
    parse_and_save = base.parse_and_save_post

    def get_origin_post(self):
        return self.content_object.get_origin_post()

    #todo: maybe remove this wnen post models are unified
    def get_text(self):
        return self.comment

    def set_text(self, text):
        self.comment = text

    def get_snippet(self):
        """returns an abbreviated snippet of the content
        todo: remove this if comment model unites with Q&A
        """
        return html_utils.strip_tags(self.html)[:120] + ' ...'

    def get_owner(self):
        return self.user

    def get_updated_activity_data(self, created = False):
        if self.content_object.__class__.__name__ == 'Question':
            return const.TYPE_ACTIVITY_COMMENT_QUESTION, self
        elif self.content_object.__class__.__name__ == 'Answer':
            return const.TYPE_ACTIVITY_COMMENT_ANSWER, self

    def get_response_receivers(self, exclude_list = None):
        """get list of users who authored comments on a post
        and the post itself
        """
        assert(exclude_list is not None)
        users = set()
        users.update(
                    #get authors of parent object and all associated comments
                    self.content_object.get_author_list(
                            include_comments = True,
                        )
                )
        users -= set(exclude_list)
        return list(users)

    def get_instant_notification_subscribers(
                                    self, 
                                    potential_subscribers = None,
                                    mentioned_users = None,
                                    exclude_list = None
                                ):
        """get list of users who want instant notifications
        about this comment

        argument potential_subscribers is required as it saves on db hits
        """
        #print 'in meta function'
        #print 'potential subscribers: ', potential_subscribers

        subscriber_set = set()

        if potential_subscribers:
            potential_subscribers = set(potential_subscribers)
        else:
            potential_subscribers = set()

        if mentioned_users:
            potential_subscribers.update(mentioned_users)

        if potential_subscribers:
            comment_subscribers = EmailFeedSetting.filter_subscribers(
                                        potential_subscribers = potential_subscribers,
                                        feed_type = 'm_and_c',
                                        frequency = 'i'
                                    )
            subscriber_set.update(comment_subscribers)
            #print 'comment subscribers: ', comment_subscribers

        origin_post = self.get_origin_post()
        selective_subscribers = origin_post.followed_by.all()
        if selective_subscribers:
            selective_subscribers = EmailFeedSetting.filter_subscribers(
                                    potential_subscribers = selective_subscribers,
                                    feed_type = 'q_sel',
                                    frequency = 'i'
                                )
            for subscriber in selective_subscribers:
                if origin_post.passes_tag_filter_for_user(subscriber):
                    subscriber_set.add(subscriber)

            subscriber_set.update(selective_subscribers)
            #print 'selective subscribers: ', selective_subscribers

        global_subscribers = EmailFeedSetting.filter_subscribers(
                                            feed_type = 'q_all',
                                            frequency = 'i'
                                        )
        #print 'global subscribers: ', global_subscribers

        subscriber_set.update(global_subscribers)

        #print 'exclude list is: ', exclude_list
        if exclude_list:
            subscriber_set -= set(exclude_list)

        #print 'final list of subscribers:', subscriber_set

        return list(subscriber_set)

    def get_time_of_last_edit(self):
        return self.added_at

    def delete(self, **kwargs):
        """deletes comment and concomitant response activity
        records, as well as mention records, while preserving
        integrity or response counts for the users
        """
        #todo: not very good import in models of other models
        #todo: potentially a circular import
        from askbot.models.user import Activity
        comment_content_type = ContentType.objects.get_for_model(self)
        comment_id = self.id

        #on these activities decrement response counter
        #todo: implement a custom delete method on these
        #all this should pack into Activity.responses.filter( somehow ).delete()
        response_activity_types = const.RESPONSE_ACTIVITY_TYPES_FOR_DISPLAY
        activities = Activity.objects.filter(
                            content_type = comment_content_type,
                            object_id = comment_id,
                            activity_type__in = response_activity_types
                        )
        for activity in activities:
            for user in activity.receiving_users.all():
                user.decrement_response_count()
                user.save()
        activities.delete()

        #mentions - simply delete
        mentions = Activity.objects.get_mentions(mentioned_in = self)
        mentions.delete()
            
        super(Comment,self).delete(**kwargs)

    def get_absolute_url(self):
        origin_post = self.get_origin_post()
        return '%s#comment-%d' % (origin_post.get_absolute_url(), self.id)

    def get_latest_revision_number(self):
        return 1

    def __unicode__(self):
        return self.comment
