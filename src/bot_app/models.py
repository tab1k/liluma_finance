from django.db import models


class FinancialData(models.Model):
    month = models.CharField(max_length=20)  # Месяц
    income = models.PositiveIntegerField()    # Доход
    expenses = models.PositiveIntegerField()  # Расходы
    profit = models.PositiveIntegerField()    # Прибыль
    tax = models.PositiveIntegerField()       # Налог

    def __str__(self):
        return f"{self.month}: Доход {self.income}€, Расходы {self.expenses}€, Прибыль {self.profit}€, Налог {self.tax}€"

    class Meta:
        ordering = ['month']
        verbose_name = "Финансовые данные"
        verbose_name_plural = "Финансовые данные"
