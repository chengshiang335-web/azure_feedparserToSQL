import logging
import azure.functions as func
import sql_server.db_service
import feedparserAPP

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */1 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def AzureTirggerToSQL(myTimer: func.TimerRequest) -> None:
    logging.info("version: 2024-06-17 15:00 - Azure Timer Triggered")
    feedparserAPP.main()  # 執行 feedparserAPP.py 中的主程式，抓取 RSS 並寫入 SQL Server
   

    if myTimer.past_due:
      logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')