from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
class SiteUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    description = models.TextField(default='I am me')
    pfpurl = models.TextField(default='https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg')
    problemssolved = models.TextField(default='0')
    points = models.IntegerField(default=0)
    def getinfo(self):
        return{
      
            "id":self.id,
            "username":self.username,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "profilepic": self.pfpurl,
            "description":self.description,
            "points": self.points,
            "problemssolved": self.problemssolved.split(),
        }

class Problem(models.Model):
    title = models.TextField()
    qmduuid = models.TextField()
    amduuid = models.TextField()
    answer = models.TextField()
    xpvalue = models.IntegerField()
    expiry = models.DateTimeField()
    release = models.DateTimeField()

    def getinfo(self):
        return {
            "id": self.id,
            "title":self.title,
            "qmduuid": self.qmduuid,
            "xpvalue":self.xpvalue,
            "expiry":self.expiry

        }
    def getanswer(self):
        return {
            "solutiontext": self.amduuid,
            "amduuid": self.answer
        }
class Submission(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    timesubmitted = models.DateTimeField()
    correct = models.BooleanField()
    at1 = models.IntegerField() 
    def getinfo(self):
        return {
            "id": self.id,
            "problem":self.problem.getinfo(),
            "user": self.user.getinfo(),
            "timesubmitted":self.timesubmitted,
            "correct": self.correct,
        }
