from django_cron import CronJobBase, Schedule


class AmazonCookieCatchCron(CronJobBase):
    RUN_EVERY_TWO_HOUR = 1  # every 2 hours

    # schedule = Schedule(run_every_mins=RUN_EVERY_TWO_HOUR)
    # code = 'amazon_cookie_catch_cron'  # a unique code

    def do(self):

        print "blqlqlqlq"

        pass  # do your thing here

    print "maiko"