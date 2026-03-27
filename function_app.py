import logging
import azure.functions as func
import feedparserAPP as feedparserAPP

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */30 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('12:31Start function  timer trigger function executed.')
    feedparserAPP.main()
    logging.info('12:31End  timer trigger function executed.')