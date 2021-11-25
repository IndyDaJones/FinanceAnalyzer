import mysql.connector

class MySQL:
  connection = "NULL"
  
  def connect(self):
    self.connection = mysql.connector.connect(
      host="192.168.34.33",
      user="test",
      password="test_user",
      database='services'
    )
    return self.connection

  def disconnect(self):
    if self.connection.is_connected():
      self.connection.close()
  
  def persistData(self, symbol, quotetype, currency, open, high, low, close, adjclose, volume, date, createdate):
    try:
        cursor = self.connection.cursor()
        # status create_dt create_by update_by
        mySql_insert_query = "INSERT INTO Stocks_Day_Test (Status, Symbol, QuoteType, Currency, Date, Open, High, Low, Close, AdjClose, Volume, Create_dt, Create_by, Update_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        record = ("OK", symbol, quotetype, currency, date, open, high, low, close, adjclose, str(volume), createdate, "sql_connector.persistData","sql_connector.persistData")  
        cursor.execute(mySql_insert_query, record)
        self.connection.commit()
        cursor.close()
        
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    
    except Exception as error:
        print("Error catched"+ error)
    
  def insertTicker(self, symbol, createdate):
    try:
        cursor = self.connection.cursor()
        # status create_dt create_by update_by
        mySql_insert_query = "INSERT INTO Ticker_Test (Status, Symbol, create_dt, create_by, update_by) VALUES (%s, %s, %s, %s, %s)"
        record = ("OK", symbol, createdate, "sql_connector.persistData","sql_connector.persistData")  
        cursor.execute(mySql_insert_query, record)
        self.connection.commit()
        cursor.close()
        
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    
    except Exception as error:
        print("Error catched"+ error)
    
  def removeTicker(self, symbol):
    try:
        cursor = self.connection.cursor()
        # status create_dt create_by update_by
        mySql_remove_query = "DELETE FROM Ticker_Test WHERE Symbol = '"+symbol+"'"
        cursor.execute(mySql_remove_query)
        self.connection.commit()
        cursor.close()
        
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    
    except Exception as error:
        print("Error catched"+ error)

  def showTicker(self):
    try:
        cursor = self.connection.cursor()
        # status create_dt create_by update_by
        result = mySql_show_query = "SELECT Status, Symbol, create_dt, create_by, update_dt, update_by FROM Ticker_Test ORDER BY Symbol"
        cursor.execute(mySql_show_query)
        
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)

        print("\nStatus \tSymbol \tCreate_dt \tCreate_by \tUpdate_dt \tUpdate_by")
        for row in records:
            print(str(row[0])+"\t"+str(row[1])+"\t"+str(row[2])+"\t"+str(row[3])+"\t"+str(row[4])+"\t"+str(row[5]))
        cursor.close()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    
    except Exception as error:
        print("Error catched"+ error)

  def updateSignal(self, date, signal):
    try:
        cursor = self.connection.cursor()
        # status create_dt create_by update_by
        mySql_update_query = "UPDATE `services`.`Stocks_Day_Test` SET Recommendation = '"+signal+"' WHERE Date = '"+date.strftime('%Y-%m-%d')+"' and Recommendation <> '"+signal+"'"
        #params = (signal, date.strftime('%Y-%m-%d %H:%M:%S'))
        #
        print(mySql_update_query)
        cursor.execute(mySql_update_query)
        print("affected rows = {}".format(cursor.rowcount))
        self.connection.commit()
        cursor.close()
        
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    
    except Exception as error:
        print("Error catched"+ error)

  def updateTicker(self, symbolOld, SymbolNew):
    try:
        cursor = self.connection.cursor()
        # status create_dt create_by update_by
        mySql_update_query = "UPDATE Ticker_Test SET Symbol = '"+SymbolNew+"' WHERE Symbol = '"+symbolOld+"'"
        cursor.execute(mySql_update_query)
        self.connection.commit()
        cursor.close()
        
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    
    except Exception as error:
        print("Error catched"+ error)
        
  def loadTicker(self):
        try:
            cursor = self.connection.cursor()
            # status create_dt create_by update_by
            mySql_load_query = "SELECT Symbol FROM Ticker_Test WHERE Status = 'OK' ORDER BY Symbol"
            cursor.execute(mySql_load_query)
            
            records = cursor.fetchall()
            
            #symbols = {'SPICHA.SW','SPMCHA.SW','WZEC.F','ROG.SW','NOW','CSL.AX','USSRS.SW', 'CL:NMX', 'NYSE:GOLD'} 
            tickers = {}
            tickers = set()
            for row in records:
                tickers.add(str(row[0]))            
            cursor.close()

            return tickers

        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        
        except Exception as error:
            print("Error catched"+ error)

  def loadTickerData(self, stock, columnname):
        try:
            cursor = self.connection.cursor()
            # status create_dt create_by update_by
            mySql_load_query = "SELECT Date, "+columnname+" FROM Stocks_Day_Test WHERE Symbol = '"+stock+"' ORDER BY Date ASC"
            print(mySql_load_query)
            cursor.execute(mySql_load_query)
            
            records = cursor.fetchall()
            
            #symbols = {'SPICHA.SW','SPMCHA.SW','WZEC.F','ROG.SW','NOW','CSL.AX','USSRS.SW', 'CL:NMX', 'NYSE:GOLD'} 
            result = {}
            result = dict()
            for row in records:
                result[str(row[0])] = str(row[1])
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        
        except Exception as error:
            print("Error catched"+ error)