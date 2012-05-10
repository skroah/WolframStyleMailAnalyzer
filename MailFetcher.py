import ConfigParser
from imaplib import IMAP4_SSL
from datetime import date,timedelta
from pylab import show
import DataPlotter as dp

CONFIG_FILE = "config.ini"
GROUP = "mail"

class MailFetcher(object):
    def __init__(self):
        config = self.parseConfigFile(CONFIG_FILE)
        self.server = self.getValue(config, GROUP, "server")
        self.user_id = self.getValue(config, GROUP, "user_id")
        self.password = self.getValue(config, GROUP, "password")
        
        
    def getHeaders(self, folder, numberOfDays):
        """
            For original source SEE: http://glowingpython.blogspot.it/2012/05/analyzing-your-gmail-with-matplotlib.html
        """
        mail = IMAP4_SSL(self.server)
        mail.login(self.user_id, self.password)
        mail.select(folder)
        # retrieving the uids
        interval = (date.today() - timedelta(numberOfDays)).strftime("%d-%b-%Y")
        result, data = mail.uid('search', None,'(SENTSINCE {date})'.format(date=interval))
        # retrieving the headers
        result, data = mail.uid('fetch', data[0].replace(' ',','),'(BODY[HEADER.FIELDS (DATE)])')
        mail.close()
        mail.logout()
        return data

    def getBodies(self, folder, numberOfDays):
        """

        """
        mail = IMAP4_SSL(self.server)
        mail.login(self.user_id, self.password)
        mail.select(folder)
        # retrieving the uids
        interval = (date.today() - timedelta(numberOfDays)).strftime("%d-%b-%Y")
        result, data = mail.uid('search', None,'(SENTSINCE {date})'.format(date=interval))
        # retrieving the headers
        result, data = mail.uid('fetch', data[0].replace(' ',','),'(BODY[HEADER.FIELDS (DATE)])')
        mail.close()
        mail.logout()
        return data

    def parseConfigFile(self, CONFIG_FILE):
        config = ConfigParser.ConfigParser()
        config.read(CONFIG_FILE)
        return config

    def getValue(self, config, group, key):
        return config.get(group, key)


if __name__ == "__main__":
    print 'Fetching emails...'
    mail  = MailFetcher()
    headers = mail.getHeaders('inbox',5)

    print 'Plotting some statistics...'
    xday,ytime = dp.diurnalPlot(headers)
    dp.dailyDistributioPlot(ytime)
    print len(xday),'Emails analysed.'
    show()