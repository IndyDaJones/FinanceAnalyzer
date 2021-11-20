-- Timestamp,Open,High,Low,Close,Volume_BTC,Volume_Currency,Weighted_Price
-- Date       High         Low        Open       Close     Volume   Adj Close

USE services;

CREATE TABLE IF NOT EXISTS `Stocks_Day_Test` ( 
`index` int(255) NOT NULL AUTO_INCREMENT, 
`status` varchar(30) NOT NULL, 
`Symbol` varchar(30) NOT NULL COMMENT 'Ticker Symbol', 
`QuoteType` varchar(255) NULL COMMENT 'ETF / EQUITY', 
`currency` varchar(30) NOT NULL COMMENT 'Currency', 
`Date` date NOT NULL DEFAULT '0000-00-00', 
`Open` double DEFAULT NULL COMMENT 'Open', 
`High` double DEFAULT NULL COMMENT 'High', 
`Low` double DEFAULT NULL COMMENT 'Low', 
`Close` double DEFAULT NULL COMMENT 'Close', 
`AdjClose` double DEFAULT NULL COMMENT 'AdjClose', 
`Volume` double DEFAULT NULL COMMENT 'Volume', 
`create_dt` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',  
`create_by` varchar(255) NOT NULL, 
`update_dt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
`update_by` varchar(255) NOT NULL, 
PRIMARY KEY (`index`) 
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;