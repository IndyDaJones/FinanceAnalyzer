
USE services;

CREATE TABLE IF NOT EXISTS `Ticker_Test` ( 
`Index` int(255) NOT NULL AUTO_INCREMENT, 
`Status` varchar(30) NOT NULL, 
`Symbol` varchar(30) NOT NULL COMMENT 'Ticker Symbol', 
`Create_dt` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',  
`Create_by` varchar(255) NOT NULL, 
`Update_dt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
`Update_by` varchar(255) NOT NULL, 
PRIMARY KEY (`index`) 
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;