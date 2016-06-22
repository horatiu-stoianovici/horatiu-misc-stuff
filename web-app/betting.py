import webapp2
from google.appengine.ext import ndb
from models import *
import json

class BettingHandler(webapp2.RequestHandler):
    def get(self):
    	opportunities = json.loads(MiscData.query(MiscData.key == 'latest-betting-opportunities').fetch(1)[0].value)
        self.response.write("""<html>
            <head>
                <title>Betting opportunities</title>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
                <script src="https://cdn.rawgit.com/MikeMcl/big.js/master/big.min.js"></script>
                <link rel="stylesheet" href="/static/css/betting.css" />
            </head>
            <body>""")
        self.response.write('<h1>Betting opportunities:</h1>')

        self.response.write('<ul>')
        i = 0
        for opportunity in opportunities:
        	self.response.write('<li> <div class="container">')
        	self.response.write('<b>%(name)s</b> - %(rate).2f<span> %%' % {"name" : opportunity["name"], "rate" : opportunity['chances']['rate']})
        	self.response.write('<div class="container backBackground">Back - %(backOdds).2f <a href="%(backUrl)s" target="_blank">%(backUrl)s</a></div>' % opportunity)
        	self.response.write('<div class="container layBackground">Lay - %(layOdds).2f with %(layMoney).2f EUR <a href="%(layUrl)s" target="_blank">%(layUrl)s</a></div>' % opportunity)
        	self.response.write("""<div class="suggestionsContainer"><div>Total <input type="text" class="moneyInput" data-index="%(index)d" id="total%(index)d"/> EUR</div><div> Back 
        		<input type="text" data-index="%(index)d" id="back%(index)d" class="backSuggestedAmount"> EUR </div><div> Lay 
        		<input type="text" data-index="%(index)d" id="lay%(index)d" class="laySuggestedAmount"> EUR (with liability of 
        		<input type="text" data-index="%(index)d" id="liability%(index)s" class="liabilitySuggestedAmount">) </div><div> Win 
        		<input type="text" data-index="%(index)d" id="win%(index)s" class="winSuggestedAmount"> EUR</div></div>""" % {"index": i})
        	self.response.write('</div></li>')
        	i += 1
        self.response.write('</ul>')
        self.response.write('<script>bettingOpportunities = ' + json.dumps(opportunities) + ';</script>')
        self.response.write("""
        	<script>
        		var totalSumChanged = function(e){
        			var money = parseFloat($(this).val());
        			var index = parseInt($(this).attr('data-index'));
        			var chances = bettingOpportunities[index].chances;

        			var backMoney = money * chances.backPercentage / chances.totalPercentage;
        			var layLiability = money * chances.layPercentage / chances.totalPercentage;

        			var layOdds = new Big(bettingOpportunities[index].layOdds);
        			layOdds = layOdds.div(layOdds.minus(1))
        			var layMoney = layOdds.minus(1).times(layLiability);

        			var winnings = new Big(money).div(new Big(chances.totalPercentage).div(100)).minus(money);
        			$('#win' + index).val(winnings.toFixed(2));
        			$('#back' + index).val(backMoney.toFixed(2));
        			$('#lay' + index).val(layMoney.toFixed(2));
        			$('#liability' + index).val(layLiability.toFixed(2));
        		};
                var backSumChanged = function(e){
                    var backMoney = new Big(parseFloat($(this).val()));
                    var index = parseInt($(this).attr('data-index'));
                    var opportunity = bettingOpportunities[index];
                    var layOdds = new Big(opportunity.layOdds);
                    
                    var backArbPercentage = new Big(opportunity.chances.backPercentage);
                    var layArbPercentage = new Big(opportunity.chances.layPercentage);
                    var totalPercentage = new Big(opportunity.chances.totalPercentage);
                    
                    var backRealRate = backArbPercentage.div(totalPercentage);
                    var layRealRate = layArbPercentage.div(totalPercentage);
                    
                    //formulas:
                    //backRealRate * totalSum = backMoney;
                    //layRealRate * totalSum = layMoney;
                    //so if backMoney changes => totalSum = backMoney / backRealRate and then layMoney = layRealRate * totalSum
                    var totalSum = backMoney.div(backRealRate);
                    layOdds = layOdds.div(layOdds.minus(1))
                    var layLiability = totalSum.times(opportunity.chances.layPercentage / opportunity.chances.totalPercentage);
                    var layMoney = layOdds.minus(1).times(layLiability);
                    var winnings = new Big(totalSum).div(new Big(totalPercentage).div(100)).minus(totalSum);
                    $('#win' + index).val(winnings.toFixed(2));
                    $('#lay' + index).val(layMoney.toFixed(2));
                    $('#liability' + index).val(layLiability.toFixed(2));
                    $('#total' + index).val(totalSum.toFixed(2));
                }
        		$('.moneyInput').keyup(totalSumChanged);
        		$('.moneyInput').val(100).keyup();

                $('.backSuggestedAmount').keyup(backSumChanged);
        	</script>
        """);
        self.response.write('</body></html>')
