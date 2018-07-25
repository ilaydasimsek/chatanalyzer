import json
import urllib

from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic.base import View
from django.views.generic.list import ListView

from analyzer.models import UserStatistics, User
from analyzer.management.calculations.bestfriendcalculation import BestFriendCalculation
from analyzer.management.calculations.ownerfinder import OwnerFinder


default_length_dict = {'Very Short': 0, 'Short': 0, 'Medium': 0, 'Long': 0, 'Very Long': 0}


class IndexView(View):
    def get(self, request):
        return render(request, 'analyzer/index.html',
                      context={})
class StatisticsView(View):
    def get(self, request):
        return render(request, 'analyzer/statistics.html',
                      context={})


class SuggestFriendsView(View):
    def get(self, request):
        username = request.user.username
        calculator = BestFriendCalculation(3, username)
        suggestion_list = calculator.find_best_friends()
        return render(request, 'analyzer/suggest_friends.html',
                      context={'best_match': suggestion_list[0][0], 'suggestion_list': suggestion_list})


class FindOwnerView(ListView):
    def get(self, request):
        username = request.user.username
        return render(request, 'analyzer/find_owner.html')


class FindOwnerResultView(View):
    def get(self, request):
        message = urllib.parse.unquote(request.COOKIES['message_text'])
        (owner, confidence) = OwnerFinder.find_owner(message)
        if confidence == -1:
            return HttpResponse("unknown")
        return HttpResponse(owner)


class CurrentUserStatsView(ListView):
    def get(self, request):
        user_statistics = self.get_statistics_object(request)
        positivity_percentage = user_statistics.positivity_percentage
        return render(request, 'analyzer/current_user_stats.html',
                      context={'positivity_percentage': positivity_percentage})

    @staticmethod
    def get_statistics_object(request):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        statistics = UserStatistics.objects.get(user=user)
        return statistics


class ChartView(View):
    def get(self, request, **kwargs):
        username = kwargs['username']
        user_statistics = self.get_statistics_object(username)
        table_data = {}
        default_data_list = [0, 0, 0, 0,
                             0]  # returns a data list of zeroes to chart for error handling (some of the user
        #  statistics in database might be null)
        if (kwargs['chart_name'] == 'time' and user_statistics.avg_time):
            table_data = json.loads(user_statistics.avg_time)

        elif (kwargs['chart_name'] == 'length' and user_statistics.avg_text_length):
            table_data = json.loads(user_statistics.avg_text_length)

        else:
            return HttpResponse(json.dumps(default_data_list))

        data_list = [table_data['Very Short'], table_data['Short'], table_data['Medium'], table_data['Long'],
                     table_data['Very Long']]
        return HttpResponse(json.dumps(data_list))

    @staticmethod
    def get_statistics_object(username):
        user = get_object_or_404(User, username=username)
        statistics = UserStatistics.objects.get(user=user)
        return statistics
