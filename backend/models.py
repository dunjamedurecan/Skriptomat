from django.db import models

class Authentications(models.Model):
    user_id = models.OneToOneField('Users', models.DO_NOTHING, db_column='userId', primary_key=True)
    provider = models.CharField(max_length=50)
    external_id = models.CharField(db_column='externalId', max_length=100)

    class Meta:
        managed = True
        db_table = 'Authentications'


class Donations(models.Model):
    donor_id = models.ForeignKey('Users', models.DO_NOTHING, db_column='donorId')
    recipient_id = models.ForeignKey('Users', models.DO_NOTHING, db_column='recipientId', related_name='donations_recipient_set')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.TextField(db_column='paymentMethod', db_comment='PayPal or Credit Card')
    payment_date = models.DateTimeField(db_column='paymentDate', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Donations'


class Courses(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField(blank=True, null=True, db_comment='Year of study (1–6)')
    semester = models.IntegerField(blank=True, null=True, db_comment='Semester (1 or 2)')
    created_at = models.DateTimeField(db_column='createdAt', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Courses'


class Comments(models.Model):
    user_id = models.ForeignKey('Users', models.DO_NOTHING, db_column='userId')
    material_id = models.ForeignKey('Materials', models.DO_NOTHING, db_column='materialId')
    text = models.TextField()
    created_at = models.DateTimeField(db_column='createdAt', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Comments'


class Users(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100)
    role_id = models.ForeignKey('Roles', models.DO_NOTHING, db_column='roleId')
    created_at = models.DateTimeField(db_column='createdAt', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Users'


class Materials(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    course_id = models.ForeignKey(Courses, models.DO_NOTHING, db_column='courseId')
    author_id = models.ForeignKey(Users, models.DO_NOTHING, db_column='authorId')
    year = models.IntegerField()
    allow_download = models.BooleanField(db_column='allowDownload', blank=True, null=True)
    file_path = models.TextField(db_column='filePath')
    status = models.TextField(blank=True, null=True)
    deleted = models.BooleanField(blank=True, null=True, db_comment='Logical deletion (true = hidden)')
    created_at = models.DateTimeField(db_column='createdAt', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Materials'


class Moderations(models.Model):
    moderator_id = models.ForeignKey(Users, models.DO_NOTHING, db_column='moderatorId')
    material_id = models.ForeignKey(Materials, models.DO_NOTHING, db_column='materialId')
    status = models.TextField()
    comment = models.TextField(blank=True, null=True)
    moderation_date = models.DateTimeField(db_column='moderationDate', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Moderations'


class Notifications(models.Model):
    user_id = models.ForeignKey(Users, models.DO_NOTHING, db_column='userId')
    material_id = models.ForeignKey(Materials, models.DO_NOTHING, db_column='materialId')
    sent_at = models.DateTimeField(db_column='sentAt', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Notifications'


class Ratings(models.Model):
    user_id = models.ForeignKey(Users, models.DO_NOTHING, db_column='userId')
    material_id = models.ForeignKey(Materials, models.DO_NOTHING, db_column='materialId')
    value = models.IntegerField(blank=True, null=True, db_comment='1 = upvote, -1 = downvote')
    created_at = models.DateTimeField(db_column='createdAt', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Ratings'
        unique_together = (('user_id', 'material_id'),)


class Messages(models.Model):
    sender_id = models.ForeignKey(Users, models.DO_NOTHING, db_column='senderId')
    recipient_id = models.ForeignKey(Users, models.DO_NOTHING, db_column='recipientId', related_name='messages_recipient_set', blank=True, null=True)
    message_text = models.TextField(db_column='messageText')
    sent_at = models.DateTimeField(db_column='sentAt', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Messages'


class Subscriptions(models.Model):
    pk = models.CompositePrimaryKey('userId', 'courseId')
    user_id = models.ForeignKey(Users, models.DO_NOTHING, db_column='userId')
    course_id = models.ForeignKey(Courses, models.DO_NOTHING, db_column='courseId')
    subscription_date = models.DateTimeField(db_column='subscriptionDate', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Subscriptions'


class Roles(models.Model):
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'Roles'
