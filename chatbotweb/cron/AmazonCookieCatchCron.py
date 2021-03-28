from django_cron import CronJobBase, Schedule

class AmazonCookieCatchCron(CronJobBase):
    RUN_EVERY_TWO_HOUR = 120 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_TWO_HOUR)
    code = 'chatbotweb.cron.AmazonCookieCatchCron'    # a unique code

    def do(self):

        print "qko"

        pass    # do your thing here