from django.db import models


class Zone(models.Model):
    min_x = models.IntegerField(default=0)
    min_y = models.IntegerField(default=0)
    max_x = models.IntegerField(default=0)
    max_y = models.IntegerField(default=0)
    name = models.CharField(max_length=1000)

    def __str__(self):
        return 'name: {0}, polygon: minX: {1}, minY: {2}, maxX: {3}, maxY: {4}'.format(self.name,
                                                                                       self.min_x,
                                                                                       self.min_y,
                                                                                       self.max_x,
                                                                                       self.max_y)
