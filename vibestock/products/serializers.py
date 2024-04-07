from django.conf import settings

from rest_framework import serializers

from vibestock.products.models import Product, ExpirationAlerts


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'stock',
            'expiration_date',
            'status',
            'days_to_expire',
            'expired_days'
        ]
        extra_kwargs = {
            'status': { 'read_only': True },
        }


class ExpirationAlertsSerializer(serializers.ModelSerializer):

    def validate_number_of_days(self, value):
        default_expiration_days = settings.DEFAULT_PRODUCT_EXPIRATION_ALERT_DAYS
        if value in default_expiration_days:
            raise serializers.ValidationError(
                f"By default we generate alert on days {default_expiration_days}"
            )
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
