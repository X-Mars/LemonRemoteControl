from django.shortcuts import render
from Zabbix.master import ZabbixMaster
from django.views.generic import View
from django.http import JsonResponse



# Create your views here.

class ZbbixView(View):
    http_method_names =  ['get']
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        alerts = ZabbixMaster().get_alerts()
        data = {
            'status': 'ok',
            'data': alerts
        }

        return JsonResponse(data=data)
