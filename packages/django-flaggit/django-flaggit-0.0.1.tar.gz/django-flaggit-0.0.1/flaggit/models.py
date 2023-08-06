from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, post_init
from flaggit.signals import flagged, review, rejected, approved


FLAGGED = 1
REVIEW = 2
CONTENT_REJECTED = 3
CONTENT_APPROVED = 4

FLAG_CHOICES = (
    (FLAGGED, 'Flagged'),
    (REVIEW, 'Under review'),
    (CONTENT_REJECTED, 'Rejected'),
    (CONTENT_APPROVED, 'Approved'),
)

class Flag(models.Model):
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)
    content_object = generic.GenericForeignKey("content_type", "object_id")
    
    _pre_save_status = None
    status = models.PositiveIntegerField(choices=FLAG_CHOICES, default=FLAGGED)
    created = models.DateTimeField(auto_now_add=True)
    reviewed = models.DateTimeField(blank=True, null=True)
    reviewer = models.ForeignKey(User, blank=True, null=True)
    
    comment = models.TextField(blank=True, null=True)
    
    
    
    def __unicode__(self):
        return u'%s: %s' % (self.get_status_display(), self.content_object)

    @property
    def num_flags(self):
        return self.flag_set.count()

class FlagInstance(models.Model):
    flag = models.ForeignKey(Flag, related_name='flags')
    user = models.ForeignKey(User, blank=True, null=True)
    ip = models.IPAddressField(blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    
    comment = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return u'%s: %s' % (self.user, self.flag.content_object)

def post_init_handler(sender, instance, **kwargs):
    instance._pre_save_status = instance.status

def flag_handler(sender, instance, created=False, **kwargs):
    if created:
        flagged.send(instance.content_object, flag=instance, created=created)
        return

    # The status didn't change. Return.
    if instance._pre_save_status == instance.status:
        return

    if instance.status == FLAGGED:
        flagged.send(instance.content_object, flag=instance, created=False)
    elif instance.status == REVIEW:
        review.send(instance.content_object, flag=instance)
    elif instance.status == CONTENT_REJECTED:
        rejected.send(instance.content_object, flag=instance)
    elif instance.status == CONTENT_APPROVED:
        approved.send(instance.content_object, flag=instance)

    
def flag_instance_handler(sender, instance, created=False, **kwargs):
    if not created:
        return
    
    flagged.send(instance.flag.content_object, flag=instance.flag, created=False)

post_init.connect(post_init_handler, sender=Flag, dispatch_uid='flaggit.flag.post_init')
post_save.connect(flag_handler, sender=Flag, dispatch_uid='flaggit.flag.post_save')
post_save.connect(flag_instance_handler, sender=FlagInstance,
    dispatch_uid='flaggit.flaginstance.post_save')
