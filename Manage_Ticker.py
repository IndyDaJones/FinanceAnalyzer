import logger as logger
from sql_connector import MySQL
import datetime as dt

def main():
    while True:
        user_input = input("Please define you operation: (Insert, Change, Remove, Show) ['exit' to stop]\n")
        if user_input == "exit":
                    logger.info("Break")
                    break

        if user_input == "Insert":
            while True:
                user_input = input("Please enter the new Ticker: [(]'exit' to stop]\n")
                logger.info("Input from user:")
                if user_input == "exit":
                    logger.info("Break")
                    break
                try:
                    data = MySQL()
                    data.connect()
                    logger.info("New Ticker inserted: "+str(user_input))    
                    end = dt.datetime.now()
                    data.insertTicker(user_input,end)
                    break
                except Exception as err:
                    logger.error("Exception cauth"+str(err))
                    print(f"Unexpected {err=}, {type(err)=}")
                    raise err
        elif user_input == "Change":
            while True:
                symbolOld = input("Please enter the Ticker to be changed: ['exit' to stop]\n")
                if user_input == "exit":
                    logger.info("Break")
                    break
                logger.info("Input from user:")
                symbolNew = input("Please enter the new Ticker: ['exit' to stop]\n")
                if user_input == "exit":
                    logger.info("Break")
                    break
                try:
                    data = MySQL()
                    data.connect()
                    logger.info("Ticker removed: "+str(user_input))    
                    end = dt.datetime.now()
                    data.updateTicker(symbolOld,symbolNew)
                    break
                except Exception as err:
                    logger.error("Exception cauth"+str(err))
                    print(f"Unexpected {err=}, {type(err)=}")
                    raise err
        elif user_input == "Remove":
            while True:
                user_input = input("Please enter the Ticker to be removed: ['exit' to stop]\n")
                logger.info("Input from user:")
                if user_input == "exit":
                    logger.info("Break")
                    break
                try:
                    data = MySQL()
                    data.connect()
                    logger.info("Ticker removed: "+str(user_input))    
                    end = dt.datetime.now()
                    data.removeTicker(user_input)
                    break
                except Exception as err:
                    logger.error("Exception cauth"+str(err))
                    print(f"Unexpected {err=}, {type(err)=}")
                    raise err
        if user_input == "Show":
            try:
                data = MySQL()
                data.connect()
                logger.info("Ticker removed: "+str(user_input))    
                end = dt.datetime.now()
                data.showTicker()
            except Exception as err:
                logger.error("Exception cauth"+str(err))
                print(f"Unexpected {err=}, {type(err)=}")
                raise err

#Main function
if __name__ == "__main__":
    main()