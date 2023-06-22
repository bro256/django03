from datetime import date, datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

User = get_user_model()

# class Priority(models.Model):
#     content = models.CharField(_('content'), max_length=100, null=True, blank=True)

#     class Meta:
#         verbose_name = _("priority")
#         verbose_name_plural = _("priorities")

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("priority_detail", kwargs={"pk": self.pk})
    

# class Status(models.Model):
#     content = models.CharField(_('content'), max_length=50)

#     class Meta:
#         verbose_name = _("status")
#         verbose_name_plural = _("statuses")

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse("status_detail", kwargs={"pk": self.pk})


class Task(models.Model):
    content = models.CharField(_('content'), max_length=250)
    note = models.TextField(_('note'), max_length=10000, null=True, blank=True,)
    start = models.DateField(_('start'),null=True, blank=True,)
    finish = models.DateField(_('finish'),null=True, blank=True,)
    owner = models.ForeignKey(
        User,
        verbose_name=_("owner"),
        on_delete=models.CASCADE,
        related_name='owner_tasks',
        null=True, blank=True,
    )
    # assignee = models.ManyToManyField(User, related_name='assignee_tasks')
    assignee = models.ForeignKey(
        User,
        verbose_name=_("assignee"),
        on_delete=models.CASCADE,
        related_name='assignee_tasks',
        null=True, blank=True,
    )
    # priority = models.ForeignKey(
    #     Priority,
    #     verbose_name=_("priority"),
    #     on_delete=models.CASCADE,
    #     related_name='tasks',
    #     null=True, blank=True,
    # )
    # status = models.ForeignKey(
    #     Status,
    #     verbose_name=_('status'),
    #     on_delete=models.CASCADE,
    #     related_name='tasks',
    #     null=True, blank=True,
    # )

    PRIORITY_CHOICES = (
        (1, _('Low')),
        (2, _('Medium')),
        (3, _('High')),
        (4, _('Critical')),
    )
    priority = models.PositiveSmallIntegerField(
        _("priority"), 
        choices=PRIORITY_CHOICES, 
        default=2,
        db_index=True,
    )

    STATUS_CHOICES = (
        (0, _('Not started')),
        (1, _('In progess')),
        (2, _('On hold')),
        (3, _('Cancelled')),
        (4, _('Completed')),
    )
    status = models.PositiveSmallIntegerField(
        _("status"), 
        choices=STATUS_CHOICES, 
        default=0,
        db_index=True,
    )
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True)    

    @property
    def is_overdue(self):
        if self.finish and date.today() > self.finish and self.status < 2:
            return True
        return False

    class Meta:
        ordering = ['status', 'finish', '-priority']
        verbose_name = _("task")
        verbose_name_plural = _("tasks")

    def mark_task_as_read(task):
        task.is_read = True
        task.read_at = datetime.now()
        task.save()

    def __str__(self):
        return f"{self.content} - {self.get_status_display()}"

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})
    

class TaskComment(models.Model):
    content = models.CharField(_('content'), max_length=250)
    task = models.ForeignKey(
        Task,
        verbose_name=_("task"),
        on_delete=models.CASCADE,
        related_name='comments',
        null=True, blank=True,
    )
    commenter = models.ForeignKey(
        User,
        verbose_name=_("commenter"),
        on_delete=models.CASCADE,
        related_name='task_comments',
        null=True, blank=True,
    )
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _("task comment")
        verbose_name_plural = _("task comments")

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("taskcomment_detail", kwargs={"pk": self.pk})