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
        mySql_insert_query = "INSERT INTO Stocks_Day_Test (Status, Symbol, QuoteType, currency, Date, Open, High, Low, Close, AdjClose, Volume, create_dt, create_by, update_by) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        record = ("OK", symbol, quotetype, currency, date, open, high, low, close, adjclose, str(volume), createdate, "sql_connector.persistData","sql_connector.persistData")  
        cursor.execute(mySql_insert_query, record)
        self.connection.commit()
        cursor.close()
        
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
    
    except Exception as error:
        print("Error catched"+ error)