import logging
import azure.functions as func
import feedparserAPP as feedparserAPP

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 0/6 * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('ver 1.1.1_Start function')
    feedparserAPP.main()