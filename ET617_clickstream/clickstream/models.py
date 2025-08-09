from django.db import models

class ClickstreamEvent(models.Model):
    student_id = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    page_url = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.student_id} - {self.action} @ {self.timestamp}"
