import webapp2
from google.appengine.ext import ndb
from models import *
import json

class BettingHandler(webapp2.RequestHandler):
    def get(self):
    	opportunities = json.loads(MiscData.query(MiscData.key == 'latest-betting-opportunities').fetch(1)[0].value)
        self.response.write("""<html><head><title>Betting opportunities</title><script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
        	<script src="https://cdn.rawgit.com/MikeMcl/big.js/master/big.min.js"></script></head><body>""")
        self.response.write('<h1>Betting opportunities:</h1>')

        self.response.write('<ul>')
        i = 0
        for opportunity in opportunities:
        	self.response.write('<li>')
        	self.response.write('<b>%(name)s</b> - %(rate).2f<span> %%' % {"name" : opportunity["name"], "rate" : opportunity['chances']['rate']})
        	self.response.write('<p>Back - %(backOdds).2f <a href="%(backUrl)s" target="_blank">%(backUrl)s</a></p>' % opportunity)
        	self.response.write('<p>Lay - %(layOdds).2f with %(layMoney).2f EUR <a href=%(layUrl)s" target="_blank">%(layUrl)s</a></p>' % opportunity)
        	self.response.write("""<input type="text" class="moneyInput" data-index="%(index)d"/> - Back 
        		<span id="back%(index)d" class="backSuggestedAmount"></span> EUR and lay 
        		<span id="lay%(index)d" class="laySuggestedAmount"></span> EUR (with liability of 
        		<span id="liability%(index)s" class="liabilitySuggestedAmount"></span>) and win 
        		<span id="win%(index)s" class="winSuggestedAmount"></span> EUR""" % {"index": i})
        	self.response.write('</li>')
        	i += 1
        self.response.write('</ul>')
        self.response.write('<script>bettingOpportunities = ' + json.dumps(opportunities) + ';</script>')
        self.response.write("""
        	<script>
        		var recalculateFunc = function(e){
        			var money = parseFloat($(this).val());
        			var index = parseInt($(this).attr('data-index'));
        			var chances = bettingOpportunities[index].chances;

        			var backMoney = money * chances.backPercentage / chances.totalPercentage;
        			var layLiability = money * chances.layPercentage / chances.totalPercentage;

        			var layOdds = new Big(bettingOpportunities[index].layOdds);
        			layOdds = layOdds.div(layOdds.minus(1))
        			var layMoney = layOdds.minus(1).times(layLiability);

        			var winnings = new Big(money).div(new Big(chances.totalPercentage).div(100)).minus(money);
        			$('#win' + index).text(winnings.toFixed(2));
        			$('#back' + index).text(backMoney.toFixed(2));
        			$('#lay' + index).text(layMoney.toFixed(2));
        			$('#liability' + index).text(layLiability.toFixed(2));
        		};
        		$('.moneyInput').change(recalculateFunc).keyup(recalculateFunc);
        	</script>
        """);
        self.response.write('</body></html>')
