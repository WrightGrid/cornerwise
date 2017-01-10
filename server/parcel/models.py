from django.contrib.gis.db import models


class ParcelManager(models.GeoManager):
    def containing(self, point):
        return self.filter(shape__contains=point)


class Parcel(models.Model):
    gid = models.AutoField(primary_key=True)
    shape_leng = models.DecimalField(
        max_digits=1000, decimal_places=24, blank=True, null=True)
    shape_area = models.DecimalField(
        max_digits=1000, decimal_places=24, blank=True, null=True)
    map_par_id = models.CharField(max_length=26, blank=True, null=True)
    loc_id = models.CharField(max_length=18, blank=True, null=True, unique=True)
    poly_type = models.CharField(max_length=15, blank=True, null=True)
    map_no = models.CharField(max_length=4, blank=True, null=True)
    source = models.CharField(max_length=15, blank=True, null=True)
    plan_id = models.CharField(max_length=40, blank=True, null=True)
    last_edit = models.IntegerField(blank=True, null=True)
    town_id = models.SmallIntegerField(blank=True, null=True)
    shape = models.MultiPolygonField(srid=4326, blank=True, null=True)

    # Address:
    address_num = models.CharField(max_length=64, null=True)
    # Stored in all caps:
    full_street = models.CharField(max_length=128, null=True)

    objects = ParcelManager()

    def index_attributes(self):
        return {a.name: a.value for a in self.attributes.all()}


class Attribute(models.Model):
    parcel = models.ForeignKey(Parcel, related_name="attributes")
    name = models.CharField(max_length=64, db_index=True)
    value = models.CharField(max_length=256, db_index=True)

    class Meta:
        unique_together = (("parcel", "name"))
