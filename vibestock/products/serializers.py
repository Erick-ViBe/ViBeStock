from rest_framework import serializers

from vibestock.products.models import Product, ExpirationAlerts


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'stock', 'expiration_date']


class ExpirationAlertsSerializer(serializers.ModelSerializer):

    def validate_number_of_days(self, value):
        expiration_alerts = ExpirationAlerts.objects.filter(
            user=self.context['request'].user
        ).values_list('number_of_days')
        expiration_alerts_days = [ day[0] for day in expiration_alerts ]
        if value in expiration_alerts_days:
            raise serializers.ValidationError(
                "There is already an alert configured with these days"
            )
        return value

    class Meta:
        model = ExpirationAlerts
        fields = ['id', 'number_of_days']
