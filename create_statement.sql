-- Timestamp,Open,High,Low,Close,Volume_BTC,Volume_Currency,Weighted_Price
-- Date       High         Low        Open       Close     Volume   Adj Close

USE services;

CREATE TABLE IF NOT EXISTS `services`.`Stocks_Day_Test` ( 
`Index` int(255) NOT NULL AUTO_INCREMENT, 
`Status` varchar(30) NOT NULL DEFAULT 'OK', 
`Recommendation` varchar(30) NOT NULL DEFAULT 'NO',
`Symbol` varchar(30) NOT NULL COMMENT 'Ticker Symbol', 
`QuoteType` varchar(255) NULL COMMENT 'ETF / EQUITY', 
`Currency` varchar(30) NOT NULL COMMENT 'Currency', 
`Date` date NOT NULL DEFAULT '0000-00-00', 
`Open` double DEFAULT NULL COMMENT 'Open', 
`High` double DEFAULT NULL COMMENT 'High', 
`Low` double DEFAULT NULL COMMENT 'Low', 
`Close` double DEFAULT NULL COMMENT 'Close', 
`AdjClose` double DEFAULT NULL COMMENT 'AdjClose', 
`Volume` double DEFAULT NULL COMMENT 'Volume', 
`Create_dt` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',  
`Create_by` varchar(255) NOT NULL, 
`Update_dt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
`Update_by` varchar(255) NOT NULL, 
PRIMARY KEY (`Index`) 
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

INSERT INTO `services`.`Stocks_Day_Test` (Status, Symbol, QuoteType, Currency, Date, Open, High, Low, Close, AdjClose, Volume, Create_dt, Create_by, Update_by) VALUES ('OK', '"+symbol+"', '"+quotetype+"', '"+currency+"', '"+date.strftime('%Y-%m-%d')+"', '"+open+"','"+high+"', '"+low+"', '"+close+"', '"+adjclose+"', '"+str(volume)+"', '"+createdate.strftime('%Y-%m-%d %H:%M:%S')+"', 'sql_connector.persistData','sql_connector.persistData') WHERE NOT EXISTS (SELECT * FROM `services`.`Stocks_Day_Test` WHERE `Status`='OK' AND `Symbol`='"+symbol+"' AND `QuoteType`='"+quotetype+"' AND `Currency`='"+currency+"' AND `Date`='"+date.strftime('%Y-%m-%d')+"' AND `Open`='"+open+"' AND `High`='"+high+"' AND `Low`='"+low+"' AND `Close`='"+close+"' AND `AdjClose`='"+adjclose+"' AND `Volume`='"+str(volume)+"' LIMIT 1)

INSERT INTO `services`.`Stocks_Day_Test` (Status, Symbol, QuoteType, Currency, Date, Open, High, Low, Close, AdjClose, Volume, Create_dt, Create_by, Update_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) WHERE NOT EXISTS (SELECT * FROM `services`.`Stocks_Day_Test` WHERE Status= %s AND Symbol=%s AND QuoteType=%s AND Currency=%s AND Date=%s AND Open=%s AND High=%s AND Low=%s AND Close=%s AND AdjClose=%s AND Volume=%s LIMIT 1)

INSERT INTO Stocks_Day_Test (Status, Symbol, QuoteType, Currency, Date, Open, High, Low, Close, AdjClose, Volume, Create_dt, Create_by, Update_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

UPDATE `services`.`Stocks_Day_Test` SET Recommendation = '"+signal+"' WHERE Date = '"+date.strftime('%Y-%m-%d')+"' and Recommendation <> '"+signal+"'


INSERT INTO `services`.`Stocks_Day_Test` (Status, Symbol, QuoteType, Currency, Date, Open, High, Low, Close, AdjClose, Volume, Create_dt, Create_by, Update_by) SELECT 'OK', '"+symbol+"', '"+quotetype+"', '"+currency+"', '"+date.strftime('%Y-%m-%d')+"', '"+open+"','"+high+"', '"+low+"', '"+close+"', '"+adjclose+"', '"+str(volume)+"', '"+createdate.strftime('%Y-%m-%d %H:%M:%S')+"', 'sql_connector.persistData','sql_connector.persistData' FROM DUAL WHERE NOT EXISTS (SELECT * FROM `services`.`Stocks_Day_Test` WHERE `Status`='OK' AND `Symbol`='"+symbol+"' AND `QuoteType`='"+quotetype+"' AND `Currency`='"+currency+"' AND `Date`='"+date.strftime('%Y-%m-%d')+"' AND `Open`='"+open+"' AND `High`='"+high+"' AND `Low`='"+low+"' AND `Close`='"+close+"' AND `AdjClose`='"+adjclose+"' AND `Volume`='"+str(volume)+"' LIMIT 1) 

SELECT * FROM `services`.`Stocks_Day_Test` 
 WHERE Symbol='ROG.SW'  
   AND QuoteType='EQUITY' 
   AND Currency='USD' 
   AND Date='2021-01-04' 
   AND Open=312.54998779296875 
   AND High=312.70001220703125 
   AND Low=308.04998779296875 
   AND Close=309.6000061035156 
   AND AdjClose=300.54095458984375 
   AND Volume='1643089.0' LIMIT 1

 , , , '1643089.0'