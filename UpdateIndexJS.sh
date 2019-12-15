#!/bin/bash
scp -i Key10.pem index.js ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/index.js
scp -i Key10.pem index.html ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/index.html
scp -i Key10.pem about.ejs ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/views/about.ejs
scp -i Key10.pem contact.ejs ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/views/contact.ejs
scp -i Key10.pem allValues.ejs ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/views/allValues.ejs
scp -i Key10.pem getValues.ejs ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/views/getValues.ejs
scp -i Key10.pem monteCarlo.ejs ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/views/monteCarlo.ejs
scp -i Key10.pem allTickers.ejs ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/views/allTickers.ejs
scp -i Key10.pem hotStocks.ejs ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/views/hotStocks.ejs
scp -i Key10.pem SP500Values.ejs ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/views/SP500Values.ejs
scp -i Key10.pem monteCarlo.ejs ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/views/monteCarlo.ejs
scp -i Key10.pem DowJonesGraph.png ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/pictures/DowJonesGraph.png
scp -i Key10.pem MultipleGraphs.png ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/pictures/MultipleGraphs.png
scp -i Key10.pem SingleGraph.png ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/pictures/SingleGraph.png
scp -i Key10.pem Share.jpg ubuntu@ec2-52-24-193-157.us-west-2.compute.amazonaws.com:~/StockProjectWeb/pictures/Share.jpg
ssh -i Key10.pem ubuntu@52.24.193.157 'cd StockProjectWeb;git add -A;cd views;git add -A;cd;cd StockProjectWeb/pictures;git add -A;git commit -m "Nope";git push heroku master;'
