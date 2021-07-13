from django.db import models

# Create your models here.
class Level(models.Model):
    number = models.IntegerField('number')

    def __str__(self):
        return str(self.id) + ' - ' + str(self.number)

class Title(models.Model):
    name = models.CharField('name', max_length=80)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.name + ' - ' + str(self.level)


class Hashtag(models.Model):
    name = models.CharField('name', max_length=80)
    sharepoint = models.CharField('sharepoint', max_length=80, blank=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' - ' + self.sharepoint + ' - ' + self.title
