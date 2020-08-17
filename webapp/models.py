from django.db import models


class Credit(models.Model):
    """ Default form to ask the user """
    monto_uf = models.IntegerField(default=500, blank=True, null=True)
    payment_deadline_days = models.IntegerField(default=5, blank=True, null=True)
    payment_day_with_calculated_tmc = models.IntegerField(default=6, blank=True, null=True)

    class Meta:
        abstract=True


class RateOfTMC(Credit):
    """ Result of the calculations made with the TMC """
    valor_tmc_at_day = models.IntegerField(default=6, blank=True, null=True)
    message = models.CharField(max_length=300)

    def __str__(self):
        """Returns a string representation of a message."""
        return f"'{self.message}' to pay at day {self.payment_day_with_calculated_tmc}"


class TMC(models.Model):
    """ Only two types are supported for less than 90 days
        type 25: Superiores al equivalente de 5.000 unidades de fomento
        type 26: Inferiores o iguales al equivalente de 5.000 unidades de fomento """

    titulo = models.CharField(max_length=300)
    subtitulo = models.CharField(max_length=300)
    valor = models.CharField(max_length=300)
    tipo = models.CharField(max_length=300)
